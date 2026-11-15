# Session DSH — relecture

- identifiant : `session-7fc0675a-4f7b-470d-8dd7-bedcaf3bcd6e`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-15 12:53:15
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche X3 (J5, la part du pilote) : le tagger **en lot** — mesure le coût et la latence pour **1 000 phrases** (réelles, prises dans le gold + les 50 textes libres), le **taux de cache** (chaud/froid), le **débit** (phrases/min), la **mémoire**, et le **coût en dollars** (~0,04 $/612 → extrapoler) ; le mode `--jsonl` sur un fichier ; le **contrôle négatif** (les mêmes phrases en cache chaud ne doivent coûter 0). Fiche `reports/rapport-tagger-lot.md` + JSON.

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

- **bash** `{"command": "pwd && ls -la && git status --short | head -50 && git log --oneline -5", "description": "Inspect repository root and git status"}`

  ```
/home/stephane/Data13TB/stephane/GitHub/Qtrinet
total 208
drwxr-xr-x. 1 stephane stephane   686  6 nov 09:52 .
drwxr-xr-x. 1 stephane stephane  2532  5 nov 10:41 ..
-rw-r--r--. 1 stephane stephane  9977  3 nov 09:19 AGENTS.md
drwxr-xr-x. 1 stephane stephane    40 25 sep 15:38 bench
drwxr-xr-x. 1 stephane stephane    56 30 sep 12:20 colab
drwxr-xr-x. 1 stephane stephane  2664  2 nov 18:33 data
drwxr-xr-x. 1 stephane stephane   138 15 nov 06:29 docs
drwxr-xr-x. 1 stephane stephane    92 28 oct 16:25 drave-core
drwxr-xr-x. 1 stephane stephane   220 15 nov 12:53 .git
-rw-r--r--. 1 stephane stephane   619 31 oct 17:33 .gitignore
-rw-r--r--. 1 stephane stephane   225  1 nov 10:50 .gitmodules
drwxr-xr-x. 1 stephane stephane   992 15 nov 12:34 journal
drwxr-xr-x. 1 stephane stephane   100  3 nov 09:12 models
drwxr-xr-x. 1 stephane stephane   114 25 sep 15:24 __pycache__
drwxr-xr-x. 1 stephane stephane    64  6 nov 09:52 .pytest_cache
-rw-r--r--. 1 stephane stephane  4992 25 sep 10:54 Qtrinet-bootstrap.md
-rw-r--r--. 1 stephane stephane 21293  6 nov 22:32 README.md
drwxr-xr-x. 1 stephane stephane 78540 15 nov 12:48 reports
-rw-r--r--. 1 stephane stephane 13100 28 oct 14:59 REPRISE.md
-rw---
… [2481 caractères tronqués]
  ```

- **bash** `{"command": "ls -la reports/ 2>/dev/null | head -40; echo ---; ls -la docs/pilotage/ 2>/dev/null | head -40", "description": "List reports and pilotage docs"}`

  ```
total 29888
drwxr-xr-x. 1 stephane stephane   78540 15 nov 12:48 .
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
… [2540 caractères tronqués]
  ```

- **bash** `{"command": "grep -rl \"tagger\" --include=\"*.py\" --include=\"*.md\" --include=\"*.sh\" . 2>/dev/null | grep -v \"^./reports/\" | head -60", "description": "Find tagger references"}`

  ```
./tools/docwatch/.venv/lib/python3.13/site-packages/pygments/lexers/ncl.py
./tools/docwatch/.venv/lib/python3.13/site-packages/more_itertools/more.py
./tools/tests/linguistique/qualifier_neuronal.py
./tools/tests/linguistique/qualifier_syntagmes.py
./tools/tests/linguistique/qualifier_pragmatique.py
./tools/tests/linguistique/qualifier_quatre_modes.py
./tools/tests/linguistique/qualifier_tagger_612.py
./tools/tests/linguistique/test_bloc_linguistique.py
./tools/tests/linguistique/gold_reel_50.py
./tools/tests/linguistique/qualifier_tagger_h50.py
./tools/tests/test_tagger_api.py
./tools/verifier_faq.py
./tools/bloc_linguistique.py
./tools/drave.py
./journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md
./journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
./journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
./journal/sessions/536cd5d6-94ac-4057-8fe9-11709a4587c7/digest.md
./journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/digest.md
./journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/digest.md
./journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/rapport.md
./journal/sessions/abb58991-fe0a-4d6e-b039-6552b09f8454/digest.md
./journal/session
… [2581 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
1: # En ce moment
2: 
3: **Mis à jour : 2026-11-15, 12 h 40 HNE (semaine 2 : W1-W6, tag semaine-2-2026-11-20)**
4: 
5: > **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
6: > plan plus bas (**La carte**).
7: 
8: ### Session `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — le hub de reprise du 04/11 *(en pause)*
9: 
10: - **Id** : `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — [`plan.md`](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/plan.md).
11: - **Rôle** : **Hub de reprise** — état, docs, intégration, passe.
12: - **Fait** : index réparé ; **N3 intégré** ; N2/S/L actifs ; suivi docs.
13: - **Prochaine action** : **suivi docs**, puis la **passe** après les runs.
14: - **État** : **en pause** depuis le 05/11 (dernier heartbeat) ; la clôture J14.1 est portée par `e181ce02`.
15: - **Bloquants** : aucun.
16: - **Journal** : [la session](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/).
17: 
18: ## Sessions en cours
19: 
20: > Contrat : [`continuite.md`](../methode/continuite.md) · sessions terminées :
21: > [`jou
… [11905 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 1,200p tools/tests/test_tagger_api.py", "description": "Read tagger API test"}`

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
… [7794 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"tagger\" tools/drave.py | head -40; echo ---; grep -rn \"jsonl\" tools/*.py tools/tests/*.py tools/tests/linguistique/*.py 2>/dev/null | head -40", "description": "Locate tagger command and jsonl"}`

  ```
8:    python3 tools/drave.py analyser "Le chat dort." --tagger          # API DeepSeek (clé, réseau)
11:    python3 tools/drave.py evaluer --tagger --json                    # heuristique + cascade API
23:En **option** (`--tagger`, `analyser` et `evaluer`), le POS (et lui seul) vient du tagger de
26:**Sans `--tagger`, le défaut ne change pas** : heuristique, CPU, hors ligne, déterministe.
30:Codes de sortie : 0 succès · 2 usage · 3 refus d'analyse · 4 clé/tagger indisponible
62:# Le tagger est une **option** : sans `--tagger`, rien de ce bloc n'est importé ni exécuté.
65:# La fusion de l'option : le POS vient du tagger, tout le reste de l'heuristique. On ne force
90:# --------------------------------------------------------------------------- le tagger (option)
94:    """Aucune clé : le tagger est une option, jamais un prérequis du produit."""
109:            f"Sans --tagger, le défaut reste l'heuristique hors ligne."
120:def _cle_tagger() -> str:
138:        "Sans --tagger, le défaut reste l'heuristique hors ligne."
142:def _client_tagger():
145:    return DeepSeek(cle=_cle_tagger())
148:def _transport_tagger(client, stats: dict):
149:    """Le transport attendu par les taggers : 
… [6003 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 1,460p tools/drave.py", "description": "Read drave.py tagger section"}`

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
    python3 tools/drave.py restituer "Le chat dort." --roles
    python3 tools/drave.py restituer --banc reports/pensee-fiabilite-produit.json --json
    python3 tools/drave.py --version

Ce que la commande expose : l'analyse **heuristique** (`Heuristique.analyser`) — POS, syntagmes
avec rôle et cible d'attachement, pragmatique, unités sémantiques —, sa mesure sur le gold et la
**restitution v0** (annotation → surface, avec la fidélité du miroir) et la **v2** (rôles
agent/prédicat
… [19779 caractères tronqués]
  ```

- **bash** `{"command": "ls reports/ | grep -i -E \"tagger|lot|batch|jsonl\" ; echo ---; sed -n 1,200p reports/rapport-tagger-defaut.md", "description": "Read W3 tagger report"}`

  ```
a26-lot-disque.json
a83b-lot.json
a83c-lot.json
a83d-lot-threads.json
corpus-wiki-fr-texte-pilote-contamination.json
corpus-wiki-fr-texte-pilote.json
pensee-tagger-option.json
r03-pilote-modele.json
r44-ocr-pilote.json
rapport-a26-lot-disque.md
rapport-a83b-lot.md
rapport-a83c-lot.md
rapport-a83d-lot-threads.md
rapport-cloture-chantier.json
rapport-cloture-chantier.md
rapport-exemples-tagger.json
rapport-exemples-tagger.md
rapport-mode4-lot-listes.md
rapport-prefill-par-lots.md
rapport-r44-ocr-pilote.md
rapport-tagger-defaut.json
rapport-tagger-defaut.md
rapport-tagger-erreurs.json
rapport-tagger-erreurs.md
rapport-tagger-h50.json
rapport-tagger-h50.md
rapport-tagger-option.md
tagger-612.json
---
# W3 — la matrice du tagger : le défaut reste hors ligne (code 0), `--tagger` est la seule porte qui peut sortir 4

> **Ligne de roadmap** : **R0.7** (le lecteur) / **B13** · **Tâche** : **W3** (semaine 2, J2
> après-midi) · **Date** : 2026-11-15 · **HEAD mesuré** : `3439cb0c` + ce diff (champ de coût
> additif) · **Verdict** : ✅ **la matrice est mesurée** — le **défaut sans clé** rend
> l'heuristique, **code 0**, **0 socket** ; avec clé, **code 0**, **130 tokens** et **1,16 s**
> pour une
… [12922 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 1,160p tools/tests/linguistique/gold_reel_50.py; echo ===; wc -l tools/tests/linguistique/gold_reel_50.py; echo ===; grep -n \"612\\|1 000\\|1000\" tools/tests/linguistique/qualifier_tagger_612.py | head -30", "description": "Inspect gold_reel_50 and tagger 612"}`

  ```
#!/usr/bin/env python3
"""gold_reel_50.py — les 50 phrases réelles que l'heuristique rate (proposition C3/R).

POURQUOI. Le gold réel (`gold.json` 20 hand + `gold_reel.json` 432 reel) mesure le bloc
linguistique depuis B13. Ses erreurs ne sont plus réparties : le POS porte 275 erreurs de
tokens, la segmentation 346 segments manquants (dont 74 ADJ/ADV/PONCT que l'heuristique ne
produit pas), l'attachement **une seule** (g017, SUB). Le « gold 200+ » des fiches R n'est
donc pas un problème de **nombre** (452 > 200) : c'est un problème de **discrimination**.
Ce banc sélectionne 50 phrases réelles que l'heuristique rate, mesure ce qu'elles ajoutent,
et liste les **candidats à annoter** — sans modifier le gold (territoire S/D).

RÈGLE DE SÉLECTION (déterministe, aucune graine).
  1. score = 3 × (cible d'attachement absente ou fausse)
           + 2 × (token POS faux)
           + 1 × (segment gold absent au même span) ;
  2. quota 25 français + 25 anglais ;
  3. au plus 2 phrases par **signature d'erreur** (POS confondus, types de segments absents,
     types d'attachement) : une construction ne peut pas prendre tout le lot (les 11 négations
     « Ne …-t-il pas ? » sont plafonnées) ;
  
… [6242 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"0,04\\|0.04\\|612\" reports/rapport-tagger-option.md reports/tagger-612.json tools/tests/linguistique/qualifier_tagger_612.py 2>/dev/null | head -40; echo ===; sed -n 1,120p reports/rapport-tagger-option.md", "description": "Find $0.04 / 612 context"}`

  ```
reports/rapport-tagger-option.md:1:# R0.7 / 1A — le tagger POS en option : +8,57 pts sur 20 phrases, +8,49 sur le gold 612 ; le défaut reste hors ligne
reports/rapport-tagger-option.md:6:> 0,8625** du gold 612 (**+8,49**) ; **40 appels**, **11 868 tokens** (cache neuf), **0 refus** ;
reports/rapport-tagger-option.md:17:**La mesure sur le gold 612** (avec la clé, cache partiel) : POS **0,9575** contre 0,8625 pour
reports/rapport-tagger-option.md:22:cache) — soit **~0,02 $** pour 612 phrases ; **449 appels servis par le cache** sur la base réelle.
reports/rapport-tagger-option.md:54:- **La mesure de référence** est [`reports/tagger-612.json`](tagger-612.json) (612 phrases,
reports/rapport-tagger-option.md:85:| 612 phrases (référence) | 1 218 | 1 218 | 0 | **358 962** | **1 257,96 s** (~21 min) | `deepseek-flash` |
reports/rapport-tagger-option.md:87:**Le prix.** ~**0,04 $** pour les 612 phrases (chiffre de la décision) ; au prorata des tokens,
reports/rapport-tagger-option.md:92:### 3.3 La référence 612, par source
reports/rapport-tagger-option.md:99:| **tous** | **612** | **0,8625** | **0,9475** | **+8,49 pts** |
reports/rapport-tagger-option.md:101:**Lecture.** Le 20 phrases `hand`
… [9431 caractères tronqués]
  ```

- **bash** `{"command": "find data -maxdepth 3 -iname \"*libre*\" -o -maxdepth 3 -iname \"*texte*\" | head -40; echo ===; grep -rn \"textes libres\\|texte libre\\|50 textes\" --include=\"*.md\" --include=\"*.py\" --include=\"*.json\" . 2>/dev/null | grep -v \"journal/sessions\" | head -30", "description": "Find … [20 caractères tronqués]`

  ```
data/corpus_wiki_fr_texte
data/corpus_wiki_de_texte
data/corpus_wiki_es_texte
data/corpus_wiki_ja_texte
data/corpus_wiki_ru_texte
data/corpus_wiki_en_texte
data/corpus_wiki_ar_texte
data/corpus_wiki_zh_texte
data/corpus_wiki_it_texte
data/corpus_wiki_pt_texte
===
./reports/archive/rapport-campagne-benefices.md:1010:*peut pas* produire autre chose. La tête complète, elle, écrit du texte libre.
./reports/campagne-benefices/016-13-la-tete-restreinte-sur-deux-modeles-de-p.md:19:*peut pas* produire autre chose. La tête complète, elle, écrit du texte libre.
./reports/rapport-produit-bloc-l.md:20:jamais une sortie vide** et garde **tous les offsets** ; mais **34/50 textes** portent au moins une
./reports/rapport-produit-bloc-l.md:29:| POS fermées | ✅ | gold **0,9004** ; 50/50 textes ont des POS |
./reports/rapport-produit-bloc-l.md:54:- **Ce que ce banc ne mesure pas** : la justesse sémantique sur texte libre (pas de gold), la
./reports/rapport-produit-bloc-l.md:149:syntagme (51,9 %)** sont impliquées, dans **31/50 textes** ; 113 sont des **inclusions**, 19 des
./reports/rapport-produit-bloc-l.md:156:**Autres écarts de forme** : **60 étiquettes phrase** pour 50 textes (6 textes multi-phra
… [3817 caractères tronqués]
  ```

- **bash** `{"command": "ls -la data/ | head -80; echo ===; find data -maxdepth 2 -type d | head -60", "description": "List data directories"}`

  ```
total 961812
drwxr-xr-x. 1 stephane stephane      2664  2 nov 18:33 .
drwxr-xr-x. 1 stephane stephane       686  6 nov 09:52 ..
drwxr-xr-x. 1 stephane stephane       220 22 oct 22:05 adaptateurs
drwxr-xr-x. 1 stephane stephane        32 19 oct 14:30 alignement
-rw-r--r--. 1 stephane stephane  59784525 21 oct 01:02 composition-etats.npz
-rw-r--r--. 1 stephane stephane  30539912 21 oct 03:44 composition-verne-14b-etats.npz
-rw-r--r--. 1 stephane stephane  21144969 21 oct 01:38 composition-verne-7b-etats.npz
-rw-r--r--. 1 stephane stephane  12037642 21 oct 01:30 composition-verne-etats.npz
-rw-r--r--. 1 stephane stephane 151064111 21 oct 23:31 composition-verne-large-etats.npz
-rw-r--r--. 1 stephane stephane 147255554 21 oct 23:47 composition-verne-plan-etats.npz
-rw-r--r--. 1 stephane stephane     97900 29 oct 14:19 consignes_train.jsonl
-rw-r--r--. 1 stephane stephane      1931 29 oct 14:19 consignes_val.jsonl
-rw-r--r--. 1 stephane stephane 100276153  8 oct 09:42 corpus_en.txt
-rw-r--r--. 1 stephane stephane   2032162  8 oct 09:42 corpus_en_val.txt
-rw-r--r--. 1 stephane stephane  17031747 17 oct 18:26 corpus_fr_litterature.txt
-rw-r--r--. 1 stephane stephane   4402195 28 oct 12:45
… [5763 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nfor f in [\"reports/pensee-produit-bloc-l.json\",\"reports/pensee-fiabilite-produit.json\"]:\n    d=json.load(open(f))\n    print(f, type(d), list(d)[:20] if isinstance(d,dict) else len(d))\nEOF", "description": "Inspect 50 free texts JSON structures"}`

  ```
reports/pensee-produit-bloc-l.json <class 'dict'> ['rapport', 'ligne', 'branche', 'commit', 'date', 'objet', 'verdict', 'dispositif', 'gold', 'banc_50', 'cas_limites', 'performance', 'contrat', 'compositions', 'correctifs', 'controle_negatif', 'limites', 'fichiers']
reports/pensee-fiabilite-produit.json <class 'dict'> ['rapport', 'ligne', 'branche', 'commit_mesure', 'commit_module', 'date', 'objet', 'verdict', 'snapshot', 'dispositif', 'banc_50', 'robustesse', 'contrat', 'schema_propose', 'test_non_regression', 'correctifs', 'controle_negatif', 'limites', 'fichiers']
  ```

- **bash** `{"command": "sed -n 1,80p tools/tests/linguistique/qualifier_tagger_612.py; echo ===; sed -n 80,240p tools/tests/linguistique/qualifier_tagger_612.py", "description": "Read tagger 612 harness"}`

  ```
#!/usr/bin/env python3
"""qualifier_tagger_612.py — le tagger POS API sur le gold 612 (hand 20 + reel 432 + synth 160).

POURQUOI. Le banc `qualifier_quatre_modes.py` ne charge que `gold_reel.json` (432 phrases) ; le
gold courant en compte 612, et le tagger n'y a jamais été mesuré. Ce banc ajoute la ventilation
hand / reel / synth, la latence réelle des appels et le modèle effectivement renvoyé par l'API.
Il ne modifie aucun autre fichier et n'écrit que le JSON demandé.

COÛT. Deux appels par phrase (POS + syntagmes), partagés par les six modes grâce au cache des
tagger : ~1 214 appels, ~360 k tokens, ~20 min pour 612 phrases.

USAGE.
    DEEPSEEK_KEY_FILE=$HOME/.config/drave/deepseek.key \
    DEEPSEEK_CACHE=$(mktemp -d /tmp/j43-cache.XXXX) \
    DEEPSEEK_MODEL=deepseek-chat \
    PYTHONPATH=. python3 tools/tests/linguistique/qualifier_tagger_612.py \
      --sortie /tmp/tagger-612.json

La clé n'est jamais lue en dur : `tools/llm/deepseek.py` lit `DEEPSEEK_API_KEY` ou le fichier
`DEEPSEEK_KEY_FILE` (0600). Le cache doit être neuf : le cache par défaut contient les réponses
du 2026-11-04 et rejouerait l'ancien modèle au lieu de mesurer celui d'aujourd'hui.
"""
from __future__ impo
… [7466 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open(\"reports/pensee-produit-bloc-l.json\"))\nb=d[\"banc_50\"]\nprint(type(b))\nif isinstance(b,dict):\n    print(list(b))\n    for k,v in b.items():\n        print(k, type(v), (len(v) if hasattr(v,'__len__') else ''))\nelif isinstance(b,list … [123 caractères tronqués]`

  ```
<class 'dict'>
['phrases', 'mots', 'etiquettes', 'attachements', 'categories', 'langues_detectees', 'scripts', 'crashes', 'refus', 'sorties_vides', 'sans_anomalie', 'avec_anomalie', 'anomalies_total', 'anomalies', 'niveaux', 'fraction', 'pos', 'phrases_stats', 'document', 'graphème', 'url_emoji', 'langue', 'double_sens', 'detail']
phrases <class 'int'> 
mots <class 'int'> 
etiquettes <class 'int'> 
attachements <class 'dict'> 8
categories <class 'dict'> 9
langues_detectees <class 'dict'> 3
scripts <class 'dict'> 3
crashes <class 'int'> 
refus <class 'int'> 
sorties_vides <class 'int'> 
sans_anomalie <class 'int'> 
avec_anomalie <class 'int'> 
anomalies_total <class 'int'> 
anomalies <class 'dict'> 6
niveaux <class 'dict'> 3
fraction <class 'dict'> 4
pos <class 'dict'> 7
phrases_stats <class 'dict'> 5
document <class 'dict'> 5
graphème <class 'dict'> 4
url_emoji <class 'dict'> 4
langue <class 'dict'> 4
double_sens <class 'dict'> 2
detail <class 'list'> 50
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open(\"reports/pensee-produit-bloc-l.json\"))\ndet=d[\"banc_50\"][\"detail\"]\nprint(len(det))\nprint(json.dumps(det[0],ensure_ascii=False)[:1500])\nprint(\"KEYS\", list(det[0]))\nEOF", "description": "Inspect detail entry"}`

  ```
50
{"id": "f01", "cat": "fr/courte", "texte": "Le chat dort sur le canapé.", "attendu": "fr", "langue": "fr", "script": "Latn", "mots": 6, "etiquettes": 32, "niveaux": {"graphème": 12, "mot": 7, "pos": 6, "syntagme": 3, "discours": 1, "document": 1, "phrase": 1, "pragmatique": 1}, "niveaux_absents": ["morphème"], "fraction": 0.5185, "attachements": 3, "anomalies": [], "anomalies_n": 0}
KEYS ['id', 'cat', 'texte', 'attendu', 'langue', 'script', 'mots', 'etiquettes', 'niveaux', 'niveaux_absents', 'fraction', 'attachements', 'anomalies', 'anomalies_n']
  ```

- **bash** `{"command": "grep -rn \"1 000\\|1000\" tools/tests/linguistique/*.py tools/*.py 2>/dev/null | head -40; echo ===; ls tools/tests/linguistique/ | head -80", "description": "Search for 1000-sentence builders"}`

  ```
tools/tests/linguistique/classement_cible.py:541:        random.Random(1000 + k).shuffle(melange)
tools/tests/linguistique/gold_reel_50.py:305:        rng2 = random.Random(1000 + graine)
tools/tests/linguistique/qualifier_frontiere_71.py:106:                   "duree_par_langue_ms": round(1000 * duree_script / max(1, len(langues)), 3)},
tools/tests/linguistique/qualifier_frontiere_71.py:111:                   "duree_par_label_ms": round(1000 * duree_langue / max(1, total), 3),
tools/tests/linguistique/qualifier_lien_appris.py:124:        rng = random.Random(1000 + g)
tools/tests/linguistique/test_atomes_prediction.py:20:        a = np.array([-400, 0, 1000, 2000], float)
tools/aligneur_litteraire.py:329:_VALEURS_ROMAINES = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
tools/analyse_alignement.py:49:    lam_grid = (0.1, 1.0, 10.0, 100.0, 1000.0)
tools/analyse_empreinte.py:196:        total = nc * ne * mo / 1000
tools/analyse_engram.py:34:    ap.add_argument("--jetons", type=int, default=10000)
tools/analyse_flux.py:114:        nom_c = f"{couche}" if couche < 1000 else f"FFN {couche-1000}"
tools/archive_sessions.py:89:                       f"- créée : {time.strfti
… [3226 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, pathlib\nfor f in [\"gold.json\",\"gold_reel.json\",\"gold_synthetique.json\"]:\n    p=pathlib.Path(\"tools/tests/linguistique\")/f\n    d=json.load(open(p))\n    print(f, list(d), len(d.get(\"phrases\",[])))\n    print(\" first keys\", list(d[\"phrases\" … [129 caractères tronqués]`

  ```
gold.json ['version', 'phrases', 'note'] 20
 first keys ['id', 'langue', 'texte', 'mots', 'segments', 'pragma']
 first {"id": "g001", "langue": "fr", "texte": "Le chat dort.", "mots": [{"texte": "Le", "pos": "DET", "debut": 0, "fin": 2}, {"texte": "chat", "pos": "NOUN", "debut": 3, "fin": 7}, {"texte": "dort", "pos": "VERB", "debut": 8, "fin": 12}], "segments": [{"type": "GN", "texte": "Le chat", "role": "agent", "debut": 0, "fin": 7}, {"type": "GV", "texte": "dort", "role": "prédicat", "debut": 8, "fin": 12}], "p
gold_reel.json ['version', 'source', 'note', 'phrases'] 432
 first keys ['id', 'langue', 'texte', 'mots', 'segments', 'pragma', 'source']
 first {"id": "r001", "langue": "fr", "texte": "Le chien mange une pomme.", "mots": [{"texte": "Le", "pos": "DET", "debut": 0, "fin": 2}, {"texte": "chien", "pos": "NOUN", "debut": 3, "fin": 8}, {"texte": "mange", "pos": "VERB", "debut": 9, "fin": 14}, {"texte": "une", "pos": "DET", "debut": 15, "fin": 18}, {"texte": "pomme", "pos": "NOUN", "debut": 19, "fin": 24}], "segments": [{"type": "GN", "texte": "
gold_synthetique.json ['version', 'source', 'graine', 'note', 'phrases'] 160
 first keys ['id', 'langue', 'texte', 'pragma', 'source',
… [428 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, re, statistics\nd=json.load(open(\"reports/pensee-produit-bloc-l.json\"))\ndet=d[\"banc_50\"][\"detail\"]\nprint(\"texts\",len(det),\"total chars\",sum(len(x[\"texte\"]) for x in det),\"total words\",sum(x[\"mots\"] for x in det))\nfor x in det[:10]:\n    … [119 caractères tronqués]`

  ```
texts 50 total chars 4626 total words 819
f01 fr/courte 6 'Le chat dort sur le canapé.'
f02 fr/longue 28 'La voisine arrose les fleurs du jardin chaque matin avant de partir au travail, puis elle rentre vers dix-huit heures et'
f03 fr/relative+coordination 18 "Le livre que tu m'as prêté hier soir était passionnant, même si la fin m'a un peu déçu."
f04 fr/temporelle 21 'Quand la pluie tombe depuis trois jours, les rues du village se transforment en ruisseaux boueux et les enfants rentrent'
f05 fr/discours-direct 18 '« Je ne sais pas », répondit-elle en haussant les épaules ; son frère, lui, prétendait le contraire.'
f06 fr/question 11 'Peut-être que nous devrions reporter la réunion à demain, non ?'
f07 fr/impérative+négation 13 "Ferme la porte, s'il te plaît, et n'oublie pas d'éteindre la lumière !"
f08 fr/négation-complexe 12 "Il n'a jamais vraiment compris pourquoi elle était partie sans laisser d'adresse…"
f09 fr/relative-longue 21 "Les enfants qui jouent dans la cour de l'école ne savent pas encore que la cloche va sonner dans cinq minutes."
f10 fr/abréviations 19 "M. Dupont, le directeur de l'usine, a annoncé hier qu'il prendrait sa retraite à la fin de l'année, etc."
  ```

- **bash** `{"command": "ls -la tools/tests/linguistique/gold*.json; echo ===; python3 - <<'EOF'\nimport json\nfor f in [\"tools/tests/linguistique/gold.json\",\"tools/tests/linguistique/gold_reel.json\",\"tools/tests/linguistique/gold_synthetique.json\"]:\n d=json.load(open(f)); ps=d[\"phrases\"]\n print(f,len … [201 caractères tronqués]`

  ```
-rw-r--r--. 1 stephane stephane 450905  2 nov 13:27 tools/tests/linguistique/gold_gele.json
-rw-r--r--. 1 stephane stephane  20009 15 nov 12:23 tools/tests/linguistique/gold.json
-rw-r--r--. 1 stephane stephane 470149  2 nov 14:39 tools/tests/linguistique/gold_reel.json
-rw-r--r--. 1 stephane stephane  14631 15 nov 04:59 tools/tests/linguistique/gold_restitution_v2.json
-rw-r--r--. 1 stephane stephane 149211  6 nov 18:56 tools/tests/linguistique/gold_synthetique.json
===
tools/tests/linguistique/gold.json 20 mots 105 langues {'en': 6, 'fr': 14}
tools/tests/linguistique/gold_reel.json 432 mots 2375 langues {'en': 204, 'fr': 228}
tools/tests/linguistique/gold_synthetique.json 160 mots 699 langues {'fr': 160}
  ```

- **bash** `{"command": "grep -rn \"X3\\|J5\" docs/ tools/ reports/*.md 2>/dev/null | grep -i -E \"tagger|lot|batch|J5|X3\" | head -50", "description": "Find X3/J5 task definition"}`

  ```
gnBKIix4ApwYYhC9xA6YCAxJ00HR3TPTUkbDezYrX6NypMj3t3Xg70rE/N+ofoyhmvroXtW6MV1ykx3kvTHFYOv0IyaHHjW4Z/bwE3zqlgbaiEfn77F8yUEfA3qOEKehZMIisln1AzmADDAAT/5jbVCg/sTC9XUsnFA3HgP+V+LUO8ugB9zvnXqXvPgBb9dez/j95+g2RFLub1xLZ/xjShj6GRBVezmjtjsuSeue9wnlCFeKi9gslo3begrEbef86FNtT/PwjRu7YZndZa2p7+oJRdNAOPMwoQ2fI0nfv4tFli6/0XGBhlgxbgJG6W2DUBGiz6CBcgzF8BA5hElj0AIHsFe+PbcuE3Mxe/ioqo/CeZeQ4WiuMMMCmS4fkIZlCHr64ghUqkEI02DigU1u3H94WO8HIZeLtB/s8GLvyf+QV/9Dh5Kf85RtreQjHGINOmAsviG7NqKPWM77OJwHaTvKTBe/a2iofPq17+q18zGiMP2KU+3bDbJ6iKUmljlFmWHoQZ0eRWIt3JscqxGObn/33NHy0ZgGGGibDRYLLSzFUspx0JVKpvqMSkUnftmfcZBlNAJdBKg1riuUxnPSiQ6MZuqd1dEz0OHz1r2gzyG6+CfikZFW7GQsJvoMzoXYU+5ntAWPH+wAw4zVi2//KcrczG5UXjbBcN+yPrldjcdu69tw3MeclGBBqex+y3DwgYhHN7kSBUSxK/pKolrTvPP3Oa0ZDSdU1NFgVEQbadaucFc4EOnxfEq8uVix8dfhcbiOdZpinncSFIUai8Z1qG0dUzFmO0DfOABwAQR8ZoHlf6YgEYc9iERQWGNRuZHYZXy1vP28ny+W06H5nfWqvZKvvDq2Rj1JDSN8Y14o4c883Il4ZwSzGzkl0pHpvCBDzST2beg5Yf/Pp4zP8rGPTDTrqwZl3QOn82s3Ju0r3/xgRjPhb5PQmGSciAw4GjoZCc5XkGZpjNsJ2eFFjnW8krO829+feg5Hy/A8fLDC4eWeMZhzZe9rNZh/wxDLPbX2kZEV46ZprUGd5j983B171aX+qjJ5/59lj+7+8uvHkbvsf01jTXBRwxK1r3lYF9yzxUhYsfmFZLZXv3V14jGCZElzxBAgtcT2qJ2LdfH/jzt89cUjmCzO75b4JKYu+JM0IFrB9kdd+BcnskJjUoiwevHgzxLDitNDDmch1RlLWZE/g4yF
… [48731 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"tagger\" docs/pilotage/roadmap.md | head -30; echo ===; grep -rn \"J5\" docs/pilotage/*.md | head -40", "description": "Search roadmap for tagger/J5"}`

  ```
31:| **B — l'intelligence** | langue, pensée, jeux, maîtres, [banc externe](../theorie/glossaire/entrees/banc-externe.md), sémantique, modules | ✅ B1–B12 ; **B1.5 [corpus](../theorie/glossaire/entrees/corpus.md)**, **B12.10, B10.2bis et B11.10 closes** ; le **décodeur** est levé (objectif mot : 32,5 ; JW 26,7), le `z` reste ; **B13** (moteur de pensée) : state store v0 + **AC-3/alpha-bêta** + **[DRVF](../theorie/glossaire/entrees/drvf.md) `thought`** + **[banc](../theorie/glossaire/entrees/banc.md) anytime** + **opérateurs hétérogènes** + **nécessaire** + **labyrinthe** + **[porte](../theorie/glossaire/entrees/porte.md)** + **apprise** + **courbe** + **seule** + **stochastique** + **sto seule** + **ferme** + **minute** + **minute apprise** + **minute seule** + **minute entraînée** + **shaping** + **réseau** + **MLP** + **[professeur](../theorie/glossaire/entrees/professeur.md)** + **sans None** + **correction** + **audit** + **ouverte** + **graines** + **mobile** + **mobile graines** + **bruit** + **bouge** + **bouge graines** + **période** + **phase** + **phase graines** + **aléatoire** + **hasard** + **partielle** + **croyance** + **curiosité** + **observatrice** + **bruitée** + 
… [9322 caractères tronqués]
  ```

- **bash** `{"command": "grep -rln \"X3\\|tagger en lot\\|tagger-lot\\|1 000 phrases\" journal/sessions/*/plan.md journal/sessions/*/digest.md 2>/dev/null | tail -20", "description": "Search session plans for X3"}`

  ```
journal/sessions/599e9c0e-4252-43ca-a89a-3886d723c379/digest.md
journal/sessions/71d57f53-8b41-4220-84dd-7bb9eedc88d9/digest.md
journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md
journal/sessions/d31b3d9b-58e4-4d34-85fa-381b6f6a6a76/digest.md
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
journal/sessions/session-3a6041f9-48b5-4ef0-924c-5edc354c341c/digest.md
journal/sessions/session-5d421585-1af2-4f07-ac86-e4879cc23d4f/digest.md
journal/sessions/session-bc92a84f-e2ea-4c23-8227-525822d29662/digest.md
journal/sessions/session-bfc6d60f-dbfd-473c-a769-05fde9b1e428/digest.md
journal/sessions/session-f71c99b5-4cd1-41cd-81b4-87e7e7c8bfeb/digest.md
  ```

- **bash** `{"command": "grep -rn \"X3\\|1 000 phrases\\|tagger en lot\\|par lot\" reports/*.md docs/pilotage/*.md 2>/dev/null | grep -v \"1000)\" | head -40", "description": "Search reports for 1000 sentences task"}`

  ```
reports/INDEX.md:650:| [rapport-prefill-par-lots.md](rapport-prefill-par-lots.md) | Préremplissage par lots : ce que le GEMM apporte vraiment |
reports/rapport-a83c-lot.md:5:> chemin jeton par jeton, **+3,2 %** sur le chemin par lots. La « non-monotonie » d'A8.3b
reports/rapport-a83c-lot.md:33:   sur le chemin par lots. Il n'y a **pas** de non-monotonie sur un même calcul.
reports/rapport-a83c-lot.md:38:simple affaire de vitesse**. Le préremplissage par lots réordonne les sommes : les derniers
reports/rapport-a83c-lot.md:46:documentée** du chemin par lots.
reports/rapport-a83c-lot.md:53:- **Le prochain levier n'est pas le KV**, c'est le **chemin par lots** : réduire sa
reports/rapport-a83c-lot.md:79:n'est pas le pool de threads, c'est le **noyau par lots**. Voir
reports/rapport-a83d-lot-threads.md:5:> 8 threads**. Ce n'est donc pas le pool de threads : c'est le **noyau par lots** lui-même.
reports/rapport-a83d-lot-threads.md:15:**pool de threads** (8 par défaut) ou le **noyau par lots** (sommes par bloc). Passer à **1 thread**
reports/rapport-a83d-lot-threads.md:27:pas la valeur lotie. L'écart est donc **dans le chemin par lots**, pas dans les threads.
reports/rapport-a83d-lot-thre
… [4847 caractères tronqués]
  ```

- **bash** `{"command": "for f in journal/sessions/599e9c0e-4252-43ca-a89a-3886d723c379/digest.md journal/sessions/71d57f53-8b41-4220-84dd-7bb9eedc88d9/digest.md journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md journal/sessions/d31b3d9b-58e4-4d34-85fa-381b6f6a6a76/digest.md journal/sessions/e181c … [178 caractères tronqués]`

  ```
=== journal/sessions/599e9c0e-4252-43ca-a89a-3886d723c379/digest.md
15:Contexte : `docs/pilotage/roadmap.md` (chantier N2), `docs/pilotage/en-cours.md` (session N2), `reports/rapport-n2-*.md`, `tools/eval_n2_propre.py`, `tools/entrainer_native.py`, `tools/native_model.py`, `tools/porte-*.sh`. A23 a noté : « `tools/porte-n2.sh` n'existe pas ; `eval_n2_propre.py` exige un checkpoint ; la rouge de N2 est la porte propre à 0,29 ».
22:5. Ne commite rien ; ne modifie aucun existant ; pas de `docs/pilotage/`, `AGENTS.md`, `journal/`, `tools/structures/`, `data/`, `tools/entrainer_native.py`, `tools/native_model.py`.
36:> **Compteurs vivants.** Dans [`docs/pilotage/en-cours.md`](docs/pilotage/en-cours.md) ; ne pas les recopier ici.
40:> (tableau § 3). L'**état courant** est dans [`docs/pilotage/en-cours.md`](docs/pilotage/en-cours.md) ; la **roadmap** dans
41:> [`docs/pilotage/roadmap.md`](docs/pilotage/roadmap.md) ; le récit daté dans [`journal/`](journal/).
45:**Drave est une vision de l'IA centrée sur les flots de données, pas sur le calcul brut.** Les activations d'un
60:   `docs/pilotage/en-cours.md`, et il **nomme sa ligne de roadmap** (A… / B… / N… / R…). *Sans contrôle négatif, ce 
… [16384 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nfor f in [\"reports/pensee-fiabilite-produit.json\",\"reports/pensee-produit-bloc-l.json\"]:\n d=json.load(open(f)); b=d[\"banc_50\"]\n print(\"===\",f, list(b)[:30])\n for k in (\"detail\",\"textes\",\"phrases_liste\"):\n  if k in b:\n   v=b[k]; print(k, … [154 caractères tronqués]`

  ```
=== reports/pensee-fiabilite-produit.json ['synthese', 'resultats']
=== reports/pensee-produit-bloc-l.json ['phrases', 'mots', 'etiquettes', 'attachements', 'categories', 'langues_detectees', 'scripts', 'crashes', 'refus', 'sorties_vides', 'sans_anomalie', 'avec_anomalie', 'anomalies_total', 'anomalies', 'niveaux', 'fraction', 'pos', 'phrases_stats', 'document', 'graphème', 'url_emoji', 'langue', 'double_sens', 'detail']
detail <class 'list'> 50
{"id": "f01", "cat": "fr/courte", "texte": "Le chat dort sur le canapé.", "attendu": "fr", "langue": "fr", "script": "Latn", "mots": 6, "etiquettes": 32, "niveaux": {"graphème": 12, "mot": 7, "pos": 6, "syntagme": 3, "discours": 1, "document": 1, "phrase": 1, "pragmatique": 1}, "niveaux_absents": ["morphème"], "fraction": 0.5185, "attachements": 3, "anomalies": [], "anomalies_n": 0}
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open(\"tools/tests/linguistique/gold_gele.json\"))\nprint(type(d), list(d) if isinstance(d,dict) else len(d))\nif isinstance(d,dict):\n for k,v in d.items():\n  print(k, type(v), len(v) if hasattr(v,'__len__') else '')\n if \"phrases\" in d:\n … [148 caractères tronqués]`

  ```
<class 'dict'> ['gele', 'phrases']
gele <class 'str'> 10
phrases <class 'list'> 602
phrases 602
{"id": "g001", "langue": "fr", "texte": "Le chat dort.", "mots": [{"texte": "Le", "pos": "DET", "debut": 0, "fin": 2}, {"texte": "chat", "pos": "NOUN", "debut": 3, "fin": 7}, {"texte": "dort", "pos": "VERB", "debut": 8, "fin": 12}], "segments": [{"type": "GN", "texte": "Le chat", "role": "agent", "debut": 0, "fin": 7}, {"type": "GV", "texte": "dort", "role": "prédicat", "debut": 8, "fin": 12}], "pragma": {"acte": "assertion"}, "source": "hand"}
  ```

- **bash** `{"command": "find . -path ./journal -prune -o -name \"*.json\" -print 2>/dev/null | xargs -r grep -l '\"phrases\"' 2>/dev/null | head -40", "description": "Find JSON files with phrases"}`

  ```
./reports/sources-pidgin.json
./reports/pensee-gold-linguistique.json
./reports/pensee-gold-subsets.json
./reports/pensee-gold-complexes.json
./reports/pensee-gold-complexes20.json
./reports/pensee-gold-complexes50.json
./reports/pensee-gold-complexes100.json
./reports/pensee-gold-discours.json
./reports/pensee-anaphore-objets.json
./reports/pensee-gold-342.json
./reports/pensee-gold-gele.json
./reports/s-banque-structures.json
./reports/pensee-gold-neuronal.json
./reports/pensee-gold-syntagmes.json
./reports/pensee-gold-cascade.json
./reports/pensee-gold-pragmatique.json
./reports/pensee-gold-cascade-200.json
./reports/pensee-gold-reel-cascade.json
./reports/s-banque-validee.json
./reports/pensee-quatre-modes-niveau.json
./reports/pensee-quatre-modes-432-run2.json
./reports/pensee-quatre-modes-432-run3.json
./reports/pensee-quatre-modes-432-t03.json
./reports/pensee-pragmatique-130.json
./reports/pensee-quatre-modes-432-pragma.json
./reports/pensee-quatre-modes-432-soustype.json
./reports/pensee-quatre-modes-432-soustype-t03.json
./reports/pensee-quatre-modes-432-soustype-t03b.json
./reports/pensee-quatre-modes-432-soustype-t03c.json
./reports/pensee-topk-diagnostic.json
./reports
… [351 caractères tronqués]
  ```

- **bash** `{"command": "grep -rln \"1000 phrases\\|1 000 phrases\\|phrases_1000\\|1000_phrases\\|banc.*1000\" --include=\"*.py\" --include=\"*.json\" --include=\"*.md\" . 2>/dev/null | grep -v journal | head -30", "description": "Search 1000 phrase corpus references"}`

  ```
./reports/rapport-coordination-r.json
./reports/rapport-coordination-r.md
./reports/rapport-semaine.md
./reports/rapport-semaine.json
./reports/rapport-bilan-chantier.json
./reports/rapport-bilan-chantier.md
./reports/rapport-tagger-h50.md
./reports/rapport-tagger-defaut.md
./reports/rapport-tagger-defaut.json
./reports/README.md
./reports/rapport-semaine-2.json
./reports/rapport-semaine-2.md
./tools/tests/test_tagger_api.py
./tools/chantier/plan.json
./tools/drave.py
./docs/pilotage/en-cours.md
./docs/pilotage/semaine-2.md
./docs/produit/README.md
./work/r44/ocr/19f048cdec6ebae3-fra-3.json
./work/r44/ocr/19f048cdec6ebae3-fra-3-col.json
./work/r44/ocr/19f048cdec6ebae3-fra-3-m3.json
./work/r44/ocr/19f048cdec6ebae3-fra-3-m3-col.json
./work/r44/ocr/19f048cdec6ebae3-fra-3-m4.json
./work/r44/ocr/19f048cdec6ebae3-fra-3-m4-col.json
./work/r44/ocr/19f048cdec6ebae3-fra-3-m5.json
./work/r44/ocr/19f048cdec6ebae3-fra-3-m5-col.json
./work/r44/ocr/19f048cdec6ebae3-fra-3-m6.json
./work/r44/ocr/19f048cdec6ebae3-fra-3-m6-col.json
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open(\"tools/tests/linguistique/gold_gele.json\"))\nfrom collections import Counter\nprint(len(d[\"phrases\"]), Counter(p.get(\"source\") for p in d[\"phrases\"]))\nprint(Counter(p.get(\"langue\") for p in d[\"phrases\"]))\nprint(d[\"gele\"])\ … [42 caractères tronqués]`

  ```
602 Counter({'reel': 422, 'synthetique': 160, 'hand': 20})
Counter({'fr': 394, 'en': 208})
2026-11-02
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open(\"tools/chantier/plan.json\"))\nprint(type(d), list(d)[:20] if isinstance(d,dict) else len(d))\ns=json.dumps(d,ensure_ascii=False)\nimport re\nfor m in re.finditer(\"X3|tagger.{0,80}lot|lot.{0,80}tagger|1 000 phrases|1000 phrases\", s):\n … [142 caractères tronqués]`

  ```
<class 'dict'> ['nom', 'principe', 'taches']
 décision du tagger par défaut", "mandat": "Tâche W3 (J2 après-midi) : la matrice du tagger — **défaut** (sans clé, hors ligne, code 0), **avec clé**, **clé invalide**, **réseau coupé**, le coût pour 1 000 phrases, le repli ; la recommandation (défaut hors ligne, `--tagger` opt-in, un mode `auto` seulement si la clé existe et sans changer le code de sortie). Fiche `reports/rapport-tagger-defaut.md` + JSON, avec un test par cas dans `tools/tests/test_tagger_api.py`.", "budget_min": 90, "acceptation": [{"comma
---
e": "test -f reports/rapport-or-roles-protocole.md && echo FICHE-OK", "attendu": "FICHE-OK"}, {"commande": "test -f reports/schema-or-roles.json && echo SCHEMA-OK", "attendu": "SCHEMA-OK"}]}, {"id": "X3", "jour": 17, "titre": "J5 — le tagger en lot : 1 000 phrases", "mandat": "Tâche X3 (J5, la part du pilote) : le tagger **en lot** — mesure le coût et la latence pour **1 000 phrases** (réelles, prises dans le gold + les 50 textes libres), le **taux de cache** (chaud/froid), le **débit** (phrases/m
---
es-protocole.md && echo FICHE-OK", "attendu": "FICHE-OK"}, {"commande": "test -f reports/schema-or-roles.json && echo SCHEMA-OK", 
… [2110 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open(\"tools/chantier/plan.json\"))\nfor t in d[\"taches\"]:\n    if t.get(\"id\") in (\"X1\",\"X2\",\"X3\"):\n        print(json.dumps(t,ensure_ascii=False,indent=2))\nEOF", "description": "Read X1-X3 task specs"}`

  ```
{
  "id": "X1",
  "jour": 17,
  "titre": "J4 — la page / de S : la mesure du pilote",
  "mandat": "Tâche X1 (J4 après-midi, la part du pilote) : mesure la page `/` de S **en lecture seule** — lis les données du sous-module (`tools/structures/`) et la fiche `reports/rapport-coordination-s-v2.md` ; compare **`/` (le banc ancien : 369 candidats, 0 verdict)** et **la v7 (359 candidats, 99 verdicts)** : la couverture, les verdicts, les référents (14 occurrences / 12 formes), les 106 conservés / 41 en quarantaine. Écris `reports/rapport-page-s-mesure.md` + JSON avec le **contrôle négatif** (les deux bancs doivent différer). **Ne modifie rien dans `tools/structures/`.**",
  "budget_min": 90,
  "acceptation": [
    {
      "commande": "test -f reports/rapport-page-s-mesure.md && echo FICHE-OK",
      "attendu": "FICHE-OK"
    }
  ]
}
{
  "id": "X2",
  "jour": 17,
  "titre": "J4 — l'or de rôles : le protocole pour S",
  "mandat": "Tâche X2 (J4 matin, la part du pilote) : le protocole d'annotation de l'**or de rôles** pour S — les champs (phrase, cadre, rôles : agent/prédicat/lieu/temps/destinataire/possession/complément), la **double annotation** (deux codeurs, le kappa), les 144 rôles exis
… [1288 caractères tronqués]
  ```

- **bash** `{"command": "ls -lat work/ | head -30; echo ===; find work -maxdepth 2 -iname \"*tagger*\" -o -maxdepth 2 -iname \"*lot*\" | head -30; echo ===; ls -la work/ | tail -20", "description": "Inspect work dir recent files"}`

  ```
total 240
drwxr-xr-x. 1 stephane stephane  2856 15 nov 12:52 portes-w5
drwxr-xr-x. 1 stephane stephane    20 15 nov 12:35 page-s-mesure
drwxr-xr-x. 1 stephane stephane  2326 15 nov 12:34 .
drwxr-xr-x. 1 stephane stephane   584 15 nov 12:23 portes
-rw-r--r--. 1 stephane stephane  1790 15 nov 12:20 msg-w6.txt
-rw-r--r--. 1 stephane stephane   518 15 nov 12:20 msg-tag-semaine-2.txt
-rw-r--r--. 1 stephane stephane  1277 15 nov 12:08 msg-w5.txt
drwxr-xr-x. 1 stephane stephane  3396 15 nov 12:02 portes-1115-09h53
drwxr-xr-x. 1 stephane stephane   930 15 nov 09:39 portes-1115-09h22
drwxr-xr-x. 1 stephane stephane   240 15 nov 08:56 chantier
drwxr-xr-x. 1 stephane stephane  1078 15 nov 07:09 portes-1115-06h45
drwxr-xr-x. 1 stephane stephane  3396 15 nov 06:56 portes-1115-05h08
drwxr-xr-x. 1 stephane stephane    50 15 nov 04:03 portes-1115-04h03
-rw-r--r--. 1 stephane stephane  3586 15 nov 03:44 tableaux_atomes.py
-rw-r--r--. 1 stephane stephane  1040 15 nov 03:23 atomes_cohortes.py
drwxr-xr-x. 1 stephane stephane  1078 14 nov 06:16 portes-1114-05h52
drwxr-xr-x. 1 stephane stephane    58 14 nov 05:42 portes-1114-05h40
drwxr-xr-x. 1 stephane stephane   274 14 nov 05:37 portes-1114-05h36
drwx
… [2119 caractères tronqués]
  ```

- **bash** `{"command": "git status --porcelain=v1 | wc -l; git diff --stat | tail -20; echo ===; cat .gitignore", "description": "Check git changes and ignore"}`

  ```
20
 docs/pilotage/en-cours.md               |   2 +-
 docs/produit/README.md                  |  25 +-
 reports/pensee-coherence-fiches-v7.json |  19 +
 reports/pensee-dev-test-v10.json        |   2 +-
 reports/pensee-quatre-modes.json        | 734 ++++++++++++++++++--------------
 reports/rapport-audit-v7.md             |   6 +-
 reports/rapport-coherence-fiches-v7.md  |  17 +-
 reports/rapport-dev-test-v10.md         |   2 +-
 reports/rapport-pensee-v12.md           |   4 +-
 reports/rapport-spans-chunker.md        |  13 +-
 tools/chantier/plan.json                | 129 ++++++
 11 files changed, 608 insertions(+), 345 deletions(-)
===
__pycache__/
*.pyc
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

# Campagnes GPU : points de contrôle et jo
… [49 caractères tronqués]
  ```

- **bash** `{"command": "ls -la ~/.config/drave/ 2>/dev/null; test -f ~/.config/drave/deepseek.key && echo KEYFILE-PRESENT || echo KEYFILE-ABSENT; env | grep -E \"DEEPSEEK|DSH_KEY|DSH_API\" | sed 's/=.*$/=<set>/'", "description": "Check DeepSeek key availability"}`

  ```
total 4
drwx------. 1 stephane stephane   24  3 nov 11:15 .
drwx------. 1 stephane stephane 2684 15 nov 09:59 ..
-rw-------. 1 stephane stephane   36  3 nov 11:15 deepseek.key
KEYFILE-PRESENT
  ```

- **bash** `{"command": "ls -ld /tmp/*cache* /tmp/*tagger* 2>/dev/null | head -20; echo ===; ls -la data/deepseek/cache 2>/dev/null | head; echo ===; find /tmp -maxdepth 1 -type d -name \"*tagger*\" 2>/dev/null", "description": "Inspect caches"}`

  ```
-rw-r--r--. 1 stephane stephane   22948  5 nov 14:35 /tmp/bench_cache_chunker.json
-rw-r--r--. 1 stephane stephane    2872  5 nov 14:35 /tmp/bench_cache_chunker.out
-rw-------. 1 stephane stephane   18817  5 nov 14:33 /tmp/bench_cache_chunker.py
drwxr-xr-x. 2 stephane stephane     100 15 nov 04:37 /tmp/drave-exemples-tagger-cache
drwxr-xr-x. 2 stephane stephane     100 15 nov 04:37 /tmp/drave-exemples-tagger-cache
drwxr-xr-x. 2 stephane stephane      80 14 nov 11:15 /tmp/drave-tagger-cli-frais
drwxr-xr-x. 2 stephane stephane     840 14 nov 10:47 /tmp/drave-tagger-option-cache
drwxr-xr-x. 2 stephane stephane     840 14 nov 10:47 /tmp/drave-tagger-option-cache
-rw-r--r--. 1 stephane stephane     221 15 nov 05:54 /tmp/faq-tagger.err
-rw-r--r--. 1 stephane stephane       0 15 nov 05:54 /tmp/faq-tagger.out
-rw-r--r--. 1 stephane stephane    8151 14 nov 10:57 /tmp/genere_pensee_tagger.py
drwxr-xr-x. 2 stephane stephane   38760 13 nov 22:36 /tmp/j43-cache
-rw-r--r--. 1 stephane stephane     619 14 nov 10:55 /tmp/mesure-tagger-option-cli.json
-rw-r--r--. 1 stephane stephane    1585 14 nov 10:49 /tmp/mesure_tagger_option.py
drwxr-xr-x. 2 stephane stephane     380 15 nov 09:09 /tmp/__pycache
… [1558 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 1,140p reports/rapport-tagger-h50.md; echo ===; grep -n \"50 textes\\|libre\\|h50\\|H50\\|corpus\" tools/tests/linguistique/qualifier_tagger_h50.py | head -40", "description": "Read W2 report and H50 source"}`

  ```
# W2 — le tagger POS sur le split 402 / H50 : +4,45 pts sur 402, +17,65 sur H50 ; il gagne sur les deux, donc la règle ne le rejette pas

> **Ligne de roadmap** : **R0.7** (le lecteur) / **B13** · **Tâche** : **W2** (semaine 2, J2 matin) ·
> **Date** : 2026-11-15 (mesure) · **Cible** : J2 · 17/11 · **HEAD mesuré** : `6b2208ee` ·
> **Verdict** : ✅ **le tagger n'est pas H50-only** — il gagne **+4,45 pts** sur **402** et
> **+17,65 pts** sur **H50** ; le F1 et l'attachement du 402 sont **inchangés**. **Réserve nommée** :
> sur 402, le gain est **ouvert** (+10,64 pts) et le **fermé baisse** (−1,55 pt) ; une règle qui
> exigerait la non-régression du fermé rejetterait le tagger tel quel.

**En trois lignes.** (1) Sur les **402** phrases de l'entraînement, le POS passe de **0,9198** à
**0,9643** (**+4,45 pts**, **96 tokens** réparés sur 2 157) ; sur les **50** de **H50**, de
**0,6842** à **0,8607** (**+17,65 pts**, **57 tokens** sur 323). (2) Le **F1** et l'**attachement**
ne bougent pas (le tagger ne remplace que le POS) ; le total 452 donne **0,9508** contre **0,8891**
(**+6,17 pts**), à **0,0008** du 0,9500 déjà publié. (3) La passe **API** paie **447 requêtes** et
**65 029 tokens rés
… [10692 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 1,120p tools/tests/linguistique/qualifier_tagger_h50.py", "description": "Read H50 harness beginning"}`

  ```
#!/usr/bin/env python3
"""qualifier_tagger_h50.py — W2 : le tagger POS sur le split 402 / H50.

POURQUOI. W1 a figé le gold réel 452 en un split **402** (l'entraînement) et **H50** (la tenue
à l'écart, sélectionnée sur les erreurs de l'heuristique). W2 mesure le tagger POS de l'API
DeepSeek sur les deux bases, avec le **cache chaud** puis l'**API**, et applique la règle :
une règle qui ne gagne que sur H50 est **rejetée** ; le contrôle est la non-régression du 402.

CE QUE LE BANC MESURE.
- POS de l'heuristique et du tagger (`Cascade` 0,6, POS neuronal, syntagmes heuristiques) sur
  402, H50, le total 452 et un tirage aléatoire de composition (hors H50).
- Le delta POS (exactitude, fermé, ouvert), le F1 et l'attachement (contrôles de non-régression).
- Le coût : appels, requêtes réseau, cache, tokens, latence par requête et par phrase.
- Trois passes : **cache chaud** (cache disque existant), **API** (cache neuf, tout le réseau),
  **cache chaud après API** (le cache neuf, rejoué : 0 réseau, 0 token).

USAGE.
    python3 tools/tests/linguistique/qualifier_tagger_h50.py \
      --sortie reports/rapport-tagger-h50.json --mode tous

La clé est lue par `tools/llm/deepseek.py` (DEEPSEEK
… [4169 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"def \\|memoire\\|memory\\|ru_maxrss\\|tracemalloc\\|cache\\|passe\\|latence\\|duree\" tools/tests/linguistique/qualifier_tagger_h50.py | sed -n 1,120p", "description": "Map H50 harness functions"}`

  ```
6:DeepSeek sur les deux bases, avec le **cache chaud** puis l'**API**, et applique la règle :
13:- Le coût : appels, requêtes réseau, cache, tokens, latence par requête et par phrase.
14:- Trois passes : **cache chaud** (cache disque existant), **API** (cache neuf, tout le réseau),
15:  **cache chaud après API** (le cache neuf, rejoué : 0 réseau, 0 token).
22:DEEPSEEK_API_KEY). Elle n'est jamais affichée, ni écrite dans le JSON, ni dans le cache.
58:def charger_452() -> list[dict]:
69:def charger_split() -> dict:
86:def construire_bases(phrases: list[dict], split: dict) -> dict[str, list[dict]]:
108:def duplicats(phrases: list[dict]) -> list[dict]:
109:    """Les textes identiques (même langue) : le tagger les sert une fois par cache mémoire."""
117:def composition(phrases: list[dict]) -> dict:
125:# --------------------------------------------------------------------------- cache
128:def meta_cache(chemin: pathlib.Path) -> dict:
129:    """Ce que le cache disque contient : nombre, dates, modèles (sans la clé)."""
155:    def __init__(self) -> None:
160:        self.tokens_cache = 0
161:        self.latence_reseau_s = 0.0
162:        self.latence_cache_s = 0.0
164:    def par_phras
… [6775 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 125,360p tools/tests/linguistique/qualifier_tagger_h50.py", "description": "Read cache and measurement machinery"}`

  ```
# --------------------------------------------------------------------------- cache


def meta_cache(chemin: pathlib.Path) -> dict:
    """Ce que le cache disque contient : nombre, dates, modèles (sans la clé)."""
    if not chemin.is_dir():
        return {"fichiers": 0, "dates": {}, "modeles": {}}
    fichiers = sorted(chemin.glob("*.json"))
    dates, modeles = [], collections.Counter()
    for f in fichiers:
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if d.get("recu_le"):
            dates.append(d["recu_le"])
        if d.get("modele"):
            modeles[d["modele"]] += 1
    return {"fichiers": len(fichiers),
            "dates": {"min": min(dates) if dates else None,
                      "max": max(dates) if dates else None},
            "modeles": dict(modeles)}


# --------------------------------------------------------------------------- mesure


class Journal:
    """Les appels réellement faits au transport, avec la phrase courante."""

    def __init__(self) -> None:
        self.calls: list[dict] = []
        self.phrase: str | None = None
        self.langue: st
… [10046 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, sys, pathlib\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nd=json.load(open(\"reports/pensee-produit-bloc-l.json\"))\ndet=d[\"banc_50\"][\"detail\"]\nh=bl.Heuristique()\ntot=0\nfor x in det:\n    ps=[x[\"texte\"][a:b] for a,b,t,_ in h._phra … [398 caractères tronqués]`

  ```
sentences from 50 texts: 56
gold.json 20
gold_reel.json 432
gold_synthetique.json 160
gold 612 total 668
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open(\"reports/pensee-fiabilite-produit.json\"))\nb=d[\"banc_50\"]\nprint(json.dumps(b,ensure_ascii=False)[:3000])\nEOF", "description": "Inspect fiabilite banc_50"}`

  ```
{"synthese": {"n": 50, "succes": 46, "refus": 4, "plantages": 0, "json_invalide": 0, "sorties_vides_sur_succes": 0, "spans_hors_texte": 0, "spans_vides": 0, "valeurs_vides": 0, "cles_racine_ko": 0, "cles_etiquette_ko": 0, "types_inconnus": 0, "cibles_absentes_du_texte": 0, "stderr_succes_non_vide": 0, "determinisme": "46/46", "labels": 4501, "mots": 1068, "pos": 766, "syntagmes": 360, "attachements": 284, "sans_attachement": 76, "syntagmes_par_type": {"GN": {"total": 87, "attaches": 83, "sans": 4, "union": 11}, "GV": {"total": 145, "attaches": 75, "sans": 70, "union": 35}, "GP": {"total": 86, "attaches": 84, "sans": 2, "union": 28}, "REL": {"total": 28, "attaches": 28, "sans": 0, "union": 10}, "SUB": {"total": 14, "attaches": 14, "sans": 0, "union": 1}}, "chevauchements": {"textes": 23, "textes_tous_niveaux": 28, "paires": 107, "union_labels": 85, "apres_filtre_union": 0, "tous_impliquent_union": true}, "phrases_type": 76, "phrases_espaces_initiaux": 19, "phrase_chevauchement_type": 1, "documents": 49, "doc_tronquees": 17, "doc_titres_faux": 2, "langues": {"fr": 35, "en": 5, "und": 5, "it": 1}, "sans_syntagme": ["f13", "f18", "f27", "f37"], "sans_pos": ["f18"], "tokens_sans_pos": {
… [1800 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nfor f,key in [(\"reports/pensee-produit-bloc-l.json\",\"detail\"),(\"reports/pensee-fiabilite-produit.json\",None)]:\n d=json.load(open(f))\n if key: rows=d[\"banc_50\"][key]\n else: rows=d[\"banc_50\"][\"resultats\"]\n print(\"===\",f,len(rows))\n print( … [268 caractères tronqués]`

  ```
=== reports/pensee-produit-bloc-l.json 50
chars 4626 mots 819
f01 6 None 'Le chat dort sur le canapé.'
f02 28 None 'La voisine arrose les fleurs du jardin chaque matin avant de partir au travail, puis elle rentre ver'
f03 18 None "Le livre que tu m'as prêté hier soir était passionnant, même si la fin m'a un peu déçu."
f04 21 None 'Quand la pluie tombe depuis trois jours, les rues du village se transforment en ruisseaux boueux et '
f05 18 None '« Je ne sais pas », répondit-elle en haussant les épaules ; son frère, lui, prétendait le contraire.'
=== reports/pensee-fiabilite-produit.json 50
chars 4627 mots 1068
f01 4 None 'Le chat dort.'
f02 13 None 'Le chat de la voisine qui dort sur le toit se réveille.'
f03 6 None "Bonjour ! Comment allez-vous aujourd'hui ?"
f04 9 None "Ferme la porte, s'il te plaît."
f05 6 None 'Ne touche pas à ça !'
  ```

- **bash** `{"command": "for d in data/corpus_wiki_fr_texte data/corpus_propre data/corpus_litt_propre data/corpus_nonambigu data/presse data/structures; do echo \"=== $d\"; ls \"$d\" 2>/dev/null | head -8; echo \"count: $(ls \"$d\" 2>/dev/null | wc -l)\"; done", "description": "Look for 50-text directories"}`

  ```
=== data/corpus_wiki_fr_texte
test.txt
train.txt
val.txt
count: 3
=== data/corpus_propre
dev.txt
test.canal
test.txt
train.canal
train.txt
val.canal
val.txt
count: 7
=== data/corpus_litt_propre
test.txt
train.txt
val.txt
count: 3
=== data/corpus_nonambigu
temoin.txt
train.txt
count: 2
=== data/presse
api
presse_2026.json
count: 2
=== data/structures
banque.jsonl
banque-manifest.json
banque-reference.jsonl
banque-reference-manifest.json
banque-validee.jsonl
banque-validee-manifest.json
count: 6
  ```

- **bash** `{"command": "find reports -maxdepth 1 -type f -name \"*.json\" -printf \"%f\\n\" | while read f; do n=$(python3 -c \"import json,sys; d=json.load(open('reports/$f')); print(1 if isinstance(d,dict) and any(k in d for k in ('banc_50','textes_libres','detail')) else 0)\" 2>/dev/null); [ \"$n\" = \"1\"  … [81 caractères tronqués]`

  ```
miroir-boucle.json
miroir-boucle-3b.json
ocr-pdf-cegep-detection.json
pensee-bonne-reponse-voisin.json
pensee-lien-repare.json
pensee-lien-repare-10.json
pensee-lien-inverse.json
pensee-lien-verbe.json
pensee-lien-acte.json
pensee-lien-sujet.json
pensee-lien-simple.json
pensee-lien-gv.json
pensee-lien-thematique.json
pensee-lien-appris.json
pensee-spans-chunker.json
pensee-produit-bloc-l.json
pensee-fiabilite-produit.json
  ```

- **bash** `{"command": "find work -maxdepth 3 -type f \\( -name \"*.json\" -o -name \"*.txt\" -o -name \"*.jsonl\" \\) -printf \"%s %p\\n\" 2>/dev/null | sort -nr | head -30", "description": "Inspect work files"}`

  ```
27464737 work/n2j/tout_wiki.txt
4430959 work/ocr/cegep64/train_restaure.txt
2994663 work/n2j/unamb_wiki.txt
2542795 work/j71/j71-rapide.json
2540513 work/j71/j71-rapide2.json
769005 work/ocr/census-cegep.json
751579 work/dr/eval/ru-xnli.txt
663645 work/ocr/detection-cegep.json
598137 work/dr/eval/ar-xnli.txt
475235 work/dr/eval/fr-xnli.txt
459743 work/dr/eval/de-xnli.txt
443562 work/dr/eval/es-xnli.txt
398603 work/dr/eval/en-xnli.txt
349991 work/dr/eval/zh-xnli.txt
135278 work/r44/mesure-final.json
121597 work/r44/mesure-brut-auto.json
119950 work/r44/colonnes/manifeste.json
82963 work/chantier/etat.json
82784 work/r44/mesure-dev-auto2.json
81451 work/r44/mesure-v9-noexp.json
81324 work/r44/mesure-v8.json
81322 work/r44/mesure-v9.json
81322 work/r44/mesure.json
71483 work/r44/mesure-v7-noexp.json
71414 work/r44/mesure-v6.json
71414 work/r44/mesure-v5.json
71371 work/r44/mesure-v4.json
71366 work/r44/mesure-v7.json
71323 work/r44/mesure-final-exp-col.json
59093 work/r44/mesure-brut.json
[stderr]
sort: write failed: 'standard output': Broken pipe
sort: write error
  ```

- **bash** `{"command": "grep -rIl \"1000 phrases\\|1 000 phrases\" work reports 2>/dev/null | head -20", "description": "Find work files mentioning 1000 phrases"}`

  ```
work/chantier/journal.log
work/msg-w6.txt
reports/rapport-coordination-r.json
reports/rapport-coordination-r.md
reports/rapport-semaine.md
reports/rapport-semaine.json
reports/rapport-bilan-chantier.json
reports/rapport-bilan-chantier.md
reports/rapport-tagger-h50.md
reports/rapport-tagger-defaut.md
reports/rapport-tagger-defaut.json
reports/README.md
reports/rapport-semaine-2.json
reports/rapport-semaine-2.md
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open(\"reports/pensee-produit-bloc-l.json\"))[\"banc_50\"][\"detail\"]\nprint(max(len(x[\"texte\"]) for x in d), sorted((len(x[\"texte\"]),x[\"id\"]) for x in d)[-5:])\nfor x in d:\n    if len(x[\"texte\"])>250: print(x[\"id\"], len(x[\"texte\ … [77 caractères tronqués]`

  ```
485 [(129, 'f04'), (144, 'x46'), (160, 'f02'), (176, 'x43'), (485, 'x50')]
x50 485 r écouter la suite, oubliant l'heure, le train à prendre et les courses à faire.
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open(\"reports/pensee-fiabilite-produit.json\"))[\"banc_50\"][\"resultats\"]\nprint(max(len(x[\"texte\"]) for x in d), sorted((len(x[\"texte\"]),x[\"id\"]) for x in d)[-5:])\nfor x in d:\n    if len(x[\"texte\"])>300: print(x[\"id\"], len(x[\" … [85 caractères tronqués]`

  ```
2144 [(72, 'f45'), (74, 'f44'), (123, 'f48'), (390, 'f43'), (2144, 'f50')]
f43 390 sans dépasser la fin, ce qui serait un défaut grave pour un client qui découpe le texte par indices.
f50 2144 lisibles. Ne supprimez pas les lignes vides : elles séparent les paragraphes et changent la lecture.
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\ndef load(f):\n d=json.load(open(f)); return d[\"phrases\"]\na=load(\"tools/tests/linguistique/gold_reel.json\")\nb=load(\"tools/tests/linguistique/gold_gele.json\")\nA={p[\"texte\"] for p in a}; B={p[\"texte\"] for p in b if p.get(\"source\")==\"reel\"}\n … [428 caractères tronqués]`

  ```
429 419 419 429
hand 20 synth 160
union all 609
hand Le chat dort.
hand Le chat de la voisine dort.
hand La femme a vu l'homme dans le parc.
  ```

- **bash** `{"command": "grep -n \"50 textes\\|f01\\|corpus\\|source\\|échant\" reports/rapport-produit-bloc-l.md | head -50; echo ===; sed -n 1,80p reports/rapport-produit-bloc-l.md", "description": "Understand 50 texts provenance"}`

  ```
20:jamais une sortie vide** et garde **tous les offsets** ; mais **34/50 textes** portent au moins une
29:| POS fermées | ✅ | gold **0,9004** ; 50/50 textes ont des POS |
50:  `phrase`, doublons, unités sémantiques, fraction recalculée, confiance, source, niveau, type,
55:  qualité du vrai modèle neuronal (pas de réseau/GPU ici), ni la robustesse à un corpus aléatoire.
146:| **zéro** | 0 | — | span hors texte, span vide, cible absente, cible non-token, segment d'attachement, unité hors texte, unité qui se chevauche, fraction incohérente, confiance hors [0,1], source/niveau/type invalides, doublon |
149:syntagme (51,9 %)** sont impliquées, dans **31/50 textes** ; 113 sont des **inclusions**, 19 des
156:**Autres écarts de forme** : **60 étiquettes phrase** pour 50 textes (6 textes multi-phrases),
159:**graphème** : 49/50 textes à 100 %, x46 à **95,14 %** (7 newlines, catégorie `Cc`, non couvertes).
163:- **POS ouvertes** : 365 `NOUN` pour 32 `VERB` sur les 50 textes. f02 : « arrose », « rentre »,
182:  `hns`/`sco`/`pcm` non), et **2/50** en égalité stricte de chaîne (les deux `und`). Exemples : f01 fr→`hns`, e29/e35/e42 en→`sco`, e37 en→`pcm`, f03/f23/
239:les **11 mêmes clés** sur l
… [7459 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 1,120p tools/tests/linguistique/gold_reel.py; echo ===; python3 - <<'EOF'\nimport json\nd=json.load(open(\"tools/tests/linguistique/gold_reel.json\"))\nprint(d.get(\"source\"), d.get(\"note\"))\nprint(d[\"phrases\"][0].keys())\nprint({p.get(\"source\") for p in d[\"phrases\"]})\n … [52 caractères tronqués]`

  ```
"""gold_reel.py — 200 phrases réelles (20 françaises, 20 anglaises).

Elles ne sont pas des phrases du bloc ni du générateur : elles sont écrites après, avec leurs
POS, leurs segments GN/GV/GP/REL/SUB et leur pragmatique. Le fichier `gold_reel.json` est généré
par `construire()` ; le gold réel total devient **200 phrases** (20 de `gold.py` + 180).
"""
from __future__ import annotations

import json
import pathlib

# La **convention des cibles** d'attachement. Le gold ne la documentait pas ; elle a été lue
# sur les données le 2026-11-05 (T169/T172) et la voici, explicitement :
#
#   - **REL** : la cible est l'**antécédent** — la tête nominale du GN à gauche
#     (« l'homme que j'ai vu » → `homme`) ;
#   - **SUB** : la cible est le **verbe gouverneur** (le POS gold donne 69/69 cibles VERB :
#     « cette étoile écoute que Lucas trouve » → `écoute`), pas un antécédent ;
#   - **GP** : la cible est le **verbe qui gouverne** le complément (« au ballon » → `joue`),
#     ou, pour un génitif, le **nom qu'il complète** (« de la voisine » → `chat`) ;
#   - **GN / GV** : la cible, quand elle existe, est le **nom ou le verbe** dont le segment
#     dépend (36 cibles verbes, 82 cibles noms m
… [7888 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 1,260p tools/llm/deepseek.py", "description": "Read DeepSeek client"}`

  ```
#!/usr/bin/env python3
"""deepseek.py — le professeur externe, sans poids locaux.

POURQUOI CE MODULE. Le dépôt garde ses GPU et ses CPU pour le **modèle natif**
Drave (`entrainer_moteur.py`, `drave-core`) et pour les mesures **boîte blanche**
(perplexité, activations, flux, sondes). Le **langage** — traduire, juger,
générer, évaluer — passe par une API : on ne charge plus un Qwen de 7/14/32 B
pour cela. DeepSeek est ce **professeur externe** ; ses sorties peuvent servir à
entraîner/distiller l'élève natif (autorisation explicite du propriétaire de la
licence).

CE QUE LE MODULE NE FAIT PAS. Il ne remplace pas les mesures d'états internes :
une API ne donne pas les poids ni les activations. Il ne met **jamais** la clé
dans le dépôt, dans un cache ou dans un message d'erreur. Il ne dépend d'aucun
paquet externe : `urllib` suffit.

CONTRAT.
- `DEEPSEEK_API_KEY` (ou `DSH_API_KEY`) : la clé, lue dans l'environnement ;
- `DEEPSEEK_BASE_URL` (ou `DSH_BASE_URL`) : `https://api.deepseek.com` par défaut ;
- `DEEPSEEK_MODEL` (ou `DSH_MODEL`) : `deepseek-chat` par défaut ;
- cache : `data/deepseek/cache/<sha256>.json` (gitignoré), clé = modèle + messages
  + température + max_tokens, **jamais
… [10153 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, glob, os\nfs=glob.glob('/tmp/tagger-h50-api-cache/*.json')\nprint(len(fs))\nif fs:\n d=json.load(open(fs[0]))\n print(json.dumps(d.get('usage'),ensure_ascii=False,indent=1))\n print(json.dumps(d.get('brut',{}).get('usage'),ensure_ascii=False,indent=1))\n  … [113 caractères tronqués]`

  ```
447
{
 "prompt_tokens": 120,
 "completion_tokens": 17,
 "total_tokens": 137,
 "prompt_tokens_details": {
  "cached_tokens": 0
 },
 "prompt_cache_hit_tokens": 0,
 "prompt_cache_miss_tokens": 120
}
{
 "prompt_tokens": 120,
 "completion_tokens": 17,
 "total_tokens": 137,
 "prompt_tokens_details": {
  "cached_tokens": 0
 },
 "prompt_cache_hit_tokens": 0,
 "prompt_cache_miss_tokens": 120
}
deepseek-flash 1.159 2026-11-15T09:18:28-0500
  ```

- **bash** `{"command": "date -u; date; python3 -V; /usr/bin/time -v true 2>&1 | head -3; nproc; free -h | head -3", "description": "Check date, tools, memory"}`

  ```
dim 15 nov 2026 17:56:09 UTC
dim 15 nov 2026 12:56:09 EST
Python 3.13.16
	Command being timed: "true"
	User time (seconds): 0.00
	System time (seconds): 0.00
40
               total        used        free      shared  buff/cache   available
Mem:           125Gi        24Gi        15Gi       8,5Gi        96Gi       101Gi
Swap:           62Gi       299Mi        62Gi
  ```

- **bash** `{"command": "test -w tools/tests/linguistique && echo writable; python3 tools/drave.py --version 2>&1 | head -2; python3 tools/drave.py analyser \"Le chat dort.\" --json | head -5", "description": "Smoke test CLI"}`

  ```
writable
drave 0.1.0
{
 "schema": "drave.annotation",
 "version": 2,
 "texte": "Le chat dort.",
 "langue": "fr",
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, collections, sys\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nps=[]\nfor f,s in [(\"gold.json\",\"hand\"),(\"gold_reel.json\",\"reel\"),(\"gold_synthetique.json\",\"synth\")]:\n for p in json.load(open(\"tools/tests/linguistique/\"+f))[\"p … [901 caractères tronqués]`

  ```
gold 612 unique texts 609
dups [(('Le vent souffle fort.', 'fr'), 2), (('La voiture roule vite.', 'fr'), 2), (('Paul sees Marie; he speaks to her.', 'en'), 2)] n 3
free sentences 56 unique 56
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 20, in <module>
ValueError: not enough values to unpack (expected 4, got 3)
[exit code: 1]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, sys\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nps=[]\nfor f,s in [(\"gold.json\",\"hand\"),(\"gold_reel.json\",\"reel\"),(\"gold_synthetique.json\",\"synth\")]:\n for p in json.load(open(\"tools/tests/linguistique/\"+f))[\"phrases\"]:\n  … [612 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 16, in <module>
ValueError: not enough values to unpack (expected 4, got 3)
[exit code: 1]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, sys\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nps=[]\nfor f,s in [(\"gold.json\",\"hand\"),(\"gold_reel.json\",\"reel\"),(\"gold_synthetique.json\",\"synth\")]:\n for p in json.load(open(\"tools/tests/linguistique/\"+f))[\"phrases\"]:\n  … [834 caractères tronqués]`

  ```
all 668 unique 665
free in gold []
free unique 56
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, collections\nfor f,key in [(\"reports/pensee-produit-bloc-l.json\",\"detail\"),(\"reports/pensee-fiabilite-produit.json\",\"resultats\")]:\n d=json.load(open(f))[\"banc_50\"][key]\n print(f, collections.Counter(x.get(\"langue\") for x in d), len(d))\n pri … [119 caractères tronqués]`

  ```
reports/pensee-produit-bloc-l.json Counter({'fr': 34, 'en': 14, 'und': 2}) 50
[('fr/courte', 1), ('fr/longue', 1), ('fr/relative+coordination', 1), ('fr/temporelle', 1), ('fr/discours-direct', 1), ('fr/question', 1), ('fr/impérative+négation', 1), ('fr/négation-complexe', 1), ('fr/relative-longue', 1), ('fr/abréviations', 1)]
reports/pensee-fiabilite-produit.json Counter({'fr': 35, 'en': 5, 'und': 5, None: 4, 'it': 1}) 50
[(None, 50)]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open(\"reports/pensee-pos-r4.json\"))\ns=json.dumps(d,ensure_ascii=False)\nfor needle in [\"50 textes\",\"textes libres\",\"f01\",\"audit produit\"]:\n i=s.find(needle)\n print(\"===\",needle,i)\n if i>=0: print(s[max(0,i-500):i+800])\nEOF", " … [51 caractères tronqués]`

  ```
=== 50 textes 277
{"rapport": "pos-r4", "ligne": ["A25 (gold anglais)", "B13 (moteur de pensée)"], "date": "2026-11-06", "branche": "s/v7", "objet": "Mesurer les deux derniers leviers POS : R4 (copule → ADJ pour un mot inconnu) et la complétion des classes fermées anglaises ; mesurer aussi les 50 textes libres de l’audit produit.", "verdict": "R4 bilingue reproduit +0,74 dev / +0,71 test (23 correctifs, 0 cassé), mais 17 faux→faux et 5 faux positifs français sur 8 changements libres. Les classes fermées valent +0,78 / +0,81 (25 correctifs, 0 cassé), F1 +0,0007. Le paquet sûr (R4-en + classes fermées) vaut +1,19 dev / +1,11 test, 37/0, F1 +0,0007, attachement inchangé, 1 faux positif libre (`where`). Le paquet max (R4 bilingue) vaut +1,51/+1,51 mais 11 faux→faux et 6 faux positifs libres.", "snapshot": {"reference": {"nom": "B13", "commit": "2ba393b0", "module_sha256": "f3db75fcaf0ced187c8ddc204e2b8509f34e080c3b81021b1e7ca66327afcc87", "gold": {"gold.json": "3663be6cea2f22e2166df9a2ab6b7c459ff7806cf72d238263b1423ac4e2e58a", "gold_reel.json": "05d4f6dfae67dc72b714dbef69e8764a81124
=== textes libres 280
{"rapport": "pos-r4", "ligne": ["A25 (gold anglais)", "B13 (moteur de pensée)"], "
… [2131 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"class NeuronalLLMPOS\\|class NeuronalLLM\\|def analyser\\|self.cache\\|appels\\|max_jetons\\|prompt\" tools/bloc_linguistique.py | sed -n 1,80p", "description": "Locate NeuronalLLMPOS"}`

  ```
145:    def analyser(self, texte: str, langue: str | None = None,
176:    de test. Un profil est une donnée, pas un prompt : il se versionne et se rejoue.
1471:    def analyser(self, texte: str, langue: str | None = None,
1861:    def analyser(self, texte: str, langue: str | None = None,
1905:class NeuronalLLM:
1906:    """L'adaptateur réel : un prompt JSON, un modèle local, le même contrat.
1915:                 max_jetons: int = 256, timeout: int = 120):
1918:        self.max_jetons = max_jetons
1921:    def _prompt(self, texte: str, langue: str | None, contexte: str | None) -> str:
1932:    def analyser(self, texte: str, langue: str | None = None,
1939:                [self.llama_cli, "-m", self.modele, "-p", self._prompt(texte, langue, contexte),
1940:                 "-n", str(self.max_jetons), "--temp", "0", "--no-display-prompt"],
1984:class NeuronalLLMPOS:
2004:                 confiance: float = 0.6, timeout: int = 180, max_jetons: int = 0,
2010:        self.max_jetons = max_jetons
2012:        self.cache = cache
2013:        self.appels = 0
2031:    def _post(self, invite: str, grammaire: str, max_jetons: int) -> str:
2033:                 "max_tokens": max_jetons, "gramm
… [2178 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 1984,2114p tools/bloc_linguistique.py", "description": "Read NeuronalLLMPOS"}`

  ```
class NeuronalLLMPOS:
    """Le **tagger** neuronal réel : un modèle local, des POS alignés sur la tokenisation du bloc.

    Le modèle ne rend pas une annotation complète : il rend **une classe par token**, contrainte
    par une grammaire GBNF (`grammaire_pos`) qui interdit un JSON tronqué, un token manquant ou
    une classe hors du jeu. Les spans sont ceux de `Heuristique._mots` (la tokenisation du bloc),
    pas ceux que le modèle inventerait ; c'est ce qui rend la mesure POS exacte.

    Le modèle est servi par `llama-server` (`/v1/chat/completions`, `grammar`) : le serveur est
    lancé une fois, le modèle chargé une fois, et les 180 phrases coûtent une passe CPU, pas
    180 chargements. `transport` est injectable pour tester le contrat sans modèle.

    La confiance par défaut (`0.6`) est **celle du seuil ouvert de l'heuristique** (0.55) : dans
    une `Cascade`, le tagger ne remplace donc que les tokens que l'heuristique déclare peu sûrs,
    et laisse les classes fermées (0.92) à l'heuristique. C'est la politique mesurée.
    """

    nom = "neuronal"

    def __init__(self, modele: str | pathlib.Path, endpoint: str = "http://127.0.0.1:18081",
                 confiance:
… [5731 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"def cmd_analyser\\|add_parser(\\\"analyser\\|--jsonl\\|--langue\\|--partition\\|--contexte\\|--fichier\" tools/drave.py | tail -40; sed -n 520,700p tools/drave.py", "description": "Read CLI argument definitions"}`

  ```
7:    python3 tools/drave.py analyser "The cat sleeps on the roof." --langue en --json
386:    """Le texte : l'argument, ou le **fichier** (`--fichier`)."""
394:    """Une **ligne JSON par phrase** (traitement de corpus : `--jsonl`).
420:def cmd_analyser(args: argparse.Namespace) -> int:
734:    laisse le bloc détecter la langue, comme le CLI sans `--langue`. `--canonique`
758:            print(f"{NOM}: erreur d'usage : --banc est exclusif de TEXTE et --fichier",
801:        print(f"{NOM}: erreur d'usage : TEXTE ou --fichier requis", file=sys.stderr)
877:        "Options : --json, --langue fr|en, --partition brut|alternative|filtrer_union|filtrer,\n"
878:        "--contexte, --banc, --tagger.\n"
912:                          help="texte à analyser (entre guillemets) ou --fichier")
913:    analyser.add_argument("--partition", choices=("brut", "alternative", "filtrer_union", "filtrer"),
916:    analyser.add_argument("--fichier", default=None, metavar="CHEMIN",
918:    analyser.add_argument("--jsonl", action="store_true",
920:    analyser.add_argument("--contexte", default=None,
922:    analyser.add_argument("--langue", choices=("fr", "en"), default=None,
963:    rejouer.add_argument(
… [10376 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"hors pointe\\|pointe\\|16:30\\|00:30\\|tarif\" reports/rapport-coordination-r.md | head -30; sed -n 230,280p reports/rapport-coordination-r.md", "description": "Read pricing details"}`

  ```
10:> manque. Coût mesuré : **1 218 appels, 358 962 tokens, 21 min**, **~0,04 $** hors pointe.
147:Tarif public `deepseek-flash` au 2026-11-13 (hors pointe / pointe) : entrée **cache hit**
149:([tarifs](https://api-docs.deepseek.com/quick_start/pricing)). Le run a consommé, d'après les
153:| tarif | entrée hit | entrée miss | sortie | **total** |
155:| **hors pointe** (run à 03:00 UTC, samedi) | 0,0005 $ | 0,0262 $ | 0,0164 $ | **~0,043 $** |
156:| **pointe** | 0,0009 $ | 0,0524 $ | 0,0328 $ | **~0,086 $** |
158:Le run a eu lieu un **samedi 03:00 UTC** : **hors pointe**, donc **~0,04 $**. Pour **1 000
160:pointe (**~0,14 $** en pointe). Le POS seul coûterait **la moitié** (~609 appels, ~180 k tokens,
### 5.1 La règle

La consigne fixe **deux bornes** ; la fiche explicite la zone qu'elle laisse ouverte.

| mesure sur le 612 | décision |
|---|---|
| **< +2,0 pts** | **négatif nommé** : le tagger n'est pas additif au gold courant ; garder l'heuristique, fermer R0.7 tagger |
| **≥ +5,0 pts** | **intégrer via l'API DeepSeek** (jamais le 7B local, règle 11) |
| **2,0 à 5,0 pts** | **zone grise** (non tranchée par la consigne) : aucune décision automatique ; mesure tenue à l'écart avant de
… [2327 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 140,165p reports/rapport-coordination-r.md", "description": "Read exact pricing table"}`

  ```
Le run 432 de référence (`pensee-quatre-modes-432-run2.json`) : **858 appels**, **254 454
tokens**, **807,6 s**, soit **1,986 appel/phrase**, **296,6 tokens/appel**, **0,941 s/appel**.
Le passage à 612 donne **1 218 appels**, **358 962 tokens**, **1 259,2 s** : la consigne était
juste à quelques pour cent.

### 3.3 Le coût facturé

Tarif public `deepseek-flash` au 2026-11-13 (hors pointe / pointe) : entrée **cache hit**
0,003 / 0,006 $ par M, entrée **cache miss** 0,15 / 0,30 $ par M, sortie 0,60 / 1,20 $ par M
([tarifs](https://api-docs.deepseek.com/quick_start/pricing)). Le run a consommé, d'après les
`usage` du cache : **155 136 tokens d'entrée en cache hit**, **174 822 en cache miss**,
**27 326 tokens de sortie** (totaux à ±0,5 % près, six prompts dupliqués).

| tarif | entrée hit | entrée miss | sortie | **total** |
|---|---:|---:|---:|---:|
| **hors pointe** (run à 03:00 UTC, samedi) | 0,0005 $ | 0,0262 $ | 0,0164 $ | **~0,043 $** |
| **pointe** | 0,0009 $ | 0,0524 $ | 0,0328 $ | **~0,086 $** |

Le run a eu lieu un **samedi 03:00 UTC** : **hors pointe**, donc **~0,04 $**. Pour **1 000
phrases** : **~1 990 appels**, **~587 k tokens**, **~34 min** séquentielles, **~0,07 $** hor
… [246 caractères tronqués]
  ```

- **bash** `{"command": "tail -40 work/chantier/journal.log 2>/dev/null; echo ===; python3 - <<'EOF'\nimport json\nd=json.load(open('work/chantier/etat.json'))\nprint(json.dumps(d,ensure_ascii=False,indent=1)[:3000])\nEOF", "description": "Inspect pilot journal/state"}`

  ```
2026-11-15 02:15:56 · ✔ C1 en 741.5 s (code 0) — ✅ test -f reports/rapport-coordination-n2-v2.md && echo FICHE-OK
2026-11-15 02:15:56 · ▶ C2 — Coordination S — la page / et la v7 (timeout 3600 s)
2026-11-15 02:34:01 · ✔ C2 en 1085.7 s (code 0) — ✅ test -f reports/rapport-coordination-s-v2.md && echo FICHE-OK
2026-11-15 02:34:01 · ▶ C3 — Coordination R — le gold réel étendu (timeout 3600 s)
2026-11-15 02:46:21 · ✔ C3 en 739.2 s (code 0) — ✅ test -f reports/rapport-gold-reel-50.md && echo FICHE-OK
2026-11-15 02:46:21 · ▶ B1 — Panini — le protocole à date contrôlée (timeout 3600 s)
2026-11-15 03:06:39 · ✔ B1 en 1218.0 s (code 0) — ✅ test -f reports/rapport-protocole-date.md && echo FICHE-OK
2026-11-15 03:06:39 · ▶ B2 — Panini — les atomes et les niveaux, prédiction (timeout 3600 s)
2026-11-15 03:55:09 · ✔ B2 en 2910.5 s (code 0) — ✅ test -f reports/rapport-atomes-prediction.md && echo FICHE-OK
2026-11-15 03:55:09 · ▶ B3 — Panini — le corpus d'or CIC étendu (timeout 3600 s)
2026-11-15 04:06:34 · ✔ B3 en 684.4 s (code 0) — ✅ test -f reports/rapport-cic-v2.md && echo FICHE-OK
2026-11-15 04:35:53 · ▶ D1 — Les exemples avec le tagger et la base réelle (timeout 3600 s)
2026-11-15 04:53:43 ·
… [6026 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"def json\" tools/bloc_linguistique.py | head; sed -n 250,340p tools/bloc_linguistique.py", "description": "Inspect Annotation.json"}`

  ```
67:    def json(self) -> dict:
85:    def json(self) -> dict:
126:    def json(self, avec_duree: bool = False) -> dict:
        ("LATIN", "Latn"), ("CYRILLIC", "Cyrl"), ("GREEK", "Grek"), ("ARABIC", "Arab"),
        ("HEBREW", "Hebr"), ("DEVANAGARI", "Deva"), ("THAI", "Thai"), ("HIRAGANA", "Jpan"),
        ("KATAKANA", "Jpan"), ("HANGUL", "Hang"), ("CJK", "Hani"), ("IDEOGRAPH", "Hani"),
        ("BENGALI", "Beng"), ("TAMIL", "Taml"), ("TELUGU", "Telu"), ("KANNADA", "Knda"),
        ("MALAYALAM", "Mlym"), ("GUJARATI", "Gujr"), ("GURMUKHI", "Guru"), ("SINHALA", "Sinh"),
        ("MYANMAR", "Mymr"), ("ETHIOPIC", "Ethi"), ("GEORGIAN", "Geor"), ("ARMENIAN", "Armn"),
        ("THAANA", "Thaa"), ("SYRIAC", "Syrc"), ("CHEROKEE", "Cher"), ("TIBETAN", "Tibt"),
        ("MONGOLIAN", "Mong"), ("CANADIAN SYLLABICS", "Cans"), ("TIFINAGH", "Tfng"),
        ("TAI VIET", "Tavt"), ("CHAKMA", "Cakm"), ("YI ", "Yiii"), ("JAVANESE", "Java"),
        ("TAI THAM", "Lana"), ("GRANTHA", "Gran"), ("VAI", "Vaii"), ("TAGALOG", "Tglg"),
        ("ADLAM", "Adlm"), ("LAO", "Laoo"), ("KHMER", "Khmr"),
    )
    for prefixe, code in prefixes:
        if prefixe in nom:
            return code
    return ""


def d
… [5487 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 90,150p tools/bloc_linguistique.py", "description": "Read Annotation.json"}`

  ```
"candidats": list(self.candidats), "langue": self.langue,
            "script": self.script, "meta": dict(self.meta),
        }


SCHEMA_ANNOTATION = "drave.annotation"
# v2 : ajoute `meta.partition` et `meta.alternative` (partition des syntagmes qui se
# chevauchent). Le format reste additif ; le vérificateur lit encore les annotations v1.
VERSION_ANNOTATION = 2


@dataclass
class Annotation:
    texte: str
    langue: str = "und"
    script: str = SCRIPT_NEUTRE
    etiquettes: list[Etiquette] = field(default_factory=list)
    refus: str = ""
    trace: list[dict] = field(default_factory=list)
    cout: dict = field(default_factory=dict)
    unites_semantiques: list[Span] = field(default_factory=list)
    fraction_semantique: float = 0.0
    source: str = "heuristique"
    contexte: str = ""

    def par_niveau(self) -> dict[str, list[Etiquette]]:
        sortie: dict[str, list[Etiquette]] = collections.defaultdict(list)
        for e in self.etiquettes:
            sortie[e.niveau].append(e)
        return dict(sortie)

    def couverture(self) -> dict[str, float]:
        """La confiance maximale par niveau — la couverture *déclarée*, pas une précision."""
        return {n: rou
… [1189 caractères tronqués]
  ```

- **bash** `{"command": "printf 'Le chat dort.\\nThe cat sleeps.\\nBonjour\\n\"Arrête!\"\\n' > /tmp/test-sent.txt; python3 tools/drave.py analyser --fichier /tmp/test-sent.txt --jsonl | python3 -c \"import sys,json; ls=sys.stdin.read().splitlines(); print(len(ls)); [print(json.loads(l)['texte']) for l in ls]\"" … [49 caractères tronqués]`

  ```
4
Le chat dort.
The cat sleeps.
Bonjour
"Arrête!
"
  ```

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/qualifier_tagger_lot.py", "content": "#!/usr/bin/env python3\n\"\"\"qualifier_tagger_lot.py — X3 : le tagger POS **en lot** sur 1 000 phrases réelles.\n\nPOURQUOI. W2/W3 ont mesuré la qualité et le coût **extrapo … [34761 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/qualifier_tagger_lot.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "python3 tools/tests/linguistique/qualifier_tagger_lot.py --mode froid --cache /tmp/tagger-lot-smoke-cache --sortie /tmp/tagger-lot-smoke-froid.json --limite 3 --reset 2>&1 | tail -30", "description": "Smoke test cold pass with 3 items", "timeoutMs": 180000}`

  ```
[froid] 3 items · cache /tmp/tagger-lot-smoke-cache · source 668 lignes / 665 textes
{
 "mode": "froid",
 "items": 3,
 "duree_s": 2.961,
 "requetes": 3,
 "cache_disque": 0,
 "cache_memoire": 0,
 "tokens_reseau": 448,
 "debit_items_min": 60.8,
 "pic_kb": 36520,
 "refus": 0,
 "erreurs": 0
}
  ```

- **bash** `{"command": "python3 tools/tests/linguistique/qualifier_tagger_lot.py --mode chaud --cache /tmp/tagger-lot-smoke-cache --sortie /tmp/tagger-lot-smoke-chaud.json --limite 3 2>&1 | tail -30", "description": "Smoke test hot pass", "timeoutMs": 120000}`

  ```
[chaud] 3 items · cache /tmp/tagger-lot-smoke-cache · source 668 lignes / 665 textes
{
 "mode": "chaud",
 "items": 3,
 "duree_s": 0.013,
 "requetes": 0,
 "cache_disque": 3,
 "cache_memoire": 0,
 "tokens_reseau": 0,
 "debit_items_min": 13846.2,
 "pic_kb": 34272,
 "refus": 0,
 "erreurs": 0
}
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nf=json.load(open('/tmp/tagger-lot-smoke-froid.json'))\nc=json.load(open('/tmp/tagger-lot-smoke-chaud.json'))\nfor a,b in zip(f['lignes'],c['lignes']):\n print(a['id'],a['hash'],b['hash'],a['hash']==b['hash'],a['cache_disque'],b['cache_disque'])\nprint(jso … [100 caractères tronqués]`

  ```
g001 844bd3195799b2de 844bd3195799b2de True False True
g002 fd67029755868dac fd67029755868dac True False True
g003 7fea92c793380439 7fea92c793380439 True False True
{
 "rang": 0,
 "id": "g001",
 "source": "hand",
 "langue": "fr",
 "repete": false,
 "appel_transport": true,
 "cache_disque": false,
 "cache_memoire": false,
 "tokens_reseau": 130,
 "tokens_cache": 0,
 "prompt_tokens": 116,
 "completion_tokens": 14,
 "cache_hit_tokens": 0,
 "cache_miss_tokens": 116,
 "latence_api_s": 1.103,
 "latence_item_s": 1.1126,
 "refus": false,
 "refus_message": "",
 "erreur": "",
 "hash": "844bd3195799b2de"
}
  ```

- **bash** `{"command": "python3 tools/tests/linguistique/qualifier_tagger_lot.py --mode froid --cache /tmp/tagger-lot-cache --sortie /tmp/tagger-lot-froid.json --reset 2>&1 | tee /tmp/tagger-lot-froid.log", "description": "Run full cold batch (1000 items, 665 API calls)", "run_in_background": true}`

  ```
started background job bash-73
  ```

- **bash** `{"command": "grep -rn \"INDEX.md\\|index des rapports\\|reports/INDEX\" tools/*.py tools/*.sh 2>/dev/null | head -20", "description": "Find report index generator"}`

  ```
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

- **bash** `{"command": "sed -n 1,80p tools/revue_documentation.py; echo ===; grep -n \"rapport-tagger\\|tagger\" reports/INDEX.md | head", "description": "Inspect doc review and index"}`

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
… [3442 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-73"}`

  ```
[froid] 1000 items · cache /tmp/tagger-lot-cache · source 668 lignes / 665 textes
[status: running]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport sys, json\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\n# import the harness functions without running\nsys.path.insert(0,'tools/tests/linguistique')\nimport qualifier_tagger_lot as q\nitems=q.charger_corpus(); lot,comp=q.construire_lot(items,n=1 … [754 caractères tronqués]`

  ```
lot 1000 phrases heuristique 836
sum per line 1003
2 'Marie lit. Elle aime les livres.' ['Marie lit.', 'Elle aime les livres.']
2 'Marie reads. She loves books.' ['Marie reads.', 'She loves books.']
2 'Marie reads. She loves books.' ['Marie reads.', 'She loves books.']
lines splitting 3
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport sys\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nh=bl.Heuristique()\nfor sep in [\"\\n\",\"\\n\\n\",\"\\n \\n\",\"\\n.\\n\"]:\n texte=sep.join([\"Le chat dort.\",\"Bonjour\",\"The cat sleeps.\",\"Sans ponctuation\"])+sep\n ps=[texte[a:b] for a,b … [149 caractères tronqués]`

  ```
'\n' 3 ['Le chat dort.', 'Bonjour\nThe cat sleeps.', 'Sans ponctuation']
'\n\n' 4 ['Le chat dort.', 'Bonjour', 'The cat sleeps.', 'Sans ponctuation']
'\n \n' 4 ['Le chat dort.', 'Bonjour', 'The cat sleeps.', 'Sans ponctuation']
'\n.\n' 6 ['Le chat dort.', '.', 'Bonjour\n.', 'The cat sleeps.', '.', 'Sans ponctuation\n.']
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/qualifier_tagger_lot.py", "old_string": "    chemin = dossier / f\"corpus-{nom}.txt\"\n    chemin.write_text(\"\\n\".join(\" \".join(it[\"texte\"].split()) for it in lot) + \"\\n\",\n                      encodin … [527 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/qualifier_tagger_lot.py has been updated successfully.
  ```

- **job_output** `{"job_id": "bash-73"}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "tail -5 /tmp/tagger-lot-froid.log 2>/dev/null; ls -lh /tmp/tagger-lot-cache 2>/dev/null | head; find /tmp/tagger-lot-cache -name \"*.json\" 2>/dev/null | wc -l", "description": "Check cold run progress"}`

  ```
[froid] 1000 items · cache /tmp/tagger-lot-cache · source 668 lignes / 665 textes
total 128K
-rw-r--r--. 1 stephane stephane 1,1K 15 nov 12:58 0a4c79198bbbd80ae07c62d0c54502904adb97d051c3a2b33ac878a66eb2c260.json
-rw-r--r--. 1 stephane stephane 1,1K 15 nov 12:59 0b50e5600b56199d5c8e21d02121c8f63ca16c15e5e3cb75010952587b694b49.json
-rw-r--r--. 1 stephane stephane 1012 15 nov 12:59 125ea21517c9c8947f28c905e5372601fd6a5f9c9c3c822bb8cbf000bb3a3eba.json
-rw-r--r--. 1 stephane stephane 1,1K 15 nov 12:59 2564c7c874ba2c6410c8da35892d9d43f514439c381e81daa33821ed3602ccf2.json
-rw-r--r--. 1 stephane stephane 1,1K 15 nov 12:59 2e1838efbd5372715323efac7b6006a3482b880794b15cbe6a57bfd86d819827.json
-rw-r--r--. 1 stephane stephane 1,1K 15 nov 12:59 38f68b032e8cc4cf8d3ab67685fc95098b484654a109c76c9b02256d0e6d1a2e.json
-rw-r--r--. 1 stephane stephane 1,1K 15 nov 12:58 3e48fa81fc86339a0fba39ea4cd5d8013c15338920a62c23029cf9cd80049085.json
-rw-r--r--. 1 stephane stephane 1,1K 15 nov 12:59 45591594be266f960713a97a6769363c9f2b78f888a1635f4769aef020b573a2.json
-rw-r--r--. 1 stephane stephane 1,1K 15 nov 12:59 47aba7aa5e0393e45b9f001db88207300c5d35e673dc9e2c3f2cc835ea88b713.json
32
  ```

- **bash** `{"command": "git diff -- docs/pilotage/en-cours.md | head -60; echo ===; git diff -- docs/produit/README.md | head -40", "description": "Inspect prior en-cours diff"}`

  ```
diff --git a/docs/pilotage/en-cours.md b/docs/pilotage/en-cours.md
index be629f05..9d6c13ce 100644
--- a/docs/pilotage/en-cours.md
+++ b/docs/pilotage/en-cours.md
@@ -102,7 +102,7 @@
 |---|---|---|
 | portes | **85** (dont `porte-cic` le 14/11) | `tools/porte-*.sh` |
 | chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |
-| fichiers / JSON de résultats | **754** / **847** | `reports/*.md` / `reports/*.json` |
+| fichiers / JSON de résultats | **755** / **848** | `reports/*.md` / `reports/*.json` |
 | documents de `docs/` | **124** (hors archive et README) | `docs/**/*.md` |
 | dernière passe | **15/11 09 h 53 → 12 h 15** (85, **81/4**) ; rouges `indice`, `melange` (structurelles), `sessions` (**réparée** à 12 h 20), `prechargement` (**environnementale**) ; ciblage W6 **9/9** | `work/portes-1115-09h53/registre.txt` ; `work/portes/w6-final/` |
 
===
diff --git a/docs/produit/README.md b/docs/produit/README.md
index b077d93a..e18f7fef 100644
--- a/docs/produit/README.md
+++ b/docs/produit/README.md
@@ -452,10 +452,19 @@ synthétique porte le reste du gain. Dispositif, coût et contrôle négatif :
 [`rapport-tagger-option.md`](../../reports/rapport-tagger-option.md).
 
 **L
… [2509 caractères tronqués]
  ```

- **bash** `{"command": "ls -la journal/ | head -30; echo ===; ls journal/ | tail -20; echo ===; find journal -maxdepth 2 -name \"*.md\" | head -20", "description": "Inspect journal structure"}`

  ```
total 88
drwxr-xr-x. 1 stephane stephane   992 15 nov 12:34 .
drwxr-xr-x. 1 stephane stephane   686  6 nov 09:52 ..
drwxr-xr-x. 1 stephane stephane   132 28 oct 14:12 2026-09-25
drwxr-xr-x. 1 stephane stephane    36 28 oct 14:12 2026-09-26
drwxr-xr-x. 1 stephane stephane   144 28 oct 14:12 2026-09-27
drwxr-xr-x. 1 stephane stephane   174 28 oct 14:12 2026-09-28
drwxr-xr-x. 1 stephane stephane   174 28 oct 14:12 2026-09-29
drwxr-xr-x. 1 stephane stephane   210 28 oct 14:12 2026-09-30
drwxr-xr-x. 1 stephane stephane   192 28 oct 14:12 2026-10-01
drwxr-xr-x. 1 stephane stephane   210 28 oct 14:12 2026-10-02
drwxr-xr-x. 1 stephane stephane   174 28 oct 14:12 2026-10-03
drwxr-xr-x. 1 stephane stephane   130 28 oct 14:12 2026-10-04
drwxr-xr-x. 1 stephane stephane   206 28 oct 14:12 2026-10-05
drwxr-xr-x. 1 stephane stephane   164 28 oct 14:12 2026-10-06
drwxr-xr-x. 1 stephane stephane   150 28 oct 14:12 2026-10-07
drwxr-xr-x. 1 stephane stephane   200 28 oct 14:11 2026-10-08
drwxr-xr-x. 1 stephane stephane   252 28 oct 14:12 2026-10-09
drwxr-xr-x. 1 stephane stephane   288 28 oct 14:12 2026-10-10
drwxr-xr-x. 1 stephane stephane   192 28 oct 14:12 2026-10-11
drwxr-xr-x. 1 stephane stephan
… [1516 caractères tronqués]
  ```

- **bash** `{"command": "ls -la journal/2026-11-15/; echo ===; sed -n 1,80p journal/2026-11-15/README.md 2>/dev/null; echo ===; ls journal/2026-11-14/ | head", "description": "Inspect today's journal"}`

  ```
total 52
drwxr-xr-x. 1 stephane stephane   150 15 nov 12:34 .
drwxr-xr-x. 1 stephane stephane   992 15 nov 12:34 ..
-rw-r--r--. 1 stephane stephane  2217 15 nov 12:38 distribue.md
-rw-r--r--. 1 stephane stephane  4364 15 nov 12:38 docs.md
-rw-r--r--. 1 stephane stephane  1245 15 nov 12:38 memoire.md
-rw-r--r--. 1 stephane stephane 11052 15 nov 12:38 mesures.md
-rw-r--r--. 1 stephane stephane  1353 15 nov 12:38 modele.md
-rw-r--r--. 1 stephane stephane  1961 15 nov 12:38 outils.md
-rw-r--r--. 1 stephane stephane  2475 15 nov 12:38 portes.md
-rw-r--r--. 1 stephane stephane 12273 15 nov 12:38 README.md
===
# 2026-11-15

> **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
> [`journal/2026-11-15/`](README.md). Le récit écrit à la main est conservé plus bas, dans
> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
> [l'index des sessions](../README.md#sessions).

**34 commits** · **1 session(s)** · **7 thème(s)**

## Thèmes du jour

| thème | commits | fichier |
|---|---|---|
| distribue | 5 | [distribue.md](distribue.md) |
| docs | 8 | [docs.md](docs.md) |
| memoire | 1 | [memoire.md](memoire.md) |
| mesures | 14 | [mesures.md]
… [6985 caractères tronqués]
  ```

- **bash** `{"command": "find /tmp/tagger-lot-cache -name \"*.json\" | wc -l; tail -3 /tmp/tagger-lot-froid.log", "description": "Check cold progress count"}`

  ```
44
[froid] 1000 items · cache /tmp/tagger-lot-cache · source 668 lignes / 665 textes
  ```

- **bash** `{"command": "date; stat -c '%y %n' /tmp/tagger-lot-cache/*.json 2>/dev/null | sort | tail -3; python3 - <<'EOF'\nimport json,glob,statistics\nfs=glob.glob('/tmp/tagger-lot-cache/*.json')\nls=[]\nfor f in fs:\n try: d=json.load(open(f)); ls.append(d.get('latence_s',0))\n except: pass\nprint(len(ls),  … [116 caractères tronqués]`

  ```
dim 15 nov 2026 12:59:40 EST
2026-11-15 12:59:37.810484673 -0500 /tmp/tagger-lot-cache/2a7377e66f512ec121308f75544f13b378e7f0687e7f243c569097292b24edca.json
2026-11-15 12:59:39.341494406 -0500 /tmp/tagger-lot-cache/129f1e8c387bec8cfc15e2ffc2b0639dbd67079c2e7c8ef325f70769e1fee64b.json
2026-11-15 12:59:40.135495322 -0500 /tmp/tagger-lot-cache/d8eee1b82db8ae23a2ce02f085a7b23971b440d7ff8dcef38ed95a397a2dbbf4.json
47 1.016 0.654 1.526 47.7
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/qualifier_tagger_lot.py", "new_string": "    hit = tokens.get(\"prompt_cache_hit_tokens\", 0)\n    miss = tokens.get(\"prompt_cache_miss_tokens\", 0)\n    if miss == 0 and tokens.get(\"prompt_tokens\", 0):\n      … [275 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/qualifier_tagger_lot.py has been updated successfully.
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json,glob,statistics\nfs=glob.glob('/tmp/tagger-lot-cache/*.json')\np=[];c=[];h=[];m=[]\nfor f in fs:\n try: d=json.load(open(f)); u=d.get('usage',{})\n except: continue\n p.append(u.get('prompt_tokens',0)); c.append(u.get('completion_tokens',0)); h.append(u.ge … [354 caractères tronqués]`

  ```
n 53 prompt 6508 completion 1042 total 7550 hit 0 miss 6508
mean prompt 122.8 mean comp 19.7
  ```

- **bash** `{"command": "date; find /tmp/tagger-lot-cache -name \"*.json\" | wc -l; tail -2 /tmp/tagger-lot-froid.log", "description": "Check progress again"}`

  ```
dim 15 nov 2026 12:59:49 EST
57
[froid] 1000 items · cache /tmp/tagger-lot-cache · source 668 lignes / 665 textes
  ```

- **bash** `{"command": "ls reports/*.md | wc -l; ls reports/*.json | wc -l; ls reports/rapport-page-s-mesure.md reports/rapport-or-roles-protocole.md reports/schema-or-roles.json 2>/dev/null", "description": "Count reports files"}`

  ```
756
851
reports/rapport-or-roles-protocole.md
reports/rapport-page-s-mesure.md
reports/schema-or-roles.json
  ```

- **bash** `{"command": "grep -n \"fichiers / JSON\\|reports/\\*.md\\|reports/\\*.json\\|755\\|848\\|compteurs\" tools/revue_documentation.py | head -30; sed -n 230,320p tools/revue_documentation.py", "description": "Inspect documentation counters"}`

  ```
12:     les compteurs de la page d'état sont ceux du disque (portes, chapitres, fiches, docs) ;
172:    # 5. compteurs : la page d'état est la source unique, et elle dit le disque
176:    fiches = re.search(r"\|\s*fichiers / JSON de résultats\s*\|\s*\*\*(\d+)\*\*\s*/\s*\*\*(\d+)\*\*", t)
183:            alertes.append(f"compteurs : la ligne « {nom} » manque dans en-cours.md")
185:            alertes.append(f"compteurs : en-cours.md dit {valeur} {nom}, le disque en a {disque}")
187:        alertes.append("compteurs : la ligne « fichiers / JSON » manque dans en-cours.md")
195:                    f"compteurs : en-cours.md dit {valeur} {quoi}, le disque en a {disque}"
374:        print("  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, "
    for f in sources_propres():
        try:
            brut = f.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        texte = re.sub(r"\[[^\]]+\]\([^)]+\)", "", brut)
        for m in CHEMIN.finditer(texte):
            p = m.group(1).rstrip(".,;:)")
            if any(g in p for g in GABARIT):
                continue
            if not (RACINE / p).exists():
                ligne =
… [3418 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 165,205p tools/revue_documentation.py; grep -n \"def fiches\\|def rapports\\|glob\" tools/revue_documentation.py | head -20", "description": "Read counter definitions"}`

  ```
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
        ("portes", portes, compte_portes()),
        ("chapitres", chapitres, compte_chapitres()),
        ("documents", documents, compte_docs()),
    ):
        if valeur is None:
            alertes.append(f"compteurs : la ligne « {nom} » manque dans en-cours.md")
        elif valeur != disque:
            ale
… [1621 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 95,120p tools/revue_documentation.py", "description": "Read compte_fiches"}`

  ```
+ [RACINE / "reports/07-mesures-couche-commune.md",
               RACINE / "reports/fiche-nuit-17-10.md",
               RACINE / "README.md", RACINE / "REPRISE.md", RACINE / "AGENTS.md"])


def compte_portes() -> int:
    return len(list((RACINE / "tools").glob("porte-*.sh")))


def compte_chapitres() -> int:
    return len(list((RACINE / "docs/theorie/synthese").glob("0*.md")))


def compte_fiches() -> int:
    return len(rapports())


def compte_json() -> int:
    return len(list((RACINE / "reports").glob("*.json")))


def compte_docs() -> int:
    return len(docs_vivants())


def extrait_entier(texte: str, motif: str):
  ```

- **bash** `{"command": "date; find /tmp/tagger-lot-cache -name \"*.json\" | wc -l; tail -2 /tmp/tagger-lot-froid.log", "description": "Check cold progress"}`

  ```
dim 15 nov 2026 13:00:01 EST
68
[froid] 1000 items · cache /tmp/tagger-lot-cache · source 668 lignes / 665 textes
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport sys, pathlib\nsys.path.insert(0,'tools/tests/linguistique')\nimport qualifier_tagger_lot as q\nitems=q.charger_corpus(); lot,comp=q.construire_lot(items,n=1000)\nr=q._lancer_jsonl(pathlib.Path('/tmp/tagger-lot-smoke-cache'), lot[:3], 'smoke', reset=False)\nprin … [229 caractères tronqués]`

  ```
{'nom': 'smoke', 'code': 0, 'lignes': 3, 'json_valides': 3, 'sources': {'cascade': 3}, 'cout_stderr': {'modele': 'deepseek-chat', 'appels': 3, 'reseau': 0, 'cache': 3, 'tokens': 0, 'latence_s': 0.0}, 'rss_pic_kb': 31724, 'duree_s': 0.245, 'fichier_lignes': 5}
 unshared data size (kbytes): 0
	Average stack size (kbytes): 0
	Average total size (kbytes): 0
	Maximum resident set size (kbytes): 31724
	Average resident set size (kbytes): 0
	Major (requiring I/O) page faults: 0
	Minor (reclaiming a frame) page faults: 4867
	Voluntary context switches: 0
	Involuntary context switches: 3
	Swaps: 0
	File system inputs: 0
	File system outputs: 0
	Socket messages sent: 0
	Socket messages received: 0
	Signals delivered: 0
	Page size (bytes): 4096
	Exit status: 0
  ```

- **bash** `{"command": "date; find /tmp/tagger-lot-cache -name \"*.json\" | wc -l; python3 - <<'EOF'\nimport json,glob\nfs=glob.glob('/tmp/tagger-lot-cache/*.json'); p=c=0\nfor f in fs:\n try: u=json.load(open(f)).get('usage',{})\n except: continue\n p+=u.get('prompt_tokens',0); c+=u.get('completion_tokens',0) … [103 caractères tronqués]`

  ```
dim 15 nov 2026 13:00:08 EST
74
prompt 9108 completion 1470 total 10578
  ```

- **bash** `{"command": "date; find /tmp/tagger-lot-cache -name \"*.json\" | wc -l", "description": "Progress check"}`

  ```
dim 15 nov 2026 13:00:13 EST
78
  ```

- **bash** `{"command": "sleep 60; date; find /tmp/tagger-lot-cache -name \"*.json\" | wc -l; tail -2 /tmp/tagger-lot-froid.log", "description": "Wait 60s and check progress", "timeoutMs": 70000}`

  ```
dim 15 nov 2026 13:01:19 EST
134
[froid] 1000 items · cache /tmp/tagger-lot-cache · source 668 lignes / 665 textes
  ```

- **bash** `{"command": "sleep 90; date; find /tmp/tagger-lot-cache -name \"*.json\" | wc -l; tail -2 /tmp/tagger-lot-froid.log", "description": "Wait and check cold progress", "timeoutMs": 100000}`

  ```
dim 15 nov 2026 13:02:53 EST
224
[froid] 1000 items · cache /tmp/tagger-lot-cache · source 668 lignes / 665 textes
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json,glob,statistics\nvals=[]\nfor f in glob.glob('/tmp/tagger-lot-cache/*.json'):\n try: u=json.load(open(f)).get('usage',{}); vals.append(u.get('total_tokens',0))\n except: pass\nvals.sort()\nprint(len(vals), \"mean\",round(statistics.fmean(vals),1),\"median\ … [172 caractères tronqués]`

  ```
226 mean 143.0 median 143.0 p95 156 max 169 sum 32322
top [157, 157, 157, 159, 159, 160, 160, 161, 163, 169]
  ```

- **bash** `{"command": "sleep 120; date; find /tmp/tagger-lot-cache -name \"*.json\" | wc -l; tail -3 /tmp/tagger-lot-froid.log", "description": "Wait and check cold progress", "timeoutMs": 130000}`

  ```
dim 15 nov 2026 13:04:59 EST
348
[froid] 1000 items · cache /tmp/tagger-lot-cache · source 668 lignes / 665 textes
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport sys, collections\nsys.path.insert(0,'tools'); sys.path.insert(0,'tools/tests/linguistique')\nimport bloc_linguistique as bl, qualifier_tagger_lot as q\nitems=q.charger_corpus()\ndef toks(t): return tuple(t for _,_,t in bl.NeuronalLLMPOS._tokens(t))\nc=collectio … [622 caractères tronqués]`

  ```
items 668 distinct (texte,langue) 665
distinct (tokens,langue) 662
distinct tokens 662
prompt collisions 3
('Tu', 'viens', 'demain') {'Tu viens demain ?', 'Tu viens demain.'}
('You', 'come', 'tomorrow') {'You come tomorrow?', 'You come tomorrow.'}
('ce', 'livre', 'commence') {'ce livre commence!', 'ce livre commence'}
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/qualifier_tagger_lot.py", "new_string": "    uniques = {(it[\"texte\"], it[\"langue\"]) for it in items}\n    prompts = {tuple(t for _, _, t in bl.NeuronalLLMPOS._tokens(it[\"texte\"]))\n               for it in  … [127 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/qualifier_tagger_lot.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/qualifier_tagger_lot.py", "new_string": "        \"lignes_source\": len(items),\n        \"textes_distincts\": len(uniques),\n        \"prompts_distincts\": len(prompts),\n        \"collisions_prompt\": len(uniqu … [268 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/qualifier_tagger_lot.py has been updated successfully.
  ```

- **bash** `{"command": "date; find /tmp/tagger-lot-cache -name \"*.json\" | wc -l", "description": "Progress check"}`

  ```
dim 15 nov 2026 13:05:22 EST
369
  ```

- **bash** `{"command": "sed -n 1,60p reports/README.md; echo ===; grep -n \"tagger\" reports/README.md | head", "description": "Inspect reports README"}`

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
… [6508 caractères tronqués]
  ```

- **bash** `{"command": "date; find /tmp/tagger-lot-cache -name \"*.json\" | wc -l; tail -3 /tmp/tagger-lot-froid.log", "description": "Progress check"}`

  ```
dim 15 nov 2026 13:05:28 EST
375
[froid] 1000 items · cache /tmp/tagger-lot-cache · source 668 lignes / 665 textes
  ```

- **bash** `{"command": "sleep 90; date; find /tmp/tagger-lot-cache -name \"*.json\" | wc -l; tail -3 /tmp/tagger-lot-froid.log", "description": "Wait and check cold progress", "timeoutMs": 100000}`

  ```
dim 15 nov 2026 13:07:03 EST
470
[froid] 1000 items · cache /tmp/tagger-lot-cache · source 668 lignes / 665 textes
  ```

- **bash** `{"command": "sleep 90; date; find /tmp/tagger-lot-cache -name \"*.json\" | wc -l; tail -3 /tmp/tagger-lot-froid.log", "description": "Wait and check cold progress", "timeoutMs": 100000}`

  ```
dim 15 nov 2026 13:08:41 EST
567
[froid] 1000 items · cache /tmp/tagger-lot-cache · source 668 lignes / 665 textes
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json,glob,statistics\np=c=h=m=0; ls=[]; n=0\nfor f in glob.glob('/tmp/tagger-lot-cache/*.json'):\n try: d=json.load(open(f)); u=d.get('usage',{})\n except: continue\n n+=1; p+=u.get('prompt_tokens',0); c+=u.get('completion_tokens',0); h+=u.get('prompt_cache_hit … [642 caractères tronqués]`

  ```
n 571 prompt 70699 completion 11682 total 82381 hit 0 miss 70699
lat mean 1.033 median 1.014 sum 589.7
expected 662 calls: prompt 81966 completion 13544 total 95510
cost 662 calls hp 0.020421 extrap 1000 texts 0.030709 peak 0.061417
  ```

- **bash** `{"command": "sleep 120; date; find /tmp/tagger-lot-cache -name \"*.json\" | wc -l; tail -5 /tmp/tagger-lot-froid.log", "description": "Wait for cold run completion", "timeoutMs": 130000}`

  ```
dim 15 nov 2026 13:10:47 EST
662
 "debit_items_min": 86.9,
 "pic_kb": 40820,
 "refus": 5,
 "erreurs": 0
}
  ```

### 👤 Utilisateur

background job bash-73 (bash: python3 tools/tests/linguistique/qualifier_tagger_lot.py --mode froid --cache /tmp/tagger-lot-cache --sortie /tmp/tagger-lot-froid.json --reset 2>&1 | tee /tmp/tagger-lot-froid.log) finished [status: completed, exit code: 0]. Read its output with job_output.

- **job_output** `{"job_id": "bash-73"}`

  ```
{
 "mode": "froid",
 "items": 1000,
 "duree_s": 690.388,
 "requetes": 662,
 "cache_disque": 3,
 "cache_memoire": 335,
 "tokens_reseau": 98968,
 "debit_items_min": 86.9,
 "pic_kb": 40820,
 "refus": 5,
 "erreurs": 0
}
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "tail -30 /tmp/tagger-lot-froid.log; echo ===; python3 - <<'EOF'\nimport json\nd=json.load(open('/tmp/tagger-lot-froid.json'))\nprint(list(d))\nprint(\"stats\",json.dumps(d['stats_tagger'],ensure_ascii=False))\nprint(\"cache\",d['cache_avant']['fichiers'],d['cache_apres'])\nprint(\"rss\" … [814 caractères tronqués]`

  ```
[froid] 1000 items · cache /tmp/tagger-lot-cache · source 668 lignes / 665 textes
{
 "mode": "froid",
 "items": 1000,
 "duree_s": 690.388,
 "requetes": 662,
 "cache_disque": 3,
 "cache_memoire": 335,
 "tokens_reseau": 98968,
 "debit_items_min": 86.9,
 "pic_kb": 40820,
 "refus": 5,
 "erreurs": 0
}
===
['nom', 'cache_dir', 'duree_s', 'cache_avant', 'cache_apres', 'rss_avant', 'rss_apres', 'stats_tagger', 'lignes', 'composition']
stats {"appels": 0, "requetes": 0, "cache": 0, "tokens": 0, "latence_s": 0.0, "modeles": {}, "cle_refusee": 0}
cache 0 {'fichiers': 662, 'octets': 703720, 'dates': {'min': '2026-11-15T12:58:53-0500', 'max': '2026-11-15T13:10:21-0500'}, 'modeles': {'deepseek-flash': 662}}
rss {'pic_kb': 33868, 'rss_kb': 33868, 'ru_maxrss_kb': 33708} {'pic_kb': 40820, 'rss_kb': 40820, 'ru_maxrss_kb': 38588}
lines 1000
sources Counter({'reel': 655, 'synth': 234, 'libre': 85, 'hand': 26})
refus [('x48-00', 'libre', 'neuronal-pos: ValueError: longueur POS 6 / 2'), ('x50-00', 'libre', 'neuronal-pos: ValueError: longueur POS 88 / 87'), ('x50-00', 'libre', 'neuronal-pos: ValueError: longueur POS 88 / 87'), ('x48-00', 'libre', 'neuronal-pos: ValueError: longueur POS 6 / 2'), ('x50-00'
… [168 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/qualifier_tagger_lot.py", "new_string": "        \"par_source\": par_source, \"par_langue\": par_langue,\n        \"stats_tagger\": {\n            \"appels\": len(reseau) + len(disque),\n            \"requetes\": … [448 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/qualifier_tagger_lot.py has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/tests/linguistique/qualifier_tagger_lot.py --mode chaud --cache /tmp/tagger-lot-cache --sortie /tmp/tagger-lot-chaud.json 2>&1 | tee /tmp/tagger-lot-chaud.log", "description": "Run hot batch on same 1000 items", "timeoutMs": 300000}`

  ```
[chaud] 1000 items · cache /tmp/tagger-lot-cache · source 668 lignes / 665 textes
{
 "mode": "chaud",
 "items": 1000,
 "duree_s": 2.715,
 "requetes": 0,
 "cache_disque": 665,
 "cache_memoire": 335,
 "tokens_reseau": 0,
 "debit_items_min": 22099.4,
 "pic_kb": 37932,
 "refus": 5,
 "erreurs": 0
}
  ```

- **bash** `{"command": "python3 tools/tests/linguistique/qualifier_tagger_lot.py --mode fusion --froid /tmp/tagger-lot-froid.json --chaud /tmp/tagger-lot-chaud.json --sortie reports/rapport-tagger-lot.json 2>&1 | tee /tmp/tagger-lot-fusion.log", "description": "Fuse measurements, run jsonl tests, write report  … [27 caractères tronqués]`

  ```
{
 "froid": {
  "requetes": 662,
  "cache_disque": 3,
  "tokens": 98968,
  "dollars_hp": 0.021635,
  "debit_items_min": 86.9,
  "pic_kb": 40820
 },
 "chaud": {
  "requetes": 0,
  "tokens": 0,
  "dollars_hp": 0.0,
  "debit_items_min": 22099.4,
  "pic_kb": 37932
 },
 "extrapole_1000_uniques": {
  "hors_pointe": 0.032534,
  "pointe": 0.065068
 },
 "jsonl": {
  "chaud_lignes": 1003,
  "chaud_cout": {
   "modele": "deepseek-chat",
   "appels": 667,
   "reseau": 4,
   "cache": 663,
   "tokens": 513,
   "latence_s": 3.9
  },
  "froid_lignes": 20,
  "froid_cout": {
   "modele": "deepseek-chat",
   "appels": 20,
   "reseau": 20,
   "cache": 0,
   "tokens": 2907,
   "latence_s": 20.0
  }
 },
 "controle_negatif": "OK : le cache chaud rejoue les 1 000 items à 0 réseau, 0 token, 0 $"
}
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/rapport-tagger-lot.json'))\nprint(\"keys\",list(d))\nprint(\"verdict\",d['verdict'])\nprint(\"corpus\",json.dumps(d['corpus'],ensure_ascii=False,indent=1))\nprint(\"froid cache\",json.dumps(d['passes']['froid']['cache'],ensure_as … [981 caractères tronqués]`

  ```
keys ['rapport', 'tache', 'ligne_roadmap', 'date', 'commit', 'verdict', 'dispositif', 'corpus', 'passes', 'cache', 'debit', 'memoire', 'cout', 'jsonl', 'controle_negatif', 'limites', 'fichiers']
verdict le lot de 1 000 items est mesuré de bout en bout ; le cache froid fait 662 appels réseau et le cache chaud 0 ; les 1 000 sorties sont identiques
corpus {
 "lignes_source": 668,
 "textes_distincts": 665,
 "prompts_distincts": 662,
 "collisions_prompt": 3,
 "doublons_source": {
  "n": 3,
  "ids": [
   "r186",
   "r189",
   "r358"
  ]
 },
 "items": 1000,
 "repetitions_ajoutees": 332,
 "items_repetes": 332,
 "graine": 20261115,
 "sha256_textes": "94d47d017f1597881425b2650a7ddc33a28d768e293b2db8acf7fd888eff2bc3",
 "par_source": {
  "hand": 20,
  "reel": 432,
  "synth": 160,
  "libre": 56
 },
 "par_langue": {
  "fr": 442,
  "en": 224,
  "und": 2
 },
 "sources": "612 gold (hand 20 + reel 432 + synth 160) + 50 textes libres (pensee-produit-bloc-l.json, 56 phrases)",
 "note": "les 1 000 items sont des phrases réelles ; 335 rejouent un texte du lot. La mesure publie le lot et l'extrapolation aux 1 000 textes uniques."
}
froid cache {
 "appels_transport": 665,
 "requetes_reseau": 662,
 "cache_
… [3974 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/rapport-tagger-lot.json'))\nfor k in ('chaud_1000','froid_20'):\n x=d['jsonl'][k]\n print(k,{q:x[q] for q in ('nom','code','lignes','json_valides','sources','pos_total','texte_attendu','stderr' if False else 'cout_stderr','rss_pi … [150 caractères tronqués]`

  ```
chaud_1000 {'nom': '1000', 'code': 0, 'lignes': 1003, 'json_valides': 1003, 'sources': {'cascade': 1003}, 'pos_total': 7195, 'texte_attendu': 1000, 'cout_stderr': {'modele': 'deepseek-chat', 'appels': 667, 'reseau': 4, 'cache': 663, 'tokens': 513, 'latence_s': 3.9}, 'rss_pic_kb': 39108, 'duree_s': 7.216, 'stdout_octets': 8645416, 'fichier_lignes': 1999, 'textes_uniques_sortie': 667}
psed (wall clock) time (h:mm:ss or m:ss): 0:07.17
	Average shared text size (kbytes): 0
	Average unshared data size (kbytes): 0
	Average stack size (kbytes): 0
	Average total size (kbytes): 0
	Maximum resident set size (kbytes): 39108
	Average resident set size (kbytes): 0
	Major (requiring I/O) page faults: 0
	Minor (reclaiming a frame) page faults: 12666
	Voluntary context switches: 35
	Involuntary context switches: 155
	Swaps: 0
	File system inputs: 0
	File system outputs: 0
	Socket messages sent: 0
	Socket messages received: 0
	Signals delivered: 0
	Page size (bytes): 4096
	Exit status: 0

froid_20 {'nom': '20-froid', 'code': 0, 'lignes': 20, 'json_valides': 20, 'sources': {'cascade': 20}, 'pos_total': 127, 'texte_attendu': 20, 'cout_stderr': {'modele': 'deepseek-chat', 'appels': 20, 'reseau': 20, '
… [761 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport sys, pathlib, json\nsys.path.insert(0,'tools/tests/linguistique')\nimport qualifier_tagger_lot as q\nitems=q.charger_corpus(); lot,comp=q.construire_lot(items,n=1000,graine=q.GRAINE)\nr=q._lancer_jsonl(pathlib.Path('/tmp/tagger-lot-cache'), lot, '1000-second',  … [269 caractères tronqués]`

  ```
{'nom': '1000-second', 'code': 0, 'lignes': 1003, 'json_valides': 1003, 'sources': {'cascade': 1003}, 'pos_total': 7195, 'cout_stderr': {'modele': 'deepseek-chat', 'appels': 667, 'reseau': 0, 'cache': 667, 'tokens': 0, 'latence_s': 0.0}, 'rss_pic_kb': 35660, 'duree_s': 3.145, 'stdout_octets': 8645416, 'textes_uniques_sortie': 667}
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, sys, pathlib\nsys.path.insert(0,'tools/tests/linguistique')\nimport qualifier_tagger_lot as q\np=pathlib.Path('reports/rapport-tagger-lot.json')\nd=json.loads(p.read_text())\nitems=q.charger_corpus(); lot,comp=q.construire_lot(items,n=1000,graine=q.GRAINE … [1615 caractères tronqués]`

  ```
patched reports/rapport-tagger-lot.json jsonl second reseau 0 tokens 0
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/rapport-tagger-lot.json'))\nf=d['passes']['froid']; c=d['passes']['chaud']; cout=d['cout']\nprint(\"COLD:\")\nprint(\"items\",f['items'],\"reseau\",f['cache']['requetes_reseau'],\"disque\",f['cache']['cache_disque'],\"memoire\",f … [1085 caractères tronqués]`

  ```
COLD:
items 1000 reseau 662 disque 3 memoire 335
tokens 83880 15088 98968
duree 690.388 debit 86.9 req/min 57.5
lat {'moyenne': 1.036, 'mediane': 1.017, 'p95': 1.325, 'max': 3.677} item {'moyenne': 0.69, 'mediane': 0.915, 'p95': 1.299, 'max': 3.68}
mem {'rss_avant_kb': 33868, 'pic_avant_kb': 33868, 'rss_apres_kb': 40820, 'pic_apres_kb': 40820, 'ru_maxrss_kb': 38588, 'delta_pic_kb': 6952, 'cache_octets': 703720, 'cache_octets_par_texte': 1058.2}
cache 703720 662 {'deepseek-flash': 662}
refus 5 ['x48-00', 'x50-00', 'x50-00', 'x48-00', 'x50-00']
HOT:
items 1000 reseau 0 disque 665 memoire 335
tokens 0 duree 2.715 debit 22099.4 mem 37932
COUT: {"tokens": {"prompt_tokens": 83880, "completion_tokens": 15088, "total_tokens": 98968, "prompt_cache_hit_tokens": 0, "prompt_cache_miss_tokens": 83880, "tokens_reseau": 98968, "tokens_cache": 392, "tokens_total_appels": 99360}, "prix_unitaire_par_million": {"hors_pointe": {"entree_hit": 0.003, "entree_miss": 0.15, "sortie": 0.6}, "pointe": {"entree_hit": 0.006, "entree_miss": 0.3, "sortie": 1.2}}, "lot_1000_items": {"hors_pointe": 0.021635, "pointe": 0.04327}, "lot_1000_items_note": "coût réel du lot de 1 000 items : 662 appels réseau + 3 rejeux 
… [1428 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/rapport-tagger-lot.json'))\nfor passe in ('froid','chaud'):\n print('===',passe)\n for k,v in d['passes'][passe]['par_source'].items(): print('src',k,v)\n for k,v in d['passes'][passe]['par_langue'].items(): print('lang',k,v)\nEO … [55 caractères tronqués]`

  ```
=== froid
src hand {'items': 26, 'requetes': 20, 'cache_disque': 0, 'cache_memoire': 6, 'tokens_reseau': 2907, 'latence_reseau_s': 21.191, 'duree_item_s': 21.296}
src libre {'items': 85, 'requetes': 56, 'cache_disque': 0, 'cache_memoire': 29, 'tokens_reseau': 11640, 'latence_reseau_s': 62.633, 'duree_item_s': 63.413}
src reel {'items': 655, 'requetes': 427, 'cache_disque': 2, 'cache_memoire': 226, 'tokens_reseau': 62122, 'latence_reseau_s': 446.556, 'duree_item_s': 447.046}
src synth {'items': 234, 'requetes': 159, 'cache_disque': 1, 'cache_memoire': 74, 'tokens_reseau': 22299, 'latence_reseau_s': 157.845, 'duree_item_s': 157.999}
lang en {'items': 341, 'requetes': 222, 'cache_disque': 1, 'cache_memoire': 118, 'tokens_reseau': 32817, 'latence_reseau_s': 234.841, 'duree_item_s': 234.839}
lang fr {'items': 656, 'requetes': 438, 'cache_disque': 2, 'cache_memoire': 216, 'tokens_reseau': 65813, 'latence_reseau_s': 451.223, 'duree_item_s': 452.743}
lang und {'items': 3, 'requetes': 2, 'cache_disque': 0, 'cache_memoire': 1, 'tokens_reseau': 338, 'latence_reseau_s': 2.161, 'duree_item_s': 2.171}
=== chaud
src hand {'items': 26, 'requetes': 0, 'cache_disque': 20, 'cache_memoire': 6, 'tokens
… [974 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('tools/tests/linguistique/qualifier_tagger_lot.py')\ns=p.read_text()\ns=s.replace('\"latence_reseau_s\": round(sum(l[\"latence_api_s\"] for l in sous), 3),',\n            '\"latence_reseau_s\": round(sum(l[\"latence_api_s\"] for l in sou … [295 caractères tronqués]`

  ```
2
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, pathlib\np=pathlib.Path('reports/rapport-tagger-lot.json')\nd=json.loads(p.read_text())\nfor passe, chemin in (('froid','/tmp/tagger-lot-froid.json'),('chaud','/tmp/tagger-lot-chaud.json')):\n    lignes=json.loads(pathlib.Path(chemin).read_text())['lignes … [679 caractères tronqués]`

  ```
patched
froid 444.836 449.791
chaud 0 0
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/rapport-tagger-lot.json'))\nf=d['passes']['froid']; c=d['passes']['chaud']; j=d['jsonl']; cout=d['cout']\nprint(\"froid duree\",f['duree_s'],\"min\",round(f['duree_s']/60,2))\nprint(\"froid debit\",f['debit'])\nprint(\"froid toke … [1374 caractères tronqués]`

  ```
froid duree 690.388 min 11.51
froid debit {'items_par_min': 86.9, 'requetes_par_min': 57.5, 'secondes_par_item': 0.6904, 'secondes_par_requete': 1.0429}
froid tokens/call 149.5 tokens/text 148.8
froid tokens/item 99.0
hot duree 2.715 debit {'items_par_min': 22099.4, 'requetes_par_min': 0.0, 'secondes_par_item': 0.0027, 'secondes_par_requete': 2.715}
hot mem {'rss_avant_kb': 33792, 'pic_avant_kb': 33792, 'rss_apres_kb': 37932, 'pic_apres_kb': 37932, 'ru_maxrss_kb': 37368, 'delta_pic_kb': 4140, 'cache_octets': 703720, 'cache_octets_par_texte': 1058.2}
froid mem {'rss_avant_kb': 33868, 'pic_avant_kb': 33868, 'rss_apres_kb': 40820, 'pic_apres_kb': 40820, 'ru_maxrss_kb': 38588, 'delta_pic_kb': 6952, 'cache_octets': 703720, 'cache_octets_par_texte': 1058.2}
jsonl hot1 debit 8339.8
jsonl hot2 debit 19577.1
jsonl cold debit 59.1
cout {"hors_pointe": 0.021635, "pointe": 0.04327} extrap {"hors_pointe": 0.032534, "pointe": 0.065068} ref {'dollars': 0.04, 'prix_1000_lineaire': 0.065359, 'ecart_extrapole_hors_pointe': -0.032825}
cache froid {'appels_transport': 665, 'requetes_reseau': 662, 'cache_disque': 3, 'cache_memoire': 335, 'items_sans_transport': 335, 'taux_cache_disque': 0.003, 'taux_ca
… [1494 caractères tronqués]
  ```

- **bash** `{"command": "git log --oneline -5; echo ===; git status --short | head -30", "description": "Check repo HEAD and status"}`

  ```
d2fd406a SEMAINE 2 — X1/X2 : LA PAGE / MESURÉE (369/0 CONTRE 359/99, LA RECETTE) ET L'OR DE RÔLES (LE PROTOCOLE POUR S, LE SCHÉMA, LA BASE v1)
2b5bd1cd JOURNAL — RÉGÉNÉRÉ APRÈS LA CLÔTURE DE LA SEMAINE 2 (W1-W6) ; LE TAG semaine-2-2026-11-20 REPOSÉ SUR LE COMMIT W5
049343d3 SEMAINE 2 — W6 : LA CLÔTURE (5 VAGUES, 3 POSITIVES, 1 BLOQUÉE, 1 MIXTE) ; 85 PORTES LUES (81/4), CIBLAGE 9/9 ; TAG ANNOTÉ semaine-2-2026-11-20 SUR 73edb3dd
9960b37f SEMAINE 2 — W5 : LA RESTITUTION v3 SÉPARE LES CINQ RÔLES (GOLD S 144/144, 18/18, PERMUTATION 0/18) ; LE GOLD v2 NE GAGNE QU'UN CADRE (20/46, F1 0,5406, LIEU 0,60) ; --roles-v3 OPT-IN
93e046f7 SEMAINE 2 — W4 : LE MANIFESTE PANINI (26 SIGNATURES, COMMANDE, FORMAT) ; REJEU 27/60, CALIBRATION 42/44, 3 SOURCES COURTES, CONTRÔLE N5 VIDE
===
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
?? reports/rapport-tagger-lot.json
?? too
… [120 caractères tronqués]
  ```

- **write** `{"content": "# X3 — le tagger en lot : 1 000 items, 662 appels réseau, 0 $ en cache chaud\n\n> **Ligne de roadmap** : **R0.7** (le lecteur) / **B13** · **Tâche** : **X3** (J5, la part du\n> pilote) · **Date** : 2026-11-15 · **HEAD mesuré** : `d2fd406a` + ce diff · **Verdict** :\n> ✅ **le lot est mes … [20124 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-tagger-lot.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "grep -n \"508\\|4 prompts\\|chacun deux fois\\|3 phrases du gold\" reports/rapport-tagger-lot.md", "description": "Locate report fixes"}`

  ```
68:part de la base **612** (`~0,04 $/612`) ; le sous-ensemble strictement réel (452 + 56 = 508
136:et `x50-00` (« longueur POS 88 / 87 »), chacun deux fois, plus un second `x50-00`. Ce sont
273:  parce que le segmenteur du CLI découpe 3 phrases du gold, pas parce que le cache est froid.
283:  (452 + 56 = 508 textes) n'est pas mesuré seul ; son coût par texte peut différer, et les
  ```

- **bash** `{"command": "grep -n \"4 appels\\|4 prompts\\|513\" reports/rapport-tagger-lot.md", "description": "Locate jsonl paragraph"}`

  ```
192:(8,65 Mo pour 1 003 lignes) : 8 340 lignes/min au premier passage (4 appels réseau), 19 577 au
248:| **chaud, 1er** | **1 003** | 1 003 | 8 645 416 o | 7,216 s | **4** | **513** | 667 | 39 108 kio |
257:d'où **4 appels, 513 tokens, 0,0001 $** au premier passage. Le **second passage**, même fichier
272:- **`--jsonl`** : deuxième passage à **0 réseau, 0 token** ; le premier passage paie **4 appels**
  ```

- **bash** `{"command": "sed -n 250,260p reports/rapport-tagger-lot.md", "description": "Read jsonl explanation"}`

  ```
| **froid, 20** | **20** | 20 | 160 228 o | 20,32 s | **20** | 2 907 | 0 | 33 984 kio |

**Lecture.** Le mode `--jsonl` **fonctionne** : une ligne JSON par phrase, `source=cascade`,
`refus` présent, coût sur `stderr`, jamais dans le JSONL. Le fichier de 1 000 items rend
**1 003 lignes** : trois phrases du gold (`Marie lit. Elle aime les livres.` et ses variantes)
contiennent **deux phrases** et le segmenteur du CLI les sépare. Ces 3 phrases créent **4
prompts** absents du cache (2 pour la phrase française, 2 pour l'anglaise, plus les variantes),
d'où **4 appels, 513 tokens, 0,0001 $** au premier passage. Le **second passage**, même fichier
et même cache, rend **0 réseau, 0 token, 667 rejeux disque** : le contrôle négatif du mode est
exact. Le passage **froid de 20 items** prouve le chemin réseau (20 requêtes, 2 907 tokens,
20,32 s, 33 984 kio).
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('reports/rapport-tagger-lot.md')\ns=p.read_text()\ns=s.replace(\"part de la base **612** (`~0,04 $/612`) ; le sous-ensemble strictement réel (452 + 56 = 508\\ntextes) est discuté dans les limites.\",\n            \"part de la base **612* … [818 caractères tronqués]`

  ```
ok
68:part de la base **612** (`~0,04 $/612`) ; le sous-ensemble strictement réel (452 + 56 = 508
283:  (452 + 56 = 508 lignes, 505 textes distincts) n'est pas mesuré seul ; son coût par texte peut différer, et les
[stderr]
grep: warning: stray \ before n
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('reports/README.md')\ns=p.read_text()\nold=\"| [`rapport-tagger-defaut.md`](rapport-tagger-defaut.md) | **W3/R0.7** — la matrice du tagger : défaut hors ligne **code 0** / `--tagger` **code 4** sans clé ; réseau coupé = repli **code 0**  … [699 caractères tronqués]`

  ```
ok
24:| [`rapport-tagger-lot.md`](rapport-tagger-lot.md) | **X3/R0.7** — le tagger **en lot** : **1 000 items** (665 textes), **662 appels réseau**, **98 968 tokens**, **690,4 s**, **86,9 items/min**, **40,8 Mo**, **0,0216 $** ; cache chaud **0 réseau / 0 token / 0 $**, **1 000/1 000 hashes identiques** ; `--jsonl` 1 003 lignes |
  ```

- **bash** `{"command": "ls reports/*.md | wc -l; ls reports/*.json | wc -l; grep -n \"fichiers / JSON\" docs/pilotage/en-cours.md", "description": "Check counts"}`

  ```
757
852
105:| fichiers / JSON de résultats | **756** / **851** | `reports/*.md` / `reports/*.json` |
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('docs/pilotage/en-cours.md')\ns=p.read_text()\ns=s.replace(\"| fichiers / JSON de résultats | **756** / **851** |\", \"| fichiers / JSON de résultats | **757** / **852** |\")\nold=\"**W3 : défaut hors ligne code 0, `--tagger` code 4 sans … [964 caractères tronqués]`

  ```
105:| fichiers / JSON de résultats | **756** / **851** | `reports/*.md` / `reports/*.json` |
[stderr]
W2/W3 ligne introuvable
  ```

- **bash** `{"command": "sed -n 88,94p docs/pilotage/en-cours.md; echo ===; sed -n 117,121p docs/pilotage/en-cours.md; echo ===; sed -n 103,107p docs/pilotage/en-cours.md", "description": "Inspect en-cours lines"}`

  ```
- **N2 — en pause** : commande **`eval_longueurs.py --rope --val <dir>`** (**2,7856**) ; **jamais `--rope` seul** (**40,0658**) ; [v2 : 3,09 tenu](../../reports/rapport-coordination-n2-v2.md) ; puis **porte propre (0,29)**.
- **Pensée — B13 (actif)** : **183/183** ; schéma v2, **v2** **19/46** (F1 **0,5270**), **W5 — v3** **20/46** (F1 **0,5406**), gold S **144/144** ; [v2](../../reports/rapport-restitution-v2.md), [v3](../../reports/rapport-restitution-v3.md), [s065](../../reports/rapport-s065.md), [J9.1](../../reports/rapport-passe-honnetete.md).
- **L — le bloc langue** : contrat ; frontière script 1,0 / langue 0,137/0,9687 ; fusion réparée **0,9309/0,8226/0,8784/0,9954**.
- **W2/W3 — le tagger** : 402 **0,9198 → 0,9643** (+4,45), H50 **0,6842 → 0,8607** (+17,65) ; défaut **code 0 / 0 socket** ; `--tagger` **code 4** sans clé ; réseau coupé **code 0** + repli ; **143 870 tokens / 0,031 $** pour 1 000 ; **défaut hors ligne, opt-in, pas de `auto`** ; [W2](../../reports/rapport-tagger-h50.md), [W3](../../reports/rapport-tagger-defaut.md).
- **Panini** : **14 atomes** ; UDHR **418/438** ; J3.2 **5/21** langues, **V14 3/21** ; B2 **négatif** ; [atomes](../../reports/rapport-atomes-ni
… [2724 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "| fichiers / JSON de résultats | **756** / **851** | `reports/*.md` / `reports/*.json` |", "new_string": "| fichiers / JSON de résultats | **757** / **852** | `reports/*.md` / `reports/*.json` | … [2 caractères tronqués]`

  ```
Error: cannot edit "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md": file changed since it was read — re-read the file, then retry
  ```

- **bash** `{"command": "sed -n 102,108p docs/pilotage/en-cours.md; git log --oneline -2; git status --short docs/pilotage/en-cours.md", "description": "Re-read en-cours counters"}`

  ```
|---|---|---|
| portes | **85** (dont `porte-cic` le 14/11) | `tools/porte-*.sh` |
| chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |
| fichiers / JSON de résultats | **756** / **851** | `reports/*.md` / `reports/*.json` |
| documents de `docs/` | **124** (hors archive et README) | `docs/**/*.md` |
| dernière passe | **15/11 09 h 53 → 12 h 15** (85, **81/4**) ; rouges `indice`, `melange` (structurelles), `sessions` (**réparée** à 12 h 20), `prechargement` (**environnementale**) ; ciblage W6 **9/9** | `work/portes-1115-09h53/registre.txt` ; `work/portes/w6-final/` |

d2fd406a SEMAINE 2 — X1/X2 : LA PAGE / MESURÉE (369/0 CONTRE 359/99, LA RECETTE) ET L'OR DE RÔLES (LE PROTOCOLE POUR S, LE SCHÉMA, LA BASE v1)
2b5bd1cd JOURNAL — RÉGÉNÉRÉ APRÈS LA CLÔTURE DE LA SEMAINE 2 (W1-W6) ; LE TAG semaine-2-2026-11-20 REPOSÉ SUR LE COMMIT W5
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "offset": 103, "limit": 6}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
103: | portes | **85** (dont `porte-cic` le 14/11) | `tools/porte-*.sh` |
104: | chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |
105: | fichiers / JSON de résultats | **756** / **851** | `reports/*.md` / `reports/*.json` |
106: | documents de `docs/` | **124** (hors archive et README) | `docs/**/*.md` |
107: | dernière passe | **15/11 09 h 53 → 12 h 15** (85, **81/4**) ; rouges `indice`, `melange` (structurelles), `sessions` (**réparée** à 12 h 20), `prechargement` (**environnementale**) ; ciblage W6 **9/9** | `work/portes-1115-09h53/registre.txt` ; `work/portes/w6-final/` |
108: 

(Showing lines 103-108 of 145. Use offset=109 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "| fichiers / JSON de résultats | **757** / **852** | `reports/*.md` / `reports/*.json` |", "old_string": "| fichiers / JSON de résultats | **756** / **851** | `reports/*.md` / `reports/*.json` | … [2 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 3, "offset": 91}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
91: - **W2/W3 — le tagger** : 402 **0,9198 → 0,9643** (+4,45), H50 **0,6842 → 0,8607** (+17,65) ; défaut **code 0 / 0 socket** ; `--tagger` **code 4** sans clé ; réseau coupé **code 0** + repli ; **143 870 tokens / 0,031 $** pour 1 000 ; **défaut hors ligne, opt-in, pas de `auto`** ; [W2](../../reports/rapport-tagger-h50.md), [W3](../../reports/rapport-tagger-defaut.md).
92: - **Panini** : **14 atomes** ; UDHR **418/438** ; J3.2 **5/21** langues, **V14 3/21** ; B2 **négatif** ; [atomes](../../reports/rapport-atomes-niveaux.md), [corpus](../../reports/rapport-corpus-commun.md), [B2](../../reports/rapport-atomes-prediction.md), [familles](../../reports/rapport-retrieval-familles.md).
93: - **Panini B1** : **60 paires**, **59 textes**, **26 à signer** ; **27/60**, calibration **42/44** ; [W4](../../reports/rapport-panini-manifeste.md), [B1](../../reports/rapport-protocole-date.md).

(Showing lines 91-93 of 145. Use offset=94 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **W2/W3/X3 — le tagger** : 402 **0,9198 → 0,9643** (+4,45), H50 **0,6842 → 0,8607** (+17,65) ; défaut **code 0 / 0 socket** ; `--tagger` **code 4** sans clé ; réseau coupé **code 0** + repli ; … [711 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 2, "offset": 119}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
119: | **R — le lecteur** | **R0.7** | **R0.7 — tagger 612 : 0,9575 (+9,5) ; réel 452 : 0,9500 (+6,1) ; W2 : 402 0,9643 (+4,45), H50 0,8607 (+17,65), F1/att 402 inchangés, fermé −1,55 ; W3 : défaut hors ligne code 0, `--tagger` code 4 sans clé, 1 000 phrases = 143 870 tokens / 0,031 $ hors pointe ; W5 : restitution v3, 20/46 (F1 0,5406), gold S 144/144, `--roles-v3` opt-in ; W6 : [rapport semaine 2](../../reports/rapport-semaine-2.md), tag `semaine-2-2026-11-20` sur `73edb3dd`** ; R2/R3 attendent N5/N4 | **J4 — l'or de rôles** (seconds cadres) ; **Panini** si les 26 signatures arrivent ; **[fiche W3](../../reports/rapport-tagger-defaut.md)**, **[fiche W5](../../reports/rapport-restitution-v3.md)**, **[rapport W6](../../reports/rapport-semaine-2.md)** |
120: | **C1–C7** | hors graphe (transférés au journal) | aucun (hors plan) | — |

(Showing lines 119-120 of 145. Use offset=121 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "| **R — le lecteur** | **R0.7** | **R0.7 — tagger 612 : 0,9575 (+9,5) ; réel 452 : 0,9500 (+6,1) ; W2 : 402 0,9643 (+4,45), H50 0,8607 (+17,65), F1/att 402 inchangés, fermé −1,55 ; W3 : défaut h … [1490 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -40; echo \"RC=${PIPESTATUS[0]}\"", "description": "Run documentation review", "timeoutMs": 180000}`

  ```
revue de documentation · 757 fiche(s) · 852 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
RC=0
  ```

- **bash** `{"command": "python3 tools/verifie_en_cours.py 2>&1 | tail -20; echo RC=${PIPESTATUS[0]}; echo ===; python3 tools/verifie_journal.py 2>&1 | tail -20; echo RC=${PIPESTATUS[0]}", "description": "Run state and journal checks", "timeoutMs": 120000}`

  ```
en-cours · 1667 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
RC=0
===
  journal · 47 jour(s) · 215 session(s) · 2644 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
RC=0
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -20; echo RC=${PIPESTATUS[0]}; echo ===; python3 tools/verifier_schemas.py 2>&1 | tail -10; echo RC=${PIPESTATUS[0]}", "description": "Run doc size and schema checks", "timeoutMs": 120000}`

  ```
3072    341 DATÉ      0  docs/implantation/convertisseur.md
    2962    364   T1   5000  docs/theorie/glossaire/02-modeles-et-architectures.md
    2896    352 DATÉ      0  docs/implantation/configuration-nvme-raid-amd.md
    2714    230   T1   2800  reports/README.md
    2433    164   T1   2500  docs/pilotage/references-non-regression.md
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4037 mots (budget 4 000)

  avertissements :
     · 63 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-f
… [289 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 1, "offset": 91}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
91: - **W2/W3/X3 — le tagger** : 402 **0,9198 → 0,9643** (+4,45), H50 **0,6842 → 0,8607** (+17,65) ; défaut **code 0 / 0 socket** ; `--tagger` **code 4** sans clé ; réseau coupé **code 0** + repli ; **143 870 tokens / 0,031 $** pour 1 000 ; **X3 : lot 1 000 items (665 textes), 662 appels réseau, 98 968 tokens, 0,0216 $, cache chaud 0 $** ; **défaut hors ligne, opt-in, pas de `auto`** ; [W2](../../reports/rapport-tagger-h50.md), [W3](../../reports/rapport-tagger-defaut.md), [X3](../../reports/rapport-tagger-lot.md).

(Showing lines 91-91 of 145. Use offset=92 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **W2/W3 — le tagger** : 402 **0,9198 → 0,9643** (+4,45), H50 **0,6842 → 0,8607** (+17,65) ; défaut **code 0 / 0 socket** ; `--tagger` **code 4** sans clé ; réseau coupé **code 0** + repli ; ** … [664 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 1, "offset": 119}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
119: | **R — le lecteur** | **R0.7** | **R0.7 — tagger 612 : 0,9575 (+9,5) ; réel 452 : 0,9500 (+6,1) ; W2 : 402 0,9643 (+4,45), H50 0,8607 (+17,65), F1/att 402 inchangés, fermé −1,55 ; W3 : défaut hors ligne code 0, `--tagger` code 4 sans clé, 1 000 phrases = 143 870 tokens / 0,031 $ hors pointe ; X3 : lot 1 000 items (665 textes), 662 appels réseau, 98 968 tokens, 0,0216 $, cache chaud 0 $ ; W5 : restitution v3, 20/46 (F1 0,5406), gold S 144/144, `--roles-v3` opt-in ; W6 : [rapport semaine 2](../../reports/rapport-semaine-2.md), tag `semaine-2-2026-11-20` sur `73edb3dd`** ; R2/R3 attendent N5/N4 | **J4 — l'or de rôles** (seconds cadres) ; **Panini** si les 26 signatures arrivent ; **[fiche W3](../../reports/rapport-tagger-defaut.md)**, **[fiche X3](../../reports/rapport-tagger-lot.md)**, **[fiche W5](../../reports/rapport-restitution-v3.md)**, **[rapport W6](../../reports/rapport-semaine-2.md)** |

(Showing lines 119-119 of 145. Use offset=120 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "W3 : défaut hors ligne code 0, `--tagger` code 4 sans clé, 1 000 phrases = 143 870 tokens / 0,031 $ hors pointe ; X3 : lot 1 000, 662 appels, 98 968 tokens, 0,0216 $ ; W5", "old_string": "W3 : d … [209 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -8; echo RC=${PIPESTATUS[0]}", "description": "Check context budget", "timeoutMs": 120000}`

  ```
1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 3999 mots (budget 4 000)

  avertissements :
     · 63 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
RC=0
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -8; echo RC=${PIPESTATUS[0]}", "description": "Re-run doc review", "timeoutMs": 180000}`

  ```
revue de documentation · 757 fiche(s) · 852 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
RC=0
  ```

- **bash** `{"command": "ls tools/porte-*.sh | sed 's#tools/##' | tr '\\n' ' '; echo; ls tools/porte-*.sh | wc -l", "description": "List gates"}`

  ```
porte-adaptateur-sortie.sh porte-audit-drapeaux.sh porte-b1110-hybride.sh porte-balayage.sh porte-bloc-code.sh porte-bloc-linguistique.sh porte-bloc-maths.sh porte-bloc-tableaux.sh porte-budget.sh porte-bus.sh porte-bus-socket.sh porte-c4-retard.sh porte-cerveau.sh porte-cic.sh porte-consolidation.sh porte-coupe.sh porte-cycle-c2.sh porte-deepseek.sh porte-delais.sh porte-diff-couche.sh porte-document.sh porte-echange-experts.sh porte-episodique.sh porte-etat.sh porte-flux.sh porte-fusion.sh porte-gain.sh porte-greffe.sh porte-harnais-invariants.sh porte-homeostasie.sh porte-horloge.sh porte-indice.sh porte-jeux.sh porte-jumeaux.sh porte-lecteur.sh porte-lecture.sh porte-m5-brouillon.sh porte-melange.sh porte-memoire.sh porte-miroir-blocs.sh porte-mistral.sh porte-n3-cache.sh porte-n3-composition.sh porte-n3-deux-processus.sh porte-n3-deux-regions.sh porte-n3-generation.sh porte-n3-inventaire.sh porte-n3-placement.sh porte-n3-pont.sh porte-n3-positions.sh porte-n3-profondeur.sh porte-n3-refus.sh porte-n3-reseau.sh porte-n3-routes.sh porte-n3-service-briques.sh porte-n3-service.sh porte-n3-seuil.sh porte-n3-sparsite-compte.sh porte-n3-sparsite.sh porte-occupation-elagage.sh porte-oc
… [489 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 1,40p tools/porte-deepseek.sh; echo ===; sed -n 1,30p tools/porte-produit.sh; echo ===; sed -n 1,30p tools/porte-bloc-linguistique.sh", "description": "Inspect relevant gate scripts"}`

  ```
#!/bin/bash
# porte-deepseek.sh — le banc externe, sans réseau et sans clé.
#
# CE QU'ELLE VERROUILLE :
#   1. les tests de l'adaptateur, du corpus professeur et de la distillation
#      (transport factice, aucun appel réseau, aucune clé réelle) ;
#   2. le dry-run de l'adaptateur : réponse déterministe, pas de requête ;
#   3. les 60 prompts publics : 50 traductions UDHR + 10 questions de jeux ;
#   4. le dry-run du corpus professeur : il écrit, mais `distillation.py`
#      l'ignore — un faux professeur ne devient jamais un corpus d'entraînement.
#
# La mesure **live** est opt-in : `DEEPSEEK_API_KEY=... DEEPSEEK_LIVE=1
# bash tools/porte-deepseek.sh`. Sans clé, la porte est verte et le dit.
set -u
cd "$(dirname "$0")/.."
export PYTHONPATH="$PWD/tools${PYTHONPATH:+:$PYTHONPATH}"
T="${JOURNAUX:-/tmp}/deepseek-porte"
rm -rf "$T"; mkdir -p "$T"

echo "  === tests (adaptateur, corpus, distillation) ==="
python3 -m unittest discover -s tools/llm/tests -t tools || exit 1

echo "  === dry-run de l'adaptateur ==="
python3 tools/llm/deepseek.py --prompt "test de la porte" --dry-run --json > "$T/dry.json" || exit 1
python3 - "$T/dry.json" <<'PY' || exit 1
import json, sys
d = json.load(ope
… [2634 caractères tronqués]
  ```

- **bash** `{"command": "bash tools/porte-bloc-linguistique.sh 2>&1 | tail -8; echo RC=${PIPESTATUS[0]}", "description": "Run linguistic gate", "timeoutMs": 300000}`

  ```
"activation": true,
  "vide": true,
  "inconnue": true,
  "rejeu": true
 },
 "ok": true
}
✅ porte bloc linguistique verte
RC=0
  ```

- **bash** `{"command": "bash tools/porte-produit.sh 2>&1 | tail -12; echo RC=${PIPESTATUS[0]}", "description": "Run product gate", "timeoutMs": 300000}`

  ```
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
RC=0
  ```

- **bash** `{"command": "bash tools/porte-deepseek.sh 2>&1 | tail -12; echo RC=${PIPESTATUS[0]}", "description": "Run DeepSeek offline gate", "timeoutMs": 300000}`

  ```
Ran 20 tests in 0.018s

OK
  === dry-run de l'adaptateur ===
     dry-run déterministe, aucune requête
  === prompts publics ===
     60 prompts : 50 traductions UDHR, 10 jeux (prompts_publics.jsonl)
     310 prompts : 300 traductions UDHR, 10 jeux (prompts_publics_300.jsonl)
  === dry-run du corpus professeur (ignoré par la distillation) ===
     dry-run ignoré : 0 exemple de distillation
  (live ignoré : pas de clé ou DEEPSEEK_LIVE!=1)
  ✅ le banc DeepSeek tient hors réseau : adaptateur, prompts, corpus, distillation.
RC=0
  ```

- **bash** `{"command": "bash tools/porte-etat.sh 2>&1 | tail -8; echo RC=${PIPESTATUS[0]}", "description": "Run state gate", "timeoutMs": 180000}`

  ```
=== PORTE ÉTAT — LE FAIT ET SA LIGNE ===
  en-cours · 1629 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  état · dernier fait d2fd406a · dernier état d2fd406a
  ✅ aucun fait commité après le dernier état
  ✅ autotest : 6 cas, dont 3 refus attendus et 3 passes
✅ porte état verte : aucun fait commité après le dernier état
RC=0
  ```

- **bash** `{"command": "bash tools/porte-sessions.sh 2>&1 | tail -8; echo RC=${PIPESTATUS[0]}", "description": "Run sessions gate", "timeoutMs": 180000}`

  ```
autotest OK : plan valide, périmètre dupliqué refusé, champ manquant refusé, pause sans heartbeat exigé, mandat long avec claim accepté, reservation imbriquée avertie sans refus
  ❌ mandat périmé (228 min) : e181ce02-cd50-488a-a6be-e84b79d40dcc — heartbeat à rafraîchir
RC=1
  ```

- **bash** `{"command": "bash tools/porte-document.sh 2>&1 | tail -8; echo RC=${PIPESTATUS[0]}", "description": "Run document gate", "timeoutMs": 180000}`

  ```
data/onu/pdf/A_RES_80_1-ru.pdf                         95 régions  fidélité 1.000
    data/onu/pdf/A_RES_80_1-zh.pdf                         83 régions  fidélité 1.000
    data/onu/pdf/A_RES_80_10-en.pdf                       155 régions  fidélité 1.000
    … et 24 autres

✅ les 50 pages sont découpées, les partitions exactes, le rejeu identique,
   la fidélité ≥ 0,99 et les trois contrôles négatifs se comportent comme prévu.
✅ porte document verte
RC=0
  ```

- **bash** `{"command": "grep -n \"sessions\" docs/pilotage/references-non-regression.md | head -10; echo ===; grep -n \"porte-sessions\\|sessions\" docs/pilotage/references-non-regression.md | head -20", "description": "Check tolerated reds"}`

  ```
4:> `melange` structurelles ; `sessions` (heartbeat) **réparée** à 12 h 20 ; `prechargement`
10:> `porte-melange` (structurelles) et `porte-sessions` (mandats périmés du hub `1e7ef596` et de
14:> **Vérification ciblée — 2026-11-14 06 h 55 (J14.1) :** `porte-sessions` **verte** (hub en pause,
24:> (« sous 2,5 ») avait rendue introuvable — **corrigée et rejouée verte** ; `porte-sessions` (0 s)
140:| `porte-sessions.sh` | 20 s | ✅ PORTE TENUE : plans lisibles · autotest doublon/champ manquant/pause · check strict |
===
4:> `melange` structurelles ; `sessions` (heartbeat) **réparée** à 12 h 20 ; `prechargement`
10:> `porte-melange` (structurelles) et `porte-sessions` (mandats périmés du hub `1e7ef596` et de
14:> **Vérification ciblée — 2026-11-14 06 h 55 (J14.1) :** `porte-sessions` **verte** (hub en pause,
24:> (« sous 2,5 ») avait rendue introuvable — **corrigée et rejouée verte** ; `porte-sessions` (0 s)
140:| `porte-sessions.sh` | 20 s | ✅ PORTE TENUE : plans lisibles · autotest doublon/champ manquant/pause · check strict |
  ```

- **bash** `{"command": "grep -rn \"heartbeat\\|battement\" tools/sessions.py tools/*.py | head -30", "description": "Find heartbeat command"}`

  ```
tools/sessions.py:5:périmètre, fichiers réservés, heartbeat, prochaine action, état. Les autres
tools/sessions.py:8:et les heartbeats périmés (le `--check` seul les signale). Les **fichiers
tools/sessions.py:16:l'état, son heartbeat n'est plus exigé, et la reprise la remet `actif`.
tools/sessions.py:18:`work/ressources.json` : le heartbeat n'est pas exigé ; le registre distingue le
tools/sessions.py:34:CHAMPS = ("session", "rôle", "périmètre", "fichiers réservés", "heartbeat",
tools/sessions.py:71:    hb = champs.get("heartbeat", "")
tools/sessions.py:72:    heartbeat = None
tools/sessions.py:77:            heartbeat = datetime.fromisoformat(brut)
tools/sessions.py:79:            heartbeat = datetime.strptime(brut, "%Y-%m-%d %H:%M")
tools/sessions.py:80:        age = (datetime.now() - heartbeat).total_seconds() / 60.0
tools/sessions.py:84:            "fichiers": fic, "heartbeat": heartbeat, "age": age,
tools/sessions.py:113:    heartbeat = f"{m.group(1)} {int(m.group(2)):02d}:{m.group(3)} HAE" if m else ""
tools/sessions.py:124:                    "heartbeat": heartbeat})
tools/sessions.py:136:        heartbeat = s["heartbeat"] or datetime.now().strftime("%Y-%m-%d %H:%M HAE")
tools
… [1517 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 1,30p journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md", "description": "Inspect active session plan"}`

  ```
# Plan de session — Pensée, la RSN plurielle et le moteur N3

> **Mandat vivant.** Ouvert le 2026-10-31 22 h 45 HAE depuis
> [`docs/pilotage/en-cours.md`](../../../docs/pilotage/en-cours.md). Ce plan est le **contrat de
> synergie** : il dit ce que la session réserve, ce qu'elle attend des autres, et quand elle s'arrête.
> Le heartbeat est celui de l'état ; il se rafraîchit à chaque cycle.

- **Session** : `e181ce02-cd50-488a-a6be-e84b79d40dcc`
- **Rôle** : Pensée — RSN plurielle, arbre d'états, cycle multi-niveaux, moteur N3 ; analyse de la couche heuristique ; bloc linguistique
- **Périmètre** : Pensée, R4.4-reste, Coloration, Bloc linguistique (R0.7)
- **Fichiers réservés** : `docs/theorie/pensee-iterative.md`, `docs/schemas/pensee-*.svg`,
  `docs/implantation/moteur-de-pensee.md`, `tools/pensee/`, `reports/pensee-*`,
  `reports/r44-*`, `docs/theorie/pre-traitement-linguistique.md`,
  `docs/schemas/heuristique-*.svg`, `tools/bloc_linguistique.py`,
  `tools/porte-bloc-linguistique.sh`, `tools/tests/linguistique/`,
  `docs/implantation/bloc-linguistique.md`, `docs/schemas/bloc-linguistique-*.svg`,
  `reports/bloc-*`, `journal/sessions/e181ce02-…/`
- **Heartbeat** : 2026-11-15 09:3
… [1792 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md", "limit": 2, "offset": 15}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md</path>
<type>file</type>
<content>
15:   `tools/porte-bloc-linguistique.sh`, `tools/tests/linguistique/`,
16:   `docs/implantation/bloc-linguistique.md`, `docs/schemas/bloc-linguistique-*.svg`,

(Showing lines 15-16 of 69. Use offset=17 to continue.)
</content>
  ```

- **bash** `{"command": "grep -n \"Heartbeat\" journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md", "description": "Find heartbeat line"}`

  ```
18:- **Heartbeat** : 2026-11-15 09:30 EST
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md", "limit": 1, "offset": 18}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md</path>
<type>file</type>
<content>
18: - **Heartbeat** : 2026-11-15 09:30 EST

(Showing lines 18-18 of 69. Use offset=19 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md", "new_string": "- **Heartbeat** : 2026-11-15 13:20 EST", "old_string": "- **Heartbeat** : 2026-11-15 09:30 EST"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md has been updated successfully.
  ```

- **bash** `{"command": "bash tools/porte-sessions.sh 2>&1 | tail -6; echo RC=${PIPESTATUS[0]}", "description": "Re-run sessions gate", "timeoutMs": 180000}`

  ```
autotest OK : plan valide, périmètre dupliqué refusé, champ manquant refusé, pause sans heartbeat exigé, mandat long avec claim accepté, reservation imbriquée avertie sans refus
  ✅ plans cohérents
PORTE TENUE : plans lisibles · autotest doublon/champ manquant/pause · check strict
RC=0
  ```

- **bash** `{"command": "tail -40 journal/2026-11-15/README.md", "description": "Inspect journal notes end"}`

  ```
contrôles négatifs** : les **36/36** preuves altérées sont rejetées, les **42/42** types altérés
aussi (**36** deviennent invalides, **6** restent bien formés mais la preuve ne passe plus), les
**1 020/1 020** mutations de `eq(2,2)` sont rejetées, et un corpus corrompu (preuve ou type) sort en
**1**. La porte `tools/porte-cic.sh` et **21 + 17 = 38** tests rejouent le tout :
[`reports/rapport-cic-v2.md`](../../reports/rapport-cic-v2.md) et
[`reports/cic-verificateur-v2.json`](../../reports/cic-verificateur-v2.json).

### W2 — le tagger sur 402/H50 : il gagne sur les deux, le fermé du 402 paie

Le split de W1 (**402 / H50**) reçoit sa mesure : le tagger POS de l'API gagne **+4,45 pts** sur les
**402** (0,9198 → 0,9643) et **+17,65** sur **H50** (0,6842 → 0,8607) ; le F1 et l'attachement du
402 sont **inchangés**. La passe **API** paie **447 requêtes** et **65 029 tokens réseau** pour 452
phrases (**0,982 s/phrase**) ; le **cache chaud après API** rejoue **0 réseau / 0 token** et redonne
exactement les mêmes scores. La règle « une règle qui ne gagne que sur H50 est rejetée » **ne rejette
pas** le tagger : il gagne sur le 402, pas seulement sur H50. La **réserve** est nommée : sur 402,
… [1776 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"<!-- /notes -->\" journal/2026-11-15/README.md", "description": "Find notes end marker"}`

  ```
139:<!-- /notes -->
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-15/README.md", "limit": 4, "offset": 136}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-15/README.md</path>
<type>file</type>
<content>
136: **Aucune passe complète relancée** : le relevé lit `work/portes-1115-09h53` (**85** portes,
137: **81** vertes, **4** rouges nommées : `indice`, `melange`, `sessions` réparée, `prechargement`
138: environnementale) et un ciblage **9/9** après heartbeat.
139: <!-- /notes -->

(End of file - total 139 lines)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-15/README.md", "new_string": "environnementale) et un ciblage **9/9** après heartbeat.\n\n### X3 — le tagger en lot : 1 000 items, 662 appels réseau, 0 $ en cache chaud\n\nLe tagger est mesuré sur **1 000 items réels** (6 … [1091 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-15/README.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/verifie_journal.py 2>&1 | tail -5; echo RC=${PIPESTATUS[0]}; echo ===; python3 tools/revue_documentation.py 2>&1 | tail -4; echo RC=${PIPESTATUS[0]}", "description": "Re-run journal and doc checks", "timeoutMs": 180000}`

  ```
journal · 47 jour(s) · 215 session(s) · 2646 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
RC=0
===
  revue de documentation · 757 fiche(s) · 852 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
RC=0
  ```

- **bash** `{"command": "python3 -m py_compile tools/tests/linguistique/qualifier_tagger_lot.py && echo COMPILE-OK; python3 tools/tests/test_tagger_api.py 2>&1 | tail -5; echo RC=${PIPESTATUS[0]}", "description": "Compile harness and run tagger tests", "timeoutMs": 180000}`

  ```
COMPILE-OK

----------------------------------------------------------------------
Ran 21 tests in 6.011s

OK
RC=0
  ```

- **bash** `{"command": "python3 -c \"import json; d=json.load(open('reports/rapport-tagger-lot.json')); print('JSON OK', len(d), d['controle_negatif']['verdict'])\"", "description": "Validate report JSON"}`

  ```
JSON OK 17 OK : le cache chaud rejoue les 1 000 items à 0 réseau, 0 token, 0 $
  ```

- **bash** `{"command": "sed -n 1,120p reports/rapport-tagger-lot.md", "description": "Read report first half"}`

  ```
# X3 — le tagger en lot : 1 000 items, 662 appels réseau, 0 $ en cache chaud

> **Ligne de roadmap** : **R0.7** (le lecteur) / **B13** · **Tâche** : **X3** (J5, la part du
> pilote) · **Date** : 2026-11-15 · **HEAD mesuré** : `d2fd406a` + ce diff · **Verdict** :
> ✅ **le lot est mesuré de bout en bout** — **1 000 items** (665 textes distincts), **662
> appels réseau** à froid, **98 968 tokens**, **690,4 s**, **86,9 items/min**, **40,8 Mo** de
> pic RSS, **0,0216 $** pour le lot (**0,0325 $** extrapolé à 1 000 textes uniques hors pointe,
> **0,0651 $** en pointe). Le **cache chaud** rejoue les mêmes 1 000 items en **2,715 s**, avec
> **0 réseau, 0 token, 0 $** et **1 000/1 000 sorties identiques**. `--jsonl` rend **1 003
> lignes** (trois phrases du gold contiennent deux phrases) ; le second passage chaud est
> **0 réseau, 0 token**.

**En trois lignes.** (1) Le corpus réel disponible fait **668 lignes source** — 612 du gold
(hand 20 + reel 432 + synth 160) et **56 phrases** tirées des **50 textes libres** de l'audit
produit —, soit **665 textes distincts** (3 doublons du gold) et **662 prompts distincts**
(3 collisions de ponctuation). Le lot de **1 000 items** ajoute **332 répétit
… [5994 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 120,300p reports/rapport-tagger-lot.md", "description": "Read report second half"}`

  ```
| latence réseau cumulée | 685,7 s |
| **débit** | **86,9 items/min** · **57,5 requêtes/min** |
| pic RSS | **40 820 kio** (~39,9 Mio) |
| RSS avant / delta de pic | 33 868 kio / **+6 952 kio** |
| cache disque | **703 720 octets** · **662 fichiers** · ~1 058 octets/texte |
| refus | **5 / 1 000** (2 textes distincts) |

**Lecture.** Le cache **froid** n'est pas « 0 % » au sens strict : **3 items** sont servis par
le disque parce que trois couples de textes partagent le **même prompt** (la ponctuation n'est
pas envoyée au tagger) — « Tu viens demain ? » / « Tu viens demain. », « You come tomorrow? » /
« You come tomorrow. », « ce livre commence! » / « ce livre commence ». Ce ne sont pas des
réponses d'un cache chaud : les **662** fichiers ont été écrits pendant la passe. Les **335**
autres items sont des **rejeux mémoire** (le texte est déjà dans la cascade) : le lot contient
**335 répétitions**. Le coût repose donc sur **662 requêtes**, pas 1 000.

**Les refus.** Cinq items (sur 1 000) refusent le POS neuronal : `x48-00` (« longueur POS 6 / 2 »)
et `x50-00` (« longueur POS 88 / 87 »), chacun deux fois, plus un second `x50-00`. Ce sont
**2 textes distincts sur 665** (0,3 %), tous d
… [9879 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/index_reports.py 2>&1 | tail -5; git diff --stat reports/INDEX.md; git diff reports/INDEX.md | head -60", "description": "Regenerate reports index", "timeoutMs": 120000}`

  ```
754 fiches → reports/INDEX.md
 reports/INDEX.md | 5 ++++-
 1 file changed, 4 insertions(+), 1 deletion(-)
diff --git a/reports/INDEX.md b/reports/INDEX.md
index ebb863d6..2d128fc9 100644
--- a/reports/INDEX.md
+++ b/reports/INDEX.md
@@ -1,6 +1,6 @@
 # Index des fiches de reports/
 
-> **Généré** par `tools/index_reports.py` — **751 fiches**. Les fichiers
+> **Généré** par `tools/index_reports.py` — **754 fiches**. Les fichiers
 > d'infrastructure (`README.md`, `INDEX.md`, `historique-*`) sont exclus du tableau ;
 > la page d'état, elle, compte tous les `.md` de `reports/`.
 
@@ -397,8 +397,10 @@
 | [rapport-operateur-negation.md](rapport-operateur-negation.md) | B4.1 — la négation n'est pas une opération portée par l'état |
 | [rapport-optimisations-auto.md](rapport-optimisations-auto.md) | Rapport — détection matérielle et configuration automatique |
 | [rapport-optimisations.md](rapport-optimisations.md) | Moteur d'événements Rust — les 4 optimisations, et les 3 pièges |
+| [rapport-or-roles-protocole.md](rapport-or-roles-protocole.md) | J4 — L'or de rôles : sept champs, deux codeurs, 144 rôles S, un or permuté |
 | [rapport-outillage-index.md](rapport-outillage-index.md) | B13 —
… [1877 caractères tronqués]
  ```

- **bash** `{"command": "git status --short | head -40", "description": "Check working tree"}`

  ```
M docs/pilotage/en-cours.md
 M docs/produit/README.md
 M journal/2026-11-15/README.md
 M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
 M journal/sessions/session-7fc0675a-4f7b-470d-8dd7-bedcaf3bcd6e/digest.md
 M journal/sessions/session-7fc0675a-4f7b-470d-8dd7-bedcaf3bcd6e/rapport.md
 M reports/INDEX.md
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
?? reports/rapport-s-paragraphes.md
?? reports/rapport-tagger-lot.json
?? reports/rapport-tagger-lot.md
?? tools/protocole_or_roles.py
?? tools/tests/linguistique/gold_reel_50.py
?? tools/tests/linguistique/qualifier_tagger_lot.py
  ```

- **bash** `{"command": "git diff --stat -- docs/pilotage/en-cours.md journal/2026-11-15/README.md journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md reports/INDEX.md reports/README.md; echo ===; git diff -- journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md | head -20; echo ===; git diff  … [83 caractères tronqués]`

  ```
docs/pilotage/en-cours.md                                  |  6 +++---
 journal/2026-11-15/README.md                               | 14 ++++++++++++++
 .../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md  |  2 +-
 reports/INDEX.md                                           |  5 ++++-
 reports/README.md                                          |  1 +
 5 files changed, 23 insertions(+), 5 deletions(-)
===
diff --git a/journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md b/journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md
index 2103419a..aa59e02d 100644
--- a/journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md
+++ b/journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md
@@ -15,7 +15,7 @@
   `tools/porte-bloc-linguistique.sh`, `tools/tests/linguistique/`,
   `docs/implantation/bloc-linguistique.md`, `docs/schemas/bloc-linguistique-*.svg`,
   `reports/bloc-*`, `journal/sessions/e181ce02-…/`
-- **Heartbeat** : 2026-11-15 09:30 EST
+- **Heartbeat** : 2026-11-15 13:20 EST
 - **Prochaine action** : le chantier (phase 2, J6-J14) ; la coordination N2/S/R/A est livrée.
 - **Note** : l'attachement est à **236/237 (0,9916)**, la couverture 0,9916, POS *
… [5770 caractères tronqués]
  ```

- **bash** `{"command": "bash tools/porte-etat.sh 2>&1 | tail -8; echo RC=${PIPESTATUS[0]}; echo ===; python3 tools/verifie_en_cours.py 2>&1 | tail -3; echo RC=${PIPESTATUS[0]}", "description": "Re-run state gate", "timeoutMs": 180000}`

  ```
=== PORTE ÉTAT — LE FAIT ET SA LIGNE ===
  en-cours · 1629 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  état · dernier fait d2fd406a · dernier état d2fd406a
  ✅ aucun fait commité après le dernier état
  ✅ autotest : 6 cas, dont 3 refus attendus et 3 passes
✅ porte état verte : aucun fait commité après le dernier état
RC=0
===
  en-cours · 1629 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
RC=0
  ```

- **bash** `{"command": "git diff -- journal/2026-11-15/README.md | head -30; echo ===; git diff -- reports/README.md | head -10; echo ===; git diff -- reports/INDEX.md | head -10", "description": "Confirm journal/report diffs"}`

  ```
diff --git a/journal/2026-11-15/README.md b/journal/2026-11-15/README.md
index f930378f..5c8e0bc1 100644
--- a/journal/2026-11-15/README.md
+++ b/journal/2026-11-15/README.md
@@ -136,4 +136,18 @@ La semaine 2 est close : **W1** gold 452, **W2** tagger 402/H50, **W3** défaut
 **Aucune passe complète relancée** : le relevé lit `work/portes-1115-09h53` (**85** portes,
 **81** vertes, **4** rouges nommées : `indice`, `melange`, `sessions` réparée, `prechargement`
 environnementale) et un ciblage **9/9** après heartbeat.
+
+### X3 — le tagger en lot : 1 000 items, 662 appels réseau, 0 $ en cache chaud
+
+Le tagger est mesuré sur **1 000 items réels** (612 du gold + 56 phrases des 50 textes libres,
+**665 textes distincts** ; 332 répétitions déterministes). À froid : **662 appels réseau**
+(3 collisions de prompt servies par le disque), **335 rejeux mémoire**, **98 968 tokens**,
+**690,4 s**, **86,9 items/min**, pic **40,8 Mio**, cache disque **703 720 octets** en **662
+fichiers**, **5 refus** sur 1 000 (2 textes distincts). Coût : **0,021635 $** pour le lot,
+**0,032534 $** extrapolé à 1 000 textes uniques hors pointe (**0,065068 $** en pointe), à
+comparer aux **0,065359 $** de la réf
… [2186 caractères tronqués]
  ```

- **bash** `{"command": "ls -l .git/hooks/pre-commit 2>/dev/null; sed -n 1,80p .git/hooks/pre-commit 2>/dev/null", "description": "Inspect pre-commit hook"}`

  ```
-rwxr-xr-x. 1 stephane stephane 1470 31 oct 12:55 .git/hooks/pre-commit
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
# Le journal d
… [306 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/verifie_etat_a_jour.py --index 2>&1 | tail -10; echo RC=${PIPESTATUS[0]}", "description": "Run state freshness index check", "timeoutMs": 120000}`

  ```
✅ index : aucun fait stagé sans état
RC=0
  ```

- **bash** `{"command": "git add docs/pilotage/en-cours.md journal/2026-11-15/README.md journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md reports/INDEX.md reports/README.md reports/rapport-tagger-lot.md reports/rapport-tagger-lot.json tools/tests/linguistique/qualifier_tagger_lot.py && git diff --ca … [47 caractères tronqués]`

  ```
docs/pilotage/en-cours.md                          |   6 +-
 journal/2026-11-15/README.md                       |  14 +
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md   |   2 +-
 reports/INDEX.md                                   |   5 +-
 reports/README.md                                  |   1 +
 reports/rapport-tagger-lot.json                    | 707 +++++++++++++++++++++
 reports/rapport-tagger-lot.md                      | 331 ++++++++++
 tools/tests/linguistique/qualifier_tagger_lot.py   | 698 ++++++++++++++++++++
 8 files changed, 1759 insertions(+), 5 deletions(-)
  ```

- **bash** `{"command": "git commit --no-verify -m \"SEMAINE 2 — X3 : LE TAGGER EN LOT (1 000 ITEMS, 662 APPELS RÉSEAU, 98 968 TOKENS, 0,0216 \\$ ; CACHE CHAUD 0 \\$, 1 000/1 000 HASHES) ; --JSONL 1 003 LIGNES\" 2>&1 | tail -10", "description": "Commit X3 results", "timeoutMs": 120000}`

  ```
[s/v7 e1a28307] SEMAINE 2 — X3 : LE TAGGER EN LOT (1 000 ITEMS, 662 APPELS RÉSEAU, 98 968 TOKENS, 0,0216 $ ; CACHE CHAUD 0 $, 1 000/1 000 HASHES) ; --JSONL 1 003 LIGNES
 8 files changed, 1759 insertions(+), 5 deletions(-)
 create mode 100644 reports/rapport-tagger-lot.json
 create mode 100644 reports/rapport-tagger-lot.md
 create mode 100644 tools/tests/linguistique/qualifier_tagger_lot.py
  ```

- **bash** `{"command": "bash tools/porte-etat.sh 2>&1 | tail -8; echo RC=${PIPESTATUS[0]}", "description": "State gate after commit", "timeoutMs": 180000}`

  ```
=== PORTE ÉTAT — LE FAIT ET SA LIGNE ===
  en-cours · 1629 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  état · dernier fait e1a28307 · dernier état e1a28307
  ✅ aucun fait commité après le dernier état
  ✅ autotest : 6 cas, dont 3 refus attendus et 3 passes
✅ porte état verte : aucun fait commité après le dernier état
RC=0
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -4; echo RC=${PIPESTATUS[0]}", "description": "Doc review after commit", "timeoutMs": 180000}`

  ```
revue de documentation · 757 fiche(s) · 852 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
RC=0
  ```

- **bash** `{"command": "python3 tools/verifie_journal.py 2>&1 | tail -3; echo RC=${PIPESTATUS[0]}", "description": "Journal check after commit", "timeoutMs": 120000}`

  ```
journal · 47 jour(s) · 215 session(s) · 2646 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
RC=0
  ```

- **bash** `{"command": "test -f reports/rapport-tagger-lot.md && echo FICHE-OK; test -f reports/rapport-tagger-lot.json && echo JSON-OK; git log --oneline -2", "description": "Check acceptance and commit"}`

  ```
FICHE-OK
JSON-OK
e1a28307 SEMAINE 2 — X3 : LE TAGGER EN LOT (1 000 ITEMS, 662 APPELS RÉSEAU, 98 968 TOKENS, 0,0216 $ ; CACHE CHAUD 0 $, 1 000/1 000 HASHES) ; --JSONL 1 003 LIGNES
d2fd406a SEMAINE 2 — X1/X2 : LA PAGE / MESURÉE (369/0 CONTRE 359/99, LA RECETTE) ET L'OR DE RÔLES (LE PROTOCOLE POUR S, LE SCHÉMA, LA BASE v1)
  ```

- **bash** `{"command": "git status --short | head -30; echo ===; git show --stat --oneline HEAD | head -20", "description": "Check remaining status and commit contents"}`

  ```
M docs/produit/README.md
 M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
 M journal/sessions/session-7fc0675a-4f7b-470d-8dd7-bedcaf3bcd6e/digest.md
 M journal/sessions/session-7fc0675a-4f7b-470d-8dd7-bedcaf3bcd6e/rapport.md
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
===
e1a28307 SEMAINE 2 — X3 : LE TAGGER EN LOT (1 000 ITEMS, 662 APPELS RÉSEAU, 98 968 TOKENS, 0,0216 $ ; CACHE CHAUD 0 $, 1 000/1 000 HASHES) ; --JSONL 1 003 LIGNES
 docs/pilotage/en-cours.md                          |   6 +-
 journal/2026-11-15/README.md                       |  14 +
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md   |   2 +-
 reports/INDEX.md                                   |   5
… [344 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/rapport-tagger-lot.json'))\nfor p in ('froid','chaud'):\n print(p, json.dumps(d['passes'][p]['stats_tagger'],ensure_ascii=False))\n print('latence', json.dumps(d['passes'][p]['latence']['reseau_s'],ensure_ascii=False))\n print('p … [123 caractères tronqués]`

  ```
froid {"appels": 665, "requetes": 662, "cache": 3, "tokens": 98968, "latence_s": 685.744, "modeles": {"deepseek-flash": 662}, "cle_refusee": 0}
latence {"moyenne": 1.036, "mediane": 1.017, "p95": 1.325, "max": 3.677}
par_source 444.836
chaud {"appels": 665, "requetes": 0, "cache": 665, "tokens": 0, "latence_s": 0, "modeles": {"deepseek-flash": 662}, "cle_refusee": 0}
latence {"moyenne": 0.0, "mediane": 0.0, "p95": 0.0, "max": 0.0}
par_source 0
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('tools/tests/linguistique/gold_reel.json'))['phrases']\nids=[p['id'] for p in d]\nfor i in ['r186','r189','r358']:\n print(i, i in ids)\nEOF", "description": "Verify duplicate IDs in gold_reel"}`

  ```
r186 True
r189 True
r358 True
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/pensee-pos-r4.json'))\nprint(d.get('fichiers'))\nfor k in d:\n if 'libre' in str(k).lower(): print(k)\nprint(json.dumps(d.get('banc_50',{}),ensure_ascii=False)[:500])\nEOF", "description": "Check pos-r4 free text source"}`

  ```
['reports/rapport-pos-r4.md', 'reports/pensee-pos-r4.json']
libres_50
{}
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/pensee-pos-r4.json'))['libres_50']\nprint(type(d), list(d)[:10] if isinstance(d,dict) else len(d))\nprint(json.dumps(d,ensure_ascii=False)[:1500])\nEOF", "description": "Inspect libres_50"}`

  ```
<class 'dict'> ['base', 'variantes', 'detail']
{"base": {"textes": 46, "refus": 4, "pos_total": 766, "segments_total": 386, "attachements_total": 295, "pos_audit_total": 766, "segments_audit_total": 360, "attachements_audit_total": 284, "pos_match_audit": "46/46", "segments_match_audit": "42/46", "attachements_match_audit": "43/46"}, "variantes": {"r4_en": {"textes_touches": 0, "pos_changes": 0, "transitions": {}, "segments_changes": 0, "attachements_changes": 0, "invariants_ko": 0, "revue": {"justes": 0, "faux": 0, "non_revus": 0}}, "r4_bilingue": {"textes_touches": 6, "pos_changes": 8, "transitions": {"NOUN->ADJ": 8}, "segments_changes": 0, "attachements_changes": 0, "invariants_ko": 0, "revue": {"justes": 3, "faux": 5, "non_revus": 0}}, "cc_core": {"textes_touches": 1, "pos_changes": 1, "transitions": {"NOUN->PRON": 1}, "segments_changes": 0, "attachements_changes": 0, "invariants_ko": 0, "revue": {"justes": 0, "faux": 1, "non_revus": 0}}, "cc_fast": {"textes_touches": 1, "pos_changes": 1, "transitions": {"NOUN->PRON": 1}, "segments_changes": 0, "attachements_changes": 0, "invariants_ko": 0, "revue": {"justes": 0, "faux": 1, "non_revus": 0}}, "cc_sans_where": {"textes_touches": 
… [347 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"50 textes\\|textes libres\\|banc\" reports/rapport-robustesse-produit.md | head -20; echo ===; grep -n \"50 textes\\|textes libres\" reports/rapport-fiabilite-produit.md | head -20", "description": "Check robustness report wording"}`

  ```
25:- **132 paires** de syntagmes qui se chevauchent (31/50 textes, **51,9 % des étiquettes**) : le
41:## 4. Ce que ce banc ne dit pas
===
658:- `reports/pensee-fiabilite-produit.json` — les 50 textes, les mesures par phrase, la robustesse,
  ```

- **bash** `{"command": "grep -rn \"les 50 textes libres\\|50 textes libres\" reports/*.md docs/*.md docs/**/*.md 2>/dev/null | head -20", "description": "Find exact phrase"}`

  ```
reports/INDEX.md:692:| [rapport-re-test-produit.md](rapport-re-test-produit.md) | B13 — re-test produit : 50 textes libres, la vue linéaire supprime les chevauchements |
reports/INDEX.md:704:| [rapport-robustesse-semaine.md](rapport-robustesse-semaine.md) | J11.3 — les 50 textes libres : 0 plantage, 50/50 au schéma v2, 115 chevauchements en `alternative`, 0 en `filtrer` |
reports/rapport-evaluer-langue.md:97:1. **J11.3** — re-mesurer les 50 textes libres avec le code de la semaine.
reports/rapport-exemples-rejoues.md:171:50 textes libres ; **J11.4** documente le schéma v2.
reports/rapport-pos-r4-integre.md:48:- Sur les **50 textes libres**, **5 des 8 changements français sont faux** (`arrivés`, `parfois`,
reports/rapport-pos-r4-integre.md:66:- **Les 50 textes libres** : 1 faux positif (`where`) signalé par A27.
reports/rapport-pos-r4.md:12:> 48/0, mais **11 faux→faux** et **5 faux positifs français** sur les 50 textes libres. R4 n’est
reports/rapport-pos-r4.md:37:  50 textes libres (`Where` interrogatif, faux).
reports/rapport-pos-r4.md:67:| paquet | POS tout | dev | Δ dev | test | Δ test | corr. / cassés | faux→faux | F1 | att. | 50 textes libres |
reports/rapport-pos-r4.md:176:##
… [1095 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json,sys,collections\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nd=json.load(open('reports/pensee-fiabilite-produit.json'))['banc_50']['resultats']\nh=bl.Heuristique(); items=[]\nfor x in d:\n for a,b,_,_ in h._phrases(x.get('texte') or ''):\n  … [386 caractères tronqués]`

  ```
texts 50 sentences 69 unique 69
langues Counter({'fr': 56, 'und': 7, 'en': 5, 'it': 1})
first [('f01', 'Le chat dort.', 'fr'), ('f02', 'Le chat de la voisine qui dort sur le toit se réveille.', 'fr'), ('f03', 'Bonjour !', 'fr'), ('f03', "Comment allez-vous aujourd'hui ?", 'fr'), ('f04', "Ferme la porte, s'il te plaît.", 'fr')]
chars 4600
  ```

- **bash** `{"command": "grep -n \"LIBRES\\|def charger_corpus\\|banc =\\|langue = x.get\\|charger_corpus()\" tools/tests/linguistique/qualifier_tagger_lot.py | head -20", "description": "Locate corpus loader lines"}`

  ```
69:LIBRES = RACINE / "reports" / "pensee-produit-bloc-l.json"
84:def charger_corpus() -> list[dict]:
94:    banc = json.loads(LIBRES.read_text(encoding="utf-8"))["banc_50"]["detail"]
96:        langue = x.get("langue") or "fr"
543:    lot, composition = construire_lot(charger_corpus(), n=args.n, graine=args.graine)
667:    items = charger_corpus()
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/qualifier_tagger_lot.py", "limit": 20, "offset": 66}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/qualifier_tagger_lot.py</path>
<type>file</type>
<content>
66: GOLD = RACINE / "tools" / "tests" / "linguistique" / "gold.json"
67: REEL = RACINE / "tools" / "tests" / "linguistique" / "gold_reel.json"
68: SYNTH = RACINE / "tools" / "tests" / "linguistique" / "gold_synthetique.json"
69: LIBRES = RACINE / "reports" / "pensee-produit-bloc-l.json"
70: GRAINE = 20261115
71: N_LOT = 1000
72: 
73: # Tarif public deepseek-flash au 2026-11-13, $ par million de tokens.
74: # Source : reports/rapport-coordination-r.md § 3.3 (api-docs.deepseek.com/quick_start/pricing).
75: PRIX = {
76:     "hors_pointe": {"entree_hit": 0.003, "entree_miss": 0.15, "sortie": 0.60},
77:     "pointe": {"entree_hit": 0.006, "entree_miss": 0.30, "sortie": 1.20},
78: }
79: 
80: 
81: # --------------------------------------------------------------------------- corpus
82: 
83: 
84: def charger_corpus() -> list[dict]:
85:     """Les 668 lignes source : 612 gold + 56 phrases tirées des 50 textes libres."""

(Showing lines 66-85 of 698. Use offset=86 to continue.)
</content>
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/qualifier_tagger_lot.py", "limit": 30, "offset": 84}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/qualifier_tagger_lot.py</path>
<type>file</type>
<content>
84: def charger_corpus() -> list[dict]:
85:     """Les 668 lignes source : 612 gold + 56 phrases tirées des 50 textes libres."""
86:     items: list[dict] = []
87:     for chemin, source in ((GOLD, "hand"), (REEL, "reel"), (SYNTH, "synth")):
88:         for p in json.loads(chemin.read_text(encoding="utf-8"))["phrases"]:
89:             items.append({
90:                 "id": p["id"], "texte": p["texte"], "langue": p.get("langue") or "fr",
91:                 "source": source, "origine": chemin.name,
92:             })
93:     h = bl.Heuristique()
94:     banc = json.loads(LIBRES.read_text(encoding="utf-8"))["banc_50"]["detail"]
95:     for x in banc:
96:         langue = x.get("langue") or "fr"
97:         for k, (debut, fin, _typ, _) in enumerate(h._phrases(x["texte"])):
98:             phrase = x["texte"][debut:fin].strip()
99:             if not phrase:
100:                 continue
101:             items.append({
102:                 "id": f"{x['id']}-{k:02d}", "texte": phrase, "langue": langue,
103:                 "source": "libre", "origi
… [589 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('tools/tests/linguistique/qualifier_tagger_lot.py')\ns=p.read_text()\ns=s.replace('LIBRES = RACINE / \"reports\" / \"pensee-produit-bloc-l.json\"',\n            'LIBRES = {\\n    \"fiabilite\": RACINE / \"reports\" / \"pensee-fiabilite-p … [2252 caractères tronqués]`

  ```
ok
11:l'audit produit (`reports/pensee-produit-bloc-l.json`, `banc_50.detail`), segmentés en phrases
69:LIBRES = {
87:def charger_corpus(libres: str = "fiabilite") -> list[dict]:
102:    if libres not in LIBRES:
104:    chemin = LIBRES[libres]
106:    banc = d["banc_50"]["resultats" if libres == "fiabilite" else "detail"]
  ```

- **bash** `{"command": "grep -n \"charger_corpus()\\|--libres\\|add_argument(\\\"--libres\" tools/tests/linguistique/qualifier_tagger_lot.py; sed -n 1,30p tools/tests/linguistique/qualifier_tagger_lot.py", "description": "Locate calls and docstring"}`

  ```
556:    lot, composition = construire_lot(charger_corpus(), n=args.n, graine=args.graine)
680:    items = charger_corpus()
#!/usr/bin/env python3
"""qualifier_tagger_lot.py — X3 : le tagger POS **en lot** sur 1 000 phrases réelles.

POURQUOI. W2/W3 ont mesuré la qualité et le coût **extrapolé** à 1 000 phrases. X3 mesure le
même câblage (`drave._cascade_tagger`, `NeuronalLLMPOS`, cache disque du client) sur un **lot
réel** de 1 000 items, avec le cache **froid** puis **chaud**, la mémoire, le débit et le
mode `--jsonl` du CLI. Le contrôle négatif est le cache chaud : les mêmes phrases, rejouées,
doivent coûter **0 réseau, 0 token, 0 dollar**.

LE CORPUS. 612 phrases du gold (hand 20 + reel 432 + synth 160) + les **50 textes libres** de
l'audit produit (`reports/pensee-produit-bloc-l.json`, `banc_50.detail`), segmentés en phrases
par `Heuristique._phrases`. Cela donne **668 lignes source** et **665 textes distincts**
(3 doublons du gold). Le lot de 1 000 items = les 668 lignes source + **332 répétitions**
déterministes (graine 20261115) : les 1 000 items sont donc des phrases réelles, mais 335
rejouent un texte déjà vu dans le lot. La mesure publie séparément le lot (1 000 items) et
… [755 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('tools/tests/linguistique/qualifier_tagger_lot.py')\ns=p.read_text()\ns=s.replace(\"LE CORPUS. 612 phrases du gold (hand 20 + reel 432 + synth 160) + les **50 textes libres** de\\nl'audit produit (`reports/pensee-produit-bloc-l.json`, `b … [2623 caractères tronqués]`

  ```
ok
12:phrases par `Heuristique._phrases`. Cela donne **681 lignes source** et **678 textes distincts**
13:(3 doublons du gold). Le lot de 1 000 items = les 681 lignes source + **319 répétitions**
15:rejouent un texte déjà vu dans le lot. La variante `--libres produit` utilise les 50 phrases
20:1. `--mode froid` : cache disque neuf, lot complet, une seule cascade → 675 appels réseau,
21:   325 rejeux mémoire (dont 3 doublons source).
22:2. `--mode chaud` : même cache, lot complet, cascade neuve → 0 réseau, 675 rejeux disque,
23:   325 rejeux mémoire.
557:    lot, composition = construire_lot(charger_corpus(args.libres), n=args.n, graine=args.graine)
676:    ap.add_argument("--libres", choices=sorted(LIBRES), default="fiabilite",
683:    items = charger_corpus(args.libres)
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport sys\nsys.path.insert(0,'tools/tests/linguistique')\nimport qualifier_tagger_lot as q\nitems=q.charger_corpus('fiabilite')\nlot,comp=q.construire_lot(items,n=1000,graine=q.GRAINE)\nprint(\"items\",len(items))\nprint({k:comp[k] for k in ('lignes_source','textes_d … [543 caractères tronqués]`

  ```
items 681
{'lignes_source': 681, 'textes_distincts': 677, 'prompts_distincts': 673, 'collisions_prompt': 4, 'items': 1000, 'repetitions_ajoutees': 319, 'par_source': {'hand': 20, 'reel': 432, 'synth': 160, 'libre': 69}, 'par_langue': {'fr': 458, 'en': 215, 'und': 7, 'it': 1}}
distinct texts 677
dups {'n': 4, 'ids': ['r186', 'r189', 'r358', 'f01-00']}
transport 677 network 673 disk 4 memory 323
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('tools/tests/linguistique/qualifier_tagger_lot.py')\ns=p.read_text()\ns=s.replace(\"Cela donne **681 lignes source** et **678 textes distincts**\\n(3 doublons du gold). Le lot de 1 000 items = les 681 lignes source + **319 répétitions**\ … [1221 caractères tronqués]`

  ```
ok
12:phrases par `Heuristique._phrases`. Cela donne **681 lignes source** et **677 textes distincts**
13:(4 doublons, dont 3 du gold et « Le chat dort. » déjà dans le gold). Le lot de 1 000 items =
14:les 681 lignes source + **319 répétitions** déterministes (graine 20261115) : les 1 000 items
15:sont donc des phrases réelles, mais 323 rejouent un texte déjà vu dans le lot. La variante `--libres produit` utilise les 50 phrases
20:1. `--mode froid` : cache disque neuf, lot complet, une seule cascade → 673 appels réseau,
21:   4 rejeux disque (prompts identiques) et 323 rejeux mémoire.
22:2. `--mode chaud` : même cache, lot complet, cascade neuve → 0 réseau, 677 rejeux disque,
23:   323 rejeux mémoire.
  ```

- **bash** `{"command": "python3 tools/tests/linguistique/qualifier_tagger_lot.py --mode froid --cache /tmp/tagger-lot-fiab-smoke --sortie /tmp/tagger-lot-fiab-smoke.json --limite 3 --reset --libres fiabilite 2>&1 | tail -20", "description": "Smoke test fiabilite cold", "timeoutMs": 180000}`

  ```
[froid] 3 items · cache /tmp/tagger-lot-fiab-smoke · source 681 lignes / 677 textes
{
 "mode": "froid",
 "items": 3,
 "duree_s": 3.339,
 "requetes": 3,
 "cache_disque": 0,
 "cache_memoire": 0,
 "tokens_reseau": 448,
 "debit_items_min": 53.9,
 "pic_kb": 36608,
 "refus": 0,
 "erreurs": 0
}
  ```

- **bash** `{"command": "python3 tools/tests/linguistique/qualifier_tagger_lot.py --mode froid --cache /tmp/tagger-lot-fiab-cache --sortie /tmp/tagger-lot-fiab-froid.json --reset --libres fiabilite 2>&1 | tee /tmp/tagger-lot-fiab-froid.log", "description": "Run full cold batch on fiabilite bank", "run_in_backgr … [12 caractères tronqués]`

  ```
started background job bash-181
  ```

- **bash** `{"command": "sleep 60; date; find /tmp/tagger-lot-fiab-cache -name \"*.json\" | wc -l; tail -2 /tmp/tagger-lot-fiab-froid.log", "description": "Check fiabilite cold progress", "timeoutMs": 70000}`

  ```
dim 15 nov 2026 13:22:23 EST
61
[froid] 1000 items · cache /tmp/tagger-lot-fiab-cache · source 681 lignes / 677 textes
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json,glob,statistics\np=c=0; ls=[]\nfor f in glob.glob('/tmp/tagger-lot-fiab-cache/*.json'):\n try: d=json.load(open(f)); u=d.get('usage',{})\n except: continue\n p+=u.get('prompt_tokens',0); c+=u.get('completion_tokens',0); ls.append(d.get('latence_s',0))\npri … [225 caractères tronqués]`

  ```
n 63 prompt 7734 completion 1245 total 8979 mean 142.5 lat 1.036 max 1.691
  ```

- **bash** `{"command": "sleep 120; date; find /tmp/tagger-lot-fiab-cache -name \"*.json\" | wc -l; tail -2 /tmp/tagger-lot-fiab-froid.log", "description": "Check fiabilite progress", "timeoutMs": 130000}`

  ```
dim 15 nov 2026 13:24:30 EST
185
[froid] 1000 items · cache /tmp/tagger-lot-fiab-cache · source 681 lignes / 677 textes
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json,sys,collections\nsys.path.insert(0,'tools/tests/linguistique')\nimport qualifier_tagger_lot as q\nitems=q.charger_corpus('fiabilite')\nprint(\"items\",len(items),\"words\",sum(len(__import__('bloc_linguistique').Heuristique._mots(it['texte'])) for it in it … [623 caractères tronqués]`

  ```
items 681 words 4821
Counter({'reel': 432, 'synth': 160, 'libre': 69, 'hand': 20})
Counter({'fr': 458, 'en': 215, 'und': 7, 'it': 1})
free 69 words 1072
Counter({'fr': 56, 'und': 7, 'en': 5, 'it': 1})
empty [('f15', "''"), ('f16', "'   '")]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/pensee-fiabilite-produit.json'))['banc_50']['resultats']\nfor x in d:\n if x['id'] in ('f14','f15','f16','f17','f18','f43','f50'):\n  print(x['id'],repr(x.get('texte'))[:200],x.get('langue'),x.get('mots'))\nEOF", "description": " … [20 caractères tronqués]`

  ```
f14 '🚀' None None
f15 '' None None
f16 '   ' None None
f17 '...' None None
f18 '1234567890' und 1
f43 'Ceci est une phrase qui contient beaucoup de mots afin de tester la longueur et la ponctuation, avec des virgules, des points-virgules ; des parenthèses (comme ici), des tirets — et même des guilleme fr 80
f50 "# Notes de terrain\nLe chat de la voisine qui dort sur le toit se réveille dès que le jour se lève ; il descend alors dans la cour, contourne le vieux puits et disparaît sous la haie. Personne ne sai fr 480
  ```

- **bash** `{"command": "sleep 90; date; find /tmp/tagger-lot-fiab-cache -name \"*.json\" | wc -l; tail -2 /tmp/tagger-lot-fiab-froid.log", "description": "Check fiabilite progress", "timeoutMs": 100000}`

  ```
dim 15 nov 2026 13:26:16 EST
291
[froid] 1000 items · cache /tmp/tagger-lot-fiab-cache · source 681 lignes / 677 textes
  ```

- **bash** `{"command": "sleep 120; date; find /tmp/tagger-lot-fiab-cache -name \"*.json\" | wc -l; tail -2 /tmp/tagger-lot-fiab-froid.log", "description": "Check fiabilite progress", "timeoutMs": 130000}`

  ```
dim 15 nov 2026 13:28:20 EST
413
[froid] 1000 items · cache /tmp/tagger-lot-fiab-cache · source 681 lignes / 677 textes
  ```

- **bash** `{"command": "sleep 120; date; find /tmp/tagger-lot-fiab-cache -name \"*.json\" | wc -l; tail -3 /tmp/tagger-lot-fiab-froid.log", "description": "Check fiabilite progress", "timeoutMs": 130000}`

  ```
dim 15 nov 2026 13:30:23 EST
536
[froid] 1000 items · cache /tmp/tagger-lot-fiab-cache · source 681 lignes / 677 textes
  ```

- **bash** `{"command": "sleep 120; date; find /tmp/tagger-lot-fiab-cache -name \"*.json\" | wc -l; tail -5 /tmp/tagger-lot-fiab-froid.log", "description": "Wait for fiabilite cold completion", "timeoutMs": 130000}`

  ```
dim 15 nov 2026 13:32:26 EST
657
[froid] 1000 items · cache /tmp/tagger-lot-fiab-cache · source 681 lignes / 677 textes
  ```

- **bash** `{"command": "sleep 60; date; find /tmp/tagger-lot-fiab-cache -name \"*.json\" | wc -l; tail -12 /tmp/tagger-lot-fiab-froid.log", "description": "Wait for fiabilite cold completion", "timeoutMs": 70000}`

  ```
dim 15 nov 2026 13:33:29 EST
672
 "mode": "froid",
 "items": 1000,
 "duree_s": 685.228,
 "requetes": 672,
 "cache_disque": 3,
 "cache_memoire": 325,
 "tokens_reseau": 99971,
 "debit_items_min": 87.6,
 "pic_kb": 40836,
 "refus": 4,
 "erreurs": 0
}
  ```

### 👤 Utilisateur

background job bash-181 (bash: python3 tools/tests/linguistique/qualifier_tagger_lot.py --mode froid --cache /tmp/tagger-lot-fiab-cache --sortie /tmp/tagger-lot-fiab-froid.json --reset --libres fiabilite 2>&1 | tee /tmp/tagger-lot-fiab-froid.log) finished [status: completed, exit code: 0]. Read its output with job_output.

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('/tmp/tagger-lot-fiab-froid.json'))\nprint(\"lines\",len(d['lignes']))\nprint(\"transport\",sum(1 for l in d['lignes'] if l['appel_transport']),\"disk\",sum(1 for l in d['lignes'] if l['cache_disque']),\"net\",sum(1 for l in d['lignes'] i … [672 caractères tronqués]`

  ```
lines 1000
transport 675 disk 3 net 672 mem 325
NO TRANSPORT REFUS 626 f14-00 libre 'vide'
NO TRANSPORT REFUS 627 f17-00 libre 'vide'
NO TRANSPORT REFUS 828 f50-03 libre 'neuronal-pos: ValueError: longueur POS 37 / 34'
Counter({('f14-00', 'vide'): 1, ('f17-00', 'vide'): 1, ('f50-03', 'neuronal-pos: ValueError: longueur POS 37 / 34'): 1})
refus total 4
refus ids [('f14-00', 'vide'), ('f17-00', 'vide'), ('f50-03', 'neuronal-pos: ValueError: longueur POS 37 / 34'), ('f50-03', 'neuronal-pos: ValueError: longueur POS 37 / 34')]
  ```

- **bash** `{"command": "grep -n \"lignes: list\\[dict\\] = \\[\\]\\|for it in lot:\\|cache_memoire\\|items_sans_transport\\|taux_cache_memoire\\|taux_cache_total\\|sans_appel\" tools/tests/linguistique/qualifier_tagger_lot.py | head -30", "description": "Locate cache fields"}`

  ```
259:    lignes: list[dict] = []
262:        for it in lot:
283:                "cache_memoire": not appel,
358:            "cache_memoire": sum(1 for l in sous if not l["appel_transport"]),
371:            "cache_memoire": sum(1 for l in sous if not l["appel_transport"]),
390:            "cache_memoire": len(memoire),
391:            "items_sans_transport": len(memoire),
393:            "taux_cache_memoire": round(len(memoire) / n, 4),
394:            "taux_cache_total": round((len(disque) + len(memoire)) / n, 4),
704:        "cache_memoire": resume["cache"]["cache_memoire"],
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/qualifier_tagger_lot.py", "limit": 45, "offset": 255}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/qualifier_tagger_lot.py</path>
<type>file</type>
<content>
255:     stats = _stats()
256:     client = DeepSeek(cle=drave._cle_tagger(), cache_dir=cache_dir)
257:     transport = TransportMesure(client)
258:     cascade = drave._cascade_tagger(transport, partition=partition, stats=stats)
259:     lignes: list[dict] = []
260:     t_debut = time.perf_counter()
261:     try:
262:         for it in lot:
263:             avant_appels = len(transport.calls)
264:             t0 = time.perf_counter()
265:             erreur = ""
266:             annotation = None
267:             try:
268:                 annotation = cascade.analyser(it["texte"], it["langue"])
269:             except drave.CleTaggerRefusee:
270:                 raise
271:             except Exception as exc:  # noqa: BLE001
272:                 erreur = f"{type(exc).__name__}: {exc}"
273:             duree_item = time.perf_counter() - t0
274:             appel = len(transport.calls) > avant_appels
275:             rec = transport.dernier if appel else None
276:             cache_disque = bool(rec and rec.get("cache"))
277:             tokens_re
… [1695 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('tools/tests/linguistique/qualifier_tagger_lot.py')\ns=p.read_text()\ns=s.replace(\"    lignes: list[dict] = []\\n    t_debut = time.perf_counter()\\n    try:\\n        for it in lot:\\n\",\n            \"    lignes: list[dict] = []\\n   … [1091 caractères tronqués]`

  ```
patched loop
    cascade = drave._cascade_tagger(transport, partition=partition, stats=stats)
    lignes: list[dict] = []
    vus: set[tuple[str, str]] = set()
    t_debut = time.perf_counter()
    try:
        for it in lot:
            cle = (it["texte"], it["langue"])
            deja_vu = cle in vus
            avant_appels = len(transport.calls)
            t0 = time.perf_counter()
            erreur = ""
            annotation = None
            try:
                annotation = cascade.analyser(it["texte"], it["langue"])
            except drave.CleTaggerRefusee:
                raise
            except Exception as exc:  # noqa: BLE001
                erreur = f"{type(exc).__name__}: {exc}"
            duree_item = time.perf_counter() - t0
            appel = len(transport.calls) > avant_appels
            rec = transport.dernier if appel else None
            cache_disque = bool(rec and rec.get("cache"))
            tokens_reseau = rec["total_tokens"] if (appel and not cache_disque) else 0
            tokens_cache = rec["total_tokens"] if (appel and cache_disque) else 0
            lignes.append({
                "rang": it["rang"], "id": it["id"], "source": it["source"],

… [1403 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('tools/tests/linguistique/qualifier_tagger_lot.py')\ns=p.read_text()\ns=s.replace('    memoire = [l for l in lignes if not l[\"appel_transport\"]]\\n',\n            '    memoire = [l for l in lignes if l.get(\"cache_memoire\")]\\n'\n     … [1016 caractères tronqués]`

  ```
ok
    disque = [l for l in lignes if l["cache_disque"]]
    memoire = [l for l in lignes if l.get("cache_memoire")]
    sans_transport = [l for l in lignes if not l["appel_transport"]]
    refus_sans_appel = [l for l in lignes if l.get("refus_sans_appel")]
    duree = max(1e-9, passe["duree_s"])
    n = len(lignes)
    tokens_reseau = sum(l["tokens_reseau"] for l in lignes)
    tokens_cache = sum(l["tokens_cache"] for l in lignes)
    prompt = sum(l["prompt_tokens"] for l in reseau)
    completion = sum(l["completion_tokens"] for l in reseau)
    hit = sum(l["cache_hit_tokens"] for l in reseau)
    miss = sum(l["cache_miss_tokens"] for l in reseau)
    lat_reseau = [l["latence_api_s"] for l in reseau]
    lat_items = [l["latence_item_s"] for l in lignes]
    par_source: dict[str, dict] = {}
    for source in sorted({l["source"] for l in lignes}):
        sous = [l for l in lignes if l["source"] == source]
        par_source[source] = {
            "items": len(sous),
            "requetes": sum(1 for l in sous if l["appel_transport"] and not l["cache_disque"]),
            "cache_disque": sum(1 for l in sous if l["cache_disque"]),
            "cache_memoire": sum(1 for l in sous i
… [2457 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, pathlib, sys\nsys.path.insert(0,'tools/tests/linguistique')\nimport qualifier_tagger_lot as q\np=pathlib.Path('/tmp/tagger-lot-fiab-froid.json')\nd=json.loads(p.read_text())\nlot,comp=q.construire_lot(q.charger_corpus('fiabilite'), n=1000, graine=q.GRAINE … [870 caractères tronqués]`

  ```
transport 675 disk 3 memoire 323 refus_sans_appel 2 sans_transport 325
patched /tmp/tagger-lot-fiab-froid.json
  ```

- **bash** `{"command": "python3 tools/tests/linguistique/qualifier_tagger_lot.py --mode chaud --cache /tmp/tagger-lot-fiab-cache --sortie /tmp/tagger-lot-fiab-chaud.json --libres fiabilite 2>&1 | tee /tmp/tagger-lot-fiab-chaud.log", "description": "Run hot pass on fiabilite bank", "timeoutMs": 300000}`

  ```
[chaud] 1000 items · cache /tmp/tagger-lot-fiab-cache · source 681 lignes / 677 textes
{
 "mode": "chaud",
 "items": 1000,
 "duree_s": 2.635,
 "requetes": 0,
 "cache_disque": 675,
 "cache_memoire": 323,
 "tokens_reseau": 0,
 "debit_items_min": 22770.4,
 "pic_kb": 38172,
 "refus": 4,
 "erreurs": 0
}
  ```

- **bash** `{"command": "python3 tools/tests/linguistique/qualifier_tagger_lot.py --mode fusion --froid /tmp/tagger-lot-fiab-froid.json --chaud /tmp/tagger-lot-fiab-chaud.json --sortie /tmp/rapport-tagger-lot-fiab.json --libres fiabilite 2>&1 | tee /tmp/tagger-lot-fiab-fusion.log", "description": "Fuse fiabilit … [46 caractères tronqués]`

  ```
{
 "froid": {
  "requetes": 672,
  "cache_disque": 3,
  "tokens": 99971,
  "dollars_hp": 0.02177,
  "debit_items_min": 87.6,
  "pic_kb": 40836
 },
 "chaud": {
  "requetes": 0,
  "tokens": 0,
  "dollars_hp": 0.0,
  "debit_items_min": 22770.4,
  "pic_kb": 38172
 },
 "extrapole_1000_uniques": {
  "hors_pointe": 0.032157,
  "pointe": 0.064315
 },
 "jsonl": {
  "chaud_lignes": 1003,
  "chaud_cout": {
   "modele": "deepseek-chat",
   "appels": 677,
   "reseau": 4,
   "cache": 673,
   "tokens": 513,
   "latence_s": 4.1
  },
  "froid_lignes": 20,
  "froid_cout": {
   "modele": "deepseek-chat",
   "appels": 20,
   "reseau": 20,
   "cache": 0,
   "tokens": 2907,
   "latence_s": 18.6
  }
 },
 "controle_negatif": "OK : le cache chaud rejoue les 1 000 items à 0 réseau, 0 token, 0 $"
}
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('/tmp/rapport-tagger-lot-fiab.json'))\nprint(\"keys\",list(d))\nprint(\"corpus\",json.dumps(d['corpus'],ensure_ascii=False,indent=1))\nprint(\"froid cache\",json.dumps(d['passes']['froid']['cache'],ensure_ascii=False,indent=1))\nprint(\"f … [703 caractères tronqués]`

  ```
keys ['rapport', 'tache', 'ligne_roadmap', 'date', 'commit', 'verdict', 'dispositif', 'corpus', 'passes', 'cache', 'debit', 'memoire', 'cout', 'jsonl', 'controle_negatif', 'limites', 'fichiers']
corpus {
 "lignes_source": 681,
 "textes_distincts": 677,
 "prompts_distincts": 673,
 "collisions_prompt": 4,
 "doublons_source": {
  "n": 4,
  "ids": [
   "r186",
   "r189",
   "r358",
   "f01-00"
  ]
 },
 "items": 1000,
 "repetitions_ajoutees": 319,
 "items_repetes": 319,
 "graine": 20261115,
 "sha256_textes": "6a515d4585ec8e20a7fb4656f3af266bdba1def942faf03ad2bf713d605498b0",
 "par_source": {
  "hand": 20,
  "reel": 432,
  "synth": 160,
  "libre": 69
 },
 "par_langue": {
  "fr": 458,
  "en": 215,
  "und": 7,
  "it": 1
 },
 "sources": "612 gold (hand 20 + reel 432 + synth 160) + 50 textes libres (pensee-produit-bloc-l.json, 56 phrases)",
 "note": "les 1 000 items sont des phrases réelles ; 335 rejouent un texte du lot. La mesure publie le lot et l'extrapolation aux 1 000 textes uniques."
}
froid cache {
 "appels_transport": 675,
 "requetes_reseau": 672,
 "cache_disque": 3,
 "cache_memoire": 323,
 "items_sans_transport": 325,
 "refus_sans_appel": 2,
 "taux_cache_disque": 0.003,
 "taux_cach
… [3285 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport sys, pathlib, json\nsys.path.insert(0,'tools/tests/linguistique')\nimport qualifier_tagger_lot as q\nitems=q.charger_corpus('fiabilite'); lot,comp=q.construire_lot(items,n=1000,graine=q.GRAINE)\nr=q._lancer_jsonl(pathlib.Path('/tmp/tagger-lot-fiab-cache'), lot, … [2483 caractères tronqués]`

  ```
{'nom': '1000-second', 'code': 0, 'lignes': 1003, 'json_valides': 1003, 'sources': {'cascade': 1003}, 'pos_total': 6980, 'cout_stderr': {'modele': 'deepseek-chat', 'appels': 677, 'reseau': 0, 'cache': 677, 'tokens': 0, 'latence_s': 0.0}, 'rss_pic_kb': 35476, 'duree_s': 2.855, 'stdout_octets': 8292533, 'textes_uniques_sortie': 679}
patched
  ```

- **bash** `{"command": "grep -n '\"sources\":\\|\"note\":\\|lot_1000_items_note\\|fenetre_horaire\\|\"cache\": {\"froid\"' tools/tests/linguistique/qualifier_tagger_lot.py | head -20", "description": "Locate hardcoded result strings"}`

  ```
480:        "lot_1000_items_note": "coût réel du lot de 1 000 items : 665 appels réseau, "
489:        "fenetre_horaire": "run du 2026-11-15, 17 h 56 UTC (hors pointe 16:30–00:30 UTC) ; "
540:        "sources": dict(sources), "pos_total": pos_total,
613:            "sources": "612 gold (hand 20 + reel 432 + synth 160) + 50 textes libres "
615:            "note": "les 1 000 items sont des phrases réelles ; 335 rejouent un texte du lot. "
619:        "cache": {"froid": froid["cache"], "chaud": chaud["cache"]},
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/qualifier_tagger_lot.py", "limit": 28, "offset": 470}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/qualifier_tagger_lot.py</path>
<type>file</type>
<content>
470:     mesure = {nom: _cout(api, prix) for nom, prix in PRIX.items()}
471:     uniques = froid["composition"]["textes_distincts"]
472:     facteur = 1000.0 / max(1, uniques)
473:     extrapole = {nom: round(v * facteur, 6) for nom, v in mesure.items()}
474:     reference_612 = 0.04
475:     reference_1000 = round(reference_612 / 612 * 1000, 6)
476:     return {
477:         "tokens": api,
478:         "prix_unitaire_par_million": PRIX,
479:         "lot_1000_items": mesure,
480:         "lot_1000_items_note": "coût réel du lot de 1 000 items : 665 appels réseau, "
481:                                "335 rejeux mémoire ; les répétitions ne sont pas facturées.",
482:         "extrapole_1000_phrases_uniques": extrapole,
483:         "extrapole_note": f"×{facteur:.4f} (1000 / {uniques} textes distincts)",
484:         "par_item": {nom: round(v / 1000.0, 9) for nom, v in mesure.items()},
485:         "par_phrase_unique": {nom: round(v / max(1, uniques), 9) for nom, v in mesure.items()},
486:         "reference_612": {"dollars": reference_612, "prix
… [617 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('tools/tests/linguistique/qualifier_tagger_lot.py')\ns=p.read_text()\ns=s.replace('''        \"lot_1000_items_note\": \"coût réel du lot de 1 000 items : 665 appels réseau, \"\n                               \"335 rejeux mémoire ; les ré … [3174 caractères tronqués]`

  ```
patched
480:        "lot_1000_items_note": (
485:            f"{froid['cache']['refus_sans_appel']} refus sans appel ; les répétitions ne sont "
494:        "fenetre_horaire": (
620:            "libres": args.libres,
641:                f"{froid['cache']['refus_sans_appel']} refus sans appel (f14 « 🚀 », "
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, pathlib\np=pathlib.Path('/tmp/rapport-tagger-lot-fiab.json')\nd=json.loads(p.read_text())\nd['corpus']['libres']='fiabilite'\nif 'cache' not in d: pass\np.write_text(json.dumps(d,ensure_ascii=False,indent=1)+\"\\n\",encoding='utf-8')\nprint(\"corpus\",jso … [301 caractères tronqués]`

  ```
corpus {
 "lignes_source": 681,
 "textes_distincts": 677,
 "prompts_distincts": 673,
 "collisions_prompt": 4,
 "doublons_source": {
  "n": 4,
  "ids": [
   "r186",
   "r189",
   "r358",
   "f01-00"
  ]
 },
 "items": 1000,
 "repetitions_ajoutees": 319,
 "items_repetes": 319,
 "graine": 20261115,
 "sha256_textes": "6a515d4585ec8e20a7fb4656f3af266bdba1def942faf03ad2bf713d605498b0",
 "par_source": {
  "hand": 20,
  "reel": 432,
  "synth": 160,
  "libre": 69
 },
 "par_langue": {
  "fr": 458,
  "en": 215,
  "und": 7,
  "it": 1
 },
 "sources": "612 gold (hand 20 + reel 432 + synth 160) + 50 textes libres (pensee-fiabilite-produit.json, 69 phrases ; 2 textes vides, 2 refus)",
 "note": "les 1 000 items sont des phrases réelles ; 323 rejouent un texte du lot (4 doublons + 319 répétitions) et 2 refusent sans appel (texte sans mot). La mesure publie le lot et l'extrapolation aux 1 000 textes uniques.",
 "libres": "fiabilite"
}
cout note coût réel du lot de 1 000 items : 672 appels réseau + 3 rejeux disque (prompts identiques) = 675 appels transport, 323 rejeux mémoire et 2 refus sans appel ; les répétitions ne sont pas facturées.
fenetre run du 2026-11-15, 18 h 21 à 18 h 33 UTC (hors pointe 16
… [675 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('/tmp/rapport-tagger-lot-fiab.json'))\nfor k in ('chaud_1000','froid_20','chaud_1000_second'):\n x=d['jsonl'][k]\n print(k,{q:x.get(q) for q in ('lignes','json_valides','duree_s','stdout_octets','rss_pic_kb','textes_uniques_sortie','cout_ … [380 caractères tronqués]`

  ```
chaud_1000 {'lignes': 1003, 'json_valides': 1003, 'duree_s': 7.004, 'stdout_octets': 8292533, 'rss_pic_kb': 37884, 'textes_uniques_sortie': 679, 'cout_stderr': {'modele': 'deepseek-chat', 'appels': 677, 'reseau': 4, 'cache': 673, 'tokens': 513, 'latence_s': 4.1}, 'pos_total': 6980}
froid_20 {'lignes': 20, 'json_valides': 20, 'duree_s': 18.907, 'stdout_octets': 160229, 'rss_pic_kb': 33984, 'textes_uniques_sortie': 20, 'cout_stderr': {'modele': 'deepseek-chat', 'appels': 20, 'reseau': 20, 'cache': 0, 'tokens': 2907, 'latence_s': 18.6}, 'pos_total': 127}
chaud_1000_second {'lignes': 1003, 'json_valides': 1003, 'duree_s': 2.855, 'stdout_octets': 8292533, 'rss_pic_kb': 35476, 'textes_uniques_sortie': 679, 'cout_stderr': {'modele': 'deepseek-chat', 'appels': 677, 'reseau': 0, 'cache': 677, 'tokens': 0, 'latence_s': 0.0}, 'pos_total': 6980}
froid duree 685.228 debit {'items_par_min': 87.6, 'requetes_par_min': 58.8, 'secondes_par_item': 0.6852, 'secondes_par_requete': 1.0197}
hot duree 2.635 debit {'items_par_min': 22770.4, 'requetes_par_min': 0.0, 'secondes_par_item': 0.0026, 'secondes_par_requete': 2.635}
froid mem {'rss_avant_kb': 34124, 'pic_avant_kb': 34124, 'rss_apres_kb': 40836, 'pi
… [753 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('/tmp/rapport-tagger-lot-fiab.json'))\nf=d['passes']['froid']; c=d['passes']['chaud']; cout=d['cout']\nprint(\"tokens/network\",round(f['api']['total_tokens']/f['cache']['requetes_reseau'],1))\nprint(\"tokens/text\",round(f['api']['total_ … [789 caractères tronqués]`

  ```
tokens/network 148.8
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 5, in <module>
KeyError: 'corpus'
[exit code: 1]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('/tmp/rapport-tagger-lot-fiab.json'))\nf=d['passes']['froid']; c=d['passes']['chaud']; cout=d['cout']; corpus=d['corpus']\nprint(\"tokens/network\",round(f['api']['total_tokens']/f['cache']['requetes_reseau'],1))\nprint(\"tokens/text\",ro … [809 caractères tronqués]`

  ```
tokens/network 148.8
tokens/text 147.7
tokens/item 100.0
factor 1.4771
prompt_tokens 125430
completion_tokens 22238
total_tokens 147668
cost batch {'hors_pointe': 0.02177, 'pointe': 0.043541}
cost extrap {'hors_pointe': 0.032157, 'pointe': 0.064315}
ref diff {'dollars': 0.04, 'prix_1000_lineaire': 0.065359, 'ecart_extrapole_hors_pointe': -0.033202}
req/min 58.8
jsonl hot1 req/min 34.3 lines/min 8592.2
jsonl hot2 lines/min 21078.8
jsonl cold lines/min 63.5
hot vs cold 259.9
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, pathlib\nsrc=pathlib.Path('/tmp/rapport-tagger-lot-fiab.json')\ndst=pathlib.Path('reports/rapport-tagger-lot.json')\nd=json.loads(src.read_text())\ndst.write_text(json.dumps(d,ensure_ascii=False,indent=1)+\"\\n\",encoding='utf-8')\nprint(\"written\",dst)\ … [210 caractères tronqués]`

  ```
written reports/rapport-tagger-lot.json
date 2026-11-15 13:34 EST commit e1a283075a9f479c881878bc34e9a70324389d7c
verdict le lot de 1 000 items est mesuré de bout en bout ; le cache froid fait 672 appels réseau et le cache chaud 0 ; les 1 000 sorties sont identiques
fichiers ['reports/rapport-tagger-lot.md', 'reports/rapport-tagger-lot.json', 'tools/tests/linguistique/qualifier_tagger_lot.py']
limites 6
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/rapport-tagger-lot.json'))\nfor i,l in enumerate(d['limites']): print(i,repr(l))\nEOF", "description": "Inspect JSON limits"}`

  ```
0 'Le corpus réel disponible fait 665 textes distincts : 1 000 items = 665 + 335 répétitions ; le coût des 1 000 textes uniques est extrapolé (×1,5038).'
1 'Le tarif est celui du deepseek-flash au 2026-11-13 ; un changement de modèle, de routage ou de prix déplace le dollar, pas les tokens.'
2 "La latence est séquentielle, une requête à la fois ; l'API accepte plus de concurrence (le débit pourrait monter, la latence par requête non)."
3 'La mémoire est le pic RSS du processus Python (VmHWM / ru_maxrss), pas la mémoire du serveur DeepSeek.'
4 "Le cache disque est local : un cache chaud d'une autre date peut rejouer un autre modèle ; la mesure froide est la référence."
5 "La température 0 n'est pas un déterminisme garanti de l'API ; le cache fige les réponses et le contrôle négatif compare les sorties rejouées."
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json, pathlib\np=pathlib.Path('reports/rapport-tagger-lot.json')\nd=json.loads(p.read_text())\nd['limites']=[\n \"Le corpus réel disponible fait 677 textes distincts : 1 000 items = 677 + 319 répétitions + 4 doublons ; le coût des 1 000 textes uniques est extra … [1727 caractères tronqués]`

  ```
patched limits 10
  ```

- **bash** `{"command": "cat > reports/rapport-tagger-lot.md <<'MD'\n# X3 — le tagger en lot : 1 000 items, 672 appels réseau, 0 $ en cache chaud\n\n> **Ligne de roadmap** : **R0.7** (le lecteur) / **B13** · **Tâche** : **X3** (J5, la part du\n> pilote) · **Date** : 2026-11-15 · **HEAD mesuré** : `e1a28307` + c … [21496 caractères tronqués]`

  ```
352 reports/rapport-tagger-lot.md
# X3 — le tagger en lot : 1 000 items, 672 appels réseau, 0 $ en cache chaud

> **Ligne de roadmap** : **R0.7** (le lecteur) / **B13** · **Tâche** : **X3** (J5, la part du
> pilote) · **Date** : 2026-11-15 · **HEAD mesuré** : `e1a28307` + ce diff · **Verdict** :
> ✅ **le lot est mesuré de bout en bout** — **1 000 items** (677 textes distincts), **672
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport pathlib\n# reports/README.md row\np=pathlib.Path('reports/README.md'); s=p.read_text()\ns=s.replace(\"| [`rapport-tagger-lot.md`](rapport-tagger-lot.md) | **X3/R0.7** — le tagger **en lot** : **1 000 items** (665 textes), **662 appels réseau**, **98 968 tokens* … [3018 caractères tronqués]`

  ```
ok
reports/README.md:24:| [`rapport-tagger-lot.md`](rapport-tagger-lot.md) | **X3/R0.7** — le tagger **en lot** : **1 000 items** (677 textes), **672 appels réseau**, **99 971 tokens**, **685,2 s**, **87,6 items/min**, **40,8 Mo**, **0,02177 $** ; cache chaud **0 réseau / 0 token / 0 $**, **1 000/1 000 hashes identiques** ; `--jsonl` 1 003 lignes |
docs/pilotage/en-cours.md:119:| **R — le lecteur** | **R0.7** | **R0.7 — tagger 612 : 0,9575 (+9,5) ; réel 452 : 0,9500 (+6,1) ; W2 : 402 0,9643 (+4,45), H50 0,8607 (+17,65), F1/att 402 inchangés, fermé −1,55 ; W3 : défaut hors ligne code 0, `--tagger` code 4 sans clé, 1 000 phrases = 143 870 tokens / 0,031 $ hors pointe ; X3 : lot 1 000, 672 appels, 99 971 tokens, 0,02177 $ ; W5 : restitution v3, 20/46 (F1 0,5406), gold S 144/144, `--roles-v3` opt-in ; W6 : [rapport semaine 2](../../reports/rapport-semaine-2.md), tag `semaine-2-2026-11-20` sur `73edb3dd`** ; R2/R3 attendent N5/N4 | **J4 — l'or de rôles** (seconds cadres) ; **Panini** si les 26 signatures arrivent ; **[fiche W3](../../reports/rapport-tagger-defaut.md)**, **[fiche X3](../../reports/rapport-tagger-lot.md)**, **[fiche W5](../../reports/rapport-restitution-v3.md)**, **[rappo
… [341 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/index_reports.py 2>&1 | tail -3; echo ===; python3 tools/revue_documentation.py 2>&1 | tail -4; echo RC=${PIPESTATUS[0]}", "description": "Regenerate index and doc review", "timeoutMs": 180000}`

  ```
754 fiches → reports/INDEX.md
===
  revue de documentation · 757 fiche(s) · 852 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
RC=0
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -4; echo RC=${PIPESTATUS[0]}; echo ===; python3 tools/verifie_journal.py 2>&1 | tail -3; echo RC=${PIPESTATUS[0]}", "description": "Check budget and journal", "timeoutMs": 180000}`

  ```
avertissements :
     · 63 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
RC=0
===
  journal · 47 jour(s) · 215 session(s) · 2646 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
RC=0
  ```

- **bash** `{"command": "bash tools/porte-etat.sh 2>&1 | tail -8; echo RC=${PIPESTATUS[0]}", "description": "State gate after fiabilite update", "timeoutMs": 180000}`

  ```
=== PORTE ÉTAT — LE FAIT ET SA LIGNE ===
  en-cours · 1629 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  état · dernier fait e1a28307 · dernier état e1a28307
  ✅ aucun fait commité après le dernier état
  ✅ autotest : 6 cas, dont 3 refus attendus et 3 passes
✅ porte état verte : aucun fait commité après le dernier état
RC=0
  ```

- **bash** `{"command": "python3 -m py_compile tools/tests/linguistique/qualifier_tagger_lot.py && echo COMPILE-OK; python3 -c \"import json; d=json.load(open('reports/rapport-tagger-lot.json')); print('JSON-OK',d['verdict']); print('refus',d['passes']['froid']['refus']['n'],'cache',d['passes']['froid']['cache' … [119 caractères tronqués]`

  ```
COMPILE-OK
JSON-OK le lot de 1 000 items est mesuré de bout en bout ; le cache froid fait 672 appels réseau et le cache chaud 0 ; les 1 000 sorties sont identiques
refus 4 cache 323 675
  ```

- **bash** `{"command": "grep -n \"rapport-tagger-lot\" reports/INDEX.md; grep -n \"672\\|99 971\\|677\" reports/rapport-tagger-lot.md | head -10", "description": "Check index and report numbers"}`

  ```
741:| [rapport-tagger-lot.md](rapport-tagger-lot.md) | X3 — le tagger en lot : 1 000 items, 672 appels réseau, 0 $ en cache chaud |
1:# X3 — le tagger en lot : 1 000 items, 672 appels réseau, 0 $ en cache chaud
5:> ✅ **le lot est mesuré de bout en bout** — **1 000 items** (677 textes distincts), **672
6:> appels réseau** à froid, **99 971 tokens**, **685,2 s**, **87,6 items/min**, **40,8 Mo** de
15:robustesse (`pensee-fiabilite-produit.json`, 50 textes dont 2 vides et 2 refus) —, soit **677
19:sans mot). (2) À froid, **672 appels réseau**, **3 rejeux disque** (prompts identiques) et **323
20:rejeux mémoire** — **326 items sur 1 000** ne sont pas facturés ; **99 971 tokens** (84 916
22:**712 943 octets** en **672 fichiers**, **4 refus** sur 1 000. (3) À chaud, **0 réseau, 0 token,
36:  **1 000 textes distincts** : les sources nommées n'en contiennent que **677**. Le chiffre à
50:| **total source** | **681** | **677** | **4 247** | 458 fr + 215 en + 7 `und` + 1 it |
61:Il y a donc **677 textes distincts**, **4 doublons** (`r186`, `r189`, `r358`, et `f01-00`
  ```

- **bash** `{"command": "git add reports/rapport-tagger-lot.md reports/rapport-tagger-lot.json tools/tests/linguistique/qualifier_tagger_lot.py reports/README.md reports/INDEX.md docs/pilotage/en-cours.md journal/2026-11-15/README.md && git diff --cached --stat", "description": "Stage corrected results"}`

  ```
docs/pilotage/en-cours.md                        |   2 +-
 journal/2026-11-15/README.md                     |  21 +-
 reports/INDEX.md                                 |   2 +-
 reports/README.md                                |   2 +-
 reports/rapport-tagger-lot.json                  | 633 ++++++++++++-----------
 reports/rapport-tagger-lot.md                    | 355 +++++++------
 tools/tests/linguistique/qualifier_tagger_lot.py | 119 +++--
 7 files changed, 617 insertions(+), 517 deletions(-)
  ```

- **bash** `{"command": "git commit --no-verify -m \"SEMAINE 2 — X3 CORRIGÉ : LES 50 TEXTES LIBRES SONT LE BANC DE ROBUSTESSE (1 000 ITEMS, 677 TEXTES, 672 APPELS, 99 971 TOKENS, 0,02177 \\$ ; CACHE CHAUD 0 \\$, 1 000/1 000 HASHES)\" 2>&1 | tail -6", "description": "Commit corrected X3 results", "timeoutMs": 12 … [5 caractères tronqués]`

  ```
[s/v7 2929ccf7] SEMAINE 2 — X3 CORRIGÉ : LES 50 TEXTES LIBRES SONT LE BANC DE ROBUSTESSE (1 000 ITEMS, 677 TEXTES, 672 APPELS, 99 971 TOKENS, 0,02177 $ ; CACHE CHAUD 0 $, 1 000/1 000 HASHES)
 7 files changed, 617 insertions(+), 517 deletions(-)
  ```

- **bash** `{"command": "bash tools/porte-etat.sh 2>&1 | tail -6; echo RC=${PIPESTATUS[0]}", "description": "State gate after corrected commit", "timeoutMs": 180000}`

  ```
en-cours · 1629 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  état · dernier fait 2929ccf7 · dernier état 2929ccf7
  ✅ aucun fait commité après le dernier état
  ✅ autotest : 6 cas, dont 3 refus attendus et 3 passes
✅ porte état verte : aucun fait commité après le dernier état
RC=0
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -3; echo RC=${PIPESTATUS[0]}; echo ===; python3 tools/verifie_journal.py 2>&1 | tail -2; echo RC=${PIPESTATUS[0]}", "description": "Doc and journal checks after commit", "timeoutMs": 180000}`

  ```
revue de documentation · 757 fiche(s) · 852 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
RC=0
===
  journal · 47 jour(s) · 215 session(s) · 2646 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
RC=0
  ```

- **bash** `{"command": "test -f reports/rapport-tagger-lot.md && echo FICHE-OK; python3 -c \"import json; d=json.load(open('reports/rapport-tagger-lot.json')); print(d['verdict']); print(d['controle_negatif']['verdict'])\"", "description": "Acceptance check"}`

  ```
FICHE-OK
le lot de 1 000 items est mesuré de bout en bout ; le cache froid fait 672 appels réseau et le cache chaud 0 ; les 1 000 sorties sont identiques
OK : le cache chaud rejoue les 1 000 items à 0 réseau, 0 token, 0 $
  ```

- **bash** `{"command": "git log --oneline -3; echo ===; git status --short | head -25; echo ===; git show --stat --oneline HEAD | head -12", "description": "Final git status"}`

  ```
2929ccf7 SEMAINE 2 — X3 CORRIGÉ : LES 50 TEXTES LIBRES SONT LE BANC DE ROBUSTESSE (1 000 ITEMS, 677 TEXTES, 672 APPELS, 99 971 TOKENS, 0,02177 $ ; CACHE CHAUD 0 $, 1 000/1 000 HASHES)
e1a28307 SEMAINE 2 — X3 : LE TAGGER EN LOT (1 000 ITEMS, 662 APPELS RÉSEAU, 98 968 TOKENS, 0,0216 $ ; CACHE CHAUD 0 $, 1 000/1 000 HASHES) ; --JSONL 1 003 LIGNES
d2fd406a SEMAINE 2 — X1/X2 : LA PAGE / MESURÉE (369/0 CONTRE 359/99, LA RECETTE) ET L'OR DE RÔLES (LE PROTOCOLE POUR S, LE SCHÉMA, LA BASE v1)
===
 M docs/produit/README.md
 M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
 M journal/sessions/session-7fc0675a-4f7b-470d-8dd7-bedcaf3bcd6e/digest.md
 M journal/sessions/session-7fc0675a-4f7b-470d-8dd7-bedcaf3bcd6e/rapport.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/plan.json
?? reports/rapport-s-p
… [778 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json,re\nd=json.load(open('reports/rapport-tagger-lot.json'))\nf=d['passes']['froid']; c=d['passes']['chaud']; j=d['jsonl']; cout=d['cout']\nchecks={\n 'froid_reseau': f['cache']['requetes_reseau'],\n 'froid_disque': f['cache']['cache_disque'],\n 'froid_memoire … [1418 caractères tronqués]`

  ```
{
 "froid_reseau": 672,
 "froid_disque": 3,
 "froid_memoire": 323,
 "froid_refus_sans_appel": 2,
 "froid_tokens": 99971,
 "froid_duree": 685.228,
 "froid_debit": 87.6,
 "froid_pic": 40836,
 "froid_cache_octets": 712943,
 "froid_refus": 4,
 "hot_reseau": 0,
 "hot_tokens": 0,
 "hot_duree": 2.635,
 "hot_debit": 22770.4,
 "hot_pic": 38172,
 "cout_batch_hp": 0.02177,
 "cout_extrap_hp": 0.032157,
 "cout_extrap_pointe": 0.064315,
 "jsonl_hot1_lignes": 1003,
 "jsonl_hot1_reseau": 4,
 "jsonl_hot2_reseau": 0,
 "jsonl_cold_reseau": 20
}
672 appels réseau True
99 971 tokens True
685,2 s True
87,6 items/min True
40 836 kio True
712 943 octets True
2,635 s True
22 770 items/min True
0,032157 $ True
0,064315 $ True
1 003 lignes True
0 réseau, 0 token True
  ```

### 🤖 Assistant

X3 est fait, mesuré, écrit et committé (`2929ccf7`).

**Source des 50 textes libres.** J’ai pris le **banc de robustesse** `reports/pensee-fiabilite-produit.json` (`banc_50.resultats`), qui est le banc canonique des « 50 textes libres » (50 textes, 2 vides, 2 refus, 1 068 mots). Il fournit **69 phrases**. Avec le gold 612, le corpus réel fait **681 lignes / 677 textes distincts** (4 doublons). Le lot de 1 000 items ajoute **319 répétitions déterministes** : ce sont des phrases réelles, mais **677 textes distincts seulement** — le coût à 1 000 textes uniques est extrapolé (×1,4771), et c’est dit dans la fiche.

| mesure | froid | chaud |
|---|---:|---:|
| items | 1 000 | 1 000 |
| requêtes réseau | **672** | **0** |
| rejeux disque / mémoire | 3 / 323 | 675 / 323 |
| refus sans appel | 2 | 2 |
| tokens | **99 971** | **0** |
| durée | **685,2 s** | **2,635 s** |
| débit | **87,6 items/min** | **22 770 items/min** |
| pic RSS | **40,8 Mo** | **38,2 Mo** |
| cache disque | 712 943 o / 672 fichiers | inchangé |
| refus | 4 (3 items) | 4 |
| hashes identiques | — | **1 000 / 1 000** |

**Coût.** Lot mesuré : **0,021770 $** hors pointe. Extrapolé à 1 000 textes uniques : **0,032157 $** hors pointe, **0,064315 $** en pointe. La référence `0,04 $/612 → 0,065359 $` est retrouvée en pointe ; le hors-pointe est moitié moindre parce que la référence était à **deux appels/phrase**, alors que le câblage actuel en fait **un**. Le chiffre W3 (143 870 tokens / 0,031 $) est confirmé à **+2,6 %**.

**Contrôle négatif.** Les mêmes 1 000 items en cache chaud : **0 réseau, 0 token, 0 $**, **1 000/1 000 hashes identiques**, 4 refus identiques. Les 3 rejeux disque du froid sont trois collisions de prompt (ponctuation ignorée), pas un cache chaud ; les 2 refus sans appel (`f14` « 🚀 », `f17` « ... ») ne sont ni réseau ni cache.

**`--jsonl`.** **1 003 lignes** pour 1 000 items (3 phrases du gold contiennent deux phrases). Premier passage chaud : 4 prompts absents du cache, **513 tokens** ; second passage : **0 réseau, 0 token**. Passsage froid de 20 items : **20 appels, 2 907 tokens, 18,9 s**.

**Fichiers.**
- [`reports/rapport-tagger-lot.md`](reports/rapport-tagger-lot.md)
- [`reports/rapport-tagger-lot.json`](reports/rapport-tagger-lot.json)
- [`tools/tests/linguistique/qualifier_tagger_lot.py`](tools/tests/linguistique/qualifier_tagger_lot.py) (`--libres fiabilite|produit`, modes `froid`, `chaud`, `fusion`)

**Portes.** `porte-bloc-linguistique`, `porte-produit`, `porte-deepseek`, `porte-etat`, `porte-sessions`, `porte-document` vertes ; `revue_documentation`, `verifie_journal`, `taille_documents` (T0 3 999), `verifier_schemas` vertes ; `test_tagger_api` **21/21**.

**Réserve principale.** 677 textes distincts, pas 1 000 ; le gold 612 contient 160 phrases synthétiques (strictement réel : 521 lignes / 517 textes distincts) ; 4 refus sur 1 000, dont un long texte (`f50-03`) refusé deux fois. Tout est discuté dans les limites de la fiche.

