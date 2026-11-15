# Session DSH — relecture

- identifiant : `session-3241a992-ffa6-4c12-ab1c-a8e175f880b7`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-15 03:55:11
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche B3 : le corpus d'or CIC (42 verdicts, 42/42 reproduits en J12.2) — étends le vérificateur : les 36 preuves altérées sont rejetées ; ajoute la vérification du **type de Bruijn** et le sha256 indépendant rejoué par une seconde implémentation ; fiche `reports/rapport-cic-v2.md` + JSON.

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

- **bash** `{"command": "pwd && ls -la && git status --short | head -50 && git log --oneline -10", "description": "Inspect repo root and git state"}`

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
drwxr-xr-x. 1 stephane stephane   198 15 nov 03:55 .git
-rw-r--r--. 1 stephane stephane   619 31 oct 17:33 .gitignore
-rw-r--r--. 1 stephane stephane   225  1 nov 10:50 .gitmodules
drwxr-xr-x. 1 stephane stephane   992 15 nov 01:33 journal
drwxr-xr-x. 1 stephane stephane   100  3 nov 09:12 models
drwxr-xr-x. 1 stephane stephane   114 25 sep 15:24 __pycache__
drwxr-xr-x. 1 stephane stephane    64  6 nov 09:52 .pytest_cache
-rw-r--r--. 1 stephane stephane  4992 25 sep 10:54 Qtrinet-bootstrap.md
-rw-r--r--. 1 stephane stephane 21293  6 nov 22:32 README.md
drwxr-xr-x. 1 stephane stephane 77034 15 nov 03:54 reports
-rw-r--r--. 1 stephane stephane 13100 28 oct 14:59 REPRISE.md
-rw---
… [2897 caractères tronqués]
  ```

- **bash** `{"command": "ls docs/pilotage reports journal 2>/dev/null | head -100", "description": "List key directories"}`

  ```
docs/pilotage:
backlog
chantiers.md
en-cours.md
manques.md
plan-travail.md
programme-r.md
README.md
references-non-regression.md
roadmap.md
semaine-autonome.md
utilisation.md

journal:
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
2026-10-05
2026-10-06
2026-10-07
2026-10-08
2026-10-09
2026-10-10
2026-10-11
2026-10-12
2026-10-13
2026-10-14
2026-10-15
2026-10-16
2026-10-17
2026-10-18
2026-10-19
2026-10-20
2026-10-21
2026-10-22
2026-10-23
2026-10-24
2026-10-25
2026-10-26
2026-10-27
2026-10-28
2026-10-29
2026-10-30
2026-10-31
2026-11-01
2026-11-02
2026-11-03
2026-11-04
2026-11-05
2026-11-06
2026-11-07
2026-11-13
2026-11-14
2026-11-15
README.md
sessions
THEMES.md

reports:
07
07-mesures-couche-commune.md
a26-bilan.json
a26-lot-disque.json
a80-audit-final.json
a80-indice-qualifie.json
a80-melange-qualifie.json
a80-pannes-ppl.json
a80-porte-adaptateur.json
a80-porte-budget.json
a80-porte-bus.json
a80-porte-bus-socket.json
a80-porte-c4-retard.json
a80-porte-consolidation.json
a80-porte-cycle-c2.json
a80-porte-delais.json
a80-porte-flux.json
a80-porte-fusion.json
a80-porte-gain.json
a80-porte-pont.json
a80-porte-profondeur.json
… [237 caractères tronqués]
  ```

- **bash** `{"command": "grep -ril \"CIC\" --include=\"*.py\" --include=\"*.md\" --include=\"*.json\" . | head -80", "description": "Find CIC references"}`

  ```
./reports/rapport-parcimonie-imposee.md
./reports/rapport-cycle-rapide.md
./reports/archive/rapport-campagne-benefices.md
./reports/campagne-benefices/008-05-les-modeles-entraines-ici-mesures-dans-l.md
./reports/restitution-udhr.json
./reports/restitution-udhr-flux.json
./reports/traduction-udhr-propre-7b.json
./reports/traduction-eurlex-0.5b.json
./reports/traduction-eurlex-1.5b.json
./reports/traduction-eurlex2509-7b.json
./reports/traduction-langues-7b.json
./reports/traduction-langues-3b.json
./reports/traduction-presse-7b.json
./reports/traduction-presse-3b.json
./reports/traduction-24langues-B.json
./reports/traduction-24langues-3b-B.json
./reports/traduction-onu-7b.json
./reports/traduction-onu-3b.json
./reports/traduction-onu6-7b.json
./reports/traduction-onu6-3b.json
./reports/r03-banc-durci-extractif.json
./reports/r03-banc-durci-modele.json
./reports/r07-routeur.json
./reports/ocr-pdf-cegep-detection.json
./reports/rapport-inventaire-panini.md
./reports/pensee-inventaire-panini.json
./reports/corpus-commun.json
./reports/retrieval-familles.json
./reports/rapport-bilan-chantier.json
./reports/rapport-bilan-chantier.md
./reports/rapport-panini-334.md
./reports/rapport-cic-
… [2076 caractères tronqués]
  ```

- **bash** `{"command": "grep -ril \"bruijn\\|de Bruijn\" --include=\"*.py\" --include=\"*.md\" --include=\"*.json\" . | head -80", "description": "Find de Bruijn references"}`

  ```
./reports/rapport-inventaire-panini.md
./reports/pensee-inventaire-panini.json
./reports/rapport-cic-verificateur.md
./reports/cic-verificateur.json
./tools/tests/cic/corpus_dor_cic_v1.json
./tools/tests/cic/manifeste.json
./tools/tests/test_verificateur_cic.py
./tools/chantier/plan.json
./tools/verificateur_cic.py
./journal/sessions/d629d7d7-e122-4596-8757-f4264a2b15cf/digest.md
./journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
./journal/sessions/bdefb627-485e-44d1-b11c-d15dd2e6b640/digest.md
./journal/sessions/session-a9b5216e-5f4b-4935-8ba0-2ec7d42aaf89/digest.md
./journal/sessions/session-3ffa6026-9a7d-4905-ac06-6b9708d65ba7/digest.md
./journal/sessions/session-c3f599ea-570a-4db4-ad78-8eff22004a4c/digest.md
./journal/sessions/session-c3f599ea-570a-4db4-ad78-8eff22004a4c/rapport.md
  ```

- **bash** `{"command": "grep -ril \"J12\" --include=\"*.py\" --include=\"*.md\" --include=\"*.json\" . | head -50", "description": "Find J12 references"}`

  ```
./reports/rapport-bilan-chantier.json
./reports/rapport-bilan-chantier.md
./reports/panini-334.json
./reports/rapport-panini-334.md
./reports/rapport-cic-verificateur.md
./reports/cic-verificateur.json
./reports/rapport-tableau-mesures.md
./reports/tableau-mesures.json
./reports/rapport-cloture-chantier.md
./reports/rapport-cloture-chantier.json
./reports/INDEX.md
./reports/README.md
./reports/rapport-atomes-prediction.md
./data/udhr/genealogie.json
./tools/tests/test_panini_334.py
./tools/tests/cic/manifeste.json
./tools/chantier/plan.json
./tools/panini_334.py
./tools/verificateur_cic.py
./journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
./journal/sessions/session-e1ad947b-50b1-4758-a921-5267225bf642/digest.md
./journal/sessions/session-932afd57-1363-4133-b6f1-64f7d937f38d/digest.md
./journal/sessions/session-1a1b15e7-d5f5-4f11-aeb3-0e6e42628dbe/digest.md
./journal/sessions/session-ce875934-0cf6-4434-a91d-cbca647b11b3/digest.md
./journal/sessions/session-6a9e96a0-20f8-4721-8b73-82eba29bd2b6/digest.md
./journal/sessions/session-6a9e96a0-20f8-4721-8b73-82eba29bd2b6/rapport.md
./journal/sessions/session-c3f599ea-570a-4db4-ad78-8eff22004a4c/digest.md
./journal/sessions
… [1137 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verificateur_cic.py"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/cic/README.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_verificateur_cic.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verificateur_cic.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """verificateur_cic.py — vérificateur INDÉPENDANT du corpus d'or CIC-lite.
3: 
4: Le corpus d'or CIC (`nipada/falsification/corpus_dor_cic_v1.json`, Panini/Research)
5: est un artefact portable : 3 définitions, 21 constantes et 42 entrées (36 attendues
6: « accepte », 6 attendues « rejette »). Chaque entrée porte une preuve et un type
7: sérialisés en **de Bruijn** (octets canoniques) et une empreinte
8: `sha256(preuve || type)`.
9: 
10: La doctrine du corpus est explicite : *toute implémentation doit reproduire
11: exactement ces verdicts à partir de cet artefact seul*. Ce module est cette
12: implémentation côté Drave. Il n'importe rien de Panini : il relit le JSON, décode
13: le format, recalcule les empreintes et rejoue les 42 jugements avec un noyau
14: CIC-lite réécrit ici.
15: 
16: Ce que le vérificateur contrôle
17: -------------------------------
18: 1. **Intégrité du fichier** : sha256 du corpus (la copie de Drave est
19:    byte-identique à l'original Panini).
20: 2. **Sérialisation canonique** : chaque terme (défs, constantes, p
… [51075 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/cic/README.md</path>
<type>file</type>
<content>
1: # Corpus d'or CIC-lite — copie portable Drave
2: 
3: Ce dossier contient la **copie byte-identique** du corpus d'or CIC de Panini/Research :
4: 
5: - source : `Panini/research/nipada/falsification/corpus_dor_cic_v1.json` ;
6: - sha256 : `3018f6f4349641534be3a73309a1b25ff4bc71a3975e7105f2c15b61da18aaec` ;
7: - commit source : `2130310db46ca9d59883500adc607bd86f534678` ;
8: - 46 714 octets, 3 définitions, 21 constantes, **42 entrées** (**36** attendues
9:   `accepte`, **6** attendues `rejette`).
10: 
11: Le fichier `manifeste.json` porte les empreintes de la source, du TSV et de la copie.
12: La copie existe pour que le vérificateur Drave soit **portable** : il n'a pas besoin
13: du dépôt Panini pour rejouer les 42 verdicts.
14: 
15: ## Ce qu'il faut lancer
16: 
17: ```bash
18: python3 tools/verificateur_cic.py --json     # mesure machine
19: python3 tools/verificateur_cic.py --verbeux  # une ligne par entrée
20: bash tools/porte-cic.sh                      # la porte : 42/42 + contrôles négatifs
21: python3 tools/tests/test_verificateur_cic.py # 21 tests
22: ```
23: 
… [203 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_verificateur_cic.py</path>
<type>file</type>
<content>
1: #!/usr/bin/env python3
2: """test_verificateur_cic.py — le banc du vérificateur indépendant du corpus d'or CIC.
3: 
4: Ce que le test fige :
5: - le corpus portable est byte-identique à l'artefact Panini (sha256) ;
6: - les 42 verdicts sont rejoués (36 acceptés, 6 rejetés), 42/42 d'accord ;
7: - les 42 empreintes `sha256(preuve || type)` sont valides ;
8: - la sérialisation de Bruijn est canonique (décodage puis ré-encodage identique) ;
9: - altérer un octet d'une preuve acceptée la fait rejeter (36/36), et l'énumération
10:   exhaustive des 1 020 mutations de `eq(2,2)` n'en accepte aucune ;
11: - un noyau « accepte tout » et un noyau « rejette tout » échouent (non-trivialité) ;
12: - un corpus localement corrompu (octet ou verdict) est détecté, pas absorbé.
13: """
14: from __future__ import annotations
15: 
16: import hashlib
17: import json
18: import pathlib
19: import subprocess
20: import sys
21: import tempfile
22: import unittest
23: 
24: RACINE = pathlib.Path(__file__).resolve().parents[2]
25: sys.path.insert(0, str(RACINE / "tools"))
26: 
27: im
… [10123 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-cic-verificateur.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-cic-verificateur.md</path>
<type>file</type>
<content>
1: # J12.2 — Le corpus d'or CIC : 42/42 verdicts rejoués par un vérificateur indépendant
2: 
3: > **Ligne de roadmap** : **L / R0.7** (le bloc langue) — chantier **Panini** · **Tâche** : **J12.2** ·
4: > **Date** : **2026-11-14** ·
5: > **Verdict** : ✅ **le corpus d'or CIC est portable et rejouable hors de Panini** — un noyau
6: > CIC-lite réécrit côté Drave, sans importer le code de Panini, rend **42/42** verdicts
7: > (**36** acceptés, **6** rejetés), **42/42** empreintes `sha256(preuve || type)` et **42/42**
8: > sérialisations canoniques. Le contrôle négatif tient : altérer le dernier octet des **36**
9: > preuves acceptées les fait **36/36** rejeter, et les **1 020** mutations d'un octet de
10: > `eq(2,2)` sont **1 020/1 020** rejetées. Un noyau « accepte tout » et un noyau « rejette
11: > tout » échouent (respectivement **6** et **36** désaccords) : le banc n'est pas vide.
12: >
13: > **Code mesuré** : `bb68b820` (HEAD au moment de la mesure) + le vérificateur de cette fiche.
14: > **JSON** : [`cic-verificateur.json`](cic-verificateur.json) ·
15: > **Ou
… [13420 caractères tronqués]
  ```

- **bash** `{"command": "python3 -c \"\nimport json\np='reports/cic-verificateur.json'\nd=json.load(open(p))\nprint(json.dumps({k:v for k,v in d.items() if k not in ('resultat','controles_negatifs')}, indent=1, ensure_ascii=False)[:8000])\nprint('--- result keys', list(d['resultat']))\nprint('--- controles', js … [128 caractères tronqués]`

  ```
{
 "tache": "J12.2",
 "titre": "Le corpus d'or CIC rejoué par un vérificateur indépendant côté Drave",
 "date": "2026-11-14",
 "ligne": "L / R0.7 (le bloc langue) — chantier Panini",
 "outil": "tools/verificateur_cic.py",
 "outil_sha256": "fd3e00b272174df3b2575ca43b23d6d4dff4ce8ce7ddb84a0e144beea5f4caed",
 "python": "3.13.16",
 "corpus": {
  "chemin": "tools/tests/cic/corpus_dor_cic_v1.json",
  "doctrine": "corpus d'or CIC-lite : preuve + type sérialisés (de Bruijn) + empreinte + verdict + ENVIRONNEMENT (defs/consts) ; toute implémentation doit reproduire exactement ces verdicts (validation croisée) à partir de cet artefact seul.",
  "sha256": "3018f6f4349641534be3a73309a1b25ff4bc71a3975e7105f2c15b61da18aaec",
  "sha256_attendu": "3018f6f4349641534be3a73309a1b25ff4bc71a3975e7105f2c15b61da18aaec",
  "sha256_ok": true,
  "octets": 46714,
  "source_panini": "Panini/research/nipada/falsification/corpus_dor_cic_v1.json",
  "commit_source": "2130310db46ca9d59883500adc607bd86f534678",
  "copie_drave_byte_identique": true
 },
 "environnement": {
  "defs": 3,
  "consts": 21,
  "serialisation_canonique": true,
  "echecs_serialisation": []
 },
 "noyau": {
  "fragment": "CIC-lite portable (de 
… [5741 caractères tronqués]
  ```

- **bash** `{"command": "cat tools/porte-cic.sh 2>/dev/null; echo '---'; cat tools/tests/cic/manifeste.json; echo '---'; python3 - <<'PY'\nimport json\nd=json.load(open('tools/tests/cic/corpus_dor_cic_v1.json'))\nprint(d.keys())\nprint('defs', list(d['defs']))\nprint('consts', list(d['consts']))\nprint('doctrin … [193 caractères tronqués]`

  ```
#!/bin/bash
# porte-cic.sh — le corpus d'or CIC est rejoué par un vérificateur INDÉPENDANT.
#
# POURQUOI CETTE PORTE EXISTE. Un corpus « d'or » ne vaut que si une seconde
# implémentation le rejoue sans importer la première. Cette porte exige :
#   1. 42/42 verdicts (36 acceptés, 6 rejetés) avec le noyau de Drave ;
#   2. 42/42 empreintes sha256(preuve || type) et 42/42 sérialisations canoniques ;
#   3. l'artefact portable byte-identique à la source Panini (sha256 du fichier) ;
#   4. le contrôle négatif : altérer un octet d'une preuve acceptée la rejette
#      (36/36), et les 1 020 mutations de eq(2,2) sont toutes rejetées ;
#   5. la non-trivialité : « accepte tout » et « rejette tout » échouent ;
#   6. un corpus localement corrompu est REFUSÉ (code 1), pas absorbé.
#
# Usage : tools/porte-cic.sh
set -u
cd "$(dirname "$0")/.."

echo "=== PORTE CIC — LE CORPUS D'OR REJOUÉ ==="
T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT

if ! python3 tools/verificateur_cic.py --json > "$T/mesure.json"; then
    echo "  ❌ le rejeu a échoué"
    python3 - "$T/mesure.json" <<'PY' 2>/dev/null || true
import json,sys
m=json.load(open(sys.argv[1]))
print(m.get("resultat",{}).get("desaccord"), "désaccord(s
… [5142 caractères tronqués]
  ```

- **bash** `{"command": "grep -rin \"B3\" docs/pilotage tools/chantier journal --include=\"*.md\" --include=\"*.json\" | head -60", "description": "Find B3 task references"}`

  ```
docs/pilotage/semaine-autonome.md:165:| J3.2 généalogie | ✅ fait | 154/154 paires hors script | `c2e629b3` |
docs/pilotage/semaine-autonome.md:199:| **J3** | après-midi : généalogie à deux faces | ✅ fait | **154/154** paires hors script au hasard ; **5/21 / 15/21 / 21/21** ; R² **0,256 / 0,230** | `c2e629b3` | signature V14 des 21 langues, matrice 9 dhātus, distance continue, corpus équilibré |
docs/pilotage/roadmap.md:274:| **B3** | le plan et la dynamique | ✅ **close** | aucune — le plan résiste (0,43), la ligne est close |
docs/pilotage/roadmap.md:449:- **clos** : B2.6 (le plan multi-tâches), B3 (le plan résiste), B4 (les opérateurs), B5/B6 (les jeux), B7/B8
docs/pilotage/en-cours.md:41:### Session `29ad180d-38a5-4481-a9a7-ec6ab31c895f` — S, les structures *(en pause)*
docs/pilotage/en-cours.md:43:- **Id** : `29ad180d-38a5-4481-a9a7-ec6ab31c895f` — [`plan.md`](../../journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/plan.md).
docs/pilotage/en-cours.md:54:- **Journal** : [la session](../../journal/sessions/29ad180d-38a5-4481-a9a7-ec6ab31c895f/).
docs/pilotage/en-cours.md:124:| **R — le lecteur** | **R0.7** | **R0.7 — tagger 612 : 0,9475 (+8,49), intégrer** ; R2/R3 attendent N5
… [12089 caractères tronqués]
  ```

- **bash** `{"command": "grep -rin \"cic\" docs/pilotage/en-cours.md docs/pilotage/roadmap.md docs/pilotage/semaine-autonome.md tools/chantier/plan.json 2>/dev/null | head -80", "description": "Find CIC in planning docs"}`

  ```
docs/pilotage/en-cours.md:98:- **Panini J12.1–J12.2** : §334 **495 paires uniques** ; CIC **42/42** verdicts, **42/42** empreintes, **36/36** preuves altérées rejetées, **1 020/1 020** mutations `eq(2,2)` rejetées ; [§334](../../reports/rapport-panini-334.md), [CIC](../../reports/rapport-cic-verificateur.md).
docs/pilotage/en-cours.md:108:| portes | **85** (dont `porte-cic` le 14/11) | `tools/porte-*.sh` |
docs/pilotage/roadmap.md:117:**J12.2 — le corpus d'or CIC rejoué hors de Panini.** Le corpus portable de Panini
docs/pilotage/roadmap.md:119:noyau **CIC-lite réécrit côté Drave**, sans importer le vérificateur de Panini : **42/42** verdicts,
docs/pilotage/roadmap.md:124:La copie `tools/tests/cic/corpus_dor_cic_v1.json` est **byte-identique** à la source
docs/pilotage/roadmap.md:125:(`3018f6f4…aaec`) ; la porte `tools/porte-cic.sh` et **21** tests rejouent le tout. C'est un
docs/pilotage/roadmap.md:128:[`fiche`](../../reports/rapport-cic-verificateur.md) + [`JSON`](../../reports/cic-verificateur.json).
docs/pilotage/roadmap.md:142:0,0445**, §334, CIC **42/42**), portes (**183/183**, passe **81/84**). La **base 612/602** est
docs/pilotage/semaine-autonome.md:53:- **7 axes** ; le no
… [1414 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\np=json.load(open('tools/chantier/plan.json'))\ndef walk(o, path=''):\n    if isinstance(o, dict):\n        if o.get('id')=='B3':\n            print(json.dumps(o, indent=1, ensure_ascii=False))\n        for k,v in o.items(): walk(v, path+'/'+str(k))\n    el … [123 caractères tronqués]`

  ```
{
 "id": "B3",
 "jour": 15,
 "titre": "Panini — le corpus d'or CIC étendu",
 "mandat": "Tâche B3 : le corpus d'or CIC (42 verdicts, 42/42 reproduits en J12.2) — étends le vérificateur : les 36 preuves altérées sont rejetées ; ajoute la vérification du **type de Bruijn** et le sha256 indépendant rejoué par une seconde implémentation ; fiche `reports/rapport-cic-v2.md` + JSON.",
 "budget_min": 90,
 "acceptation": [
  {
   "commande": "test -f reports/rapport-cic-v2.md && echo FICHE-OK",
   "attendu": "FICHE-OK"
  }
 ]
}
  ```

- **bash** `{"command": "sed -n '100,145p' docs/pilotage/roadmap.md; echo '--- en-cours 80-130'; sed -n '80,130p' docs/pilotage/en-cours.md", "description": "Read roadmap and current state around CIC"}`

  ```
J11.4 **ferme la suite produit** ; la prochaine action B13 est **trancher `g017`**.

**J12.1 — le §334 et les 44 signatures.** La deuxième vague Panini est **mesurée et auditée** :
les **655 lignes** de paires ne contiennent que **495 paires uniques** (**160 doublons**, **7
auto-paires**) et **48 textes** distincts, dont **44** ont une signature V14 ; les **102/107**
sources acquises ne sont pas 102 URL (71 URL uniques). La loi H0 se reproduit (**R² = 0,909139** sur
655 lignes, **0,906307** sur 488 paires uniques non auto) ; la date seule explique **0,258**, mais
n'ajoute que **0,0089** après la topologie (p=0,86). Le plan est **colinéaire** : 180 paires de même
tradition à **28,7 ans** d'écart (max 230), 308 paires inter-traditions à **1 189 ans**. Le contraste
de filiation à date fixe (**Δ=−0,166**, p=0,0005) **disparaît à surface contrôlée** (**Δ=−0,135**
contre null **−0,129**, p=0,335). Sur les 44 signatures, le retrieval brut donne **61,4 %** de même
tradition et **56,8 %** de voisins à ≤50 ans, mais les contrôles croisés ramènent la filiation à
**50,0 %** (p=0,0492, Holm 0,128) et l'époque à **53,8 %** (p=0,373) ; seule une petite prédiction
d'année intra-tradition survit (*
… [8821 caractères tronqués]
  ```

- **bash** `{"command": "ls -d ../Panini* ../*Panini* 2>/dev/null; find .. -maxdepth 3 -iname \"*corpus_dor_cic*\" 2>/dev/null | head -20; find .. -maxdepth 4 -path \"*nipada*\" -iname \"*cic*\" 2>/dev/null | head -30", "description": "Locate Panini source implementation"}`

  ```
../Panini
../Panini
../Panini-AttributionRegistry
../Panini-AttributionRegistry
../Panini-AutonomousMissions
../Panini-AutonomousMissions
../Panini-CloudOrchestrator
../Panini-CloudOrchestrator
../Panini-CoLabController
../Panini-CoLabController
../Panini-CopilotageShared
../Panini-CopilotageShared
../Panini-DatasetsIngestion
../Panini-DatasetsIngestion
../Panini-ExecutionOrchestrator
../Panini-ExecutionOrchestrator
../Panini-FS
../Panini-FS
../Panini-PublicationEngine
../Panini-PublicationEngine
../Panini-Research
../Panini-Research
../Panini-SemanticCore
../Panini-SemanticCore
../Panini-SpecKit-Shared
../Panini-SpecKit-Shared
../Panini-UltraReactive
../Panini-UltraReactive
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('tools/tests/cic/corpus_dor_cic_v1.json'))\nfor e in d['entrees'][:10]:\n    print(e['nom'])\n    print(json.dumps(e,indent=1,ensure_ascii=False)[:2000])\nPY", "description": "Inspect entry schema"}`

  ```
eq(2,2)
{
 "nom": "eq(2,2)",
 "verdict": "accepte",
 "preuve_hex": "0a070706",
 "type_hex": "0905070706070706",
 "empreinte": "f62bb346b8bb97f1870197e9870c1c2e1040be250f37121958cd32c6abca4813"
}
eq(4,4)
{
 "nom": "eq(4,4)",
 "verdict": "accepte",
 "preuve_hex": "0a0707070706",
 "type_hex": "090507070707060707070706",
 "empreinte": "8548bd462377798fe9730d0f82dda1320fad387c4144b503c2c7dadd557049b6"
}
eq(11,11)
{
 "nom": "eq(11,11)",
 "verdict": "accepte",
 "preuve_hex": "0a070707070707070707070706",
 "type_hex": "0905070707070707070707070706070707070707070707070706",
 "empreinte": "85695f19ab7cf484221ce243e53581a7544feda5969d9027c03f13ac51eee05c"
}
eq(a,c)
{
 "nom": "eq(a,c)",
 "verdict": "accepte",
 "preuve_hex": "04040404040403010003000003000103000203090003000200010309000400020001040b00050004030005030900060005000002090007000100040900080007000503090005000400020000000300010000110353796d110161110162110163110565715f6162110565715f6263",
 "type_hex": "09110353796d110161110163",
 "empreinte": "7ff10529da2c5ba1b173002355d726391b880d31ead69c0b958646f335d04d66"
}
sum(5,5,10)
{
 "nom": "sum(5,5,10)",
 "verdict": "accepte",
 "preuve_hex": "0a0707070707070707070706",
 "type_hex": "0905040410036
… [1367 caractères tronqués]
  ```

- **bash** `{"command": "find ../Panini -maxdepth 4 -type f \\( -iname \"*cic*\" -o -iname \"*formal*\" \\) 2>/dev/null | head -50", "description": "Find CIC files in Panini"}`

  ```
../Panini/research/nipada/falsification/corpus_dor_cic_v1.json
../Panini/research/nipada/falsification/corpus_dor_cic_v1.tsv
../Panini/research/scripts/cic_checker.cpp
../Panini/research/tests/formal/test_cic.py
../Panini/research/tests/formal/test_cic_cpp.py
  ```

- **bash** `{"command": "find ../Panini-Research -maxdepth 5 -type f \\( -iname \"*cic*\" -o -iname \"*falsification*\" \\) 2>/dev/null | head -50", "description": "Find CIC files in Panini-Research"}`

  ```
(no output)
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Panini/research/tests/formal/test_cic.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Panini/research/tests/formal/test_cic.py</path>
<type>file</type>
<content>
1: """Tests — substrat CIC-lite (noyau dépendant minimal, spec-défini).
2: 
3: Vérifie la doctrine (`VISION_TECHNIQUE_NOYAU_v1.0.md` §3) :
4:   - le checker `verify(terme, type)` est une fonction PURE, totale, déterministe ;
5:   - il ACCEPTE les termes de preuve des certitudes (refl, symm/trans via J,
6:     arithmétique Peano via ι-réduction, divisibilité via Σ-witness, syllogisme
7:     via composition) ;
8:   - il REJETTE les termes mal typés (jamais de faux théorème) ;
9:   - la conversion β/ι/δ normalise (add 2 3 ≡ 5, mul 2 2 ≡ 4).
10: 
11: La `Surface` ci-dessous est une mini-couche d'élaboration NON FIABLE (noms →
12: indices de de Bruijn) : elle n'est là que pour LISIBILITÉ des termes de preuve ;
13: seul `Kernel.check` fait foi.
14: """
15: import sys
16: from pathlib import Path
17: sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))
18: 
19: from nipada.formalkernel import cic as C
20: 
21: 
22: # ---------------------------------------------------------------------------
23: # Surface d'élaboration (non fiable) — noms → de
… [10358 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"de Bruijn\\|bruijn\\|sha256\\|type\\|type_hex\\|preuve\" ../Panini/research/nipada/falsification/*.py ../Panini/research/nipada/falsification/*.md 2>/dev/null | head -80", "description": "Find CIC generation/type docs in Panini"}`

  ```
../Panini/research/nipada/falsification/nipada_v346_pattern_mining_report.md:8:## Axe 1 — Profils de types d'ambiguïté
  ```

- **bash** `{"command": "find ../Panini/research/src -path \"*formalkernel*\" -type f | head -20; echo '---'; grep -n \"def hash_term\\|def serialize\\|def deserialize\\|def check\\|def verify\\|def infer\\|def conv\" ../Panini/research/src/nipada/formalkernel/cic.py | head -50", "description": "Find Panini CIC … [13 caractères tronqués]`

  ```
../Panini/research/src/nipada/formalkernel/__pycache__/certitudes.cpython-314.pyc
../Panini/research/src/nipada/formalkernel/__pycache__/cic.cpython-314.pyc
../Panini/research/src/nipada/formalkernel/__pycache__/cic_named.cpython-314.pyc
../Panini/research/src/nipada/formalkernel/__pycache__/core.cpython-314.pyc
../Panini/research/src/nipada/formalkernel/__pycache__/demonstrations.cpython-314.pyc
../Panini/research/src/nipada/formalkernel/__pycache__/elaboration.cpython-314.pyc
../Panini/research/src/nipada/formalkernel/__pycache__/entiers.cpython-314.pyc
../Panini/research/src/nipada/formalkernel/__pycache__/exploit_grammar.cpython-314.pyc
../Panini/research/src/nipada/formalkernel/__pycache__/exploitation.cpython-314.pyc
../Panini/research/src/nipada/formalkernel/__pycache__/extraction.cpython-314.pyc
../Panini/research/src/nipada/formalkernel/__pycache__/golden_corpus.cpython-314.pyc
../Panini/research/src/nipada/formalkernel/__pycache__/hypotheses.cpython-314.pyc
../Panini/research/src/nipada/formalkernel/__pycache__/logic_core.cpython-314.pyc
../Panini/research/src/nipada/formalkernel/__pycache__/parallele.cpython-314.pyc
../Panini/research/src/nipada/formalkernel/__pycache__/
… [811 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"hash_term\\|sha256\\|de Bruijn\\|de_bruijn\\|type\" ../Panini/research/src/nipada/formalkernel/cic.py | head -80", "description": "Inspect hash/type functions in Panini kernel"}`

  ```
9:déterministe `check : (contexte, terme, type) → {ok, ko}`.
19:Syntaxe (termes en indices de de Bruijn ; `#0` = lieur le plus récent) :
22:             |   #i                        variable (de Bruijn)
26:             |   ℕ                         type des entiers
30:             |   Id(A; a; b)               type identité (a, b : A)
39:Contexte Γ = suite de types (chaque entrée type un lieur).
94:  - pas de vérification de positivité/garde (les types inductifs sont FIXES, pas
105:# Syntaxe — constructeurs (indices de de Bruijn)
177:    Contrairement à `sigma` (prédicatif, réservé aux types de DONNÉES — ℤ, ℚ, ℝ),
179:    si ℝ est un grand type (niveau 1). Indispensable à la complétude de ℝ (sup)."""
197:    """W-type `W(A, B)` : arbres bien fondés — le type inductif GÉNÉRAL de
198:    Martin-Löf (jalon J5). `A` = type des « formes » (nœuds), `B : A → ★` =
207:    """Constructeur de W-type : `sup a f : W(A,B)` si `a:A` et `f : B a → W(A,B)`."""
212:    """Récurseur de W-type : `wrec A B C h t : C t` si `C : W(A,B) → ★_j`,
280:# -- List (premier « type inductif riche » — fondation de la RÉFLEXION) ------
288:    """La liste vide `[] : List A` (type vérifié par `check`, A ambigu).""
… [3268 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1540,1670p' ../Panini/research/src/nipada/formalkernel/cic.py", "description": "Read Panini serialization/hash"}`

  ```
n >>= 7
        if n:
            out.append(b | 0x80)
        else:
            out.append(b)
            return bytes(out)


def _read_varint(buf: bytes, i: int):
    shift, val = 0, 0
    while True:
        b = buf[i]
        i += 1
        val |= (b & 0x7F) << shift
        if not (b & 0x80):
            return val, i
        shift += 7


def serialize(t) -> bytes:
    """Encodage CANONIQUE d'un terme (de Bruijn) → octets. Déterministe.

    Un même terme (α-équivalent = structurellement identique en de Bruijn) donne
    exactement les mêmes octets : c'est le format d'artefact portable.
    """
    tag = _TAGS[t[0]]
    if tag == 0x00:                                    # var
        return bytes([tag]) + _varint(t[1])
    if tag == 0x01:                                    # sort (niveau)
        return bytes([tag]) + _varint(t[1])
    if tag in (0x05, 0x06, 0x12, 0x13, 0x14, 0x17, 0x18, 0x19, 0x1C, 0x1F, 0x21, 0x22):  # nat, zero, unit, tt, empty, bool, true, false, nil, expr, ezero, eone
        return bytes([tag])
    if tag in (0x07, 0x0A, 0x0E, 0x0F, 0x1B, 0x20):   # suc, refl, fst, snd, list, evar
        return bytes([tag]) + serialize(t[1])
    if tag in (0x02, 0x03, 0
… [3229 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"empreinte\\|sha256\\|hash_term\\|preuve_hex\\|type_hex\\|42\\|def .*corpus\" ../Panini/research/src/nipada/formalkernel/golden_corpus.py | head -80", "description": "Inspect Panini golden corpus generator"}`

  ```
5:(preuve, type) sérialisé en de Bruijn (hex) + son empreinte SHA-256 + le verdict
25:def construire_corpus() -> dict:
126:                    "+ empreinte + verdict + ENVIRONNEMENT (defs/consts) ; toute "
139:        "preuve_hex": C.serialize(preuve).hex(),
140:        "type_hex": C.serialize(ty).hex(),
141:        # empreinte du COUPLE (preuve, type) — la même preuve (ex. refl(4)) peut
143:        "empreinte": hashlib.sha256(C.serialize(preuve) + C.serialize(ty)).hexdigest(),
147:def verifier_avec(checker_fn, corpus: dict) -> list[dict]:
155:        preuve, _ = C.deserialize(bytes.fromhex(e["preuve_hex"]))
156:        ty, _ = C.deserialize(bytes.fromhex(e["type_hex"]))
165:def reconstruire_kernel(corpus: dict) -> C.Kernel:
177:def sauvegarder(corpus: dict, path) -> None:
182:def sauvegarder_plat(corpus: dict, path) -> None:
186:    (`nom \\t verdict \\t preuve_hex \\t type_hex`). Le doublon C++ lit l'ENVIRONNEMENT
197:    lignes.append("nom\tverdict\tpreuve_hex\ttype_hex")
199:        lignes.append(f"{e['nom']}\t{e['verdict']}\t{e['preuve_hex']}\t{e['type_hex']}")
  ```

- **bash** `{"command": "grep -rin \"rapport-cic-v2\\|cic-v2\\|type de Bruijn\\|type de bruijn\\|sha256 indépendant\\|seconde implémentation\" journal docs reports tools --include=\"*.md\" --include=\"*.json\" --include=\"*.py\" 2>/dev/null | head -80", "description": "Search for v2/hardening hints"}`

  ```
journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md:2283:| **0.3 codec de référence** | `tools/flux_codec.py` — la **seconde implémentation** du format DRVF | aller-retour **IDENTIQUE** sur 132 396 736 octets ; encodage 40 Mo/s, décodage 15 Mo/s en Python ; projection phase 3 : 512 jetons = **265 Mo** sur le fil |
journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:22039:| **0.3 codec de référence** | `tools/flux_codec.py` — la **seconde implémentation** du format DRVF | aller-retour **IDENTIQUE** sur 132 396 736 octets ; encodage 40 Mo/s, décodage 15 Mo/s en Python ; projection phase 3 : 512 jetons = **265 Mo** sur le fil |
journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:30707:D7 (MOYEN) — le contrôle indépendant du dépôt ne connaît pas le mode 4 : tools/pair_factice.py:17-18 (pas de mode 4) et :76 (`n*4` octets). Preuve : « mode 4 · n=16 · corps 64 octets » au lieu de 23 248 → désynchronisation, puis mort du client. Le mode 4 n'a donc AUCUNE vérification par une seconde implémentation.
journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:30798:**Preuve** : face à un flux mode 4 de `t=16`, il annonce `corps 64 octets` (au lieu de
… [5336 caractères tronqués]
  ```

- **bash** `{"command": "ls reports | grep -i \"v2\\|cic\"; echo '--- recent reports by mtime'; ls -lt reports/*.md | head -20; echo '--- index head'; sed -n '1,80p' reports/INDEX.md", "description": "Inspect report naming and index"}`

  ```
cic-verificateur.json
pensee-attachement-v2.json
pensee-audit-v2.json
pensee-echecs-v2.json
pensee-pos-anglais-v2.json
pensee-schema-v2.json
r04-tete-survol-v2.json
rapport-audit-v2.md
rapport-cic-verificateur.md
rapport-coordination-n2-v2.json
rapport-coordination-n2-v2.md
rapport-coordination-s-v2.json
rapport-coordination-s-v2.md
rapport-echecs-v2.md
rapport-pensee-attachement-v2.md
rapport-pos-anglais-v2.md
rapport-schema-v2-doc.md
rapport-schema-v2.md
schema-v2-doc.json
--- recent reports by mtime
-rw-r--r--. 1 stephane stephane  27038 15 nov 03:54 reports/rapport-atomes-prediction.md
-rw-r--r--. 1 stephane stephane  21601 15 nov 03:46 reports/README.md
-rw-r--r--. 1 stephane stephane  29978 15 nov 03:03 reports/rapport-protocole-date.md
-rw-r--r--. 1 stephane stephane  26036 15 nov 02:45 reports/rapport-gold-reel-50.md
-rw-------. 1 stephane stephane  23828 15 nov 02:30 reports/rapport-coordination-s-v2.md
-rw-r--r--. 1 stephane stephane 102003 15 nov 02:25 reports/INDEX.md
-rw-------. 1 stephane stephane  15412 15 nov 02:12 reports/rapport-coordination-n2-v2.md
-rw-------. 1 stephane stephane  10801 15 nov 01:42 reports/rapport-tagger-option.md
-rw-r--r--. 1 stephane stephan
… [10941 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('tools/tests/cic/corpus_dor_cic_v1.json'))\nacc=[e for e in d['entrees'] if e['verdict']=='accepte']\nprint('acceptes',len(acc),'bytes total',sum(len(e['preuve_hex'])//2 for e in acc))\nprint('max',max((len(e['preuve_hex'])//2,e['nom']) fo … [86 caractères tronqués]`

  ```
acceptes 36 bytes total 17400
max (6705, 'mul_comm')
all prefixes?
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys,json\nsys.path.insert(0,'tools')\nimport verificateur_cic as vc\nd=json.load(open('tools/tests/cic/corpus_dor_cic_v1.json'))\ndefs={k:vc.decode_exact(v) for k,v in d['defs'].items()}\nconsts={k:vc.decode_exact(v) for k,v in d['consts'].items()}\nk=vc.Kernel( … [229 caractères tronqués]`

  ```
eq(2,2)                  accepte  type_infer=('sort', 0)
eq(4,4)                  accepte  type_infer=('sort', 0)
eq(11,11)                accepte  type_infer=('sort', 0)
eq(a,c)                  accepte  type_infer=('sort', 0)
sum(5,5,10)              accepte  type_infer=('sort', 0)
sum(2,1,3)               accepte  type_infer=('sort', 0)
prod(2,3,6)              accepte  type_infer=('sort', 0)
prod(2,2,4)              accepte  type_infer=('sort', 0)
divides(2,4)             accepte  type_infer=('sort', 0)
divides(3,9)             accepte  type_infer=('sort', 0)
divides(6,12)            accepte  type_infer=('sort', 0)
divides(7,7)             accepte  type_infer=('sort', 0)
less(2,5)                accepte  type_infer=('sort', 0)
less(4,9)                accepte  type_infer=('sort', 0)
less(1,3)                accepte  type_infer=('sort', 0)
less(1,4)                accepte  type_infer=('sort', 0)
is(socrate,mortel)       accepte  type_infer=('sort', 0)
is(socrate,périssable)   accepte  type_infer=('sort', 0)
implies(homme,périssable) accepte  type_infer=('sort', 0)
teaches(socrate,aristote) accepte  type_infer=('sort', 0)
not(eq(4,5))             accepte  type_infer=('sort', 0)
n
… [1195 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys,json\nsys.path.insert(0,'tools')\nimport verificateur_cic as vc\nd=json.load(open('tools/tests/cic/corpus_dor_cic_v1.json'))\nLIEURS=vc.LIEURS\ndef hors(t,depth=0,acc=None):\n    if acc is None: acc=[]\n    tag=t[0]\n    if tag=='var':\n        if t[1]>=dept … [907 caractères tronqués]`

  ```
bad []
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys,json\nsys.path.insert(0,'tools')\nimport verificateur_cic as vc\nd=json.load(open('tools/tests/cic/corpus_dor_cic_v1.json'))\ndefs={k:vc.decode_exact(v) for k,v in d['defs'].items()}\nconsts={k:vc.decode_exact(v) for k,v in d['consts'].items()}\nk=vc.Kernel( … [365 caractères tronqués]`

  ```
eq(2,2)                  infer=ok conv=True
eq(4,4)                  infer=ok conv=True
eq(11,11)                infer=ok conv=True
eq(a,c)                  infer=ok conv=True
sum(5,5,10)              infer=ok conv=True
sum(2,1,3)               infer=ok conv=True
prod(2,3,6)              infer=ok conv=True
prod(2,2,4)              infer=ok conv=True
divides(2,4)             infer=None conv=False
divides(3,9)             infer=None conv=False
divides(6,12)            infer=None conv=False
divides(7,7)             infer=None conv=False
less(2,5)                infer=None conv=False
less(4,9)                infer=None conv=False
less(1,3)                infer=None conv=False
less(1,4)                infer=None conv=False
is(socrate,mortel)       infer=ok conv=True
is(socrate,périssable)   infer=ok conv=True
implies(homme,périssable) infer=ok conv=True
teaches(socrate,aristote) infer=ok conv=True
not(eq(4,5))             infer=ok conv=True
not(prod(2,2,5))         infer=ok conv=True
not(less(2,1))           infer=ok conv=True
transport                infer=ok conv=True
ap                       infer=ok conv=True
symm                     infer=ok conv=True
trans                    infer
… [409 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys,json\nsys.path.insert(0,'tools')\nimport verificateur_cic as vc\nd=json.load(open('tools/tests/cic/corpus_dor_cic_v1.json'))\ndefs={k:vc.decode_exact(v) for k,v in d['defs'].items()}\nconsts={k:vc.decode_exact(v) for k,v in d['consts'].items()}\nk=vc.Kernel( … [222 caractères tronqués]`

  ```
def add infer= ('pi', ('nat',), ('pi', ('nat',), ('nat',)))
def mul infer= ('pi', ('nat',), ('pi', ('nat',), ('nat',)))
def pred infer= ('pi', ('nat',), ('nat',))
const Obj type= ('sort', 0) niveau= 1
const homme type= ('pi', ('const', 'Obj'), ('sort', 0)) niveau= 1
const mortel type= ('pi', ('const', 'Obj'), ('sort', 0)) niveau= 1
const perissable type= ('pi', ('const', 'Obj'), ('sort', 0)) niveau= 1
const socrate type= ('const', 'Obj') niveau= 0
const hom_mort type= ('pi', ('const', 'Obj'), ('pi', ('app', ('const', 'homme'), ('var', 0)), ('app', ('const', 'mortel'), ('var', 1)))) niveau= 0
const mort_per type= ('pi', ('const', 'Obj'), ('pi', ('app', ('const', 'mortel'), ('var', 0)), ('app', ('const', 'perissable'), ('var', 1)))) niveau= 0
const soc_hom type= ('app', ('const', 'homme'), ('const', 'socrate')) niveau= 0
const Sym type= ('sort', 0) niveau= 1
const a type= ('const', 'Sym') niveau= 0
const b type= ('const', 'Sym') niveau= 0
const c type= ('const', 'Sym') niveau= 0
const eq_ab type= ('id', ('const', 'Sym'), ('const', 'a'), ('const', 'b')) niveau= 0
const eq_bc type= ('id', ('const', 'Sym'), ('const', 'b'), ('const', 'c')) niveau= 0
const teaches type= ('pi', ('const', '
… [898 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/methode/resultats.md", "limit": 220}`

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

- **bash** `{"command": "python3 tools/revue_documentation.py --help 2>&1 | head -40; echo '---'; sed -n '1,160p' tools/porte-tableaux.sh", "description": "Inspect documentation review tools"}`

  ```
revue de documentation · 740 fiche(s) · 834 JSON · 123 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
---
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
#      on écri
… [6964 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys,json\nsys.path.insert(0,'tools')\nimport verificateur_cic as vc\nd=json.load(open('tools/tests/cic/corpus_dor_cic_v1.json'))\ndefs={k:vc.decode_exact(v) for k,v in d['defs'].items()}\nconsts={k:vc.decode_exact(v) for k,v in d['consts'].items()}\nk=vc.Kernel( … [407 caractères tronqués]`

  ```
mutated type still accepted 0 []
  ```

- **bash** `{"command": "sed -n '240,300p' docs/pilotage/roadmap.md; echo '---'; grep -n \"Panini\\|B1[0-9]\\|B2[0-9]\" docs/pilotage/roadmap.md | head -60", "description": "Inspect roadmap B section"}`

  ```
Les durées sont des ordres de grandeur ; les dépendances réelles sont dans le [graphe du backlog](backlog/dependances.md).*

---

## Programme A — Le moteur (la drave, les flux)

Le moteur est **mature** : les six axes de la vision ont leurs mesures. Les lignes restantes sont des **lignes
ouvertes**, des **bloqués nommés** ou des **opt-in** à passer par défaut. Le détail chiffré et les fiches sont dans l'archive A/B.

| # | chantier | état | prochaine action |
|---|---|---|---|
| **A1** | observer et régler : [trace](../theorie/glossaire/entrees/trace.md) v3, [diff par couche](../theorie/glossaire/entrees/diff-par-couche.md), profilage, décision par [couche](../theorie/glossaire/entrees/couche.md) | ✅ | aucune — la table est faite, la [quantification](../theorie/glossaire/entrees/quantification.md) testée |
| **A2** | placer sur une machine : [KV](../theorie/glossaire/entrees/kv.md) paginé, [GPU](../theorie/glossaire/entrees/gpu-quadro-rtx-5000-miroir-vram-deport.md), [top-k](../theorie/glossaire/entrees/top-k.md), ordonnanceur | ✅ / ⚠️ | **partielle** — tête 4 bits refusée (+10 % PPL), experts bloqués par **A6.2** ; [`bilan`](../../reports/rapport-a26-bilan.md) |
| **A3** | répart
… [24452 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,80p' docs/pilotage/en-cours.md; echo '--- tail'; tail -80 docs/pilotage/en-cours.md", "description": "Read en-cours structure"}`

  ```
# En ce moment

**Mis à jour : 2026-11-15, 03 h 46 HNE (B2 : atomes → niveaux, négatif contrôlé)**

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
> le hook pre-co
… [12604 caractères tronqués]
  ```

- **bash** `{"command": "ls -la journal/2026-11-15/ 2>/dev/null; ls -la journal/sessions | tail -10; date '+%Y-%m-%d %H:%M %Z'", "description": "Inspect journal date folder and current date"}`

  ```
total 24
drwxr-xr-x. 1 stephane stephane   94 15 nov 02:32 .
drwxr-xr-x. 1 stephane stephane  992 15 nov 01:33 ..
-rw-r--r--. 1 stephane stephane 1541 15 nov 03:53 distribue.md
-rw-r--r--. 1 stephane stephane  905 15 nov 03:53 docs.md
-rw-r--r--. 1 stephane stephane 2397 15 nov 03:53 mesures.md
-rw-r--r--. 1 stephane stephane 1412 15 nov 03:53 portes.md
-rw-r--r--. 1 stephane stephane 4164 15 nov 03:53 README.md
drwxr-xr-x. 1 stephane stephane    80 14 nov 00:53 session-bfa61e65-a77c-4ab8-bce1-72505858a3d5
drwxr-xr-x. 1 stephane stephane    80 14 nov 05:56 session-c3f599ea-570a-4db4-ad78-8eff22004a4c
drwxr-xr-x. 1 stephane stephane    80 14 nov 03:55 session-ce875934-0cf6-4434-a91d-cbca647b11b3
drwxr-xr-x. 1 stephane stephane    80 14 nov 03:24 session-d58794d6-d201-493e-b6ab-fffee9656e15
drwxr-xr-x. 1 stephane stephane    80 15 nov 02:18 session-e0896820-1b14-4849-a926-cc56f678b88d
drwxr-xr-x. 1 stephane stephane    80  7 nov 13:18 session-e1ad947b-50b1-4758-a921-5267225bf642
drwxr-xr-x. 1 stephane stephane    80 13 nov 23:09 session-e8c327f2-a7ec-464a-8e40-0615e5befecb
drwxr-xr-x. 1 stephane stephane    80 14 nov 01:07 session-e9ee2692-96f9-42d2-886c-c5abfb51ce07
drwxr-xr-x. 1 st
… [196 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,80p' journal/2026-11-15/README.md 2>/dev/null; echo '---'; sed -n '1,100p' journal/README.md", "description": "Read journal conventions"}`

  ```
# 2026-11-15

> **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
> [`journal/2026-11-15/`](README.md). Le récit écrit à la main est conservé plus bas, dans
> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
> [l'index des sessions](../README.md#sessions).

**8 commits** · **1 session(s)** · **4 thème(s)**

## Thèmes du jour

| thème | commits | fichier |
|---|---|---|
| distribue | 2 | [distribue.md](distribue.md) |
| docs | 1 | [docs.md](docs.md) |
| mesures | 4 | [mesures.md](mesures.md) |
| portes | 1 | [portes.md](portes.md) |

## Sessions DSH

| session | titre | début | durée | liens |
|---|---|---|---|---|
| `e181ce02-cd50-488a-a6be-e84b79d40dcc` | Documentation Drave avec diagrammes et implémentation | 2026-10-31 17:40 | 347.1 h | [rapport](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md) · [digest](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md) |

## Tous les commits (heure réelle)

| heure | commit | fait |
|---|---|---|
| 01:31 | `ce7241d5` | 6A — LA BASE HONNÊTE : evaluer --reel (452 PHRASES RÉELLES : POS 88,91 %, F1 79,06 %, ATTACHEMENT 99,46 %) ET LA LIGNE BASE RÉELLE DANS LA SORTIE
… [24050 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verificateur_cic.py", "old_string": "def empreinte(preuve_hex: str, type_hex: str) -> str:\n    \"\"\"Empreinte du corpus : sha256(preuve || type), octets binaires.\"\"\"\n    return hashlib.sha256(bytes.fromhex(preuve_hex) + bytes … [6935 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verificateur_cic.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verificateur_cic.py", "old_string": "    def niveau(self, ctx: tuple, t: tuple) -> Optional[int]:\n        ty = self.infer(ctx, t)\n        if ty is None:\n            return None\n        ty = self.eval(ty)\n        return ty[1] i … [1065 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verificateur_cic.py has been updated successfully.
  ```

- **bash** `{"command": "grep -n \"def rejouer\\|def construire_environnement\\|def controle_octet_altere\\|def controle_exhaustif\\|def controle_non_trivialite\\|def mesurer\" tools/verificateur_cic.py", "description": "Locate functions after insertion"}`

  ```
975:def construire_environnement(defs_hex: dict, consts_hex: dict) -> tuple[dict, dict, dict]:
994:def rejouer(corpus: dict, defs: dict, consts: dict) -> dict:
1063:def controle_octet_altere(corpus: dict, defs: dict, consts: dict) -> dict:
1098:def controle_exhaustif_petite_preuve(corpus: dict, defs: dict, consts: dict) -> dict:
1135:def controle_non_trivialite(corpus: dict, defs: dict, consts: dict) -> dict:
1173:def mesurer(chemin: pathlib.Path, sha_attendu: Optional[str] = None,
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verificateur_cic.py", "offset": 994, "limit": 140}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verificateur_cic.py</path>
<type>file</type>
<content>
994: def rejouer(corpus: dict, defs: dict, consts: dict) -> dict:
995:     """Rejoue toutes les entrées ; rend le bilan détaillé."""
996:     noyau = Kernel(defs, consts)
997:     resultats = []
998:     for e in corpus["entrees"]:
999:         nom = e.get("nom", "?")
1000:         attendu = e.get("verdict")
1001:         if attendu not in ("accepte", "rejette"):
1002:             raise DecodeError(f"verdict inconnu pour {nom!r} : {attendu!r}")
1003:         preuve_hex, type_hex = e.get("preuve_hex"), e.get("type_hex")
1004:         if not isinstance(preuve_hex, str) or not isinstance(type_hex, str):
1005:             raise DecodeError(f"preuve/type absents pour {nom!r}")
1006:         t0 = time.perf_counter()
1007:         try:
1008:             preuve = decode_exact(preuve_hex)
1009:             typ = decode_exact(type_hex)
1010:             decode_ok = True
1011:         except DecodeError as exc:
1012:             preuve = typ = None
1013:             decode_ok = False
1014:             detail_decode = str(exc)
1015:         obtenu = noyau.verify(preuve, typ) if de
… [5316 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verificateur_cic.py", "old_string": "        t0 = time.perf_counter()\n        try:\n            preuve = decode_exact(preuve_hex)\n            typ = decode_exact(type_hex)\n            decode_ok = True\n        except DecodeError  … [5638 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verificateur_cic.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verificateur_cic.py", "old_string": "    noyau = Kernel(defs, consts)\n    mutations = acceptes = empreintes_changees = 0\n    details = []\n    for e in corpus[\"entrees\"]:\n        if e.get(\"verdict\") != \"accepte\":\n         … [4385 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verificateur_cic.py has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verificateur_cic.py", "offset": 1180, "limit": 130}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verificateur_cic.py</path>
<type>file</type>
<content>
1180:                     and empreintes_pures_changees == mutations else "fail"),
1181:     }
1182: 
1183: 
1184: def controle_exhaustif_petite_preuve(corpus: dict, defs: dict, consts: dict) -> dict:
1185:     """Énumère TOUTES les mutations d'un octet de la plus petite preuve acceptée."""
1186:     noyau = Kernel(defs, consts)
1187:     candidates = [e for e in corpus["entrees"] if e.get("verdict") == "accepte"]
1188:     if not candidates:
1189:         return {"verdict": "fail", "raison": "aucune preuve acceptée"}
1190:     e = min(candidates, key=lambda x: len(x["preuve_hex"]))
1191:     original = bytes.fromhex(e["preuve_hex"])
1192:     typ = decode_exact(e["type_hex"])
1193:     total = acceptes = 0
1194:     exemples = []
1195:     for i in range(len(original)):
1196:         for v in range(256):
1197:             if v == original[i]:
1198:                 continue
1199:             total += 1
1200:             b = bytearray(original)
1201:             b[i] = v
1202:             try:
1203:                 r = noyau.verify(decode_exact(b.hex()), typ)
1204:     
… [4810 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verificateur_cic.py", "old_string": "# ---------------------------------------------------------------------------\n# CLI et mesure\n# ---------------------------------------------------------------------------\n\ndef _tags_present … [3856 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verificateur_cic.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verificateur_cic.py", "old_string": "            \"sha256_haslib\": sha_hl,", "new_string": "            \"sha256_hashlib\": sha_hl,"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verificateur_cic.py has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verificateur_cic.py", "offset": 1329, "limit": 160}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verificateur_cic.py</path>
<type>file</type>
<content>
1329: 
1330: def _tags_presents(t: tuple, acc: set[str]) -> None:
1331:     acc.add(t[0])
1332:     for x in t[1:]:
1333:         if isinstance(x, tuple):
1334:             _tags_presents(x, acc)
1335: 
1336: 
1337: def _chemin_affiche(chemin: pathlib.Path) -> str:
1338:     try:
1339:         return str(chemin.resolve().relative_to(RACINE))
1340:     except ValueError:
1341:         return str(chemin)
1342: 
1343: 
1344: def mesurer(chemin: pathlib.Path, sha_attendu: Optional[str] = None,
1345:             controles: bool = True) -> dict:
1346:     t0 = time.perf_counter()
1347:     defs_hex, consts_hex, brut, sha = charger_corpus(chemin)
1348:     artefact = json.loads(brut)
1349:     defs, consts, bilan_serial = construire_environnement(defs_hex, consts_hex)
1350:     entrees = artefact["entrees"]
1351:     exercees: set[str] = set()
1352:     decodage_entrees_ok = True
1353:     for t in list(defs.values()) + list(consts.values()):
1354:         _tags_presents(t, exercees)
1355:     for e in entrees:
1356:         for cle in ("preuve_hex", "type_hex"):
1357:       
… [7197 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verificateur_cic.py", "old_string": "    rejeu = rejouer({\"entrees\": entrees}, defs, consts)\n    controles_negatifs = {}\n    if controles:\n        controles_negatifs = {\n            \"octet_altere\": controle_octet_altere({\" … [8827 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verificateur_cic.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verificateur_cic.py", "old_string": "        f\"Verdicts : {r['accord']}/{r['verdicts']} d’accord \"\n        f\"({r['attendus_acceptes']} acceptés, {r['attendus_rejetes']} rejetés) \"\n        f\"— désaccords {r['desaccord']}\",\n … [3078 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verificateur_cic.py has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verificateur_cic.py", "old_string": "2. **Sérialisation canonique** : chaque terme (défs, constantes, preuves, types)\n   se décode puis se ré-encode exactement sur les mêmes octets.\n3. **Empreinte** : `sha256(octets(preuve) || oc … [1890 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verificateur_cic.py has been updated successfully.
  ```

- **bash** `{"command": "python3 -m py_compile tools/verificateur_cic.py && python3 tools/verificateur_cic.py --sans-controles", "description": "Compile and run verifier without controls"}`

  ```
Corpus : tools/tests/cic/corpus_dor_cic_v1.json
sha256 : 3018f6f4349641534be3a73309a1b25ff4bc71a3975e7105f2c15b61da18aaec (attendu)
Environnement : 3 defs, 21 consts, sérialisation canonique ✅
Verdicts : 42/42 d’accord (36 acceptés, 6 rejetés) — désaccords 0
Empreintes : 42/42 valides (hashlib) · 42/42 par la seconde implémentation
Type de Bruijn : 42/42 types clos et bien formés (42/42 preuves closes)
sha256 indépendant : pass (corpus ok, 42/42 couples, 24/24 termes)
Contrôles négatifs :
  désactivés
Durée : 0.715 s — VERDICT PASS
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys\nsys.path.insert(0,'tools')\nimport verificateur_cic as vc\nprint(vc.autotest_sha256_pur())\nprint(vc.sha256_pur(b'abc'))\nPY", "description": "Test pure SHA-256 self-test"}`

  ```
{'implementation': 'FIPS 180-4 réécrite dans ce module, sans hashlib', 'vecteurs': 16, 'ecarts': [], 'verdict': 'pass'}
ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad
  ```

- **bash** `{"command": "time python3 tools/verificateur_cic.py", "description": "Run verifier with all controls", "timeoutMs": 120000}`

  ```
Corpus : tools/tests/cic/corpus_dor_cic_v1.json
sha256 : 3018f6f4349641534be3a73309a1b25ff4bc71a3975e7105f2c15b61da18aaec (attendu)
Environnement : 3 defs, 21 consts, sérialisation canonique ✅
Verdicts : 42/42 d’accord (36 acceptés, 6 rejetés) — désaccords 0
Empreintes : 42/42 valides (hashlib) · 42/42 par la seconde implémentation
Type de Bruijn : 42/42 types clos et bien formés (42/42 preuves closes)
sha256 indépendant : pass (corpus ok, 42/42 couples, 24/24 termes)
Contrôles négatifs :
  octet altéré (36 preuves acceptées) : 36/36 rejetés, 0 accepté(s) — pass
  type altéré (42 entrées) : 42/42 rejetés, 36 type(s) invalide(s) — pass
  exhaustif eq(2,2) : 1020/1020 rejetés, 0 accepté(s) — pass
  non-trivialité : accepte-tout 36/42, rejette-tout 6/42
Durée : 1.058 s — VERDICT PASS
[stderr]

real	0m1,148s
user	0m1,119s
sys	0m0,029s
  ```

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_verificateur_cic_v2.py", "content": "#!/usr/bin/env python3\n\"\"\"test_verificateur_cic_v2.py — le banc des ajouts B3 au corpus d'or CIC.\n\nCe que ce fichier fige, en plus des 21 tests de J12.2 :\n- la seconde implémen … [8171 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/test_verificateur_cic_v2.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "python3 tools/tests/test_verificateur_cic_v2.py", "description": "Run new B3 tests", "timeoutMs": 120000}`

  ```
[stderr]
test_cli_json (__main__.TestMesureEtCLI.test_cli_json) ... ok
test_corpus_avec_type_corrompu_refuse (__main__.TestMesureEtCLI.test_corpus_avec_type_corrompu_refuse) ... ok
test_verdict_global_et_integrite (__main__.TestMesureEtCLI.test_verdict_global_et_integrite) ... ok
test_36_preuves_alterees_rejetees (__main__.TestPreuvesEtTypesAlteres.test_36_preuves_alterees_rejetees) ... ok
test_42_types_alteres_rejetes (__main__.TestPreuvesEtTypesAlteres.test_42_types_alteres_rejetes) ... ok
test_exhaustif_eq_2_2 (__main__.TestPreuvesEtTypesAlteres.test_exhaustif_eq_2_2) ... ok
test_24_termes_de_environnement (__main__.TestSha256SecondeImplementation.test_24_termes_de_environnement) ... ok
test_42_empreintes_par_la_seconde_implementation (__main__.TestSha256SecondeImplementation.test_42_empreintes_par_la_seconde_implementation) ... ok
test_sha256_du_corpus (__main__.TestSha256SecondeImplementation.test_sha256_du_corpus) ... ok
test_un_octet_change_empreinte (__main__.TestSha256SecondeImplementation.test_un_octet_change_empreinte) ... ok
test_vecteurs_connus (__main__.TestSha256SecondeImplementation.test_vecteurs_connus) ... ok
test_vecteurs_fips_et_rembourrage (__main__.TestSha256S
… [606 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/tests/test_verificateur_cic.py", "description": "Run existing J12.2 tests", "timeoutMs": 120000}`

  ```
[stderr]
test_mutation_directe (__main__.TestControlesNegatifs.test_mutation_directe) ... ok
test_non_trivialite (__main__.TestControlesNegatifs.test_non_trivialite) ... ok
test_octet_altere_exhaustif (__main__.TestControlesNegatifs.test_octet_altere_exhaustif) ... ok
test_octet_altere_sur_les_36_preuves (__main__.TestControlesNegatifs.test_octet_altere_sur_les_36_preuves) ... ok
test_empreintes (__main__.TestCorpusPortable.test_empreintes) ... ok
test_manifeste_et_copie (__main__.TestCorpusPortable.test_manifeste_et_copie) ... ok
test_serialisation_canonique (__main__.TestCorpusPortable.test_serialisation_canonique) ... ok
test_structure (__main__.TestCorpusPortable.test_structure) ... ok
test_42_sur_42 (__main__.TestRejeu.test_42_sur_42) ... ok
test_integrite (__main__.TestRejeu.test_integrite) ... ok
test_les_arithmetiques_sont_acceptees (__main__.TestRejeu.test_les_arithmetiques_sont_acceptees) ... ok
test_les_six_rejets_sont_rejetes (__main__.TestRejeu.test_les_six_rejets_sont_rejetes) ... ok
test_verdict_global (__main__.TestRejeu.test_verdict_global) ... ok
test_cli_corpus_corrompu_code_1 (__main__.TestRobustesse.test_cli_corpus_corrompu_code_1) ... ok
test_cli_json (__main_
… [687 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-cic.sh"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-cic.sh</path>
<type>file</type>
<content>
1: #!/bin/bash
2: # porte-cic.sh — le corpus d'or CIC est rejoué par un vérificateur INDÉPENDANT.
3: #
4: # POURQUOI CETTE PORTE EXISTE. Un corpus « d'or » ne vaut que si une seconde
5: # implémentation le rejoue sans importer la première. Cette porte exige :
6: #   1. 42/42 verdicts (36 acceptés, 6 rejetés) avec le noyau de Drave ;
7: #   2. 42/42 empreintes sha256(preuve || type) et 42/42 sérialisations canoniques ;
8: #   3. l'artefact portable byte-identique à la source Panini (sha256 du fichier) ;
9: #   4. le contrôle négatif : altérer un octet d'une preuve acceptée la rejette
10: #      (36/36), et les 1 020 mutations de eq(2,2) sont toutes rejetées ;
11: #   5. la non-trivialité : « accepte tout » et « rejette tout » échouent ;
12: #   6. un corpus localement corrompu est REFUSÉ (code 1), pas absorbé.
13: #
14: # Usage : tools/porte-cic.sh
15: set -u
16: cd "$(dirname "$0")/.."
17: 
18: echo "=== PORTE CIC — LE CORPUS D'OR REJOUÉ ==="
19: T=$(mktemp -d)
20: trap 'rm -rf "$T"' EXIT
21: 
22: if ! python3 tools/verificateur_cic.py --json > "$T/mesure.json"; then
23:     
… [2907 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-cic.sh", "old_string": "#   1. 42/42 verdicts (36 acceptés, 6 rejetés) avec le noyau de Drave ;\n#   2. 42/42 empreintes sha256(preuve || type) et 42/42 sérialisations canoniques ;\n#   3. l'artefact portable byte-identique à … [1242 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-cic.sh has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-cic.sh", "old_string": "r = m[\"resultat\"]\ni = m[\"integrite\"]\na = m[\"controles_negatifs\"][\"octet_altere\"]\ne = m[\"controles_negatifs\"][\"octet_altere_exhaustif\"]\nn = m[\"controles_negatifs\"][\"non_trivialite\"]\ … [3557 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-cic.sh has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-cic.sh", "old_string": "if python3 tools/verificateur_cic.py --corpus \"$T/corpus-corrompu.json\" \\\n        --sha256 \"\" --sans-controles > \"$T/corrompu.log\" 2>&1; then\n    echo \"  ❌ un corpus corrompu a été ACCEPTÉ —  … [2505 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-cic.sh has been updated successfully.
  ```

- **bash** `{"command": "bash tools/porte-cic.sh", "description": "Run CIC gate with new checks", "timeoutMs": 180000}`

  ```
=== PORTE CIC — LE CORPUS D'OR REJOUÉ ===
  42/42 verdicts · 42/42 empreintes · 42/42 sérialisations
  de Bruijn : 42/42 types bien formés · 42/42 preuves closes · niveaux [0, 1]
  sha256 2e implémentation : corpus ok · 42/42 couples · 24/24 termes · 16 vecteurs
  octet altéré : 36/36 rejetés · type altéré : 42/42 rejetés · exhaustif eq(2,2) : 1020/1020 rejetés
  non-trivialité : accepte-tout 6 désaccords, rejette-tout 36 désaccords
  corpus corrompu (preuve) : refusé (code 1)
  corpus corrompu (type) : refusé (code 1)
  tests : 21 (J12.2) + 17 (B3) = 38 cas
✅ porte CIC verte : 42/42 verdicts, empreintes, de Bruijn, sha256 2e implémentation,
   preuves et types altérés rejetés, corpus corrompu refusé
  ```

- **bash** `{"command": "python3 tools/verificateur_cic.py --json > /tmp/cic-v2.json && python3 - <<'PY'\nimport json\nm=json.load(open('/tmp/cic-v2.json'))\nprint(json.dumps({k:m[k] for k in ('tache','titre','date','verdict','duree_s','type_de_bruijn','integrite')},indent=1,ensure_ascii=False))\nprint('--- sha … [384 caractères tronqués]`

  ```
{
 "tache": "B3",
 "titre": "Corpus d'or CIC v2 : type de Bruijn vérifié + sha256 rejoué par une seconde implémentation",
 "date": "2026-11-15",
 "verdict": "pass",
 "duree_s": 1.041,
 "type_de_bruijn": {
  "definition": "un type valide est clos (aucun indice hors portée) et [] ⊢ type : sort n ; la preuve est close elle aussi",
  "types_totaux": 42,
  "types_clos": 42,
  "types_bien_formes": 42,
  "preuves_closes": 42,
  "niveaux_observes": [
   0,
   1
  ],
  "verdict": "pass"
 },
 "integrite": {
  "sha256_corpus": true,
  "serialisation_environnement": true,
  "serialisation_entrees": true,
  "decodage_entrees": true,
  "empreintes": true,
  "empreintes_pures": true,
  "type_de_bruijn": true,
  "preuves_closes": true,
  "sha256_seconde_implementation": true,
  "verdicts": true
 }
}
--- sha
{
 "implementation": "SHA-256 FIPS 180-4 réécrite dans verificateur_cic.py (sans hashlib)",
 "autotest": {
  "implementation": "FIPS 180-4 réécrite dans ce module, sans hashlib",
  "vecteurs": 16,
  "ecarts": [],
  "verdict": "pass"
 },
 "corpus": {
  "sha256_hashlib": "3018f6f4349641534be3a73309a1b25ff4bc71a3975e7105f2c15b61da18aaec",
  "sha256_pur": "3018f6f4349641534be3a73309a1b25ff4bc71a397
… [1827 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json,collections\nm=json.load(open('/tmp/cic-v2.json'))\nc=collections.Counter(e['niveau_type'] for e in m['resultat']['entrees'])\nprint('niveaux',c)\nprint('accepted by level',collections.Counter((e['attendu'],e['niveau_type']) for e in m['resultat']['entrees' … [413 caractères tronqués]`

  ```
niveaux Counter({0: 38, 1: 4})
accepted by level Counter({('accepte', 0): 32, ('rejette', 0): 6, ('accepte', 1): 4})
type bytes total 953
proof bytes total 17443
max proof (6705, 'mul_comm')
max type (48, 'add_assoc')
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys,json\nsys.path.insert(0,'tools')\nimport verificateur_cic as vc\nd=json.load(open('tools/tests/cic/corpus_dor_cic_v1.json'))\nacc=set()\nfor e in d['entrees']:\n    vc._tags_presents(vc.decode_exact(e['type_hex']),acc)\nprint(sorted(acc),len(acc))\nacc2=set( … [183 caractères tronqués]`

  ```
['app', 'const', 'def', 'empty', 'id', 'nat', 'pi', 'sigma', 'sort', 'suc', 'var', 'zero'] 12
['app', 'const', 'def', 'empty', 'id', 'j', 'lam', 'nat', 'natind', 'natrec', 'pair', 'pi', 'refl', 'sort', 'suc', 'tt', 'unit', 'var', 'zero'] 19
  ```

- **bash** `{"command": "git rev-parse HEAD; sha256sum tools/verificateur_cic.py tools/tests/test_verificateur_cic.py tools/tests/test_verificateur_cic_v2.py tools/porte-cic.sh tools/tests/cic/corpus_dor_cic_v1.json tools/tests/cic/manifeste.json", "description": "Get HEAD and source hashes"}`

  ```
01b6db6ebd4e5bb6532800c8d3bd8a54b0ac9839
0666551fdbaa677b7ed45879b72030c27f9aeb27ae57cd2a17bcc089c4efa338  tools/verificateur_cic.py
2c41e2181f7b05bce9d26b035e0b045c111331feb0a0c6796dded6fddd2c150f  tools/tests/test_verificateur_cic.py
81f532016f326c19da025b83260e1fdbaf1c9b6af458c763d04446fd81f0ca44  tools/tests/test_verificateur_cic_v2.py
60ef074ddee93db2838b505273cbb3b390eb351de36ba66e9f7b9114f11278a8  tools/porte-cic.sh
3018f6f4349641534be3a73309a1b25ff4bc71a3975e7105f2c15b61da18aaec  tools/tests/cic/corpus_dor_cic_v1.json
7ab08e17a380ff79b1fbff2d921e0bbfdf935d32c6d466be2482befbf0bf9e53  tools/tests/cic/manifeste.json
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\np=json.load(open('tools/chantier/plan.json'))\n# find list containing B3\ndef find(o):\n    if isinstance(o,dict):\n        if o.get('id')=='B3': return o\n        for v in o.values():\n            r=find(v)\n            if r: return r\n    elif isinstance … [570 caractères tronqués]`

  ```
{'id': 'B3', 'jour': 15, 'titre': "Panini — le corpus d'or CIC étendu", 'mandat': "Tâche B3 : le corpus d'or CIC (42 verdicts, 42/42 reproduits en J12.2) — étends le vérificateur : les 36 preuves altérées sont rejetées ; ajoute la vérification du **type de Bruijn** et le sha256 indépendant rejoué par une seconde implémentation ; fiche `reports/rapport-cic-v2.md` + JSON.", 'budget_min': 90, 'acceptation': [{'commande': 'test -f reports/rapport-cic-v2.md && echo FICHE-OK', 'attendu': 'FICHE-OK'}]}
[('J0', 0, 'Le contrôle du superviseur'), ('J1.1', 1, 'r035 : la relative zéro'), ('J1.2', 1, 'La convention des GV'), ('J1.3', 1, 'Le schéma v2'), ('J1.4', 1, 'La restitution v0'), ('J2.1', 2, 'Panini I — la table atomes ↔ niveaux'), ('J2.2', 2, 'Panini I — le corpus commun'), ('J3.1', 3, 'Panini II — le retrieval à époque contrôlée'), ('J3.2', 3, 'Panini II — la généalogie à deux faces'), ('J4.1', 4, 'Coordination N2 — le mètre RoPE'), ('J4.2', 4, 'Coordination S — les 11 verdicts'), ('J4.3', 4, 'Coordination R — le tagger sur 612'), ('J4.4', 4, 'Coordination A — A6.2 et A8.3b2'), ('J5.1', 5, 'Le rapport de semaine'), ('J5.2', 5, 'La passe complète et le tag'), ('J6.1', 6, 'Le dernier spa
… [950 caractères tronqués]
  ```

- **write** `{"content": "# B3 — Corpus d'or CIC v2 : le type de Bruijn vérifié, le sha256 rejoué deux fois\n\n> **Ligne de roadmap** : **L / R0.7** (le bloc langue) — chantier **Panini** · **Tâche** : **B3** ·\n> **Date** : **2026-11-15** ·\n> **Verdict** : ✅ **le corpus d'or CIC reste 42/42, et le vérificateur … [15381 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-cic-v2.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport hashlib, json, pathlib, subprocess, sys\nRACINE = pathlib.Path('.').resolve()\nsys.path.insert(0, str(RACINE / 'tools'))\nimport verificateur_cic as vc\n\ncorpus = RACINE / 'tools/tests/cic/corpus_dor_cic_v1.json'\nm = vc.mesurer(corpus, vc.SHA256_CORPUS, contro … [2667 caractères tronqués]`

  ```
ecrit /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/cic-verificateur-v2.json 23362 octets
verdict pass tests {'commande': 'python3 tools/tests/test_verificateur_cic.py ; python3 tools/tests/test_verificateur_cic_v2.py', 'cas_j122': None, 'cas_b3': None, 'cas_total': 0, 'echecs': 0} porte 0
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json, pathlib, subprocess, sys\np = pathlib.Path('reports/cic-verificateur-v2.json')\nm = json.loads(p.read_text(encoding='utf-8'))\ndef ran(cmd):\n    q = subprocess.run(cmd, capture_output=True, text=True)\n    for line in (q.stdout + '\\n' + q.stderr).splitli … [735 caractères tronqués]`

  ```
{'commande': 'python3 tools/tests/test_verificateur_cic.py ; python3 tools/tests/test_verificateur_cic_v2.py', 'cas_j122': 21, 'cas_b3': 17, 'cas_total': 38, 'echecs': 0}
json tests ok True
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nm=json.load(open('reports/cic-verificateur-v2.json'))\nprint(json.dumps({k:m[k] for k in ('tache','titre','date','commande','commit_mesure','verdict','duree_s','tests','porte')},indent=1,ensure_ascii=False))\nprint('sources',json.dumps(m['sources_code'],in … [97 caractères tronqués]`

  ```
{
 "tache": "B3",
 "titre": "Corpus d'or CIC v2 : type de Bruijn vérifié + sha256 rejoué par une seconde implémentation",
 "date": "2026-11-15",
 "commande": "python3 tools/verificateur_cic.py --json",
 "commit_mesure": "01b6db6ebd4e5bb6532800c8d3bd8a54b0ac9839",
 "verdict": "pass",
 "duree_s": 1.044,
 "tests": {
  "commande": "python3 tools/tests/test_verificateur_cic.py ; python3 tools/tests/test_verificateur_cic_v2.py",
  "cas_j122": 21,
  "cas_b3": 17,
  "cas_total": 38,
  "echecs": 0
 },
 "porte": {
  "commande": "bash tools/porte-cic.sh",
  "code_sortie": 0,
  "verdict": "verte",
  "sortie": [
   "=== PORTE CIC — LE CORPUS D'OR REJOUÉ ===",
   "  42/42 verdicts · 42/42 empreintes · 42/42 sérialisations",
   "  de Bruijn : 42/42 types bien formés · 42/42 preuves closes · niveaux [0, 1]",
   "  sha256 2e implémentation : corpus ok · 42/42 couples · 24/24 termes · 16 vecteurs",
   "  octet altéré : 36/36 rejetés · type altéré : 42/42 rejetés · exhaustif eq(2,2) : 1020/1020 rejetés",
   "  non-trivialité : accepte-tout 6 désaccords, rejette-tout 36 désaccords",
   "  corpus corrompu (preuve) : refusé (code 1)",
   "  corpus corrompu (type) : refusé (code 1)",
   "  tests : 21 (J1
… [1215 caractères tronqués]
  ```

- **bash** `{"command": "git status --short | head -40", "description": "Check working tree"}`

  ```
M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/plan.json
 M tools/porte-cic.sh
 M tools/verificateur_cic.py
?? reports/cic-verificateur-v2.json
?? reports/rapport-cic-v2.md
?? reports/rapport-gold-reel-50.json
?? reports/rapport-gold-reel-50.md
?? reports/rapport-s-paragraphes.md
?? tools/tests/linguistique/gold_reel_50.py
?? tools/tests/test_verificateur_cic_v2.py
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/cic/README.md", "old_string": "Le fichier `manifeste.json` porte les empreintes de la source, du TSV et de la copie.\nLa copie existe pour que le vérificateur Drave soit **portable** : il n'a pas besoin\ndu dépôt Panini pour  … [1561 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/cic/README.md has been updated successfully.
  ```

- **bash** `{"command": "ls reports/*.md | wc -l; ls reports/*.json | wc -l; find docs -name '*.md' -not -path '*/archive/*' -not -name 'README.md' | wc -l; git log -1 --format=%ad --date=short", "description": "Count report and doc files"}`

  ```
741
835
458
2026-11-15
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "**Mis à jour : 2026-11-15, 03 h 46 HNE (B2 : atomes → niveaux, négatif contrôlé)**", "new_string": "**Mis à jour : 2026-11-15, 04 h 10 HNE (B3 : corpus d'or CIC v2, type de Bruijn + sha256 par d … [24 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md": file has not been read — read the file, then retry
  ```

- **bash** `{"command": "wc -l docs/pilotage/en-cours.md", "description": "Count en-cours lines"}`

  ```
148 docs/pilotage/en-cours.md
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 10}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
1: # En ce moment
2: 
3: **Mis à jour : 2026-11-15, 03 h 46 HNE (B2 : atomes → niveaux, négatif contrôlé)**
4: 
5: > **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
6: > plan plus bas (**La carte**).
7: 
8: ### Session `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — le hub de reprise du 04/11 *(en pause)*
9: 
10: - **Id** : `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — [`plan.md`](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/plan.md).

(Showing lines 1-10 of 148. Use offset=11 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "**Mis à jour : 2026-11-15, 03 h 46 HNE (B2 : atomes → niveaux, négatif contrôlé)**", "new_string": "**Mis à jour : 2026-11-15, 04 h 10 HNE (B3 : corpus d'or CIC v2, type de Bruijn + sha256 par d … [24 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "offset": 92, "limit": 18}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
92: - **Panini J2.1–J3.2 + B2** : **14 atomes** ; UDHR **418/438** ; J3.2 : **5/21** langues (Glottolog **21/21**), **154/154** paires hors script au hasard, **V14 3/21** ; **B2 : atomes → niveaux négatif** (POS −0,092, syntagmes −0,160, attachement −0,092 ; style absorbé par la date) ; [atomes](../../reports/rapport-atomes-niveaux.md), [corpus](../../reports/rapport-corpus-commun.md), [époque](../../reports/rapport-retrieval-epoque.md), [deux faces](../../reports/rapport-genealogie-deux-faces.md), [B2](../../reports/rapport-atomes-prediction.md).
93: - **Panini J7.1** : 532 textes (445 langues) ; hors script, hasard ; famille **66,1 %** / sœur **26,1 %** (hasard 10,3/2,5) ; LANG_TREE : sœurs **0,619** vs **0,0445** (13,9×, p=0,002) ; [fiche](../../reports/rapport-retrieval-familles.md).
94: - **Panini B1 — protocole à date contrôlée** : **60 paires** (20 G1 inter-traditions à ±10 ans,
95:   20 G2 même tradition à 20–200 ans, 20 G3 même langue à dates décalées), **59 textes**, **26 à signer** ;
96:   le §334 ne fournit qu'**une** paire G1 déjà signée ; [fiche](../../re
… [1418 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "- **Panini J12.1–J12.2** : §334 **495 paires uniques** ; CIC **42/42** verdicts, **42/42** empreintes, **36/36** preuves altérées rejetées, **1 020/1 020** mutations `eq(2,2)` rejetées ; [§334]( … [847 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "offset": 106, "limit": 12}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
106: 
107: | invariant | valeur | contrôle |
108: |---|---|---|
109: | portes | **85** (dont `porte-cic` le 14/11) | `tools/porte-*.sh` |
110: | chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |
111: | fichiers / JSON de résultats | **740** / **834** | `reports/*.md` / `reports/*.json` |
112: | documents de `docs/` | **123** (hors archive et README) | `docs/**/*.md` |
113: | dernière passe | **14/11 00 h 30** (84, **81/3**) ; rouges tolérées `indice`, `melange` ; `sessions` **revérifiée verte** le 14/11 06 h 55 | `docs/pilotage/references-non-regression.md` |
114: 
115: ## Les chantiers et leurs bloquants
116: 
117: **Dépendances** : [le graphe](backlog/dependances.md) ; cette table ne garde que les **bloquants

(Showing lines 106-117 of 149. Use offset=118 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "| fichiers / JSON de résultats | **740** / **834** | `reports/*.md` / `reports/*.json` |", "new_string": "| fichiers / JSON de résultats | **741** / **835** | `reports/*.md` / `reports/*.json` | … [2 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "offset": 117, "limit": 14}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md</path>
<type>file</type>
<content>
117: **J12.2 — le corpus d'or CIC rejoué hors de Panini.** Le corpus portable de Panini
118: (**3** defs, **21** consts, **42** entrées : **36** `accepte`, **6** `rejette`) est rejoué par un
119: noyau **CIC-lite réécrit côté Drave**, sans importer le vérificateur de Panini : **42/42** verdicts,
120: **42/42** empreintes `sha256(preuve || type)`, **42/42** sérialisations canoniques. Le contrôle
121: négatif est net : altérer le dernier octet des **36** preuves acceptées les fait **36/36** rejeter,
122: et les **1 020** mutations d'un octet de `eq(2,2)` sont **1 020/1 020** rejetées ; un noyau
123: « accepte tout » et un noyau « rejette tout » échouent (respectivement **6** et **36** désaccords).
124: La copie `tools/tests/cic/corpus_dor_cic_v1.json` est **byte-identique** à la source
125: (`3018f6f4…aaec`) ; la porte `tools/porte-cic.sh` et **21** tests rejouent le tout. C'est un
126: **verrou de portabilité** : « nos deux systèmes vérifient les mêmes preuves », pas une preuve de
127: correction du noyau Panini (le corpus n'exerce que **20** des **39** étiquettes du for
… [270 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "old_string": "[`fiche`](../../reports/rapport-cic-verificateur.md) + [`JSON`](../../reports/cic-verificateur.json).\n\n**B2 — atomes et niveaux : négatif.**", "new_string": "[`fiche`](../../reports/rapport-cic … [997 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-15/README.md", "offset": 35, "limit": 30}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-15/README.md</path>
<type>file</type>
<content>
35: | 03:04 | `c37fed06` | B1 — LE PROTOCOLE À DATE CONTRÔLÉE GELÉ : 60 PAIRES (20/20/20), 59 TEXTES, 26 À SIGNER ; LE §334 N'EN FOURNIT QU'UNE DÉJÀ SIGNÉE |
36: | 03:48 | `011b8b8e` | B2 — LES ATOMES NE PRÉDISENT PAS POS, SYNTAGMES NI ATTACHEMENT : SUR 28 ŒUVRES PROPRES, R² −0,092 / −0,160 / −0,092 (p 0,56 / 0,85 / 0,67) ; LE STYLE EST PRÉDIT (GRAPHÈMES +0,811, MOTS +0,657, NÉGATION +0,440, VERBES +0,429) MAIS ABSORBÉ PAR LA DATE (p_resid 0,76–1,0) |
37: 
38: ## Le récit de la journée (écrit à la main)
39: 
40: <!-- notes -->
41: ### B2 — les atomes ne prédisent pas les niveaux
42: 
43: La table J2.1 promettait un **porteur** pour chacun des 14 atomes ; B2 devait la mesurer. Le résultat est
44: un **négatif contrôlé**. Sur les **44 signatures** de Panini, **36 œuvres** ont assez de prose pour être
45: mesurées, **28** ont une fenêtre de signature propre et ≥ 1 000 jetons. Sur ces 28, les 14 atomes ne
46: prédisent pas **POS** (R²_CV **−0,092**, p=0,56), les **syntagmes** (**−0,160**, p=0,85) ni
47: l'**attachement** (**−0,092**, p=0,67). Le seul ρ nominal (POS **+0
… [1163 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-15/README.md", "old_string": "[`reports/atomes-prediction.json`](../../reports/atomes-prediction.json). La suite : un gold anglais de\nniveaux et une signature recalculée sur le texte nettoyé.\n<!-- /notes -->", "new_stri … [1390 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-15/README.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py", "description": "Run documentation review", "timeoutMs": 180000}`

  ```
revue de documentation · 741 fiche(s) · 835 JSON · 123 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ```

- **bash** `{"command": "bash tools/porte-tableaux.sh", "description": "Run table and link gate", "timeoutMs": 180000}`

  ```
❌ 1 tableau(x) ne rendront pas (mistune refuse le tableau ENTIER) :
     reports/rapport-cic-v2.md:174 — 4 cellules ≠ 2 attendues
[stderr]
  1813 fichier(s) examiné(s)
[exit code: 1]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-cic-v2.md", "offset": 168, "limit": 15}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-cic-v2.md</path>
<type>file</type>
<content>
168: | mesure | valeur |
169: |---|---:|
170: | vecteurs de l'auto-test | **16** |
171: | écart sur les vecteurs | **0** |
172: | sha256 du corpus (`hashlib`) | `3018f6f4…aaec` |
173: | sha256 du corpus (seconde implémentation) | `3018f6f4…aaec` |
174: | couples `preuve || type` concordants | **42 / 42** |
175: | empreintes déclarées retrouvées | **42 / 42** |
176: | preuves seules concordantes | **42 / 42** |
177: | types seuls concordants | **42 / 42** |
178: | termes de l'environnement concordants | **24 / 24** |
179: | écarts | **0** |
180: 
181: La seconde implémentation n'est pas une seconde **exécution** de `hashlib` : elle ne partage ni ses
182: tables, ni son code, ni son interface. Elle est écrite depuis la norme, avec les mêmes constantes

(Showing lines 168-182 of 267. Use offset=183 to continue.)
</content>
  ```

- **bash** `{"command": "grep -n \"preuve || type\\|preuve ||\\| || \" reports/rapport-cic-v2.md", "description": "Find double-pipe usages in report"}`

  ```
9:> couples `preuve || type` et les **24** termes de l'environnement : **0 écart**. Les contrôles
88:- les **42** couples `preuve || type` — c'est l'empreinte déclarée par le corpus ;
174:| couples `preuve || type` concordants | **42 / 42** |
237:   chemin `hashlib` et la formule `sha256(preuve || type)` sur ces 42 entrées. Elle ne prouve ni la
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-cic-v2.md", "old_string": "| couples `preuve || type` concordants | **42 / 42** |", "new_string": "| couples `preuve ‖ type` concordants | **42 / 42** |"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-cic-v2.md has been updated successfully.
  ```

- **bash** `{"command": "bash tools/porte-tableaux.sh", "description": "Re-run table and link gate", "timeoutMs": 180000}`

  ```
✅ 1813 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4358 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-15)
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport hashlib,json,pathlib\np=pathlib.Path('reports/cic-verificateur-v2.json')\nm=json.loads(p.read_text(encoding='utf-8'))\nm['sources_code']['reports/rapport-cic-v2.md']=hashlib.sha256(pathlib.Path('reports/rapport-cic-v2.md').read_bytes()).hexdigest()\np.write_text … [173 caractères tronqués]`

  ```
1bf1227a37716dc9e14a85a5e9aa2d919a86e5072acd2c8b67e348c1251230bb
  ```

- **bash** `{"command": "python3 tools/verifie_en_cours.py", "description": "Validate en-cours state", "timeoutMs": 120000}`

  ```
en-cours · 1698 mots · 7 sections · 4 session(s) · 11 puces · 5 questions
  ❌ 1 anomalie(s) :
     · 11 puces dans « Ce qui est en cours » > 10
[exit code: 1]
  ```

- **bash** `{"command": "python3 tools/verifie_journal.py", "description": "Validate journal structure", "timeoutMs": 120000}`

  ```
journal · 47 jour(s) · 199 session(s) · 2565 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
  ```

- **bash** `{"command": "python3 tools/taille_documents.py", "description": "Check document size budget", "timeoutMs": 120000}`

  ```
budget de contexte · documents chargeables
    mots lignes  cat budget  document
    9133    500   T1   9000  docs/pilotage/roadmap.md
    5999    597 DATÉ      0  docs/implantation/contexte-long.md
    4858    515   T1   5000  docs/theorie/glossaire/10-le-pont-linguistico-semantique-le-vocabu.md
    4085    431 DATÉ      0  docs/implantation/numa-segregation.md
    3310    317   T1   3500  README.md
    3072    341 DATÉ      0  docs/implantation/convertisseur.md
    2962    364   T1   5000  docs/theorie/glossaire/02-modeles-et-architectures.md
    2896    352 DATÉ      0  docs/implantation/configuration-nvme-raid-amd.md
    2496    171   T1   2500  docs/pilotage/references-non-regression.md
    2371    216   T1   2800  reports/README.md
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/form
… [597 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "offset": 96, "limit": 10}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
96:   le §334 ne fournit qu'**une** paire G1 déjà signée ; [fiche](../../reports/rapport-protocole-date.md),
97:   [JSON](../../reports/protocole-date.json).
98: - **Panini J12.1–J12.2** : §334 **495 paires uniques** ; CIC **42/42** verdicts, **42/42** empreintes, **36/36** preuves altérées rejetées, **1 020/1 020** mutations `eq(2,2)` rejetées ; [§334](../../reports/rapport-panini-334.md), [CIC](../../reports/rapport-cic-verificateur.md).
99: - **Panini B3 — CIC v2** : **42/42** verdicts ; **42/42** types de Bruijn clos et bien formés (`[] ⊢ type : sort n`), **42/42** preuves closes ; **42/42** empreintes rejouées par **deux** implémentations (hashlib + FIPS 180-4 sans hashlib) et **24/24** termes ; **36/36** preuves altérées et **42/42** types altérés rejetés ; corpus corrompu (preuve ou type) refusé ; [fiche](../../reports/rapport-cic-v2.md), [JSON](../../reports/cic-verificateur-v2.json).
100: - **J5.1 / J10.1 / J13.1 / J14.1 — bilans et clôture** : F1 **0,7902** (tagger **0,9475**), chantier **20/21** ; **J13.1** **612/602** ; **J14.1** clôture **84/81/3** (tag `c
… [659 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "- **Panini J12.1–J12.2** : §334 **495 paires uniques** ; CIC **42/42** verdicts, **42/42** empreintes, **36/36** preuves altérées rejetées, **1 020/1 020** mutations `eq(2,2)` rejetées ; [§334]( … [1038 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "offset": 117, "limit": 25}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md</path>
<type>file</type>
<content>
117: **J12.2 — le corpus d'or CIC rejoué hors de Panini.** Le corpus portable de Panini
118: (**3** defs, **21** consts, **42** entrées : **36** `accepte`, **6** `rejette`) est rejoué par un
119: noyau **CIC-lite réécrit côté Drave**, sans importer le vérificateur de Panini : **42/42** verdicts,
120: **42/42** empreintes `sha256(preuve || type)`, **42/42** sérialisations canoniques. Le contrôle
121: négatif est net : altérer le dernier octet des **36** preuves acceptées les fait **36/36** rejeter,
122: et les **1 020** mutations d'un octet de `eq(2,2)` sont **1 020/1 020** rejetées ; un noyau
123: « accepte tout » et un noyau « rejette tout » échouent (respectivement **6** et **36** désaccords).
124: La copie `tools/tests/cic/corpus_dor_cic_v1.json` est **byte-identique** à la source
125: (`3018f6f4…aaec`) ; la porte `tools/porte-cic.sh` et **21** tests rejouent le tout. C'est un
126: **verrou de portabilité** : « nos deux systèmes vérifient les mêmes preuves », pas une preuve de
127: correction du noyau Panini (le corpus n'exerce que **20** des **39** étiquettes du for
… [1202 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "old_string": "**J12.2 — le corpus d'or CIC rejoué hors de Panini.** Le corpus portable de Panini\n(**3** defs, **21** consts, **42** entrées : **36** `accepte`, **6** `rejette`) est rejoué par un\nnoyau **CIC- … [3186 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/verifie_en_cours.py", "description": "Re-check en-cours state", "timeoutMs": 120000}`

  ```
en-cours · 1657 mots · 7 sections · 4 session(s) · 10 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -20", "description": "Re-check context budget", "timeoutMs": 120000}`

  ```
2962    364   T1   5000  docs/theorie/glossaire/02-modeles-et-architectures.md
    2896    352 DATÉ      0  docs/implantation/configuration-nvme-raid-amd.md
    2496    171   T1   2500  docs/pilotage/references-non-regression.md
    2371    216   T1   2800  reports/README.md
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4027 mots (budget 4 000)

  avertissements :
     · 55 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 2 violation(s) :
     · docs/pilotage/
… [110 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport re\nlines=open('docs/pilotage/en-cours.md').read().splitlines()\nfor i,l in enumerate(lines,1):\n    if 'Panini J12' in l or 'J11.1' in l or 'J5.1' in l:\n        print(i,len(re.findall(r'\\S+',l)),l)\nPY", "description": "Count words per candidate line"}`

  ```
64 39 - **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/239 (0,9958)**, **F1 0,7902**, **1 span** ; **`s065`** et **`r035`** réglés, **convention des GV** ; **restitution v1** (46/46 canonique, strict 0,1087 ; [fiche](../../reports/rapport-restitution-v1.md)) ; **J11.1–J11.4** ([exemples](../../reports/rapport-exemples-rejoues.md), [par-langue](../../reports/rapport-evaluer-langue.md), [robustesse](../../reports/rapport-robustesse-semaine.md), [schéma](../../reports/rapport-schema-v2-doc.md)).
98 48 - **Panini J12.1–J12.2 + B3** : §334 **495 paires uniques** ; CIC **42/42** verdicts ; B3 ajoute **42/42** types de Bruijn clos et bien formés, **42/42** empreintes par **deux** implémentations (hashlib + FIPS 180-4, **24/24** termes), **36/36** preuves et **42/42** types altérés rejetés ; [§334](../../reports/rapport-panini-334.md), [CIC](../../reports/rapport-cic-verificateur.md), [v2](../../reports/rapport-cic-v2.md), [JSON](../../reports/cic-verificateur-v2.json).
99 33 - **J5.1 / J10.1 / J13.1 / J14.1 — bilans et clôture** : F1 **0,7902** (tagger **0,9475**), chantier **20/21** ; **J13.1** **612/602** ; **J14.1** clôture **84/81/3** (tag `chantier-2026-11-14`) ; [se
… [798 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport re\nlines=open('docs/pilotage/en-cours.md').read().splitlines()\nstart=next(i for i,l in enumerate(lines) if l.startswith('## Ce qui est en cours'))\nend=next(i for i,l in enumerate(lines) if l.startswith('## Les chiffres'))\nfor i in range(start,end):\n    if l … [156 caractères tronqués]`

  ```
88 26 - **S — les structures** : 61/61 types, 144/144 rôles, 56 tests, banque 84/67 ; **19/19 verdicts `389b99f`** ; `/paragraphes` v7, `/` ancien
89 28 - **N2 — en pause** : **commande validée** `eval_longueurs.py --rope --val <dir>` (**2,7856**) ; **jamais `--rope` seul** (**40,0658**) ; [v
90 35 - **Pensée — B13 (actif)** : **183/183** ; `r035` (238/238), convention GV (0,7902), `s065` (238/238), **J6.1 rejeté** (g017 à trancher), sc
91 20 - **L — le bloc langue** : contrat ; frontière script 1,0, langue 0,137/0,9687 ; fusion réparée par niveau **0,9309/0,8226/0,8784/0,9954**.
92 52 - **Panini J2.1–J3.2 + B2** : **14 atomes** ; UDHR **418/438** ; J3.2 : **5/21** langues (Glottolog **21/21**), **154/154** paires hors scri
93 33 - **Panini J7.1** : 532 textes (445 langues) ; hors script, hasard ; famille **66,1 %** / sœur **26,1 %** (hasard 10,3/2,5) ; LANG_TREE : sœ
94 17 - **Panini B1 — protocole à date contrôlée** : **60 paires** (20 G1 inter-traditions à ±10 ans,
98 48 - **Panini J12.1–J12.2 + B3** : §334 **495 paires uniques** ; CIC **42/42** verdicts ; B3 ajoute **42/42** types de Bruijn clos et bien form
99 33 - **J5.1 / J10.1 / J13.1 / J14.1 — bilans et clôture** : F1 **0,
… [224 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "- **Panini J12.1–J12.2 + B3** : §334 **495 paires uniques** ; CIC **42/42** verdicts ; B3 ajoute **42/42** types de Bruijn clos et bien formés, **42/42** empreintes par **deux** implémentations  … [682 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "- **J11.1–J11.4** : fr/en, 50 textes, schéma v2 ; [exemples](../../reports/rapport-exemples-rejoues.md), [langue](../../reports/rapport-evaluer-langue.md), [robustesse](../../reports/rapport-rob … [92 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "old_string": "**B3 — CIC v2 : le contrat et l'empreinte vérifiés deux fois.** Sans changer la fixture : **42/42**\ntypes de de Bruijn clos et bien formés (`[] ⊢ type : sort n`), **42/42** preuves closes ; sha2 … [936 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -8", "description": "Re-check budget", "timeoutMs": 120000}`

  ```
1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4000 mots (budget 4 000)

  avertissements :
     · 55 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 1 violation(s) :
     · docs/pilotage/roadmap.md : 9004 mots > budget 9000 (T1)
  ```

- **bash** `{"command": "python3 tools/verifie_en_cours.py", "description": "Re-check en-cours", "timeoutMs": 120000}`

  ```
en-cours · 1630 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "old_string": "**B3 — CIC v2 : le contrat et l'empreinte vérifiés deux fois.** **42/42** types de Bruijn clos et\nbien formés (`[] ⊢ type : sort n`), **42/42** preuves closes ; sha256 rejoué par une **seconde\n … [386 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -6; echo '---'; python3 tools/revue_documentation.py", "description": "Check budget and docs review", "timeoutMs": 180000}`

  ```
T0 max : 4000 mots (budget 4 000)

  avertissements :
     · 55 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
---
  revue de documentation · 741 fiche(s) · 835 JSON · 123 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ```

- **bash** `{"command": "bash tools/porte-tableaux.sh", "description": "Re-run table/link gate", "timeoutMs": 180000}`

  ```
✅ 1813 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4358 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-15)
  ```

- **bash** `{"command": "python3 tools/verifie_journal.py", "description": "Re-check journal", "timeoutMs": 120000}`

  ```
journal · 47 jour(s) · 199 session(s) · 2565 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
  ```

- **bash** `{"command": "sed -n '1,120p' tools/toutes-les-portes.sh", "description": "Inspect all-gates script"}`

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

- **bash** `{"command": "PORTES=\"cic\" DELAI=300 bash tools/toutes-les-portes.sh; echo '--- registre'; cat work/portes-*/registre.txt 2>/dev/null | tail -5", "description": "Run CIC gate via registry", "timeoutMs": 360000}`

  ```
=== PASSE COMPLÈTE DES PORTES (1 portes, borne 300 s) ===
    journaux : work/portes-1115-04h03
  porte-cic              ✅                          10 s  ✅ porte CIC verte : 42/42 verdicts, empreintes, de Bruijn, sha256 2e implémentation,
--- 1 vertes, 0 rouges ---
TOUTES LES PORTES SONT VERTES — et elles ont TOUTES tourné, ce que rien ne garantissait avant.
Journaux : work/portes-1115-04h03
--- registre
porte-n3-service 0 6
porte-n3-seuil 0 6
porte-n3-sparsite-compte 0 4
porte-n3-sparsite 0 5
--- 17 vertes, 0 rouges ---
  ```

- **bash** `{"command": "cat work/portes-1115-04h03/registre.txt; awk '$2 != 0' work/portes-1115-04h03/registre.txt; echo \"awk_exit=$?\"", "description": "Read current gate registry verdict"}`

  ```
porte-cic 0 10
--- 1 vertes, 0 rouges ---
--- 1 vertes, 0 rouges ---
awk_exit=0
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport hashlib,json,pathlib\nm=json.load(open('reports/cic-verificateur-v2.json'))\nok=True\nfor p,h in m['sources_code'].items():\n    cur=hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()\n    if cur!=h:\n        ok=False; print('MISMATCH',p,h,cur)\nprint('sou … [146 caractères tronqués]`

  ```
sources ok True
verdict pass tests {'commande': 'python3 tools/tests/test_verificateur_cic.py ; python3 tools/tests/test_verificateur_cic_v2.py', 'cas_j122': 21, 'cas_b3': 17, 'cas_total': 38, 'echecs': 0} porte 0
  ```

- **bash** `{"command": "python3 tools/index_reports.py --help 2>&1 | head -30", "description": "Inspect reports index generator"}`

  ```
usage: index_reports.py [-h] [--verifier] [--aide]

Génère reports/INDEX.md (déterministe).

options:
  -h, --help  show this help message and exit
  --verifier  ne réécrit rien : compare l'index au disque, sort 1 s'il est
              périmé
  --aide      affiche l'aide et sort
  ```

- **bash** `{"command": "python3 tools/index_reports.py --verifier; echo exit=$?", "description": "Check if reports index is stale"}`

  ```
exit=1
  ```

- **bash** `{"command": "git diff --stat -- tools/verificateur_cic.py tools/porte-cic.sh tools/tests/cic/README.md docs/pilotage/en-cours.md docs/pilotage/roadmap.md journal/2026-11-15/README.md; echo '---'; git diff -- tools/verificateur_cic.py | sed -n '1,260p'", "description": "Review diff of modified tracke … [9 caractères tronqués]`

  ```
docs/pilotage/en-cours.md    |   7 +-
 docs/pilotage/roadmap.md     |  27 +--
 journal/2026-11-15/README.md |  15 ++
 tools/porte-cic.sh           |  77 +++++++--
 tools/tests/cic/README.md    |  16 +-
 tools/verificateur_cic.py    | 400 +++++++++++++++++++++++++++++++++++++++++--
 6 files changed, 495 insertions(+), 47 deletions(-)
---
diff --git a/tools/verificateur_cic.py b/tools/verificateur_cic.py
index f6512e79..b7ac9c57 100644
--- a/tools/verificateur_cic.py
+++ b/tools/verificateur_cic.py
@@ -19,13 +19,21 @@ Ce que le vérificateur contrôle
    byte-identique à l'original Panini).
 2. **Sérialisation canonique** : chaque terme (défs, constantes, preuves, types)
    se décode puis se ré-encode exactement sur les mêmes octets.
-3. **Empreinte** : `sha256(octets(preuve) || octets(type))` égale l'empreinte déclarée.
-4. **Verdicts** : le noyau rend `True` pour les 36 « accepte » et `False` pour les
+3. **Type de de Bruijn** (B3) : chaque type est **clos** (aucun indice hors
+   portée) et bien formé (`[] ⊢ type : sort n`) ; chaque preuve est close elle
+   aussi. Un type valide n'est pas supposé : il est vérifié avant de servir de
+   contrat à la preuve.
+4. **Empreinte** : `sh
… [11397 caractères tronqués]
  ```

- **bash** `{"command": "git diff --check -- tools/verificateur_cic.py tools/porte-cic.sh tools/tests/cic/README.md docs/pilotage/en-cours.md docs/pilotage/roadmap.md journal/2026-11-15/README.md; echo diffcheck=$?; python3 -m py_compile tools/verificateur_cic.py tools/tests/test_verificateur_cic_v2.py; echo co … [57 caractères tronqués]`

  ```
diffcheck=0
compile=0
  ```

- **bash** `{"command": "git add tools/verificateur_cic.py tools/tests/test_verificateur_cic_v2.py tools/porte-cic.sh tools/tests/cic/README.md reports/rapport-cic-v2.md reports/cic-verificateur-v2.json docs/pilotage/en-cours.md docs/pilotage/roadmap.md journal/2026-11-15/README.md && git status --short && echo … [86 caractères tronqués]`

  ```
M  docs/pilotage/en-cours.md
M  docs/pilotage/roadmap.md
M  journal/2026-11-15/README.md
A  reports/cic-verificateur-v2.json
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
A  reports/rapport-cic-v2.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/plan.json
M  tools/porte-cic.sh
M  tools/tests/cic/README.md
A  tools/tests/test_verificateur_cic_v2.py
M  tools/verificateur_cic.py
?? reports/rapport-gold-reel-50.json
?? reports/rapport-gold-reel-50.md
?? reports/rapport-s-paragraphes.md
?? tools/tests/linguistique/gold_reel_50.py
--- staged stat
 docs/pilotage/en-cours.md               |   7 +-
 docs/pilotage/roadmap.md                |  27 +-
 journal/2026-11-15/README.md            |  15 +
 reports/cic-verificateur-v2.json        | 944 ++++++++++++++++++++++++++++++++
 reports/rapport-cic-v2.md               | 267 +++++++++
 tools/porte-cic.sh                      |  77 ++-
 tools/tests/cic/README.md               |  16 +-
 tools/tests/test_verificateur_cic_v2.py | 183 +
… [122 caractères tronqués]
  ```

- **bash** `{"command": "git commit -m \"B3 — LE CORPUS D'OR CIC V2 : 42/42 TYPES DE BRUJIN BIEN FORMÉS, 42/42 SHA256 PAR DEUX IMPLÉMENTATIONS, 36/36 PREUVES ET 42/42 TYPES ALTÉRÉS REJETÉS\" -m \"Le corpus portable (3 defs, 21 consts, 42 entrées) et ses 42 verdicts sont inchangés. Le vérificateur gagne trois co … [695 caractères tronqués]`

  ```
[s/v7 2067a6f0] B3 — LE CORPUS D'OR CIC V2 : 42/42 TYPES DE BRUJIN BIEN FORMÉS, 42/42 SHA256 PAR DEUX IMPLÉMENTATIONS, 36/36 PREUVES ET 42/42 TYPES ALTÉRÉS REJETÉS
 21 files changed, 4582 insertions(+), 75 deletions(-)
 create mode 100644 journal/sessions/session-3241a992-ffa6-4c12-ab1c-a8e175f880b7/digest.md
 create mode 100644 journal/sessions/session-3241a992-ffa6-4c12-ab1c-a8e175f880b7/rapport.md
 create mode 100644 reports/cic-verificateur-v2.json
 create mode 100644 reports/rapport-cic-v2.md
 create mode 100644 tools/tests/test_verificateur_cic_v2.py
[stderr]
  ✅ index : aucun fait stagé sans état
  ```

- **bash** `{"command": "git show --stat --oneline HEAD | head -40; echo '--- status'; git status --short | head -30", "description": "Inspect commit contents and status"}`

  ```
2067a6f0 B3 — LE CORPUS D'OR CIC V2 : 42/42 TYPES DE BRUJIN BIEN FORMÉS, 42/42 SHA256 PAR DEUX IMPLÉMENTATIONS, 36/36 PREUVES ET 42/42 TYPES ALTÉRÉS REJETÉS
 docs/pilotage/en-cours.md                          |    7 +-
 docs/pilotage/roadmap.md                           |   27 +-
 journal/2026-11-15/README.md                       |   22 +-
 journal/2026-11-15/distribue.md                    |    2 +-
 journal/2026-11-15/docs.md                         |    5 +-
 journal/2026-11-15/mesures.md                      |    2 +-
 journal/2026-11-15/portes.md                       |    2 +-
 journal/README.md                                  |    5 +-
 journal/sessions/MANIFEST.md                       |    7 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md |   11 +
 .../rapport.md                                     |   14 +-
 .../digest.md                                      |  183 ++
 .../rapport.md                                     |   54 +-
 .../digest.md                                      | 2254 ++++++++++++++++++++
 .../rapport.md                                     |  175 ++
 reports/cic-verificateur-v2.json                   |  944 ++++++++
 reports/rapport-cic-v2.md  
… [822 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py", "description": "Final docs review", "timeoutMs": 180000}`

  ```
revue de documentation · 741 fiche(s) · 835 JSON · 123 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ```

- **bash** `{"command": "bash tools/porte-tableaux.sh", "description": "Final table/link gate", "timeoutMs": 180000}`

  ```
✅ 1813 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4358 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-15)
  ```

- **bash** `{"command": "python3 tools/verifie_en_cours.py && python3 tools/verifie_journal.py && python3 tools/taille_documents.py 2>&1 | tail -4", "description": "Final state/budget checks", "timeoutMs": 180000}`

  ```
en-cours · 1630 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  journal · 47 jour(s) · 200 session(s) · 2569 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
  avertissements :
     · 55 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  ```

- **bash** `{"command": "git log -1 --format='%h %s' && echo '---' && python3 tools/verificateur_cic.py | tail -8", "description": "Final commit and verifier summary", "timeoutMs": 120000}`

  ```
2067a6f0 B3 — LE CORPUS D'OR CIC V2 : 42/42 TYPES DE BRUJIN BIEN FORMÉS, 42/42 SHA256 PAR DEUX IMPLÉMENTATIONS, 36/36 PREUVES ET 42/42 TYPES ALTÉRÉS REJETÉS
---
Type de Bruijn : 42/42 types clos et bien formés (42/42 preuves closes)
sha256 indépendant : pass (corpus ok, 42/42 couples, 24/24 termes)
Contrôles négatifs :
  octet altéré (36 preuves acceptées) : 36/36 rejetés, 0 accepté(s) — pass
  type altéré (42 entrées) : 42/42 rejetés, 36 type(s) invalide(s) — pass
  exhaustif eq(2,2) : 1020/1020 rejetés, 0 accepté(s) — pass
  non-trivialité : accepte-tout 36/42, rejette-tout 6/42
Durée : 1.101 s — VERDICT PASS
  ```

### 🤖 Assistant

**B3 terminée et committée** — `2067a6f0`.

## Ce qui a été ajouté au vérificateur

**1. Vérification du type de de Bruijn** (`tools/verificateur_cic.py`)
- portée purement structurelle : aucun `var i` hors des lieurs ouverts ;
- bien-formedness : `[] ⊢ type : sort n` ;
- une preuve n'est acceptée que si son type est clos et bien formé.

**Résultat** : **42/42** types clos et bien formés (**38** en `sort 0`, **4** en `sort 1`), **42/42** preuves closes.

**2. Seconde implémentation de SHA-256**
- FIPS 180-4 réécrite dans le module, **sans `hashlib`** ;
- **16** vecteurs (FIPS + longueurs de rembourrage) ;
- rejeu du sha256 du fichier, des **42** couples `preuve || type` et des **24** termes de l'environnement ;
- **0 écart** avec `hashlib` et avec les empreintes déclarées.

**3. Contrôles négatifs étendus**
- **36/36** preuves altérées rejetées ;
- **42/42** types altérés rejetés — dont **36** types devenus invalides et **6** rejets par la preuve ;
- **1 020/1 020** mutations de `eq(2,2)` rejetées ;
- corpus corrompu (preuve **ou** type) refusé en code **1**.

## Porte et tests
`bash tools/porte-cic.sh` : ✅ verte
- **21** tests J12.2 + **17** tests B3 = **38** cas.

## Livrables
- Fiche : [`reports/rapport-cic-v2.md`](reports/rapport-cic-v2.md)
- JSON : [`reports/cic-verificateur-v2.json`](reports/cic-verificateur-v2.json)
- Code : [`tools/verificateur_cic.py`](tools/verificateur_cic.py), [`tools/porte-cic.sh`](tools/porte-cic.sh), [`tools/tests/test_verificateur_cic_v2.py`](tools/tests/test_verificateur_cic_v2.py)
- État et roadmap mis à jour (`docs/pilotage/en-cours.md`, `docs/pilotage/roadmap.md`), récit dans `journal/2026-11-15/README.md`.

Les modifications préexistantes hors B3 (autres rapports, `tools/chantier/plan.json`) n'ont pas été touchées.

