# Session DSH — relecture

- identifiant : `session-bfa61e65-a77c-4ab8-bce1-72505858a3d5`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-14 00:41:36
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche J6.1 : le dernier span du gold, `g017` (« She said that she would come yesterday. ») — le gold attend la SUB « that she would come » (sans « yesterday »), le bloc l'inclut. Reproduis, propose UNE règle mesurée (l'adverbe final de temps hors de la SUB), vérifie dev/test et l'attachement, fiche `reports/rapport-g017.md` + JSON, commit. Si la règle casse autre chose, écris la fiche du rejet.

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

- **bash** `{"command": "pwd && ls && git log --oneline -5 && git status --short | head -30", "description": "Inspect repo root and git state"}`

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
34e3e4ab J5.1 — LE RAPPORT DE SEMAINE : F1 0,7533 → 0,7902, ATTACHEMENT 236 → 237, TAGGER 0,9475 (+8,49, INTÉGRER), INTÉGRATION BORNÉE (TABLE 14/14, CORPUS 418/438), 13 DÉCISIONS, 21 REJETS
dc78f223 ÉTAT — T0 DANS LE BUDGET (3 991 MOTS) : LA LIGNE R0.7 PORTE LE TAGGER 612 (0,9475, +8,49, INTÉGRER)
a934d779 R0.7 — LE TAGGER POS SUR LE GOLD 612 : 0,9475 (3012/3179), +8,49 PTS, LA RÈGLE DIT INTÉGRER ; LA CLÉ ÉTAIT PRÉSENTE ET 0,8500 ÉTAIT DATÉ (0,8625)
ced21933 CHANTIER — PHASE 2 (12 H) : LE VERDICT ACCEPTATION D'ABORD (TIMEOUT APRÈS COMMIT = FAIT), 12 TÂCHES AJOUTÉES (J4 COORDINATION, J6 SPANS, J7-J10 PANINI/BILAN), ÉTAT CORRIGÉ
c7f26b35 DOCS — LA PASSE APRÈS LE CHANTIER : 8 FICHES INDEXÉES, L'ÉTAT PAR JOUR DU PLAN, LE JOURNAL DU CHANTIER, CHANTIERS À JOUR (F1 0,7902, 237/238)
 M docs/pilotage/references-non-r
… [793 caractères tronqués]
  ```

- **bash** `{"command": "ls reports/ | tail -40; echo ---; ls docs/pilotage/", "description": "List reports and pilotage docs"}`

  ```
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
xnli-32b.json
xnli-32b-l32.json
xnli-3b.json
xnli-3b-l30.json
xnli-entrainement-3b.json
xnli-mlp-3b.json
xnli-train-complet-3b.json
---
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
  ```

- **bash** `{"command": "grep -rn \"g017\" --include=* -l . 2>/dev/null | head -40", "description": "Find files mentioning g017"}`

  ```
[still running after 60000ms; moved to background job bash-3]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **bash** `{"command": "grep -rn \"She said that she would come\" . 2>/dev/null | head -20", "description": "Find the sentence"}`

  ```
[still running after 60000ms; moved to background job bash-4]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-spans-chunker.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-spans-chunker.md</path>
<type>file</type>
<content>
1: # Chunker seul et les 94 spans REL/SUB/GP — 0 exact, deux règles en récupèrent 84 sans perdre un span déjà bon
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Territoire** : **L** (bloc
4: > linguistique, chunker) · **Date** : 2026-11-05 · **Verdict** : sur les **94** cibles du gold
5: > sans segment prédit au bon span (**48 REL, 33 SUB, 13 GP**), le chunker seul
6: > (`Heuristique(segmenter_s=False)`) en couvre **0 exactement** — et c'est structurel : le mode
7: > par défaut est l'union du générateur S et du chunker, donc un span exact du chunker serait déjà
8: > bon. Deux règles simulées sur une copie locale en récupèrent **84/94** (47 REL, 32 SUB, 5 GP),
9: > soit **229/239** cibles au bon span, **sans perdre aucun** des 77 spans déjà exacts du chunker
10: > seul ni des 145 du mode par défaut. Le prix est mesuré : +9 faux positifs pour (a), −201 pour
11: > (b), −207 pour (a)+(b).
12: >
13: > **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (lecture seule),
14: > [`evaluer_gold.py`](../tools/tests/linguistique
… [15511 caractères tronqués]
  ```

- **job_kill** `{"job_id": "bash-3"}`

  ```
requested cancellation of job bash-3
  ```

- **job_kill** `{"job_id": "bash-4"}`

  ```
requested cancellation of job bash-4
  ```

- **grep** `{"pattern": "g017", "path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools"}`

  ```
Found 8 matches

tools/chantier/plan.json
Line 227:    "titre": "Le dernier span g017",
Line 228:    "mandat": "Tâche J6.1 : le dernier span du gold, `g017` (« She said that she would come yesterday. ») — le gold attend la SUB « that she would come » (sans « yesterday »), le bloc l'inclut. Reproduis, propose UNE règle mesurée (l'adverbe final de temps hors de la SUB), vérifie dev/test et l'attachement, fiche `reports/rapport-g017.md` + JSON, commit. Si la règle casse autre chose, écris la fiche du rejet.",
Line 232:      "commande": "test -f reports/rapport-g017.md && echo FICHE-OK",

tools/tests/linguistique/gold_gele.json
Line 1096: "id": "g017",

tools/tests/linguistique/gold.json
Line 1080:    "id": "g017",

tools/tests/linguistique/gold.py
Line 71:     ("g017", "en", "She said that she would come yesterday.",

tools/structures/donnees/mesure-analyseur.json
Line 431:    "id": "g017",

tools/structures/donnees/gold-analyseur.json
Line 343:    "id": "g017",
  ```

- **grep** `{"pattern": "yesterday", "path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique"}`

  ```
Found 15 matches

tools/tests/linguistique/gold.json
Line 1082:    "texte": "She said that she would come yesterday.",
Line 1121:      "texte": "yesterday",

tools/tests/linguistique/gold.py
Line 71:     ("g017", "en", "She said that she would come yesterday.",
Line 73:       ("come", "VERB"), ("yesterday", "ADV")],

tools/tests/linguistique/gold_gele.json
Line 1098: "texte": "She said that she would come yesterday.",
Line 1137: "texte": "yesterday",
Line 3034: "texte": "It rains since yesterday.",
Line 3055: "texte": "yesterday",
Line 3078: "texte": "since yesterday",

tools/tests/linguistique/gold_reel.json
Line 1690:    "texte": "It rains since yesterday.",
Line 1711:      "texte": "yesterday",
Line 1734:      "texte": "since yesterday",

tools/tests/linguistique/gold_reel.py
Line 121:     ("r028", "en", "It rains since yesterday.",
Line 122:      [("It", "PRON"), ("rains", "VERB"), ("since", "PREP"), ("yesterday", "ADV")],
Line 123:      [("GN", "It", "agent"), ("GV", "rains", "prédicat"), ("GP", "since yesterday", "temps", "rains")], {"acte": "assertion"}),
  ```

- **bash** `{"command": "ls tools/tests/linguistique/ && echo --- && ls tools/structures/ && echo --- && ls tools/ | head -60", "description": "List linguistics tools"}`

  ```
anaphore.py
classement_cible.py
classer_gv.py
evaluer_gold.py
gold_gele.json
gold.json
gold.py
gold_reel.json
gold_reel.py
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
replis_cible.py
test_bloc_linguistique.py
---
arbre_svg.py
candidats_corpus.py
construire_donnees.py
donnees
exporter_corpus.py
generateur.py
llm.py
mesure_analyseur.py
mesure_arbre.py
mesure_corpus.py
__pycache__
README.md
serveur.py
static
tests
verifier_corpus.py
---
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
apres-telechargement-k3.sh
archive_sessions.py
audit_drapeaux_harnais.py
banc_complet.py
banc_durci.py
banc-experts.py
banc_lecteur.py
banc_lecture.py
banc-prelire.py

… [652 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold.py", "offset": 55, "limit": 40}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/chantier/plan.json", "offset": 180, "limit": 120}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/gold.py</path>
<type>file</type>
<content>
55:      [("GN", "Le canard", "agent"), ("GV", "est prêt", "prédicat"), ("GP", "à manger", "but", ["prêt", "canard"])], {"acte": "assertion", "double_sens": True}),
56:     ("g013", "fr", "Peux-tu venir ?",
57:      [("Peux-tu", "VERB"), ("venir", "VERB")],
58:      [("GV", "Peux-tu venir", "prédicat")], {"acte": "question", "reponse": "oui"}),
59:     ("g014", "fr", "J'ai vu l'homme avec le télescope.",
60:      [("J'ai", "PRON"), ("vu", "VERB"), ("l'homme", "DET"), ("avec", "PREP"), ("le", "DET"), ("télescope", "NOUN")],
61:      [("GN", "J'ai", "agent"), ("GV", "vu", "prédicat"), ("GN", "l'homme", "patient"),
62:       ("GP", "avec le télescope", "moyen", "vu")], {"acte": "assertion"}),
63:     ("g015", "en", "The cat sleeps.",
64:      [("The", "DET"), ("cat", "NOUN"), ("sleeps", "VERB")],
65:      [("GN", "The cat", "agent"), ("GV", "sleeps", "prédicat")], {"acte": "assertion"}),
66:     ("g016", "en", "The woman saw the man in the park.",
67:      [("The", "DET"), ("woman", "NOUN"), ("saw", "VERB"), ("the", "DET"), ("man", "NOUN"),
68:       ("in", "PREP")
… [1699 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/chantier/plan.json</path>
<type>file</type>
<content>
180:   },
181:   {
182:    "id": "J4.4",
183:    "jour": 4,
184:    "titre": "Coordination A — A6.2 et A8.3b2",
185:    "mandat": "Tâche J4.4 : la coordination A — A6.2 est libre (le MoE local 18 Go existe ; le blocage est la résidence mono-GPU) et A8.3b2 est nommée. **Ne modifie rien dans A** (ni natifs, ni données). Fiche `reports/rapport-coordination-a.md` + JSON : l'état des deux lignes, les commandes, les décisions à prendre.",
186:    "budget_min": 90,
187:    "acceptation": [
188:     {
189:      "commande": "test -f reports/rapport-coordination-a.md && echo FICHE-OK",
190:      "attendu": "FICHE-OK"
191:     }
192:    ]
193:   },
194:   {
195:    "id": "J5.1",
196:    "jour": 5,
197:    "titre": "Le rapport de semaine",
198:    "mandat": "Tâche J5.1 : le rapport de semaine — relis les fiches des jours 1 à 4, écris `reports/rapport-semaine.md` + JSON : les chiffres avant/après (POS, F1, attachement, le produit, l'intégration), les décisions, les rejets, ce qui reste. Mets à jour `docs/pilotage/semaine-autonome.md` (l'état de chaque jour).",
199:    "budget_min": 
… [4574 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1070,1140p' tools/tests/linguistique/gold.json", "description": "Show g017 gold JSON"}`

  ```
"man"
     ],
     "cible": "saw"
    }
   ],
   "pragma": {
    "acte": "assertion"
   }
  },
  {
   "id": "g017",
   "langue": "en",
   "texte": "She said that she would come yesterday.",
   "mots": [
    {
     "texte": "She",
     "pos": "PRON",
     "debut": 0,
     "fin": 3
    },
    {
     "texte": "said",
     "pos": "VERB",
     "debut": 4,
     "fin": 8
    },
    {
     "texte": "that",
     "pos": "CONJ",
     "debut": 9,
     "fin": 13
    },
    {
     "texte": "she",
     "pos": "PRON",
     "debut": 14,
     "fin": 17
    },
    {
     "texte": "would",
     "pos": "AUX",
     "debut": 18,
     "fin": 23
    },
    {
     "texte": "come",
     "pos": "VERB",
     "debut": 24,
     "fin": 28
    },
    {
     "texte": "yesterday",
     "pos": "ADV",
     "debut": 29,
     "fin": 38
    }
   ],
   "segments": [
    {
     "type": "GN",
     "texte": "She",
     "role": "agent",
     "debut": 0,
     "fin": 3
    },
    {
     "type": "GV",
     "texte": "said",
     "role": "prédicat",
     "debut": 4,
     "fin": 8
  ```

- **bash** `{"command": "wc -l tools/bloc_linguistique.py tools/tests/linguistique/evaluer_gold.py tools/porte-bloc-linguistique.sh tools/tests/linguistique/test_bloc_linguistique.py 2>/dev/null; echo ---; cat tools/porte-bloc-linguistique.sh", "description": "Check file sizes and gate script"}`

  ```
2881 tools/bloc_linguistique.py
   307 tools/tests/linguistique/evaluer_gold.py
    11 tools/porte-bloc-linguistique.sh
   258 tools/tests/linguistique/test_bloc_linguistique.py
  3457 total
---
#!/usr/bin/env bash
# Porte du bloc linguistique — tests de contrat + mesure UDHR (langue/script).
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
echo "=== PORTE BLOC LINGUISTIQUE ==="
python3 -m unittest discover -s tools/tests/linguistique -p 'test_bloc_linguistique.py' || { echo "❌ tests"; exit 1; }
python3 tools/bloc_linguistique.py --autotest --udhr data/udhr/articles.jsonl --sortie /tmp/bloc-linguistique-porte.json || { echo "❌ autotest"; exit 1; }
python3 tools/tests/linguistique/gold.py >/dev/null || { echo "❌ gold"; exit 1; }
python3 tools/tests/linguistique/evaluer_gold.py --json /tmp/pensee-gold-porte.json >/dev/null || { echo "❌ évaluation gold"; exit 1; }
echo "✅ porte bloc linguistique verte"
  ```

- **grep** `{"path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "pattern": "SUB|adverbe|ADV|fronti|yesterday|demain|hier"}`

  ```
Found 62 matches

tools/bloc_linguistique.py
Line 24:     python3 tools/bloc_linguistique.py --mode parallele --fichier page.txt --json
Line 313:         "ADV": set("ne n pas plus jamais rien très bien mal ici hier demain aujourd'hui peut-être fort souvent toujours déjà encore tard tôt ainsi alors aussi".split()),
Line 322:         "ADV": set("not never very well here yesterday today tomorrow often always already still too late out maybe hard far again now down outside".split()),
Line 377: # les subordonnants qui n'ont pas d'antécédent : toujours SUB
Line 383: SUBORDONNANTS = {"because", "although", "though", "if", "while", "as", "since", "unless",
Line 386: # marqueurs **ambigus** : relatifs après un GN (« The day when we left »), SUB ailleurs
Line 389: SUB_PAR_LANGUE = {"fr": {"car", "parce", "puisque", "comme", "quand", "si", "lorsque"},
Line 478: # adverbes de **temps** (circonstants finaux) : le gold les laisse hors du GV
Line 479: # (« Tu viens | demain », r010, r030) ; la négation (« ne dort pas ») n'en est pas un.
Line 480: ADVERBES_TEMPS = {"hier", "demain", "aujourd'hui", "maintenant", "yesterday", "tomorrow",
Line 484: ADVERBES_SEULS = {"peut-être", "vite", "bien", "mal"
… [4439 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' tools/tests/linguistique/evaluer_gold.py", "description": "Read evaluator start"}`

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
… [3743 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 120, "offset": 1180}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 120, "offset": 1370}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
1180:     @staticmethod
1181:     def _verbes_proches(texte: str, segment: dict, gvs: list[dict],
1182:                         k: int = 3, verbes: list[tuple[int, int, str]] | None = None,
1183:                         cache: dict | None = None) -> list[str]:
1184:         """Les verbes des `k` GV les plus proches — les **candidats** d'attachement."""
1185:         if segment.get("type") == "GV" or not gvs:
1186:             return []
1187:         def ecart(g: dict) -> int:
1188:             if g["fin"] <= segment["debut"]:
1189:                 return segment["debut"] - g["fin"]
1190:             if g["debut"] >= segment["fin"]:
1191:                 return g["debut"] - segment["fin"]
1192:             return 0
1193:         proches: list[str] = []
1194:         for g in sorted(gvs, key=ecart)[:k]:
1195:             v = Heuristique._verbe_gv(texte, g, verbes, cache)
1196:             if v and v not in proches:
1197:                 proches.append(v)
1198:         return proches
1199: 
1200:     def _syntagmes_simple(self, texte: str, langue: str,
1201:             
… [6121 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
1370:                     and (est_verbe(mots[i + 1][0], mots[i + 1][2])
1371:                          or _normaliser(mots[i + 1][2]) in lex.get("AUX", set()))):
1372:                 segments.append({"type": "GN", "role": "agent", "niveau": 0,
1373:                                  "debut": d, "fin": f, "texte": texte[d:f], "candidats": []})
1374:                 i += 1
1375:                 continue
1376:             if (typ == "mot" and n in _suj and i + 1 < len(mots)
1377:                     and (est_verbe(mots[i + 1][0], mots[i + 1][2])
1378:                          or _normaliser(mots[i + 1][2]) in lex.get("AUX", set())
1379:                          or _normaliser(mots[i + 1][2]) in {"ne", "n'", "n’"})):
1380:                 segments.append({"type": "GN", "role": "agent", "niveau": 0,
1381:                                  "debut": d, "fin": f, "texte": texte[d:f], "candidats": []})
1382:                 i += 1
1383:                 continue
1384:             if typ == "mot" and (n in lex.get("AUX", set()) or est_verbe(d, t)
1385:                           
… [7236 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 75, "offset": 1296}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 35, "offset": 470}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
1296:                     while j < len(mots) and mots[j][3] == "mot":
1297:                         m = mots[j][2]
1298:                         aux = _normaliser(m) in AUXILIAIRES
1299:                         if aux:
1300:                             if predicat_vu and not prec_aux:
1301:                                 break      # un AUX après un prédicat ouvre la principale
1302:                             prec_aux = True
1303:                             j += 1
1304:                             continue
1305:                         if est_verbe(mots[j][0], m):
1306:                             if prec_aux:
1307:                                 # verbe plein collé à son auxiliaire : même groupe verbal
1308:                                 predicat_vu = True
1309:                                 prec_aux = False
1310:                                 j += 1
1311:                                 continue
1312:                             verbes_vus += 1
1313:                             if predicat_vu or verbes_vus == 2:
1314:                                 brea
… [3996 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
470: serais serait serions seriez seraient sois soit soyons soyez soient étant
471: ai as a avons avez ont avais avait avions aviez avaient aurai auras aura aurons aurez auront
472: aurais aurait aurions auriez auraient aie aies ait ayons ayez aient ayant eu
473: am is are was were be been being have has had having do does did done
474: would must can could should will shall may might ought cannot
475: """.split())
476: 
477: 
478: # adverbes de **temps** (circonstants finaux) : le gold les laisse hors du GV
479: # (« Tu viens | demain », r010, r030) ; la négation (« ne dort pas ») n'en est pas un.
480: ADVERBES_TEMPS = {"hier", "demain", "aujourd'hui", "maintenant", "yesterday", "tomorrow",
481:                   "today", "now", "later", "soon", "tonight"}
482: 
483: 
484: ADVERBES_SEULS = {"peut-être", "vite", "bien", "mal", "hier", "demain", "aujourd'hui", "ici",
485:                   "là", "souvent", "toujours", "jamais", "déjà", "encore", "enfin", "alors",
486:                   "puis", "donc", "aussi", "très", "trop", "plus", "moins", "maybe", "perhaps"}
487: 

… [837 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '120,307p' tools/tests/linguistique/evaluer_gold.py", "description": "Read evaluator rest"}`

  ```
bloc_langue = par_langue.get(langue, par_langue["fr"])
        for s in phrase["segments"]:
            cibles = s.get("cibles") or ([s["cible"]] if s.get("cible") else [])
            if not cibles:
                continue
            att_n += 1
            bloc_langue["cibles"] += 1
            e = labels.get((s["type"], s["debut"], s["fin"]))
            if e is None:
                continue
            att_labels += 1
            bloc_langue["labels"] += 1
            att = (e.meta or {}).get("attachement") or {}
            cible = (att.get("cible") or "").strip()
            juste = cible == cibles[0]
            if juste:
                att_exact += 1
                bloc_langue["exact"] += 1
            # le gold admet parfois plusieurs cibles (43/96 GP) : mesure secondaire
            if cible in cibles:
                att_exact_any += 1
            # le gold mêle deux conventions : la cible est un verbe (le gouverneur) ou un nom
            # (l'antécédent d'un REL, la tête d'un GP). On mesure les deux séparément — en
            # suivant le **POS du gold** (plus fiable que le lexique : « poussent », « aboie »
            # y sont VERB), avec `_est_verbe` en repli si
… [9629 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, json\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nfrom tests.linguistique.evaluer_gold import charger\np=[x for x in charger() if x['id']=='g017'][0]\na=bl.Heuristique().analyser(p['text … [431 caractères tronqués]`

  ```
texte: She said that she would come yesterday.
gold segments: [('GN', 0, 3, 'She', None), ('GV', 4, 8, 'said', None), ('SUB', 9, 28, 'that she would come', ['said'])]
pred segments:
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 12, in <module>
AttributeError: 'Etiquette' object has no attribute 'texte'
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"class Etiquette\" -A 30 tools/bloc_linguistique.py | head -45", "description": "Inspect Etiquette class"}`

  ```
68:class Etiquette:
69-    niveau: str
70-    type: str
71-    valeur: str
72-    debut: int
73-    fin: int
74-    source: str = "heuristique"
75-    confiance: float = 0.5
76-    candidats: list[str] = field(default_factory=list)
77-    langue: str = "und"
78-    script: str = SCRIPT_NEUTRE
79-    meta: dict = field(default_factory=dict)
80-
81-    def json(self) -> dict:
82-        return {
83-            "niveau": self.niveau, "type": self.type, "valeur": self.valeur,
84-            "debut": self.debut, "fin": self.fin, "source": self.source,
85-            "confiance": round(float(self.confiance), 4),
86-            "candidats": list(self.candidats), "langue": self.langue,
87-            "script": self.script, "meta": dict(self.meta),
88-        }
89-
90-
91-SCHEMA_ANNOTATION = "drave.annotation"
92-# v2 : ajoute `meta.partition` et `meta.alternative` (partition des syntagmes qui se
93-# chevauchent). Le format reste additif ; le vérificateur lit encore les annotations v1.
94-VERSION_ANNOTATION = 2
95-
96-
97-@dataclass
98-class Annotation:
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nfrom tests.linguistique.evaluer_gold import charger\np=[x for x in charger() if x['id']=='g017'][0]\na=bl.Heuristique().analyser(p['texte'], p … [426 caractères tronqués]`

  ```
texte: She said that she would come yesterday.
gold segments: [('GN', 0, 3, 'She', None), ('GV', 4, 8, 'said', None), ('SUB', 9, 28, 'that she would come', ['said'])]
pred segments:
  GN 0 3 'She' {'segment': 'She', 'cible': 'said'}
  GV 4 8 'said' None
  SUB 9 38 'that she would come yesterday' {'segment': 'that she would come yesterday', 'cible': 'said'}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat tools/tests/linguistique/gold_split.py", "description": "Read gold split logic"}`

  ```
"""gold_split.py — le gold 612 coupé en **dev** et **test**, de façon déterministe.

Le problème. Toutes les mesures de la session sont **in-sample** : les règles de segmentation et
d'attachement ont été dessinées en regardant les échecs du même gold qui les mesure. Pour juger
une règle, il faut un gold **tenu à l'écart** : on règle sur `dev`, on évalue sur `test`.

Protocole (fixé ici). Le split est un **hash stable de l'identifiant** (`crc32(id) % 3 == 0` →
test, sinon dev), donc reproductible, insensible à l'ordre et indépendant du contenu. Il est
**stratifié par source** (`hand`, `reel`, `synthetique`) et par langue : on vérifie l'équilibre
dans la fiche. Aucune phrase n'est dupliquée entre les deux ; l'union redonne les 612.

Usage :
    from tools.tests.linguistique.gold_split import dev, test, compter
    ph = charger(); d = dev(ph); t = test(ph)
"""
from __future__ import annotations

import zlib

PART_TEST = 3  # une phrase sur trois va au test


def _est_test(phrase: dict) -> bool:
    return zlib.crc32(str(phrase.get("id", "")).encode()) % PART_TEST == 0


def dev(phrases: list[dict]) -> list[dict]:
    """Les phrases de développement (2/3)."""
    return [p for p in phr
… [708 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys,json\nsys.path.insert(0,'tools')\nfrom tests.linguistique.evaluer_gold import charger\nph=charger()\nfor p in ph:\n    for s in p['segments']:\n        if s['type']!='SUB': continue\n        txt=p['texte … [476 caractères tronqués]`

  ```
r210 reel "Bien qu'il soit tard" | last= 'tard' ADV | full: "Bien qu'il soit tard, il travaille."
r218 reel 'Although it is late' | last= 'late' ADV | full: 'Although it is late, he works.'
r264 reel "qu'il vient demain" | last= 'demain' ADV | full: "Je sais qu'il vient demain."
r288 reel 'that he comes tomorrow' | last= 'tomorrow' ADV | full: 'I know that he comes tomorrow.'
r303 reel 'car il est tard' | last= 'tard' ADV | full: 'Je pars car il est tard.'
r313 reel 'because it is late' | last= 'late' ADV | full: 'I leave because it is late.'
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,140p' docs/pilotage/en-cours.md", "description": "Read current state doc"}`

  ```
# En ce moment

**Mis à jour : 2026-11-13, 23 h 10 HNE (heure locale, EST).**

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
… [10314 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nj=json.load(open('reports/pensee-spans-chunker.json'))\nprint(json.dumps({k:v for k,v in j.items() if k not in ('detail','spans','causes')},ensure_ascii=False,indent=1)[:4000])\nEOF", "description": "I … [24 caractères tronqués]`

  ```
{
 "date": "2026-11-05",
 "ligne": "B13",
 "territoire": "L (bloc linguistique, chunker)",
 "objet": "ce que le chunker seul couvre des 94 spans perdus REL/SUB/GP, et deux règles mesurées",
 "verdict": {
  "chunker_seul_sur_94": 0,
  "regle_a_gain": 79,
  "regle_b_gain": 41,
  "regles_ab_gain": 84,
  "exacts_ab_union": 229,
  "cibles": 239,
  "perdus_apres_ab": 10,
  "regression_spans_deja_bons": 0
 },
 "dispositif": {
  "gold": "tools/tests/linguistique/evaluer_gold.py::charger",
  "phrases": 612,
  "cibles": 239,
  "cibles_par_type": {
   "GP": 96,
   "SUB": 69,
   "REL": 74
  },
  "chunker_seul": "Heuristique(segmenter_s=False) — tools/bloc_linguistique.py",
  "copie_locale": "/tmp/spans/bloc_linguistique_copie.py (copie non commitée)",
  "fichiers_du_depot_modifies": 0
 },
 "etat": {
  "defaut": {
   "labels": 145,
   "perdus": 94,
   "perdus_par_type": {
    "GP": 13,
    "SUB": 33,
    "REL": 48
   }
  },
  "chunker_seul": {
   "exacts": 77,
   "par_type": {
    "GP": 77
   },
   "sur_les_94": 0,
   "raison": "le mode par défaut contient déjà le chunker (union) : un span exact du chunker seul serait déjà bon"
  },
  "categories_meme_type": {
   "plus_large": 24,
   "aucun": 6
… [2800 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, json\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nfrom tests.linguistique.evaluer_gold import charger, evaluer_bloc, par_source\nfrom tests.linguistique.gold_split import dev, test, comp … [544 caractères tronqués]`

  ```
all n= 612 seg= {'precision': 0.786, 'rappel': 0.7944, 'f1': 0.7902, 'tp': 1480, 'fp': 403, 'fn': 383, 'tete': {'precision': 0.9261, 'rappel': 0.8808, 'f1': 0.9029, 'tp': 1641, 'fp': 131, 'fn': 222}} att= {'cibles': 239, 'labels': 238, 'exact': 237, 'top1': 237, 'topk': 236, 'exact_taux': 0.9916, 'top1_taux': 0.9916, 'topk_taux': 0.9874, 'couverture': 0.9958}
hand n= 20 seg= {'precision': 0.8333, 'rappel': 0.9821, 'f1': 0.9016, 'tp': 55, 'fp': 11, 'fn': 1, 'tete': {'precision': 0.9492, 'rappel': 1.0, 'f1': 0.9739, 'tp': 56, 'fp': 3, 'fn': 0}} att= {'cibles': 13, 'labels': 12, 'exact': 12, 'top1': 12, 'topk': 12, 'exact_taux': 0.9231, 'top1_taux': 0.9231, 'topk_taux': 0.9231, 'couverture': 0.9231}
reel_new n= 432 seg= {'precision': 0.8118, 'rappel': 0.7612, 'f1': 0.7857, 'tp': 1100, 'fp': 255, 'fn': 345, 'tete': {'precision': 0.9379, 'rappel': 0.8574, 'f1': 0.8959, 'tp': 1239, 'fp': 82, 'fn': 206}} att= {'cibles': 171, 'labels': 171, 'exact': 171, 'top1': 171, 'topk': 170, 'exact_taux': 1.0, 'top1_taux': 1.0, 'topk_taux': 0.9942, 'couverture': 1.0}
synthetique n= 160 seg= {'precision': 0.7035, 'rappel': 0.8978, 'f1': 0.7888, 'tp': 325, 'fp': 137, 'fn': 37, 'tete': {'precision': 0.88
… [1179 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls reports/ | grep -i -E \"convention|adverbe|g017|gv\" ; echo ---; grep -rln \"adverbe final\" reports/*.md | head", "description": "Find prior final-adverb reports"}`

  ```
pensee-convention-doc.json
pensee-convention-gv.json
pensee-conventions.json
pensee-lien-gv.json
pensee-verbe-gv.json
rapport-convention-gv.md
rapport-pensee-convention-doc.md
rapport-pensee-conventions.md
rapport-pensee-lien-gv.md
rapport-pensee-verbe-gv.md
---
reports/rapport-audit-r1r3.md
reports/rapport-audit-v10.md
reports/rapport-coherence-fiches-v8.md
reports/rapport-convention-gv.md
reports/rapport-dev-test-v10.md
reports/rapport-gn-pronom-sujet.md
reports/rapport-pensee-couverture-v7.md
reports/rapport-pensee-v11.md
reports/rapport-pensee-v9.md
reports/rapport-semaine.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"convention\" reports/rapport-*.md | grep -i \"gv\\|adverbe\\|final\" | head -20", "description": "Search convention GV references"}`

  ```
reports/rapport-coherence-fiches.md:129:| convention-doc | convention REL/SUB/GP/GN/GV | antécédent / verbe / nom | idem | T174 + `CONVENTION_CIBLE` | ✅ cohérent |
reports/rapport-convention-gv.md:1:# B13 — la convention des GV : le sujet hors du GV, F1 0,7549 → 0,7902
reports/rapport-convention-gv.md:15:> (T110–T115, T156 recalés) ; JSON [`pensee-convention-gv.json`](pensee-convention-gv.json).
reports/rapport-convention-gv.md:70:  n'est donc pas une correction locale : c'est **la convention du gold**.
reports/rapport-convention-gv.md:71:- **L'adverbe final n'est pas une convention unique** : 39 GV du gold finissent par un `ADV`,
reports/rapport-convention-gv.md:150:convention du § 2, pas un défaut de la règle.
reports/rapport-convention-gv.md:189:la même convention, vue sur les mêmes phrases. Le test ne bouge pas contre la règle, mais il ne
reports/rapport-convention-gv.md:194:1. **Le gold est la source de la règle.** La convention « le sujet est un GN » est lue dans le
reports/rapport-convention-gv.md:197:2. **L'adverbe final est contradictoire.** `r019`/`r186` et `r051`/`r189` sont deux conventions
reports/rapport-convention-gv.md:220:3. **La convention d'adverbe** : décider et
… [1672 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-convention-gv.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-convention-gv.md</path>
<type>file</type>
<content>
1: # B13 — la convention des GV : le sujet hors du GV, F1 0,7549 → 0,7902
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée) · **Tâche** : J1.2 · **Date** : 2026-11-07 ·
4: > **Verdict** : ✅
5: > Les **322 FP / 180 FN** du plan sont les erreurs **de GV** du gold d'avant `r035` (F1 0,7533) ;
6: > après `r035` (J1.1), la base courante est **320 FP / 179 FN** (F1 0,7549). Le classement ne
7: > change pas : **144 FP de sujet (45 %)** dominent, puis 73 d'objet, 39 de troncature. Deux règles
8: > candidates sont mesurées : **le sujet hors du GV** (F1 **+0,0332**, 0 perte d'attachement) et
9: > **l'arrêt à l'adverbe final de temps** (F1 **+0,0026**). Les deux sont **gardées** et combinées :
10: > **F1 0,7549 → 0,7902** (dev **0,7875**, test **0,7962**), **POS 0,8625 inchangée**, **attachement
11: > 237/238 inchangé** (0 cible perdue), **183/183 portes**. S/D/N2 intouchés.
12: >
13: > **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_sujet_hors_gv`,
14: > `ADVERBES_TEMPS`, la condition d'adverbe du GV), [`autotest.py`](../tools/pensee/a
… [14817 caractères tronqués]
  ```

- **bash** `{"command": "mkdir -p /tmp/g017 && cp tools/bloc_linguistique.py /tmp/g017/bloc_g017.py && cd /tmp/g017 && python3 - <<'EOF'\nimport re, pathlib\np=pathlib.Path('bloc_g017.py')\ns=p.read_text()\nold='''                        j += 1\n                    segments.append({\"type\": stype,'''\nnew='''  … [1781 caractères tronqués]`

  ```
patched
all seg {'precision': 0.8664, 'rappel': 0.7762, 'f1': 0.8188, 'tp': 1446, 'fp': 223, 'fn': 417} att {'cibles': 239, 'labels': 224, 'exact': 212, 'exact_taux': 0.887, 'couverture': 0.9372}
dev seg {'precision': 0.8617, 'rappel': 0.7647, 'f1': 0.8103, 'tp': 991, 'fp': 159, 'fn': 305} att {'cibles': 163, 'labels': 152, 'exact': 145, 'exact_taux': 0.8896, 'couverture': 0.9325}
test seg {'precision': 0.8767, 'rappel': 0.8025, 'f1': 0.8379, 'tp': 455, 'fp': 64, 'fn': 112} att {'cibles': 76, 'labels': 72, 'exact': 67, 'exact_taux': 0.8816, 'couverture': 0.9474}
hand seg {'precision': 0.8868, 'rappel': 0.8393, 'f1': 0.8624, 'tp': 47, 'fp': 6, 'fn': 9} att {'cibles': 13, 'labels': 11, 'exact': 11, 'exact_taux': 0.8462, 'couverture': 0.8462}
reel_new seg {'precision': 0.8591, 'rappel': 0.7467, 'f1': 0.799, 'tp': 1079, 'fp': 177, 'fn': 366} att {'cibles': 171, 'labels': 158, 'exact': 151, 'exact_taux': 0.883, 'couverture': 0.924}
synthetique seg {'precision': 0.8889, 'rappel': 0.884, 'f1': 0.8864, 'tp': 320, 'fp': 40, 'fn': 42} att {'cibles': 55, 'labels': 55, 'exact': 50, 'exact_taux': 0.9091, 'couverture': 1.0}
CHANGE g005 hand "Elle a dit qu'elle viendrait hier."
  gold [('GN', 0, 
… [864 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONPATH=/tmp/g017 python3 - <<'EOF'\nimport sys\nsys.path.insert(0,'/tmp/g017'); sys.path.insert(0,'tools')\nimport bloc_linguistique as base\nimport bloc_g017 as new\nfrom tests.linguistique.evaluer_gold import charger\nph=charge … [1043 caractères tronqués]`

  ```
changed phrases 4 base segs 16 new segs 14
g005 "Elle a dit qu'elle viendrait hier."
g017 'She said that she would come yesterday.'
r264 "Je sais qu'il vient demain."
r288 'I know that he comes tomorrow.'
sub-end-adv g005 SUB "qu'elle viendrait hier" hier
sub-end-adv g017 SUB 'that she would come yesterday' yesterday
sub-end-adv r264 SUB "qu'il vient demain" demain
sub-end-adv r288 SUB 'that he comes tomorrow' tomorrow
total sub/rel ending adv 4
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,66p' tools/bloc_linguistique.py", "description": "Read bloc imports"}`

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
… [1412 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"sys.path\\|import generateur\\|from generateur\\|RACINE\" tools/bloc_linguistique.py | head -40", "description": "Find sys.path/import in bloc"}`

  ```
49:RACINE = pathlib.Path(__file__).resolve().parent.parent
990:            if str(RACINE / "tools/structures") not in sys.path:
991:                sys.path.insert(0, str(RACINE / "tools/structures"))
992:            import generateur  # le générateur S, importé en lecture seule
1007:            import generateur
2852:    ap.add_argument("--modele", default=str(RACINE / "models/Qwen2.5-0.5B-Q4_0.gguf"))
2857:    ap.add_argument("--udhr", default=str(RACINE / "data/udhr/articles.jsonl"))
  ```

- **bash** `{"command": "cd /tmp/g017 && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('bloc_g017.py'); s=p.read_text()\nold='RACINE = pathlib.Path(__file__).resolve().parent.parent'\nnew=\"RACINE = pathlib.Path('/home/stephane/Data13TB/stephane/GitHub/Qtrinet')\"\nassert s.count(old)==1\np.write_text(s.rep … [1478 caractères tronqués]`

  ```
racine patched
base all seg {'precision': 0.786, 'rappel': 0.7944, 'f1': 0.7902, 'tp': 1480, 'fp': 403, 'fn': 383} att {'cibles': 239, 'labels': 238, 'exact': 237, 'exact_taux': 0.9916, 'couverture': 0.9958}
base dev seg {'precision': 0.7887, 'rappel': 0.7863, 'f1': 0.7875, 'tp': 1019, 'fp': 273, 'fn': 277} att {'cibles': 163, 'labels': 162, 'exact': 161, 'exact_taux': 0.9877, 'couverture': 0.9939}
base test seg {'precision': 0.78, 'rappel': 0.8131, 'f1': 0.7962, 'tp': 461, 'fp': 130, 'fn': 106} att {'cibles': 76, 'labels': 76, 'exact': 76, 'exact_taux': 1.0, 'couverture': 1.0}
base hand seg {'precision': 0.8333, 'rappel': 0.9821, 'f1': 0.9016, 'tp': 55, 'fp': 11, 'fn': 1} att {'cibles': 13, 'labels': 12, 'exact': 12, 'exact_taux': 0.9231, 'couverture': 0.9231}
base reel_new seg {'precision': 0.8118, 'rappel': 0.7612, 'f1': 0.7857, 'tp': 1100, 'fp': 255, 'fn': 345} att {'cibles': 171, 'labels': 171, 'exact': 171, 'exact_taux': 1.0, 'couverture': 1.0}
base synthetique seg {'precision': 0.7035, 'rappel': 0.8978, 'f1': 0.7888, 'tp': 325, 'fp': 137, 'fn': 37} att {'cibles': 55, 'labels': 55, 'exact': 54, 'exact_taux': 0.9818, 'couverture': 1.0}
regle all seg {'precision': 0.7863, 'rapp
… [2027 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys\nsys.path.insert(0,'tools')\nfrom tests.linguistique.evaluer_gold import charger\nfrom tests.linguistique.gold_split import dev,test\nph=charger(); d={p['id'] for p in dev(ph)}; t={p['id'] for p in test( … [201 caractères tronqués]`

  ```
g005 dev
g017 dev
r264 test
r288 test
r210 dev
r218 dev
r303 dev
r313 dev
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"J6\\|g017\\|s065\" docs/pilotage/semaine-autonome.md docs/pilotage/plan-travail.md journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md 2>/dev/null | head -60", "description": "Find J6 context in plans"}`

  ```
docs/pilotage/semaine-autonome.md:25:| 1 span (`g017` arbitrage d'adverbe) ; `r035` relative zéro **réglé** | attachement exact **237/238 (0,9958)** | [`rapport-r035.md`](../../reports/rapport-r035.md) |
docs/pilotage/semaine-autonome.md:87:| **J1 · 07/11** | matin | le produit : le **span `g017`**, la **convention des GV** | attachement et F1, fiche v13 |
docs/pilotage/semaine-autonome.md:176:| **J1** | matin : `r035` + convention GV | ✅ fait | exact **237/238**, couverture **0,9958**, F1 **0,7533 → 0,7902**, POS inchangée | `25a6c0ff`, `92652984` | `g017`, `s065`, objet (75 FP / 51 FN), 5 FP sujet |
docs/pilotage/semaine-autonome.md:194:**Ce que la semaine n'a pas produit.** Le **deuxième span** (`g017`), la **preuve** de la théorie
docs/pilotage/plan-travail.md:456:**Reste** : 3 spans (`r035`, `r264`, `g017`), les inventaires N2/S/R/A, la restitution.
journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md:19:- **Prochaine action** : les 2 spans restants (`r035`, `g017`) ; la convention des GV ; les deux états N2/S/R/A sont intégrés.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md 2>/dev/null | head -120", "description": "Read Pensée session plan"}`

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
- **Heartbeat** : 2026-11-07 01:2
… [5574 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys,json\nsys.path.insert(0,'tools')\nfrom tests.linguistique.evaluer_gold import charger\nph=charger()\nfor i in ['g005','g017','r264','r288','r210','r303']:\n    p=[x for x in ph if x['id']==i][0]\n    pri … [224 caractères tronqués]`

  ```
g005 "Elle a dit qu'elle viendrait hier."
   [('GN', "'Elle'", 'agent', None), ('GV', "'a dit'", 'prédicat', None), ('SUB', '"qu\'elle viendrait"', 'contenu', ['dit'])]
g017 'She said that she would come yesterday.'
   [('GN', "'She'", 'agent', None), ('GV', "'said'", 'prédicat', None), ('SUB', "'that she would come'", 'contenu', ['said'])]
r264 "Je sais qu'il vient demain."
   [('GN', "'Je'", 'agent', None), ('GV', "'sais'", 'prédicat', None), ('SUB', '"qu\'il vient demain"', 'complément', ['sais'])]
r288 'I know that he comes tomorrow.'
   [('GN', "'I'", 'agent', None), ('GV', "'know'", 'prédicat', None), ('SUB', "'that he comes tomorrow'", 'complément', ['know'])]
r210 "Bien qu'il soit tard, il travaille."
   [('SUB', '"Bien qu\'il soit tard"', 'concession', ['travaille']), ('GN', "'il'", 'agent', None), ('GV', "'travaille'", 'prédicat', None)]
r303 'Je pars car il est tard.'
   [('GN', "'Je'", 'agent', None), ('GV', "'pars'", 'prédicat', None), ('SUB', "'car il est tard'", 'cause', ['pars'])]
  ```

- **bash** `{"command": "set -e\ncd /tmp/g017\ncp /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py bloc_placebo.py\ncp /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py bloc_garde.py\npython3 - <<'EOF'\nimport pathlib\nroot=\"/home/stephane/Data13TB/stephane/Gi … [2364 caractères tronqués]`

  ```
wrote bloc_placebo.py
wrote bloc_garde.py
base all: F1=0.7902 tp=1480 fp=403 fn=383 att=237/238 cov=0.9958 | dev: F1=0.7875 tp=1019 fp=273 fn=277 att=161/162 cov=0.9939 | test: F1=0.7962 tp=461 fp=130 fn=106 att=76/76 cov=1.0
blanket all: F1=0.7901 tp=1479 fp=402 fn=384 att=236/237 cov=0.9916 | dev: F1=0.7886 tp=1020 fp=271 fn=276 att=162/163 cov=1.0 | test: F1=0.7934 tp=459 fp=131 fn=108 att=74/74 cov=0.9737
garde all: F1=0.7909 tp=1481 fp=401 fn=382 att=238/239 cov=1.0 | dev: F1=0.7886 tp=1020 fp=271 fn=276 att=162/163 cov=1.0 | test: F1=0.7962 tp=461 fp=130 fn=106 att=76/76 cov=1.0
placebo all: F1=0.7107 tp=1372 fp=626 fn=491 att=159/160 cov=0.6695 | dev: F1=0.7069 tp=943 fp=429 fn=353 att=107/107 cov=0.6564 | test: F1=0.7192 tp=429 fp=197 fn=138 att=52/53 cov=0.6974
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && bash tools/porte-bloc-linguistique.sh 2>&1 | tail -20", "description": "Run bloc linguistique gate baseline", "timeoutMs": 300000}`

  ```
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
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"g017\\|qu'elle viendrait\\|would come\\|vient demain\\|comes tomorrow\" tools/pensee/autotest.py tools/tests/linguistique/test_bloc_linguistique.py tools/tests/linguistique/*.py | head -40", "description": "Find test refer … [24 caractères tronqués]`

  ```
tools/tests/linguistique/gold.py:29:    ("g005", "fr", "Elle a dit qu'elle viendrait hier.",
tools/tests/linguistique/gold.py:31:     [("GN", "Elle", "agent"), ("GV", "a dit", "prédicat"), ("SUB", "qu'elle viendrait", "contenu", ["dit"])], {"acte": "assertion"}),
tools/tests/linguistique/gold.py:71:    ("g017", "en", "She said that she would come yesterday.",
tools/tests/linguistique/gold.py:74:     [("GN", "She", "agent"), ("GV", "said", "prédicat"), ("SUB", "that she would come", "contenu", ["said"])],
tools/tests/linguistique/gold_reel.py:844:    ('r264', 'fr', "Je sais qu'il vient demain.",
tools/tests/linguistique/gold_reel.py:846:     [('GN', 'Je', 'agent'), ('GV', 'sais', 'prédicat'), ('SUB', "qu'il vient demain", 'complément', 'sais')], {'acte': 'assertion'}),
tools/tests/linguistique/gold_reel.py:916:    ('r288', 'en', 'I know that he comes tomorrow.',
tools/tests/linguistique/gold_reel.py:918:     [('GN', 'I', 'agent'), ('GV', 'know', 'prédicat'), ('SUB', 'that he comes tomorrow', 'complément', 'know')], {'acte': 'assertion'}),
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"T110\\|T111\\|T112\\|T113\\|T114\\|T115\\|T156\\|183\\|SUB\" tools/pensee/autotest.py | head -60", "description": "Inspect autotest SUB tests"}`

  ```
2408:    """Les spans perdus : 9 REL, 5 SUB, 4 GP (18)."""
2423:    return (cats["REL"] == 0 and cats["SUB"] == 1 and cats["GP"] == 0), (
2424:        f"spans : {cats['REL']} REL, {cats['SUB']} SUB, {cats['GP']} GP")
2544:    attendus = {"REL", "SUB", "GP", "GN", "GV"}
2573:    """La règle du segment précédent : SUB après un GV → le verbe gouverneur."""
2584:            if s["type"] != "SUB":
2758:              ("T110 segmenteur", t110_segmenteur),
2759:              ("T111 hybride segmenteur", t111_hybride_seg),
2760:              ("T112 union segmenteurs", t112_union),
2761:              ("T113 union par défaut", t113_union_defaut),
2762:              ("T114 cascade + union", t114_cascade_union),
2763:              ("T115 tête cascade", t115_tete_cascade),
2804:              ("T156 relation GN-GV", t156_relation),
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '2370,2440p' tools/pensee/autotest.py && echo ==== && sed -n '2800,2880p' tools/pensee/autotest.py", "description": "Read autotest span tests"}`

  ```
cibles = s.get("cibles") or ([s["cible"]] if s.get("cible") else [])
            if not cibles:
                continue
            e = labels.get((s["type"], s["debut"], s["fin"]))
            if e is None:
                span += 1
                continue
            if not any(any(c in nom for c in cibles) for nom in (e.candidats or [])):
                cible += 1
    return span == 1 and cible == 2, (
        f"échecs : {span} de span, {cible} de cible (33 avant les correctifs)")


def t164_verbe_gv() -> tuple[bool, str]:
    """Le verbe du GV-phrase : le POS VERB, pas le dernier mot."""
    import tools.bloc_linguistique as bl
    from ..tests.linguistique.evaluer_gold import charger, evaluer_bloc
    h = bl.Heuristique()
    a = h.analyser("The boy saw the cat in the park.", "en")
    gp = [e for e in a.etiquettes if e.niveau == "syntagme" and e.type == "GP"]
    cible = ((gp[0].meta or {}).get("attachement") or {}).get("cible") if gp else None
    r = evaluer_bloc("h", bl.Heuristique(), charger())["attachement"]
    return cible == "saw" and r["exact"] == 237, (
        f"verbe du GV : {cible} (attendu saw) ; exact {r['exact']}/239")


def t165_lexique_verbal() -> tuple[b
… [5195 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rln \"rejet\" reports/rapport-*.md | head -20 && echo --- && grep -rn \"g017\" reports/*.md | head -30", "description": "Find prior rejection sheets and g017 mentions"}`

  ```
reports/rapport-audit-v2.md
reports/rapport-capteur-hebbien.md
reports/rapport-cerveau-modules.md
reports/rapport-coherence-fiches-v7.md
reports/rapport-coherence-fiches-v8.md
reports/rapport-convention-gv.md
reports/rapport-corpus-commun.md
reports/rapport-dev-test-v10.md
reports/rapport-dev-test-v7.md
reports/rapport-e9-homeostasie.md
reports/rapport-gn-pronom-sujet.md
reports/rapport-inventaire-panini.md
reports/rapport-ocr-pdf.md
reports/rapport-pensee-attachement-v2.md
reports/rapport-pensee-defaut-niveau.md
reports/rapport-pensee-fusion-reparee.md
reports/rapport-pos-anglais.md
reports/rapport-pos-ponctuation.md
reports/rapport-pos-r4-integre.md
reports/rapport-pos-r4.md
---
reports/rapport-audit-r1r3.md:121:- **R1c** — gains : `r224 r291` (dev), `r115 r239` (test) ; **perte** : `g017` (dev).
reports/rapport-audit-r1r3.md:147:### 3.4 R1c — le second prédicat : +4, mais `g017` perdu
reports/rapport-audit-r1r3.md:151:`verbes_vus`**. La garde d'adverbe final teste `verbes_vus >= 1`. Sur `g017` (« that she would
reports/rapport-audit-r1r3.md:153:dans la SUB, span prédit `[9:38]` au lieu de `[9:28]`. En enlevant R1c, `g017` redevient
reports/rapport-audit-r1r3.md:212:  **23 sont i
… [3740 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '100,170p' reports/rapport-audit-r1r3.md && echo ===== && sed -n '250,280p' reports/rapport-audit-r1r3.md && echo ===== && sed -n '380,450p' reports/rapport-audit-r1r3.md", "description": "Read g017 history in audit r1r3"}`

  ```
| ablation | labels | exact | Δ exact | gains dev/test | pertes dev/test | F1 vivant (Δ) |
|---|---:|---:|---:|---:|---:|---:|
| **R1a** `SUJETS` (pronom) | 203 | 203 | −9 | 12 / 3 | **3 / 3** | 0,5643 (−0,0077) |
| **R1b** modaux | 211 | 211 | −1 | 1 / 0 | 0 / 0 | 0,5711 (−0,0009) |
| **R1c** second prédicat | 209 | 209 | −3 | 2 / 2 | **1 / 0** | 0,5685 (−0,0035) |
| **R1** (R1a+R1b+R1c) | 199 | 199 | −13 | 14 / 5 | **3 / 3** | 0,5602 (−0,0118) |
| **R2** SUB sans précédent | 209 | 209 | −3 | 4 / 0 | **1 / 0** | 0,5704 (−0,0016) |
| **R3a** subordonnants par langue | 212 | 212 | **0** | 0 / 0 | 0 / 0 | 0,5720 (0) |
| **R3c** `fall`/`call` | 212 | 210 | **−2** | 2 / 0 | 0 / 0 | 0,5688 (−0,0032) |
| *tout éteint* | 196 | 195 | −17 | 19 / 5 = 24 | **4 / 3 = 7** | 0,5555 (−0,0165) |
| *R3a fidèle (contrefactuel)* | 213 | 213 | +1 | 1 / 0 | 0 / 0 | 0,5727 (+0,0007) |

> **R3a fidèle** n'est pas le code livré : c'est la règle d'A17 appliquée pour de vrai
> (`SUBORDONNANTS − {car}` en anglais, dans les quatre usages de `_syntagmes_simple`). Elle
> récupère **r280** (+1 exact). Le code livré, lui, ne fait rien (voir § 3.6).

### 3.1 Identifiants

- **R1a** — gains : `r034 r074 r114 r205 r
… [10366 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '140,200p' reports/rapport-audit-v10.md && echo ===== && sed -n '260,330p' reports/rapport-audit-v10.md", "description": "Read g017 history in audit v10"}`

  ```
**1 perte** (`r303`), soit **+7 = 219**. La différence est `r303`, perdue.
- **`predicat_vu` n'est pas un gain net** : il rouvre `g017` mais **ferme `r303`**
  (`car il est tard`, SUB `[8:23]` → `[8:18]`). Net **0** exact, **0** F1 ; la fiche ne
  mentionne pas la perte, et le dev 152/152 cache l'échange.

## 4. Ablations — l'effet réel de chaque correction

**Lecture.** On part du code v10 (220 exacts). « Gain » = cible exacte du code livré qui
**cesse** de l'être quand on retire la règle ; « perte » = cible exacte **rétablie** quand on
la retire. `F1` = union sur le **gelé 602**. Les identifiants sont `phrase:type`.

| ablation | labels | exact | Δ exact | gains | pertes | F1 gelé (Δ) | top-k | spans | dev | test |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **garde PRON** (retirée, SUJETS relatifs conservés) | 203 | 203 | **−17** | **17** | 0 | 0,5718 (−0,0162) | 202 | 36 (18 REL, 14 SUB) | 138/138 | 65/65 |
| **expansion SUJETS** (retirée, garde conservée) | 214 | 214 | **−6** | 6 | 0 | 0,5833 (−0,0047) | 213 | 25 (15 REL, 6 SUB) | 149/149 | 65/65 |
| **PRON + SUJETS** (les deux retirées) | 214 | 214 | **−6** | 6 | 0 | 0,5808 (−0,0072) | 213 | 25 (15 REL, 6 SUB) |
… [7659 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"verbes_vus\\|predicat_vu\" tools/bloc_linguistique.py", "description": "Find predicate guards"}`

  ```
1293:                    verbes_vus = 0
1295:                    predicat_vu = False   # un prédicat a déjà été vu dans la clause
1300:                            if predicat_vu and not prec_aux:
1308:                                predicat_vu = True
1312:                            verbes_vus += 1
1313:                            if predicat_vu or verbes_vus == 2:
1315:                            predicat_vu = True
1318:                                predicat_vu = True   # « is red » : copule + attribut
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -15 -- tools/bloc_linguistique.py && git log -S \"verbes_vus\" --oneline -- tools/bloc_linguistique.py | head -20", "description": "Git history of predicate guard"}`

  ```
8eb0cc49 B13 — RESTITUTION v0 : 46/46 SURFACES EXACTES, MIROIR STRICT 0,1087, LE MIROIR TROUVE LES SAUTS DE LIGNE
9a259953 B13 — SCHÉMA v2 : meta.partition + meta.alternative, 26 CAS VALIDÉS (0 ÉCHEC), v1 TOUJOURS LUE
92652984 B13 — LA CONVENTION DES GV : SUJET HORS DU GV + ADVERBE FINAL, F1 0,7549 → 0,7902, ATTACHEMENT 237/238 ; 183/183
25a6c0ff B13 — r035 RÉGLÉ : LA RELATIVE ZÉRO, EXACT 236 → 237, POS INCHANGÉE ; 183/183
efbae885 B13 — LE NOM PROPRE SUJET EST UN GN : F1 0,7438 → 0,7535, TÊTE 0,865, ATTACHEMENT 236/237 ; 183/183
295e0d7b B13 — LES PRONOMS SUJETS ANGLAIS AUSSI : F1 0,7013 → 0,7438, TÊTE 0,8561, ATTACHEMENT PRÉSERVÉ ; 183/183
c78a53bd B13 — LE PRONOM SUJET EST UN GN : F1 0,6519 → 0,7013 (+4,9), TÊTE 0,7709 → 0,8141, ATTACHEMENT PRÉSERVÉ (236/237, 0,9916) ; 183/183
5d2fa775 B13 — r264 RÉGLÉ : LE GV S'ARRÊTE AU MARQUEUR ÉLIDÉ (RADICAL qu), EXACT 236/237, COUVERTURE 0,9874 → 0,9916, F1 0,6519 ; 183/183
c43dd5cc B13 — LA RÈGLE « QUE » (PRON APRÈS UN NOM, CONJ AILLEURS) : POS 85,84 → 86,25 %, F1 ET ATTACHEMENT INCHANGÉS ; 183/183
6b976cb1 B13 — R4-FR FILTRÉ (ADJECTIF CONNU OU SUFFIXE) : POS 85,75 → 85,84 %, F1 ET ATTACHEMENT INCHANGÉS ; 183/183
7a45325f B13 — LA PONCTUAT
… [1072 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"pensee/autotest\\|autotest.py\\|183\" tools/toutes-les-portes.sh tools/porte-*.sh 2>/dev/null | head -20", "description": "Check if autotest is a gate"}`

  ```
(no output)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls tools/porte-* | grep -i \"pensee\\|b13\\|lingu\" && sed -n '1,60p' tools/toutes-les-portes.sh", "description": "Inspect gate registry"}`

  ```
tools/porte-bloc-linguistique.sh
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
#   5. il sort e
… [1574 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"g017\\|adverbe\\|SUB\\|237\\|238\\|yesterday\\|demain\" tools/tests/linguistique/test_bloc_linguistique.py", "description": "Check unit tests for g017"}`

  ```
34:        ni de la préposition. Une préposition avec complément, un adverbe ou l'absence de
82:    def test_adverbe_final_hors_du_gv(self):
83:        """Un circonstant de temps final hors du GV ; la négation et l'adverbe non final restent."""
91:        self.assertIn(("GV", "viens"), syntagmes("Tu viens demain ?"))
92:        self.assertNotIn(("GV", "viens demain"), syntagmes("Tu viens demain ?"))
94:        # « demain matin » : l'adverbe n'est pas final, le GV n'est pas coupé
95:        self.assertIn(("GV", "viens demain matin"), syntagmes("Tu viens demain matin."))
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"g017\\|would come\\|yesterday\\|237\\|238\\|SUB\" tools/bloc_linguistique.py | tail -40", "description": "Check bloc self-test references"}`

  ```
322:        "ADV": set("not never very well here yesterday today tomorrow often always already still too late out maybe hard far again now down outside".split()),
377:# les subordonnants qui n'ont pas d'antécédent : toujours SUB
383:SUBORDONNANTS = {"because", "although", "though", "if", "while", "as", "since", "unless",
386:# marqueurs **ambigus** : relatifs après un GN (« The day when we left »), SUB ailleurs
389:SUB_PAR_LANGUE = {"fr": {"car", "parce", "puisque", "comme", "quand", "si", "lorsque"},
480:ADVERBES_TEMPS = {"hier", "demain", "aujourd'hui", "maintenant", "yesterday", "tomorrow",
1016:        """REL → tête du GN précédent ; SUB après un GV → son verbe (le gouverneur)."""
1021:        if segment.get("type") == "SUB" and precedent.get("type") == "GV":
1029:        """Les candidats que le **précédent** impose : l'antécédent d'une REL, le verbe d'une SUB."""
1035:        if segment.get("type") == "SUB" and precedent.get("type") == "GV":
1064:        """Sans gouverneur extérieur, une SUB/REL prend son propre verbe (« qu'il viendra »)."""
1065:        if cible or segment.get("type") not in ("SUB", "REL"):
1076:        if not cible or segment.get("type") not in ("GP", "SUB")
… [1605 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp/g017 && python3 - <<'EOF'\nimport pathlib\nroot=\"/home/stephane/Data13TB/stephane/GitHub/Qtrinet\"\ns=pathlib.Path(root+'/tools/bloc_linguistique.py').read_text()\ns=s.replace(\"RACINE = pathlib.Path(__file__).resolve().parent.parent\", f\"RACINE = pathlib.Path('{root}')\")\nol … [1478 caractères tronqués]`

  ```
written
base F1 0.7902 tp/fp/fn 1480 403 383 att 237 / 238 cov 0.9958
blanket F1 0.7901 tp/fp/fn 1479 402 384 att 236 / 237 cov 0.9916
adv_large F1 0.7885 tp/fp/fn 1476 405 387 att 233 / 234 cov 0.9791
garde F1 0.7909 tp/fp/fn 1481 401 382 att 238 / 239 cov 1.0
placebo F1 0.7107 tp/fp/fn 1372 626 491 att 159 / 160 cov 0.6695
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"B13\\|g017\\|s065\" docs/pilotage/roadmap.md | head -40", "description": "Locate B13 in roadmap"}`

  ```
31:| **B — l'intelligence** | langue, pensée, jeux, maîtres, [banc externe](../theorie/glossaire/entrees/banc-externe.md), sémantique, modules | ✅ B1–B12 ; **B1.5 [corpus](../theorie/glossaire/entrees/corpus.md)**, **B12.10, B10.2bis et B11.10 closes** ; le **décodeur** est levé (objectif mot : 32,5 ; JW 26,7), le `z` reste ; **B13** (moteur de pensée) : state store v0 + **AC-3/alpha-bêta** + **[DRVF](../theorie/glossaire/entrees/drvf.md) `thought`** + **[banc](../theorie/glossaire/entrees/banc.md) anytime** + **opérateurs hétérogènes** + **nécessaire** + **labyrinthe** + **[porte](../theorie/glossaire/entrees/porte.md)** + **apprise** + **courbe** + **seule** + **stochastique** + **sto seule** + **ferme** + **minute** + **minute apprise** + **minute seule** + **minute entraînée** + **shaping** + **réseau** + **MLP** + **[professeur](../theorie/glossaire/entrees/professeur.md)** + **sans None** + **correction** + **audit** + **ouverte** + **graines** + **mobile** + **mobile graines** + **bruit** + **bouge** + **bouge graines** + **période** + **phase** + **phase graines** + **aléatoire** + **hasard** + **partielle** + **croyance** + **curiosité** + **observatrice** + **bruitée** + 
… [7738 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"B13\\|g017\\|s065\" docs/pilotage/en-cours.md", "description": "Locate B13 in en-cours"}`

  ```
59:- **Plan** : B13, bloc linguistique.
63:- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement exact 237/238 (0,9958)**, **F1 0,7902**, **1 span + 1 cible fausse** ; **`r035` réglé** ; **convention des GV réglée** (sujet hors du GV + adverbe final : 320/179 → GV F1 0,7549 → 0,7902, 0 perte d'attachement) ; **schéma v2** (26 cas, 0 échec ; v1 lue) ; **restitution v0** (`restituer` : **46/46 surfaces**, miroir **0,1087**, correctif `C`) ; **contrat v1** validé ; frontières, partition, GN ; **`drave` v0**.
66:- **Prochaine action** : **`g017`** ; puis T132/T133, gold 200+.
90:- **Pensée — B13 (actif)** : **183/183**, gold 432 ; pragmatique 130/432 ; **`r035` réglé** (237/238, 0,9958) ; **convention des GV réglée** (F1 **0,7902**, 0 perte d'attachement) ; **schéma v2** publié (26 cas, 0 échec ; `meta.partition`/`meta.alternative`, v1 lue) ; **restitution v0** : **46/46 surfaces**, miroir **0,1087** ; [fiche](../../reports/rapport-restitution-v0.md).
116:| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, gold 432, r035 et convention des GV faits (F1 0,7902, 237/238), schéma v2 publié (v1 lue), restitution v0 (46/46 surfaces, miroir 0
… [331 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"J6\" docs/pilotage/semaine-autonome.md && sed -n '80,105p' docs/pilotage/semaine-autonome.md && sed -n '170,200p' docs/pilotage/semaine-autonome.md", "description": "Read week plan J6 area"}`

  ```
(no output)
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,60p' docs/pilotage/semaine-autonome.md", "description": "Read week plan header"}`

  ```
# Le chantier autonome — une semaine (7 → 14 novembre 2026)

> **Ce que ce document est.** Le **plan du chantier d'une semaine** : tous les travaux ouverts du
> dépôt et l'**intégration avec l'écosystème Panini**. Il dit **quoi**, **dans quel ordre**, **avec
> quels sous-agents**, **comment on mesure**, et **ce qui peut faire échouer**. L'état courant est
> dans [`en-cours.md`](en-cours.md) ; la théorie de la généalogie dans
> [`../theorie/genealogie-des-langues.md`](../theorie/genealogie-des-langues.md) ; la méthode
> Panini/Nipada dans [`../methode/panini-nipada.md`](../methode/panini-nipada.md).
> *À relire chaque matin du chantier.*

## 1. L'objet

**Une semaine, un système utilisable, une intégration mesurée.** Le produit `drave` (CLI, contrat,
porte) est la **priorité** ; l'intégration avec Panini/Nipada est le **second axe** ; les chantiers
N2/S/R/A sont **coordonnés** (jamais écrits par cette session). Chaque vague produit un
**résultat mesuré**, une **fiche** et son **JSON**, la mise à jour de l'**état** et un **commit
vérifié** — jamais une intention.

## 2. L'inventaire — ce qui est ouvert

### 2.1 Drave — le produit (priorité)

| reste | mesure | où |
|---|---|---|
| 1 
… [2846 caractères tronqués]
  ```

- **bash** `{"command": "cat > /tmp/g017/mesure.py <<'PY'\n\"\"\"Mesure de la règle J6.1 — l'adverbe final de temps hors de la SUB.\n\nLe module de base est tools/bloc_linguistique.py (lecture seule). Les variantes sont des copies\ndans /tmp/g017/ dont le RACINE pointe sur le dépôt (sinon le générateur S n'est  … [12017 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "/tmp/g017/mesure.py", line 218, in <module>
    sortie.write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
                      ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib64/python3.13/json/__init__.py", line 242, in dumps
    **kw).encode(obj)
          ~~~~~~^^^^^
  File "/usr/lib64/python3.13/json/encoder.py", line 202, in encode
    chunks = self.iterencode(o, _one_shot=True)
  File "/usr/lib64/python3.13/json/encoder.py", line 263, in iterencode
    return _iterencode(o, 0)
TypeError: keys must be str, int, float, bool or None, not tuple
[exit code: 1]
  ```

- **bash** `{"command": "cd /tmp/g017 && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('mesure.py'); s=p.read_text()\nold='''            \"attachement\": {\n                cle: ((b.get(cle) or n.get(cle)).meta or {}).get(\"attachement\")\n                for cle in sorted(set(b) | set(n))\n                 … [580 caractères tronqués]`

  ```
fixed
écrit /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-g017.json
base {'all': 0.7902, 'dev': 0.7875, 'test': 0.7962} {'all': (237, 238, 0.9958), 'dev': (161, 162, 0.9939), 'test': (76, 76, 1.0)}
regle {'all': 0.7901, 'dev': 0.7886, 'test': 0.7934} {'all': (236, 237, 0.9916), 'dev': (162, 163, 1.0), 'test': (74, 74, 0.9737)}
phrases changées: ['g005', 'g017', 'r264', 'r288']
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nj=json.load(open('reports/pensee-g017.json'))\nprint(json.dumps({k:j[k] for k in ('date','ligne','tache','verdict','reproduction','regle','convention','controles','limites','suite','fichiers')},ensure_ … [423 caractères tronqués]`

  ```
{
 "date": "2026-11-15",
 "ligne": "B13",
 "tache": "J6.1",
 "verdict": {
  "regle": "rejetée",
  "raison": "elle corrige g017 (dev) mais casse r264 et r288 (test) : F1 all −0,0001, test −0,0028, attachement 237/238 → 236/237",
  "f1_avant": 0.7902,
  "f1_apres": 0.7901,
  "delta_f1": -0.0001,
  "dev_avant": 0.7875,
  "dev_apres": 0.7886,
  "delta_dev": 0.0011,
  "test_avant": 0.7962,
  "test_apres": 0.7934,
  "delta_test": -0.0028,
  "attachement_avant": "237/238",
  "attachement_apres": "236/237",
  "couverture_avant": 0.9958,
  "couverture_apres": 0.9916
 },
 "reproduction": {
  "phrase": "She said that she would come yesterday.",
  "gold_sub": [
   9,
   28,
   "that she would come"
  ],
  "bloc_sub": [
   9,
   38,
   "that she would come yesterday"
  ],
  "attachement_bloc": {
   "segment": "that she would come yesterday",
   "cible": "said"
  },
  "lecture": "le span est 10 caractères trop long ; la cible d'attachement (said) est déjà juste ; c'est le seul label manquant des 239 cibles"
 },
 "regle": {
  "nom": "adverbe final de temps hors de la SUB",
  "description": "quand le dernier token d'une SUB est un adverbe de ADVERBES_TEMPS (hier, demain, aujourd'hui, maintenant, y
… [5799 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json\nj=json.load(open('reports/pensee-g017.json'))\nfor nom in ('base','regle'):\n    print('==',nom)\n    for split in ('all','dev','test','hand','reel_new','synthetique'):\n        m=j['mesures'][nom][spl … [880 caractères tronqués]`

  ```
== base
all          n=612 F1=0.7902 P=0.7860 R=0.7944 tp/fp/fn=1480/403/383 att=237/238 exact_taux=0.9916 span=0.9958 cov=0.9958 topk=0.9874
dev          n=422 F1=0.7875 P=0.7887 R=0.7863 tp/fp/fn=1019/273/277 att=161/162 exact_taux=0.9877 span=0.9938 cov=0.9939 topk=0.9877
test         n=190 F1=0.7962 P=0.7800 R=0.8131 tp/fp/fn=461/130/106 att=76/76 exact_taux=1.0 span=1.0 cov=1.0 topk=0.9868
hand         n= 20 F1=0.9016 P=0.8333 R=0.9821 tp/fp/fn=55/11/1 att=12/12 exact_taux=0.9231 span=1.0 cov=0.9231 topk=0.9231
reel_new     n=432 F1=0.7857 P=0.8118 R=0.7612 tp/fp/fn=1100/255/345 att=171/171 exact_taux=1.0 span=1.0 cov=1.0 topk=0.9942
synthetique  n=160 F1=0.7888 P=0.7035 R=0.8978 tp/fp/fn=325/137/37 att=54/55 exact_taux=0.9818 span=0.9818 cov=1.0 topk=0.9818
== regle
all          n=612 F1=0.7901 P=0.7863 R=0.7939 tp/fp/fn=1479/402/384 att=236/237 exact_taux=0.9874 span=0.9958 cov=0.9916 topk=0.9833
dev          n=422 F1=0.7886 P=0.7901 R=0.7870 tp/fp/fn=1020/271/276 att=162/163 exact_taux=0.9939 span=0.9939 cov=1.0 topk=0.9939
test         n=190 F1=0.7934 P=0.7780 R=0.8095 tp/fp/fn=459/131/108 att=74/74 exact_taux=0.9737 span=1.0 cov=0.9737 topk=0.9605
hand         n= 20 F1=0.
… [739 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONPATH=/tmp/g017 python3 - <<'EOF'\nimport sys\nsys.path.insert(0,'/tmp/g017'); sys.path.insert(0,'tools')\nimport bloc_linguistique as base, bloc_g017 as regle\nfrom tests.linguistique.evaluer_gold import charger, evaluer_bloc\n … [716 caractères tronqués]`

  ```
POS diff 0 tokens 3749
base 0.8625 {'precision': 0.786, 'rappel': 0.7944, 'f1': 0.7902, 'tp': 1480, 'fp': 403, 'fn': 383, 'tete': {'precision': 0.9261, 'rappel': 0.8808, 'f1': 0.9029, 'tp': 1641, 'fp': 131, 'fn': 222}} {'exact': 237, 'labels': 238, 'exact_taux': 0.9916, 'exact_taux_span': 0.9958, 'couverture': 0.9958, 'topk_taux': 0.9874}
regle 0.8625 {'precision': 0.7863, 'rappel': 0.7939, 'f1': 0.7901, 'tp': 1479, 'fp': 402, 'fn': 384, 'tete': {'precision': 0.9261, 'rappel': 0.8808, 'f1': 0.9029, 'tp': 1641, 'fp': 131, 'fn': 222}} {'exact': 236, 'labels': 237, 'exact_taux': 0.9874, 'exact_taux_span': 0.9958, 'couverture': 0.9916, 'topk_taux': 0.9833}
  ```

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-g017.md", "content": "# B13 — g017 : l'adverbe final hors de la SUB est rejeté (g017 gagné, r264 et r288 perdus)\n\n> **Ligne de roadmap** : **B13** (moteur de pensée) · **Tâche** : J6.1 · **Date** : 2026-11-15 ·\n> **Ver … [12031 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-g017.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-g017.md", "old_string": "4. **Puis J6.2** : `s065` (la cible fausse), qui ramènerait l'attachement à 238/239 si le span\n   `g017` était réglé par la convention.", "new_string": "4. **Puis J6.2** : `s065` (la cible fausse … [234 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-g017.md has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json, pathlib\np=pathlib.Path('reports/pensee-g017.json')\nj=json.loads(p.read_text())\nj['suite'][-1] = (\"Puis J6.2 : s065 (la cible fausse). Avec g017 encore sans label, sa correction donnerait 238/239 \" … [261 caractères tronqués]`

  ```
json suite patched
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '59,68p' docs/pilotage/en-cours.md && echo ==== && sed -n '88,92p' docs/pilotage/en-cours.md && echo ==== && sed -n '114,128p' docs/pilotage/en-cours.md", "description": "Show exact en-cours lines to edit"}`

  ```
- **Plan** : B13, bloc linguistique.
- **Stratégie** : v0 mesuré.
- **Ambition** : un runtime cognitif tracé.
- **Objectif final** : un moteur de pensée v0.
- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement exact 237/238 (0,9958)**, **F1 0,7902**, **1 span + 1 cible fausse** ; **`r035` réglé** ; **convention des GV réglée** (sujet hors du GV + adverbe final : 320/179 → GV F1 0,7549 → 0,7902, 0 perte d'attachement) ; **schéma v2** (26 cas, 0 échec ; v1 lue) ; **restitution v0** (`restituer` : **46/46 surfaces**, miroir **0,1087**, correctif `C`) ; **contrat v1** validé ; frontières, partition, GN ; **`drave` v0**.
- **Ce qu'elle fait** : l'API rejoue le gold (mêmes verdicts).
- **Ce que font les autres** : **N2**, **S**, **hub**.
- **Prochaine action** : **`g017`** ; puis T132/T133, gold 200+.
- **Sous-agents** : 4 mandats, [plan-travail](plan-travail.md) § 9.
- **Bloquants** : 7B locales interdites (règle 11) ; **gold 200+**.
====
- **N2 — en pause** : **1 024** = recette de production ; **2 048 fini** ; la distillation est mesurée (bilan ci-dessus) ; prochaine : la **porte propre (0,29)** ; **GPUs libres** (claim `n2-jour` libéré).
- **N3 — clos** : 17 portes de brique
… [2826 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('docs/pilotage/en-cours.md'); s=p.read_text()\nold = \"- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement exact 237/238 (0,9958)**, **F1 0,7902**, **1 span + 1 cible fausse … [3366 caractères tronqués]`

  ```
en-cours updated
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls journal/ | head -30 && echo --- && ls journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/ && echo --- && ls journal/2026-11* 2>/dev/null | tail -10", "description": "Inspect journal layout"}`

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
---
digest.md
plan.md
rapport.md
session.v4.jsonl.zstd
---
mesures.md
modele.md
portes.md
README.md

journal/2026-11-13:
distribue.md
docs.md
memoire.md
README.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && tail -80 journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md", "description": "Read session journal tail"}`

  ```
- FICHE — LA V12 ANNOTÉE : L'ÉTAT COURANT EST 226/226 APRÈS LE GOLD CORRIGÉ" -- reports/rapport-pensee-v12.md 2>&1 | tail -1   if git log -1 --format='%s' | grep 
- B13 — LA MORPHOLOGIE DU 1ER GROUPE : 10 SPANS RETROUVÉS, EXACT 235/236, COUVERTURE 0,9874, 3 SPANS ; 183/183" -- tools/bloc_linguistique.py tools/pensee/autotes
- DOC PRODUIT — LES CHIFFRES À JOUR : POS 83,83 %, F1 64,74 %, ATTACHEMENT 235/236 (98,33 %), 3 SPANS ; SORTIE D'EVALUER REJOUÉE" -- docs/produit/README.md docs/p
- B13 — LES COMPOSITIONS NE PERDENT PLUS : CASCADE = HEURISTIQUE (0,8383, 235/236), VERDICT COMPARATIF RESTAURÉ ; 183/183" -- tools/bloc_linguistique.py tools/tes
- DOCS — LE LIEN DE LA FICHE COMPOSITION CORRIGÉ" -- docs/pilotage/references-non-regression.md docs/pilotage/en-cours.md 2>&1 | tail -1   if git log -1 --format=
- JOURNAL ET ROADMAP — LA SOIRÉE DES P0 : CONTRAT V1, GOLD CORRIGÉ (226/226), MORPHOLOGIE (235/236), COMPOSITIONS SANS PERTE" -- journal/2026-11-06/README.md docs
- JOURNAL ET ROADMAP — LA SOIRÉE DES P0 : CONTRAT V1, GOLD CORRIGÉ (226/226), MORPHOLOGIE (235/236), COMPOSITIONS SANS PERTE ; ÉTAT HORODATÉ" -- journal/2026-11-0
- B13 — LE PAQUET POS SÛR (CLASSES FERMÉES + R4-EN) : POS 8
… [11676 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat journal/2026-11-13/README.md && echo ===== && cat journal/README.md | head -80", "description": "Read journal conventions"}`

  ```
# 2026-11-13

> **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
> [`journal/2026-11-13/`](README.md). Le récit écrit à la main est conservé plus bas, dans
> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
> [l'index des sessions](../README.md#sessions).

**4 commits** · **1 session(s)** · **3 thème(s)**

## Thèmes du jour

| thème | commits | fichier |
|---|---|---|
| distribue | 1 | [distribue.md](distribue.md) |
| docs | 2 | [docs.md](docs.md) |
| memoire | 1 | [memoire.md](memoire.md) |

## Sessions DSH

| session | titre | début | durée | liens |
|---|---|---|---|---|
| `e181ce02-cd50-488a-a6be-e84b79d40dcc` | Documentation Drave avec diagrammes et implémentation | 2026-10-31 17:40 | 318.4 h | [rapport](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md) · [digest](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md) |

## Tous les commits (heure réelle)

| heure | commit | fait |
|---|---|---|
| 21:31 | `c7f26b35` | DOCS — LA PASSE APRÈS LE CHANTIER : 8 FICHES INDEXÉES, L'ÉTAT PAR JOUR DU PLAN, LE JOURNAL DU CHANTIER, CHANTIERS À JOUR (F1 0,7902, 237/238) |
| 21:35 | `ced21933` | CHANTIER — PHASE 2
… [18383 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,80p' tools/journal_auto.py && echo ==== && sed -n '1,80p' tools/verifie_journal.py", "description": "Inspect journal automation"}`

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
… [6405 caractères tronqués]
  ```

- **bash** `{"command": "date '+%Y-%m-%d %H:%M:%S %Z' && git log -1 --format='%ad' --date=iso", "description": "Check system and last commit date"}`

  ```
2026-11-14 00:49:50 EST
2026-11-13 23:08:01 -0500
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport json, pathlib\n# fiche\np=pathlib.Path('reports/rapport-g017.md'); s=p.read_text()\ns=s.replace('**Tâche** : J6.1 · **Date** : 2026-11-15', '**Tâche** : J6.1 · **Date** : 2026-11-14')\np.write_text(s)\n# jso … [665 caractères tronqués]`

  ```
dates patched
3:> **Ligne de roadmap** : **B13** (moteur de pensée) · **Tâche** : J6.1 · **Date** : 2026-11-14 ·
181:3. **La variante étroite** (passé + modal/conditionnel) est la seule candidate mesurée qui ne
2026-11-14
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls .git/hooks/ | head -20 && echo --- && grep -rn \"journal_auto\\|verifie_journal\" .git/hooks/ tools/*.sh 2>/dev/null | head -20", "description": "Check git hooks for journal automation"}`

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
.git/hooks/pre-commit:25:python3 tools/journal_auto.py --quiet >/dev/null || { echo "  ⛔ journal du jour en échec"; exit 1; }
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat .git/hooks/pre-commit", "description": "Read pre-commit hook"}`

  ```
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
# Le journal du jour, par thème (sources : git + journal/sessions). L'index README est
… [234 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,160p' tools/verifie_etat_a_jour.py", "description": "Read state freshness check"}`

  ```
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
  python3 tools/verifie_etat_a_jour.py --index     # pour le hook
  python3 tools/verifie_eta
… [5141 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls tools/porte-tableaux.sh tools/taille_documents.py tools/verifie_en_cours.py tools/verifie_journal.py tools/verifier_schemas.py 2>/dev/null; echo ---; python3 tools/revue_documentation.py 2>&1 | tail -60", "description": "Run docum … [38 caractères tronqués]`

  ```
tools/porte-tableaux.sh
tools/taille_documents.py
tools/verifie_en_cours.py
tools/verifie_journal.py
tools/verifier_schemas.py
---
  revue de documentation · 719 fiche(s) · 813 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ❌ 3 anomalie(s) :
     · fraîcheur : en-cours.md dit 2026-11-14, le dernier commit date du 2026-11-13
     · compteurs : en-cours.md dit 718 fichiers, le disque en a 719
     · compteurs : en-cours.md dit 812 JSON, le disque en a 813
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('docs/pilotage/en-cours.md'); s=p.read_text()\nold='| fichiers / JSON de résultats | **718** / **812** | `reports/*.md` / `reports/*.json` |'\nnew='| fichiers / JSON de résultats | ** … [301 caractères tronqués]`

  ```
counters updated
  ❌ LA PAGE VIVANTE EST EN RETARD : docs/pilotage/en-cours.md dit « Mis à jour : 2026-11-14 »,
     et le dernier commit date du 2026-11-13.
     → mettre à jour docs/pilotage/en-cours.md (l'état du travail, les questions ouvertes, ce qui est
       nouveau), puis relancer cette porte. Un petit cycle sans page à jour est un cycle
       que personne ne peut lire.
TABLEAUX-0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && bash tools/porte-tableaux.sh > /tmp/g017/porte-tableaux.log 2>&1; echo \"EXIT=$?\"; tail -8 /tmp/g017/porte-tableaux.log", "description": "Run table gate with real exit code", "timeoutMs": 120000}`

  ```
EXIT=1
  ✅ 1779 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 3938 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ❌ LA PAGE VIVANTE EST EN RETARD : docs/pilotage/en-cours.md dit « Mis à jour : 2026-11-14 »,
     et le dernier commit date du 2026-11-13.
     → mettre à jour docs/pilotage/en-cours.md (l'état du travail, les questions ouvertes, ce qui est
       nouveau), puis relancer cette porte. Un petit cycle sans page à jour est un cycle
       que personne ne peut lire.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/taille_documents.py > /tmp/g017/taille.log 2>&1; echo \"TAILLE=$?\"; tail -12 /tmp/g017/taille.log", "description": "Check document budget", "timeoutMs": 120000}`

  ```
TAILLE=1
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4076 mots (budget 4 000)

  avertissements :
     · 47 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 1 violation(s) :
     · T0 : 4076 mots (AGENTS + en-cours + une tâche) > budget 4 000
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifie_en_cours.py > /tmp/g017/encours.log 2>&1; echo \"ENCOURS=$?\"; tail -12 /tmp/g017/encours.log", "description": "Check en-cours state", "timeoutMs": 120000}`

  ```
ENCOURS=0
  en-cours · 1706 mots · 7 sections · 4 session(s) · 8 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifie_journal.py > /tmp/g017/journal.log 2>&1; echo \"JOURNAL=$?\"; tail -12 /tmp/g017/journal.log", "description": "Check journal links", "timeoutMs": 120000}`

  ```
JOURNAL=0
  journal · 45 jour(s) · 179 session(s) · 2415 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifier_schemas.py > /tmp/g017/schemas.log 2>&1; echo \"SCHEMAS=$?\"; tail -8 /tmp/g017/schemas.log", "description": "Check SVG schemas", "timeoutMs": 120000}`

  ```
SCHEMAS=0
  schémas · 463 document(s) · 67 SVG · 2 source(s)
  ✅ aucun ASCII art, SVG valides et référencés, blocs PlantUML inline valides,
     sources et images relatives.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && head -40 /tmp/g017/taille.log", "description": "Inspect budget breakdown"}`

  ```
budget de contexte · documents chargeables
    mots lignes  cat budget  document
    7351    385   T1   9000  docs/pilotage/roadmap.md
    5999    597 DATÉ      0  docs/implantation/contexte-long.md
    4858    515   T1   5000  docs/theorie/glossaire/10-le-pont-linguistico-semantique-le-vocabu.md
    4085    431 DATÉ      0  docs/implantation/numa-segregation.md
    3310    317   T1   3500  README.md
    3072    341 DATÉ      0  docs/implantation/convertisseur.md
    2962    364   T1   5000  docs/theorie/glossaire/02-modeles-et-architectures.md
    2896    352 DATÉ      0  docs/implantation/configuration-nvme-raid-amd.md
    2661    199   T1   2800  reports/README.md
    2404    162   T1   2500  docs/pilotage/references-non-regression.md
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/form
… [519 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"T0\\|AGENTS\\|tache\\|tâche\" tools/taille_documents.py | head -40 && sed -n '1,80p' tools/taille_documents.py", "description": "Inspect T0 budget logic"}`

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
154:        violations.append(f"T0 : {t0} mots (AGENTS + en-cours + une tâche) > budget 4 000")
163:    print(f"  T0 max : {t0} mots (budget 4 000)")
#!/usr/bin/env python3
"""taille_documents.py — le budget de contexte et la cohésion des documents.

Ce que l'outil vérifie :
  1. la taille des documents **chargeables** (T0/T1) en mots, avec un budget par catégorie ;
  2. la cohésion minimale : un titre, un résumé 
… [3262 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport re, pathlib\ns=pathlib.Path('docs/pilotage/en-cours.md').read_text()\nlines=s.splitlines()\nprint('total words',len(re.findall(r'\\S+',s)))\nfor i,l in enumerate(lines,1):\n    w=len(re.findall(r'\\S+',l))\n … [94 caractères tronqués]`

  ```
total words 1706
48 37 - **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référ
63 112 - **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement exact 237/238 (0,9958)**, **F1 0,7902*
79 60 - **Ce qu'elle fait** : **erratum 04/11** : la distillation native ne gagne rien à parité stricte (−
88 36 - **N2 — en pause** : **1 024** = recette de production ; **2 048 fini** ; la distillation est mesur
89 36 - **N3 — clos** : 17 portes de brique vertes (11 h 32, 92 s, 0 rouge) ; inventaire exécutable (`port
90 70 - **Pensée — B13 (actif)** : **183/183**, gold 432 ; pragmatique 130/432 ; **`r035` réglé** (237/238
92 53 - **Panini J2.1/J2.2/J3.1/J3.2** : table **14 atomes** ; UDHR **418/438** ; **J3.1** : script domine
94 30 - **Coordination J4** : N2 **2,9726/2,7856** ; S **7 acceptés / 4 exclus** ; R **0,9475 (+8,49)** ; 
115 36 | **A — le moteur** | **A2.6** | A3.4 Colab ; A5.4 FPGA ; **A6.2 libre** (MoE 18,56 Go, PPL 37,2013 
116 65 | **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, gold 
117 60 | **N — le natif** | **N2, N4** | N2 : **fenêtre 1 024 — 2,3911 / 2,3522 au grand corpus (sous 2,5)*
11
… [537 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '48p;63p;66p;79p;90p;116p' docs/pilotage/en-cours.md", "description": "Show lines to condense"}`

  ```
- **Fait** : types **61/61**, rôles **144/144** ; corpus **8,5 %/65,5 %** ; arbre **99 à ≥3**, référents **294/371**, traduction **14/14** ; page **`/paragraphes`**, **banque 9 paragraphes** ; **56 tests** ; fiches [analyseur](../../reports/rapport-s-analyseur-roles.md), [arbre](../../reports/rapport-s-arbre-referents.md), [limites](../../reports/rapport-s-limites-v6.md), [fait divers](../../reports/rapport-s-fait-divers.md).
- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement exact 237/238 (0,9958)**, **F1 0,7902**, **1 span + 1 cible fausse** ; **`r035` réglé** ; **convention des GV réglée** (sujet hors du GV + adverbe final : 320/179 → GV F1 0,7549 → 0,7902, 0 perte d'attachement) ; **J6.1 : la règle de l'adverbe final hors de la SUB est rejetée** (g017 gagné en dev, r264/r288 perdus en test ; F1 −0,0001, test −0,0028, attachement 237/238 → 236/237 ; [fiche](../../reports/rapport-g017.md)) ; **schéma v2** (26 cas, 0 échec ; v1 lue) ; **restitution v0** (`restituer` : **46/46 surfaces**, miroir **0,1087**, correctif `C`) ; **contrat v1** validé ; frontières, partition, GN ; **`drave` v0**.
- **Prochaine action** : **trancher la convention d'adverbe (`g017`)** ; puis **`
… [1531 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib, re\np=pathlib.Path('docs/pilotage/en-cours.md'); s=p.read_text()\nrepls=[\n(\"- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement exact 237/238 (0,9958)**, **F1 0,7902**, **1 span + 1 cibl … [4164 caractères tronqués]`

  ```
words 1649
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/taille_documents.py > /tmp/g017/taille2.log 2>&1; echo \"TAILLE=$?\"; grep \"T0 max\" /tmp/g017/taille2.log; tail -5 /tmp/g017/taille2.log", "description": "Recheck T0 budget", "timeoutMs": 120000}`

  ```
TAILLE=1
  T0 max : 4019 mots (budget 4 000)
  avertissements :
     · 47 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 1 violation(s) :
     · T0 : 4019 mots (AGENTS + en-cours + une tâche) > budget 4 000
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib, re\np=pathlib.Path('docs/pilotage/en-cours.md'); s=p.read_text()\nold=\"- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 237/238 (0,9958)**, **F1 0,7902**, **1 span + 1 cible fausse** ; … [1151 caractères tronqués]`

  ```
words 1625
TAILLE=0
  T0 max : 3995 mots (budget 4 000)
     · 47 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,8p;59,68p;88,92p;114,128p' docs/pilotage/en-cours.md", "description": "Review updated en-cours"}`

  ```
# En ce moment

**Mis à jour : 2026-11-14, 00 h 50 HNE (heure locale, EST).**

> **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
> plan plus bas (**La carte**).

### Session `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — le hub de reprise du 04/11
- **Plan** : B13, bloc linguistique.
- **Stratégie** : v0 mesuré.
- **Ambition** : un runtime cognitif tracé.
- **Objectif final** : un moteur de pensée v0.
- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 237/238 (0,9958)**, **F1 0,7902**, **1 span + 1 cible fausse** ; **`r035`**, **convention des GV** (0,7902, 0 perte) ; **J6.1 rejetée** (adverbe final hors SUB : g017 gagné, r264/r288 perdus ; test −0,0028, att. 236/237 ; [fiche](../../reports/rapport-g017.md)) ; **restitution v0** (46/46, miroir 0,1087) ; **contrat v1**, **`drave` v0**.
- **Ce qu'elle fait** : l'API rejoue le gold (mêmes verdicts).
- **Ce que font les autres** : **N2**, **S**, **hub**.
- **Prochaine action** : **trancher la convention d'adverbe (`g017`)** ; puis **`s065`** (J6.2), T132/T133, gold 200+.
- **Sous-agents** : 4 mandats, [plan-travail](plan-travail.md) § 9.
- **Bloquants** : 7B locales interdites (règle 
… [3206 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/journal_auto.py --jour 2026-11-14 --dry-run 2>&1 | head -60", "description": "Preview day journal generation"}`

  ```
2026-11-14 : 0 commits
  (sec) journal/2026-11-14/README.md
  (sec) journal/THEMES.md
2 fichiers (simulation) · 0 commits classés
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/journal_auto.py --jour 2026-11-14 2>&1 | head -20 && echo --- && cat journal/2026-11-14/README.md", "description": "Generate day journal and inspect"}`

  ```
2026-11-14 : 0 commits
  journal/2026-11-14/README.md
  journal/THEMES.md
2 fichiers écrits · 0 commits classés
---
# 2026-11-14

> **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
> [`journal/2026-11-14/`](README.md). Le récit écrit à la main est conservé plus bas, dans
> le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
> [l'index des sessions](../README.md#sessions).

**0 commits** · **1 session(s)** · **0 thème(s)**

## Thèmes du jour

| thème | commits | fichier |
|---|---|---|

## Sessions DSH

| session | titre | début | durée | liens |
|---|---|---|---|---|
| `e181ce02-cd50-488a-a6be-e84b79d40dcc` | Documentation Drave avec diagrammes et implémentation | 2026-10-31 17:40 | 319.6 h | [rapport](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md) · [digest](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md) |

## Le récit de la journée (écrit à la main)

<!-- notes -->

<!-- /notes -->
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('journal/2026-11-14/README.md'); s=p.read_text()\nnote = \"\"\"**J6.1 — g017 : la règle de l'adverbe final hors de la SUB est rejetée.** Le bloc inclut\n`yesterday` dans la SUB de `g0 … [991 caractères tronqués]`

  ```
note inserted
JOURNAL=0
  journal · 46 jour(s) · 179 session(s) · 2422 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short | head -40", "description": "Check working tree status"}`

  ```
M docs/pilotage/en-cours.md
 M docs/pilotage/references-non-regression.md
 M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
 M journal/sessions/session-e8c327f2-a7ec-464a-8e40-0615e5befecb/digest.md
 M journal/sessions/session-e8c327f2-a7ec-464a-8e40-0615e5befecb/rapport.md
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
?? journal/2026-11-14/
?? journal/sessions/session-048748b0-e27f-4f44-8706-b882cae40ff4/
?? reports/pensee-g017.json
?? reports/rapport-g017.md
?? reports/rapport-s-paragraphes.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff --stat -- journal/README.md journal/sessions/MANIFEST.md journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md journal/sessions/session-e8c327f2-a7ec … [161 caractères tronqués]`

  ```
journal/README.md                                  |   7 +-
 journal/sessions/MANIFEST.md                       |   7 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md |  95 +++++++++
 .../rapport.md                                     |  14 +-
 .../digest.md                                      | 214 +++++++++++++++++++++
 .../rapport.md                                     |  52 ++++-
 6 files changed, 369 insertions(+), 20 deletions(-)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff --stat -- reports/pensee-coherence-fiches-v7.json reports/pensee-dev-test-v10.json reports/pensee-quatre-modes.json reports/rapport-audit-v7.md reports/rapport-coherence-fiches-v7.md reports/rapport-dev-test-v10.md reports/r … [174 caractères tronqués]`

  ```
docs/pilotage/references-non-regression.md |   2 +-
 reports/pensee-coherence-fiches-v7.json    |  19 +
 reports/pensee-dev-test-v10.json           |   2 +-
 reports/pensee-quatre-modes.json           | 734 ++++++++++++++++-------------
 reports/rapport-audit-v7.md                |   6 +-
 reports/rapport-coherence-fiches-v7.md     |  17 +-
 reports/rapport-dev-test-v10.md            |   2 +-
 reports/rapport-pensee-v12.md              |   4 +-
 reports/rapport-spans-chunker.md           |  13 +-
 tools/chantier/plan.json                   | 116 +++++
 10 files changed, 577 insertions(+), 338 deletions(-)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff -- journal/README.md | head -60", "description": "Inspect journal index diff"}`

  ```
diff --git a/journal/README.md b/journal/README.md
index 32415b60..2ee4eb0d 100644
--- a/journal/README.md
+++ b/journal/README.md
@@ -13,7 +13,7 @@ chaque rapport renvoie à son jour et à `en-cours`.
 
 | jour | index | thèmes |
 |---|---|---|
-| **2026-11-13** | [2026-11-13/README.md](2026-11-13/README.md) | [docs](2026-11-13/docs.md) |
+| **2026-11-13** | [2026-11-13/README.md](2026-11-13/README.md) | [distribue](2026-11-13/distribue.md) · [docs](2026-11-13/docs.md) · [memoire](2026-11-13/memoire.md) |
 | **2026-11-07** | [2026-11-07/README.md](2026-11-07/README.md) | [distribue](2026-11-07/distribue.md) · [docs](2026-11-07/docs.md) · [memoire](2026-11-07/memoire.md) · [mesures](2026-11-07/mesures.md) · [modele](2026-11-07/modele.md) · [portes](2026-11-07/portes.md) |
 | **2026-11-06** | [2026-11-06/README.md](2026-11-06/README.md) | [distribue](2026-11-06/distribue.md) · [docs](2026-11-06/docs.md) · [memoire](2026-11-06/memoire.md) · [mesures](2026-11-06/mesures.md) · [modele](2026-11-06/modele.md) · [moteur](2026-11-06/moteur.md) · [outils](2026-11-06/outils.md) · [portes](2026-11-06/portes.md) |
 | **2026-11-05** | [2026-11-05/README.md](2026-11-05/README.md) | [attention](202
… [4157 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show --stat --oneline dc78f223 | head -30 && echo ==== && git show --stat --oneline a934d779 | head -30", "description": "Inspect previous commit contents"}`

  ```
dc78f223 ÉTAT — T0 DANS LE BUDGET (3 991 MOTS) : LA LIGNE R0.7 PORTE LE TAGGER 612 (0,9475, +8,49, INTÉGRER)
 docs/pilotage/en-cours.md | 4 ++--
 1 file changed, 2 insertions(+), 2 deletions(-)
====
a934d779 R0.7 — LE TAGGER POS SUR LE GOLD 612 : 0,9475 (3012/3179), +8,49 PTS, LA RÈGLE DIT INTÉGRER ; LA CLÉ ÉTAIT PRÉSENTE ET 0,8500 ÉTAIT DATÉ (0,8625)
 docs/pilotage/en-cours.md                          |    8 +-
 journal/2026-11-13/README.md                       |    7 +-
 journal/2026-11-13/docs.md                         |    5 +-
 journal/README.md                                  |    7 +-
 journal/sessions/MANIFEST.md                       |    7 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md |   89 +
 .../rapport.md                                     |   16 +-
 .../digest.md                                      | 1905 +++++++++++++++++
 .../rapport.md                                     |  173 ++
 .../digest.md                                      | 2086 +++++++++++++++++++
 .../rapport.md                                     |  205 ++
 .../digest.md                                      | 1346 ++++++++++++
 .../rapport.md                                     |  142 ++
… [325 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && bash tools/porte-bloc-linguistique.sh > /tmp/g017/porte-bloc.log 2>&1; echo \"EXIT=$?\"; tail -3 /tmp/g017/porte-bloc.log", "description": "Run acceptance gate", "timeoutMs": 300000}`

  ```
EXIT=0
 "ok": true
}
✅ porte bloc linguistique verte
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add reports/rapport-g017.md reports/pensee-g017.json docs/pilotage/en-cours.md journal/2026-11-14/README.md && git status --short | head -30 && echo --- && python3 tools/verifie_etat_a_jour.py --index; echo \"ETAT_INDEX=$?\"", "d … [53 caractères tronqués]`

  ```
M  docs/pilotage/en-cours.md
 M docs/pilotage/references-non-regression.md
A  journal/2026-11-14/README.md
 M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
 M journal/sessions/session-e8c327f2-a7ec-464a-8e40-0615e5befecb/digest.md
 M journal/sessions/session-e8c327f2-a7ec-464a-8e40-0615e5befecb/rapport.md
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
A  reports/pensee-g017.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
A  reports/rapport-g017.md
 M reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/plan.json
 m tools/structures
?? journal/sessions/session-048748b0-e27f-4f44-8706-b882cae40ff4/
?? reports/rapport-s-paragraphes.md
---
  ✅ index : aucun fait stagé sans état
ETAT_INDEX=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git commit -m \"J6.1 — g017 : LA RÈGLE DE L'ADVERBE FINAL HORS SUB EST REJETÉE (G017 GAGNÉ EN DEV, R264/R288 PERDUS EN TEST ; F1 0,7901, TEST −0,0028, ATTACHEMENT 236/237) ; CONVENTION DU GOLD À TRANCHER\" 2>&1 | tail -30; echo \"COM … [104 caractères tronqués]`

  ```
✅ index : aucun fait stagé sans état
[s/v7 b76b888a] J6.1 — g017 : LA RÈGLE DE L'ADVERBE FINAL HORS SUB EST REJETÉE (G017 GAGNÉ EN DEV, R264/R288 PERDUS EN TEST ; F1 0,7901, TEST −0,0028, ATTACHEMENT 236/237) ; CONVENTION DU GOLD À TRANCHER
 14 files changed, 6100 insertions(+), 28 deletions(-)
 create mode 100644 journal/2026-11-14/README.md
 create mode 100644 journal/sessions/session-048748b0-e27f-4f44-8706-b882cae40ff4/digest.md
 create mode 100644 journal/sessions/session-048748b0-e27f-4f44-8706-b882cae40ff4/rapport.md
 create mode 100644 journal/sessions/session-bfa61e65-a77c-4ab8-bce1-72505858a3d5/digest.md
 create mode 100644 journal/sessions/session-bfa61e65-a77c-4ab8-bce1-72505858a3d5/rapport.md
 create mode 100644 reports/pensee-g017.json
 create mode 100644 reports/rapport-g017.md
COMMIT_EXIT=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/revue_documentation.py > /tmp/g017/revue-post.log 2>&1; echo \"REVUE=$?\"; tail -20 /tmp/g017/revue-post.log", "description": "Post-commit documentation review", "timeoutMs": 180000}`

  ```
REVUE=0
  revue de documentation · 719 fiche(s) · 813 JSON · 123 doc(s) · 84 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && bash tools/porte-tableaux.sh > /tmp/g017/tableaux-post.log 2>&1; echo \"TABLEAUX=$?\"; tail -6 /tmp/g017/tableaux-post.log", "description": "Post-commit table gate", "timeoutMs": 120000}`

  ```
TABLEAUX=0
  ✅ 1780 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 3938 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-14)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/taille_documents.py > /tmp/g017/taille-post.log 2>&1; echo \"TAILLE=$?\"; grep \"T0 max\" /tmp/g017/taille-post.log; tail -2 /tmp/g017/taille-post.log", "description": "Post-commit budget check", "timeoutMs": 120000}`

  ```
TAILLE=0
  T0 max : 3995 mots (budget 4 000)

  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 tools/verifie_en_cours.py > /tmp/g017/encours-post.log 2>&1; echo \"ENCOURS=$?\"; tail -2 /tmp/g017/encours-post.log; python3 tools/verifie_journal.py > /tmp/g017/journal-post.log 2>&1; echo \"JOURNAL=$?\"; tail -2 /tmp/g017/ … [90 caractères tronqués]`

  ```
ENCOURS=0
  en-cours · 1625 mots · 7 sections · 4 session(s) · 8 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
JOURNAL=0
  journal · 46 jour(s) · 180 session(s) · 2427 lien(s)
  ✅ un dossier par jour, sessions ancrées, liens relatifs résolus
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show --stat --oneline HEAD | head -25 && echo ==== && git status --short | head -25", "description": "Review commit and remaining changes"}`

  ```
b76b888a J6.1 — g017 : LA RÈGLE DE L'ADVERBE FINAL HORS SUB EST REJETÉE (G017 GAGNÉ EN DEV, R264/R288 PERDUS EN TEST ; F1 0,7901, TEST −0,0028, ATTACHEMENT 236/237) ; CONVENTION DU GOLD À TRANCHER
 docs/pilotage/en-cours.md                          |   16 +-
 journal/2026-11-14/README.md                       |   32 +
 journal/README.md                                  |    9 +-
 journal/sessions/MANIFEST.md                       |    8 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md |  170 ++
 .../rapport.md                                     |   14 +-
 .../digest.md                                      | 1497 +++++++++++++
 .../rapport.md                                     |  157 ++
 .../digest.md                                      | 2314 ++++++++++++++++++++
 .../rapport.md                                     |  150 ++
 .../digest.md                                      |  214 ++
 .../rapport.md                                     |   52 +-
 reports/pensee-g017.json                           | 1295 +++++++++++
 reports/rapport-g017.md                            |  200 ++
 14 files changed, 6100 insertions(+), 28 deletions(-)
====
 M docs/pilotage/references-non-regres
… [383 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && test -f reports/rapport-g017.md && echo FICHE-OK; bash tools/porte-bloc-linguistique.sh 2>&1 | tail -1", "description": "Run plan acceptance commands", "timeoutMs": 300000}`

  ```
FICHE-OK
✅ porte bloc linguistique verte
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nfrom tests.linguistique.evaluer_gold import charger\nh=bl.Heuristique(); ph=charger(); missing=[]\nfor p in ph:\n    a=h.analyser(p['texte'],p … [381 caractères tronqués]`

  ```
383
[('g017', 'SUB', 9, 28, 'that she would come'), ('r004', 'GN', 0, 9, 'Le soleil'), ('r004', 'GV', 10, 16, 'brille'), ('r019', 'GV', 8, 15, 'souffle'), ('r023', 'GV', 3, 7, 'love')]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nfrom tests.linguistique.evaluer_gold import charger\nh=bl.Heuristique(); ph=charger(); missing=[]\nfor p in ph:\n    a=h.analyser(p['texte'],p … [498 caractères tronqués]`

  ```
1
[('g017', 'SUB', 9, 28, 'that she would come', ['said'])]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nfrom tests.linguistique.evaluer_gold import charger\nh=bl.Heuristique(); ph=charger(); wrong=[]\nfor p in ph:\n    a=h.analyser(p['texte'],p[' … [593 caractères tronqués]`

  ```
1
[('s065', 'REL', 'qui commence', 'elle', 'nage')]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && PYTHONPATH=/tmp/g017 python3 - <<'EOF'\nimport sys\nsys.path.insert(0,'/tmp/g017'); sys.path.insert(0,'tools')\nimport bloc_linguistique as base, bloc_adv_large as broad\nfrom tests.linguistique.evaluer_gold import charger\nph=charge … [519 caractères tronqués]`

  ```
8
g005 "Elle a dit qu'elle viendrait hier." lost [] gained []
g017 'She said that she would come yesterday.' lost [] gained [('SUB', 9, 28)]
r210 "Bien qu'il soit tard, il travaille." lost [] gained []
r218 'Although it is late, he works.' lost [('SUB', 0, 19)] gained []
r264 "Je sais qu'il vient demain." lost [('SUB', 8, 26)] gained []
r288 'I know that he comes tomorrow.' lost [('SUB', 7, 29)] gained []
r303 'Je pars car il est tard.' lost [('SUB', 8, 23)] gained []
r313 'I leave because it is late.' lost [('SUB', 8, 26)] gained []
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('reports/rapport-g017.md'); s=p.read_text()\nold=\"| **ADV large** : retirer tout `ADV` final, pas seulement les adverbes de temps | **0,7885** | 1476 / 405 / 387 | 233/234 | 0,9791 | … [715 caractères tronqués]`

  ```
fiche adv_large corrected
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('reports/rapport-g017.md'); s=p.read_text()\nold=\"Quatre autres SUB finissent par un `ADV`, mais ce sont des **attributs** (« il soit **tard** »,\\n« it is **late** »), pas des circo … [686 caractères tronqués]`

  ```
convention sentence corrected
138:relèvent pas de la même règle ; la version large en casse trois (`r218`, `r303`, `r313`) et
163:  de la version large ne condamne pas la version étroite.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-g017.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-g017.md</path>
<type>file</type>
<content>
1: # B13 — g017 : l'adverbe final hors de la SUB est rejeté (g017 gagné, r264 et r288 perdus)
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée) · **Tâche** : J6.1 · **Date** : 2026-11-14 ·
4: > **Verdict** : ❌ **règle rejetée**.
5: > La règle demandée — **l'adverbe final de temps hors de la SUB** — corrige bien `g017`
6: > (`that she would come` au lieu de `that she would come yesterday`) et retire un faux positif
7: > de `g005`, mais elle **casse `r264`** (`qu'il vient demain`) et **`r288`**
8: > (`that he comes tomorrow`) : **F1 0,7902 → 0,7901 (−0,0001)**, **dev +0,0011**, **test
9: > −0,0028**, **attachement 237/238 → 236/237**, **couverture 0,9958 → 0,9916**. Les deux cas
10: > favorables sont en **dev**, les deux cas défavorables en **test** : le gain est in-sample, la
11: > perte est hors échantillon. **Aucun code de production n'est modifié** ; la porte du bloc
12: > reste verte, et l'état reste à **237/238**.
13: >
14: > **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (lecture seule),
15: > [`evaluer_gold.py`](../tools/tests/lin
… [12214 caractères tronqués]
  ```

- **bash** `{"command": "date '+%H h %M'", "description": "Current time"}`

  ```
00 h 55
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport pathlib\np=pathlib.Path('docs/pilotage/en-cours.md'); s=p.read_text()\nold='**Mis à jour : 2026-11-14, 00 h 50 HNE (heure locale, EST).**'\nnew='**Mis à jour : 2026-11-14, 00 h 55 HNE (heure locale, EST).**' … [312 caractères tronqués]`
