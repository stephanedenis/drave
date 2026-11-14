# Session DSH — relecture

- identifiant : `session-6a9e96a0-20f8-4721-8b73-82eba29bd2b6`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-14 05:08:37
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche J12.1 : la deuxième vague Panini — le corpus §334 (114 textes, 655 paires, 102 sources) et les signatures des 44 œuvres (14 flottants) : mesurer le retrieval et la prédiction de l'époque vs la filiation, avec le contrôle de date. Fiche `reports/rapport-panini-334.md` + JSON.

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

- **bash** `{"command": "pwd && ls && echo '---' && ls reports | tail -40 && echo '---' && ls journal | tail -20", "description": "List repo root, reports, journal"}`

  ```
/home/stephane/Data13TB/stephane/GitHub/Qtrinet
AGENTS.md
bench
colab
data
docs
drave-core
journal
models
__pycache__
Qtrinet-bootstrap.md
README.md
reports
REPRISE.md
run_8bit_perfection.py
run_clusters.py
run_cpu.py
run_encoding.py
run_harness.py
run_list_mode.py
run_precision.py
run_quantify.py
run_real_clusters.py
run_sparsity.py
run_value_encoding.py
sprints
src
tools
work
---
traduction-eurlex-7b-fraeng.json
traduction-eurlex-7b.json
traduction-jw-A.json
traduction-jw-B.json
traduction-langues-3b.json
traduction-langues-7b.json
traduction-legal-0.5b-6.json
traduction-legal-1.5b.json
traduction-legal-3b.json
traduction-legal-7b.json
traduction-legal.json
traduction-litteraire-3b.json
traduction-litteraire-7b.json
traduction-onu-3b.json
traduction-onu6-3b.json
traduction-onu6-7b.json
traduction-onu-7b.json
traduction-pidgin-14b.json
traduction-pidgin-7b.json
traduction-presse-3b.json
traduction-presse-7b.json
traduction-udhr-propre-3b-fraeng.json
traduction-udhr-propre-7b-fraeng.json
traduction-udhr-propre-7b.json
universaux-mesures.json
xnli-14b.json
xnli-14b-l18.json
xnli-14b-l24.json
xnli-14b-l30.json
xnli-14b-l36.json
xnli-1.5b.json
xnli-1.5b-l14.json
xnli-1.5b-l22.json
xnl
… [348 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/methode/panini-nipada.md"}`

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

- **bash** `{"command": "ls ../ | head -30; echo '--- panini files'; ls reports | grep -i panini; echo '--- journal'; grep -ril panini journal | tail -30; echo '--- tools'; ls tools | grep -i panini; echo '--- src'; find src -iname '*panini*' -o -iname '*334*' | head -40", "description": "Find Panini-related fi … [5 caractères tronqués]`

  ```
915-SPO (1).com
915-SPO.com
915-SPO.com-2
Ai_Docs
arduino-i2c-scanner
Arduino-IRremote
ArduinoNunchuk
Biblio
Biblio-2
blue-pill-quickstart
bohemian-lab
consolider_panini_research.sh
contcal
copilotage
copilotage-shared
DeDRM_tools
drave-structures
emails
equipement-kindle
equipment-cam-IP-PTZ
equipment-dvr-coax
equipment-hauru
equipment-kamaji
equipment-mystery
equipment-ponyo
equipment-radio
equipment-remarkable
equipment-router
equipment-totoro
ESP32-CAM-Experiments
--- panini files
pensee-inventaire-panini.json
rapport-inventaire-panini.md
--- journal
journal/sessions/session-b0a87524-43a4-4935-a248-72c1d42c8471/digest.md
journal/sessions/session-b0a87524-43a4-4935-a248-72c1d42c8471/rapport.md
journal/sessions/session-9d3b2074-c5f0-4f11-be10-31d317bac657/digest.md
journal/sessions/session-9d3b2074-c5f0-4f11-be10-31d317bac657/rapport.md
journal/sessions/session-6b997dd9-9a2e-4d72-b31a-5a6d40609d56/digest.md
journal/sessions/session-6b997dd9-9a2e-4d72-b31a-5a6d40609d56/rapport.md
journal/sessions/session-631f4ba2-5c36-4fdc-b751-fa0a2cce9d21/digest.md
journal/sessions/session-631f4ba2-5c36-4fdc-b751-fa0a2cce9d21/rapport.md
journal/2026-10-10/reprise-historique.md
journal/2026-10-17
… [600 caractères tronqués]
  ```

- **bash** `{"command": "git log --oneline -30; echo '--- status'; git status --short | head -40", "description": "Recent git history and status"}`

  ```
febfdfff J11.4 — SCHÉMA v2 DOCUMENTÉ : 4 CHAMPS PARTITION + 10 CHAMPS ALTERNATIVE, 6 CAS / 0 ÉCHEC, LES DEUX VERSIONS LUES (612 v2 + 612 v1)
55bde5c5 J11.3 — LES 50 TEXTES LIBRES : 0 PLANTAGE, 50/50 SCHÉMA V2, 115 CHEVAUCHEMENTS ALTERNATIVE / 0 FILTRER ; RESTITUTION 46/46, STRICT 0,1087 (F1 0,7902)
09e54143 J11.2 — EVALUER --PAR-LANGUE : FR 0,8159/0,7475 (151/151), EN 0,9451/0,8656 (87/88), GLOBAL INCHANGÉ
84e393bb J11.1 — LES 5 EXEMPLES REJOUÉS : 4 BLOCS SUR 5 CORRIGÉS, r035 DÉSORMAIS PRÉDIT ; F1 0,7902, ATTACHEMENT 238/238
a6808c5e CHANTIER — LE PLAN EST RELU À CHAQUE TOUR (LA BOUCLE VOYAIT UNE FILE VIDE APRÈS UN AJOUT DE TÂCHES) ; ÉTAT HORODATÉ
03ecee41 J10.1 — LE BILAN DU CHANTIER : F1 0,7533 → 0,7902, ATTACHEMENT 236 → 238, 20/21 TÂCHES, 5 TIMEOUTS, 1 ÉCHEC (LE TAG) ; PANINI MESURÉ ET BORNÉ
81fc9ecf JOURNAL — 2026-11-14 : J9.1 AU RÉCIT (19 FICHES « INSTANTANÉ HISTORIQUE »)
ecef7250 J9.1 — PASSE D'HONNÊTETÉ : 19 FICHES « INSTANTANÉ HISTORIQUE », 4 CHIFFRES DÉPASSÉS NE SE LISENT PLUS COMME L'ÉTAT COURANT
229098ec J8.1 — RESTITUTION V1 : FORME CANONIQUE 46/46, MIROIR STRICT 0,1087 (NE MONTE PAS)
d31e8788 J7.1 — RETRIEVAL PAR FAMILLE : 532 TEXTES (445 LANGUES), SŒURS 0,619 VS 0,04
… [3104 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"J12\\|J11\\|Panini\\|panini\\|334\" docs/pilotage/en-cours.md | head -60; echo '=== plan'; python3 - <<'EOF'\nimport json\np=json.load(open('tools/chantier/plan.json'))\nprint(type(p), list(p)[:20] if isinstance(p,dict) else len(p))\nEOF", "description": "Search state and plan … [12 caractères tronqués]`

  ```
63:- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/238 labels (238/239 cibles, 0,9958)**, **F1 0,7902**, **1 span (`g017`)** ; **`s065` réglé** (porte produit 183/183 ; [fiche](../../reports/rapport-s065.md)) ; **`r035`**, **convention des GV** (0,7902, 0 perte) ; **J6.1 rejetée** (test −0,0028, att. 236/237 ; [fiche](../../reports/rapport-g017.md)) ; **restitution v1** (46/46 canonique, strict 0,1087 ; [fiche](../../reports/rapport-restitution-v1.md)) ; **J11.1–J11.4** ([exemples](../../reports/rapport-exemples-rejoues.md), [par-langue](../../reports/rapport-evaluer-langue.md), [robustesse](../../reports/rapport-robustesse-semaine.md), [schéma](../../reports/rapport-schema-v2-doc.md)) ; **contrat v1**, **`drave` v0**.
91:- **Panini J2.1/J2.2/J3.1/J3.2** : table **14 atomes** ; UDHR **418/438** ; **J3.1** : script domine, date non significative ; **J3.2** : `lang_distance` couvre **5/21** langues (Glottolog **21/21**), **154/154** paires hors script au hasard, la famille vit dans **2-3 paires**, **V14 : 3/21** ; [atomes](../../reports/rapport-atomes-niveaux.md), [corpus](../../reports/rapport-corpus-commun.md), [époque](../../reports/rapport-retrieval-epoque.md), 
… [1127 caractères tronqués]
  ```

- **bash** `{"command": "wc -l reports/rapport-inventaire-panini.md; ls -la ../Panini ../Panini-Research 2>&1 | head -50; echo '=== consolider script'; sed -n '1,80p' ../consolider_panini_research.sh", "description": "Inspect Panini repos and inventory report"}`

  ```
548 reports/rapport-inventaire-panini.md
lrwxrwxrwx. 1 stephane stephane  15 18 oct 18:03 ../Panini-Research -> Panini/research

../Panini:
total 312
drwxr-xr-x. 1 stephane stephane    814 22 oct 22:15 .
drwxr-xr-x. 1 stephane stephane   2532  5 nov 10:41 ..
drwxr-xr-x. 1 stephane stephane    126 27 jan  2026 config
-rw-------. 1 stephane stephane  19733 14 sep 13:19 CONTEXTE-IA.md
drwxr-xr-x. 1 stephane stephane    324 19 mai 09:33 copilotage
drwxr-xr-x. 1 stephane stephane     62  2 mai  2026 corpus
drwxr-xr-x. 1 stephane stephane   6202  8 sep 07:56 data
-rw-r--r--. 1 stephane stephane    635 27 jan  2026 Dockerfile.template
drwxr-xr-x. 1 stephane stephane   1150 13 sep 12:43 docs
-rw-r--r--. 1 stephane stephane    721 27 jan  2026 .env
-rw-r--r--. 1 stephane stephane    769 27 jan  2026 .env.example
drwxr-xr-x. 1 stephane stephane    118 11 mai  2026 experiments
-rw-r--r--. 1 stephane stephane    894 27 jan  2026 experiments.json
drwxr-xr-x. 1 stephane stephane    208 22 oct 22:16 .git
drwxr-xr-x. 1 stephane stephane    140 10 sep 09:23 .github
-rw-r--r--. 1 stephane stephane   2221 19 mai 08:45 .gitignore
-rw-r--r--. 1 stephane stephane   2005  7 sep 12:45 .gitmodules
drwxr-xr
… [3946 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\np=json.load(open('tools/chantier/plan.json'))\nfor t in p['taches']:\n    if 'J12' in str(t.get('id','')) or 'J11' in str(t.get('id','')) or 'panini' in json.dumps(t,ensure_ascii=False).lower():\n        print(json.dumps(t,ensure_ascii=False,indent=1)[:30 … [88 caractères tronqués]`

  ```
{
 "id": "J2.1",
 "jour": 2,
 "titre": "Panini I — la table atomes ↔ niveaux",
 "mandat": "Tâche J2.1 : la table de correspondance entre les **14 atomes** de Panini (∃ ∆ ∼ ↗ ⊙ ⧖ ◇ № ⊕ ⊗ λ ⊞ ≍ ≡) et nos **niveaux** (graphème, mot, pos, syntagme, phrase, pragmatique, discours, document). Lis `../Panini/README.md`, `../Panini-Research/`, `docs/theorie/genealogie-des-langues.md`. Produis `reports/rapport-atomes-niveaux.md` + JSON : 14 lignes, ce que chaque atome capte, quel niveau le porte, la mesure possible. Aucune écriture dans Panini.",
 "budget_min": 90,
 "acceptation": [
  {
   "commande": "test -f reports/rapport-atomes-niveaux.md && echo FICHE-OK",
   "attendu": "FICHE-OK"
  },
  {
   "commande": "grep -c '∃' reports/rapport-atomes-niveaux.md",
   "attendu": ""
  }
 ]
}
---
{
 "id": "J2.2",
 "jour": 2,
 "titre": "Panini I — le corpus commun",
 "mandat": "Tâche J2.2 : le corpus commun — choisir un échantillon (10-50 textes) présent des deux côtés (Panini/NIPADA et Drave), le normaliser (UTF-8, une phrase par ligne, métadonnées langue/époque), l'écrire dans `work/corpus-commun/` (non versionné) + une fiche `reports/rapport-corpus-commun.md` + JSON. Lire les corpus Panini sans les
… [6349 caractères tronqués]
  ```

- **bash** `{"command": "grep -rln \"lang_distance\\|retrieval.epoque\\|655\" --include='*.py' --include='*.json' --include='*.md' . ../Panini/research 2>/dev/null | grep -v '.git/' | head -40", "description": "Locate retrieval scripts and 655 references"}`

  ```
./reports/rapport-mur-memoire-4bits.md
./reports/rapport-drapeaux-ignores.md
./reports/rapport-v41-mhc.md
./reports/rapport-pont-generatif.md
./reports/archive/rapport-toutes-langues.md
./reports/toutes-langues/047-47-fidelite-et-invariance-tirent-en-sens-op.md
./reports/toutes-langues/051-51-la-contrainte-dinvariance-fonctionne-dan.md
./reports/toutes-langues/055-55-le-pont-transfere-sur-le-corpus-wikipedi.md
./reports/toutes-langues/086-79-la-verification-a-482-articles-le-result.md
./reports/toutes-langues/087-80-le-discriminant-lui-non-seulement-se-rep.md
./reports/toutes-langues/091-R-c-4-ce-qui-reste-ouvert-en-une-question.md
./reports/toutes-langues/094-82-la-cible-du-projet-etait-un-effet-de-pan.md
./reports/toutes-langues/102-90-la-replication-du-88-5-le-gain-de-fideli.md
./reports/toutes-langues/103-91-tableau-de-bord-chaque-chiffre-avec-ses.md
./reports/rapport-consolidation-c7.md
./reports/rapport-memoire-travail-n5.md
./reports/restitution-udhr.json
./reports/restitution-udhr-flux.json
./reports/marqueurs-bruit.json
./reports/marqueurs-bruit-3b.json
./reports/bruit-entree.json
./reports/traduction-eurlex-0.5b.json
./reports/traduction-eurlex-1.5b.json
./reports/traduct
… [785 caractères tronqués]
  ```

- **job_kill** `{"job_id": "bash-7", "reason": "Grep over huge repo; use targeted search instead"}`

  ```
requested cancellation of job bash-7
  ```

- **bash** `{"command": "cd ../Panini/research && git log --oneline -15; echo '=== top'; ls; echo '=== 334'; grep -ril '334' --include='*.md' --include='*.py' --include='*.json' . 2>/dev/null | head -40", "description": "Inspect Panini research repo for §334"}`

  ```
e10d695e6 docs(incident): la classe vue depuis les KITS — un False rapide est un kit incomplet, pas une preuve cassee ; diagnostic en une commande
610a75d3b docs(catalogue): §3septiesdecies — localisation du produit : 2 pieces prouvees, le mur = DISTRIBUTIVITE Q absente (mesuree 936 s + >39 min)
e89594b79 docs(chantiers): incident — la DISTRIBUTIVITE Q manque (936 s de construction, >39 min de verification) ; bloquera mul_cut_located et toutes les lois d'anneau futures
7863eecf4 docs(noyau): chaine complete + C6j verifiee (296 defs / 412 consts / aucune manquante) ; passation §18 — 65 lemmes, 4 instruments, et ce qui n'est PAS prouve
38b515a11 docs(chantiers): C6j partiel — lois des coins livrees, 4 pieces restantes pour mul_cut_located, Archimede localise
200cfba81 feat(noyau): C6j — les LOIS DES COINS et 13 briques ℚ pour `mul_cut_located`
14f6e164d docs(journal): 2026-10-25 — la nuit du transfert de boite (23 lemmes), le mur de la double negation qui n'en etait pas un, et la dette des builders standalone
22e78f314 feat(noyau): la chaîne `_base_mul_un` inclut désormais C6f-b, C6h et C6i
369b51bd6 docs(noyau): audit n°3 vert (261/358/226) ; C6h/C6i faits ; dette identifiee — build
… [6965 caractères tronqués]
  ```

- **grep** `{"pattern": "§334|44 (œuvres|oeuvres)|14 flottants|655 paires|102 sources", "path": "/home/stephane/Data13TB/stephane/GitHub/Panini/research", "include": "*.md"}`

  ```
Found 244 matches

/home/stephane/Data13TB/stephane/GitHub/Panini/research/GATES_G1_G3_REPORT_2026-09-07.md
Line 20: ## G3 — Calibrage R² : ⚠️ reproduit 0.907849 (648 paires) vs officiel 0.909139 (655 paires)
Line 22: Résultats reproduit vs officiel §334 :
Line 28: Écart 7 paires = artefact DOCUMENTÉ (journal 24/05) : 7 textes signés entre §313-§334 dans des
Line 29: fichiers corpus intermédiaires non chargés. Corpus persistés actuels = ceux du §334 (vérifié).

/home/stephane/Data13TB/stephane/GitHub/Panini/research/REVISION_JOURNAUX_DE_BORD_2026-08-28.md
Line 27: - **Sprint ISO §329→§334** : R² 0.6067 → 0.7116 → 0.7710 → 0.8078 → 0.8983 → **0.909139 (milestone R²>0.90)** — graphe **v35 (1753 nœuds, 19 951 arêtes)**, 114 textes actifs, 655 paires, r=0.9535, p≈10⁻²⁴⁰.
Line 50: | R² falsification H₀ (§334, officiel) | **0.909139** (655 paires, 114 textes) | ✅ `nipada/falsification/nipada_v334_revalidation_v35.json` (decision=ACCEPTÉ) |
Line 51: | Répartition §334 | a) intra-trad 0.8866 · b) réf×trad 0.9014 · c) intra-refs **0.3240** | ✅ idem |
Line 89: 4. **Graphe v35 gelé** après §334 ; **Théorème de Fermeture** → toute densification dégrade (vérifié §366, §527).
Line 99:    - **Pas
… [27611 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini/research && ls docs | head -50; echo '=== catalogue'; find docs -iname '*catalogue*' | head; echo '=== recent docs changed'; git log --name-only --pretty=format: -10 | grep '\\.md' | sort -u | head -40", "description": "Find catalogue and recent docs"}`

  ```
ARCHITECTURE_NOYAU_NIPADA_v1.0.md
ARCHITECTURE_NOYAU_NIPADA_v2.0.md
CADRES_THEORIQUES_ET_IDEES_ORIGINALES.md
CRITIQUE_NIPADA_2026-07-14.md
DEMO_NIPADA_UDHR_Article1_COMPARAISON.md
DEMO_NIPADA_UDHR_Article1_EN.md
DEMO_NIPADA_UDHR_Article1_FR.md
DEMO_NIPADA_UDHR_Article1.md
directives
ETUDE_PROJET_PARENT_v1.0.md
images
journal-de-bord
MEMO_ARCHITECTURE_NIPADA_v1.md
NIPADA_SESSION_476_478c_FINAL_REPORT.md
NIPADA_SESSION_478d_479_FINAL_REPORT.md
NIPADA_SESSION_480_481_FINAL_REPORT.md
NIPADA_VULGARISATION.md
noyau
ouvrage
RECONCILIATION_DEMO_SYSTEME_v1.md
ROADMAP_v2_2026-07-14.md
ROADMAP_v3_2026-07-15.md
SYNTHESE_PIPELINE_SEMANTIQUE_v1.0.md
=== catalogue
docs/noyau/J4_CATALOGUE.md
=== recent docs changed
docs/journal-de-bord/2026-10-25.md
docs/noyau/CHANTIERS.md
docs/noyau/INCIDENT_2026-10-22_const_manquantes.md
docs/noyau/J4_CATALOGUE.md
docs/noyau/J4_PASSATION.md
docs/noyau/VALIDATIONS.md
  ```

- **bash** `{"command": "cd ../Panini/research && ls -lh nipada/falsification/ | head -40; echo '=== pair ax'; python3 - <<'EOF'\nimport json,os\np='nipada/falsification/pairs334_axes_v1.json'\nprint(os.path.getsize(p))\nd=json.load(open(p))\nprint(type(d), list(d)[:20] if isinstance(d,dict) else len(d))\nif is … [163 caractères tronqués]`

  ```
total 208M
-rw-r--r--. 1 stephane stephane  22K 18 oct 10:03 analytic_sigs_v1.json
-rw-r--r--. 1 stephane stephane 6,9K 18 oct 10:03 axeA_p1_subset_v1.json
-rw-r--r--. 1 stephane stephane 1,7K 18 oct 10:03 benchmark_generatif_analytique_v1.json
-rw-r--r--. 1 stephane stephane 4,2K 18 oct 10:03 benchmark_generatif_clean_v1.json
-rw-r--r--. 1 stephane stephane 9,2K  8 sep 15:34 benchmark_generatif_contenu_v1.json
-rw-r--r--. 1 stephane stephane 6,0K 18 oct 10:03 benchmark_generatif_corpus_v1.json
-rw-r--r--. 1 stephane stephane 2,2K 18 oct 10:03 benchmark_generatif_v1.json
-rw-r--r--. 1 stephane stephane  25K 30 avr  2026 circular_translation_test.json
-rw-r--r--. 1 stephane stephane 1,7K 18 oct 10:03 container_profiles_v1.json
-rw-r--r--. 1 stephane stephane 7,8K 28 jun 19:53 context_q1_embedding.json
-rw-r--r--. 1 stephane stephane 3,8K 28 jun 19:48 context_q1_normalized.json
-rw-r--r--. 1 stephane stephane  12K 28 jun 19:32 context_q1_translation_drift.json
-rw-r--r--. 1 stephane stephane  773 28 jun 19:32 context_q3_channel_stability.json
-rw-r--r--. 1 stephane stephane  46K 18 oct 10:03 corpus_dor_cic_v1.json
-rw-r--r--. 1 stephane stephane  37K 18 oct 10:03 corpus_dor_cic_v1.ts
… [2201 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini/research && grep -ril \"44\" --include='*.py' --include='*.json' nipada scripts philosophy-theory 2>/dev/null | xargs -r grep -il \"oeuvre\\|œuvre\\|works\\|signature\" 2>/dev/null | head -30", "description": "Search for 44 works signatures"}`

  ```
nipada/corpus/_cache/sources_manifest.json
nipada/corpus/_cache/sources_coverage.json
nipada/corpus/_cache/public_domain_auto/gutendex/manifest.json
nipada/corpus/catalog_african_colonial_v206x.json
nipada/corpus/catalog_buddhist_axial_v205.json
nipada/corpus/catalog_chinese_late_antique_v206f.json
nipada/corpus/catalog_chinese_medieval_v206h.json
nipada/corpus/catalog_greco_latin_axial_v206k.json
nipada/corpus/catalog_greco_latin_late_antique_v206l.json
nipada/corpus/catalog_greco_latin_medieval_v206m.json
nipada/corpus/catalog_indian_axial_v206a.json
nipada/corpus/catalog_indigenous_american_colonial_v206x.json
nipada/corpus/catalog_islamic_medieval_v206j.json
nipada/corpus/catalog_orientalist_translation_modern_v206c.json
nipada/corpus/catalog_western_radical_modern_v206p.json
nipada/corpus/catalog_western_rational_early_modern_v206n.json
nipada/corpus/catalog_western_rational_modern_v206o.json
nipada/corpus/delta_restitution_v260.json
nipada/corpus/nipada_v224_greco_latin_catalog.json
nipada/corpus/references_v272_analysis.json
nipada/corpus/signed_corpus_v208.json
nipada/corpus/signed_corpus_v212f.json
nipada/corpus/signed_corpus_v225_greco_latin.json
nipada/corpus/signed_corp
… [350 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini/research && python3 - <<'EOF'\nimport json\nfor p in ['nipada/falsification/analytic_sigs_v1.json','nipada/falsification/modern_sigs_v1.json','nipada/falsification/modern_corpus_sigs_v2.json']:\n    d=json.load(open(p)); print('\\n===',p, type(d))\n    if isinstance(d,dict) … [277 caractères tronqués]`

  ```
=== nipada/falsification/analytic_sigs_v1.json <class 'dict'>
['2_esdras', 'aristotle_categories', 'aristotle_de_caelo', 'aristotle_nicomachean_ethics', 'aristotle_parts_of_animals', 'aristotle_posterior_analytics', 'aristotle_prior_analytics', 'bengio_2003', 'book_of_enoch', 'curry_1930', 'daniel_book', 'dn1_brahmajala']
  2_esdras <class 'dict'> ['ÊTRE', 'DIFFÉRENCE', 'RAPPORT', 'ORIENTATION', 'SUJET', 'TEMPS', 'MODALITÉ', 'NOMBRE']
  aristotle_categories <class 'dict'> ['ÊTRE', 'DIFFÉRENCE', 'RAPPORT', 'ORIENTATION', 'SUJET', 'TEMPS', 'MODALITÉ', 'NOMBRE']
  aristotle_de_caelo <class 'dict'> ['ÊTRE', 'DIFFÉRENCE', 'RAPPORT', 'ORIENTATION', 'SUJET', 'TEMPS', 'MODALITÉ', 'NOMBRE']

=== nipada/falsification/modern_sigs_v1.json <class 'dict'>
['2_esdras', 'aristotle_categories', 'aristotle_nicomachean_ethics', 'aristotle_prior_analytics', 'bengio_2003', 'book_of_enoch', 'daniel_book', 'dn1_brahmajala', 'ezekiel_book', 'hosea_book', 'isaiah_book', 'jeremiah_book']
  2_esdras <class 'dict'> ['ÊTRE', 'DIFFÉRENCE', 'RAPPORT', 'ORIENTATION', 'SUJET', 'TEMPS', 'MODALITÉ', 'NOMBRE']
  aristotle_categories <class 'dict'> ['ÊTRE', 'DIFFÉRENCE', 'RAPPORT', 'ORIENTATION', 'SUJET', 'TEMPS', 'MO
… [657 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini/research && grep -ril \"44\" --include='*.md' philosophy-theory docs nipada 2>/dev/null | xargs -r grep -il \"œuvre\\|oeuvre\\|flottant\" 2>/dev/null | head -20", "description": "Search docs for 44 works and floating"}`

  ```
docs/journal-de-bord/2026-04-22.md
docs/journal-de-bord/2026-04-25.md
docs/journal-de-bord/2026-04-26.md
docs/journal-de-bord/2026-04-27.md
docs/journal-de-bord/2026-04-29.md
docs/journal-de-bord/2026-05-01.md
docs/journal-de-bord/2026-05-02.md
docs/journal-de-bord/2026-05-21.md
docs/journal-de-bord/2026-05-22.md
docs/journal-de-bord/2026-05-24.md
docs/journal-de-bord/2026-06-02.md
docs/journal-de-bord/2026-06-03.md
docs/journal-de-bord/2026-06-30.md
docs/journal-de-bord/2026-07-01.md
docs/journal-de-bord/2026-07-02.md
docs/journal-de-bord/2026-07-07.md
docs/journal-de-bord/2026-07-08.md
docs/journal-de-bord/2026-07-12.md
docs/journal-de-bord/2026-09-08.md
docs/CADRES_THEORIQUES_ET_IDEES_ORIGINALES.md
  ```

- **bash** `{"command": "cd ../Panini/research && python3 - <<'EOF'\nimport json\nfor p in ['nipada/falsification/analytic_sigs_v1.json','nipada/falsification/modern_sigs_v1.json','nipada/falsification/modern_corpus_sigs_v2.json']:\n    d=json.load(open(p)); print(p, 'n=',len(d))\n    k=next(iter(d)); v=d[k]\n  … [448 caractères tronqués]`

  ```
nipada/falsification/analytic_sigs_v1.json n= 44
 sample keys ['ÊTRE', 'DIFFÉRENCE', 'RAPPORT', 'ORIENTATION', 'SUJET', 'TEMPS', 'MODALITÉ', 'NOMBRE', 'ESPACE', 'OPÉRATION', 'FONCTION', 'STRUCTURE', 'SYMÉTRIE', 'ÉQUATION']
 nvals 14 first [0.07446500282604852, 0.013816044014481109, 0.10099345547363615, 0.005331763602619648] sum 0.9999999999999999
nipada/falsification/modern_sigs_v1.json n= 35
 sample keys ['ÊTRE', 'DIFFÉRENCE', 'RAPPORT', 'ORIENTATION', 'SUJET', 'TEMPS', 'MODALITÉ', 'NOMBRE', 'ESPACE', 'OPÉRATION', 'FONCTION', 'STRUCTURE', 'SYMÉTRIE', 'ÉQUATION']
 nvals 14 first [0.0, 0.11089005, 0.0, 0.00015707] sum 1.0
nipada/falsification/modern_corpus_sigs_v2.json n= 39
 sample keys ['sig', 'ntok', 'nrec']
=== grep flottant
docs/journal-de-bord/2026-07-05.md:20:| `openocd` scan chain | `all ones` (TDO flottante) |
docs/NIPADA_VULGARISATION.md:258:| `delta_expected` | valeur flottante ou `null` | Écart de restitution attendu si l'ambiguïté est irréductible |
nipada/corpus/_cache/public_domain_auto/gutendex/pg14287_l_île_mystérieuse_fr.txt:332:déplacement dans le sens vertical. L'appareil, flottant dans
nipada/corpus/_cache/public_domain_auto/gutendex/pg14287_l_île_mystérieuse_f
… [2719 caractères tronqués]
  ```

- **bash** `{"command": "ls -l reports/rapport-retrieval-epoque.md reports/rapport-genealogie-deux-faces.md reports/rapport-retrieval-familles.md reports/rapport-corpus-commun.md reports/rapport-atomes-niveaux.md 2>&1; echo '=== looking for scripts'; find work tools -maxdepth 3 -type f \\( -iname '*panini*' -o  … [148 caractères tronqués]`

  ```
-rw-------. 1 stephane stephane 22407  7 nov 14:53 reports/rapport-atomes-niveaux.md
-rw-------. 1 stephane stephane 21491  7 nov 15:16 reports/rapport-corpus-commun.md
-rw-r--r--. 1 stephane stephane 27574  7 nov 18:19 reports/rapport-genealogie-deux-faces.md
-rw-r--r--. 1 stephane stephane 20872  7 nov 17:40 reports/rapport-retrieval-epoque.md
-rw-r--r--. 1 stephane stephane 34244 14 nov 01:44 reports/rapport-retrieval-familles.md
=== looking for scripts
tools/__pycache__/retrieval_parallele.cpython-313.pyc
tools/__pycache__/retrieval_udhr.cpython-313.pyc
tools/__pycache__/decoupage_familles.cpython-313.pyc
tools/__pycache__/retrieval_epoque.cpython-313.pyc
tools/__pycache__/retrieval_familles.cpython-313.pyc
tools/retrieval_parallele.py
tools/retrieval_udhr.py
tools/decoupage_familles.py
tools/decouper_sous_familles.py
tools/retrieval_epoque.py
tools/retrieval_familles.py
  ```

- **bash** `{"command": "sed -n '1,180p' reports/rapport-retrieval-epoque.md", "description": "Read prior epoch retrieval report"}`

  ```
# J3.1 — Le retrieval inter-langues à époque contrôlée

> **Ligne de roadmap** : R0.7 (le bloc langue) · **Chantier** : semaine Panini, J3.1 · **Date** : 2026-11-07
> **Verdict** : ✅ **la mesure est faite ; elle borne l'avertissement** —
> dans ce retrieval de **surface**, **l'écriture domine** (+0,609 ; IC 95 % [0,529 ; 0,702]), la **famille**
> compte ensuite (+0,181 [0,106 ; 0,253]), et **l'écart d'années ne pèse pas en moyenne** (−0,034 par siècle
> [−0,075 ; +0,009], p = 0,19 par permutation). À écriture contrôlée, les couples **contemporains** et
> **décalés** sont au **même niveau** : **0,710 vs 0,710**. Le renversement brut (0,238 vs 0,427) est un
> **effet de composition** : les couples décalés contiennent **60 %** de paires de même écriture, les
> contemporains **33 %**. **L'époque ne domine pas ici ; le confondant de composition, lui, n'est pas nul : sans
> contrôle, il fausse la comparaison.**
> **Dispositif** : trois corpus, un même retrieval de surface (n-grammes de caractères, TF-IDF, cosinus,
> top-1) ; **B7** (71 langues, 35 concepts, libellés Wikidata 2026), **UDHR** (21 langues du corpus commun,
> 30 articles, 1948), **BIBLE** (12 traductions datées de 1744 à 201
… [10752 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini/research && python3 - <<'EOF'\nimport json\nd=json.load(open('nipada/falsification/pairs334_axes_v1.json'))\nprint(json.dumps(d['r2_L2'],ensure_ascii=False,indent=1))\nprint(json.dumps(d['vopt'],ensure_ascii=False,indent=1))\nprint('pair keys', list(d['pairs'][0]))\nfor p i … [129 caractères tronqués]`

  ```
{
 "a": 0.8865868831832314,
 "b": 0.9013737063007868,
 "c": 0.3239867750290341,
 "all": 0.9091387033097759
}
{
 "direct": 0.01,
 "translation": 0.01,
 "indirect": 1.0,
 "other": 1.8
}
pair keys ['section', 'a', 'b', 'd_topo', 'd_lex', 'd_H', 'cos', 'trad_a', 'trad_b', 'lang_a', 'lang_b', 'same_comp']
{
 "section": "a",
 "a": "dn1_brahmajala",
 "b": "mn2_sabbasava",
 "d_topo": 3.6,
 "d_lex": 0.33870554623886845,
 "d_H": 0.6076717359284258,
 "cos": 0.7492899129132787,
 "trad_a": "BUDDHIST_AXIAL",
 "trad_b": "BUDDHIST_AXIAL",
 "lang_a": "eng",
 "lang_b": "eng",
 "same_comp": true
}
{
 "section": "a",
 "a": "dn1_brahmajala",
 "b": "mn35_culasaccaka",
 "d_topo": 3.6,
 "d_lex": 0.25142955342124895,
 "d_H": 0.39816781717180877,
 "cos": 0.8085855379994222,
 "trad_a": "BUDDHIST_AXIAL",
 "trad_b": "BUDDHIST_AXIAL",
 "lang_a": "eng",
 "lang_b": "eng",
 "same_comp": true
}
{
 "section": "a",
 "a": "dn1_brahmajala",
 "b": "brahma_sutra_badarayana",
 "d_topo": 5.84,
 "d_lex": 0.1759746945506818,
 "d_H": 0.3467542343087578,
 "cos": 0.8748775343155926,
 "trad_a": "BUDDHIST_AXIAL",
 "trad_b": "INDIAN_AXIAL",
 "lang_a": "eng",
 "lang_b": "eng",
 "same_comp": true
}
  ```

- **bash** `{"command": "cd ../Panini/research && ls nipada/corpus | grep -i 'signed\\|catalog\\|corpus\\|manifest' | head -40; echo '=== reval'; python3 - <<'EOF'\nimport json\np='nipada/falsification/nipada_v334_revalidation_v35.json'\nd=json.load(open(p)); print(json.dumps(d,ensure_ascii=False,indent=1)[:300 … [81 caractères tronqués]`

  ```
catalog_african_colonial_v206x.json
catalog_buddhist_axial_v205.json
catalog_buddhist_late_antique_v206d.json
catalog_buddhist_medieval_v206i.json
catalog_chinese_axial_v206b.json
catalog_chinese_early_modern_v206s.json
catalog_chinese_late_antique_v206f.json
catalog_chinese_medieval_v206h.json
catalog_chinese_modern_v206t.json
catalog_greco_latin_axial_v206k.json
catalog_greco_latin_late_antique_v206l.json
catalog_greco_latin_medieval_v206m.json
catalog_indian_axial_v206a.json
catalog_indian_early_modern_v206q.json
catalog_indian_late_antique_v206e.json
catalog_indian_medieval_v206g.json
catalog_indian_modern_v206r.json
catalog_indigenous_american_colonial_v206x.json
catalog_islamic_medieval_v206j.json
catalog_islamic_modern_v206u.json
catalog_orientalist_translation_modern_v206c.json
catalog_south_american_colonial_v206x.json
catalog_western_radical_contemporary_v206w.json
catalog_western_radical_modern_v206p.json
catalog_western_rational_contemporary_v206v.json
catalog_western_rational_early_modern_v206n.json
catalog_western_rational_modern_v206o.json
INDEX_catalogs_v206z.json
INDEX_catalogs_v207a.json
nipada_v224_greco_latin_catalog.json
nipada_v226_islamic_catalog.json
signed_
… [1069 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini/research && python3 - <<'EOF'\nimport json\nfor p in ['nipada/corpus/_cache/sources_manifest.json','nipada/corpus/_cache/sources_coverage.json','nipada/corpus/signed_corpus_v208.json']:\n    try:\n        d=json.load(open(p))\n    except Exception as e:\n        print(p,e); … [351 caractères tronqués]`

  ```
=== nipada/corpus/_cache/sources_manifest.json <class 'list'> 107
[{"id": "dn1_brahmajala", "lang": "eng", "url": "https://suttacentral.net/dn1/en/sujato", "title": "dn1_brahmajala"}, {"id": "dn2_samannaphala", "lang": "eng", "url": "https://suttacentral.net/dn2/en/sujato", "title": "dn2_samannaphala"}]

=== nipada/corpus/_cache/sources_coverage.json <class 'list'> 107
[{"id": "dn1_brahmajala", "ok": true, "words": 12773}, {"id": "dn2_samannaphala", "ok": true, "words": 12082}]

=== nipada/corpus/signed_corpus_v208.json <class 'dict'> 6
['version', 'n_signed', 'n_matched', 'n_nomatch', 'v14_atoms', 'signed']
  version "v208"
  n_signed 37
  ```

- **bash** `{"command": "cd ../Panini/research && find nipada -maxdepth 2 -type f -iname '*.json' | grep -i 'text\\|catalog\\|index\\|graph' | head -30; echo '=== graph node sample'; python3 - <<'EOF'\nimport json\np='nipada/falsification/nipada_v334_graph_v35.json'\nd=json.load(open(p))\nprint(type(d), list(d) … [233 caractères tronqués]`

  ```
nipada/corpus/INDEX_catalogs_v206z.json
nipada/corpus/INDEX_catalogs_v207a.json
nipada/corpus/catalog_african_colonial_v206x.json
nipada/corpus/catalog_buddhist_axial_v205.json
nipada/corpus/catalog_buddhist_late_antique_v206d.json
nipada/corpus/catalog_buddhist_medieval_v206i.json
nipada/corpus/catalog_chinese_axial_v206b.json
nipada/corpus/catalog_chinese_early_modern_v206s.json
nipada/corpus/catalog_chinese_late_antique_v206f.json
nipada/corpus/catalog_chinese_medieval_v206h.json
nipada/corpus/catalog_chinese_modern_v206t.json
nipada/corpus/catalog_greco_latin_axial_v206k.json
nipada/corpus/catalog_greco_latin_late_antique_v206l.json
nipada/corpus/catalog_greco_latin_medieval_v206m.json
nipada/corpus/catalog_indian_axial_v206a.json
nipada/corpus/catalog_indian_early_modern_v206q.json
nipada/corpus/catalog_indian_late_antique_v206e.json
nipada/corpus/catalog_indian_medieval_v206g.json
nipada/corpus/catalog_indian_modern_v206r.json
nipada/corpus/catalog_indigenous_american_colonial_v206x.json
nipada/corpus/catalog_islamic_medieval_v206j.json
nipada/corpus/catalog_islamic_modern_v206u.json
nipada/corpus/catalog_orientalist_translation_modern_v206c.json
nipada/corpus/catalog_south_a
… [624 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini/research && python3 - <<'EOF'\nimport json\nd=json.load(open('nipada/falsification/nipada_v334_graph_v35.json'))\nprint('nodes type',type(d['nodes']), len(d['nodes']))\nks=list(d['nodes'])[:5]\nfor k in ks: print(k, json.dumps(d['nodes'][k],ensure_ascii=False)[:600])\nprint … [281 caractères tronqués]`

  ```
nodes type <class 'dict'> 1753
epicurus_letters {"kind": "proto_atheist_work", "author": "Épicure", "year": -300, "language_original": "grc", "tradition_label": "GRECO_LAT_MATERIAL", "v14_signature": {"ÊTRE": 0.06521739130434782, "DIFFÉRENCE": 0.32608695652173914, "RAPPORT": 0.08695652173913043, "ORIENTATION": 0.021739130434782608, "SUJET": 0.06521739130434782, "TEMPS": 0.06521739130434782, "MODALITÉ": 0.2826086956521739, "NOMBRE": 0.043478260869565216, "ESPACE": 0.0, "OPÉRATION": 0.021739130434782608, "FONCTION": 0.0, "STRUCTURE": 0.0, "SYMÉTRIE": 0.021739130434782608, "ÉQUATION": 0.0}, "ingestion_status": "signed_v208", "signed_n_chars": 
lucretius_drn {"kind": "proto_atheist_work", "year": -55, "lang": "eng", "tradition_label": "ANCIENT_EPICUREAN", "author": "lucretius", "v14_signature": {"ÊTRE": 0.10994634340222575, "DIFFÉRENCE": 0.0831677265500795, "RAPPORT": 0.27091613672496023, "ORIENTATION": 0.03274046104928458, "SUJET": 0.10721383147853736, "TEMPS": 0.0587241653418124, "MODALITÉ": 0.10825715421303657, "NOMBRE": 0.0643879173290938, "ESPACE": 0.033634737678855324, "OPÉRATION": 0.015103338632750398, "FONCTION": 0.004868839427662957, "STRUCTURE": 0.027722575516693163, "SYMÉTRI
… [2113 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini/research && python3 - <<'EOF'\nimport json\np='nipada/corpus/catalog_greco_latin_axial_v206k.json'\nd=json.load(open(p))\nprint(type(d), list(d)[:10] if isinstance(d,dict) else len(d))\ns=json.dumps(d,ensure_ascii=False,indent=1)\nprint(s[:4000])\nEOF", "description": "Insp … [31 caractères tronqués]`

  ```
<class 'dict'> ['version', 'generated', 'macro_culture', 'epoch', 'n_works', 'target', 'primary_sources', 'language_original_dominant', 'schools_covered', 'works']
{
 "version": "v206k_greco_latin_axial",
 "generated": "2026-04-29",
 "macro_culture": "GRECO_LATIN",
 "epoch": "axial",
 "n_works": 70,
 "target": 70,
 "primary_sources": [
  "Perseus Digital Library (Tufts)",
  "Diels-Kranz fragments",
  "sacred-texts (Jowett, Ross)",
  "TLG fragments libres"
 ],
 "language_original_dominant": "grc (Grec ancien)",
 "schools_covered": [
  "Pré-socratiques (Milésiens, Pythagoriciens, Éléates, Atomistes, Sophistes — 15 entrées)",
  "Hippocrate (3 traités du Corpus)",
  "Platon (20 dialogues majeurs)",
  "Aristote (corpus 20 traités : Organon, Physique, De Anima, Métaphysique, 2 Éthiques, Politique, Rhétorique, Poétique)",
  "Stoïcisme ancien (Zénon Citium, Cléanthe Hymne à Zeus, Chrysippe SVF)",
  "Épicurisme (Épicure 4 textes, Philodème)",
  "Cynisme (Diogène, Cratès, Antisthène)",
  "Scepticisme (Pyrrhon, Timon Silloi)",
  "Sciences hellénistiques (Euclide, Archimède ×2, Apollonius, Aratos, Aristarque)",
  "Théophraste Caractères"
 ],
 "works": [
  {
   "id": "thales_fragments",
   "tit
… [2964 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini/research && python3 - <<'EOF'\nimport json, collections\npairs=json.load(open('nipada/falsification/pairs334_axes_v1.json'))['pairs']\ng=json.load(open('nipada/falsification/nipada_v334_graph_v35.json'))\nnodes=g['nodes']\nids=sorted({x['a'] for x in pairs}|{x['b'] for x in … [802 caractères tronqués]`

  ```
unique texts 48
sections Counter({'a': 459, 'b': 180, 'c': 16})
trads Counter({'': 199, 'BUDDHIST_AXIAL': 107, 'GRECO_PLATONIC': 56, 'FUZZY_LOGIC': 35, 'MANY_VALUED_LOGIC': 34, 'RECURSIVE_FUNCTIONS': 33, 'COMBINATORY_LOGIC': 32, 'SEMANTIC_NETWORKS': 31, 'CONCEPTUAL_DEPENDENCY': 30, 'INDIAN_AXIAL': 26, 'CHINESE_AXIAL': 25, 'CONFUCIAN_AXIAL': 24, 'ABRAHAMIC_PROPHETIC_AXIAL': 12, 'JUDEAN_APOCALYPTIC_LATE': 4, 'NORSE_EDDIC_MEDIEVAL': 3, 'RENAISSANCE_OCCULT_EARLY_MODERN': 2, 'MILLENARIAN_MODERN_PROTESTANT': 1, 'DISTRIBUTIONAL_SEMANTICS': 1})
missing in graph 0 []
fields Counter({'kind': 48, 'author': 48, 'year': 48, 'tradition_label': 48, 'title_en': 48, 'ingestion_status': 48, 'v14_signature': 45, 'tradition_micro': 41, 'language_original': 35, 'title_original': 35, 'tags': 28, 'lang': 13, 'source_type': 13, 'v14_top3': 12, 'n_words': 12, 'publisher': 8, 'relevance_score': 8, 'nipada_relation': 8, 'url': 8, 'language_version': 7, 'interprets_ref': 2, 'id': 1, 'type': 1, 'tradition': 1, 'added_in': 1})

 2_esdras {"kind": "apocalyptic_text", "author": "anonymous (Ezra apocalypse tradition)", "year": 100, "lang": "eng", "tradition_label": "JUDEAN_APOCALYPTIC_LATE", "tradition_micro": "JE
… [2480 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini/research && python3 - <<'EOF'\nimport json, collections\na=json.load(open('nipada/falsification/analytic_sigs_v1.json'))\nprint('44 sample ids', list(a)[:44])\ng=json.load(open('nipada/falsification/nipada_v334_graph_v35.json'))['nodes']\nmiss=[k for k in a if k not in g]\n … [466 caractères tronqués]`

  ```
44 sample ids ['2_esdras', 'aristotle_categories', 'aristotle_de_caelo', 'aristotle_nicomachean_ethics', 'aristotle_parts_of_animals', 'aristotle_posterior_analytics', 'aristotle_prior_analytics', 'bengio_2003', 'book_of_enoch', 'curry_1930', 'daniel_book', 'dn1_brahmajala', 'ezekiel_book', 'hosea_book', 'isaiah_book', 'jeremiah_book', 'kleene_1936', 'lukasiewicz_1920', 'mengzi', 'mikolov_2013', 'miller_evidence_prophecy', 'mn2_sabbasava', 'mn35_culasaccaka', 'nostradamus_centuries', 'plato_charmides', 'plato_gorgias', 'plato_gorgias_jowett', 'plato_laws', 'plato_meno', 'plato_meno_jowett', 'plato_phaedo', 'plato_phaedrus_jowett', 'plato_philebus_jowett', 'plato_republic_jowett', 'plato_sophist', 'plato_symposium_jowett', 'plato_theaetetus_jowett', 'qiwulun', 'quillian_1968', 'russell_parousia_1878', 'schank_1972', 'sibylline_oracles', 'voluspa', 'zechariah_book']
not in graph 0 []
2_esdras {'kind': 'apocalyptic_text', 'year': 100, 'tradition_label': 'JUDEAN_APOCALYPTIC_LATE', 'lang': 'eng', 'language_original': None, 'author': 'anonymous (Ezra apocalypse tradition)'}
aristotle_categories {'kind': 'canon_work', 'year': -340, 'tradition_label': 'GRECO_LATIN_AXIAL', 'lang': None, 'la
… [593 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini/research && python3 - <<'EOF'\nimport json, collections\npairs=json.load(open('nipada/falsification/pairs334_axes_v1.json'))['pairs']\nids={x['a'] for x in pairs}|{x['b'] for x in pairs}\na=json.load(open('nipada/falsification/analytic_sigs_v1.json'))\nprint('pair texts',le … [930 caractères tronqués]`

  ```
pair texts 48 sigs 44
sigs in pairs 44 sigs not pairs []
pairs not sigs 4 ['an7_64_kodhana', 'aristotle_de_anima', 'brahma_sutra_badarayana', 'zadeh_1965']
Counter({('ingestion_status', 'catalog_only'): 1641, ('ingestion_status', 'signed_v208'): 28, ('ingestion_status', 'signed_v295'): 22, ('ingestion_status', 'signed_v272'): 10})
graph nodes with v14 sig 57
intersection pairs/sig 12
coverage 107 ok 102
unique words positive 102
  ```

- **bash** `{"command": "cd ../Panini/research && grep -rl \"114\" --include='*.json' nipada | head -20; echo '=== files pairs'; find nipada -iname '*pair*' -type f | head -20; echo '=== reval full?'; ls -lh nipada/falsification/*334* 2>/dev/null", "description": "Find artifact listing 114 active texts"}`

  ```
nipada/corpus/_cache/sources_coverage.json
nipada/corpus/_cache/public_domain_auto/gutendex/manifest.json
nipada/corpus/catalog_greco_latin_medieval_v206m.json
nipada/corpus/catalog_indigenous_american_colonial_v206x.json
nipada/corpus/catalog_islamic_medieval_v206j.json
nipada/corpus/delta_restitution_v260.json
nipada/corpus/gap_analysis_v14_v272.json
nipada/corpus/ingestion_log_v3.json
nipada/corpus/nipada_v224_greco_latin_catalog.json
nipada/corpus/quality_audit_v273.json
nipada/corpus/references_v272_analysis.json
nipada/corpus/references_v272_analysis_clean.json
nipada/corpus/signed_corpus_v208.json
nipada/corpus/signed_corpus_v212f.json
nipada/corpus/signed_corpus_v225b_greco_latin.json
nipada/corpus/signed_corpus_v225d_greco_latin.json
nipada/corpus/signed_corpus_v225e_greco_latin_curated.json
nipada/corpus/signed_corpus_v226_islamic.json
nipada/corpus/signed_corpus_v235_suttacentral_collections.json
nipada/corpus/signed_corpus_v236_chinese_classics.json
=== files pairs
nipada/corpus/_cache/public_domain_auto/gutendex/pg224_a_pair_of_blue_eyes_en.txt
nipada/corpus/_cache/wikipedia_dump/wiki_de_maintenance_repair_and_operations.txt
nipada/corpus/_cache/wikipedia_dump/wiki_en_
… [1682 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini/research && python3 - <<'EOF'\nimport json\nfor p in ['nipada/falsification/nipada_v334_graph_v35.json','nipada/falsification/pairs334_axes_v1.json']:\n    d=json.load(open(p))\n    print(p, d.get('section'), d.get('version'))\n    if 'nodes' in d:\n        ks=list(d['nodes … [149 caractères tronqués]`

  ```
nipada/falsification/nipada_v334_graph_v35.json §334 v35
{"epicurus_letters": {"kind": "proto_atheist_work", "author": "Épicure", "year": -300, "language_original": "grc", "tradition_label": "GRECO_LAT_MATERIAL", "v14_signature": {"ÊTRE": 0.06521739130434782, "DIFFÉRENCE": 0.32608695652173914, "RAPPORT": 0.08695652173913043, "ORIENTATION": 0.021739130434782608, "SUJET": 0.06521739130434782, "TEMPS": 0.06521739130434782, "MODALITÉ": 0.2826086956521739, "NOMBRE": 0.043478260869565216, "ESPACE": 0.0, "OPÉRATION": 0.021739130434782608, "FONCTION": 0.0, "STRUCTURE": 0.0, "SYMÉTRIE": 0.021739130434782608, "ÉQUATION": 0.0}, "ingestion_status": "signed_v208", "signed_n_chars": 498}, "lucretius_drn": {"kind": "proto_atheist_work", "year": -55, "lang": "eng", "tradition_label": "ANCIENT_EPICUREAN", "author": "lucretius", "v14_signature": {"ÊTRE": 0.10994634340222575, "DIFFÉRENCE": 0.0831677265500795, "RAPPORT": 0.27091613672496023, "ORIENTATION": 0.03274046104928458, "SUJET": 0.10721383147853736, "TEMPS": 0.0587241653418124, "MODALITÉ": 0.10825715421303657, "NOMBRE": 0.0643879173290938, "ESPACE": 0.033634737678855324, "OPÉRATION": 0.015103338632750398, "FONCTION": 0.004868839427662957, "STRU
… [210 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini/research && python3 - <<'EOF'\nimport json\np='nipada/falsification/nipada_v334_graph_v35_gps.json'\nd=json.load(open(p)); print(type(d), list(d)[:20] if isinstance(d,dict) else len(d))\nfor k,v in (d.items() if isinstance(d,dict) else []):\n    print(k,type(v), len(v) if h … [79 caractères tronqués]`

  ```
<class 'dict'> ['version', 'section', 'iso_from_v34', 'nodes', 'edges']
version <class 'str'> 3
section <class 'str'> 4
iso_from_v34 <class 'list'> 2
nodes <class 'dict'> 1753
edges <class 'list'> 19967
  ```

- **bash** `{"command": "cd ../Panini/research && python3 - <<'EOF'\nimport json\npairs=json.load(open('nipada/falsification/pairs334_axes_v1.json'))['pairs']\nids=sorted({x['a'] for x in pairs}|{x['b'] for x in pairs})\ng=json.load(open('nipada/falsification/nipada_v334_graph_v35.json'))['nodes']\na=json.load( … [682 caractères tronqués]`

  ```
2_esdras                               y=   100 lang=eng  trad=JUDEAN_APOCALYPTIC_LATE      micro=JEWISH_APOCALYPTIC         sig=Y src=Y words=3733
an7_64_kodhana                         y=  -410 lang=pli  trad=BUDDHIST_AXIAL               micro=BUDDHISM_THERAVADA         sig=- src=- words=
aristotle_categories                   y=  -340 lang=grc  trad=GRECO_LATIN_AXIAL            micro=GREEK_ARISTOTELIAN         sig=Y src=Y words=17525
aristotle_de_anima                     y=  -330 lang=grc  trad=GRECO_LATIN_AXIAL            micro=GREEK_ARISTOTELIAN         sig=- src=- words=
aristotle_de_caelo                     y=  -330 lang=grc  trad=GRECO_LATIN_AXIAL            micro=GREEK_ARISTOTELIAN         sig=Y src=Y words=13559
aristotle_nicomachean_ethics           y=  -340 lang=grc  trad=GRECO_LATIN_AXIAL            micro=GREEK_ARISTOTELIAN         sig=Y src=Y words=116372
aristotle_parts_of_animals             y=  -330 lang=grc  trad=GRECO_LATIN_AXIAL            micro=GREEK_ARISTOTELIAN         sig=Y src=Y words=7548
aristotle_posterior_analytics          y=  -340 lang=grc  trad=GRECO_LATIN_AXIAL            micro=GREEK_ARISTOTELIAN         sig=Y src=Y words=941
aristotle_prior_analy
… [5931 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini/research && python3 - <<'EOF'\nimport json, itertools, math\na=json.load(open('nipada/falsification/analytic_sigs_v1.json'))\ng=json.load(open('nipada/falsification/nipada_v334_graph_v35.json'))['nodes']\n# compare to graph\ndiff=[]\nfor k,s in a.items():\n    gs=g[k].get(' … [788 caractères tronqués]`

  ```
sig diffs vs graph 44 [('2_esdras', 'nosig'), ('aristotle_categories', 'nosig'), ('aristotle_de_caelo', 'nosig'), ('aristotle_nicomachean_ethics', 'nosig'), ('aristotle_parts_of_animals', 'nosig')]
n 44
(1.0, 'plato_gorgias', 'plato_gorgias_jowett')
(0.9999999999999999, 'plato_meno', 'plato_meno_jowett')
(0.9999271312622623, 'isaiah_book', 'jeremiah_book')
(0.9997440683484348, 'hosea_book', 'zechariah_book')
(0.9994263052204031, 'ezekiel_book', 'jeremiah_book')
(0.9992608327633645, 'plato_phaedrus_jowett', 'plato_symposium_jowett')
(0.9992308266234078, 'daniel_book', 'zechariah_book')
(0.9992119908437811, 'ezekiel_book', 'isaiah_book')
(0.9990258661413429, 'daniel_book', 'hosea_book')
(0.9986759029278653, 'plato_laws', 'plato_republic_jowett')
(0.9984542027302212, 'plato_gorgias_jowett', 'plato_republic_jowett')
(0.9984542027302212, 'plato_gorgias', 'plato_republic_jowett')
multi-author {'aristotle': ['aristotle_categories', 'aristotle_de_caelo', 'aristotle_nicomachean_ethics', 'aristotle_parts_of_animals', 'aristotle_posterior_analytics', 'aristotle_prior_analytics'], 'anonymous_sangha': ['dn1_brahmajala', 'mn2_sabbasava', 'mn35_culasaccaka'], 'plato': ['plato_charmides', 'plato_g
… [264 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini/research && python3 - <<'EOF'\nimport json, math, statistics\npairs=json.load(open('nipada/falsification/pairs334_axes_v1.json'))['pairs']\na=json.load(open('nipada/falsification/analytic_sigs_v1.json'))\nkeys=sorted(a)\ndef l2(x,y): return math.sqrt(sum((x[k]-y[k])**2 for  … [1281 caractères tronqués]`

  ```
pairs both sig 490
l2 d_lex r= 0.4751 maxdiff 0.5067
l2 d_H r= 0.4547 maxdiff 1.1134
l2 cos r= -0.4312 maxdiff 0.9998

cos d_lex r= -0.4173 maxdiff 0.9912
cos d_H r= -0.3961 maxdiff 0.9828
cos cos r= 0.3709 maxdiff 0.8609

hell d_lex r= 0.4742 maxdiff 0.483
hell d_H r= 0.4605 maxdiff 1.0898
hell cos r= -0.4296 maxdiff 0.9998

js d_lex r= 0.4755 maxdiff 0.4594
js d_H r= 0.4616 maxdiff 1.0661
js cos r= -0.4309 maxdiff 0.9998

sample d_lex, cos, l2
0.3387 0.7493 0.1127 0.2507
0.2514 0.8086 0.135 0.1914
0.1968 0.8396 0.1179 0.1604
0.2192 0.7962 0.1241 0.2038
0.2373 0.763 0.0499 0.237
  ```

- **bash** `{"command": "sed -n '1,220p' docs/theorie/genealogie-des-langues.md", "description": "Read genealogy theory doc"}`

  ```
# La généalogie des langues, des dialectes et des styles

> **Ce que cette page est.** La **théorie** de la structure généalogique qui doit organiser l'**étage
> entrée-sortie** (nom historique : « couche commune ») de Drave, et ce que les projets complémentaires
> **Panini** et **Nipada** ont établi sur elle. Les **mesures** sont dans
> [`reports/07-mesures-couche-commune.md`](../../reports/07-mesures-couche-commune.md), dans
> [`reports/rapport-corpus-commun.md`](../../reports/rapport-corpus-commun.md),
> [`reports/rapport-retrieval-epoque.md`](../../reports/rapport-retrieval-epoque.md) et, pour la
> confrontation des deux faces, dans
> [`reports/rapport-genealogie-deux-faces.md`](../../reports/rapport-genealogie-deux-faces.md).
> *À relire et à mettre à jour à chaque cycle : Panini et Nipada sont des sources vivantes.*

## 1. Pourquoi une généalogie

Une couche entrée-sortie ne peut pas être « riche en langues » au sens d'une **liste**. Les langues forment
une **structure** : des familles, des branches, des dialectes, des styles, et des **traductions** qui
traversent tout cela. Si la structure est réelle, elle doit se voir dans les états du modèle — et si elle
ne s'y voit pas, c
… [9943 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '180,380p' reports/rapport-retrieval-epoque.md; echo '=== JSON keys'; python3 - <<'EOF'\nimport json\nd=json.load(open('reports/retrieval-epoque.json'))\nprint(json.dumps(d,ensure_ascii=False,indent=1)[:3000])\nEOF", "description": "Read rest of prior report and JSON schema"}`

  ```
groupes sont identiques : 0,710 vs 0,710.** C'est un **effet de composition** (Simpson) : l'époque n'est pas
la variable qui explique le classement brut, c'est l'écriture.

**Les contrastes appariés.** On fixe la paire de langues et on ne change que la date du pivot :

- **pivot anglais** (KJV 1769 → WEB 2000), cibles de même écriture (OST, SPA, LSG, LUT, POR, PCM) :
  Δ moyen **+0,52 point**, IC 95 % **[−2,9 ; +4,3]**. Les effets par cible ne sont pas monotones :
  **PCM +8,7** (p < 0,001), **POR +2,7** (p = 0,024), mais **SPA −3,6**, **LUT −4,9** (p < 0,001).
- **pivot français** (OST 1744 → LSG 1910), cibles de même écriture (KJV, SPA, LUT, WEB, POR, PCM) :
  Δ moyen **+0,52 point**, IC 95 % **[−1,2 ; +1,9]**. Positifs : **LUT +2,6**, **KJV +2,1**,
  **WEB +1,6** ; négatif : **POR −3,2**.

**Le 2×2 anglais × français.** Quatre cellules, même paire de langues, dates croisées :

| | Ostervald 1744 | Segond 1910 |
|---|---:|---:|
| **KJV 1769** | 0,971 | 0,970 |
| **WEB 2000** | 0,976 | 0,967 |

Interaction **(WEB−LSG) − (WEB−OST) − (KJV−LSG) + (KJV−OST)** = **−0,008** : aucune. À écriture et famille
contrôlées, 231 ans d'écart ne déplacent pas le retrieval.

**La régression des 13
… [10272 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,200p' docs/methode/resultats.md; echo '=== portes'; sed -n '1,160p' docs/methode/portes.md", "description": "Read result and gate conventions"}`

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
… [7643 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' reports/rapport-retrieval-familles.md; echo '=== journal latest'; ls journal/2026-11-14; sed -n '1,80p' journal/2026-11-14/README.md", "description": "Read retrieve families report and latest journal"}`

  ```
# J7.1 — Le retrieval approfondi par famille Glottolog

> **Ligne de roadmap** : R0.7 (le bloc langue) / L · **Chantier** : Panini, J7.1 · **Date** : 2026-11-14
> **Verdict** : ✅ **le retrieval retrouve la famille, mais seulement dans la même écriture — et il faut
> des sœurs pour le voir.** Sur les 532 textes UDHR (445 langues distinctes après déduplication, 1948),
> le top-1 de voisinage est de la même famille dans **66,1 %** des cas (hasard 10,3 %) et de la même
> branche (sœur) dans **26,1 %** (hasard 2,5 %). Mais **hors écriture, tout retombe au hasard** :
> famille 9,9 % contre 8,1 %, sœur 0,7 % contre 0,8 %. Dans la même écriture, la famille monte à
> **69,8 %** (hasard 16,2 %) et la sœur à **27,8 %** (hasard 5,7 %). Le retrieval parallèle 30 articles
> le confirme et le chiffre : sur les **25 langues LANG_TREE** disponibles, les sœurs valent **0,619**
> (60 paires), les mêmes familles d'une autre branche **0,170** (216), les familles différentes
> **0,0445** (324) — **13,9×**, Δ **+0,574** [0,490 ; 0,655], coefficient de sœur **+0,448**
> (p = 0,002) contre +0,213 pour l'écriture. Sur l'**échantillon 20**, le même contraste est **nul** :
> sœurs 0,0583 (12 paires) contre 0,
… [13480 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport sys\nprint(sys.version)\nfor m in ('numpy','scipy','sklearn','pandas'):\n    try:\n        x=__import__(m); print(m, x.__version__)\n    except Exception as e: print(m,'NO',e)\nEOF", "description": "Check Python scientific stack"}`

  ```
3.13.16 (main, Oct 16 2026, 19:23:15) [GCC]
numpy 2.5.3
scipy 1.18.1
sklearn NO No module named 'sklearn'
pandas NO No module named 'pandas'
  ```

- **bash** `{"command": "sed -n '1,160p' tools/retrieval_familles.py", "description": "Read prior tool conventions"}`

  ```
#!/usr/bin/env python3
"""retrieval_familles.py — J7.1 : le retrieval approfondi par famille Glottolog.

LA QUESTION. J3.1 a mesuré le retrieval de surface sur 21 langues UDHR (30 articles, 1948) :
top-1 0,049, écriture +0,062, famille +0,056, R² 0,14. J3.2 a montré que, sur ces 21 langues,
le signal de famille vit dans 2-3 paires et que les paires hors écriture sont exactement au hasard.
J7.1 demande d'aller plus loin : utiliser les **532 langues UDHR de Panini** (même source XML,
article 1), mesurer le retrieval **par famille Glottolog** sur les **29 langues de
`language_genealogy.py`** et sur l'**échantillon 20** du corpus commun, avec le **contrôle
d'époque**, et comparer à J3.1.

LE DISPOSITIF, EN DEUX TEMPS.
  1. **Global 532** (article 1, 1948) : chaque langue est une requête ; on classe les 440 autres
     langues (une par code ISO, les variantes d'une même langue sont dédupliquées) par similarité
     de surface. On regarde si le top-1 est de la même famille, de la même branche (sœur), ou d'une
     autre famille. C'est un retrieval de **voisinage généalogique**, pas un retrieval parallèle.
  2. **Parallèle 30 articles** (les 29 langues de LANG_TREE + l'échantillon 20) : p
… [6337 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini/research && python3 - <<'EOF'\nimport json,collections\npairs=json.load(open('nipada/falsification/pairs334_axes_v1.json'))['pairs']\nblank=[p for p in pairs if not p['trad_a'] or not p['trad_b']]\nprint('blank pairs',len(blank))\nfor p in blank[:5]: print(p)\nprint(collect … [322 caractères tronqués]`

  ```
blank pairs 442
{'section': 'a', 'a': 'dn1_brahmajala', 'b': 'plato_gorgias', 'd_topo': 5.869999999999999, 'd_lex': 0.23731611871356678, 'd_H': 0.4354771113182558, 'cos': 0.7629578768099119, 'trad_a': 'BUDDHIST_AXIAL', 'trad_b': '', 'lang_a': 'eng', 'lang_b': '', 'same_comp': True}
{'section': 'a', 'a': 'dn1_brahmajala', 'b': 'plato_meno', 'd_topo': 5.869999999999999, 'd_lex': 0.2384437732350959, 'd_H': 0.4031699514295756, 'cos': 0.7658006252153536, 'trad_a': 'BUDDHIST_AXIAL', 'trad_b': '', 'lang_a': 'eng', 'lang_b': '', 'same_comp': True}
{'section': 'a', 'a': 'dn1_brahmajala', 'b': 'plato_phaedo', 'd_topo': 5.85, 'd_lex': 0.16377727871936493, 'd_H': 0.3051956609199528, 'cos': 0.8923290470146422, 'trad_a': 'BUDDHIST_AXIAL', 'trad_b': '', 'lang_a': 'eng', 'lang_b': '', 'same_comp': True}
{'section': 'a', 'a': 'dn1_brahmajala', 'b': 'plato_sophist', 'd_topo': 6.63, 'd_lex': 0.2750656656059483, 'd_H': 0.43072937698545044, 'cos': 0.7102702969166068, 'trad_a': 'BUDDHIST_AXIAL', 'trad_b': '', 'lang_a': 'eng', 'lang_b': '', 'same_comp': True}
{'section': 'a', 'a': 'dn1_brahmajala', 'b': 'plato_laws', 'd_topo': 4.83, 'd_lex': 0.24093133794533642, 'd_H': 0.446523257470176, 'cos': 0.7486957
… [626 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini/research && python3 - <<'EOF'\nimport json,collections\na=json.load(open('nipada/falsification/analytic_sigs_v1.json'))\ng=json.load(open('nipada/falsification/nipada_v334_graph_v35.json'))['nodes']\nfor k in sorted(a):\n    n=g[k]\n    print(f\"{k:34s} {n.get('tradition_la … [202 caractères tronqués]`

  ```
2_esdras                           JUDEAN_APOCALYPTIC_LATE          JEWISH_APOCALYPTIC           anonymous (Ezra apocalypse tradition)
aristotle_categories               GRECO_LATIN_AXIAL                GREEK_ARISTOTELIAN           aristotle
aristotle_de_caelo                 GRECO_LATIN_AXIAL                GREEK_ARISTOTELIAN           aristotle
aristotle_nicomachean_ethics       GRECO_LATIN_AXIAL                GREEK_ARISTOTELIAN           aristotle
aristotle_parts_of_animals         GRECO_LATIN_AXIAL                GREEK_ARISTOTELIAN           aristotle
aristotle_posterior_analytics      GRECO_LATIN_AXIAL                GREEK_ARISTOTELIAN           aristotle
aristotle_prior_analytics          GRECO_LATIN_AXIAL                GREEK_ARISTOTELIAN           aristotle
bengio_2003                        NEURAL_LANGUAGE_MODELS           DISTRIBUTED_REPRESENTATIONS  Yoshua Bengio
book_of_enoch                      JUDEAN_APOCALYPTIC_LATE          JEWISH_APOCALYPTIC           anonymous (R.H. Charles trans. 1913)
curry_1930                         COMBINATORY_LOGIC                COMBINATORS                  Haskell B. Curry
daniel_book                        ABRAHAMIC_PROPHETIC_AXIAL    
… [4333 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"0,138\\|0.138\\|0,049\\|0.049\\|β\\|beta\\|régression\\|regression\" reports/rapport-genealogie-deux-faces.md | head -50; sed -n '1,120p' reports/rapport-genealogie-deux-faces.md", "description": "Read genealogy two faces report for beta context"}`

  ```
92:   (0,133). Une même valeur de distance recouvre des réalités opposées ; la régression linéaire sur cette
107:| **toutes** | 210 | **0,1510** | 0,0494 | — |
147:### 3.3 Les régressions : le script d'abord, la distance ensuite
281:1. **La surface passe avant la filiation, des deux côtés.** Panini : β époque 0,1378 > β filiation 0,0489.
287:3. **Un signal de filiation résiduel est détectable quand la surface est contrôlée.** Panini : β filiation
331:| 3 | **Distance Panini continue, étendue aux 21** | LANG_TREE couvre 5/21 ; 200/210 paires « inconnues » | étendre LANG_TREE ou apprendre une distance continue sur Glottolog, refaire la régression sur 210 paires | comparer à la distance discrète : si le R² ne bouge pas, le gain est nul |
363:| [`genealogie-deux-faces.json`](genealogie-deux-faces.json) | tous les chiffres : 210 paires, groupes, régressions, permutations, LOO, ACP, §150 |
# J3.2 — La généalogie à deux faces : Panini et Glottolog sur le corpus commun

> **Ligne de roadmap** : R0.7 (le bloc langue) / L · **Chantier** : semaine Panini, J3.2 · **Date** : 2026-11-07
> **Verdict** : ✅ **la confrontation est faite, et elle déplace la question.** Les deux faces ne mesurent
> **
… [8082 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '200,330p' reports/rapport-genealogie-deux-faces.md", "description": "Read ACP 44 works section"}`

  ```
4. **Leave-one-language-out** : le coefficient reste négatif dans les 21 retraits, mais varie de −0,296 à
   −0,103 (P2) et de −0,294 à −0,100 (G) : la **direction** est robuste, la **taille** ne l'est pas.
5. **Décomposition de l'inconnu** : voir § 3.4 — le gain apparent de P2 sur toutes les paires disparaît
   quand on sépare la couverture de la distance.

## 4. La face « atomes » — 14 atomes, 9 dhātus, et pourquoi ce n'est pas une généalogie

### 4.1 Ce que les signatures V14 disent d'elles-mêmes

Sur les **44 œuvres** de `analytic_sigs_v1.json` (14 parts normalisées, somme 1), l'ACP sur la **matrice
de corrélation des parts CLR** (la convention de J2.1) donne :

| composante | valeur propre | variance | cumul |
|---:|---:|---:|---:|
| 1 | 6,967 | 49,76 % | 49,76 % |
| 2 | 2,845 | 20,32 % | 70,08 % |
| 3 | 1,491 | 10,65 % | **80,73 %** |
| 4 | 1,260 | 9,00 % | 89,73 % |
| 5 | 0,528 | 3,77 % | 93,51 % |
| 6 | 0,381 | 2,72 % | 96,23 % |

**4 composantes > 1** ; **3 composantes pour 80 %** ; **5 pour 90 %** ; **6 pour 95 %**. Sur la
**covariance** des parts CLR (sans standardiser), il n'y a plus qu'**une** composante > 1 (52,63 % de la
variance). Le « 4 dimensions effectives » dépe
… [7705 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini/research && python3 - <<'EOF'\nimport json, math, itertools, statistics\nimport numpy as np\nfrom scipy import stats\npairs=json.load(open('nipada/falsification/pairs334_axes_v1.json'))['pairs']\ng=json.load(open('nipada/falsification/nipada_v334_graph_v35.json'))['nodes']\ … [3827 caractères tronqués]`

  ```
top pairs by cos:
1.0 plato_gorgias plato_gorgias_jowett 5 False False
1.0 plato_meno plato_meno_jowett 0 False False
0.9999 isaiah_book jeremiah_book 100 True False
0.9997 hosea_book zechariah_book 230 True False
0.9994 ezekiel_book jeremiah_book 10 True False
0.9993 plato_phaedrus_jowett plato_symposium_jowett 15 True True
0.9992 daniel_book zechariah_book 355 True False
0.9992 ezekiel_book isaiah_book 110 True False
0.999 daniel_book hosea_book 585 True False
0.9987 plato_laws plato_republic_jowett 30 False False

excl_dup False same_trad 0.3409090909090909 same_author 0.1590909090909091 mean dy 235.52272727272728 med 45.0 <=50 0.5681818181818182 <=100 0.7272727272727273

excl_dup True same_trad 0.38636363636363635 same_author 0.20454545454545456 mean dy 233.5909090909091 med 36.0 <=50 0.5909090909090909 <=100 0.7045454545454546
chance same trad 0.11416490486257928 author 0.05708245243128964

all pairs 946 cos vs dy spearman SignificanceResult(statistic=np.float64(-0.25084840199505165), pvalue=np.float64(4.851231334907442e-15)) pearson PearsonRResult(statistic=np.float64(-0.07024337082939233), pvalue=np.float64(0.030749787807467004))
cos same trad 0.9736946770213519 diff 0.93279
… [729 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini/research && python3 - <<'EOF'\nimport json, itertools, numpy as np, random\nfrom scipy import stats\npairs=json.load(open('nipada/falsification/pairs334_axes_v1.json'))['pairs']\ng=json.load(open('nipada/falsification/nipada_v334_graph_v35.json'))['nodes']\nsigs=json.load(o … [3671 caractères tronqués]`

  ```
same_trad logdy w [-3.102 -1.809] AUC 0.899
same_trad cos w [-2.709  1.701] AUC 0.791
same_trad logdy+cos w [-3.267 -1.566  0.932] AUC 0.921

near50 logdy w [ -902.982 -1054.131] AUC 1.0
near50 cos w [-1.506  1.173] AUC 0.751
near50 logdy+cos w [-9.016040e+02 -1.052752e+03 -4.450000e-01] AUC 1.0

near100 logdy w [-257.304 -519.104] AUC 1.0
near100 cos w [-0.854  0.924] AUC 0.725
near100 logdy+cos w [-247.094 -503.768   -3.311] AUC 1.0

within same trad: cos vs dy SignificanceResult(statistic=np.float64(0.23572256233350422), pvalue=np.float64(0.014052900354271947))
within diff trad: cos vs dy SignificanceResult(statistic=np.float64(-0.12609740568233602), pvalue=np.float64(0.0002527430051140432))
bin 0 50 n 197 st 81 cos same 0.97 diff 0.964
bin 50 150 n 151 st 17 cos same 0.98 diff 0.939
bin 150 300 n 124 st 4 cos same 0.997 diff 0.901
bin 300 1000 n 110 st 6 cos same 0.991 diff 0.913
bin 1000 3000 n 364 st 0 cos same None diff 0.937
same trad obs 0.3409090909090909 null mean 0.299625 p 0.3145
mean dy obs 235.52272727272728 null 251.24375 p 0.0405
near50 obs 0.5681818181818182 null 0.56625 p 0.571
[stderr]
<stdin>:18: RuntimeWarning: overflow encountered in exp
<stdin>:27: RuntimeWa
… [34 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini/research && python3 - <<'EOF'\nimport json, numpy as np\nfrom scipy import stats\npairs=json.load(open('nipada/falsification/pairs334_axes_v1.json'))['pairs']\ng=json.load(open('nipada/falsification/nipada_v334_graph_v35.json'))['nodes']\nfor p in pairs:\n    p['ya']=g[p['a … [2232 caractères tronqués]`

  ```
d_lex dist [0.00879223 0.11068179 0.16107309 0.35690188 0.69470867]
H0 (array([0.05297106, 0.07623309]), np.float64(0.9091387033097751))
epoch (array([0.22424192, 0.07661285]), np.float64(0.27362514407034166))
joint (array([ 0.22424192,  0.14222686, -0.00451862]), np.float64(0.909780817992272))
trad (array([ 0.25909636, -0.14179912]), np.float64(0.17376812863626068))
joint+trad (array([ 0.22670696,  0.14090217, -0.00534994, -0.01002861]), np.float64(0.9104773956413585))
reverse dtopo~dy (array([2.24667339, 1.04496767]), np.float64(0.3253984262616535))
corr dtopo^0.67 dy SignificanceResult(statistic=np.float64(0.6014901641964561), pvalue=np.float64(1.0825574727598524e-65)) pearson PearsonRResult(statistic=np.float64(0.5704370484651698), pvalue=np.float64(8.331157182668692e-58))
corr dlex dy SignificanceResult(statistic=np.float64(0.627931622679699), pvalue=np.float64(4.0080161487861414e-73)) pearson PearsonRResult(statistic=np.float64(0.523091907861651), pvalue=np.float64(2.7733101260942387e-47))
corr dlex dtopo SignificanceResult(statistic=np.float64(0.9022842965767428), pvalue=np.float64(8.822923576507062e-241)) pearson PearsonRResult(statistic=np.float64(0.9522034742108616), pval
… [570 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini/research && python3 - <<'EOF'\nimport json, numpy as np\nfrom scipy import stats\ng=json.load(open('nipada/falsification/nipada_v334_graph_v35.json'))['nodes']\nsigs=json.load(open('nipada/falsification/analytic_sigs_v1.json'))\nids=sorted(sigs); n=len(ids); atoms=list(sigs … [2072 caractères tronqués]`

  ```
cos ~ st (array([0.93279912, 0.04089555]), np.float64(0.05556239060584245))
cos ~ logdy (array([ 0.96777114, -0.00536991]), np.float64(0.03686735317235912))
cos ~ st+logdy (array([ 0.9337744 ,  0.03235286, -0.00562263]), np.float64(0.06352327576990646))
cos ~ st+logdy+inter (array([ 0.93409335,  0.05850118, -0.00746144,  0.02150412]), np.float64(0.07262916092616223))
R2 st 0.05556239060584245 dy 0.03686735317235912 joint 0.06352327576990646 partial st 0.02767627354897212 partial dy 0.008429233529963722
bin 0 50 n 197 diff 0.00607 same n 81 diff n 116
bin 50 150 n 151 diff 0.04036 same n 17 diff n 134
bin 150 300 n 124 diff 0.09601 same n 4 diff n 120
bin 300 1000 n 110 diff 0.07709 same n 6 diff n 104
cos ~ same_author+logdy (array([ 0.93619131,  0.02236502, -0.00825287]), np.float64(0.04391143925103547))
dup pairs 3 [('isaiah_book', 'jeremiah_book'), ('plato_gorgias', 'plato_gorgias_jowett'), ('plato_meno', 'plato_meno_jowett')]
dup same trad 0.3333333333333333 same author 0.0
no dup: cos same trad 0.973449513897605 diff 0.9326383548661454 n 943
no dup cos~st+logdy (array([ 0.93355667,  0.03271793, -0.00525249]), np.float64(0.06199394532932445))
  ```

- **bash** `{"command": "cd ../Panini/research && python3 - <<'EOF'\nimport json, numpy as np, collections\npairs=json.load(open('nipada/falsification/pairs334_axes_v1.json'))['pairs']\ng=json.load(open('nipada/falsification/nipada_v334_graph_v35.json'))['nodes']\nrows=[]\nfor p in pairs:\n    ya,yb=g[p['a']][' … [690 caractères tronqués]`

  ```
same trad n 161 max dy 230 p95 60.0
(230, True, 'ABRAHAMIC_PROPHETIC_AXIAL', 'ABRAHAMIC_PROPHETIC_AXIAL', 'zechariah_book', 'hosea_book', 0.1614090331208263)
(180, True, 'ABRAHAMIC_PROPHETIC_AXIAL', 'ABRAHAMIC_PROPHETIC_AXIAL', 'isaiah_book', 'zechariah_book', 0.13139739624893637)
(160, True, 'ABRAHAMIC_PROPHETIC_AXIAL', 'ABRAHAMIC_PROPHETIC_AXIAL', 'ezekiel_book', 'hosea_book', 0.1438617995681967)
(150, True, 'ABRAHAMIC_PROPHETIC_AXIAL', 'ABRAHAMIC_PROPHETIC_AXIAL', 'jeremiah_book', 'hosea_book', 0.13365532130820676)
(110, True, 'ABRAHAMIC_PROPHETIC_AXIAL', 'ABRAHAMIC_PROPHETIC_AXIAL', 'isaiah_book', 'ezekiel_book', 0.131250651956476)
(100, True, 'ABRAHAMIC_PROPHETIC_AXIAL', 'ABRAHAMIC_PROPHETIC_AXIAL', 'isaiah_book', 'jeremiah_book', 0.08483776593003847)
(80, True, 'ABRAHAMIC_PROPHETIC_AXIAL', 'ABRAHAMIC_PROPHETIC_AXIAL', 'jeremiah_book', 'zechariah_book', 0.16290084086032214)
(70, True, 'ABRAHAMIC_PROPHETIC_AXIAL', 'ABRAHAMIC_PROPHETIC_AXIAL', 'ezekiel_book', 'zechariah_book', 0.12254728979459316)
(60, True, 'GRECO_LATIN_AXIAL', 'GRECO_LATIN_AXIAL', 'plato_charmides', 'aristotle_parts_of_animals', 0.11876185459565711)
(60, True, 'GRECO_LATIN_AXIAL', 'GRECO_LATIN_AXIAL', 'plato_c
… [910 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini/research && python3 - <<'EOF'\nimport json, numpy as np\nfrom scipy import stats\ng=json.load(open('nipada/falsification/nipada_v334_graph_v35.json'))['nodes']\nsigs=json.load(open('nipada/falsification/analytic_sigs_v1.json'))\nids=sorted(sigs); n=len(ids); atoms=list(sigs … [3848 caractères tronqués]`

  ```
fams Counter({'GRECO': 19, 'ABRAHAMIC': 8, 'COGNITIVE_SCIENCE': 4, 'FORMAL_LOGIC': 3, 'BUDDHIST': 3, 'CHINESE': 2, 'MILLENARIAN': 2, 'RENAISSANCE_OCCULT_EARLY_MODERN': 1, 'CLASSICAL_ORACULAR': 1, 'NORSE_EDDIC_MEDIEVAL': 1})
auths [('plato', 13), ('aristotle', 6), ('anonymous_sangha', 3), ('anonymous (Ezra apocalypse tradition)', 1), ('Yoshua Bengio', 1), ('anonymous (R.H. Charles trans. 1913)', 1), ('Haskell B. Curry', 1), ('anonymous (Daniel tradition)', 1), ('Ezekiel ben Buzi (attributed)', 1), ('Hosea ben Beeri (attributed)', 1), ('Isaiah ben Amoz (attributed)', 1), ('Jeremiah ben Hilkiah (attributed)', 1), ('Stephen C. Kleene', 1), ('Jan Łukasiewicz', 1), ('mencius', 1), ('Tomáš Mikolov', 1), ('William Miller', 1), ('Michel de Nostredame (Nostradamus)', 1), ('anonymous', 1), ('M. Ross Quillian', 1), ('James Stuart Russell', 1), ('Roger C. Schank', 1), ('anonymous (Milton S. Terry trans. 1899)', 1), ('anonymous (Bellows trans. 1936)', 1), ('Zechariah ben Berechiah (attributed)', 1)]
fam n 213 cos same 0.969262782424029 diff 0.9282288091815627
 cos~L+logdy (array([0.92743794, 0.04454649, 0.00214322]), np.float64(0.0973028266986421))
 cos~L (array([0.92822881, 0.04103397]), np.flo
… [913 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini/research && python3 - <<'EOF'\nimport json,collections\npairs=json.load(open('nipada/falsification/pairs334_axes_v1.json'))['pairs']\nids={x['a'] for x in pairs}|{x['b'] for x in pairs}\nsigs=json.load(open('nipada/falsification/analytic_sigs_v1.json'))\ncov={x['id']:x for  … [859 caractères tronqués]`

  ```
sig coverage 44 / 44
sig manifest 44 /44
sig unique urls 26
sig langs Counter({'eng': 24, '': 19, 'fra': 1})
all coverage ok 102 / 107
all unique urls 72
all langs Counter({'eng': 71, '': 30, 'en': 2, 'grc': 2, 'ara': 1, 'fra': 1})
missing an7_64_kodhana sig False
missing aristotle_de_anima sig False
missing brahma_sutra_badarayana sig False
  ```

- **bash** `{"command": "cd ../Panini/research && python3 - <<'EOF'\nimport json\nman={x['id']:x for x in json.load(open('nipada/corpus/_cache/sources_manifest.json'))}\nfor i in ['plato_gorgias','plato_gorgias_jowett','aristotle_categories','dn1_brahmajala','mengzi','lukasiewicz_1920','book_of_enoch','voluspa' … [192 caractères tronqués]`

  ```
plato_gorgias {'id': 'plato_gorgias', 'lang': '', 'url': '', 'title': 'plato_gorgias'}
plato_gorgias_jowett {'id': 'plato_gorgias_jowett', 'lang': '', 'url': '', 'title': ''}
aristotle_categories {'id': 'aristotle_categories', 'lang': '', 'url': '', 'title': 'aristotle_categories'}
dn1_brahmajala {'id': 'dn1_brahmajala', 'lang': 'eng', 'url': 'https://suttacentral.net/dn1/en/sujato', 'title': 'dn1_brahmajala'}
mengzi {'id': 'mengzi', 'lang': 'eng', 'url': '', 'title': ''}
lukasiewicz_1920 {'id': 'lukasiewicz_1920', 'lang': 'eng', 'url': 'https://scholar.google.com/scholar?q=Lukasiewicz+1920+trivalent+logic', 'title': 'lukasiewicz_1920'}
book_of_enoch {'id': 'book_of_enoch', 'lang': 'eng', 'url': 'https://www.sacred-texts.com/bib/boe/index.htm', 'title': 'book_of_enoch'}
voluspa {'id': 'voluspa', 'lang': 'eng', 'url': 'https://www.sacred-texts.com/neu/poe/poe03.htm', 'title': 'voluspa'}
sibylline_oracles {'id': 'sibylline_oracles', 'lang': 'eng', 'url': 'https://www.sacred-texts.com/cla/sib/index.htm', 'title': 'sibylline_oracles'}
2_esdras {'id': '2_esdras', 'lang': 'eng', 'url': 'https://www.sacred-texts.com/bib/poly/es2.htm', 'title': '2_esdras'}
qiwulun {'id': 'qiwulun', 'lang':
… [389 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini/research && python3 - <<'EOF'\nimport json\nman=json.load(open('nipada/corpus/_cache/sources_manifest.json'))\nurls=[m['url'] for m in man]\nprint('entries',len(man),'nonempty',sum(bool(u) for u in urls),'unique nonempty',len({u for u in urls if u}),'blank',sum(not u for u  … [221 caractères tronqués]`

  ```
entries 107 nonempty 80 unique nonempty 71 blank 27
sig nonempty url 25
  ```

- **bash** `{"command": "date -Iseconds; git log -1 --format='%ci %h %s'", "description": "Check current date and HEAD date"}`

  ```
2026-11-14T05:15:33-05:00
2026-11-14 05:05:58 -0500 febfdfff J11.4 — SCHÉMA v2 DOCUMENTÉ : 4 CHAMPS PARTITION + 10 CHAMPS ALTERNATIVE, 6 CAS / 0 ÉCHEC, LES DEUX VERSIONS LUES (612 v2 + 612 v1)
  ```

- **bash** `{"command": "cd ../Panini/research && python3 - <<'EOF'\nimport json, numpy as np\ng=json.load(open('nipada/falsification/nipada_v334_graph_v35.json'))['nodes']\nsigs=json.load(open('nipada/falsification/analytic_sigs_v1.json'))\nids=sorted(sigs); n=len(ids); atoms=list(sigs[ids[0]])\nX=np.array([[s … [2928 caractères tronqués]`

  ```
k 1 MAE 235.4090909090909 R2 0.6135852637380077 r 0.8181794316220083
k 3 MAE 322.6666666666667 R2 0.6298860168627372 r 0.7977124311241203
k 5 MAE 430.3136363636364 R2 0.45268395271907746 r 0.6784413216387183
obs 235.4090909090909 null 269.9615340909091 16.736683323445313 p 0.008
global null 940.1274090909092 156.89148206485334 p 0.0
res std 121.78371269357909 range -321.875 528.125
res MAE 55.70828349282295 R2 0.04176725737595954 r 0.3908912614776748
res null 81.81704076953747 p 0.033
  ```

- **bash** `{"command": "cd ../Panini/research && python3 - <<'EOF'\nimport json, numpy as np, collections\ng=json.load(open('nipada/falsification/nipada_v334_graph_v35.json'))['nodes']\nsigs=json.load(open('nipada/falsification/analytic_sigs_v1.json'))\nids=sorted(sigs); n=len(ids); atoms=list(sigs[ids[0]])\nX … [2431 caractères tronqués]`

  ```
obs acc 0.6136363636363636 bal 0.306140350877193 majority 0.4318181818181818
bins Counter({np.int64(2): 24, np.int64(8): 7, np.int64(1): 5, np.int64(3): 3, np.int64(9): 2, np.int64(7): 2, np.int64(4): 1})
null 0.4998090909090909 0.06089691805090939 p 0.0472
global null 0.22470909090909091 0.06819725643399423 p 0.0
Counter({'GRECO': 19, 'ABRAHAMIC': 8, 'COGNITIVE_SCIENCE': 4, 'FORMAL_LOGIC': 3, 'BUDDHIST': 3, 'CHINESE': 2, 'MILLENARIAN': 2, 'RENAISSANCE_OCCULT_EARLY_MODERN': 1, 'CLASSICAL_ORACULAR': 1, 'NORSE_EDDIC_MEDIEVAL': 1})
ABRAHAMIC 8 Counter({'ABRAHAMIC': 6, 'CLASSICAL_ORACULAR': 1, 'GRECO': 1})
BUDDHIST 3 Counter({'GRECO': 3})
CHINESE 2 Counter({'GRECO': 1, 'FORMAL_LOGIC': 1})
CLASSICAL_ORACULAR 1 Counter({'FORMAL_LOGIC': 1})
COGNITIVE_SCIENCE 4 Counter({'FORMAL_LOGIC': 2, 'GRECO': 1, 'COGNITIVE_SCIENCE': 1})
FORMAL_LOGIC 3 Counter({'FORMAL_LOGIC': 2, 'COGNITIVE_SCIENCE': 1})
GRECO 19 Counter({'GRECO': 17, 'ABRAHAMIC': 1, 'BUDDHIST': 1})
MILLENARIAN 2 Counter({'MILLENARIAN': 1, 'RENAISSANCE_OCCULT_EARLY_MODERN': 1})
NORSE_EDDIC_MEDIEVAL 1 Counter({'RENAISSANCE_OCCULT_EARLY_MODERN': 1})
RENAISSANCE_OCCULT_EARLY_MODERN 1 Counter({'MILLENARIAN': 1})
  ```

- **bash** `{"command": "cd ../Panini/research && python3 - <<'EOF'\nimport json, numpy as np\npairs=json.load(open('nipada/falsification/pairs334_axes_v1.json'))['pairs']\ng=json.load(open('nipada/falsification/nipada_v334_graph_v35.json'))['nodes']\nids=sorted({p['a'] for p in pairs}|{p['b'] for p in pairs}); … [2117 caractères tronqués]`

  ```
obs r2 joint 0.909780817992272
date perm p 0.2725 null mean 0.9096965774072351
st 282
obs fam coef -0.013335187240547275 perm p 0.934 null -0.0017179287383187992
H0 obs 0.9091387033097751 perm p 0.0
  ```

- **bash** `{"command": "cd ../Panini/research && find . -name 'nipada_v150_validation.json' -o -name '*v150*' | head -20", "description": "Locate Panini v150 validation artifact"}`

  ```
./nipada/falsification/nipada_v150_validation.json
  ```

- **bash** `{"command": "cd ../Panini/research && python3 - <<'EOF'\nimport json\nd=json.load(open('nipada/falsification/nipada_v150_validation.json'))\nprint(json.dumps(d,ensure_ascii=False,indent=1)[:6000])\nEOF", "description": "Inspect v150 validation regression"}`

  ```
{
 "version": "v150",
 "step": "§150 — validation prédictive Phase B révisée (composite)",
 "H1_stratification": {
  "median_d_graph": 0.6694,
  "n_strong_transmission": 17,
  "n_weak_transmission": 12,
  "mean_dsig_strong": 0.3403,
  "mean_dsig_weak": 0.3727,
  "expected": "mean_dsig_strong < mean_dsig_weak (signature plus proche si héritage fort)",
  "u_stat": 94.0,
  "p_value_two_tailed": 0.7232,
  "verdict": "KO"
 },
 "H2_loocv_tradition": {
  "baseline_majority_acc": 0.3,
  "acc_full_signature": 0.4,
  "acc_reflexion_signature": 0.2,
  "delta_full_vs_baseline": 0.1,
  "delta_refl_vs_baseline": -0.1,
  "delta_refl_vs_full": -0.2,
  "verdict": "KO",
  "loocv_full": {
   "accuracy": 0.4,
   "n": 10,
   "n_correct": 4,
   "confusion": {
    "GRECO_LAT_MATERIAL": {
     "GRECO_LAT_MATERIAL": 2,
     "CHINESE_MATERIAL": 1
    },
    "SCEPT": {
     "ISLAMIC_RATIONALIST": 1
    },
    "INDIAN_MATERIAL": {
     "CHINESE_MATERIAL": 1
    },
    "CHINESE_MATERIAL": {
     "INDIAN_MATERIAL": 1
    },
    "ISLAMIC_RATIONALIST": {
     "SCEPT": 1
    },
    "MODERN_WESTERN": {
     "INDIAN_MATERIAL": 1,
     "MODERN_WESTERN": 2
    }
   },
   "detail": [
    {
     "work": "democritus_frag
… [4795 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini/research && grep -n \"0.1378\\|0.0489\\|0.3004\\|beta\\|r2\" nipada/falsification/nipada_v150_validation.json | head -40", "description": "Find beta regression values in v150 JSON"}`

  ```
362:      "beta": [
364:        0.0489,
365:        0.1378,
368:      "r2": 0.3004
371:      "beta": [
377:      "r2": 0.0128
  ```

- **bash** `{"command": "cd ../Panini/research && sed -n '330,400p' nipada/falsification/nipada_v150_validation.json", "description": "Read regression block of v150 validation"}`

  ```
"GRECO_LAT_MATERIAL": 0.4844,
            "INDIAN_MATERIAL": 0.4896,
            "ISLAMIC_RATIONALIST": 0.5382,
            "MODERN_WESTERN": 0.3175,
            "SCEPT": 0.5986
          }
        },
        {
          "work": "feuerbach_wesen",
          "true": "MODERN_WESTERN",
          "pred": "MODERN_WESTERN",
          "ok": true,
          "scores": {
            "CHINESE_MATERIAL": 0.0105,
            "GRECO_LAT_MATERIAL": 0.4708,
            "INDIAN_MATERIAL": 0.5263,
            "ISLAMIC_RATIONALIST": 0.4544,
            "MODERN_WESTERN": 0.5551,
            "SCEPT": 0.0861
          }
        }
      ]
    }
  },
  "H3_ols_regression": {
    "features": [
      "intercept",
      "d_graph",
      "dyear_per_1000y",
      "same_tradition"
    ],
    "ols_dsig": {
      "beta": [
        0.1594,
        0.0489,
        0.1378,
        0.0022
      ],
      "r2": 0.3004
    },
    "ols_drefl": {
      "beta": [
        0.7014,
        -0.0279,
        -0.0365,
        -0.1114
      ],
      "r2": 0.0128
    },
    "interpretation_dsig": "d_sig ≈ +0.159 +0.049·d_graph +0.138·(Δyear/1000) +0.002·same_trad  (R²=0.300)",
    "verdict": "OK"
  },
  "verdict": {
    "H1_strong
… [475 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini/research && python3 - <<'EOF'\nimport json,numpy as np\npairs=json.load(open('nipada/falsification/pairs334_axes_v1.json'))['pairs']\ng=json.load(open('nipada/falsification/nipada_v334_graph_v35.json'))['nodes']\ndef fam(t):\n    if t in ('GRECO_LATIN_AXIAL','GRECO_PLATONIC … [2204 caractères tronqués]`

  ```
raw v150-like (array([ 0.11519464,  0.03009625, -0.00553801, -0.02881134]), np.float64(0.911897693666116))
std (array([ 0.22424192,  0.13364535, -0.00561195, -0.01426597]), np.float64(0.9118976936661161))
sig L2 mean 0.11028828680057376
490 raw v150-like (array([ 0.11024875,  0.03017229, -0.00492953, -0.02942126]), np.float64(0.90100626117472))
490 std (array([ 0.20176743,  0.11667916, -0.00494571, -0.01469298]), np.float64(0.90100626117472))
  ```

- **bash** `{"command": "cd ../Panini/research && python3 - <<'EOF'\nimport json,numpy as np\nfrom scipy import stats\npairs=json.load(open('nipada/falsification/pairs334_axes_v1.json'))['pairs']\ng=json.load(open('nipada/falsification/nipada_v334_graph_v35.json'))['nodes']\nsigs=json.load(open('nipada/falsific … [1841 caractères tronqués]`

  ```
n 490 d_sig mean 0.08199728787538357
raw (array([ 0.0906991 ,  0.00293316, -0.00636391, -0.0316864 ]), np.float64(0.2497391573987866))
std (array([ 0.08199729,  0.01134282, -0.00638479, -0.01582419]), np.float64(0.2497391573987866))
corr d_sig dy SignificanceResult(statistic=np.float64(0.3601836034379295), pvalue=np.float64(1.8643870088861926e-16)) d_sig dtopo SignificanceResult(statistic=np.float64(0.4650130467069152), pvalue=np.float64(1.1693643571091867e-27))
date only (array([0.0760276 , 0.00902729]), np.float64(0.04489539903653461)) topo only (array([0.06493099, 0.00473417]), np.float64(0.18344206747393366))
1-cos raw (array([ 0.05282778,  0.04434666,  0.01129652, -0.0362525 ]), np.float64(0.9012753844368))
1-cos std (array([ 0.20292576,  0.17149281,  0.01133359, -0.01810449]), np.float64(0.9012753844368))
  ```

- **todo_write** `{"todos": [{"content": "Auditer les artefacts §334 (114/655/48/44/102) et les signatures 14 flottants", "status": "completed"}, {"content": "Écrire tools/panini_334.py : retrieval, prédiction, contrôles de date/surface, permutations", "status": "in_progress"}, {"content": "Exécuter, vérifier les chi … [338 caractères tronqués]`

  ```
Updated todo list: 4 pending, 1 in progress, 1 completed.
  ```

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/panini_334.py", "content": "#!/usr/bin/env python3\n\"\"\"panini_334.py — J12.1 : le corpus §334 et les signatures des 44 œuvres.\n\nLA QUESTION. Panini/Nipada ont mesuré que leur signature lexicale capte l'époque\n(β +0,138) bien  … [60260 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/panini_334.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "python3 tools/panini_334.py --rapide --sortie /tmp/panini-334-test.json 2>&1 | tail -40", "description": "Run Panini analysis in fast mode"}`

  ```
J12.1 — Panini §334 et 44 signatures
audit : {'corpus_actif_officiel': 114, 'paires': 655, 'textes_distincts_paires': 48, 'textes_absents_des_paires': 66, 'oeuvres_signees': 44, 'sources_ok': 102, 'sources_manifeste': 107, 'sources_ok_parmi_44': 44, 'urls_uniques_non_vides': 71}
paires : H0 R2=0.909139 | date R2=0.2736 | partiel date|topo=0.0071 | partiel topo|date=0.8758
œuvres : top1 tradition=0.614 (hasard 0.224, p_bins=0.0419) | top1 proche50=0.568 (hasard 0.228, p_trad=0.0080)
prédiction : MAE année=235.4 (R2=0.614, null dans tradition=268.6) | résidu within-tradition R2=0.042 p=0.0259
écrit : /tmp/panini-334-test.json
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('tools/panini_334.py')\ns=p.read_text()\n# Remove unused vals in bins_retrieval\ns=s.replace('''        # paires de la tranche\n        idx = np.where(m)[0]\n        vals_t, vals_d = [], []\n        for ii in idx:\n            for jj i … [4925 caractères tronqués]`

  ```
patched
OK
  ```

- **bash** `{"command": "python3 tools/panini_334.py --rapide --sortie /tmp/panini-334-test.json 2>&1 | tail -30", "description": "Re-run fast after patch"}`

  ```
J12.1 — Panini §334 et 44 signatures
audit : {'corpus_actif_officiel': 114, 'paires': 655, 'textes_distincts_paires': 48, 'textes_absents_des_paires': 66, 'oeuvres_signees': 44, 'sources_ok': 102, 'sources_manifeste': 107, 'sources_ok_parmi_44': 44, 'urls_uniques_non_vides': 71}
paires : H0 R2=0.909139 | date R2=0.2736 | partiel date|topo=0.0071 | partiel topo|date=0.8758
œuvres : top1 tradition=0.614 (hasard 0.224, p_bins=0.0679) | top1 proche50=0.568 (hasard 0.228, p_trad=0.3473)
prédiction : MAE année=235.4 (R2=0.614, null dans tradition=269.0) | résidu within-tradition R2=0.042 p=0.0319
écrit : /tmp/panini-334-test.json
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('/tmp/panini-334-test.json'))\nprint('top keys',list(d))\nprint('audit lang',d['audit']['langues_source_44'])\nprint('surface eng',json.dumps(d['oeuvres']['surface_eng'],ensure_ascii=False,indent=1))\nprint('sans doublons',json.dumps(d['o … [651 caractères tronqués]`

  ```
top keys ['tache', 'titre', 'date', 'graine', 'sources', 'audit', 'paires', 'oeuvres', 'synthese', 'limites']
audit lang {'eng': 24, 'inconnu': 19, 'fra': 1}
surface eng {
 "n_paires": 276,
 "n_oeuvres": 24,
 "beta": [
  0.9181624807204023,
  0.023973506780526493,
  8.690030235760603e-06
 ],
 "r2": 0.016435598409120455,
 "top1_tradition_dans_eng": 0.5,
 "top1_proche50_dans_eng": 0.375,
 "n_requetes": 24
}
sans doublons {
 "n_candidats_retires": 6,
 "retrieval": {
  "top1_meme_tradition": 0.6136363636363636,
  "top1_meme_auteur": 0.36363636363636365,
  "top1_proche_50ans": 0.5909090909090909,
  "chance_meme_tradition": 0.22299406020336254,
  "chance_meme_auteur": 0.09991946038457668,
  "chance_proche_50ans": 0.2281787979462398
 }
}
bootstrap {
 "n_demandes": 300,
 "n_valides": 300,
 "top1_meme_tradition": {
  "moyenne": 0.5916448140738432,
  "ic95": [
   0.44626436781609197,
   0.7407407407407407
  ]
 },
 "top1_meme_auteur": {
  "moyenne": 0.32741663731040954,
  "ic95": [
   0.17848020434227332,
   0.46001602564102556
  ]
 },
 "top1_proche_50ans": {
  "moyenne": 0.5249453951033154,
  "ic95": [
   0.36172727272727273,
   0.6666666666666666
  ]
 },
 "beta_tradition": {
  "moyenne": 0.
… [4551 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('/tmp/panini-334-test.json'))\nprint('perm paires',json.dumps(d['paires']['permutations'],ensure_ascii=False,indent=1))\nprint('positivite',json.dumps(d['paires']['positivite'],ensure_ascii=False,indent=1))\nprint('bins date tail',json.du … [558 caractères tronqués]`

  ```
perm paires {
 "n": 500,
 "date": {
  "r2_date_seule_observe": 0.27362514407034166,
  "r2_date_seule_null_moyen": 0.012021263680403883,
  "p_date_seule": 0.001996007984031936,
  "partiel_date_apres_topo_observe": 0.00706697687449957,
  "partiel_date_apres_topo_null_moyen": 0.005746973806338484,
  "p_partiel_date_apres_topo": 0.908183632734531,
  "coef_date_joint_observe": -0.000445908702320863,
  "coef_date_joint_null_moyen": 4.231894807302755e-05,
  "p_coef_date_joint": 0.1437125748502994,
  "r2_inverse_observe": 0.3253984262616535,
  "r2_inverse_null_moyen": 0.011311335428570704,
  "p_inverse": 0.001996007984031936
 },
 "tradition": {
  "delta_observe": -0.1914987369744145,
  "delta_null_moyen": -0.007495441445160007,
  "p_delta": 0.001996007984031936,
  "partiel_tradition_apres_topo_observe": 0.012865779353342247,
  "partiel_tradition_apres_topo_null_moyen": 0.005273783017200004,
  "p_partiel_tradition_apres_topo": 0.1277445109780439
 },
 "H0": {
  "r2_observe": 0.9091387033097751,
  "r2_null_moyen": 0.0016237911467302853,
  "p_h0": 0.001996007984031936
 }
}
positivite {
 "n_meme_tradition": 282,
 "n_tradition_differente": 373,
 "dy_meme_tradition": {
  "moyenne": 28.00709219858
… [4031 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini/research && python3 - <<'EOF'\nimport json,collections\npairs=json.load(open('nipada/falsification/pairs334_axes_v1.json'))['pairs']\ng=json.load(open('nipada/falsification/nipada_v334_graph_v35.json'))['nodes']\nids=sorted({p['a'] for p in pairs}|{p['b'] for p in pairs})\n … [256 caractères tronqués]`

  ```
2_esdras                              100 bin4 JUDEAN_APOCALYPTIC_LATE
an7_64_kodhana                       -410 bin2 BUDDHIST_AXIAL
aristotle_categories                 -340 bin2 GRECO_LATIN_AXIAL
aristotle_de_anima                   -330 bin2 GRECO_LATIN_AXIAL
aristotle_de_caelo                   -330 bin2 GRECO_LATIN_AXIAL
aristotle_nicomachean_ethics         -340 bin2 GRECO_LATIN_AXIAL
aristotle_parts_of_animals           -330 bin2 GRECO_LATIN_AXIAL
aristotle_posterior_analytics        -340 bin2 GRECO_LATIN_AXIAL
aristotle_prior_analytics            -340 bin2 GRECO_LATIN_AXIAL
bengio_2003                          2003 bin9 NEURAL_LANGUAGE_MODELS
book_of_enoch                        -200 bin3 JUDEAN_APOCALYPTIC_LATE
brahma_sutra_badarayana              -300 bin2 INDIAN_AXIAL
curry_1930                           1930 bin8 COMBINATORY_LOGIC
daniel_book                          -165 bin3 ABRAHAMIC_PROPHETIC_AXIAL
dn1_brahmajala                       -440 bin2 BUDDHIST_AXIAL
ezekiel_book                         -590 bin1 ABRAHAMIC_PROPHETIC_AXIAL
hosea_book                           -750 bin1 ABRAHAMIC_PROPHETIC_AXIAL
isaiah_book                          -700 bin1 ABRAHAMIC_PROPHETI
… [1987 caractères tronqués]
  ```

- **bash** `{"command": "cd ../Panini/research && python3 - <<'EOF'\nimport json,numpy as np,collections\npairs=json.load(open('nipada/falsification/pairs334_axes_v1.json'))['pairs']\ng=json.load(open('nipada/falsification/nipada_v334_graph_v35.json'))['nodes']\nman={x['id']:x for x in json.load(open('nipada/co … [2921 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 17, in <module>
KeyError: <function b at 0x7fe31bc8d260>
[exit code: 1]
  ```

- **bash** `{"command": "cd ../Panini/research && python3 - <<'EOF'\nimport json,numpy as np,collections\npairs=json.load(open('nipada/falsification/pairs334_axes_v1.json'))['pairs']\ng=json.load(open('nipada/falsification/nipada_v334_graph_v35.json'))['nodes']\nman={x['id']:x for x in json.load(open('nipada/co … [2677 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 17, in <module>
NameError: name 'b' is not defined
[exit code: 1]
  ```

- **bash** `{"command": "cd ../Panini/research && python3 - <<'EOF'\nimport json,numpy as np,collections\npairs=json.load(open('nipada/falsification/pairs334_axes_v1.json'))['pairs']\ng=json.load(open('nipada/falsification/nipada_v334_graph_v35.json'))['nodes']\nman={x['id']:x for x in json.load(open('nipada/co … [2689 caractères tronqués]`

  ```
all n 655 same 282 diff 373 dlex same 0.115 diff 0.307 delta -0.191
   same mem [('plato_gorgias', 22), ('plato_meno', 21), ('plato_phaedo', 20), ('plato_sophist', 19), ('plato_laws', 18)] [('aristotle_parts_of_animals', 31), ('aristotle_nicomachean_ethics', 28), ('aristotle_posterior_analytics', 28), ('aristotle_de_anima', 27), ('aristotle_categories', 26)]
same bin2 n 437 same 262 diff 175 dlex same 0.108 diff 0.275 delta -0.167
   same mem [('plato_gorgias', 22), ('plato_meno', 21), ('plato_phaedo', 20), ('plato_sophist', 19), ('plato_laws', 18)] [('aristotle_parts_of_animals', 31), ('aristotle_nicomachean_ethics', 28), ('aristotle_posterior_analytics', 28), ('aristotle_de_anima', 27), ('aristotle_categories', 26)]
bin2 eng-eng n 21 same 7 diff 14 dlex same 0.255 diff 0.309 delta -0.054
   same mem [('dn1_brahmajala', 3), ('mn2_sabbasava', 2), ('mn35_culasaccaka', 1), ('qiwulun', 1)] [('an7_64_kodhana', 3), ('mn35_culasaccaka', 2), ('mn2_sabbasava', 1), ('mengzi', 1)]
bin2 same lang n 21 same 7 diff 14 dlex same 0.255 diff 0.309 delta -0.054
   same mem [('dn1_brahmajala', 3), ('mn2_sabbasava', 2), ('mn35_culasaccaka', 1), ('qiwulun', 1)] [('an7_64_kodhana', 3), ('mn35_culasacca
… [458 caractères tronqués]
  ```

- **bash** `{"command": "time python3 tools/panini_334.py --sortie reports/panini-334.json 2>&1 | tail -30", "description": "Run full Panini analysis", "timeoutMs": 600000}`

  ```
J12.1 — Panini §334 et 44 signatures
audit : {'corpus_actif_officiel': 114, 'paires': 655, 'textes_distincts_paires': 48, 'textes_absents_des_paires': 66, 'oeuvres_signees': 44, 'sources_ok': 102, 'sources_manifeste': 107, 'sources_ok_parmi_44': 44, 'urls_uniques_non_vides': 71}
paires : H0 R2=0.909139 | date R2=0.2736 | partiel date|topo=0.0071 | partiel topo|date=0.8758
œuvres : top1 tradition=0.614 (hasard 0.224, p_bins=0.0492) | top1 proche50=0.568 (hasard 0.228, p_trad=0.3579)
prédiction : MAE année=235.4 (R2=0.614, null dans tradition=269.6) | résidu within-tradition R2=0.042 p=0.0322
écrit : reports/panini-334.json
[stderr]

real	1m8,989s
user	1m11,857s
sys	0m0,361s
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/panini-334.json'))\nprint(json.dumps(d['synthese'],ensure_ascii=False,indent=1))\nprint('\\nperm paires',json.dumps(d['paires']['permutations'],ensure_ascii=False,indent=1))\nprint('\\nretrieval nulls',json.dumps(d['oeuvres']['re … [1015 caractères tronqués]`

  ```
{
 "audit": {
  "corpus_actif_officiel": 114,
  "paires": 655,
  "textes_distincts_paires": 48,
  "textes_absents_des_paires": 66,
  "oeuvres_signees": 44,
  "sources_ok": 102,
  "sources_manifeste": 107,
  "sources_ok_parmi_44": 44,
  "urls_uniques_non_vides": 71
 },
 "paires": {
  "r2_h0": 0.9091387033097751,
  "r2_date": 0.27362514407034166,
  "partiel_topo_apres_date": 0.8757952849396747,
  "partiel_date_apres_topo": 0.00706697687449957,
  "beta_date_joint": -0.000445908702320863,
  "n_meme_tradition": 282,
  "dy_moyen_meme_tradition": 28.00709219858156,
  "dy_moyen_tradition_differente": 1172.053619302949
 },
 "oeuvres": {
  "top1_meme_tradition": 0.6136363636363636,
  "chance_meme_tradition": 0.22390013087687508,
  "top1_meme_auteur": 0.36363636363636365,
  "chance_meme_auteur": 0.09991946038457668,
  "top1_proche_50ans": 0.5681818181818182,
  "chance_proche_50ans": 0.22815362931642003,
  "p_top1_tradition_bins": 0.04919016196760648,
  "p_top1_proche_tradition": 0.35792841431713657,
  "top1_proche_null_date": 0.5384954545454546,
  "top1_tradition_null_bins": 0.5000090909090908,
  "mae_annee_knn1": 235.4090909090909,
  "r2_annee_knn1": 0.6135852637380077,
  "mae_annee_null_dan
… [6402 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('tools/panini_334.py')\ns=p.read_text()\n# 1. Fix bin labels\nold='''NOMS_BINS = [\n    \"< -500\", \"-500..-250\", \"-250..0\", \"0..250\", \"250..500\",\n    \"500..1000\", \"1000..1800\", \"1800..2000\", \"2000..2020\", \"> 2020\",\ … [2476 caractères tronqués]`

  ```
patched 1
OK
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('tools/panini_334.py')\ns=p.read_text()\n# Add date+surface contrast before \"return {\" of analyser_paires\nold='''    return {\n        \"n_paires\": int(len(d_lex)),\n        \"n_textes\": int(len(ids_paires)),\n        \"modeles\": … [5269 caractères tronqués]`

  ```
patched 2
OK
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('tools/panini_334.py')\ns=p.read_text()\nold='''def synthese(audit, paires, oeuvres):\n    return {'''\nnew='''def synthese(audit, paires, oeuvres):\n    tests = [\n        (\"retrieval_filiation\", \"top1 même tradition > null à date  … [1461 caractères tronqués]`

  ```
patched 3
OK
J12.1 — Panini §334 et 44 signatures
audit : {'corpus_actif_officiel': 114, 'paires': 655, 'textes_distincts_paires': 48, 'textes_absents_des_paires': 66, 'oeuvres_signees': 44, 'sources_ok': 102, 'sources_manifeste': 107, 'sources_ok_parmi_44': 44, 'urls_uniques_non_vides': 71}
paires : H0 R2=0.909139 | date R2=0.2736 | partiel date|topo=0.0071 | partiel topo|date=0.8758
œuvres : top1 tradition=0.614 (hasard 0.224, p_bins=0.0659) | top1 proche50=0.568 (hasard 0.228, p_trad=0.3273)
prédiction : MAE année=235.4 (R2=0.614, null dans tradition=269.6) | résidu within-tradition R2=0.042 p=0.0359
écrit : /tmp/panini-334-test2.json
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('/tmp/panini-334-test2.json'))\nprint(json.dumps(d['oeuvres']['v150'],ensure_ascii=False,indent=1))\nprint(json.dumps(d['paires']['contraste_date_surface'],ensure_ascii=False,indent=1))\nprint(json.dumps(d['synthese']['tests_principaux'], … [285 caractères tronqués]`

  ```
{
 "n_paires": 374,
 "formule": "d_sig(L2 V14) ~ 1 + d_topo + Δannée/1000 + même_tradition",
 "beta_brut": [
  0.09062586335944518,
  0.002705890923622122,
  -0.005954476978865826,
  -0.036616557785975265
 ],
 "beta_standardise": [
  0.368972089316387,
  0.26423958399548,
  -0.14801197147188613,
  -0.8789526204097384
 ],
 "r2": 0.30916874198922484,
 "publie_v150": {
  "beta": [
   0.1594,
   0.0489,
   0.1378,
   0.0022
  ],
  "r2": 0.3004,
  "formule": "d_sig ~ 1 + d_graph + Δyear/1000 + même_tradition"
 },
 "lecture": "le coefficient de date reconstruit est négatif et non significatif ; le +0,138 publié n'est pas reproduit sur les 44 signatures du §334"
}
{
 "bin_axial": {
  "n": 437,
  "n_meme_tradition": 262,
  "n_tradition_differente": 175,
  "d_lex_meme_tradition": 0.10846805407998446,
  "d_lex_tradition_differente": 0.27519027856471745,
  "delta": -0.166722224484733,
  "cos_panini_meme_tradition": 0.9417728552741907,
  "cos_panini_tradition_differente": 0.7132249350591444
 },
 "bin_axial_meme_langue": {
  "n": 21,
  "n_meme_tradition": 7,
  "n_tradition_differente": 14,
  "d_lex_meme_tradition": 0.254956457822126,
  "d_lex_tradition_differente": 0.30869554391192205,
  "delta
… [2054 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\npairs=json.load(open('../Panini/research/nipada/falsification/pairs334_axes_v1.json'))['pairs']\nsigs=json.load(open('../Panini/research/nipada/falsification/analytic_sigs_v1.json'))\nids=sorted(sigs)\ … [342 caractères tronqués]`

  ```
572 [('2_esdras', 'aristotle_categories'), ('2_esdras', 'aristotle_de_caelo'), ('2_esdras', 'aristotle_nicomachean_ethics'), ('2_esdras', 'aristotle_parts_of_animals'), ('2_esdras', 'aristotle_posterior_analytics'), ('2_esdras', 'aristotle_prior_analytics'), ('2_esdras', 'bengio_2003'), ('2_esdras', 'book_of_enoch'), ('2_esdras', 'curry_1930'), ('2_esdras', 'daniel_book'), ('2_esdras', 'dn1_brahmajala'), ('2_esdras', 'ezekiel_book'), ('2_esdras', 'hosea_book'), ('2_esdras', 'isaiah_book'), ('2_esdras', 'jeremiah_book'), ('2_esdras', 'kleene_1936'), ('2_esdras', 'lukasiewicz_1920'), ('2_esdras', 'mengzi'), ('2_esdras', 'mikolov_2013'), ('2_esdras', 'mn2_sabbasava')]
pair both sig 490
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\npairs=json.load(open('../Panini/research/nipada/falsification/pairs334_axes_v1.json'))['pairs']\nsigs=json.load(open('../Panini/research/nipada/falsification/analytic_sigs_v1.json'))\nids=sorted(sigs); … [452 caractères tronqués]`

  ```
44 374
490
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json,collections\npairs=json.load(open('../Panini/research/nipada/falsification/pairs334_axes_v1.json'))['pairs']\nsigs=json.load(open('../Panini/research/nipada/falsification/analytic_sigs_v1.json'))\nuniq= … [653 caractères tronqués]`

  ```
rows 655 unique unordered 495 duplicated rows 160
duplicate multiplicities Counter({1: 355, 2: 130, 4: 10})
top duplicates [(('aristotle_de_anima', 'aristotle_nicomachean_ethics'), 4), (('aristotle_categories', 'aristotle_nicomachean_ethics'), 4), (('aristotle_nicomachean_ethics', 'aristotle_posterior_analytics'), 4), (('aristotle_nicomachean_ethics', 'aristotle_parts_of_animals'), 4), (('aristotle_categories', 'aristotle_de_anima'), 4), (('aristotle_de_anima', 'aristotle_posterior_analytics'), 4), (('aristotle_de_anima', 'aristotle_parts_of_animals'), 4), (('aristotle_categories', 'aristotle_posterior_analytics'), 4), (('aristotle_categories', 'aristotle_parts_of_animals'), 4), (('aristotle_parts_of_animals', 'aristotle_posterior_analytics'), 4)]
sig rows 490 sig unique 380 dups 110
sig mult Counter({1: 282, 2: 92, 4: 6})
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json,numpy as np,collections\npairs=json.load(open('../Panini/research/nipada/falsification/pairs334_axes_v1.json'))['pairs']\ng=json.load(open('../Panini/research/nipada/falsification/nipada_v334_graph_v35. … [1634 caractères tronqués]`

  ```
unique 495
H0 (array([0.0552535 , 0.07529863]), np.float64(0.9080623043144012))
date (array([0.17763372, 0.00745317]), np.float64(0.2633662532725236))
joint (array([ 0.05537726,  0.07682487, -0.00049814]), np.float64(0.9088656981205444))
trad (array([ 0.30655662, -0.19322575]), np.float64(0.3818149705925621))
same n 187 diff 308 dy same 27.6096256684492 diff 1189.1915584415585
Counter({'a': 329, 'b': 150, 'c': 16})
a 329 (array([0.05735934, 0.07412727]), np.float64(0.8944447871859046))
b 150 (array([0.0189997 , 0.08286745]), np.float64(0.8962048938642984))
c 16 (array([0.14505016, 0.05981158]), np.float64(0.32398677502903384))
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json,collections\npairs=json.load(open('../Panini/research/nipada/falsification/pairs334_axes_v1.json'))['pairs']\nsigs=json.load(open('../Panini/research/nipada/falsification/analytic_sigs_v1.json'))\nids=s … [456 caractères tronqués]`

  ```
unique sig pairs 380
missing from uniq 572 [('2_esdras', 'aristotle_categories'), ('2_esdras', 'aristotle_de_caelo'), ('2_esdras', 'aristotle_nicomachean_ethics'), ('2_esdras', 'aristotle_parts_of_animals'), ('2_esdras', 'aristotle_posterior_analytics'), ('2_esdras', 'aristotle_prior_analytics'), ('2_esdras', 'bengio_2003'), ('2_esdras', 'book_of_enoch'), ('2_esdras', 'curry_1930'), ('2_esdras', 'daniel_book')]
all 44 pairs 946
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\npairs=json.load(open('../Panini/research/nipada/falsification/pairs334_axes_v1.json'))['pairs']\nsigs=json.load(open('../Panini/research/nipada/falsification/analytic_sigs_v1.json'))\nids=sorted(sigs)\ … [521 caractères tronqués]`

  ```
374 983
uniq not lookup [] 0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\npairs=json.load(open('../Panini/research/nipada/falsification/pairs334_axes_v1.json'))['pairs']\nsigs=json.load(open('../Panini/research/nipada/falsification/analytic_sigs_v1.json'))\nids=sorted(sigs); … [574 caractères tronqués]`

  ```
44 374 572 [('2_esdras', 'aristotle_categories'), ('2_esdras', 'aristotle_de_caelo'), ('2_esdras', 'aristotle_nicomachean_ethics'), ('2_esdras', 'aristotle_parts_of_animals'), ('2_esdras', 'aristotle_posterior_analytics'), ('2_esdras', 'aristotle_prior_analytics'), ('2_esdras', 'bengio_2003'), ('2_esdras', 'book_of_enoch'), ('2_esdras', 'curry_1930'), ('2_esdras', 'daniel_book')]
uniq 380 cnt set 374
in uniq not cnt [('aristotle_de_caelo', 'aristotle_de_caelo'), ('aristotle_parts_of_animals', 'aristotle_parts_of_animals'), ('aristotle_categories', 'aristotle_categories'), ('aristotle_nicomachean_ethics', 'aristotle_nicomachean_ethics'), ('aristotle_posterior_analytics', 'aristotle_posterior_analytics'), ('aristotle_prior_analytics', 'aristotle_prior_analytics')]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json,collections\npairs=json.load(open('../Panini/research/nipada/falsification/pairs334_axes_v1.json'))['pairs']\nselfp=[p for p in pairs if p['a']==p['b']]\nprint('self rows',len(selfp))\nfor p in selfp: p … [187 caractères tronqués]`

  ```
self rows 7
{'section': 'a', 'a': 'aristotle_prior_analytics', 'b': 'aristotle_prior_analytics', 'd_topo': 0.0, 'd_lex': 0.020398064939621086, 'd_H': 0.03188335689578322, 'cos': 0.9988485935228805, 'trad_a': '', 'trad_b': '', 'lang_a': '', 'lang_b': 'eng', 'same_comp': True}
{'section': 'a', 'a': 'aristotle_nicomachean_ethics', 'b': 'aristotle_nicomachean_ethics', 'd_topo': 0.0, 'd_lex': 0.015474724076131373, 'd_H': 0.028141478996642242, 'cos': 0.9988252045293309, 'trad_a': '', 'trad_b': '', 'lang_a': '', 'lang_b': 'eng', 'same_comp': True}
{'section': 'a', 'a': 'aristotle_de_anima', 'b': 'aristotle_de_anima', 'd_topo': 0.0, 'd_lex': 0.018417622549696814, 'd_H': 0.02680957725980074, 'cos': 0.9984793586074322, 'trad_a': '', 'trad_b': '', 'lang_a': '', 'lang_b': 'eng', 'same_comp': True}
{'section': 'a', 'a': 'aristotle_categories', 'b': 'aristotle_categories', 'd_topo': 0.0, 'd_lex': 0.022063886936528197, 'd_H': 0.040791081054353286, 'cos': 0.998102139203775, 'trad_a': '', 'trad_b': '', 'lang_a': '', 'lang_b': 'eng', 'same_comp': True}
{'section': 'a', 'a': 'aristotle_posterior_analytics', 'b': 'aristotle_posterior_analytics', 'd_topo': 0.0, 'd_lex': 0.009141241444754642, 'd_H': 0.0
… [1272 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json,numpy as np\npairs=json.load(open('../Panini/research/nipada/falsification/pairs334_axes_v1.json'))['pairs']\ng=json.load(open('../Panini/research/nipada/falsification/nipada_v334_graph_v35.json'))['nod … [1392 caractères tronqués]`

  ```
unique non-self 488
H0 (array([0.0567295 , 0.07492235]), np.float64(0.9063069849629749))
date (array([0.18119035, 0.00729171]), np.float64(0.2578757779988474))
joint (array([ 0.05685834,  0.07645342, -0.0005001 ]), np.float64(0.9071415066021324))
trad (array([ 0.30655662, -0.18941592]), np.float64(0.369213449647362))
same 180 diff 308
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('tools/panini_334.py')\ns=p.read_text()\nold='''def analyser_paires(paires, textes, ids_paires, n_perm=2000, n_boot=1000, graine=0):\n    idx = {tid: i for i, tid in enumerate(ids_paires)}\n    annees = np.array([textes[t][\"annee\"] f … [3316 caractères tronqués]`

  ```
patched 4
OK
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('tools/panini_334.py')\ns=p.read_text()\ns=s.replace('''            \"sources_ok_parmi_44\": audit[\"sources_ok_parmi_44\"],\n            \"urls_uniques_non_vides\": audit[\"urls_uniques_non_vides\"],\n        },\n        \"paires\": { … [937 caractères tronqués]`

  ```
patched 5
OK
J12.1 — Panini §334 et 44 signatures
audit : {'corpus_actif_officiel': 114, 'paires': 655, 'textes_distincts_paires': 48, 'textes_absents_des_paires': 66, 'oeuvres_signees': 44, 'sources_ok': 102, 'sources_manifeste': 107, 'sources_ok_parmi_44': 44, 'urls_uniques_non_vides': 71, 'paires_uniques': 495, 'paires_auto': 7, 'paires_doublons_lignes': 160, 'paires_inference': 488}
paires : H0 R2=0.906307 | date R2=0.2579 | partiel date|topo=0.0089 | partiel topo|date=0.8749
œuvres : top1 tradition=0.614 (hasard 0.224, p_bins=0.0639) | top1 proche50=0.568 (hasard 0.228, p_trad=0.3373)
prédiction : MAE année=235.4 (R2=0.614, null dans tradition=269.8) | résidu within-tradition R2=0.042 p=0.0339
écrit : /tmp/panini-334-test3.json
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('/tmp/panini-334-test3.json'))\nprint(d['paires']['n_paires'],d['paires']['n_paires_officielles'],d['paires']['n_paires_uniques'],d['paires']['n_auto_paires'],d['paires']['n_doublons_lignes'])\nprint(json.dumps(d['paires']['modeles']['H0' … [403 caractères tronqués]`

  ```
488 655 495 7 160
{
 "formule": "d_lex ~ 1 + d_topo^0.67",
 "beta": [
  0.05672950123098694,
  0.07492234540968082
 ],
 "r2": 0.9063069849629749,
 "n": 488,
 "n_officiel": 655,
 "r2_655_lignes": 0.9091387033097751,
 "officiel_r2": 0.909139,
 "ecart_officiel_655": 2.966902249434966e-07,
 "ecart_officiel_488": 0.0028320150370251262
}
v150 n 374
{
 "bin_axial": {
  "n": 300,
  "n_meme_tradition": 160,
  "n_tradition_differente": 140,
  "d_lex_meme_tradition": 0.10637741483783078,
  "d_lex_tradition_differente": 0.27206013962450404,
  "delta": -0.16568272478667326,
  "cos_panini_meme_tradition": 0.9443525475186816,
  "cos_panini_tradition_differente": 0.7203382667615167
 },
 "bin_axial_meme_langue": {
  "n": 21,
  "n_meme_tradition": 7,
  "n_tradition_differente": 14,
  "d_lex_meme_tradition": 0.254956457822126,
  "d_lex_tradition_differente": 0.30869554391192205,
  "delta": -0.05373908608979605,
  "cos_panini_meme_tradition": 0.8386554236064271,
  "cos_panini_tradition_differente": 0.6910367699281713
 },
 "meme_langue_eng": {
  "n": 98,
  "n_meme_tradition": 27,
  "n_tradition_differente": 71,
  "d_lex_meme_tradition": 0.21665315019575399,
  "d_lex_tradition_differente": 0.35173801683
… [1569 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('tools/panini_334.py')\ns=p.read_text()\n# Add balanced nulls\nold='''    null_cls_global, null_cls_bins = [], []\n    for _ in range(n_perm):\n        tp = rng.permutation(trad)\n        null_cls_global.append(metrique_classe(knn_clas … [3747 caractères tronqués]`

  ```
patched 6
OK
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('tools/panini_334.py')\ns=p.read_text()\ns=s.replace('''        \"classes\": dict(collections.Counter(trad.tolist())),\n    }''','''    }\n    classes[\"classes\"] = dict(collections.Counter(trad.tolist()))''')\n# Add balanced p to syn … [655 caractères tronqués]`

  ```
patched 7
OK
J12.1 — Panini §334 et 44 signatures
audit : {'corpus_actif_officiel': 114, 'paires': 655, 'textes_distincts_paires': 48, 'textes_absents_des_paires': 66, 'oeuvres_signees': 44, 'sources_ok': 102, 'sources_manifeste': 107, 'sources_ok_parmi_44': 44, 'urls_uniques_non_vides': 71, 'paires_uniques': 495, 'paires_auto': 7, 'paires_doublons_lignes': 160, 'paires_inference': 488}
paires : H0 R2=0.906307 | date R2=0.2579 | partiel date|topo=0.0089 | partiel topo|date=0.8749
œuvres : top1 tradition=0.614 (hasard 0.224, p_bins=0.0659) | top1 proche50=0.568 (hasard 0.228, p_trad=0.3513)
prédiction : MAE année=235.4 (R2=0.614, null dans tradition=269.4) | résidu within-tradition R2=0.042 p=0.0339
écrit : /tmp/panini-334-test4.json
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('/tmp/panini-334-test4.json'))\nprint(json.dumps(d['oeuvres']['prediction']['tradition'],ensure_ascii=False,indent=1)[:3500])\nprint(json.dumps(d['oeuvres']['surface_eng'],ensure_ascii=False,indent=1))\nprint(json.dumps(d['synthese']['tes … [115 caractères tronqués]`

  ```
{
 "baseline_majoritaire": {
  "classe": "GRECO",
  "exactitude": 0.4318181818181818
 },
 "knn": {
  "1": {
   "exactitude": 0.6136363636363636,
   "exactitude_equilibree": 0.306140350877193,
   "f1_macro": 0.28873015873015867,
   "n_classes": 10
  },
  "3": {
   "exactitude": 0.5909090909090909,
   "exactitude_equilibree": 0.2894736842105263,
   "f1_macro": 0.25166666666666665,
   "n_classes": 10
  },
  "5": {
   "exactitude": 0.5454545454545454,
   "exactitude_equilibree": 0.18947368421052632,
   "f1_macro": 0.17376283846872081,
   "n_classes": 10
  }
 },
 "nulls": {
  "n": 500,
  "global": {
   "exactitude_null_moyenne": 0.22254545454545455,
   "p": 0.001996007984031936,
   "exactitude_equilibree_null_moyenne": 0.0764127192982456,
   "p_equilibree": 0.001996007984031936
  },
  "dans_bins_date": {
   "exactitude_null_moyenne": 0.49868181818181817,
   "p": 0.041916167664670656,
   "exactitude_equilibree_null_moyenne": 0.21934956140350875,
   "p_equilibree": 0.08982035928143713
  }
 },
 "classes": {
  "ABRAHAMIC": 8,
  "GRECO": 19,
  "COGNITIVE_SCIENCE": 4,
  "FORMAL_LOGIC": 3,
  "BUDDHIST": 3,
  "CHINESE": 2,
  "MILLENARIAN": 2,
  "RENAISSANCE_OCCULT": 1,
  "CLASSICAL_ORACULAR": 1
… [1037 caractères tronqués]
  ```

- **bash** `{"command": "time python3 tools/panini_334.py --sortie reports/panini-334.json 2>&1 | tail -20", "description": "Run final full analysis", "timeoutMs": 600000}`

  ```
J12.1 — Panini §334 et 44 signatures
audit : {'corpus_actif_officiel': 114, 'paires': 655, 'textes_distincts_paires': 48, 'textes_absents_des_paires': 66, 'oeuvres_signees': 44, 'sources_ok': 102, 'sources_manifeste': 107, 'sources_ok_parmi_44': 44, 'urls_uniques_non_vides': 71, 'paires_uniques': 495, 'paires_auto': 7, 'paires_doublons_lignes': 160, 'paires_inference': 488}
paires : H0 R2=0.906307 | date R2=0.2579 | partiel date|topo=0.0089 | partiel topo|date=0.8749
œuvres : top1 tradition=0.614 (hasard 0.224, p_bins=0.0496) | top1 proche50=0.568 (hasard 0.228, p_trad=0.3669)
prédiction : MAE année=235.4 (R2=0.614, null dans tradition=269.8) | résidu within-tradition R2=0.042 p=0.0314
écrit : reports/panini-334.json
[stderr]

real	1m4,257s
user	1m7,112s
sys	0m0,419s
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/panini-334.json'))\ns=d['synthese']\nprint(json.dumps(s,ensure_ascii=False,indent=1))\nprint('\\nTEST HOLM',json.dumps(s['tests_principaux'],ensure_ascii=False,indent=1))\nprint('\\nPAIR MODELS',json.dumps(d['paires']['modeles'], … [1043 caractères tronqués]`

  ```
{
 "tests_principaux": [
  {
   "nom": "retrieval_filiation",
   "hypothese": "top1 même tradition > null à date contrôlée",
   "p_brut": 0.049590081983603276,
   "p_holm": 0.1277744451109778
  },
  {
   "nom": "retrieval_epoque",
   "hypothese": "top1 proche ≤50 ans > null à filiation contrôlée",
   "p_brut": 0.3669266146770646,
   "p_holm": 0.3669266146770646
  },
  {
   "nom": "prediction_filiation",
   "hypothese": "exactitude tradition > null dans les tranches de date",
   "p_brut": 0.04259148170365927,
   "p_holm": 0.1277744451109778
  },
  {
   "nom": "prediction_epoque",
   "hypothese": "MAE année < null dans chaque tradition",
   "p_brut": 0.007798440311937612,
   "p_holm": 0.03119376124775045
  }
 ],
 "audit": {
  "corpus_actif_officiel": 114,
  "paires": 655,
  "textes_distincts_paires": 48,
  "textes_absents_des_paires": 66,
  "oeuvres_signees": 44,
  "sources_ok": 102,
  "sources_manifeste": 107,
  "sources_ok_parmi_44": 44,
  "urls_uniques_non_vides": 71,
  "paires_uniques": 495,
  "paires_auto": 7,
  "paires_doublons_lignes": 160,
  "paires_inference": 488
 },
 "paires": {
  "r2_h0": 0.9063069849629749,
  "r2_h0_655": 0.9091387033097751,
  "n_paires_inference": 488,

… [11895 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('tools/panini_334.py')\ns=p.read_text()\nold='''    contraste_date_surface[\"ols_effets_fixes\"] = {\n        \"beta_meme_tradition\": float(b_fe[1]),\n        \"r2\": float(r2_fe),\n        \"formule\": \"d_lex ~ 1 + même_tradition +  … [2108 caractères tronqués]`

  ```
patched 8
OK
J12.1 — Panini §334 et 44 signatures
audit : {'corpus_actif_officiel': 114, 'paires': 655, 'textes_distincts_paires': 48, 'textes_absents_des_paires': 66, 'oeuvres_signees': 44, 'sources_ok': 102, 'sources_manifeste': 107, 'sources_ok_parmi_44': 44, 'urls_uniques_non_vides': 71, 'paires_uniques': 495, 'paires_auto': 7, 'paires_doublons_lignes': 160, 'paires_inference': 488}
paires : H0 R2=0.906307 | date R2=0.2579 | partiel date|topo=0.0089 | partiel topo|date=0.8749
œuvres : top1 tradition=0.614 (hasard 0.224, p_bins=0.0496) | top1 proche50=0.568 (hasard 0.228, p_trad=0.3603)
prédiction : MAE année=235.4 (R2=0.614, null dans tradition=269.9) | résidu within-tradition R2=0.042 p=0.0312
écrit : reports/panini-334.json
[stderr]

real	1m7,880s
user	1m10,688s
sys	0m0,411s
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/panini-334.json'))\nprint(json.dumps(d['paires']['contraste_date_surface']['permutation_date_controlee'],ensure_ascii=False,indent=1))\nprint(json.dumps(d['synthese']['tests_principaux'],ensure_ascii=False,indent=1))\nprint('audi … [134 caractères tronqués]`

  ```
{
 "n": 2000,
 "bin_axial": {
  "delta_observe": -0.16568272478667326,
  "delta_null_moyen": -0.0012026393387938234,
  "p": 0.0004997501249375312
 },
 "meme_langue_eng": {
  "delta_observe": -0.1350848666432028,
  "delta_null_moyen": -0.12913246090169342,
  "p": 0.3353323338330835
 }
}
[
 {
  "nom": "retrieval_filiation",
  "hypothese": "top1 même tradition > null à date contrôlée",
  "p_brut": 0.049590081983603276,
  "p_holm": 0.1277744451109778
 },
 {
  "nom": "retrieval_epoque",
  "hypothese": "top1 proche ≤50 ans > null à filiation contrôlée",
  "p_brut": 0.3603279344131174,
  "p_holm": 0.3603279344131174
 },
 {
  "nom": "prediction_filiation",
  "hypothese": "exactitude tradition > null dans les tranches de date",
  "p_brut": 0.04259148170365927,
  "p_holm": 0.1277744451109778
 },
 {
  "nom": "prediction_epoque",
  "hypothese": "MAE année < null dans chaque tradition",
  "p_brut": 0.010597880423915218,
  "p_holm": 0.04239152169566087
 }
]
audit {
 "corpus_actif_officiel": 114,
 "paires": 655,
 "textes_distincts_paires": 48,
 "textes_absents_des_paires": 66,
 "oeuvres_signees": 44,
 "sources_ok": 102,
 "sources_manifeste": 107,
 "sources_ok_parmi_44": 44,
 "urls_uniques_non_vid
… [110 caractères tronqués]
  ```

- **bash** `{"command": "ls -lh reports/panini-334.json; python3 - <<'EOF'\nimport json,os\nd=json.load(open('reports/panini-334.json'))\nprint(os.path.getsize('reports/panini-334.json'))\nprint('audit textes',len(d['audit']['textes']))\nprint('paires',len(d['paires']['paires']))\nprint('oeuvres',len(d['oeuvres … [56 caractères tronqués]`

  ```
-rw-r--r--. 1 stephane stephane 235K 14 nov 05:26 reports/panini-334.json
239823
audit textes 48
paires 488
oeuvres 44
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('tools/panini_334.py')\ns=p.read_text()\nold='''            \"n_meme_tradition\": paires[\"positivite\"][\"n_meme_tradition\"],\n            \"dy_moyen_meme_tradition\": paires[\"positivite\"][\"dy_meme_tradition\"][\"moyenne\"],\n     … [1801 caractères tronqués]`

  ```
patched 9
J12.1 — Panini §334 et 44 signatures
audit : {'corpus_actif_officiel': 114, 'paires': 655, 'textes_distincts_paires': 48, 'textes_absents_des_paires': 66, 'oeuvres_signees': 44, 'sources_ok': 102, 'sources_manifeste': 107, 'sources_ok_parmi_44': 44, 'urls_uniques_non_vides': 71, 'paires_uniques': 495, 'paires_auto': 7, 'paires_doublons_lignes': 160, 'paires_inference': 488}
paires : H0 R2=0.906307 | date R2=0.2579 | partiel date|topo=0.0089 | partiel topo|date=0.8749
œuvres : top1 tradition=0.614 (hasard 0.224, p_bins=0.0496) | top1 proche50=0.568 (hasard 0.228, p_trad=0.3521)
prédiction : MAE année=235.4 (R2=0.614, null dans tradition=270.1) | résidu within-tradition R2=0.042 p=0.0350
écrit : reports/panini-334.json
[stderr]

real	1m3,165s
user	1m5,795s
sys	0m0,394s
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/panini-334.json'))\na=d['audit']; s=d['synthese']; o=d['oeuvres']; p=d['paires']\nprint('audit keys'); print(json.dumps({k:v for k,v in a.items() if k!='textes'},ensure_ascii=False,indent=1))\nprint('synthese'); print(json.dumps( … [431 caractères tronqués]`

  ```
audit keys
{
 "corpus_actif_officiel": 114,
 "corpus_actif_tradition": 104,
 "corpus_actif_references": 10,
 "paires": 655,
 "sections": {
  "a": 459,
  "b": 180,
  "c": 16
 },
 "textes_distincts_paires": 48,
 "textes_absents_des_paires": 66,
 "oeuvres_signees": 44,
 "textes_paires_sans_signature": [
  "an7_64_kodhana",
  "aristotle_de_anima",
  "brahma_sutra_badarayana",
  "zadeh_1965"
 ],
 "sources_manifeste": 107,
 "sources_ok": 102,
 "sources_ok_parmi_48": 45,
 "sources_ok_parmi_44": 44,
 "urls_non_vides": 80,
 "urls_uniques_non_vides": 71,
 "langues_source_44": {
  "eng": 24,
  "inconnu": 19,
  "fra": 1
 }
}
synthese
{
 "tests_principaux": [
  {
   "nom": "retrieval_filiation",
   "hypothese": "top1 même tradition > null à date contrôlée",
   "p_brut": 0.049590081983603276,
   "p_holm": 0.1277744451109778
  },
  {
   "nom": "retrieval_epoque",
   "hypothese": "top1 proche ≤50 ans > null à filiation contrôlée",
   "p_brut": 0.352129574085183,
   "p_holm": 0.352129574085183
  },
  {
   "nom": "prediction_filiation",
   "hypothese": "exactitude tradition > null dans les tranches de date",
   "p_brut": 0.04259148170365927,
   "p_holm": 0.1277744451109778
  },
  {
   "nom": "predic
… [3088 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,150p' docs/pilotage/en-cours.md", "description": "Read current state file"}`

  ```
# En ce moment

**Mis à jour : 2026-11-14, 04 h 38 HNE (heure locale, EST).**

> **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
> plan plus bas (**La carte**).

### Session `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — le hub de reprise du 04/11

- **Id** : `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — [`plan.md`](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/plan.md).
- **Rôle** : **Hub de reprise** — état, docs, intégration, passe.
- **Fait** : index réparé ; **N3 intégré** ; N2/S/L actifs ; suivi docs (revue, liens, tableaux).
- **Prochaine action** : **suivi docs**, puis la **passe** après les runs.
- **Bloquants** : aucun.
- **Journal** : [la session](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/).

## Sessions en cours

> Contrat : [`continuite.md`](../methode/continuite.md) · sessions terminées :
> [`journal/sessions/`](../../journal/sessions/). Chaque session expose son mandat dans son
> `plan.md` (`python3 tools/sessions.py --status`). **Une session écrit l'état à la fois** :
> le hook pre-commit refuse un fait sans ligne d'état ; une session arrêtée passe `État : en pause`.
>
> **Règle 11** : serveurs loca
… [11327 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"Panini\\|J11\\|J12\\|R0.7\\|B13\" docs/pilotage/roadmap.md | head -40; sed -n '1,120p' docs/pilotage/roadmap.md", "description": "Read roadmap relevant sections"}`

  ```
31:| **B — l'intelligence** | langue, pensée, jeux, maîtres, [banc externe](../theorie/glossaire/entrees/banc-externe.md), sémantique, modules | ✅ B1–B12 ; **B1.5 [corpus](../theorie/glossaire/entrees/corpus.md)**, **B12.10, B10.2bis et B11.10 closes** ; le **décodeur** est levé (objectif mot : 32,5 ; JW 26,7), le `z` reste ; **B13** (moteur de pensée) : state store v0 + **AC-3/alpha-bêta** + **[DRVF](../theorie/glossaire/entrees/drvf.md) `thought`** + **[banc](../theorie/glossaire/entrees/banc.md) anytime** + **opérateurs hétérogènes** + **nécessaire** + **labyrinthe** + **[porte](../theorie/glossaire/entrees/porte.md)** + **apprise** + **courbe** + **seule** + **stochastique** + **sto seule** + **ferme** + **minute** + **minute apprise** + **minute seule** + **minute entraînée** + **shaping** + **réseau** + **MLP** + **[professeur](../theorie/glossaire/entrees/professeur.md)** + **sans None** + **correction** + **audit** + **ouverte** + **graines** + **mobile** + **mobile graines** + **bruit** + **bouge** + **bouge graines** + **période** + **phase** + **phase graines** + **aléatoire** + **hasard** + **partielle** + **croyance** + **curiosité** + **observatrice** + **bruitée** + 
… [33497 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,30p' reports/rapport-retrieval-familles.md; echo '---'; sed -n '1,20p' reports/rapport-bilan-chantier.md", "description": "Check report header conventions"}`

  ```
# J7.1 — Le retrieval approfondi par famille Glottolog

> **Ligne de roadmap** : R0.7 (le bloc langue) / L · **Chantier** : Panini, J7.1 · **Date** : 2026-11-14
> **Verdict** : ✅ **le retrieval retrouve la famille, mais seulement dans la même écriture — et il faut
> des sœurs pour le voir.** Sur les 532 textes UDHR (445 langues distinctes après déduplication, 1948),
> le top-1 de voisinage est de la même famille dans **66,1 %** des cas (hasard 10,3 %) et de la même
> branche (sœur) dans **26,1 %** (hasard 2,5 %). Mais **hors écriture, tout retombe au hasard** :
> famille 9,9 % contre 8,1 %, sœur 0,7 % contre 0,8 %. Dans la même écriture, la famille monte à
> **69,8 %** (hasard 16,2 %) et la sœur à **27,8 %** (hasard 5,7 %). Le retrieval parallèle 30 articles
> le confirme et le chiffre : sur les **25 langues LANG_TREE** disponibles, les sœurs valent **0,619**
> (60 paires), les mêmes familles d'une autre branche **0,170** (216), les familles différentes
> **0,0445** (324) — **13,9×**, Δ **+0,574** [0,490 ; 0,655], coefficient de sœur **+0,448**
> (p = 0,002) contre +0,213 pour l'écriture. Sur l'**échantillon 20**, le même contraste est **nul** :
> sœurs 0,0583 (12 paires) contre 0,
… [2976 caractères tronqués]
  ```

- **bash** `{"command": "cat > reports/rapport-panini-334.md <<'EOF'\n# J12.1 — Le §334 et les 44 œuvres : le retrieval et la prédiction de l'époque vs la filiation\n\n> **Ligne de roadmap** : R0.7 (le bloc langue) / L · **Chantier** : Panini, J12.1 · **Date** : 2026-11-14\n> **Verdict** : ✅ **le §334 est une g … [27398 caractères tronqués]`

  ```
383 reports/rapport-panini-334.md
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('tools/panini_334.py')\ns=p.read_text()\nold='''    lignes_v150 = []\n    for i in range(n):\n        for j in range(i + 1, n):\n            cle = (ids_signes[i], ids_signes[j])\n            if cle not in d_topo_lookup:\n               … [3909 caractères tronqués]`

  ```
patched 10
J12.1 — Panini §334 et 44 signatures
audit : {'corpus_actif_officiel': 114, 'paires': 655, 'textes_distincts_paires': 48, 'textes_absents_des_paires': 66, 'oeuvres_signees': 44, 'sources_ok': 102, 'sources_manifeste': 107, 'sources_ok_parmi_44': 44, 'urls_uniques_non_vides': 71, 'paires_uniques': 495, 'paires_auto': 7, 'paires_doublons_lignes': 160, 'paires_inference': 488}
paires : H0 R2=0.906307 | date R2=0.2579 | partiel date|topo=0.0089 | partiel topo|date=0.8749
œuvres : top1 tradition=0.614 (hasard 0.224, p_bins=0.0498) | top1 proche50=0.568 (hasard 0.228, p_trad=0.3565)
prédiction : MAE année=235.4 (R2=0.614, null dans tradition=269.8) | résidu within-tradition R2=0.042 p=0.0314
écrit : reports/panini-334.json
[stderr]

real	1m5,541s
user	1m8,322s
sys	0m0,404s
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/panini-334.json'))\nprint(json.dumps(d['oeuvres']['v150'],ensure_ascii=False,indent=1))\nprint(json.dumps(d['synthese'],ensure_ascii=False,indent=1)[:3500])\nprint('resid p',d['oeuvres']['prediction']['annee']['nulls']['residu_wi … [551 caractères tronqués]`

  ```
{
 "n_paires": 374,
 "formule": "d_sig(L2 V14) ~ 1 + d_topo + Δannée/1000 + même_tradition",
 "beta_brut": [
  0.09062586335944518,
  0.002705890923622122,
  -0.005954476978865826,
  -0.036616557785975265
 ],
 "beta_standardise": [
  0.368972089316387,
  0.26423958399548,
  -0.14801197147188613,
  -0.8789526204097384
 ],
 "r2": 0.30916874198922484,
 "date_coef": -0.005954476978865826,
 "date_coef_null_moyen": 1.361791897904736e-06,
 "date_p_permutation": 0.09295352323838081,
 "date_n_permutations": 2000,
 "publie_v150": {
  "beta": [
   0.1594,
   0.0489,
   0.1378,
   0.0022
  ],
  "r2": 0.3004,
  "formule": "d_sig ~ 1 + d_graph + Δyear/1000 + même_tradition"
 },
 "lecture": "le coefficient de date reconstruit est négatif ; le +0,138 publié n'est pas reproduit sur les 44 signatures du §334"
}
{
 "tests_principaux": [
  {
   "nom": "retrieval_filiation",
   "hypothese": "top1 même tradition > null à date contrôlée",
   "p_brut": 0.04979004199160168,
   "p_holm": 0.1277744451109778
  },
  {
   "nom": "retrieval_epoque",
   "hypothese": "top1 proche ≤50 ans > null à filiation contrôlée",
   "p_brut": 0.35652869426114775,
   "p_holm": 0.35652869426114775
  },
  {
   "nom": "prediction
… [3281 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"0,0496\\|0,352\\|0,0088\\|0,035\\|0,032\\|0,013\\|0,0498\\|0,0106\" reports/rapport-panini-334.md", "description": "Find report numbers to update"}`

  ```
8:> (p = 0,86 ; β standardisé **−0,035**). Le plan est **colinéaire** : **180** paires de même tradition
15:> la filiation à **50,0 %** (p = 0,0496, **Holm 0,128**) et l'époque à **53,8 %** (p = 0,352). Seule une
16:> **petite** prédiction d'année intra-tradition survit (**R² = 0,042**, p = 0,0088, **Holm 0,035**).
149:Le modèle joint standardisé donne **β(d_topo^0,67) = 0,971** et **β(|Δannée|/100) = −0,035** : à
210:| **filiation** (top-1 même tradition, étiquettes permutées dans les tranches de 250 ans) | **61,4 %** | **50,0 %** | **0,0496** | **0,128** |
211:| **époque** (top-1 ≤ 50 ans, années permutées dans chaque tradition) | **56,8 %** | **53,8 %** | **0,352** | 0,352 |
216:significative (0,352). Le top-1 d'époque **brut** (56,8 %) est donc presque entièrement expliqué par
220:filiation (p = 0,013). Mais le seuil **≤ 50 ans** ne la voit pas (p = 0,352) : la trace est dans la
228:| **année, null dans chaque tradition** | MAE **235,4** | **270,1** ; p = **0,0088** | il reste un petit signal **au-delà** de la tradition |
229:| **année, résidu intra-tradition** | MAE **55,7** ; R² **0,042** | **82,1** ; p = **0,032** | 4,2 % de la variance intra-tradition |
235:global). Il rest
… [680 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('reports/rapport-panini-334.md')\ns=p.read_text()\ns=s.replace('(p = 0,0496, **Holm 0,128**) et l\\'époque à **53,8 %** (p = 0,352)',\n            '(p = 0,0498, **Holm 0,128**) et l\\'époque à **53,8 %** (p = 0,3565)')\ns=s.replace('p  … [2771 caractères tronqués]`

  ```
report numbers updated
15:> la filiation à **50,0 %** (p = 0,0498, **Holm 0,128**) et l'époque à **53,8 %** (p = 0,3565). Seule une
16:> **petite** prédiction d'année intra-tradition survit (**R² = 0,042**, p = 0,0106, **Holm 0,042**).
210:| **filiation** (top-1 même tradition, étiquettes permutées dans les tranches de 250 ans) | **61,4 %** | **50,0 %** | **0,0498** | **0,128** |
211:| **époque** (top-1 ≤ 50 ans, années permutées dans chaque tradition) | **56,8 %** | **53,8 %** | **0,3565** | 0,3565 |
216:significative (0,3565). Le top-1 d'époque **brut** (56,8 %) est donc presque entièrement expliqué par
220:filiation (p = 0,0108). Mais le seuil **≤ 50 ans** ne la voit pas (p = 0,3565) : la trace est dans la
228:| **année, null dans chaque tradition** | MAE **235,4** | **270,1** ; p = **0,0106** | il reste un petit signal **au-delà** de la tradition |
229:| **année, résidu intra-tradition** | MAE **55,7** ; R² **0,042** | **82,1** ; p = **0,031** | 4,2 % de la variance intra-tradition |
235:global). Il reste **4,2 %** de variance intra-tradition (p = 0,031), et c'est le **seul** test qui
293:   (56,8 % vs 22,8 %), mais les contrôles croisés ramènent la filiation à 50,0 % (p = 0,04
… [292 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"Holm 0,035\\|Holm 0,042\\|0,093\\|−0,0060\" reports/rapport-panini-334.md; sed -n '280,380p' reports/rapport-panini-334.md", "description": "Check final report tail"}`

  ```
16:> **petite** prédiction d'année intra-tradition survit (**R² = 0,042**, p = 0,0106, **Holm 0,042**).
264:| `|Δannée|/1000` | **−0,0060** | **−0,148** | **+0,1378** |
269:il est **négatif** (**−0,0060**) et non significatif (p = **0,093** par 2 000 permutations des
296:   (R² = 0,042, p = 0,0106, Holm 0,042) : il reste une trace d'époque, mais 96 % de la variance
375:  **petite** prédiction d'année intra-tradition (R² = 0,042, Holm 0,042) ; la filiation est **marginale**
## 7. Ce que cela dit de l'avertissement de Panini

1. **La loi H0 du §334 est une loi de filiation/topologie**, pas d'époque : R² = 0,909139 sur les 655
   lignes, 0,906307 sur les 488 paires uniques ; la date seule explique 0,258, mais n'ajoute que
   0,0089 après la topologie (p = 0,86).
2. **Le plan est colinéaire** : 180 paires de même tradition à 28,7 ans d'écart (max 230), 308 paires
   inter-traditions à 1 189 ans (136 à ≤ 100 ans). Le corpus **ne peut pas** identifier un effet
   d'époque indépendant de la filiation ; il ne peut pas non plus identifier une filiation indépendante
   de la date.
3. **À date fixe, la filiation est forte** dans la tranche axiale (Δ = −0,166, p = 0,0005), mais
   **elle dispa
… [6612 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('docs/theorie/genealogie-des-langues.md')\ns=p.read_text()\nanchor='''**Ce que J3.2 ajoute à la lecture de cet avertissement.** Leur « filiation » (`d_graph`) est une distance\nde **tradition** — la position d'une œuvre dans un graphe  … [3099 caractères tronqués]`

  ```
theory updated
    3310    317   T1   3500  README.md
    3072    341 DATÉ      0  docs/implantation/convertisseur.md
    2962    364   T1   5000  docs/theorie/glossaire/02-modeles-et-architectures.md
    2896    352 DATÉ      0  docs/implantation/configuration-nvme-raid-amd.md
    2746    203   T1   2800  reports/README.md
    2450    166   T1   2500  docs/pilotage/references-non-regression.md
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
     · 50 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.m
… [154 caractères tronqués]
  ```

- **bash** `{"command": "ls reports/*.md | wc -l; ls reports/*.json | wc -l", "description": "Count reports md and json"}`

  ```
729
823
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('docs/pilotage/en-cours.md')\ns=p.read_text()\ns=s.replace('**Mis à jour : 2026-11-14, 04 h 38 HNE (heure locale, EST).**',\n            '**Mis à jour : 2026-11-14, 05 h 55 HNE (heure locale, EST).**')\nanchor='''- **Panini J7.1** : 53 … [1827 caractères tronqués]`

  ```
en-cours updated
  en-cours · 1738 mots · 7 sections · 4 session(s) · 10 puces · 5 questions
  ❌ 1 anomalie(s) :
     · puce > 80 mots : **Panini J12.1 — le §334 et les 44 signatures** : **655 lign
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('docs/pilotage/en-cours.md')\ns=p.read_text()\nold='''- **Panini J12.1 — le §334 et les 44 signatures** : **655 lignes = 495 paires uniques (160 doublons, 7 auto-paires), 48 textes, 44 signatures** ; H0 **0,909139** (655 lignes) / **0, … [1344 caractères tronqués]`

  ```
shortened
  en-cours · 1734 mots · 7 sections · 4 session(s) · 11 puces · 5 questions
  ❌ 1 anomalie(s) :
     · 11 puces dans « Ce qui est en cours » > 10
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('docs/pilotage/en-cours.md')\ns=p.read_text()\nold='''- **Panini J12.1 — audit** : **655 lignes = 495 paires uniques (160 doublons, 7 auto-paires), 48 textes, 44 signatures** ; H0 **0,909139** (655) / **0,906307** (488) ; date seule ** … [1202 caractères tronqués]`

  ```
merged
  en-cours · 1714 mots · 7 sections · 4 session(s) · 10 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('docs/pilotage/roadmap.md')\ns=p.read_text()\nold='J3.1 reproduit** ([fiche](../../reports/rapport-retrieval-familles.md))'\nnew='J3.1 reproduit** ([fiche](../../reports/rapport-retrieval-familles.md)) ; **J12.1 §334 : 655 lignes = 495 … [2571 caractères tronqués]`

  ```
roadmap updated, occurrences replaced: 2
35:| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 langues à 0,9687**, script 1,0000 ; analyse heuristique (5 schémas) ; **contrat de substitution écrit** ([`contrat-bloc-langue.md`](../theorie/contrat-bloc-langue.md)) ; **frontière : script 1,0, langue 0,137 (libellés) / 0,9687 (texte long)** ; **porte des quatre modes : neuronal 0,9309/0,8226/0,8784 ; fusion 0,928/0,802/0,857** ; **fusion réparée par niveau : 0,9309/0,8226/0,8784/0,9954 (le max)** ([fiche](../../reports/rapport-pensee-fusion-reparee.md)) ; **corpus commun UDHR : 21 textes, 418/438 paires exactes (95,4 %), 20 écarts exclus** ([fiche](../../reports/rapport-corpus-commun.md)) ; **J3.1 retrieval à époque contrôlée : l'écriture domine (+0,609), l'époque ne pèse pas à écriture contrôlée (−0,034/siècle, p=0,19), le brut est un effet de composition (0,238 vs 0,427)** ([fiche](../../reports/rapport-retrieval-epoque.md)) ; **J3.2 généalogie à deux faces : Panini couvre 5/21 langues (200/210 paires « inconnues »), Glottolog 21/21 ; 154/154 paires hors script au has
… [3137 caractères tronqués]
  ```

- **bash** `{"command": "tail -40 journal/2026-11-14/README.md", "description": "Read journal notes tail"}`

  ```
`rendre_mots`/`rendre_pos` séparent la ponctuation (`dort .`). La v1 construit une **forme
canonique** depuis les **segments + rôles + cibles** : **46/46 formes exactes** contre une
source canonisée (casse repliée, ponctuation retirée), mais **1/46 = 0,0217** contre la source
brute — et le **miroir strict reste 0,1087**. C'est la réponse : le strict ne doit pas monter,
il mesure la surface ; la forme canonique mesure autre chose. La structure tient : **395
segments**, **395 rôles**, **315 cibles**, **315/315 résolues**, **313/315** portées par un
autre segment ; couverture **65,84 % des jetons**, **75,19 % des caractères**. La limite est la
**stabilité structurelle** : **18/46** seulement après re-analyse de la surface canonique (le
lexique, lui, est stable 46/46). Contrôles : mélange/troncature canoniques **0/46**, détection
**46/46** ; rôles/cibles retirés, clé changée **43/43** textes éligibles. Fiche
[`reports/rapport-restitution-v1.md`](../../reports/rapport-restitution-v1.md), JSON
[`reports/pensee-restitution-v1.json`](../../reports/pensee-restitution-v1.json), outil
[`tools/mesurer_restitution_v1.py`](../../tools/mesurer_restitution_v1.py).
**J11.3 — les 50 textes libres : 
… [2326 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('journal/2026-11-14/README.md')\ns=p.read_text()\nanchor='<!-- /notes -->'\naddition='''**J12.1 — le §334 et les 44 signatures : la filiation, pas l'époque — et un corpus qui ne les sépare pas.**\nLa deuxième vague Panini est d'abord u … [1763 caractères tronqués]`

  ```
journal updated
  journal · 46 jour(s) · 190 session(s) · 2495 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
  ```

- **bash** `{"command": "python3 -c \"import pytest; print(pytest.__version__)\" 2>&1; ls tools/tests | head -20", "description": "Check pytest and test layout"}`

  ```
9.1.1
code
documents
linguistique
maths
__pycache__
qualifier_politique_drvm.py
qualifier_porte_bouge_drvm.py
qualifier_porte_drvm.py
qualifier_porte_fenetre_drvm.py
qualifier_porte_minute_drvm.py
qualifier_porte_mobile_drvm.py
qualifier_porte_sto_drvm.py
qualifier_porte_sto_graines.py
tableaux
test_pensee_politique.py
test_pensee_store.py
test_produit_libre.py
test_produit.py
test_restitution.py
test_schema_produit.py
  ```

- **bash** `{"command": "cat > tools/tests/test_panini_334.py <<'EOF'\n\"\"\"Tests de J12.1 — l'outil `panini_334.py` et ses invariants.\n\nLes artefacts Panini sont hors du dépôt Drave (`../Panini/research`) : les\ntests sont sautés s'ils ne sont pas présents. On vérifie les **faits de\nstructure** (pas les p- … [3534 caractères tronqués]`

  ```
....                                                                     [100%]
4 passed in 1.54s
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('tools/tests/test_panini_334.py')\ns=p.read_text()\ns=s.replace('''    res = mod.analyser_oeuvres(textes, ids_signes, n_perm=10, n_boot=10, graine=0)\n    doublons = {(d[\"a\"], d[\"b\"]) for d in res[\"paires\"][\"doublons_exacts\"]}  … [448 caractères tronqués]`

  ```
test cleaned
....                                                                     [100%]
4 passed in 1.32s
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -60", "description": "Run documentation review"}`

  ```
revue de documentation · 729 fiche(s) · 823 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ```

- **bash** `{"command": "bash tools/porte-tableaux.sh 2>&1 | tail -30", "description": "Run table gate"}`

  ```
❌ 1 tableau(x) ne rendront pas (mistune refuse le tableau ENTIER) :
     reports/rapport-panini-334.md:264 — 6 cellules ≠ 4 attendues
  1794 fichier(s) examiné(s)
  ```

- **bash** `{"command": "sed -n '258,268p' reports/rapport-panini-334.md", "description": "Inspect broken table"}`

  ```
On reconstruit la même forme sur les **374 paires uniques non auto** des 44 signatures, avec
`d_sig` = distance L2 des 14 atomes et `d_topo` à la place de `d_graph` :

| terme | β brut (nous) | β standardisé (nous) | β publié (v150) |
|---|---:|---:|---:|
| `d_topo` | **+0,0027** | **+0,264** | +0,0489 |
| `|Δannée|/1000` | **−0,0060** | **−0,148** | **+0,1378** |
| même tradition | **−0,0366** | **−0,879** | +0,0022 |
| **R²** | **0,3092** | — | 0,3004 |

Le R² est du même ordre (0,309 contre 0,300), mais le **signe du coefficient de date est inversé** :
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('reports/rapport-panini-334.md')\ns=p.read_text().replace('| `|Δannée|/1000` |', '| `Δannée/1000` |')\np.write_text(s)\nprint('fixed')\nEOF\nbash tools/porte-tableaux.sh 2>&1 | tail -10", "description": "Fix table and rerun gate"}`

  ```
fixed
  ✅ 1794 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4165 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-14)
  ```

- **bash** `{"command": "python3 tools/verifier_schemas.py 2>&1 | tail -20; echo '--- liens?'; python3 tools/verifie_liens.py 2>&1 | tail -10 || true", "description": "Run schema and link checks"}`

  ```
schémas · 463 document(s) · 67 SVG · 2 source(s)
  ✅ aucun ASCII art, SVG valides et référencés, blocs PlantUML inline valides,
     sources et images relatives.
--- liens?
python3: can't open file '/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifie_liens.py': [Errno 2] No such file or directory
  ```

- **bash** `{"command": "time python3 tools/panini_334.py --sortie /tmp/panini-334-repro.json >/tmp/panini-334-repro.log 2>&1; tail -5 /tmp/panini-334-repro.log; python3 - <<'EOF'\nimport json,hashlib\na=open('reports/panini-334.json','rb').read(); b=open('/tmp/panini-334-repro.json','rb').read()\nprint('same b … [320 caractères tronqués]`

  ```
audit : {'corpus_actif_officiel': 114, 'paires': 655, 'textes_distincts_paires': 48, 'textes_absents_des_paires': 66, 'oeuvres_signees': 44, 'sources_ok': 102, 'sources_manifeste': 107, 'sources_ok_parmi_44': 44, 'urls_uniques_non_vides': 71, 'paires_uniques': 495, 'paires_auto': 7, 'paires_doublons_lignes': 160, 'paires_inference': 488}
paires : H0 R2=0.906307 | date R2=0.2579 | partiel date|topo=0.0089 | partiel topo|date=0.8749
œuvres : top1 tradition=0.614 (hasard 0.224, p_bins=0.0494) | top1 proche50=0.568 (hasard 0.228, p_trad=0.3505)
prédiction : MAE année=235.4 (R2=0.614, null dans tradition=270.0) | résidu within-tradition R2=0.042 p=0.0300
écrit : /tmp/panini-334-repro.json
same bytes False sha 3c2d40732700d8ae 64a7b4d645d38626
diff key oeuvres
diff key synthese
[stderr]

real	1m9,082s
user	1m11,946s
sys	0m0,411s
  ```

- **bash** `{"command": "grep -n \"set(trad)\\|set(bins\\|set(langue\\|set(fams\" tools/panini_334.py", "description": "Find nondeterministic set iterations"}`

  ```
482:    for b in sorted(set(bins_paire)):
670:    for bv in sorted(set(bins_paire.tolist()))[1:]:
672:    for lv in sorted(set(langue_paire.tolist()))[1:]:
686:        for b in set(bins):
920:        for t in set(trad):
930:        for b in set(bins_ret):
994:    for b in sorted(set(bins)):
1037:        for t in set(trad):
1045:    moyennes = {t: float(np.mean(annees[trad == t])) for t in set(trad)}
1050:        for t in set(trad):
1055:        pm = {t: float(np.mean(yp[trad == t])) for t in set(trad)}
1094:        for b in set(bins):
1122:    for c in sorted(set(trad)):
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('tools/panini_334.py')\ns=p.read_text()\ns=s.replace('        for b in set(bins):\\n            idx_b = np.where(bins == b)[0]', '        for b in sorted(set(bins.tolist())):\\n            idx_b = np.where(bins == b)[0]')\ns=s.replace( … [1140 caractères tronqués]`

  ```
deterministic sorts patched
no unsorted loops
OK
  ```

- **bash** `{"command": "python3 tools/panini_334.py --sortie reports/panini-334.json >/tmp/panini-run1.log 2>&1 && python3 tools/panini_334.py --sortie /tmp/panini-334-repro2.json >/tmp/panini-run2.log 2>&1; tail -4 /tmp/panini-run1.log; tail -4 /tmp/panini-run2.log; python3 - <<'EOF'\nimport hashlib\na=open(' … [278 caractères tronqués]`

  ```
paires : H0 R2=0.906307 | date R2=0.2579 | partiel date|topo=0.0089 | partiel topo|date=0.8749
œuvres : top1 tradition=0.614 (hasard 0.224, p_bins=0.0492) | top1 proche50=0.568 (hasard 0.228, p_trad=0.3731)
prédiction : MAE année=235.4 (R2=0.614, null dans tradition=269.9) | résidu within-tradition R2=0.042 p=0.0328
écrit : reports/panini-334.json
paires : H0 R2=0.906307 | date R2=0.2579 | partiel date|topo=0.0089 | partiel topo|date=0.8749
œuvres : top1 tradition=0.614 (hasard 0.224, p_bins=0.0492) | top1 proche50=0.568 (hasard 0.228, p_trad=0.3731)
prédiction : MAE année=235.4 (R2=0.614, null dans tradition=269.9) | résidu within-tradition R2=0.042 p=0.0328
écrit : /tmp/panini-334-repro2.json
same bytes True sha cf59d4e707bfa163 cf59d4e707bfa163
  ```

- **bash** `{"command": "python3 - <<'EOF'\nimport json\nd=json.load(open('reports/panini-334.json'))\ns=d['synthese']; o=d['oeuvres']; p=d['paires']\nprint('tests',json.dumps(s['tests_principaux'],ensure_ascii=False,indent=1))\nprint('oeuvres p',s['oeuvres']['p_top1_tradition_bins'],s['oeuvres']['p_top1_proche … [547 caractères tronqués]`

  ```
tests [
 {
  "nom": "retrieval_filiation",
  "hypothese": "top1 même tradition > null à date contrôlée",
  "p_brut": 0.04919016196760648,
  "p_holm": 0.1277744451109778
 },
 {
  "nom": "retrieval_epoque",
  "hypothese": "top1 proche ≤50 ans > null à filiation contrôlée",
  "p_brut": 0.373125374925015,
  "p_holm": 0.373125374925015
 },
 {
  "nom": "prediction_filiation",
  "hypothese": "exactitude tradition > null dans les tranches de date",
  "p_brut": 0.04259148170365927,
  "p_holm": 0.1277744451109778
 },
 {
  "nom": "prediction_epoque",
  "hypothese": "MAE année < null dans chaque tradition",
  "p_brut": 0.008598280343931213,
  "p_holm": 0.03439312137572485
 }
]
oeuvres p 0.04919016196760648 0.373125374925015 0.09198160367926415
resid {'mae_observe': 55.70828349282295, 'r2_observe': 0.04176725737595954, 'mae_null_moyen': 82.23768704146731, 'p': 0.03279344131173765}
year null {'mae_null_moyen': 269.89419545454547, 'p': 0.008598280343931213}
trad null {'exactitude_null_moyenne': 0.5001318181818182, 'p': 0.04259148170365927, 'exactitude_equilibree_null_moyenne': 0.21954473684210524, 'p_equilibree': 0.09198160367926415}
mean dy p 0.009398120375924815
v150 0.09295352323838081
pair p 
… [263 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('reports/rapport-panini-334.md')\ns=p.read_text()\ns=s.replace('(p = 0,0498, **Holm 0,128**) et l\\'époque à **53,8 %** (p = 0,3565)',\n            '(p = 0,0492, **Holm 0,128**) et l\\'époque à **53,8 %** (p = 0,373)')\ns=s.replace('** … [2482 caractères tronqués]`

  ```
numbers synced
old numbers gone
15:> la filiation à **50,0 %** (p = 0,0492, **Holm 0,128**) et l'époque à **53,8 %** (p = 0,373). Seule une
16:> **petite** prédiction d'année intra-tradition survit (**R² = 0,042**, p = 0,0086, **Holm 0,034**).
210:| **filiation** (top-1 même tradition, étiquettes permutées dans les tranches de 250 ans) | **61,4 %** | **50,0 %** | **0,0492** | **0,128** |
211:| **époque** (top-1 ≤ 50 ans, années permutées dans chaque tradition) | **56,8 %** | **53,8 %** | **0,373** | 0,373 |
216:significative (0,373). Le top-1 d'époque **brut** (56,8 %) est donc presque entièrement expliqué par
220:filiation (p = 0,0094). Mais le seuil **≤ 50 ans** ne la voit pas (p = 0,373) : la trace est dans la
228:| **année, null dans chaque tradition** | MAE **235,4** | **270,1** ; p = **0,0086** | il reste un petit signal **au-delà** de la tradition |
229:| **année, résidu intra-tradition** | MAE **55,7** ; R² **0,042** | **82,2** ; p = **0,033** | 4,2 % de la variance intra-tradition |
235:global). Il reste **4,2 %** de variance intra-tradition (p = 0,033), et c'est le **seul** test qui
293:   (56,8 % vs 22,8 %), mais les contrôles croisés ramènent la filiation à 50,0 % (p = 
… [405 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\nfor f in ['docs/pilotage/en-cours.md','docs/pilotage/roadmap.md','journal/2026-11-14/README.md']:\n    p=Path(f); s=p.read_text()\n    s=s.replace('0,0498', '0,0492').replace('0,3565', '0,373')\n    s=s.replace('p=0,0106', 'p=0,0086').replace … [349 caractères tronqués]`

  ```
patched docs/pilotage/en-cours.md
patched docs/pilotage/roadmap.md
patched journal/2026-11-14/README.md
docs/pilotage/en-cours.md:93:- **Panini J12.1 — §334** : **655 lignes = 495 paires uniques (160 doublons, 7 auto-paires), 48 textes, 44 signatures** ; H0 **0,909139** / **0,906307** (488) ; date **0,258** seule, **0,0089** après topo (p=0,86) ; filiation à date fixe **Δ=−0,166** (p=0,0005), mais **Δ=−0,135** vs null **−0,129** (p=0,335) à surface contrôlée ; 44 œuvres : filiation **61,4 %** vs **50,0 %** (Holm 0,128), époque **56,8 %** vs **53,8 %** (p=0,373), année intra-tradition **R²=0,042** (Holm 0,034) ; [fiche](../../reports/rapport-panini-334.md).
docs/pilotage/roadmap.md:35:| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 langues à 0,9687**, script 1,0000 ; analyse heuristique (5 schémas) ; **contrat de substitution écrit** ([`contrat-bloc-langue.md`](../theorie/contrat-bloc-langue.md)) ; **frontière : script 1,0, langue 0,137 (libellés) / 0,9687 (texte long)** ; **porte des quatre modes : neuronal 0,9309/0,8226/0,8784 ; fusion 0,928/0,802/0,857** ; **fu
… [4677 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/verifie_en_cours.py 2>&1 | tail -10; python3 tools/revue_documentation.py 2>&1 | tail -20; bash tools/porte-tableaux.sh 2>&1 | tail -10", "description": "Run state, doc and table checks"}`

  ```
en-cours · 1714 mots · 7 sections · 4 session(s) · 10 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  revue de documentation · 729 fiche(s) · 823 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ✅ 1794 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4165 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-14)
  ```

- **bash** `{"command": "git status --short", "description": "Check git status"}`

  ```
M docs/pilotage/en-cours.md
 M docs/pilotage/roadmap.md
 M docs/theorie/genealogie-des-langues.md
 M journal/2026-11-14/README.md
 M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
 M journal/sessions/session-631f4ba2-5c36-4fdc-b751-fa0a2cce9d21/digest.md
 M journal/sessions/session-631f4ba2-5c36-4fdc-b751-fa0a2cce9d21/rapport.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/plan.json
 m tools/structures
?? journal/sessions/session-6a9e96a0-20f8-4721-8b73-82eba29bd2b6/
?? reports/panini-334.json
?? reports/rapport-panini-334.md
?? reports/rapport-s-paragraphes.md
?? tools/panini_334.py
?? tools/tests/test_panini_334.py
  ```

- **bash** `{"command": "git diff --stat journal/README.md journal/sessions/MANIFEST.md journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md journal/sessions/session-631f4ba2-5c36-4fdc-b751-fa0a2cce9d21/digest.md journal/sessions/sessio … [212 caractères tronqués]`

  ```
journal/README.md                                  |  5 +-
 journal/sessions/MANIFEST.md                       |  7 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md | 10 +++
 .../rapport.md                                     | 14 ++--
 .../digest.md                                      | 92 ++++++++++++++++++++++
 .../rapport.md                                     | 45 +++++++++--
 6 files changed, 153 insertions(+), 20 deletions(-)
--- sample
diff --git a/journal/sessions/MANIFEST.md b/journal/sessions/MANIFEST.md
index 171a0e97..3edce539 100644
--- a/journal/sessions/MANIFEST.md
+++ b/journal/sessions/MANIFEST.md
@@ -146,7 +146,7 @@ trace brute (`session*.jsonl.zstd`) reste sur disque et n'est pas suivie par git
 | `ddf8d740` | 2026-10-22 08:28 | 0.1 Mo | 22 Ko | 1 | 17 | 14 | 0 | 0 |
 | `df1b1098` | 2026-10-31 17:52 | 0.0 Mo | 13 Ko | 1 | 4 | 0 | 0 | 0 |
 | `e14c26ae` | 2026-10-02 21:15 | 0.7 Mo | 109 Ko | 1 | 49 | 76 | 0 | 0 |
-| `e181ce02` | 2026-10-31 17:40 | 19.9 Mo | 3741 Ko | 194 | 3685 | 3281 | 7 | 16 |
+| `e181ce02` | 2026-10-31 17:40 | 19.9 Mo | 3742 Ko | 194 | 3686 | 3282 | 7 | 16 |
 | `e7dfe34f` | 2026-09-28 14:56 | 0.2 Mo | 28 Ko | 1 | 20 | 21 | 0 | 0 |
 | `ea
… [4473 caractères tronqués]
  ```

- **bash** `{"command": "git show --stat --oneline 55bde5c5 | head -30; echo '---'; git show --stat --oneline 09e54143 | head -30", "description": "Check prior commit file sets"}`

  ```
55bde5c5 J11.3 — LES 50 TEXTES LIBRES : 0 PLANTAGE, 50/50 SCHÉMA V2, 115 CHEVAUCHEMENTS ALTERNATIVE / 0 FILTRER ; RESTITUTION 46/46, STRICT 0,1087 (F1 0,7902)
 docs/pilotage/en-cours.md                          |    8 +-
 docs/pilotage/roadmap.md                           |   11 +
 journal/2026-11-14/README.md                       |   20 +-
 journal/2026-11-14/docs.md                         |    2 +-
 journal/2026-11-14/memoire.md                      |    2 +-
 journal/2026-11-14/mesures.md                      |    8 +-
 journal/2026-11-14/portes.md                       |    2 +-
 journal/README.md                                  |    5 +-
 journal/THEMES.md                                  |    2 +-
 journal/sessions/MANIFEST.md                       |    7 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md |    9 +
 .../rapport.md                                     |   14 +-
 .../digest.md                                      | 2490 ++++++++++++++++
 .../rapport.md                                     |  181 ++
 .../digest.md                                      |  106 +
 .../rapport.md                                     |   47 +-
 reports/pensee-robustesse-semaine.jso
… [1710 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"math\\.\\|sys\\.\" tools/panini_334.py | head; python3 -m pyflakes tools/panini_334.py 2>&1 | head -20 || true", "description": "Check unused imports"}`

  ```
/usr/bin/python3: No module named pyflakes
  ```

- **bash** `{"command": "python3 - <<'EOF'\nfrom pathlib import Path\np=Path('tools/panini_334.py')\ns=p.read_text()\ns=s.replace('import math\\n','').replace('import sys\\n','')\ns=s.replace('        bv_std, r2v_std, _ = ols(', '        bv_std, _, _ = ols(')\np.write_text(s)\nprint('cleaned imports')\nEOF\npyt … [166 caractères tronqués]`

  ```
cleaned imports
....                                                                     [100%]
4 passed in 1.36s
  ```

- **bash** `{"command": "ls tools/porte-*.sh | sed 's#tools/porte-##;s#\\.sh##' | tr '\\n' ' '; echo", "description": "List gate names"}`

  ```
adaptateur-sortie audit-drapeaux b1110-hybride balayage bloc-code bloc-linguistique bloc-maths bloc-tableaux budget bus bus-socket c4-retard cerveau consolidation coupe cycle-c2 deepseek delais diff-couche document echange-experts episodique etat flux fusion gain greffe harnais-invariants homeostasie horloge indice jeux jumeaux lecteur lecture m5-brouillon melange memoire miroir-blocs mistral n3-cache n3-composition n3-deux-processus n3-deux-regions n3-generation n3-inventaire n3-placement n3-pont n3-positions n3-profondeur n3-refus n3-reseau n3-routes n3-service-briques n3-service n3-seuil n3-sparsite-compte n3-sparsite occupation-elagage occupation-moteur ocr-scans ocr pannes peripherie poids-creux pont prechargement produit profondeur-routee push-paresseux r13-bpe recurrence reflexe registre reparti-moteur ressources sauvegarde-modele sessions speculatif tableaux tokenizer-kimi topologie trace vision
  ```

- **bash** `{"command": "PORTES=\"document tableaux registre etat sessions budget\" DELAI=600 bash tools/toutes-les-portes.sh 2>&1 | tail -40", "description": "Run relevant document gates", "timeoutMs": 900000}`

  ```
=== PASSE COMPLÈTE DES PORTES (7 portes, borne 600 s) ===
    journaux : work/portes-1114-05h36
  porte-bloc-tableaux    ✅                           1 s  ✅ porte bloc tableaux verte
  porte-budget           ✅                          46 s    ✅ paires depassees : nommees (total, budget, pas, plafond), code 9, AUCUNE perplexite
  porte-document         ✅                           6 s  ✅ porte document verte
  porte-etat             ✅                           0 s  ✅ porte état verte : aucun fait commité après le dernier état
  porte-registre         ✅                          16 s    ✅ région absente : refusée en la nommant (code 2), rien n'est calculé
  porte-sessions         ❌ code 1                    0 s    ❌ mandat périmé (263 min) : e181ce02-cd50-488a-a6be-e84b79d40dcc — heartbeat à rafraîchir
  porte-tableaux         ✅                           1 s    ✅ la page vivante date du dernier commit (2026-11-14)
--- 6 vertes, 1 rouges ---
À RELIRE (les six dernières lignes de chaque rouge) :
  --- porte-sessions ---
    autotest OK : plan valide, périmètre dupliqué refusé, champ manquant refusé, pause sans heartbeat exigé, mandat long avec claim accepté, reservation imbriquée avertie 
… [247 caractères tronqués]
  ```

- **bash** `{"command": "ls -l .git/hooks/pre-commit 2>/dev/null; sed -n '1,120p' .git/hooks/pre-commit 2>/dev/null; echo '--- config'; git config --get core.hooksPath", "description": "Inspect commit hooks"}`

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
… [332 caractères tronqués]
  ```

- **bash** `{"command": "git diff --check -- docs/pilotage/en-cours.md docs/pilotage/roadmap.md docs/theorie/genealogie-des-langues.md journal/2026-11-14/README.md reports/rapport-panini-334.md tools/panini_334.py tools/tests/test_panini_334.py; echo CODE:$?; git status --short | head -30", "description": "Chec … [25 caractères tronqués]`

  ```
CODE:0
 M docs/pilotage/en-cours.md
 M docs/pilotage/roadmap.md
 M docs/theorie/genealogie-des-langues.md
 M journal/2026-11-14/README.md
 M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
 M journal/sessions/session-631f4ba2-5c36-4fdc-b751-fa0a2cce9d21/digest.md
 M journal/sessions/session-631f4ba2-5c36-4fdc-b751-fa0a2cce9d21/rapport.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/plan.json
 m tools/structures
?? journal/sessions/session-6a9e96a0-20f8-4721-8b73-82eba29bd2b6/
?? reports/panini-334.json
?? reports/rapport-panini-334.md
?? reports/rapport-s-paragraphes.md
?? tools/panini_334.py
?? tools/tests/test_panini_334.py
  ```

- **bash** `{"command": "git add docs/pilotage/en-cours.md docs/pilotage/roadmap.md docs/theorie/genealogie-des-langues.md journal/2026-11-14/README.md reports/panini-334.json reports/rapport-panini-334.md tools/panini_334.py tools/tests/test_panini_334.py && git status --short | head -30", "description": "Stag … [15 caractères tronqués]`

  ```
M  docs/pilotage/en-cours.md
M  docs/pilotage/roadmap.md
M  docs/theorie/genealogie-des-langues.md
M  journal/2026-11-14/README.md
 M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
 M journal/sessions/session-631f4ba2-5c36-4fdc-b751-fa0a2cce9d21/digest.md
 M journal/sessions/session-631f4ba2-5c36-4fdc-b751-fa0a2cce9d21/rapport.md
A  reports/panini-334.json
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
A  reports/rapport-panini-334.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/plan.json
A  tools/panini_334.py
 m tools/structures
A  tools/tests/test_panini_334.py
?? journal/sessions/session-6a9e96a0-20f8-4721-8b73-82eba29bd2b6/
?? reports/rapport-s-paragraphes.md
  ```

- **bash** `{"command": "cat > /tmp/commit-j121.txt <<'EOF'\nJ12.1 — LE §334 EST UNE GÉOMÉTRIE DE FILIATION : 655 LIGNES = 495 PAIRES UNIQUES (160 DOUBLONS, 7 AUTO-PAIRES), 48 TEXTES, 44 SIGNATURES ; H0 0,909139 / 0,906307 (488), DATE 0,0089 APRÈS TOPO (p=0,86) ; FILIATION 61,4 % vs 50,0 % (HOLM 0,128), ÉPOQUE  … [1695 caractères tronqués]`
