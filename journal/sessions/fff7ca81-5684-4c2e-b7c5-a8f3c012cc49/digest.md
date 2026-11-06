# Session DSH — relecture

- identifiant : `fff7ca81-5684-4c2e-b7c5-a8f3c012cc49`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-05 21:12:21
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7, Python). Mission : **améliorer le top-k** de l'attachement (état `f908d7b0`) et le mesurer, sans modifier le code du dépôt.

Contexte : `tools/bloc_linguistique.py` (`Heuristique`, `_candidats_precedent`, `_verbes_proches`), `tools/tests/linguistique/evaluer_gold.py` (`evaluer_bloc`). État : 212 labels, exact 212/212, **top-k 177/239 (0,7406)** ; le top-k mesure si la cible gold est **dans** `candidats` (sous-chaîne).

À faire :
1. Qualifie les **62 cibles** (239 − 177) dont la cible n'est pas dans les candidats : par type (REL/SUB/GP/GN/GV), par langue, par source ; distingue les 27 spans non prédits des 35 échecs de couverture de candidats.
2. Propose 2 à 3 règles de **complétion des candidats** (par ex. l'antécédent du GN à gauche pour toute REL, le verbe de la principale pour toute SUB, la tête du GN pour un GP, les verbes du voisinage à distance ≤ 3) ; mesure sur **dev** (gains/pertes du top-k), puis sur **test**.
3. Contrôle négatif : candidats permutés, candidat aléatoire.
4. Écris **uniquement** deux fichiers neufs : `reports/rapport-topk-v8.md` et `reports/pensee-topk-v8.json`.

Règles strictes : ne committe rien ; ne modifie aucun fichier existant ; simulation par sous-classe ou copie locale. N'écris pas dans `docs/pilotage/`, `AGENTS.md`, `journal/`, `tools/structures/`, `data/`, `tools/entrainer_native.py`, `tools/native_model.py`. Rends un résumé : les 5 motifs principaux, le top-k dev/test de chaque règle, ta recommandation.
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

⏵ Exploration du dépôt et des fichiers clés de l'attachement

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git branch --show-current && git status --short | head -20 && ls", "description": "Show branch, status, and top-level files"}`

  ```
s/v7
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
r
… [80 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls tools/tests/linguistique/ && ls reports/ | head -40", "description": "List linguistique tests and reports"}`

  ```
anaphore.py
classement_cible.py
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
replis_cible.py
test_bloc_linguistique.py
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
align
… [51 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && wc -l tools/bloc_linguistique.py tools/tests/linguistique/evaluer_gold.py tools/tests/linguistique/gold_gele.json tools/tests/linguistique/gold_split.py && ls reports/ | grep -i topk", "description": "Check sizes of key files and exi … [20 caractères tronqués]`

  ```
2172 tools/bloc_linguistique.py
   305 tools/tests/linguistique/evaluer_gold.py
 41311 tools/tests/linguistique/gold_gele.json
    50 tools/tests/linguistique/gold_split.py
 43838 total
pensee-topk-diagnostic.json
pensee-topk-strict.json
rapport-aiguille-topk.md
rapport-gpu-topk-selection.md
rapport-gpu-topk-tout.md
rapport-pensee-topk-strict.md
rapport-topk-diagnostic.md
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -5 && grep -rn \"f908d7b0\" --include=*.md --include=*.json -l | head -20", "description": "Recent commits and references to state f908d7b0"}`

  ```
f908d7b0 B13 — R1/R2/R3 : EXACT 212/212 (1,0000), COUVERTURE 0,887, F1 0,5763, FR 1,0 / EN 1,0 ; 27 SPANS DONT 17 INATTEIGNABLES ; 183/183
638ac8e8 PORTES — 13 DOCSTRINGS PÉRIMÉES MISES À JOUR (ATTACHEMENT 195/196, SPANS 43, TOP-K 166) ; 183/183
4ebeb683 B13 — L'AUDIT V7 INTÉGRÉ : DEUX RÉCITS CORRIGÉS (8 LABELS, +0,0118, EXEMPLE r204), VALEURS VÉRIFIÉES
9bf94feb FICHES — LA LISTE DE L'AUDIT APPLIQUÉE : PROSES V4/V5, SPLIT LEXICAL DE LA V2, F1 V6 SUR BASE CONSTANTE, CONTRÔLES
35a67bc7 FICHES — TITRES V4/V5 ALIGNÉS SUR LEUR INSTANT, BASE 602 DE LA V7, README ET ÉTAT À JOUR
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && head -100 reports/rapport-topk-diagnostic.md", "description": "Read existing topk diagnostic report"}`

  ```
# B13 — le top-k strict de l'attachement : 57 échecs, dont 45 d'emballage

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 ·
> **Verdict** : ✅ **les 57 échecs du top-k strict sont qualifiés** (0 « autre »). Sur les
> **145 segments gold dont le span est prédit**, la cible est dans les candidats **134 fois en
> sous-chaîne** (0,9241) mais **88 fois en égalité exacte** (0,6069) : **57 échecs**. **45** sont
> des **candidats du générateur S non réduits à leur tête** — la cible est déjà dans la chaîne
> « « segment » → … », il suffit d'en extraire la tête ; **8** sont des **verbes anglais hors
> lexique** ; **4** sont de la **couverture locale** (génitif, enclitique, GV mal délimité).
> Le **top-1 est déjà juste 41 fois sur 57** : le top-k strict mesure surtout l'**emballage** des
> candidats, pas le choix de la cible. Trois correctifs **simulés, non appliqués**, couvrent
> **45 + 8 + 4 = 57** — borne haute, mesurée sur le même gold.
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`Heuristique`,
> `_tete_nom`, `_verbes_proches`, `VERBES_CONNUS`) · [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py)
> (`char
… [5767 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && head -120 reports/rapport-pensee-topk-strict.md", "description": "Read existing strict topk report"}`

  ```
# B13 — le top-k strict : 0,6069, pas 0,9241

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-05 · **Verdict** : ✅
> **176/176 portes** : le top-k publié jusqu'ici acceptait les **sous-chaînes** (`vu` ⊂ `aperçu`,
> `a` ⊂ `parle`) et affichait **0,9241** ; en **égalité exacte**, la bonne cible n'est dans les
> candidats que **88 fois sur 145** — **0,6069**. L'écart de 32 points est un artefact de mesure,
> pas un résultat.
>
> **Dispositif** : [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
> [`autotest.py`](../tools/pensee/autotest.py), JSON [`pensee-topk-strict.json`](pensee-topk-strict.json).

## 1. Les deux top-k (145 segments au bon span)

| mesure | sous-chaîne | **égalité exacte** |
|---|---:|---:|
| top-k (count) | 134 | **88** |
| taux sur les spans | 0,9241 | **0,6069** |
| rendement (÷ 239) | 0,5607 | **0,3682** |

**Ce que ça dit** :

- **Le top-k lenient gonflait le rappel** : 46 « succès » étaient des sous-chaînes (un candidat
  `a` compte pour la cible `parle`, `vu` pour `aperçu`).
- **Le vrai rappel est 0,6069** : la cible exacte est dans la liste 6 fois sur
… [1405 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/evaluer_gold.py"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique/evaluer_gold.py</path>
<type>file</type>
<content>
1: """evaluer_gold.py — mesure le bloc linguistique sur le gold réel (20) + synthétique (160).
2: 
3: Trois niveaux : POS (token, exact), syntagmes (exact + **par tête**), pragmatique. Quatre
4: lectures : heuristique, mock neuronal, parallèle, cascade. Le vrai modèle est optionnel
5: (`--reel`) : s'il ne répond pas, il est refusé, pas simulé.
6: """
7: from __future__ import annotations
8: 
9: import argparse
10: import json
11: import pathlib
12: import sys
13: from collections import Counter, defaultdict
14: 
15: RACINE = pathlib.Path(__file__).resolve().parents[3]
16: sys.path.insert(0, str(RACINE / "tools"))
17: import bloc_linguistique as bl  # noqa: E402
18: 
19: GOLD = pathlib.Path(__file__).with_name("gold.json")
20: REEL = pathlib.Path(__file__).with_name("gold_reel.json")
21: SYNTH = pathlib.Path(__file__).with_name("gold_synthetique.json")
22: 
23: 
24: def charger() -> list[dict]:
25:     hand = json.loads(GOLD.read_text(encoding="utf-8"))["phrases"]
26:     reel = json.loads(REEL.read_text(encoding="utf-8"))["phrases"]
27:     synth = json.
… [15928 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"_candidats_precedent\\|_verbes_proches\\|candidats\" tools/bloc_linguistique.py | head -80", "description": "Locate candidate functions in bloc_linguistique.py"}`

  ```
7:    **candidats** pour l'ambigu ; elle déclare sa couverture et sa confiance ;
19:`niveau`, son `span`, sa `source`, sa `confiance`, sa `langue`, son `script` et ses `candidats`.
76:    candidats: list[str] = field(default_factory=list)
86:            "candidats": list(self.candidats), "langue": self.langue,
680:    def _candidats_precedent(texte: str, segment: dict, precedent: dict | None) -> list[str]:
681:        """Les candidats que le **précédent** impose : l'antécédent d'une REL, le verbe d'une SUB."""
826:    def _verbes_proches(texte: str, segment: dict, gvs: list[dict],
829:        """Les verbes des `k` GV les plus proches — les **candidats** d'attachement."""
923:                                     "texte": texte[d:mots[j - 1][1]], "candidats": []})
944:                                 "texte": texte[d:mots[j - 1][1]], "candidats": []})
960:                                 "texte": texte[d:mots[j - 1][1]], "candidats": []})
976:                                 "texte": texte[d:mots[j - 1][1]], "candidats": []})
1020:                                            candidats=[] if not ouvert else [classe.lower()],
1027:                                                self.nom
… [1977 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"class Heuristique\\|def analyser\\|def _tete_nom\\|def _cible_proche\\|VERBES_CONNUS\\|def _est_verbe\" tools/bloc_linguistique.py | head -40", "description": "Locate class and helpers"}`

  ```
133:    def analyser(self, texte: str, langue: str | None = None,
387:VERBES_CONNUS = set("""
478:def _est_verbe(mot: str) -> bool:
483:    if n in VERBES_CONNUS:
488:        if n.endswith(suf) and n[:-len(suf)] in VERBES_CONNUS:
492:        if n.endswith(suf) and (n[:-len(suf)] + "er") in VERBES_CONNUS:
522:class Heuristique:
753:    def _tete_nom(texte: str, debut: int, fin: int) -> str | None:
791:    def _cible_proche(texte: str, segment: dict, gvs: list[dict],
983:    def analyser(self, texte: str, langue: str | None = None,
1256:    def analyser(self, texte: str, langue: str | None = None,
1325:    def analyser(self, texte: str, langue: str | None = None,
1435:    def analyser(self, texte: str, langue: str | None = None,
1569:    def analyser(self, texte: str, langue: str | None = None,
1661:    def analyser(self, texte: str, langue: str | None = None,
1739:    def analyser(self, texte: str, langue: str | None = None,
1922:    def analyser(self, texte: str, langue: str | None = None,
1950:    def analyser(self, texte: str, langue: str | None = None,
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "offset": 620, "limit": 280}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
620:         return ("NOUN" if (n and n[0].islower()) else "MOT"), True, 0.3
621: 
622:     # -- morphèmes ----------------------------------------------------------
623:     @staticmethod
624:     def _morphemes(mot: str) -> list[tuple[str, int, int, str]]:
625:         n = _normaliser(mot)
626:         sortie = []
627:         for suf in SUFFIXES:
628:             if len(n) > len(suf) + 2 and n.endswith(suf):
629:                 sortie.append(("suffixe", len(mot) - len(suf), len(mot), suf))
630:                 break
631:         for pre in PREFIXES:
632:             if len(n) > len(pre) + 2 and n.startswith(pre):
633:                 sortie.append(("préfixe", 0, len(pre), pre))
634:                 break
635:         return sortie
636: 
637:     # -- syntagmes ----------------------------------------------------------
638:     def _syntagmes_s(self, texte: str) -> list[dict] | None:
639:         if not self.segmenter_s:
640:             return None
641:         try:
642:             if str(RACINE / "tools/structures") not in sys.path:
643:                 sys.path
… [14105 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", "limit": 240, "offset": 983}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py</path>
<type>file</type>
<content>
983:     def analyser(self, texte: str, langue: str | None = None,
984:                  contexte: str | None = None) -> Annotation:
985:         t0 = time.perf_counter()
986:         texte = texte or ""
987:         trace: list[dict] = []
988:         if not texte.strip() or not any(ch.isalpha() or ch.isdigit() for ch in texte):
989:             return Annotation(texte=texte, refus="vide", source=self.nom,
990:                               trace=[{"etape": "refus", "raison": "vide"}],
991:                               cout={"octets": len(texte.encode()), "duree_s": round(time.perf_counter() - t0, 6)})
992: 
993:         lg, conf_lg, script = self._langue(texte, langue)
994:         trace.append({"etape": "langue", "langue": lg, "script": script, "confiance": conf_lg,
995:                       "indice": langue or ""})
996:         etiquettes: list[Etiquette] = []
997:         unites: list[Span] = []
998: 
999:         # 1. graphème — des plages de classes, pas un caractère par étiquette
1000:         classes = {"L": "lettres", "N": "chiffres", "P": "ponctuation", "
… [15703 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lancement de l'évaluation de référence pour vérifier l'état (177/239)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && time python3 tools/tests/linguistique/evaluer_gold.py 2>&1 | tail -30", "description": "Run baseline gold evaluation", "timeoutMs": 600000}`

  ```
"taux": 1.0
    },
    "nom": {
     "cibles": 63,
     "justes": 63,
     "taux": 1.0
    },
    "couverture": 0.8243,
    "par_langue": {
     "fr": {
      "cibles": 151,
      "labels": 114,
      "exact": 114,
      "topk": 106,
      "exact_taux_span": 1.0
     },
     "en": {
      "cibles": 88,
      "labels": 83,
      "exact": 83,
      "topk": 57,
      "exact_taux_span": 1.0
     }
    }
   },
   "attachement_tete": {
    "cibles": 197,
    "labels": 197,
    "top1": 19
heuristique all: {"pos": {"exactitude": 0.7581, "exactitude_ferme": 0.9004, "exactitude_ouvert": 0.6234, "tokens": 3179, "confusions": {"ADJ": {"ADJ": 50, "NOUN": 80, "VERB": 4}, "ADV": {"ADV": 117, "NOUN": 20, "PREP": 2, "ADJ": 1, "?": 1}, "AUX": {"PREP": 4, "AUX": 118, "?": 3, "NOUN": 3}, "CONJ": {"CONJ": 44, "PRON": 25, "DET": 12, "?": 13, "PREP": 2, "NOUN": 2}, "DET": {"DET": 586, "?": 2}, "NOUN": {"NOUN": 657, "ADJ": 17, "VERB": 7, "?": 1}, "NUM": {"NUM": 2}, "PONCT": {"?": 25}, "PREP": {"PREP": 114}, "PRON": {"PRON": 411, "NOUN": 8, "?": 30, "DET": 25, "CONJ": 1}, "VERB": {"VERB": 311, "NOUN": 450, "ADJ": 5, "PREP": 2, "?": 16, "AUX": 7, "ADV": 1}}}, "syntagme": {"precision": 0.6157, "rappel": 0.53
… [324 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, json\nsys.path.insert(0,'tools/tests/linguistique')\nimport evaluer_gold as eg\nimport bloc_linguistique as bl\nphrases = eg.charger()\nh = bl.Heuristique()\nr = eg.evaluer_bloc('heuristique', h, phrases … [146 caractères tronqués]`

  ```
{
 "cibles": 239,
 "labels": 212,
 "top1": 212,
 "topk": 177,
 "exact": 212,
 "top1_taux": 0.887,
 "topk_taux": 0.7406,
 "exact_taux": 0.887,
 "exact_any": 212,
 "exact_any_taux_span": 1.0,
 "top1_taux_span": 1.0,
 "topk_taux_span": 0.8349,
 "topk_exact": 177,
 "topk_exact_taux": 0.7406,
 "topk_exact_taux_span": 0.8349,
 "exact_taux_span": 1.0,
 "verbe": {
  "cibles": 148,
  "justes": 148,
  "taux": 1.0
 },
 "nom": {
  "cibles": 64,
  "justes": 64,
  "taux": 1.0
 },
 "couverture": 0.887,
 "par_langue": {
  "fr": {
   "cibles": 151,
   "labels": 129,
   "exact": 129,
   "topk": 120,
   "exact_taux_span": 1.0
  },
  "en": {
   "cibles": 88,
   "labels": 83,
   "exact": 83,
   "topk": 57,
   "exact_taux_span": 1.0
  }
 }
}
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat tools/tests/linguistique/gold_split.py && sed -n 1,80p tools/tests/linguistique/gold.py", "description": "Read gold split and loader"}`

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
… [6452 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport json\nfor f in ['gold','gold_reel','gold_synthetique','gold_gele']:\n    d=json.load(open(f'tools/tests/linguistique/{f}.json'))\n    ph=d['phrases']\n    n=sum(1 for p in ph for s in p.get('segments',[]) if  … [161 caractères tronqués]`

  ```
gold 20 targets 13 keys ['version', 'phrases', 'note']
gold_reel 432 targets 171 keys ['version', 'source', 'note', 'phrases']
gold_synthetique 160 targets 55 keys ['version', 'source', 'graine', 'note', 'phrases']
gold_gele 602 targets 239 keys ['gele', 'phrases']
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport sys, json, collections\nsys.path.insert(0,'tools/tests/linguistique')\nimport evaluer_gold as eg, bloc_linguistique as bl\nfor nom, phrases in [('vivant', eg.charger()), ('gele', eg.charger_gele())]:\n    h=b … [480 caractères tronqués]`

  ```
vivant {'cibles': 239, 'labels': 212, 'exact': 212, 'topk': 177, 'topk_exact': 177, 'couverture': 0.887, 'topk_taux': 0.7406}
  langs {'fr': {'cibles': 151, 'labels': 129, 'exact': 129, 'topk': 120, 'exact_taux_span': 1.0}, 'en': {'cibles': 88, 'labels': 83, 'exact': 83, 'topk': 57, 'exact_taux_span': 1.0}}
  sources {'hand': 20, 'reel': 432, 'synthetique': 160} langues {'fr': 402, 'en': 210}
gele {'cibles': 239, 'labels': 212, 'exact': 212, 'topk': 177, 'topk_exact': 177, 'couverture': 0.887, 'topk_taux': 0.7406}
  langs {'fr': {'cibles': 151, 'labels': 129, 'exact': 129, 'topk': 120, 'exact_taux_span': 1.0}, 'en': {'cibles': 88, 'labels': 83, 'exact': 83, 'topk': 57, 'exact_taux_span': 1.0}}
  sources {'hand': 20, 'reel': 422, 'synthetique': 160} langues {'fr': 394, 'en': 208}
  ```

### 🤖 Assistant

⏵ Construction du diagnostic des 62 échecs (spans + couverture)

- **write** `{"file_path": "/tmp/topk_v8_diag.py", "content": "\"\"\"Diagnostic top-k v8 — lecture seule, hors dépôt. Simule des règles de complétion\npar post-traitement de l'Annotation (aucune modification du code du dépôt).\"\"\"\nfrom __future__ import annotations\nimport sys, json, collections, random\nsys. … [2984 caractères tronqués]`

  ```
<path>/tmp/topk_v8_diag.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /tmp && python3 topk_v8_diag.py 2>&1 | head -120", "description": "Run topk diagnostic, first part", "timeoutMs": 300000}`

  ```
{
 "cibles": 239,
 "labels": 212,
 "spans_non_predits": 27,
 "topk": 177,
 "echecs": 62,
 "echecs_couverture": 35,
 "topk_taux": 0.7406
}

ECHECS 62
type {'GP': 7, 'SUB': 7, 'REL': 48}
langue {'fr': 31, 'en': 31}
source {'hand': 3, 'reel': 36, 'synthetique': 23}

croisement span/coverage: {('couverture', 'GP'): 2, ('span', 'SUB'): 6, ('couverture', 'REL'): 32, ('span', 'REL'): 16, ('span', 'GP'): 5, ('couverture', 'SUB'): 1}

croisement langue x span/coverage: {('fr', 'couverture'): 9, ('en', 'span'): 5, ('en', 'couverture'): 26, ('fr', 'span'): 22}

g002 [fr/hand] GP «de la voisine» -> ['chat'] COUV choisi='chat'
  cands=['GP', 'dort']
  texte=Le chat de la voisine dort.

g006 [fr/hand] GP «du voisin» -> ['chien'] COUV choisi='chien'
  cands=['GP', 'aboie']
  texte=Le chien du voisin aboie la nuit.

g017 [en/hand] SUB «that she would come» -> ['said'] SPAN choisi=''
  cands=[]
  texte=She said that she would come yesterday.

r034 [en/reel] REL «that I read» -> ['book'] COUV choisi='book'
  cands=['REL', 'exciting']
  texte=The book that I read is exciting.

r035 [en/reel] REL «she talks about» -> ['film'] SPAN choisi=''
  cands=[]
  texte=The film she talks about is out.

r074 [en
… [2683 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp && python3 topk_v8_diag.py 2>&1 | sed -n '120,400p'", "description": "See remaining failure details", "timeoutMs": 300000}`

  ```
r273 [fr/reel] REL «qui pousse ici» -> ['fleur'] SPAN choisi=''
  cands=[]
  texte=La fleur qui pousse ici est rare.

r278 [en/reel] REL «that you eat» -> ['bread'] COUV choisi='bread'
  cands=['REL', 'fresh']
  texte=The bread that you eat is fresh.

r280 [en/reel] REL «that I bought» -> ['car'] SPAN choisi=''
  cands=[]
  texte=The car that I bought runs.

r283 [en/reel] REL «who sings» -> ['boy'] COUV choisi='boy'
  cands=['REL', 'is']
  texte=The boy who sings is my friend.

r285 [en/reel] REL «that we took» -> ['table'] COUV choisi='table'
  cands=['REL', 'big']
  texte=The table that we took is big.

r287 [en/reel] REL «that flies» -> ['bird'] COUV choisi='bird'
  cands=['REL', 'blue']
  texte=The bird that flies is blue.

r288 [en/reel] SUB «that he comes tomorrow» -> ['know'] SPAN choisi=''
  cands=[]
  texte=I know that he comes tomorrow.

r289 [en/reel] REL «where we live» -> ['place'] COUV choisi='place'
  cands=['REL', 'quiet']
  texte=The place where we live is quiet.

r291 [en/reel] REL «that is on the table» -> ['book'] COUV choisi='book'
  cands=['REL', 'mine']
  texte=The book that is on the table is mine.

r293 [en/reel] REL «whom I mention» -> ['person'] COUV cho
… [3513 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'PY'\nimport json\nrows=json.load(open('/tmp/topk_v8_rows.json'))\ncov=[r for r in rows if r['label'] and not r['ok_topk']]\nprint(len(cov), 'coverage failures')\nfor r in cov:\n    print(f\"{r['id']:6} {r['langue']} {r['type']:4} cible={r['cible']!r:12} cands={r[ … [88 caractères tronqués]`

  ```
35 coverage failures
g002   fr GP   cible='chat'       cands=['GP', 'dort'] | Le chat de la voisine dort.
g006   fr GP   cible='chien'      cands=['GP', 'aboie'] | Le chien du voisin aboie la nuit.
r034   en REL  cible='book'       cands=['REL', 'exciting'] | The book that I read is exciting.
r074   en REL  cible='book'       cands=['REL', 'long'] | The book that you read is long.
r075   en REL  cible='city'       cands=['REL', 'beautiful'] | The city where we live is beautiful.
r114   en REL  cible='film'       cands=['REL', 'long'] | The film that we saw was long.
r115   en REL  cible='house'      cands=['REL', 'small'] | The house where I was born is small.
r204   en REL  cible='man'        cands=['REL', 'is'] | The man who speaks is my father.
r206   fr REL  cible='chat'       cands=['REL', 'dormait'] | Le chat que j'ai vu dormait.
r214   en REL  cible='book'       cands=['REL', 'good'] | The book that I read is good.
r217   en REL  cible='student'    cands=['REL', 'absent'] | The student whom I mention is absent.
r220   en REL  cible='cat'        cands=['REL', 'black'] | The cat that sleeps is black.
r224   fr REL  cible='homme'      cands=['REL', 'arrive'] | L'homme dont la v
… [2052 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'PY'\nimport json, collections\nrows=json.load(open('/tmp/topk_v8_rows.json'))\nfor dim in ('type','langue','source'):\n    c=collections.defaultdict(lambda:[0,0,0])\n    for r in rows:\n        c[r[dim]][0]+=1; c[r[dim]][1]+=int(bool(r['label'])); c[r[dim]][2]+=i … [401 caractères tronqués]`

  ```
type {'GP': {'cibles': 96, 'labels': 91, 'topk': 89}, 'REL': {'cibles': 74, 'labels': 58, 'topk': 26}, 'SUB': {'cibles': 69, 'labels': 63, 'topk': 62}}
langue {'en': {'cibles': 88, 'labels': 83, 'topk': 57}, 'fr': {'cibles': 151, 'labels': 129, 'topk': 120}}
source {'hand': {'cibles': 13, 'labels': 12, 'topk': 10}, 'reel': {'cibles': 171, 'labels': 164, 'topk': 135}, 'synthetique': {'cibles': 55, 'labels': 36, 'topk': 32}}

GP rows:
g002   fr ok=False lab=True  cible='chat'          cands=['GP', 'dort'] | de la voisine
g003   fr ok=True  lab=True  cible='vu'            cands=["« dans le parc » → l'homme", '« dans le parc » → a vu', 'vu', 'homme'] | dans le parc
g004   fr ok=True  lab=True  cible='couru'         cands=['« pour attraper le bus » → Il a couru', '« pour attraper le bus » = cause', 'bus', 'couru'] | pour attraper le bus
g006   fr ok=False lab=True  cible='chien'         cands=['GP', 'aboie'] | du voisin
g007   fr ok=True  lab=True  cible='jouent'        cands=['« dans le jardin » → Les enfants', '« dans le jardin » → jouent', 'jouent', 'enfants'] | dans le jardin
g010   fr ok=True  lab=True  cible='Viens'         cands=['« ici » → Viens', 'Viens'] | ici
g012   fr ok=Tru
… [10305 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'PY'\nimport sys\nsys.path.insert(0,'/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique')\nsys.path.insert(0,'/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools')\nimport evaluer_gold as eg, bloc_linguistique as bl\nfrom topk_v8_diag impor … [685 caractères tronqués]`

  ```
r034 The book that I read is exciting.
  GN   [0,8] 'The book' cands=['GN', 'exciting']
  REL  [9,20] 'that I read' cands=['REL', 'exciting']
  GV   [21,32] 'is exciting' cands=['GV']
  POS: []

 r206 Le chat que j'ai vu dormait.
  GN   [0,7] 'Le chat' cands=["« que j'ai vu dormait » → Le chat", 'dormait', 'chat']
  REL  [8,19] "que j'ai vu" cands=['REL', 'dormait']
  REL  [8,27] "que j'ai vu dormait" cands=["« que j'ai vu dormait » → Le chat", 'dormait', 'chat']
  GV   [20,27] 'dormait' cands=['GV']
  POS: [("'", 'DET')]

 s050 mon jardin qui ouvre rêve
  GN   [0,10] 'mon jardin' cands=['« qui ouvre rêve » → mon jardin', 'rêve', 'jardin']
  REL  [11,20] 'qui ouvre' cands=['REL', 'rêve']
  REL  [11,25] 'qui ouvre rêve' cands=['« qui ouvre rêve » → mon jardin', 'rêve', 'jardin']
  GV   [21,25] 'rêve' cands=['GV']
  POS: [('ê', 'DET')]

 g002 Le chat de la voisine dort.
  GN   [0,7] 'Le chat' cands=['« de la voisine dort » → Le chat', 'dort', 'chat']
  GP   [8,21] 'de la voisine' cands=['GP', 'dort']
  GP   [8,26] 'de la voisine dort' cands=['« de la voisine dort » → Le chat', 'dort', 'chat']
  GV   [22,26] 'dort' cands=['GV']
  POS: []

 r309 Peut-être qu'il viendra.
  GV   [0,9] 'P
… [161 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Implémentation des règles de complétion (copie locale) et mesure dev/test

- **write** `{"content": "\"\"\"topk_v8_rules.py — simulation par sous-classe des règles de complétion des candidats.\n\nAucune modification du dépôt : `HeuristiqueCompletee` hérite de `bl.Heuristique`, appelle\n`super().analyser` puis **ajoute** des candidats aux étiquettes syntagme (jamais ne retire,\njamais n … [7742 caractères tronqués]`

  ```
<path>/tmp/topk_v8_rules.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /tmp && python3 topk_v8_rules.py 2>&1 | tail -160", "description": "Run completion-rule simulation", "timeoutMs": 600000}`

  ```
Traceback (most recent call last):
  File "/tmp/topk_v8_rules.py", line 149, in <module>
    rows = collect(h, tous)
  File "/tmp/topk_v8_rules.py", line 118, in collect
    rows.append({'id': p.get('id'), 'split': 'test' if p in _TEST_IDS else 'dev',
                                                       ^^^^^^^^^^^^^^
TypeError: unhashable type: 'dict'
  ```

- **bash** `{"command": "cd /tmp && sed -i \"s/'split': 'test' if p in _TEST_IDS else 'dev'/'split': 'test' if id(p) in _TEST_IDS else 'dev'/\" topk_v8_rules.py && python3 topk_v8_rules.py 2>&1 | tail -170", "description": "Fix split test and rerun", "timeoutMs": 600000}`

  ```
},
  "candidats_moyens": 2.443,
  "candidats_max": 5
 },
 "R1+R2": {
  "all": {
   "cibles": 239,
   "labels": 212,
   "topk": 212,
   "taux": 0.887,
   "taux_span": 1.0,
   "echecs": 27,
   "echecs_span": 27,
   "echecs_couverture": 0
  },
  "dev": {
   "cibles": 163,
   "labels": 148,
   "topk": 148,
   "taux": 0.908,
   "taux_span": 1.0,
   "echecs": 15,
   "echecs_span": 15,
   "echecs_couverture": 0
  },
  "test": {
   "cibles": 76,
   "labels": 64,
   "topk": 64,
   "taux": 0.8421,
   "taux_span": 1.0,
   "echecs": 12,
   "echecs_span": 12,
   "echecs_couverture": 0
  },
  "par_type": {
   "GP": {
    "cibles": 96,
    "labels": 91,
    "topk": 91
   },
   "REL": {
    "cibles": 74,
    "labels": 58,
    "topk": 58
   },
   "SUB": {
    "cibles": 69,
    "labels": 63,
    "topk": 63
   }
  },
  "par_langue": {
   "en": {
    "cibles": 88,
    "labels": 83,
    "topk": 83
   },
   "fr": {
    "cibles": 151,
    "labels": 129,
    "topk": 129
   }
  },
  "par_source": {
   "hand": {
    "cibles": 13,
    "labels": 12,
    "topk": 12
   },
   "reel": {
    "cibles": 171,
    "labels": 164,
    "topk": 164
   },
   "synthetique": {
    "cibles": 55,
    "labels": 36,
    "topk": 
… [1626 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp && sed -i '/^PY$/d' topk_v8_rules.py && tail -5 topk_v8_rules.py && python3 topk_v8_rules.py 2>&1 | python3 -c \"\nimport sys, json, re\ntxt=sys.stdin.read()\ni=txt.find('{')\n# split the two json objects\ndec=json.JSONDecoder()\nres,_=dec.raw_decode(txt[i:])\nprint(json.dumps({ … [252 caractères tronqués]`

  ```
# contrôle : evaluer_bloc sur la sous-classe R1+R2 (all/dev/test)
    h = HeuristiqueCompletee(('R1', 'R2'))
    got = {nom: eg.evaluer_bloc(nom, h, ps)['attachement'] for nom, ps in
           [('all', tous), ('dev', devp), ('test', testp)]}
    print('evaluer_bloc R1+R2', json.dumps({k: {x: v[x] for x in ('cibles', 'labels', 'topk', 'exact')} for k, v in got.items()}, ensure_ascii=False))
{
 "base": {
  "dev": {
   "cibles": 163,
   "labels": 148,
   "topk": 120,
   "taux": 0.7362,
   "taux_span": 0.8108,
   "echecs": 43,
   "echecs_span": 15,
   "echecs_couverture": 28
  },
  "test": {
   "cibles": 76,
   "labels": 64,
   "topk": 57,
   "taux": 0.75,
   "taux_span": 0.8906,
   "echecs": 19,
   "echecs_span": 12,
   "echecs_couverture": 7
  },
  "all": {
   "cibles": 239,
   "labels": 212,
   "topk": 177,
   "taux": 0.7406,
   "taux_span": 0.8349,
   "echecs": 62,
   "echecs_span": 27,
   "echecs_couverture": 35
  },
  "candidats_moyens": 2.434,
  "candidats_max": 5
 },
 "R1": {
  "dev": {
   "cibles": 163,
   "labels": 148,
   "topk": 148,
   "taux": 0.908,
   "taux_span": 1.0,
   "echecs": 15,
   "echecs_span": 15,
   "echecs_couverture": 0
  },
  "test": {
   "cibles": 76,
   
… [2931 caractères tronqués]
  ```

- **bash** `{"command": "cd /tmp && python3 - <<'PY'\nimport json, collections\nrows=json.load(open('/tmp/topk_v8_rows.json'))\nech=[r for r in rows if not r['ok_topk']]\nspan=[r for r in ech if not r['label']]\ncouv=[r for r in ech if r['label']]\ndef ct(rs, dim): return dict(collections.Counter(r[dim] for r i … [598 caractères tronqués]`

  ```
SPAN 27 {'SUB': 6, 'REL': 16, 'GP': 5} {'en': 5, 'fr': 22} {'hand': 1, 'reel': 7, 'synthetique': 19}
COUV 35 {'GP': 2, 'REL': 32, 'SUB': 1} {'fr': 9, 'en': 26} {'hand': 2, 'reel': 29, 'synthetique': 4}
ECHECS 62 {'GP': 7, 'SUB': 7, 'REL': 48} {'fr': 31, 'en': 31} {'hand': 3, 'reel': 36, 'synthetique': 23}

span fr/synth par type {('en', 'hand', 'SUB'): 1, ('en', 'reel', 'REL'): 2, ('en', 'reel', 'GP'): 1, ('fr', 'reel', 'REL'): 2, ('fr', 'reel', 'SUB'): 1, ('en', 'reel', 'SUB'): 1, ('fr', 'synthetique', 'REL'): 12, ('fr', 'synthetique', 'GP'): 4, ('fr', 'synthetique', 'SUB'): 3}

span ids [('g017', 'en', 'hand', 'SUB'), ('r035', 'en', 'reel', 'REL'), ('r153', 'en', 'reel', 'GP'), ('r255', 'fr', 'reel', 'REL'), ('r264', 'fr', 'reel', 'SUB'), ('r273', 'fr', 'reel', 'REL'), ('r280', 'en', 'reel', 'REL'), ('r288', 'en', 'reel', 'SUB'), ('s010', 'fr', 'synthetique', 'REL'), ('s027', 'fr', 'synthetique', 'GP'), ('s032', 'fr', 'synthetique', 'REL'), ('s035', 'fr', 'synthetique', 'REL'), ('s037', 'fr', 'synthetique', 'REL'), ('s044', 'fr', 'synthetique', 'SUB'), ('s061', 'fr', 'synthetique', 'REL'), ('s065', 'fr', 'synthetique', 'REL'), ('s069', 'fr', 'synthetique', 'REL'), ('s072', 'fr', 
… [1483 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Quantification du bruit des candidats ajoutés et contrôles négatifs

- **write** `{"content": "\"\"\"topk_v8_controls.py — bruit des complétions + contrôles négatifs (hors dépôt).\"\"\"\nfrom __future__ import annotations\nimport sys, json, collections, random\nsys.path.insert(0, '/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/tests/linguistique')\nsys.path.insert(0, '/hom … [6959 caractères tronqués]`

  ```
<path>/tmp/topk_v8_controls.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

