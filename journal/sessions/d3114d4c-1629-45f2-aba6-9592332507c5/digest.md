# Session DSH — relecture

- identifiant : `d3114d4c-1629-45f2-aba6-9592332507c5`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-05 21:12:21
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : vérifier la **cohérence des huit fiches de la journée** (v2 → v8) avec leurs JSON et avec l'état committé `f908d7b0`.

Fiches (chacune avec son JSON) :
- `rapport-pensee-attachement-v2.md`, `-v3.md`, `-segmentation-v4.md`, `-couverture-v5.md`, `-attachement-parfait.md` (v6), `-couverture-v7.md`, `-r1r3.md` (v8), `rapport-gold-split.md`.

À faire :
1. Pour chaque fiche : les chiffres du texte == ceux du JSON == ceux du code au commit (si la fiche est **courante**), ou cohérence avec son **instantané** (si historique) ; vérifie la mention d'historique et la base (612 vivant / 602 gelé) partout où F1/POS/tête sont citées.
2. Signale les valeurs contradictoires entre fiches, les tableaux dont la somme ne tombe pas, les chiffres d'un JSON absents du texte et réciproquement, les fiches sans contrôle négatif.
3. Vérifie que chaque fiche nomme B13, sa date, son verdict, et que `reports/README.md` les référence ; signale les lignes du README périmées.
4. Écris **uniquement** deux fichiers neufs : `reports/rapport-coherence-fiches-v8.md` et `reports/pensee-coherence-fiches-v8.json`.

Règles strictes : ne committe rien ; ne modifie aucun fichier existant ; n'écris pas dans `docs/pilotage/`, `AGENTS.md`, `journal/`, `tools/structures/`, `data/`, `tools/entrainer_native.py`, `tools/native_model.py`. Rends un résumé : nombre de fiches, écarts par fiche, liste priorisée des corrections.
Your parent agent id is "e181ce02-cd50-488a-a6be-e84b79d40dcc". Before you finish, send your result to that agent with send_message({ agent_id: "e181ce02-cd50-488a-a6be-e84b79d40dcc", message: "<self-contained result>" }). The parent shares your workspace but does not automatically receive your transcript, tool output, or reasoning. Send earlier messages as well when a finding changes what the parent should do next; sending a message does not end your turn.

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

You are a delegated subagent: your permission scope was fixed when you were started and cannot be widened from inside this session — operations that require approval are rejected automatically. When the task needs access beyond that scope, do not retry the denied operation; state the limitation in your reply so the delegating agent can handle it.

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

⏵ Inventaire du dépôt et des huit fiches

Je commence par explorer le dépôt et lire les fiches.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short | head -50 && echo \"---BRANCH---\" && git branch --show-current && echo \"---HEAD---\" && git log --oneline -5 && echo \"---F908---\" && git log --oneline -1 f908d7b0 2>/dev/null || echo \"f908d7b0 NOT FOUND\"", " … [54 caractères tronqués]`

  ```
MM journal/2026-11-05/README.md
D  journal/2026-11-05/attention.md
MM journal/2026-11-05/distribue.md
MM journal/2026-11-05/docs.md
MM journal/2026-11-05/memoire.md
MM journal/2026-11-05/mesures.md
MM journal/2026-11-05/modele.md
MM journal/2026-11-05/moteur.md
MM journal/2026-11-05/portes.md
MM journal/README.md
MM journal/THEMES.md
MM journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/digest.md
MM journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/rapport.md
D  journal/sessions/1b0cf09a-a77a-443d-82e2-68a5d6cacdf0/digest.md
D  journal/sessions/1b0cf09a-a77a-443d-82e2-68a5d6cacdf0/rapport.md
MM journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/digest.md
MM journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/rapport.md
D  journal/sessions/24001907-4f19-4ea5-87f6-98334496719f/digest.md
D  journal/sessions/24001907-4f19-4ea5-87f6-98334496719f/rapport.md
D  journal/sessions/24529ced-6556-4491-9633-9401c2dffb0c/digest.md
D  journal/sessions/24529ced-6556-4491-9633-9401c2dffb0c/rapport.md
D  journal/sessions/2cc1ad4a-373e-4362-a341-3c4a630c2e0c/digest.md
D  journal/sessions/2cc1ad4a-373e-4362-a341-3c4a630c2e0c/rapport.md
D  journal/sessions/3144cf23-6004-46ef-bc3d-f05d81c0cf
… [2489 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls reports/ | head -100 && echo \"---COUNT---\" && ls reports/ | wc -l", "description": "List reports directory"}`

  ```
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
a80-porte-reflexe.json
a80-porte-reparti.json
a80-portes-ppl.json
a80-porte-topologie.json
a80-porte-trace.json
a83a-coupe.json
a83a-flux.json
a83a-pont.json
a83b-decision.json
a83b-lot.json
a83b-regimes.json
a83c-ctx.json
a83c-lot.json
a83-defaut.json
a83d-lot-threads.json
aiguille-30b.md
aiguille-gpt-oss.md
alignement-3b.json
alignement-7b.json
alignement-verne.md
analyse-litteraire.json
archive
b102bis-capacite.json
b102bis-corpus-jw.json
b102bis-decodeur.json
b10-decodeur-mots.json
b10-mots-contraste.json
b10-mots-jw.json
b1110-audit.json
b1110b-hybride.json
b1110-cartes.json
b1110c-case.json
b13-porte-134.json
b13-porte-138.json
b13-porte-140.json
bilan-b11.md
bilan-multi-materiel.md
bloc-linguistique.json
bruit-entree.json
c
… [1062 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Localisation des huit fiches et de leurs JSON associés

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la reports/rapport-pensee-attachement-v2.md reports/rapport-pensee-attachement-v3.md reports/rapport-pensee-segmentation-v4.md reports/rapport-pensee-couverture-v5.md reports/rapport-pensee-attachement-parfait.md reports/rapport- … [134 caractères tronqués]`

  ```
-rw-r--r--. 1 stephane stephane 3304  5 nov 20:15 reports/rapport-gold-split.md
-rw-r--r--. 1 stephane stephane 4072  5 nov 20:32 reports/rapport-pensee-attachement-parfait.md
-rw-r--r--. 1 stephane stephane 5770  5 nov 20:32 reports/rapport-pensee-attachement-v2.md
-rw-r--r--. 1 stephane stephane 5158  5 nov 20:15 reports/rapport-pensee-attachement-v3.md
-rw-r--r--. 1 stephane stephane 4773  5 nov 20:32 reports/rapport-pensee-couverture-v5.md
-rw-r--r--. 1 stephane stephane 4547  5 nov 20:47 reports/rapport-pensee-couverture-v7.md
-rw-r--r--. 1 stephane stephane 3857  5 nov 21:08 reports/rapport-pensee-r1r3.md
-rw-r--r--. 1 stephane stephane 5262  5 nov 20:32 reports/rapport-pensee-segmentation-v4.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la reports/ | grep -i \"pensee\" ", "description": "List pensee-related files in reports"}`

  ```
-rw-r--r--. 1 stephane stephane     702 28 oct 11:21 native-pensee.json
-rw-r--r--. 1 stephane stephane    2079 21 oct 03:50 pas-de-pensee-14b.json
-rw-r--r--. 1 stephane stephane    2075 21 oct 01:53 pas-de-pensee-7b.json
-rw-r--r--. 1 stephane stephane    6848 21 oct 01:58 pas-de-pensee-contracte-3b.json
-rw-r--r--. 1 stephane stephane    6825 21 oct 01:59 pas-de-pensee-contracte-7b.json
-rw-r--r--. 1 stephane stephane    3160 21 oct 23:15 pas-de-pensee-corrige-14b.json
-rw-r--r--. 1 stephane stephane    3154 21 oct 23:15 pas-de-pensee-corrige-3b.json
-rw-r--r--. 1 stephane stephane    3168 21 oct 23:15 pas-de-pensee-corrige-7b.json
-rw-r--r--. 1 stephane stephane    3186 21 oct 23:40 pas-de-pensee-corrige-large.json
-rw-r--r--. 1 stephane stephane    2084 21 oct 01:49 pas-de-pensee.json
-rw-r--r--. 1 stephane stephane      81 21 oct 02:02 pas-de-pensee-mlp-18.json
-rw-r--r--. 1 stephane stephane      83 21 oct 02:03 pas-de-pensee-mlp-6.json
-rw-r--r--. 1 stephane stephane    2707 21 oct 23:15 pas-de-pensee-non-lineaire-3b.json
-rw-r--r--. 1 stephane stephane    2742 21 oct 23:40 pas-de-pensee-non-lineaire-large.json
-rw-r--r--. 1 stephane stephane     892 21 oct 16:10 pas-de-pen
… [36269 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des huit fiches

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-r1r3.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-attachement-v2.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-attachement-v3.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-segmentation-v4.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-r1r3.md</path>
<type>file</type>
<content>
1: # B13 — R1/R2/R3 : exact 212/212 (1,0000), couverture 0,887, F1 0,5763
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **État courant** : commit à jour
4: > (après `4ebeb683`) · **Verdict** : ✅
5: > **183/183 portes** : les quatre règles de la fiche [spans v7](rapport-spans-v7.md) (A17) sont
6: > intégrées — **R1** frontière de clause (pronom, modaux, second prédicat), **R2** SUB sans
7: > précédent, **R3a** subordonnants par langue, **R3c** `fall`/`call`. Résultat : **212 labels**
8: > (sur 239), **exact 212/212 = 1,0000** (fr **129/129**, en **83/83**), **couverture 0,887**,
9: > **F1 0,5763** (union ; S 0,4966, chunker 0,6057), tête **0,7316** ; **27 spans** restants
10: > (16 REL, 6 SUB, 5 GP), dont 17 sont **inatteignables** (lexique synthétique ou bug du gold).
11: >
12: > **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`SUJETS`, `MODAUX`,
13: > `SUB_PAR_LANGUE`, boucle REL/SUB), [`autotest.py`](../tools/pensee/autotest.py) (24 assertions) ;
14: > JSON [`pensee-r1r3.json`](pensee-r1r3.json).
15: 
16: ## 1. L
… [3017 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-attachement-v2.md</path>
<type>file</type>
<content>
1: # B13 — l'attachement v2 : exact 0,8483 → 0,9448, top-k strict 0,6069 → 0,9724
2: 
3: > **Instantané historique** : état au commit `9d5337ce` (2026-11-05) ; ne décrit pas l'état courant `69bd865e` — voir [rapport-pensee-couverture-v7](rapport-pensee-couverture-v7.md).
4: 
5: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
6: > **180/180 portes** : trois corrections **mesurées**, issues de trois sous-agents indépendants :
7: > (1) la règle du **segment précédent** (un SUB après un GV est une complétive → cible = le verbe ;
8: > après un GN, une relative → cible = l'antécédent), (2) les **têtes des candidats** de S
9: > (« « … » → Le livre » → `livre`), (3) le **lexique verbal anglais** complété. Sur les 145
10: > segments au bon span : **exact 123 → 137 (0,9448)**, top1 **126 → 140 (0,9655)**, top-k
11: > **134 → 142 (0,9793)**, **top-k strict 88 → 141 (0,9724)**.
12: >
13: > **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
14: > [`evaluer_gold.py`](../tools/tests/linguisti
… [4922 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-attachement-v3.md</path>
<type>file</type>
<content>
1: # B13 — l'attachement v3 : exact 0,9448 → 0,9724, les noms à 1,0
2: 
3: > **Instantané historique** : état au commit `dcf7bc91` (2026-11-05) ; ne décrit pas l'état courant `69bd865e` — voir [rapport-pensee-couverture-v7](rapport-pensee-couverture-v7.md).
4: 
5: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
6: > **181/181 portes** : trois règles **générales** issues du diagnostic des 8 échecs (A9) sont
7: > intégrées — **R2** (un GP n'est pas gouverné par un mot de son span), **R3** (cible vide :
8: > génitif → tête du GN à gauche), **R4** (enclitique `appelle-moi` → `appelle`). Sur les 145
9: > segments au bon span : **exact 137 → 141 (0,9724)**, top1 **140 → 143 (0,9862)**, top-k 142
10: > (0,9793), **top-k strict 142 (0,9793)** ; les **cibles noms atteignent 29/29 = 1,0**.
11: >
12: > **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_cible_hors_span`,
13: > `_repli_cible_gp`, `_sans_enclitique`), [`autotest.py`](../tools/pensee/autotest.py) ;
14: > fiche A9 [échecs v2
… [4301 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-segmentation-v4.md</path>
<type>file</type>
<content>
1: # B13 — la segmentation d'abord : F1 0,2862 → 0,4539, exact 157/160 (0,9812), couverture 160/239
2: 
3: > **Instantané historique** : état au commit `392f03aa` (2026-11-05) ; ne décrit pas l'état courant `69bd865e` — voir [rapport-pensee-couverture-v7](rapport-pensee-couverture-v7.md).
4: 
5: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
6: > **183/183 portes** : le diagnostic de A12/A14 était juste — le trou n'était pas l'attachement mais le
7: > **découpage**. Sept corrections générales font passer la **F1 syntagmes de 0,2862 à 0,4539**
8: > (union ; S 0,4285, chunker 0,4143), la **tête de 0,4989 à 0,6432**, et la **couverture de 145 à
9: > 160 labels** (sur 239) ; l'attachement suit : **exact 157/160 = 0,9812**, **top-k 156/239**,
10: > par langue **fr 0,9915** (117/118) et **en 0,9524** (40/42) — l'anglais passe de **28 à 42 labels**.
11: >
12: > **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_syntagmes_simple`,
13: > `_verbe_dans`, `_cible_hors_span`), [`autotes
… [4407 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des quatre autres fiches et des JSON

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-couverture-v5.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-attachement-parfait.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-couverture-v7.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-split.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-couverture-v5.md</path>
<type>file</type>
<content>
1: # B13 — la couverture : 187 labels, exact 186/187 (0,9947), F1 0,5156
2: 
3: > **Instantané historique** : état au commit `b975011b` (2026-11-05) ; ne décrit pas l'état courant `69bd865e` — voir [rapport-pensee-couverture-v7](rapport-pensee-couverture-v7.md).
4: 
5: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
6: > **183/183 portes** : la **couverture** passe de **160 à 187 labels** (sur 239) et l'exactitude
7: > tient : **exact 186/187 = 0,9947** (fr **0,9921**, en **1,0000** — 60/60) ; la **F1 syntagmes**
8: > monte à **0,5156** (union ; S 0,4582, chunker 0,5351) et la tête à **0,6826** ; les **spans
9: > perdus** tombent de **79 à 52** (24 REL, 12 SUB, 16 GP). Sur le gold tenu à l'écart : **dev
10: > 126/126 (1,000)**, **test 60/61** — la progression n'est pas un surajustement visible.
11: >
12: > **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_syntagmes_simple`,
13: > `_cible_precedent`), [`autotest.py`](../tools/pensee/autotest.py) (25 assertions recalées) ;
14: 
… [3941 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-attachement-parfait.md</path>
<type>file</type>
<content>
1: # B13 — l'attachement parfait sur les spans prédits : 187/187 (1,0000)
2: 
3: > **Instantané historique** : état au commit `0ec6c27d` (2026-11-05) ; ne décrit pas l'état courant `69bd865e` — voir [rapport-pensee-couverture-v7](rapport-pensee-couverture-v7.md).
4: 
5: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
6: > **183/183 portes** : sur les **187 segments dont le span est prédit** (sur 239 cibles), la cible
7: > est **juste 187 fois** — **français 127/127 (1,0)**, **anglais 60/60 (1,0)**, **verbes 131/131**,
8: > **noms 56/56** ; **dev 126/126**, **test 61/61**. Le **rendement global** reste **187/239 =
9: > 0,7824** : les 52 spans non prédits sont la seule frontière qui reste.
10: >
11: > **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_cible_precedent`,
12: > `_candidats_precedent`, `_repli_verbe_propre`, `_est_adverbe_seul`),
13: > [`autotest.py`](../tools/pensee/autotest.py) ; dev/test [`gold_split.py`](../tools/tests/linguistique/gold_split.py) ;
14: > J
… [3265 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-pensee-couverture-v7.md</path>
<type>file</type>
<content>
1: # B13 — la couverture à 0,8201 : POS contextuel, GV avant GP, prépositions ambiguës
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
4: > **183/183 portes** : la **couverture** passe de **187 à 196 labels** (sur 239) et l'exactitude
5: > tient : **exact 195/196 = 0,9949** (fr **135/135 = 1,0**, en **60/61**) ; la **F1 syntagmes**
6: > monte à **0,5595** (union ; S 0,4741, chunker 0,5858), la tête à **0,7205** ; la **POS** passe de
7: > **0,7482 à 0,7603** (gelé 602) ; les **spans perdus** tombent de **52 à 43** (21 REL, 17 SUB, 5 GP).
8: >
9: > **État courant** : commit `69bd865e` · **Base** : F1/tête/POS sur le gold **gelé 602** (portes
10: > T110-T115) ; sur le **612** : F1 **0,5555**, tête **0,7152**, POS **0,7581**. Couverture et
11: > exactitude sur le **612**.
12: >
13: > **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (POS contextuel,
14: > ordre GV/GP, prépositions composées, sujets), [`autotest.py`](../tools/pensee/autotest.py)
15: > (32 assertions recalées) 
… [3733 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gold-split.md</path>
<type>file</type>
<content>
1: # B13 — le gold coupé en dev/test : les gains généralisent (test 0,9814, dev 0,9811)
2: 
3: > **Instantané historique** : état au commit `85e4082b` (2026-11-05) ; ne décrit pas l'état courant `69bd865e` — voir [rapport-pensee-couverture-v7](rapport-pensee-couverture-v7.md).
4: 
5: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
6: > Le gold 612 est coupé en **dev** (422 phrases, 163 cibles, 106 labels) et **test** (190, 76, 54)
7: > par un **hash stable de l'identifiant** (`crc32(id) % 3 == 0` → test), stratifié par source et
8: > par langue. Mesuré : **dev exact 104/106 (0,9811)**, **test 53/54 (0,9814)** — les règles de la
9: > journée ne sont donc pas un surajustement visible à ce niveau ; la F1 est même meilleure sur le
10: > test (0,4719 contre 0,4414).
11: >
12: > **Dispositif** : [`gold_split.py`](../tools/tests/linguistique/gold_split.py) (`dev`, `test`,
13: > `compter`), [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py) ; JSON
14: > [`pensee-gold-split.json`](pensee-gold-split.json).

… [2450 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des huit JSON et de leurs structures

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports && for f in pensee-attachement-v2.json pensee-attachement-v3.json pensee-segmentation-v4.json pensee-couverture-v5.json pensee-attachement-parfait.json pensee-couverture-v7.json pensee-r1r3.json pensee-gold-split.json; do echo \ … [108 caractères tronqués]`

  ```
=============== pensee-attachement-v2.json ===============
{
 "date": "2026-11-05",
 "ligne": "B13",
 "portes": "180/180",
 "labels": 145,
 "cibles": 239,
 "avant": {
  "exact": 123,
  "exact_span": 0.8483,
  "top1": 126,
  "topk": 134,
  "topk_exact": 88,
  "verbe_est": 0.9524,
  "nom_est": 0.7683
 },
 "apres": {
  "exact": 137,
  "exact_span": 0.9448,
  "top1": 140,
  "topk": 142,
  "topk_exact": 141,
  "top1_span": 0.9655,
  "topk_span": 0.9793,
  "topk_exact_span": 0.9724,
  "verbe_pos": 0.9569,
  "nom_pos": 0.8966,
  "verbe_cibles": 116,
  "nom_cibles": 29
 },
 "rendement": {
  "top1": 0.5858,
  "topk": 0.5941,
  "exact": 0.5732
 },
 "corrections": {
  "segment_precedent": {
   "gain_exact": 6,
   "source": "A7",
   "ids": [
    "s012",
    "s030",
    "s052",
    "s097",
    "s124",
    "s139"
   ]
  },
  "lexique_anglais": {
   "gain_exact": 8,
   "gain_top1": 8,
   "source": "A2",
   "risque": "borne haute"
  },
  "tetes_candidats": {
   "gain_topk_strict": 45,
   "source": "A2"
  }
 },
 "modele_appris": {
  "exact": 0.9793,
  "vs_regle": 137,
  "gain": 5,
  "mcnemar": "7/2",
  "p": 0.18,
  "ic95": [
   -0.7,
   7.6
  ],
  "decision": "rejete"
 },
 "echecs": {
  "hors_candi
… [6918 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification des commits, des portes et du README

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for c in 9d5337ce dcf7bc91 392f03aa b975011b 0ec6c27d 85e4082b 69bd865e f908d7b0; do echo -n \"$c : \"; git log --oneline -1 \"$c\" 2>&1 | head -1; done; echo \"---LOG 69bd865e..HEAD---\"; git log --oneline 69bd865e..HEAD; echo \"--- … [124 caractères tronqués]`

  ```
9d5337ce : 9d5337ce B13 — L'ATTACHEMENT V2 : EXACT SPANS 0,8483 → 0,9448, TOP-K STRICT 0,6069 → 0,9724 ; 3 SOUS-AGENTS INTÉGRÉS, LE MODÈLE APPRIS REJETÉ ; 180/180
dcf7bc91 : dcf7bc91 B13 — L'ATTACHEMENT V3 : EXACT 0,9448 → 0,9724, NOMS 29/29 = 1,0 ; R2/R3/R4 DE A9 ; 181/181
392f03aa : 392f03aa B13 — S NE SEGMENTE QUE LE FRANÇAIS : F1 0,4194 → 0,4539, TÊTE 0,6432 ; EXACT 157/160, FR 0,9915 / EN 0,9524 ; 183/183
b975011b : b975011b B13 — LES CANDIDATS DU PRÉCÉDENT : EXACT 186/187 (0,9947), ANGLAIS 60/60, DEV 126/126 ; 183/183
0ec6c27d : 0ec6c27d B13 — L'ATTACHEMENT PARFAIT SUR LES SPANS PRÉDITS : 187/187 (1,0000), FR 1,0, EN 1,0, DEV 126/126, TEST 61/61 ; RENDEMENT 0,7824 ; 183/183
85e4082b : 85e4082b B13 — LE GOLD DEV/TEST : TEST 0,9814, DEV 0,9811, LES GAINS GÉNÉRALISENT ; RÈGLE « RÉGLER SUR DEV, ACCEPTER SI TEST NE BAISSE PAS »
69bd865e : 69bd865e B13 — LA COUVERTURE À 0,8201 : POS CONTEXTUEL 0,7603, F1 0,5595, EXACT 195/196 (0,9949), 43 SPANS ; 183/183
f908d7b0 : f908d7b0 B13 — R1/R2/R3 : EXACT 212/212 (1,0000), COUVERTURE 0,887, F1 0,5763, FR 1,0 / EN 1,0 ; 27 SPANS DONT 17 INATTEIGNABLES ; 183/183
---LOG 69bd865e..HEAD---
5c15ee91 JOURNAL — LES RÈGLES DE A17 : EXACT 212/212, CO
… [1067 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls reports/ | grep -i coherence; echo \"---\"; ls -la reports/rapport-coherence* 2>&1; echo \"---README head---\"; wc -l reports/README.md", "description": "List coherence reports and README size"}`

  ```
pensee-coherence-fiches.json
pensee-coherence-fiches-v7.json
rapport-coherence-docs-2.md
rapport-coherence-docs-3.md
rapport-coherence-docs.md
rapport-coherence-fiches.md
rapport-coherence-fiches-v7.md
rapport-coherence-vision.md
---
-rw-r--r--. 1 stephane stephane 30570 28 oct 14:07 reports/rapport-coherence-docs-2.md
-rw-r--r--. 1 stephane stephane 12367 28 oct 14:07 reports/rapport-coherence-docs-3.md
-rw-r--r--. 1 stephane stephane 29105 28 oct 09:17 reports/rapport-coherence-docs.md
-rw-------. 1 stephane stephane 38511  5 nov 14:41 reports/rapport-coherence-fiches.md
-rw-------. 1 stephane stephane 28110  5 nov 20:26 reports/rapport-coherence-fiches-v7.md
-rw-r--r--. 1 stephane stephane 14824 28 oct 09:17 reports/rapport-coherence-vision.md
---README head---
180 reports/README.md
  ```

### 🤖 Assistant

⏵ Lecture de l'audit de cohérence précédent (v7)

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-fiches-v7.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-fiches-v7.md</path>
<type>file</type>
<content>
1: # Cohérence des fiches B13 du 2026-11-05 — v2 → v7
2: 
3: > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ❌
4: > **7 fiches auditées** (1 courante, 6 historiques), **23 écarts numériques**, dont **4 critiques** ;
5: > **7 fiches** ont au moins une lacune JSON ↔ texte ; **5 fiches** n'ont pas de contrôle négatif ;
6: > **6 fiches historiques** n'ont pas de mention d'historique ; **2 lignes** de `reports/README.md`
7: > répètent les valeurs périmées. Aucun renvoi de § faux, aucun lien relatif cassé, un seul tableau
8: > dont la somme visible ne tombe pas (les corrections de la v2).
9: >
10: > **État audité** : commit **`69bd865e`** (2026-11-05 19:22), branche `s/v7`. Pendant l'audit, HEAD a
11: > avancé (`e4cd4408`, puis `35a67bc7`) ; les sept fiches, leurs JSON et `reports/README.md` sont
12: > **identiques dans `69bd865e` et `e4cd4408`** ; le commit `35a67bc7` applique ensuite des
13: > corrections (voir § 11). L'audit reste ancré sur `69bd865e`.
14: >
15: > **Méthode** : lecture des 7 fiches et de le
… [28023 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Analyse du diff 69bd865e→f908d7b0 et du README

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff --stat 69bd865e..HEAD -- reports/ tools/ docs/pilotage/ | cat", "description": "Diff stat since v7 commit"}`

  ```
docs/pilotage/en-cours.md                     |    4 +-
 docs/pilotage/roadmap.md                      |    2 +-
 reports/README.md                             |    9 +-
 reports/pensee-audit-v7.json                  | 1199 ++++++++++
 reports/pensee-coherence-fiches-v7.json       |  901 +++++++
 reports/pensee-dev-test-v7.json               | 3128 +++++++++++++++++++++++++
 reports/pensee-r1r3.json                      |   45 +
 reports/rapport-audit-v7.md                   |  556 +++++
 reports/rapport-coherence-fiches-v7.md        |  359 +++
 reports/rapport-dev-test-v7.md                |  226 ++
 reports/rapport-gold-split.md                 |    4 +-
 reports/rapport-pensee-attachement-parfait.md |    7 +-
 reports/rapport-pensee-attachement-v2.md      |    4 +-
 reports/rapport-pensee-attachement-v3.md      |    2 +
 reports/rapport-pensee-couverture-v5.md       |   21 +-
 reports/rapport-pensee-couverture-v7.md       |   26 +-
 reports/rapport-pensee-r1r3.md                |   73 +
 reports/rapport-pensee-segmentation-v4.md     |   15 +-
 tools/bloc_linguistique.py                    |   48 +-
 tools/pensee/autotest.py                      |  110 +-
 20 files changed, 6644 
… [30 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline --all -- reports/rapport-pensee-attachement-v2.md reports/rapport-pensee-attachement-v3.md reports/rapport-pensee-segmentation-v4.md reports/rapport-pensee-couverture-v5.md reports/rapport-pensee-attachement-parfait … [182 caractères tronqués]`

  ```
f908d7b0 B13 — R1/R2/R3 : EXACT 212/212 (1,0000), COUVERTURE 0,887, F1 0,5763, FR 1,0 / EN 1,0 ; 27 SPANS DONT 17 INATTEIGNABLES ; 183/183
4ebeb683 B13 — L'AUDIT V7 INTÉGRÉ : DEUX RÉCITS CORRIGÉS (8 LABELS, +0,0118, EXEMPLE r204), VALEURS VÉRIFIÉES
9bf94feb FICHES — LA LISTE DE L'AUDIT APPLIQUÉE : PROSES V4/V5, SPLIT LEXICAL DE LA V2, F1 V6 SUR BASE CONSTANTE, CONTRÔLES
35a67bc7 FICHES — TITRES V4/V5 ALIGNÉS SUR LEUR INSTANT, BASE 602 DE LA V7, README ET ÉTAT À JOUR
8d6c318d B13 — AUDIT DES 7 FICHES (23 ÉCARTS), DEV/TEST V7 (133/134, 62/62), LA V7 CORRIGÉE AVEC SON CONTRÔLE (195/196 VS 1,67)
69bd865e B13 — LA COUVERTURE À 0,8201 : POS CONTEXTUEL 0,7603, F1 0,5595, EXACT 195/196 (0,9949), 43 SPANS ; 183/183
0ec6c27d B13 — L'ATTACHEMENT PARFAIT SUR LES SPANS PRÉDITS : 187/187 (1,0000), FR 1,0, EN 1,0, DEV 126/126, TEST 61/61 ; RENDEMENT 0,7824 ; 183/183
b975011b B13 — LES CANDIDATS DU PRÉCÉDENT : EXACT 186/187 (0,9947), ANGLAIS 60/60, DEV 126/126 ; 183/183
7a9f0d6a B13 — LA COUVERTURE : 187 LABELS, EXACT 185/187 (0,9893), F1 0,5156, DEV 125/126 ET TEST 60/61 ; 183/183
85e4082b B13 — LE GOLD DEV/TEST : TEST 0,9814, DEV 0,9811, LES GAINS GÉNÉRALISENT ; RÈGLE « RÉGLER SUR DEV, ACCEPTER 
… [2327 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/README.md"}`

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
18: | [`rapport-pensee-r1r3.md`](rapport-pensee-r1r3.md) | **B13** — R1/R2/R3 : exact **212/212 (1,0000)**, couverture **0,887**, F1 **0,5763**
… [22491 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Inspection des outils de mesure et du gold

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,160p' tools/tests/linguistique/evaluer_gold.py", "description": "Read evaluer_gold.py head"}`

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
… [5769 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"def \\|RACINE\\|gold_gele\\|gold.json\\|612\\|602\" tools/tests/linguistique/evaluer_gold.py | head -80", "description": "Find functions and constants in evaluer_gold"}`

  ```
15:RACINE = pathlib.Path(__file__).resolve().parents[3]
16:sys.path.insert(0, str(RACINE / "tools"))
19:GOLD = pathlib.Path(__file__).with_name("gold.json")
24:def charger() -> list[dict]:
35:GELE = pathlib.Path(__file__).with_name("gold_gele.json")
38:def charger_gele() -> list[dict]:
47:def par_source(phrases: list[dict], source: str) -> list[dict]:
51:def _pos_map(a: bl.Annotation) -> dict[tuple[int, int], str]:
55:def _seg(a: bl.Annotation) -> set[tuple[str, int, int]]:
59:def _tete(a: bl.Annotation) -> set[tuple[str, int]]:
64:def _pragma(a: bl.Annotation) -> dict:
72:def _prf(tp: int, fp: int, fn: int) -> dict:
80:def evaluer_bloc(nom: str, bloc, phrases: list[dict]) -> dict:
225:def main() -> int:
247:            m = NeuronalLLM(RACINE / "models/Qwen2.5-0.5B-Q4_0.gguf", timeout=10)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '160,320p' tools/tests/linguistique/evaluer_gold.py", "description": "Read evaluer_bloc tail and main"}`

  ```
att_topk_exact += 1
            # attachement par tête : le segment prédit qui couvre la tête du gold
            att_t_n += 1
            tete = [x for x in a.etiquettes if x.niveau == "syntagme"
                    and x.type == s["type"] and x.debut <= s["debut"] < x.fin]
            if not tete:
                continue
            et = tete[0]
            att_t_labels += 1
            att2 = (et.meta or {}).get("attachement") or {}
            cible2 = (att2.get("cible") or "").strip()
            if cible2 and any(c in cible2 or cible2 in c for c in cibles):
                att_t_top1 += 1
            if any(any(c in nom for c in cibles) for nom in (et.candidats or [])):
                att_t_topk += 1
        pr, g = _pragma(a), phrase["pragma"]
        acte_ok += int(pr["acte"] == g.get("acte", "assertion"))
        neg_ok += int(pr["negation"] == bool(g.get("negation", False)))
        mod_ok += int(pr["modalite"] == bool(g.get("modalite", False)))
        ds_ok += int(pr["double_sens"] == bool(g.get("double_sens", False)))
    n = len(phrases)
    return {
        "bloc": nom, "phrases": n,
        "pos": {"exactitude": round(pos_ok / max(1, pos_n), 4),
                "e
… [7387 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Reproduction des mesures au commit f908d7b0

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, json, pathlib\nR = pathlib.Path('.').resolve()\nsys.path.insert(0, str(R/'tools')); sys.path.insert(0, str(R/'tools/tests/linguistique'))\nimport bloc_linguistique as bl\nimport evaluer_gold as eg\nph61 … [1047 caractères tronqués]`

  ```
612 phrases 612 cibles 1863 labels gold 239
602 phrases 602 cibles 1831 labels gold 239
612 F1 0.572 tete 0.7262 POS 0.7581 labels 212 exact 212 1.0 couverture 0.887 topk 177 0.7406 topkstrict 177 0.8349 fr {'cibles': 151, 'labels': 129, 'exact': 129, 'topk': 120, 'exact_taux_span': 1.0} en {'cibles': 88, 'labels': 83, 'exact': 83, 'topk': 57, 'exact_taux_span': 1.0} verbe {'cibles': 148, 'justes': 148, 'taux': 1.0} nom {'cibles': 64, 'justes': 64, 'taux': 1.0}
602 F1 0.5763 tete 0.7316 POS 0.7603 labels 212 exact 212 1.0 couverture 0.887 topk 177 0.7406 topkstrict 177 0.8349 fr {'cibles': 151, 'labels': 129, 'exact': 129, 'topk': 120, 'exact_taux_span': 1.0} en {'cibles': 88, 'labels': 83, 'exact': 83, 'topk': 57, 'exact_taux_span': 1.0} verbe {'cibles': 148, 'justes': 148, 'taux': 1.0} nom {'cibles': 64, 'justes': 64, 'taux': 1.0}
  ```

### 🤖 Assistant

⏵ Diff des fiches depuis l'audit v7

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for f in reports/rapport-pensee-attachement-v2.md reports/rapport-pensee-attachement-v3.md reports/rapport-pensee-segmentation-v4.md reports/rapport-pensee-couverture-v5.md reports/rapport-pensee-attachement-parfait.md reports/rappor … [203 caractères tronqués]`

  ```
################ reports/rapport-pensee-attachement-v2.md
diff --git a/reports/rapport-pensee-attachement-v2.md b/reports/rapport-pensee-attachement-v2.md
index 662f3a35..5a5f21be 100644
--- a/reports/rapport-pensee-attachement-v2.md
+++ b/reports/rapport-pensee-attachement-v2.md
@@ -1,5 +1,7 @@
 # B13 — l'attachement v2 : exact 0,8483 → 0,9448, top-k strict 0,6069 → 0,9724
 
+> **Instantané historique** : état au commit `9d5337ce` (2026-11-05) ; ne décrit pas l'état courant `69bd865e` — voir [rapport-pensee-couverture-v7](rapport-pensee-couverture-v7.md).
+
 > **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
 > **180/180 portes** : trois corrections **mesurées**, issues de trois sous-agents indépendants :
 > (1) la règle du **segment précédent** (un SUB après un GV est une complétive → cible = le verbe ;
@@ -24,7 +26,7 @@
 | top-k (sous-chaîne) | 134 (0,9241) | **142 (0,9793)** | +8 |
 | **exact** | **123 (0,8483)** | **137 (0,9448)** | **+14** |
 | **top-k strict** | **88 (0,6069)** | **141 (0,9724)** | **+53** |
-| cibles verbes (POS gold) | 63 (0,9524) | **111/116 (0,9569)** | +48 cibles |
+| cibles verbes (POS gold) | 63 (0,9
… [16660 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Mesure des POS historiques v6/v7 et du contrôle de permutation

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,80p' tools/bloc_linguistique.py && echo '---IMPORTS---' && grep -n '^import \\|^from ' tools/bloc_linguistique.py", "description": "Inspect bloc_linguistique imports"}`

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
… [2101 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show 0ec6c27d:tools/bloc_linguistique.py | grep -n '^import \\|^from ' && echo '---diff v6->v7 code---' && git diff 0ec6c27d..69bd865e -- tools/bloc_linguistique.py | head -120", "description": "Check historical module imports an … [8 caractères tronqués]`

  ```
30:from __future__ import annotations
32:import os
34:import argparse
35:import collections
36:import copy
37:import json
38:import pathlib
39:import re
40:import subprocess
41:import sys
42:import threading
43:import time
44:import unicodedata
45:import urllib.request
46:from dataclasses import dataclass, field
47:from typing import Protocol, Sequence
---diff v6->v7 code---
diff --git a/tools/bloc_linguistique.py b/tools/bloc_linguistique.py
index 4db853e2..364b3545 100644
--- a/tools/bloc_linguistique.py
+++ b/tools/bloc_linguistique.py
@@ -298,7 +298,7 @@ LEXIQUES = {
 POS_FERME = {
     "fr": {
         "DET": set("le la les l un une ce cet cette ces mon ma mes ton ta tes son sa ses notre nos votre vos leur leurs quel quelle quels quelles".split()),
-        "PREP": set("à a au aux de du des d en dans par pour sur sous avec sans chez vers entre depuis pendant durant contre malgré selon près loin devant derrière après avant".split()),
+        "PREP": set("à a au aux de du des d en dans par pour sur sous avec sans chez vers entre depuis pendant durant contre malgré selon près loin devant derrière après avant au-dessus au-dessous vis-à-vis en-dehors".split()),
         "PRON": se
… [6691 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"RACINE\" tools/bloc_linguistique.py | head -20; echo '---'; grep -n \"class Heuristique\" -A 30 tools/bloc_linguistique.py | head -40", "description": "Check RACINE use and Heuristique init"}`

  ```
49:RACINE = pathlib.Path(__file__).resolve().parent.parent
642:            if str(RACINE / "tools/structures") not in sys.path:
643:                sys.path.insert(0, str(RACINE / "tools/structures"))
2143:    ap.add_argument("--modele", default=str(RACINE / "models/Qwen2.5-0.5B-Q4_0.gguf"))
2148:    ap.add_argument("--udhr", default=str(RACINE / "data/udhr/articles.jsonl"))
---
522:class Heuristique:
523-    """L'implémentation CPU : elle étiquette la surface et **déclare** ce qu'elle ne couvre pas."""
524-
525-    nom = "heuristique"
526-
527-    def __init__(self, profils: dict[str, dict] | None = None, segmenter_s: bool = True,
528-                 seuil_ouvert: float = 0.55, seuil_langue: float = 0.12,
529-                 union: bool = True):
530-        self.profils = profils
531-        self.segmenter_s = segmenter_s
532-        self.seuil_ouvert = seuil_ouvert
533-        self.seuil_langue = seuil_langue
534-        self.union = union
535-
536-    # -- langues / script ---------------------------------------------------
537-    def _langue(self, texte: str, indice: str | None) -> tuple[str, float, str]:
538-        langue, conf, _ = detecter_langue(texte, self.profils, ind
… [676 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport subprocess, types, pathlib, sys, json\nR = pathlib.Path('.').resolve()\nsys.path.insert(0, str(R/'tools')); sys.path.insert(0, str(R/'tools/tests/linguistique'))\nimport evaluer_gold as eg\n\ndef load_hist(c … [1037 caractères tronqués]`

  ```
[stderr]
Traceback (most recent call last):
  File "<stdin>", line 26, in <module>
  File "<stdin>", line 10, in load_hist
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", line 58, in <module>
    @dataclass(frozen=True)
     ~~~~~~~~~^^^^^^^^^^^^^
  File "/usr/lib64/python3.13/dataclasses.py", line 1344, in wrap
    return _process_class(cls, init, repr, eq, order, unsafe_hash,
                          frozen, match_args, kw_only, slots,
                          weakref_slot)
  File "/usr/lib64/python3.13/dataclasses.py", line 997, in _process_class
    and _is_type(type, cls, dataclasses, dataclasses.KW_ONLY,
        ~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                 _is_kw_only))):
                 ^^^^^^^^^^^^
  File "/usr/lib64/python3.13/dataclasses.py", line 757, in _is_type
    ns = sys.modules.get(cls.__module__).__dict__
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute '__dict__'. Did you mean: '__dir__'?
[exit code: 1]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport subprocess, types, pathlib, sys\nR = pathlib.Path('.').resolve()\nsys.path.insert(0, str(R/'tools')); sys.path.insert(0, str(R/'tools/tests/linguistique'))\nimport evaluer_gold as eg\n\ndef load_hist(commit) … [1187 caractères tronqués]`

  ```
0ec6c27d 602 2350/3141 = 0.748169
0ec6c27d 612 2372/3179 = 0.746147
69bd865e 602 2388/3141 = 0.760267
69bd865e 612 2410/3179 = 0.758100
HEAD 602 2388/3141 = 0.760267
HEAD 612 2410/3179 = 0.758100
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"0,0118\\|0.0118\\|0,7485\\|0.7485\\|0,7482\\|0.7482\\|0,7475\\|0.7475\" reports/rapport-audit-v7.md reports/pensee-audit-v7.json reports/rapport-coherence-fiches-v7.md reports/pensee-coherence-fiches-v7.json tools/pensee/a … [90 caractères tronqués]`

  ```
reports/rapport-audit-v7.md:44:1. le POS contextuel ne rend pas **neuf** labels mais **huit** (196 − 188), et **+0,0118** de POS
reports/rapport-audit-v7.md:149:| POS | 0,7475 | 0,7461 | 0,7482 | **v4 gelé** (0,7475) |
reports/rapport-audit-v7.md:157:Le POS 0,7475 est l'ancienne valeur de T107, mesurée sur le **v4**. La tête 0,6826 est l'ancienne
reports/rapport-audit-v7.md:163:| POS | 0,7461 | 0,7482 |
reports/rapport-audit-v7.md:182:Le « +0,0132 » du texte n'est même pas la différence des valeurs affichées (0,7603 − 0,7475 =
reports/rapport-audit-v7.md:183:0,0128). Le vrai gain POS est **+0,0118** (gelé) ou **+0,0116** (vivant). Le gain F1 est
reports/rapport-audit-v7.md:365:| sans POS contextuel | **0,7485** | **188** | **188** | **1,0** | **0,7866** | **159** | **0,5534** | **0,7185** | 135/135 | **53/53** | **126/126** | 62/62 |
reports/rapport-audit-v7.md:375:- **+0,0118 de POS** sur le gelé (0,7603 − 0,7485), **+0,0116** sur le vivant, pas +0,0132 ;
reports/rapport-audit-v7.md:385:contextuel, contre 187 en v6). De même, le « +0,0132 » est calculé sur le 0,7475 de la v4, pas
reports/rapport-audit-v7.md:386:sur la v6 (0,7482 gelé / 0,7461 vivant).
reports/rapport-audit-v7.md:4
… [3746 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"0118\\|7485\\|7482\\|7475\" reports/*.md reports/*.json tools/*.py tools/pensee/*.py 2>/dev/null | head -60", "description": "Search repo for POS values"}`

  ```
reports/rapport-audit-v7.md:44:1. le POS contextuel ne rend pas **neuf** labels mais **huit** (196 − 188), et **+0,0118** de POS
reports/rapport-audit-v7.md:149:| POS | 0,7475 | 0,7461 | 0,7482 | **v4 gelé** (0,7475) |
reports/rapport-audit-v7.md:157:Le POS 0,7475 est l'ancienne valeur de T107, mesurée sur le **v4**. La tête 0,6826 est l'ancienne
reports/rapport-audit-v7.md:163:| POS | 0,7461 | 0,7482 |
reports/rapport-audit-v7.md:182:Le « +0,0132 » du texte n'est même pas la différence des valeurs affichées (0,7603 − 0,7475 =
reports/rapport-audit-v7.md:183:0,0128). Le vrai gain POS est **+0,0118** (gelé) ou **+0,0116** (vivant). Le gain F1 est
reports/rapport-audit-v7.md:365:| sans POS contextuel | **0,7485** | **188** | **188** | **1,0** | **0,7866** | **159** | **0,5534** | **0,7185** | 135/135 | **53/53** | **126/126** | 62/62 |
reports/rapport-audit-v7.md:375:- **+0,0118 de POS** sur le gelé (0,7603 − 0,7485), **+0,0116** sur le vivant, pas +0,0132 ;
reports/rapport-audit-v7.md:385:contextuel, contre 187 en v6). De même, le « +0,0132 » est calculé sur le 0,7475 de la v4, pas
reports/rapport-audit-v7.md:386:sur la v6 (0,7482 gelé / 0,7461 vivant).
reports/rapport-audit-v7.md:4
… [5648 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"^class \" tools/bloc_linguistique.py", "description": "List classes in bloc_linguistique"}`

  ```
59:class Span:
68:class Etiquette:
92:class Annotation:
130:class BlocLinguistique(Protocol):
137:class RefusNeuronal(RuntimeError):
522:class Heuristique:
1244:class MockNeuronal:
1298:class NeuronalLLM:
1377:class NeuronalLLMPOS:
1508:class NeuronalLLMChunks:
1643:class NeuronalLLMCompose:
1693:class NeuronalLLMPragmatique:
1905:class Parallele:
1930:class Cascade:
1968:class CoucheSemantique:
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport sys, pathlib, json\nR = pathlib.Path('.').resolve(); sys.path.insert(0,str(R/'tools')); sys.path.insert(0,str(R/'tools/tests/linguistique'))\nimport bloc_linguistique as bl, evaluer_gold as eg\nph = eg.charg … [456 caractères tronqués]`

  ```
SegmenteurS ABSENT
Chunker ABSENT
Heuristique F1 0.5763 tete 0.7316 labels 212
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"f1_s\\|f1_chunker\\|segmenteur_s\\|S seul\\|chunker seul\" tools/pensee tools/*.py reports/rapport-audit-v7.md | head -40", "description": "Find how S/chunker F1 are measured"}`

  ```
(no output)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"segmenter_s\\|_syntagmes_simple\\|def _syntagmes\" tools/bloc_linguistique.py | head -30", "description": "Find segmentation methods"}`

  ```
527:    def __init__(self, profils: dict[str, dict] | None = None, segmenter_s: bool = True,
531:        self.segmenter_s = segmenter_s
638:    def _syntagmes_s(self, texte: str) -> list[dict] | None:
639:        if not self.segmenter_s:
656:        if not self.segmenter_s:
845:    def _syntagmes_simple(self, texte: str, langue: str,
1077:        simples = self._syntagmes_simple(texte, lg, pos_verbes)
1265:        h = Heuristique(segmenter_s=False)
1284:        for s in h._syntagmes_simple(texte, lg):
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '620,700p' tools/bloc_linguistique.py && echo '---1070---' && sed -n '1060,1120p' tools/bloc_linguistique.py", "description": "Read S and union segmentation code"}`

  ```
return ("NOUN" if (n and n[0].islower()) else "MOT"), True, 0.3

    # -- morphèmes ----------------------------------------------------------
    @staticmethod
    def _morphemes(mot: str) -> list[tuple[str, int, int, str]]:
        n = _normaliser(mot)
        sortie = []
        for suf in SUFFIXES:
            if len(n) > len(suf) + 2 and n.endswith(suf):
                sortie.append(("suffixe", len(mot) - len(suf), len(mot), suf))
                break
        for pre in PREFIXES:
            if len(n) > len(pre) + 2 and n.startswith(pre):
                sortie.append(("préfixe", 0, len(pre), pre))
                break
        return sortie

    # -- syntagmes ----------------------------------------------------------
    def _syntagmes_s(self, texte: str) -> list[dict] | None:
        if not self.segmenter_s:
            return None
        try:
            if str(RACINE / "tools/structures") not in sys.path:
                sys.path.insert(0, str(RACINE / "tools/structures"))
            import generateur  # le générateur S, importé en lecture seule
            return generateur.analyser(texte)
        except Exception:
            return None

    def _cibles_s(self, tex
… [6857 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"0,4966\\|0.4966\\|0,6057\\|0.6057\" reports/*.md reports/*.json tools/ | head -20", "description": "Search for S/chunker values v8"}`

  ```
reports/rapport-matvec-f32-parallele.md:96:(V4-Flash 8430,4966 et tous les chiffres du chemin f32 seraient à re-mesurer).
reports/rapport-pensee-r1r3.md:9:> **F1 0,5763** (union ; S 0,4966, chunker 0,6057), tête **0,7316** ; **27 spans** restants
reports/rapport-pensee-r1r3.md:33:| S / chunker (F1) | 0,4741 / 0,5858 | **0,4966 / 0,6057** |
reports/rapport-vitesse-v41.md:29:| V4-Flash ctx 32 (4 jetons notés) | — | 12,8 s de calcul, PPL **8430,4966** |
reports/rapport-vitesse-v41.md:40:| porte `tools/portes.sh rapide` | toutes vertes, **V4-Flash 8430,4966** |
reports/rapport-vitesse-v41.md:90:# les portes : toutes vertes, V4-Flash 8430,4966
reports/m7-frequence.json:5738:     0.0014966337990867488,
reports/m7-frequence.json:8104:     -0.002149409496652578
reports/m7-frequence.json:8995:    "ecart_type": 0.07430560573489481,
reports/pensee-r1r3.json:18:  "f1_s": 0.4966,
reports/pensee-r1r3.json:19:  "f1_chunker": 0.6057,
tools/portes.sh:130:        # 8430,2968 -> 8430,4966 le 02/10 : la rotation des couches COMPRESSÉES est
tools/portes.sh:143:        compare "V4-Flash 43 couches ctx 32" "8430.4966" "$p"
tools/pensee/autotest.py:1671:    """Le segmenteur : S F1 0,4966 (français seul), 
… [397 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"f1_s\\|f1_chunker\" reports/rapport-audit-v7.md reports/pensee-audit-v7.json | head -20", "description": "Find audit v7 measurement of S/chunker"}`

  ```
reports/pensee-audit-v7.json:103:  "f1_s": {
reports/pensee-audit-v7.json:110:  "f1_chunker": {
  ```

