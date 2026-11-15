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
