# Session DSH — relecture

- identifiant : `session-3ee08872-fd34-4732-af49-0639cb5d82a9`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-15 05:53:45
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche D3 : la FAQ du produit — 10 questions qu'un utilisateur se pose (la langue, le hors-ligne, le coût, le tagger, le schéma, l'attachement, les spans inatteignables, la restitution, les limites, l'installation) avec les réponses **vérifiées** contre le code courant ; dans `docs/produit/README.md` (une section FAQ) + fiche `reports/rapport-faq.md` + JSON, commit.

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

- **bash** `{"command": "pwd; ls; git status --short | head -50; git log --oneline -5", "description": "Inspect repo state and recent commits"}`

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
 M docs/pilotage/en-cours.md
 M docs/pilotage/roadmap.md
 M docs/produit/README.md
 M journal/2026-11-15/mesures.md
 M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
 M journal/sessions/session-e73a3601-e2c6-417c-a009-88ffadca4e61/digest.md
 M journal/sessions/session-e73a3601-e2c6-417c-a009-88ffadca4e61/rapport.md
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
 M 
… [1299 caractères tronqués]
  ```

- **bash** `{"command": "ls docs/produit 2>/dev/null || echo \"no docs/produit\"; ls reports | head -40", "description": "Check docs/produit and reports"}`

  ```
exemples.md
README.md
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
[stderr]
ls: write error: Broken pipe
  ```

- **bash** `{"command": "wc -l docs/produit/README.md docs/produit/exemples.md docs/pilotage/en-cours.md; git diff --stat", "description": "Check sizes and current diff stat"}`

  ```
679 docs/produit/README.md
 1009 docs/produit/exemples.md
  147 docs/pilotage/en-cours.md
 1835 total
 docs/pilotage/en-cours.md                          |  10 +-
 docs/pilotage/roadmap.md                           |   4 +-
 docs/produit/README.md                             |   9 +
 journal/2026-11-15/mesures.md                      |  15 +
 journal/README.md                                  |   5 +-
 journal/sessions/MANIFEST.md                       |   7 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md |  27 +
 .../rapport.md                                     |  14 +-
 .../digest.md                                      |  98 +++
 .../rapport.md                                     |  54 +-
 reports/INDEX.md                                   |   3 +-
 reports/README.md                                  |   1 +
 reports/pensee-coherence-fiches-v7.json            |  19 +
 reports/pensee-dev-test-v10.json                   |   2 +-
 reports/pensee-quatre-modes.json                   | 734 ++++++++++++---------
 reports/rapport-audit-v7.md                        |   6 +-
 reports/rapport-coherence-fiches-v7.md             |  17 +-
 reports/rapport-dev-test-v10.md              
… [375 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"D3\\|FAQ\\|faq\" docs/pilotage/en-cours.md docs/pilotage/roadmap.md tools/chantier/plan.json | head -40", "description": "Locate D3 references"}`

  ```
tools/chantier/plan.json:531:   "id": "D3",
tools/chantier/plan.json:533:   "titre": "La FAQ du produit",
tools/chantier/plan.json:534:   "mandat": "Tâche D3 : la FAQ du produit — 10 questions qu'un utilisateur se pose (la langue, le hors-ligne, le coût, le tagger, le schéma, l'attachement, les spans inatteignables, la restitution, les limites, l'installation) avec les réponses **vérifiées** contre le code courant ; dans `docs/produit/README.md` (une section FAQ) + fiche `reports/rapport-faq.md` + JSON, commit.",
tools/chantier/plan.json:538:     "commande": "test -f reports/rapport-faq.md && echo FICHE-OK",
  ```

- **bash** `{"command": "sed -n '500,580p' tools/chantier/plan.json", "description": "Read D3 plan block"}`

  ```
{
   "id": "D1",
   "jour": 15,
   "titre": "Les exemples avec le tagger et la base réelle",
   "mandat": "Tâche D1 : les exemples de `docs/produit/exemples.md` — ajoute 3 exemples avec `--tagger` (la sortie réelle avec la clé, le coût affiché) et 2 avec `--reel` (la base honnête), et vérifie que les sorties collent au code courant (F1 0,7902, 238/239, schéma v2). Fiche `reports/rapport-exemples-tagger.md` + JSON, commit.",
   "budget_min": 90,
   "acceptation": [
    {
     "commande": "test -f reports/rapport-exemples-tagger.md && echo FICHE-OK",
     "attendu": "FICHE-OK"
    },
    {
     "commande": "bash tools/porte-produit.sh 2>&1 | tail -1",
     "attendu": "verte"
    }
   ]
  },
  {
   "id": "D2",
   "jour": 15,
   "titre": "La restitution v2 — les rôles",
   "mandat": "Tâche D2 : la restitution v2 — au-delà de la surface exacte (v0) et de la forme canonique (v1), restitue les **rôles** (agent, prédicat, lieu) dans une forme lisible et mesure la fidélité des rôles sur les 46 textes de la v0 ; fiche `reports/rapport-restitution-v2.md` + JSON, tests, commit. Si les rôles ne se restituent pas, écris le négatif.",
   "budget_min": 90,
   "acceptation": [
    {
     "commande"
… [719 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,147p' docs/pilotage/en-cours.md", "description": "Read current state"}`

  ```
# En ce moment

**Mis à jour : 2026-11-15, 05 h 30 HNE (D2)**

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
> le hook pre-commit refuse un fait sans ligne d'état
… [11349 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md"}`

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
… [43755 caractères tronqués]
  ```

- **bash** `{"command": "git diff -- docs/produit/README.md docs/pilotage/en-cours.md docs/pilotage/roadmap.md | head -120", "description": "Show uncommitted doc changes"}`

  ```
diff --git a/docs/pilotage/en-cours.md b/docs/pilotage/en-cours.md
index 578cdace..80739dc3 100644
--- a/docs/pilotage/en-cours.md
+++ b/docs/pilotage/en-cours.md
@@ -1,6 +1,6 @@
 # En ce moment
 
-**Mis à jour : 2026-11-15, 05 h 00 HNE (D1)**
+**Mis à jour : 2026-11-15, 05 h 30 HNE (D2)**
 
 > **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
 > plan plus bas (**La carte**).
@@ -87,7 +87,7 @@
 
 - **S — les structures** : 61/61 types, 144/144 rôles, 56 tests, banque 84/67 ; **19/19 verdicts `389b99f`** ; `/paragraphes` v7, `/` ancien arbre ; [v2](../../reports/rapport-coordination-s-v2.md).
 - **N2 — en pause** : **commande validée** `eval_longueurs.py --rope --val <dir>` (**2,7856**) ; **jamais `--rope` seul** (**40,0658**) ; [v2 : 3,09 tenu](../../reports/rapport-coordination-n2-v2.md) ; puis **porte propre (0,29)**.
-- **Pensée — B13 (actif)** : **183/183** ; `r035` (238/238), convention GV (0,7902), `s065` (238/238), **J6.1 rejeté** (g017 à trancher), schéma v2, restitution v1 (46/46, strict 0,1087), **J9.1** (19 fiches), **D1** ; [s065](../../reports/rapport-s065.md), [restitution v1](../../reports/rapport-restitution-v1.md), [J9.1
… [13251 caractères tronqués]
  ```

- **bash** `{"command": "ls -a .git/hooks/ | grep -v sample; sed -n '1,80p' tools/porte-produit.sh", "description": "Check hooks and product gate"}`

  ```
.
..
pre-commit
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
    dit ❌ "analyser $langue 
… [2158 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '80,200p' tools/porte-produit.sh", "description": "Read rest of product gate"}`

  ```
d = json.load(sys.stdin)
assert d['schema'] == 'drave.restitution.v2', d.get('schema')
assert d['roles']['principal']['agent'] == 'Le chat', d['roles']['principal']
assert d['roles']['principal']['predicat'] == 'dort', d['roles']['principal']
assert d['rendu']['exact'], d['rendu']
assert d['controle_negatif_rendu']['detecte'], d['controle_negatif_rendu']
" 2>/dev/null; then
  dit ✅ "restitution v2 : rôles lisibles, rendu relu, contrôle détecté"
else
  dit ❌ "restitution v2 : sortie inattendue : $sortie"; ko=1
fi

if python3 tools/tests/test_restitution.py >/tmp/porte-produit-restitution.log 2>&1; then
  dit ✅ "restitution v0/v1 : $(grep -oE 'Ran [0-9]+ tests' /tmp/porte-produit-restitution.log | head -1)"
else
  dit ❌ "restitution v0/v1 en échec (voir /tmp/porte-produit-restitution.log)"; ko=1
fi

if python3 tools/tests/test_restitution_v2.py >/tmp/porte-produit-restitution-v2.log 2>&1; then
  dit ✅ "restitution v2 : $(grep -oE 'Ran [0-9]+ tests' /tmp/porte-produit-restitution-v2.log | head -1)"
else
  dit ❌ "restitution v2 en échec (voir /tmp/porte-produit-restitution-v2.log)"; ko=1
fi

if python3 tools/tests/test_schema_produit.py >/tmp/porte-produit-schema.log 2>&1; then
  dit ✅
… [907 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,200p' .git/hooks/pre-commit", "description": "Read pre-commit hook"}`

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

- **bash** `{"command": "python3 tools/drave.py --version; python3 tools/drave.py --aide 2>&1 | head -60; echo \"---\"; python3 tools/drave.py analyser \"Le chat dort.\" | head -5", "description": "Run CLI help and basic analysis"}`

  ```
drave 0.1.0
usage: drave [-h] [-V] {analyser,evaluer,rejouer,restituer} ...

Point d'entrée produit du bloc linguistique (analyse et restitution).

arguments:
  {analyser,evaluer,rejouer,restituer}
    analyser            étiqueter un texte (POS, syntagmes, pragmatique)
    evaluer             mesurer l'heuristique sur le gold
    rejouer             analyser deux fois et vérifier le déterminisme
    restituer           reconstruire la surface depuis l'annotation et mesurer le miroir

options:
  -h, --help, --aide    afficher cette aide et quitter
  -V, --version         afficher la version et quitter

Commandes : analyser, evaluer, rejouer, restituer.
Codes de sortie : 0 succès · 2 usage · 3 refus d'analyse (JSON) ·
4 clé/tagger absent · 1 erreur.
Options : --json, --langue fr|en, --partition brut|alternative|filtrer_union|filtrer,
--contexte, --banc, --tagger.
Limites : heuristique CPU, hors ligne, déterministe par défaut ; --tagger appelle l'API
DeepSeek (clé, réseau) pour le POS ; la restitution est un codec de surface (graphème),
pas un décodeur neuronal ; ni traduction ni génération.
Exemples :
  python3 tools/drave.py analyser "Le chat dort."
  python3 tools/drave.py analyse
… [460 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"tagger\\|DEEPSEEK\\|socket\\|reseau\\|réseau\\|exit\\|code 4\\|return 4\" tools/drave.py | head -80", "description": "Inspect tagger/network code"}`

  ```
8:    python3 tools/drave.py analyser "Le chat dort." --tagger          # API DeepSeek (clé, réseau)
11:    python3 tools/drave.py evaluer --tagger --json                    # heuristique + cascade API
23:En **option** (`--tagger`, `analyser` et `evaluer`), le POS (et lui seul) vient du tagger de
24:l'API DeepSeek : la clé est lue dans `DEEPSEEK_KEY_FILE`, `~/.config/drave/deepseek.key` puis
25:`DEEPSEEK_API_KEY` ; le cache du client évite de refaire un appel ; la clé n'est jamais affichée.
26:**Sans `--tagger`, le défaut ne change pas** : heuristique, CPU, hors ligne, déterministe.
30:Codes de sortie : 0 succès · 2 usage · 3 refus d'analyse · 4 clé/tagger absent · 1 erreur.
60:# Le tagger est une **option** : sans `--tagger`, rien de ce bloc n'est importé ni exécuté.
63:# La fusion de l'option : le POS vient du tagger, tout le reste de l'heuristique. On ne force
88:# --------------------------------------------------------------------------- le tagger (option)
92:    """Aucune clé : le tagger est une option, jamais un prérequis du produit."""
102:def _cle_tagger() -> str:
104:    for variable in ("DEEPSEEK_KEY_FILE", "DSH_KEY_FILE"):
113:    for variable in ("DEEPSEEK_API_KEY", "D
… [4613 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,230p' tools/drave.py", "description": "Read top of drave.py"}`

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
… [9120 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '330,430p' tools/drave.py; sed -n '700,810p' tools/drave.py", "description": "Read main and parser definition"}`

  ```
return pathlib.Path(args.fichier).read_text(encoding="utf-8", errors="replace")
    return args.texte or ""


def _analyser_jsonl(texte: str, args: argparse.Namespace, h: bl.Heuristique, bloc,
                    stats: dict | None = None) -> int:
    """Une **ligne JSON par phrase** (traitement de corpus : `--jsonl`).

    `h` segmente (le tagger ne change pas les frontières de phrase) ; `bloc` analyse — la
    cascade du tagger quand `--tagger` est posé. Le coût va sur `stderr`, jamais dans le JSONL.
    """
    n = 0
    refus = 0
    for debut, fin, _typ, _ in h._phrases(texte):
        phrase = texte[debut:fin]
        if not phrase.strip():
            continue
        a = bloc.analyser(phrase, args.langue, args.contexte)
        refus += int(bool(a.refus))
        sys.stdout.write(_sur(json.dumps(a.json(), ensure_ascii=False)) + "\n")
        n += 1
    if n == 0:
        print(f"{NOM}: refus d'analyse : vide", file=sys.stderr)
        return 3
    if stats is not None:
        print(f"{NOM}: TAGGER API · {_ligne_tagger(stats)}", file=sys.stderr)
        if refus:
            print(f"{NOM}: tagger · {refus}/{n} phrase(s) refusée(s) (JSON partiel)",
                  file=sys
… [7951 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '810,920p' tools/drave.py", "description": "Read parser options"}`

  ```
sous = parseur.add_subparsers(dest="commande",
                                  metavar="{analyser,evaluer,rejouer,restituer}",
                                  required=True)

    analyser = sous.add_parser(
        "analyser",
        help="étiqueter un texte (POS, syntagmes, pragmatique)",
        description="Analyse un texte avec l'heuristique et rend la lecture compacte ou le JSON. "
                    "Avec --tagger, le POS (et lui seul) vient du tagger de l'API DeepSeek : "
                    "clé requise, réseau, cache du client ; sans l'option, rien ne change.",
        epilog="Exemples : python3 tools/drave.py analyser \"Le chat dort.\" --json ; "
               "python3 tools/drave.py analyser \"Le chat dort.\" --tagger",
        formatter_class=_Formateur,
    )
    analyser.add_argument("texte", metavar="TEXTE", nargs="?", default=None,
                          help="texte à analyser (entre guillemets) ou --fichier")
    analyser.add_argument("--partition", choices=("brut", "alternative", "filtrer_union", "filtrer"),
                          default="alternative",
                          help="la vue des syntagmes qui se chevauchent (défaut : alternative)")
  
… [6178 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"socket\\|réseau\\|reseau\\|import\\|offline\\|hors ligne\\|DEEPSEEK\" tools/tests/test_tagger_api.py tools/tests/test_produit.py | head -60", "description": "Search offline tests"}`

  ```
tools/tests/test_tagger_api.py:1:"""test_tagger_api.py — le tagger POS par API, **en option**, sans réseau.
tools/tests/test_tagger_api.py:12:6. l'ordre de résolution de la clé : `DEEPSEEK_KEY_FILE`, puis `~/.config/drave/deepseek.key`,
tools/tests/test_tagger_api.py:13:   puis `DEEPSEEK_API_KEY`.
tools/tests/test_tagger_api.py:15:Aucun test n'ouvre de socket : les transports sont injectés, et le test « sans clé » lance la
tools/tests/test_tagger_api.py:19:from __future__ import annotations
tools/tests/test_tagger_api.py:21:import contextlib
tools/tests/test_tagger_api.py:22:import copy
tools/tests/test_tagger_api.py:23:import io
tools/tests/test_tagger_api.py:24:import json
tools/tests/test_tagger_api.py:25:import os
tools/tests/test_tagger_api.py:26:import pathlib
tools/tests/test_tagger_api.py:27:import subprocess
tools/tests/test_tagger_api.py:28:import sys
tools/tests/test_tagger_api.py:29:import tempfile
tools/tests/test_tagger_api.py:30:import unittest
tools/tests/test_tagger_api.py:31:from types import SimpleNamespace
tools/tests/test_tagger_api.py:32:from unittest import mock
tools/tests/test_tagger_api.py:39:import bloc_linguistique as bl  # noqa: E402
tools/tests/test_ta
… [2312 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' reports/rapport-tagger-option.md", "description": "Read tagger report"}`

  ```
# R0.7 / 1A — le tagger POS en option : +8,57 pts sur 20 phrases, +8,49 sur le gold 612 ; le défaut reste hors ligne

> **Ligne de roadmap** : **R0.7** (le lecteur) · **Décision** : **1A** du 14/11 · **Date** :
> 2026-11-14 · **Verdict** : ✅ **option livrée** — `--tagger` sur `analyser` et `evaluer` ; POS
> **88,57 % → 97,14 %** sur 20 phrases `hand` (**+8,57 pts**), cohérent avec le **0,9475 contre
> 0,8625** du gold 612 (**+8,49**) ; **40 appels**, **11 868 tokens** (cache neuf), **0 refus** ;
> le **défaut** reste l'**heuristique**, CPU, hors ligne, déterministe. Le gain est **+4,67** sur
> le seul gold réel 432 : lire le chiffre avec sa source.

## 1 bis. Les deux défauts corrigés (15/11)

| défaut | avant | **après** |
|---|---|---|
| **2 appels par phrase** (le tagger de syntagmes était appelé sans être utilisé) | 2 appels | **1 appel** |
| **`PONCT` perdu** (le tagger ne reçoit que mots et nombres) | 0 ponctuation étiquetée | **25/25** (restituée depuis l'heuristique) |

**La mesure sur le gold 612** (avec la clé, cache partiel) : POS **0,9575** contre 0,8625 pour
l'heuristique — **+9,5 points** (le `PONCT` restitué ajoute 0,25 pt ; le reste vient du tagger).
**Sur la base r
… [5591 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,90p' reports/rapport-restitution-v2.md", "description": "Read restitution v2 report"}`

  ```
# B13 — la restitution v2 : les rôles se lisent, leur fidélité ne suit pas

> **Ligne de roadmap** : **B13** (produit) · **Tâche** : D2 · **Date** : 2026-11-15 ·
> **Verdict** : ❌ **négatif sur la fidélité** — la forme est fidèle (46/46), la sémantique
> ne l'est pas : **19/46 cadres exacts** (dont **16 non vides**), **F1 0,5270**, **32 faux
> positifs** et **38 faux négatifs**.
>
> **La question.** Au-delà de la surface exacte (v0 : 46/46) et de la forme canonique
> (v1 : 46/46), peut-on **restitue les rôles** — agent, prédicat, lieu — dans une forme
> lisible et **mesurer leur fidélité** sur les **46 textes annotables** de la v0 ?
>
> **La réponse.** Les rôles **se restituent** comme **forme** : un cadre principal lisible,
> 198 segments de rôle, 198/198 spans dans la source, et un rendu qui se relit à l'identique
> (**46/46**). Mais leur **fidélité au texte** n'est pas acquise : sur un or écrit à la main,
> **19/46 cadres exacts** (0,4130), **16/46 non vides** (0,3478), **91/138 cellules de rôle
> exactes** (0,6594) — mais seulement **39 justes sur 77 attendus** et **71 prédits**, soit
> **précision 0,5493 · rappel 0,5065 · F1 0,5270**. Le contrôle « rôle constant par type »
> n
… [3275 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,80p' reports/rapport-restitution-v1.md; echo ====; sed -n '1,60p' reports/rapport-restitution-v0.md", "description": "Read restitution v0/v1 reports"}`

  ```
# B13 — la restitution v1 : la forme canonique à 46/46, le miroir strict reste à 0,1087

> **Ligne de roadmap** : **B13** (produit) · **Tâche** : J8.1 · **Date** : 2026-11-14 ·
> **Verdict** : ✅
>
> **La question.** Au-delà de la surface exacte (46/46), produire une **forme canonique**
> depuis l'annotation — **segments + rôles + cibles** — et la mesurer : le **miroir strict**
> (0,1087) doit-il monter ?
>
> **La réponse.** **Non — et il ne doit pas.** Le miroir strict compare une sortie à la
> **surface brute** ; la forme canonique replie la casse, retire la ponctuation et réduit
> les espaces. Contre la source canonisée, elle est exacte **46/46 = 1,0000** ; contre la
> source brute, elle tombe à **1/46 = 0,0217** (seul `f18`, `1234567890`, n'a ni casse ni
> ponctuation). Le **miroir strict reste 5/46 = 0,1087** : la v1 ne fabrique pas de
> surface, elle mesure autre chose. Le chiffre utile de la v1 est **1,0000 canonique**,
> pas 0,1087 strict.
>
> **Le chiffre.** 46 annotations, **46/46 formes canoniques exactes** contre la source
> canonisée ; **395 segments**, **395 rôles**, **315 cibles**, **315/315 cibles résolues**
> dans la source, **313/315** portées par un autre segment 
… [6066 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"Python\\|pip\\|installation\\|Installer\\|prérequis\\|dépendance\\|3.10\\|3.13\" README.md docs/produit/README.md | head -40", "description": "Search install info"}`

  ```
docs/produit/README.md:32:**Prérequis** : le dépôt, Python 3.10+ (testé en 3.13), **aucune dépendance externe**, aucun GPU,
docs/produit/README.md:515:| **`drave evaluer`** | **0,55 s** au total | une lecture (heuristique), démarrage Python compris |
docs/produit/README.md:560:| **4** | dépendance absente : la clé du tagger | `--tagger` sans clé (message clair, rien sur `stdout`) |
docs/produit/README.md:570:Le point d'entrée existe : `tools/drave.py`, version **0.1.0**, sans dépendance externe.
docs/produit/README.md:636:| **l'entrée standard** | `--fichier` lit un fichier, mais pas de pipe (`cat corpus.txt \| drave analyser`) |
docs/produit/README.md:639:| **`--mode` / la cascade locale** | le CLI expose l'heuristique et la cascade **API** (`--tagger`) ; `parallele` et la cascade **locale** demandent le code Python |
docs/produit/README.md:646:| **l'empaquetage** | pas de `pip install`, pas de commande `drave` dans le `PATH` ; tout part de la racine du dépôt |
  ```

- **bash** `{"command": "cat tools/schemas/drave-annotation-v2.json | head -80; echo ===; ls tools/schemas", "description": "Inspect schema v2"}`

  ```
{
 "$schema": "https://json-schema.org/draft/2020-12/schema",
 "$id": "https://drave.local/schema/annotation-v2.json",
 "title": "drave.annotation v2",
 "description": "L'annotation du bloc linguistique heuristique, version 2 : identique à la v1 et documente, dans `meta`, la partition des syntagmes qui se chevauchent (`meta.partition`) et les segments alternatifs du groupe (`meta.alternative`). Les deux champs sont additifs et optionnels : v1 reste lue.",
 "type": "object",
 "required": [
  "schema",
  "version",
  "texte",
  "langue",
  "script",
  "refus",
  "etiquettes",
  "unites_semantiques"
 ],
 "properties": {
  "schema": {
   "const": "drave.annotation"
  },
  "version": {
   "const": 2
  },
  "texte": {
   "type": "string"
  },
  "langue": {
   "type": "string",
   "pattern": "^[a-z]{2,3}$|^und$"
  },
  "script": {
   "type": "string"
  },
  "source": {
   "type": "string"
  },
  "refus": {
   "type": "string",
   "enum": [
    "",
    "vide",
    "non_texte",
    "trop_long",
    "neuronal"
   ]
  },
  "etiquettes": {
   "type": "array",
   "items": {
    "type": "object",
    "required": [
     "niveau",
     "type",
     "valeur",
     "debut",
     "fin",
     "source"
… [423 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"rapport-.*\\.md\\|\\.json\" reports/README.md | head -30; sed -n '1,80p' reports/README.md", "description": "Read reports conventions"}`

  ```
18:| [`rapport-bilan-nuit.md`](rapport-bilan-nuit.md) | **Bilan** — la nuit du 14 au 15/11 : le tagger, la base honnête, la phase C/B |
19:| [`rapport-gold-reel-50.md`](rapport-gold-reel-50.md) | **R0.7** — le gold réel : 452 phrases, 50 ratées, le « 200+ » obsolète |
20:| [`rapport-protocole-date.md`](rapport-protocole-date.md) | **Panini** — le protocole à date contrôlée : 60 paires, trois strates |
21:| [`rapport-cic-v2.md`](rapport-cic-v2.md) | **Panini** — le CIC v2 : 42/42, les types clos, le sha256 sans hashlib |
22:| [`rapport-base-reelle.md`](rapport-base-reelle.md) | **B13** — la base honnête : `--reel`, 452 phrases, POS 88,91 %, F1 79,06 % |
24:| [`rapport-panini-334.md`](rapport-panini-334.md) | **Panini** — le §334 : H0 0,909/0,906, la |
25:| [`rapport-exemples-rejoues.md`](rapport-exemples-rejoues.md) | **B13** — les 5 exemples de la doc |
26:| [`rapport-exemples-tagger.md`](rapport-exemples-tagger.md) | **D1** — les 3 exemples `--tagger` (coût affiché) et les 2 `--reel` (base honnête) |
27:| [`rapport-evaluer-langue.md`](rapport-evaluer-langue.md) | **B13** — `evaluer --par-langue` : fr 0,8159 / |
28:| [`rapport-robustesse-semaine.md`](rapport-robustesse-semaine.md) 
… [10397 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' reports/INDEX.md", "description": "Read reports index top"}`

  ```
# Index des fiches de reports/

> **Généré** par `tools/index_reports.py` — **741 fiches**. Les fichiers
> d'infrastructure (`README.md`, `INDEX.md`, `historique-*`) sont exclus du tableau ;
> la page d'état, elle, compte tous les `.md` de `reports/`.

| fiche | titre |
|---|---|
| [07-mesures-couche-commune.md](07-mesures-couche-commune.md) | 7. Les modèles alternatifs pour l'entrée et la sortie — vers une couche commune |
| [aiguille-30b.md](aiguille-30b.md) | aiguille v2 — /home/stephane/Data13TB/stephane/modeles/gguf/Qwen3-30B-A3B-Instruct-2507-Q4_K_M.gguf |
| [aiguille-gpt-oss.md](aiguille-gpt-oss.md) | aiguille v2 — /home/stephane/Data13TB/stephane/modeles/gguf/gpt-oss-120b-MXFP4.gguf |
| [alignement-verne.md](alignement-verne.md) | Alignement phrase à phrase — *Le Tour du monde en quatre-vingts jours* (français → anglais) |
| [bilan-b11.md](bilan-b11.md) | Bilan B11 — ce qui tient, ce qui ne tient pas |
| [bilan-multi-materiel.md](bilan-multi-materiel.md) | Bilan multi-matériel — CPU, FPGA, GPU |
| [campagne-benefices.md](campagne-benefices.md) | Campagne 24 h — où Drave est à son meilleur, tâche par tâche |
| [fiche-nuit-17-10.md](fiche-nuit-17-10.md) | La nuit du 17 au 18 
… [14520 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/drave.py evaluer --json > /tmp/faq-eval.json 2>/tmp/faq-eval.err; echo exit=$?; python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/faq-eval.json'))\ndef walk(o,p=''):\n    if isinstance(o,dict):\n        for k,v in o.items():\n            if isinstance(v,(dict,list)): w … [192 caractères tronqués]`

  ```
exit=0
/version = 0.1.0
/gold/nom = vivant (hand + reel + synthétique)
/gold/gele = False
/gold/phrases = 612
/gold/tokens = 3179
/gold/cibles_attachement = 239
/heuristique/bloc = heuristique
/heuristique/phrases = 612
/heuristique/pos/exactitude = 0.8625
/heuristique/pos/exactitude_ferme = 0.9373
/heuristique/pos/exactitude_ouvert = 0.7918
/heuristique/pos/tokens = 3179
/heuristique/pos/confusions/ADJ/ADJ = 65
/heuristique/pos/confusions/ADJ/NOUN = 65
/heuristique/pos/confusions/ADJ/VERB = 4
/heuristique/pos/confusions/ADV/ADV = 131
/heuristique/pos/confusions/ADV/NOUN = 7
/heuristique/pos/confusions/ADV/PREP = 1
/heuristique/pos/confusions/ADV/ADJ = 1
/heuristique/pos/confusions/ADV/? = 1
/heuristique/pos/confusions/AUX/PREP = 4
/heuristique/pos/confusions/AUX/AUX = 119
/heuristique/pos/confusions/AUX/? = 3
/heuristique/pos/confusions/AUX/NOUN = 1
/heuristique/pos/confusions/AUX/VERB = 1
/heuristique/pos/confusions/CONJ/PRON = 15
/heuristique/pos/confusions/CONJ/CONJ = 68
/heuristique/pos/confusions/CONJ/? = 13
/heuristique/pos/confusions/CONJ/PREP = 2
/heuristique/pos/confusions/DET/DET = 586
/heuristique/pos/confusions/DET/? = 2
/heuristique/pos/confusions/NOUN/NOUN = 657
/heu
… [3999 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/verifier_schema_produit.py --json > /tmp/faq-schema.json 2>/tmp/faq-schema.err; echo exit=$?; cat /tmp/faq-schema.json; cat /tmp/faq-schema.err | head", "description": "Run schema verifier JSON"}`

  ```
exit=0
{
 "schemas": {
  "1": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/schemas/drave-annotation-v1.json",
  "2": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/schemas/drave-annotation-v2.json"
 },
 "versions_lues": [
  1,
  2
 ],
 "validateur": true,
 "retrocompatibilite": {
  "v1_lue": true,
  "v2_refuse_v1": true
 },
 "cas": [
  {
   "cas": "fr",
   "version": 2,
   "ok": true,
   "erreurs": []
  },
  {
   "cas": "en",
   "version": 2,
   "ok": true,
   "erreurs": []
  },
  {
   "cas": "vide",
   "version": 2,
   "ok": true,
   "erreurs": []
  },
  {
   "cas": "ponctuation",
   "version": 2,
   "ok": true,
   "erreurs": []
  },
  {
   "cas": "long",
   "version": 2,
   "ok": true,
   "erreurs": []
  },
  {
   "cas": "v1",
   "version": 1,
   "ok": true,
   "erreurs": []
  }
 ]
}
  ```

- **bash** `{"command": "set +e\npython3 tools/drave.py analyser \"Élodie sourit.\" --json >/tmp/faq-und.json 2>/tmp/faq-und.err; echo und_exit=$?\npython3 -c \"import json; d=json.load(open('/tmp/faq-und.json')); print('langue',d['langue'],'refus',d['refus'])\"\npython3 tools/drave.py analyser \"Le chat dort.\ … [374 caractères tronqués]`

  ```
und_exit=0
langue und refus 
de_exit=2
usage: drave analyser [-h] [--partition {brut,alternative,filtrer_union,filtrer}] [--fichier CHEMIN]
                      [--jsonl] [--contexte CONTEXTE] [--langue {fr,en}] [--tagger] [--json]
und_fr_exit=0
langue und
  ```

- **bash** `{"command": "env -u DEEPSEEK_KEY_FILE -u DSH_KEY_FILE -u DEEPSEEK_API_KEY -u DSH_API_KEY HOME=/tmp/faq-home python3 tools/drave.py analyser \"Le chat dort.\" --tagger >/tmp/faq-tagger.out 2>/tmp/faq-tagger.err; echo exit=$?; echo \"stdout=[$(cat /tmp/faq-tagger.out)]\"; head -3 /tmp/faq-tagger.err", … [49 caractères tronqués]`

  ```
exit=4
stdout=[]
drave: dépendance absente : clé DeepSeek absente : exportez DEEPSEEK_KEY_FILE, déposez la clé dans ~/.config/drave/deepseek.key, ou exportez DEEPSEEK_API_KEY. Sans --tagger, le défaut reste l'heuristique hors ligne.
  ```

- **bash** `{"command": "python3 tools/drave.py restituer --banc reports/pensee-fiabilite-produit.json --json > /tmp/faq-rest-v0.json 2>/tmp/faq-rest-v0.err; echo exit=$?; python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/faq-rest-v0.json'))\nfor k,v in d.items():\n    if not isinstance(v,(list,dict)): prin … [87 caractères tronqués]`

  ```
exit=0
schema = drave.restitution.banc
version = 1
definition_miroir = minimum des fidélités binaires de la surface (graphème), des mots et des POS ; une sortie n'est fidèle que si elle reproduit exactement la source
banc = reports/pensee-fiabilite-produit.json
keys ['schema', 'version', 'definition_miroir', 'parametres', 'synthese', 'resultats', 'banc']
  ```

- **bash** `{"command": "python3 tools/drave.py restituer --banc reports/pensee-fiabilite-produit.json --roles --json > /tmp/faq-rest-v2.json 2>/tmp/faq-rest-v2.err; echo exit=$?; python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/faq-rest-v2.json'))\nprint('schema',d.get('schema'),'version',d.get('version') … [155 caractères tronqués]`

  ```
exit=0
schema drave.restitution.v2.banc version 1
schema = drave.restitution.v2.banc
version = 1
definition = rôles (agent, prédicat, lieu) lus depuis les syntagmes ; cadre principal ; fidélité comparée à l'or écrit à la main
banc = reports/pensee-fiabilite-produit.json
keys ['schema', 'version', 'definition', 'parametres', 'synthese', 'resultats', 'banc']
  ```

- **bash** `{"command": "python3 tools/drave.py restituer \"Le chat dort.\" --json > /tmp/faq-rest-one.json; python3 - <<'PY'\nimport json\nd=json.load(open('/tmp/faq-rest-one.json'))\nfor k,v in d.items():\n    if not isinstance(v,(dict,list)): print(k,'=',v)\nprint(json.dumps(d,ensure_ascii=False)[:1200])\nPY … [48 caractères tronqués]`

  ```
schema = drave.restitution
version = 1
langue = fr
refus = 
source_caracteres = 13
source_octets = 13
etiquettes = 20
{"schema": "drave.restitution", "version": 1, "langue": "fr", "refus": "", "source_caracteres": 13, "source_octets": 13, "etiquettes": 20, "niveaux": {"graphème": {"exact": true, "fidelite": 1.0, "fidelite_caractere": 1.0, "caracteres": 13, "octets": 13, "niveau": "graphème", "nom": "surface", "rendu": "Le chat dort.", "couverture": 1.0}, "mot": {"exact": false, "fidelite": 0.0, "fidelite_caractere": 0.9286, "caracteres": 14, "octets": 14, "niveau": "mot", "nom": "mots", "rendu": "Le chat dort .", "couverture": 0.8462}, "pos": {"exact": false, "fidelite": 0.0, "fidelite_caractere": 0.9286, "caracteres": 14, "octets": 14, "niveau": "pos", "nom": "pos", "rendu": "Le chat dort .", "couverture": 0.8462}}, "surface": {"exact": true, "fidelite": 1.0, "fidelite_caractere": 1.0, "caracteres": 13, "octets": 13, "niveau": "graphème", "nom": "surface", "rendu": "Le chat dort.", "couverture": 1.0}, "surface_sans_controle": {"exact": true, "fidelite": 1.0, "fidelite_caractere": 1.0, "caracteres": 13, "octets": 13}, "miroir": {"definition": "minimum des fidélités binaires de la s
… [118 caractères tronqués]
  ```

- **bash** `{"command": "python3 -c \"import json; d=json.load(open('reports/pensee-tagger-option.json')); print(json.dumps(d,ensure_ascii=False,indent=1)[:3000])\"", "description": "Inspect tagger option JSON"}`

  ```
{
 "date": "2026-11-14",
 "branche": "s/v7",
 "decision": "1A — le tagger API en option, le défaut reste hors ligne",
 "ligne_roadmap": "R0.7 (le lecteur)",
 "option": {
  "drapeau": "--tagger",
  "commandes": [
   "analyser",
   "evaluer"
  ],
  "modele_demande": "deepseek-chat",
  "seuil_cascade": 0.6,
  "fusion": {
   "pos": "neuronal (tagger)",
   "syntagme": "heuristique",
   "pragmatique": "heuristique",
   "pourquoi": "le tagger ne rend ni rôle ni cible : forcer ses syntagmes ferait perdre l'attachement mesuré"
  },
  "cle": [
   "DEEPSEEK_KEY_FILE",
   "~/.config/drave/deepseek.key",
   "DEEPSEEK_API_KEY",
   "DSH_KEY_FILE / DSH_API_KEY (repli)"
  ],
  "cle_absente": {
   "code": 4,
   "message": "clé DeepSeek absente ; le défaut reste l'heuristique hors ligne"
  },
  "cache": "mémoire par (texte, langue) dans chaque tagger + cache disque du client (modèle + messages + température + max_tokens, jamais la clé)",
  "defaut": "heuristique, CPU, hors ligne, déterministe ; aucun import du module réseau"
 },
 "mesure_20": {
  "dispositif": "20 premières phrases de gold.json (source hand), 105 tokens ; transport réel via tools/llm/deepseek.py, température 0, cache neuf /tmp/drave-
… [1800 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nfor f in ['/tmp/faq-rest-v0.json','/tmp/faq-rest-v2.json']:\n    d=json.load(open(f)); print('===',f)\n    print(json.dumps(d['synthese'],ensure_ascii=False,indent=1))\nPY", "description": "Print restitution synthesis"}`

  ```
=== /tmp/faq-rest-v0.json
{
 "n": 50,
 "annotations": 46,
 "refus": 4,
 "refus_ids": [
  "f14",
  "f15",
  "f16",
  "f17"
 ],
 "surface": {
  "exacts": 46,
  "fidelite": 1.0,
  "fidelite_caractere": 1.0
 },
 "surface_sans_controle": {
  "exacts": 45,
  "fidelite": 0.9783,
  "fidelite_caractere": 0.9999
 },
 "mots": {
  "exacts": 5,
  "fidelite": 0.1087,
  "fidelite_caractere": 0.9506
 },
 "pos": {
  "exacts": 5,
  "fidelite": 0.1087,
  "fidelite_caractere": 0.9506
 },
 "miroir": {
  "exacts": 5,
  "fidelite": 0.1087
 },
 "controle_negatif": {
  "melange_exacts": 0,
  "melange_fidelite": 0.0,
  "melange_fidelite_caractere": 0.263,
  "tronque_exacts": 0,
  "tronque_fidelite_caractere": 0.9506,
  "detectes": 46
 }
}
=== /tmp/faq-rest-v2.json
{
 "n": 50,
 "annotations": 46,
 "refus": 4,
 "refus_ids": [
  "f14",
  "f15",
  "f16",
  "f17"
 ],
 "or": {
  "textes": 46,
  "variantes": 65,
  "roles_attendus": 77
 },
 "cadre": {
  "exacts": 19,
  "taux": 0.413,
  "exacts_non_vides": 16,
  "exacts_vides": 3,
  "partiels": 42,
  "partiels_taux": 0.913,
  "exacts_stricts": 16,
  "taux_strict": 0.3478,
  "roles_exacts_moyens": 1.9783
 },
 "or_textes": 46,
 "roles": {
  "exacts": 91,
  "total": 13
… [4966 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-tagger-option.json'))\nprint(json.dumps(d.get('mesure_612_reference'),ensure_ascii=False,indent=1))\nprint('TOP KEYS',list(d))\nPY", "description": "Print tagger 612 reference"}`

  ```
{
 "source": "reports/tagger-612.json",
 "date": "2026-11-13 22:21 EST",
 "gold": {
  "phrases": 612,
  "tokens": 3179,
  "sources": {
   "hand": 20,
   "reel": 432,
   "synth": 160
  },
  "modalite": "api-deepseek (deepseek-chat → modèle renvoyé), aucun serveur local"
 },
 "heuristique_pos": 0.8625,
 "cascade_pos": 0.9475,
 "delta_pos_publie": 0.0849,
 "par_source": {
  "hand": {
   "heuristique": 0.8857,
   "neuronal": 0.9714,
   "delta": 0.0857
  },
  "reel": {
   "heuristique": 0.8893,
   "neuronal": 0.936,
   "delta": 0.0467
  },
  "synth": {
   "heuristique": 0.7682,
   "neuronal": 0.9828,
   "delta": 0.2146
  }
 },
 "appels": 1218,
 "tokens": 358962,
 "latence_s": 1257.9579999999992,
 "duree_totale_s": 1259.2,
 "refus": 1,
 "refus_detail": [
  "s015"
 ],
 "modeles_renvoyes": {
  "deepseek-flash": 1218
 },
 "cout_annonce_usd": 0.04
}
TOP KEYS ['date', 'branche', 'decision', 'ligne_roadmap', 'option', 'mesure_20', 'mesure_612_reference', 'tests', 'limites', 'apres_15_11', 'base_reelle_452']
  ```

- **bash** `{"command": "python3 tools/drave.py restituer \"Le chat dort.\" --roles --json | python3 -c \"import json,sys; d=json.load(sys.stdin); print(json.dumps({k:d[k] for k in d if k in ('schema','version','roles','rendu','controle_negatif_rendu')},ensure_ascii=False,indent=1))\"", "description": "Inspect  … [22 caractères tronqués]`

  ```
{
 "schema": "drave.restitution.v2",
 "version": 1,
 "roles": {
  "definition": "cadre principal (agent, prédicat, lieu) lu depuis les syntagmes et leur meta.role ; cadres par prédicat ; segments de rôle",
  "principal": {
   "agent": "Le chat",
   "predicat": "dort",
   "lieu": "",
   "agent_role": "agent",
   "agent_origine": "agent_avant",
   "lieu_role": "",
   "lieu_origine": "",
   "agent_span": [
    0,
    7
   ],
   "predicat_span": [
    8,
    12
   ],
   "lieu_span": null
  },
  "cadres": [
   {
    "agent": "Le chat",
    "predicat": "dort",
    "lieu": "",
    "agent_role": "agent",
    "agent_origine": "agent_avant",
    "lieu_role": "",
    "lieu_origine": "",
    "agent_span": [
     0,
     7
    ],
    "predicat_span": [
     8,
     12
    ],
    "lieu_span": null
   }
  ],
  "segments": [
   {
    "type": "GN",
    "role": "agent",
    "role_normalise": "agent",
    "niveau": 1,
    "debut": 0,
    "fin": 7,
    "valeur": "Le chat",
    "cible": "dort",
    "lineaire": true,
    "union": false,
    "confiance": 0.55,
    "source": "heuristique"
   },
   {
    "type": "GV",
    "role": "predicat",
    "role_normalise": "predicat",
    "niveau": 0,
    "debut": 8
… [2056 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-tagger-option.json'))\nprint(json.dumps(d.get('apres_15_11'),ensure_ascii=False,indent=1))\nprint(json.dumps(d.get('base_reelle_452'),ensure_ascii=False,indent=1))\nPY", "description": "Inspect updated tagger figures"}`

  ```
{
 "appels_par_phrase": 1,
 "ponct": "25/25",
 "pos_612": 0.9575,
 "delta": 0.095,
 "cout": {
  "appels": 609,
  "tokens": 22299,
  "latence_s": 155.636,
  "requetes": 159
 }
}
{
 "pos_heuristique": 0.8891,
 "pos_tagger": 0.95,
 "delta": 0.0609,
 "appels": 449,
 "cache": 449,
 "reseau": 0
}
  ```

- **bash** `{"command": "grep -rn \"22299\\|22 299\\|609 appels\\|155 s\\|0.9575\\|0,9575\" reports/*.json reports/*.md | head -30", "description": "Locate current tagger cost figures"}`

  ```
reports/atomes-prediction.json:9369:    "graph_lettres": 0.9575087895529885,
reports/atomes-prediction.json:11709:    "disc_connecteurs_1000": 24.623803009575923,
reports/atomes-prediction-mesures.json:904:    "graph_lettres": 0.9575087895529885,
reports/atomes-prediction-mesures.json:3244:    "disc_connecteurs_1000": 24.623803009575923,
reports/panini-334.json:1623:    "d_lex_meme_tradition": 0.21665315019575399,
reports/panini-334.json:8471:    "chance_meme_tradition": 0.22299406020336254,
reports/pensee-bilan-nuit.json:5:  "tagger_612": 0.9575,
reports/pensee-classement-appris.json:5280:     "score": -4.222998
reports/pensee-tagger-option.json:175:  "pos_612": 0.9575,
reports/pensee-tagger-option.json:179:   "tokens": 22299,
reports/r44-reel.json:138:   "rappel": 0.9575,
reports/rapport-coordination-r.json:86:    "pos_seul": "environ la moitié : ~609 appels, ~180 k tokens, ~10,5 min",
reports/rapport-exemples-tagger.json:114:    "pos_tagger": 0.9575,
reports/restitution-udhr.json:4124:  "bits_octet": 2.1354692032019575,
reports/retrieval-familles.json:20762:     "ap_famille": 0.009179255029575357,
reports/retrieval-familles.json:20779:     "ap_famille": 0.009179255029575357,
rep
… [1222 caractères tronqués]
  ```

- **bash** `{"command": "ls pyproject.toml setup.py setup.cfg requirements*.txt 2>/dev/null || true; python3 --version; grep -rn \"python_requires\\|requires-python\\|3\\.10\" README.md tools/ 2>/dev/null | head -10", "description": "Check packaging and Python version requirements"}`

  ```
Python 3.13.16
tools/docwatch/.github/workflows/ci.yml:14:        python-version: ["3.9", "3.10", "3.11", "3.12", "3.13"]
tools/docwatch/pyproject.toml:10:requires-python = ">=3.9"
tools/docwatch/pyproject.toml:23:    "Programming Language :: Python :: 3.10",
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_internal/build_env/venv.py:85:        # These attributes seem to exist in every CPython version after 3.10.1 and
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_internal/cli/cmdoptions.py:1099:    "--ignore-requires-python",
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_internal/cli/main.py:78:    # TODO: Re-evaluate whether this is still needed once pip drops Python 3.10.
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_internal/cli/req_command.py:408:            script_requires_python = script_metadata.get("requires-python", "")
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_internal/index/package_finder.py:151:            "data-requires-python" attribute.
tools/docwatch/.venv/lib/python3.13/site-packages/pip/_internal/index/package_finder.py:155:            PEP 503 "data-requires-python" values in HTML links. Defaults
tools/docwatch/.venv/l
… [148 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"sortie\\|stdin\\|entrée standard\\|pip install\\|drave\" README.md | head -30; sed -n '1,60p' README.md", "description": "Read repo README install section"}`

  ```
13:*« Stream of logs » : le flux des listes. Et « la drave » — ces billots qu'on confiait à la rivière au printemps,
22:python3 tools/drave.py analyser "Le chat de la voisine qui dort sur le toit se réveille."
23:python3 tools/drave.py analyser "The cat that sleeps on the roof is black." --langue en --json
24:python3 tools/drave.py evaluer        # la mesure sur le gold (POS, F1, attachement)
25:python3 tools/drave.py rejouer "Le chat dort."   # vérifie le déterminisme (sha256)
30:**format est versionné** (`schema: "drave.annotation"`, `version: 1`, schéma publié dans
134:1. **L'entrée-sortie linguistique** — lire et produire toutes les langues, dans tous les registres. On la juge en
151:On lui fait traduire le texte, puis on compare sa sortie à la traduction humaine **caractère par caractère** — une
269:| le **moteur d'inférence** (Rust) | [`drave-core/`](drave-core/) |
278:d'architecture (étage 1 entrée-sortie, étage 2 pensée) ; une **unité de sens** est un élément de la représentation
# Drave

> **Ce que ce document est.** La vitrine publique de Drave : la vision, les cinq axes, les deux
> étages, six résultats et l'état du dépôt. Les chiffres sont cités comme état ; les fiches 
… [3541 caractères tronqués]
  ```

- **bash** `{"command": "command -v python3.10 python3.11 python3.12 python3.13 || true; ls /usr/bin/python3.* 2>/dev/null | head", "description": "Check available Python versions"}`

  ```
/usr/bin/python3.13
/usr/bin/python3.13
/usr/bin/python3.13-config
/usr/bin/python3.14
  ```

- **bash** `{"command": "grep -n \"from __future__\\| | None\\|list\\[\" tools/drave.py tools/bloc_linguistique.py | head -10", "description": "Check Python 3.10 syntax usage"}`

  ```
tools/drave.py:32:from __future__ import annotations
tools/drave.py:168:    def analyser(self, texte: str, langue: str | None = None,
tools/drave.py:169:                 contexte: str | None = None) -> bl.Annotation:
tools/drave.py:233:def _envelopper(prefixe: str, contenu: str, largeur: int = LARGEUR) -> list[str]:
tools/drave.py:249:                        stats: dict | None = None) -> str:
tools/drave.py:291:        par_span: dict[tuple[int, int], list[bl.Etiquette]] = {}
tools/drave.py:335:                    stats: dict | None = None) -> int:
tools/drave.py:420:def _cibles_gold(phrases: list[dict]) -> list[str]:
tools/drave.py:424:def _controle_hasard(phrases: list[dict]) -> float:
tools/drave.py:924:def main(argv: list[str] | None = None) -> int:
[stderr]
grep: write error: Broken pipe
  ```

- **bash** `{"command": "grep -rn \"match \\|case \\|tomllib\\|removeprefix\\|removesuffix\\|isinstance(.*|\" tools/drave.py tools/bloc_linguistique.py tools/restitution.py tools/restitution_v2.py | head -20", "description": "Search version-specific constructs"}`

  ```
(no output)
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport ast, pathlib\nfor f in ['tools/drave.py','tools/bloc_linguistique.py','tools/restitution.py','tools/restitution_v2.py']:\n    try:\n        ast.parse(pathlib.Path(f).read_text(), feature_version=(3,10)); print(f,'parse 3.10 OK')\n    except SyntaxError as e: pri … [82 caractères tronqués]`

  ```
tools/drave.py parse 3.10 OK
tools/bloc_linguistique.py parse 3.10 OK
tools/restitution.py parse 3.10 OK
tools/restitution_v2.py parse 3.10 OK
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport ast, pathlib\nfor v in [(3,9),(3,10)]:\n  for f in ['tools/drave.py','tools/bloc_linguistique.py','tools/restitution.py','tools/restitution_v2.py']:\n    try: ast.parse(pathlib.Path(f).read_text(), feature_version=v); ok='OK'\n    except SyntaxError as e: ok=f'F … [83 caractères tronqués]`

  ```
(3, 9) tools/drave.py OK
(3, 9) tools/bloc_linguistique.py OK
(3, 9) tools/restitution.py OK
(3, 9) tools/restitution_v2.py OK
(3, 10) tools/drave.py OK
(3, 10) tools/bloc_linguistique.py OK
(3, 10) tools/restitution.py OK
(3, 10) tools/restitution_v2.py OK
  ```

- **bash** `{"command": "sed -n '920,980p' tools/drave.py", "description": "Read CLI main"}`

  ```
restituer.set_defaults(fonction=cmd_restituer)
    return parseur


def main(argv: list[str] | None = None) -> int:
    # un stdout non-UTF-8 ne doit pas faire planter l'en-tête (« — ») : on tolère les remplacements
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
    args = construire_parseur().parse_args(argv)
    try:
        return args.fonction(args)
    except BrokenPipeError:
        # `drave analyser ... | head` : le lecteur a fermé la sortie, ce n'est pas une erreur.
        return 0
    except KeyboardInterrupt:
        print(f"{NOM}: interrompu", file=sys.stderr)
        return 1
    except Exception as exc:  # noqa: BLE001 — le point d'entrée rend un code, pas une trace
        print(f"{NOM}: erreur : {type(exc).__name__} : {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
  ```

- **bash** `{"command": "python3 - <<'PY' 2>/tmp/faq-net.err\nimport socket, sys, runpy\ndef deny(*a, **k):\n    raise AssertionError(\"socket ouverte\")\nsocket.socket = deny\nsocket.create_connection = deny\nsys.argv = ['drave.py', 'analyser', 'Le chat dort.', '--json']\ntry:\n    runpy.run_path('tools/drave. … [183 caractères tronqués]`

  ```
exit=1
Traceback (most recent call last):
  File "<stdin>", line 8, in <module>
  File "<frozen runpy>", line 294, in run_path
  File "<frozen runpy>", line 98, in _run_module_code
  File "<frozen runpy>", line 88, in _run_code
  File "tools/drave.py", line 52, in <module>
    import bloc_linguistique as bl  # noqa: E402  (import après l'installation des chemins)
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/bloc_linguistique.py", line 45, in <module>
    import urllib.request
  File "/usr/lib64/python3.13/urllib/request.py", line 88, in <module>
    import http.client
  File "/usr/lib64/python3.13/http/client.py", line 1498, in <module>
    import ssl
  File "/usr/lib64/python3.13/ssl.py", line 996, in <module>
    class SSLSocket(socket):
    ...<454 lines>...
                return None
TypeError: function() argument 'code' must be code, not str
  ```

- **bash** `{"command": "python3 - <<'PY' >/tmp/faq-net.out 2>/tmp/faq-net.err\nimport socket, sys\nsys.path.insert(0, 'tools')\nimport drave\ndef deny(*a, **k):\n    raise AssertionError(\"socket ouverte\")\nsocket.socket = deny\nsocket.create_connection = deny\nrc = drave.main(['analyser', 'Le chat dort.', '- … [215 caractères tronqués]`

  ```
exit=0
 },
 "contexte": ""
}
RC 0
MODULE_RESEAU False
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nfor f in ['tools/tests/linguistique/gold.json']:\n    d=json.load(open(f))\n    print(type(d), list(d)[:5] if isinstance(d,dict) else len(d))\n    phrases=d.get('phrases') if isinstance(d,dict) else d\n    for p in phrases:\n        if p.get('id')=='g017': … [110 caractères tronqués]`

  ```
<class 'dict'> ['version', 'phrases', 'note']
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
  },
  {
   "type": "SUB",
   "texte": "that she would come",
   "role": "contenu",
   "debut": 9,
   "fin": 28,
   "cibles": [
    "said"
   ],
   "cible": "said"
  }
 ],
 "pragma": {
  "acte": "assertion",
  "modalite": true
 }
}
  ```

- **bash** `{"command": "grep -n \"g017\" reports/rapport-audit-v10.md reports/rapport-s065.md reports/rapport-r035.md 2>/dev/null | head -20", "description": "Locate g017 evidence"}`

  ```
reports/rapport-audit-v10.md:52:`g017`). Ce changement a ensuite été **committé** dans `653a7981` (2026-11-06 00:28:42,
reports/rapport-audit-v10.md:59:(9 REL, 5 SUB, 4 GP), dev 152/152, test 69/69** (il répare `s037` et `r303`, perd `g017`,
reports/rapport-audit-v10.md:139:  **+10** sur 212 = **222** ; le mesuré est **8 gains bruts** (6 REL + `r280` + `g017`) et
reports/rapport-audit-v10.md:141:- **`predicat_vu` n'est pas un gain net** : il rouvre `g017` mais **ferme `r303`**
reports/rapport-audit-v10.md:165:- **Garde PRON** — gains : `g017 r034 r074 r114 r205 r219 r240 r243 r247 r278 r280 r285
reports/rapport-audit-v10.md:170:- **`predicat_vu`** — gain : `g017` (dev) ; **perte : `r303`** (dev).
reports/rapport-audit-v10.md:173:- **v8 → v10** — 9 gains (`g017 r273 r280 s069 s135` dev ; `r153 s032 s072 s115` test),
reports/rapport-audit-v10.md:193:- **`predicat_vu` est un échange, pas un gain** : `g017` gagné, `r303` perdu, net **0**.
reports/rapport-audit-v10.md:273:152/152, mais sa composition change : `predicat_vu` gagne `g017` et perd `r303`, tous deux
reports/rapport-audit-v10.md:318:3. **Majeure — `r303` est une régression non documentée.** `predicat_vu` (v9) rouvre `g017`
re
… [1042 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,80p' reports/rapport-g017.md", "description": "Read g017 report"}`

  ```
# B13 — g017 : l'adverbe final hors de la SUB est rejeté (g017 gagné, r264 et r288 perdus)

> **Instantané historique** — les chiffres publiés ici sont ceux du commit de la fiche ; ils ne
> décrivent pas l'état courant. L'état courant du bloc est dans
> [`en-cours`](../docs/pilotage/en-cours.md) et [`la roadmap`](../docs/pilotage/roadmap.md).

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Tâche** : J6.1 · **Date** : 2026-11-14 ·
> **Verdict** : ❌ **règle rejetée**.
> La règle demandée — **l'adverbe final de temps hors de la SUB** — corrige bien `g017`
> (`that she would come` au lieu de `that she would come yesterday`) et retire un faux positif
> de `g005`, mais elle **casse `r264`** (`qu'il vient demain`) et **`r288`**
> (`that he comes tomorrow`) : **F1 0,7902 → 0,7901 (−0,0001)**, **dev +0,0011**, **test
> −0,0028**, **attachement 237/238 → 236/237**, **couverture 0,9958 → 0,9916**. Les deux cas
> favorables sont en **dev**, les deux cas défavorables en **test** : le gain est in-sample, la
> perte est hors échantillon. **Aucun code de production n'est modifié** ; la porte du bloc
> reste verte, et l'état reste à **237/238**.
>
> **Dispositif** : [`bloc_linguistique.py`
… [2933 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/drave.py evaluer --reel | tail -12", "description": "Run real-base evaluation"}`

  ```
gold réel (hand + reel, sans synthétique) · 452 phrases · 2480 tokens · 184 cibles d'attachement

POS         exactitude 88.91 %  (fermé 92.94 %, ouvert 84.66 %)
SYNTAGMES   F1 79.06 %  (P 81.28 % / R 76.95 %)
  tête      F1 89.90 %  (P 93.84 % / R 86.28 %)
  vue linéaire (partition filtrer) F1 79.53 %  · attachement 91.85 % de couverture
BASE RÉELLE — (déjà la base, ou gold gelé)
ATTACHEMENT exact 99.46 % · couverture 99.46 % · exact sur span 100.00 % · top-k 98.91 %
  tête      couverture 100.00 % · top-k 99.45 %
PRAGMATIQUE acte 99.56 % · négation 96.90 % · modalité 98.45 % · double sens 96.46 %
FRACTION SÉMANTIQUE 50.82 %
CONTRÔLE NÉGATIF cible exacte tirée au hasard 0.00 % (graine 0, 184 cibles)
  ```

- **bash** `{"command": "python3 tools/drave.py evaluer --reel --json 2>/dev/null | python3 -c \"import json,sys; d=json.load(sys.stdin); print(json.dumps(d.get('attachement',d),ensure_ascii=False,indent=1)[:1500])\"", "description": "Inspect real-base attachment JSON"}`

  ```
{
 "version": "0.1.0",
 "gold": {
  "nom": "réel (hand + reel, sans synthétique)",
  "gele": false,
  "phrases": 452,
  "tokens": 2480,
  "cibles_attachement": 184
 },
 "heuristique": {
  "bloc": "heuristique",
  "phrases": 452,
  "pos": {
   "exactitude": 0.8891,
   "exactitude_ferme": 0.9294,
   "exactitude_ouvert": 0.8466,
   "tokens": 2480,
   "confusions": {
    "ADJ": {
     "ADJ": 65,
     "NOUN": 11,
     "VERB": 4
    },
    "ADV": {
     "ADV": 89,
     "NOUN": 7,
     "PREP": 1,
     "ADJ": 1,
     "?": 1
    },
    "AUX": {
     "PREP": 4,
     "AUX": 116,
     "?": 3,
     "NOUN": 1,
     "VERB": 1
    },
    "CONJ": {
     "PRON": 8,
     "CONJ": 60,
     "?": 13,
     "PREP": 2
    },
    "DET": {
     "DET": 441,
     "?": 2
    },
    "NOUN": {
     "NOUN": 502,
     "ADJ": 11,
     "VERB": 5,
     "?": 1
    },
    "NUM": {
     "NUM": 2
    },
    "PONCT": {
     "PONCT": 25
    },
    "PREP": {
     "PREP": 90
    },
    "PRON": {
     "PRON": 386,
     "?": 30,
     "CONJ": 2,
     "DET": 14
    },
    "VERB": {
     "VERB": 429,
     "NOUN": 125,
     "PREP": 2,
     "ADJ": 2,
     "?": 16,
     "AUX": 7,
     "ADV": 1
    }
   }
  },
  "syntagme": {
   "preci
… [300 caractères tronqués]
  ```

- **bash** `{"command": "for t in \"Der Hund schläft.\" \"El perro duerme.\" \"Il cane dorme.\" \"Le chien dort.\" \"The dog sleeps.\"; do printf '%s -> ' \"$t\"; python3 tools/drave.py analyser \"$t\" --json 2>/dev/null | python3 -c \"import json,sys; d=json.load(sys.stdin); print(d['langue'],d['script'],round … [131 caractères tronqués]`

  ```
Der Hund schläft. -> de Latn 0.99
El perro duerme. -> es Latn 0.99
Il cane dorme. -> fr Latn 0.99
Le chien dort. -> fr Latn 0.99
The dog sleeps. -> en Latn 0.99
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys\nsys.path.insert(0,'tools')\nimport bloc_linguistique as bl\nfor t in [\"Der Hund schläft.\",\"El perro duerme.\",\"Il cane dorme.\",\"Élodie sourit.\",\"Le chien dort.\",\"The dog sleeps.\"]:\n    a=bl.Heuristique().analyser(t)\n    print(repr(t),'->',a.lan … [86 caractères tronqués]`

  ```
'Der Hund schläft.' -> de Latn
'El perro duerme.' -> es Latn
'Il cane dorme.' -> fr Latn
'Élodie sourit.' -> und Latn
'Le chien dort.' -> fr Latn
'The dog sleeps.' -> en Latn
  ```

- **bash** `{"command": "grep -n \"cle\\|api_key\\|Authorization\\|print\\|log\" tools/llm/deepseek.py | head -40; sed -n '1,60p' tools/llm/deepseek.py", "description": "Inspect DeepSeek client key handling"}`

  ```
73:def _cle_env() -> str:
96:def _cache_cle(modele: str, messages: list[dict], temperature: float,
127:    def __init__(self, cle: str | None = None, base_url: str | None = None,
131:        self.cle = cle if cle is not None else _cle_env()
146:        return bool(self.cle)
151:    def _lire_cache(self, cle: str) -> ReponseDeepSeek | None:
152:        chemin = self.cache_dir / f"{cle}.json"
166:    def _ecrire_cache(self, cle: str, r: ReponseDeepSeek) -> None:
169:            (self.cache_dir / f"{cle}.json").write_text(json.dumps({
196:        if not self.cle:
200:        cle = _cache_cle(self.modele, messages, temperature, max_tokens)
202:            deja = self._lire_cache(cle)
208:        entetes = {"Authorization": f"Bearer {self.cle}",
227:                    self._ecrire_cache(cle, r)
259:        print(f"ERREUR : {e}", file=sys.stderr)
262:        print(json.dumps({"contenu": r.contenu, "raisonnement": r.raisonnement,
267:        print(r.contenu)
#!/usr/bin/env python3
"""deepseek.py — le professeur externe, sans poids locaux.

POURQUOI CE MODULE. Le dépôt garde ses GPU et ses CPU pour le **modèle natif**
Drave (`entrainer_moteur.py`, `drave-core`) et pour les mesures **boîte
… [2030 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"cache\" tools/llm/deepseek.py | head -30", "description": "Inspect client cache behavior"}`

  ```
14:dans le dépôt, dans un cache ou dans un message d'erreur. Il ne dépend d'aucun
21:- cache : `data/deepseek/cache/<sha256>.json` (gitignoré), clé = modèle + messages
44:CACHE_DEFAUT = RACINE / "data" / "deepseek" / "cache"
66:    cache: bool = False
96:def _cache_cle(modele: str, messages: list[dict], temperature: float,
128:                 modele: str | None = None, cache_dir: str | pathlib.Path | None = None,
137:        self.cache_dir = pathlib.Path(cache_dir or os.environ.get("DEEPSEEK_CACHE")
151:    def _lire_cache(self, cle: str) -> ReponseDeepSeek | None:
152:        chemin = self.cache_dir / f"{cle}.json"
164:                               cache=True, brut=d.get("brut"))
166:    def _ecrire_cache(self, cle: str, r: ReponseDeepSeek) -> None:
168:            self.cache_dir.mkdir(parents=True, exist_ok=True)
169:            (self.cache_dir / f"{cle}.json").write_text(json.dumps({
176:            # un cache indisponible ne doit pas faire échouer une mesure
183:                cache: bool = True) -> ReponseDeepSeek:
195:                modele=self.modele, usage={}, latence_s=0.0, cache=False)
200:        cle = _cache_cle(self.modele, messages, temperature, max_tokens)
201:  
… [405 caractères tronqués]
  ```

- **bash** `{"command": "python3 -S tools/drave.py analyser \"Le chat dort.\" --json >/tmp/faq-S.json 2>/tmp/faq-S.err; echo exit=$?; head -3 /tmp/faq-S.err; python3 -c \"import json;d=json.load(open('/tmp/faq-S.json'));print(d['langue'],len(d['etiquettes']))\" 2>&1", "description": "Run CLI without site packag … [4 caractères tronqués]`

  ```
exit=0
fr 20
  ```

- **bash** `{"command": "ls -1 tools/tests/linguistique/gold*.json; python3 - <<'PY'\nimport json, pathlib\nfor p in sorted(pathlib.Path('tools/tests/linguistique').glob('gold*.json')):\n    try:\n        d=json.loads(p.read_text())\n        n=len(d.get('phrases', d)) if isinstance(d,dict) else len(d)\n    exce … [93 caractères tronqués]`

  ```
tools/tests/linguistique/gold_gele.json
tools/tests/linguistique/gold.json
tools/tests/linguistique/gold_reel.json
tools/tests/linguistique/gold_restitution_v2.json
tools/tests/linguistique/gold_synthetique.json
tools/tests/linguistique/gold.json 20
tools/tests/linguistique/gold_gele.json 602
tools/tests/linguistique/gold_reel.json 432
tools/tests/linguistique/gold_restitution_v2.json 7
tools/tests/linguistique/gold_synthetique.json 160
  ```

- **bash** `{"command": "grep -rn \"produit/README.md#\\|§ 8\\|#8\" docs README.md reports 2>/dev/null | head -20", "description": "Check references to product section 8"}`

  ```
docs/archive/modele-pour-drave.md:30:| découpage à deux nœuds : **3,4 ms par jeton et par ms de RTT** (§ 8 bis) | le transport est exact à toute latence (perplexité inchangée à 50 ms) | répartir ne paie que si le calcul local dépasse 3,4 ms × RTT : **la taille du modèle décide**, pas le réseau |
docs/schemas/pipeline.mmd.svg:2:<svg id="my-svg" width="100%" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" class="flowchart" style="max-width: 1259.11px; background-color: white;" viewBox="4 4 1259.109375 208.7083282470703" role="graphics-document document" aria-roledescription="flowchart-v2"><title>Diagramme Mermaid</title><desc>Généré par Mermaid</desc><style>#my-svg{font-family:"Recursive Variable",arial,sans-serif;font-size:14px;fill:#28253D;}@keyframes edge-animation-frame{from{stroke-dashoffset:0;}}@keyframes dash{to{stroke-dashoffset:0;}}#my-svg .edge-animation-slow{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 50s linear infinite;stroke-linecap:round;}#my-svg .edge-animation-fast{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 20s linear infinite;stroke-linecap:round;}#my-svg .error-icon{fill:#ffffff;}#my-svg
… [25981 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"docs/produit/README\" docs README.md reports journal AGENTS.md 2>/dev/null | head -20", "description": "Check product README links"}`

  ```
docs/pilotage/roadmap.md:91:[`docs/produit/README.md`](../produit/README.md) § 3.3 bis documente les **quatre** champs de
README.md:32:complète est [`docs/produit/README.md`](docs/produit/README.md), les exemples vérifiés
reports/rapport-evaluer-langue.md:98:2. **J11.4** — documenter le schéma v2 (rétro-compatibilité v1) dans `docs/produit/README.md`.
reports/rapport-evaluer-langue.md:107:- [`docs/produit/README.md`](../docs/produit/README.md) — § 3.3 et § 7 (option documentée).
reports/schema-v2-doc.json:13:  "fichier": "docs/produit/README.md",
reports/rapport-schema-v2-doc.md:10:> [`docs/produit/README.md`](../docs/produit/README.md) § 3.3 bis : les **quatre** champs de
reports/rapport-schema-v2-doc.md:24:> [`docs/produit/README.md`](../docs/produit/README.md) ; JSON
reports/rapport-schema-v2-doc.md:183:- [`docs/produit/README.md`](../docs/produit/README.md) — § 3.3 bis : les deux champs, l'exemple,
reports/rapport-tagger-option.md:176:- [`docs/produit/README.md`](../docs/produit/README.md) § 3.7 — la notice d'usage de l'option.
reports/rapport-exemples-tagger.md:148:- [`docs/produit/README.md`](../docs/produit/README.md) § 3.7 — recalé sur le code courant :
journal/sessions/e18
… [2548 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,160p' docs/methode/rangement.md", "description": "Read documentation review method"}`

  ```
# Le rangement, et la revue de documentation

> Document de tâche, chargé depuis [`AGENTS.md`](../../AGENTS.md). La règle la plus souvent violée du dépôt : à lire
> **avant de classer un fichier** ou de clore un sous-chantier.

## Les quatre dossiers (règle stricte)

| dossier | ce qu'il contient | ce qu'il ne contient **jamais** |
|---|---|---|
| **`docs/`** | quatre familles : **méthode**, **pilotage**, **théorie**, **implantation** — ce qui reste vrai quand les chiffres changent | des **résultats** de mesure, des tableaux de chiffres, des comptes rendus de round |
| **`reports/`** | les **résultats mesurés** : fiches, séries de mesures, tableaux, erratums, récits de round, JSON de résultats | la documentation de référence |
| **`journal/`** | le **récit daté** : ce qui a été fait, quand, et ce qu'on en a appris | les chiffres seuls (ils vont dans `reports/`) |
| **`data/`** | les corpus et leur généalogie (`data/udhr/`, `data/corpus_*.txt`, `data/eurlex/`) | du code |

Dans `docs/`, les quatre familles sont **séparées** : `methode/` (comment on travaille), `pilotage/` (où l'on en
est), `theorie/` (ce qui reste vrai), `implantation/` (comment c'est construit). Une page de `docs/`
… [4004 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,160p' tools/revue_documentation.py", "description": "Read documentation review tool"}`

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
… [4497 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"D1\\|D2\\|D3\\|jour 15\\|J15\" docs/pilotage/roadmap.md docs/pilotage/en-cours.md journal/README.md | head -40", "description": "Find D tasks in roadmap/state"}`

  ```
docs/pilotage/roadmap.md:56:D1–D20, rejets R1–R30, échecs, reste — est dans
docs/pilotage/roadmap.md:65:[`fiche`](../../reports/rapport-exemples-rejoues.md) + JSON. **D1** ajoute **3** exemples
docs/pilotage/en-cours.md:3:**Mis à jour : 2026-11-15, 05 h 30 HNE (D2)**
docs/pilotage/en-cours.md:64:- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/239 (0,9958)**, **F1 0,7902**, **1 span** ; **`s065`** et **`r035`** réglés, **convention des GV** ; **restitution v1** (46/46 canonique, strict 0,1087 ; [fiche](../../reports/rapport-restitution-v1.md)) ; **J11.1–J11.4** ([exemples](../../reports/rapport-exemples-rejoues.md), [par-langue](../../reports/rapport-evaluer-langue.md), [robustesse](../../reports/rapport-robustesse-semaine.md), [schéma](../../reports/rapport-schema-v2-doc.md)) ; **D1** ([fiche](../../reports/rapport-exemples-tagger.md)).
docs/pilotage/en-cours.md:90:- **Pensée — B13 (actif)** : **183/183** ; `r035` (238/238), convention GV (0,7902), `s065` (238/238), **J6.1 rejeté** (g017 à trancher), schéma v2, **restitution v2** **16/46** ([fiche](../../reports/rapport-restitution-v2.md)), **J9.1**, **D1** ; [s065](../../reports/rapport-s065.md), [J9.1](../../rep
… [33 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,140p' tools/verifie_etat_a_jour.py", "description": "Read state freshness checker"}`

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
… [4239 caractères tronqués]
  ```

- **bash** `{"command": "git status --porcelain=v1 | sed -n '1,80p'; echo ===; git diff --stat -- tools/drave.py tools/porte-produit.sh tools/restitution_v2.py 2>/dev/null", "description": "Full working tree status"}`

  ```
M docs/pilotage/en-cours.md
 M docs/pilotage/roadmap.md
 M docs/produit/README.md
 M journal/2026-11-15/mesures.md
 M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
 M journal/sessions/session-e73a3601-e2c6-417c-a009-88ffadca4e61/digest.md
 M journal/sessions/session-e73a3601-e2c6-417c-a009-88ffadca4e61/rapport.md
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
 M tools/drave.py
 M tools/porte-produit.sh
?? journal/sessions/session-53896e61-4a68-417d-89e0-de0de156949b/
?? reports/pensee-restitution-v2.json
?? reports/rapport-gold-reel-50.json
?? reports/rapport-gold-reel-50.md
?? reports/rapport-restitution-v2.md
?? reports/rapport-s-paragraphes.md
?? tools/mesurer_restitution_v2.py
?? tools/restitution_v2.py
?? tools/tests/linguistique/go
… [286 caractères tronqués]
  ```

- **bash** `{"command": "git diff -- tools/drave.py | head -120", "description": "Inspect drave.py D2 diff"}`

  ```
diff --git a/tools/drave.py b/tools/drave.py
index 8e037dc4..25f0a204 100644
--- a/tools/drave.py
+++ b/tools/drave.py
@@ -11,13 +11,15 @@ Une seule commande, quatre gestes, hors ligne et déterministe :
     python3 tools/drave.py evaluer --tagger --json                    # heuristique + cascade API
     python3 tools/drave.py rejouer "Le chat de la voisine qui dort sur le toit se réveille."
     python3 tools/drave.py restituer "Le chat dort."
+    python3 tools/drave.py restituer "Le chat dort." --roles
     python3 tools/drave.py restituer --banc reports/pensee-fiabilite-produit.json --json
     python3 tools/drave.py --version
 
 Ce que la commande expose : l'analyse **heuristique** (`Heuristique.analyser`) — POS, syntagmes
 avec rôle et cible d'attachement, pragmatique, unités sémantiques —, sa mesure sur le gold et la
-**restitution v0** (annotation → surface, avec la fidélité du miroir). La restitution est un
-**codec de surface** : elle reconstruit depuis le niveau `graphème`, pas un décodeur neuronal.
+**restitution v0** (annotation → surface, avec la fidélité du miroir) et la **v2** (rôles
+agent/prédicat/lieu lisibles). La restitution est un **codec de surface** : elle 
… [5700 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"rapport-gold-reel-50\\|rapport-s-paragraphes\\|gold_reel_50\" docs/pilotage/en-cours.md docs/pilotage/roadmap.md reports/README.md journal/2026-11-15/mesures.md 2>/dev/null | head -20", "description": "Check references to other untracked work"}`

  ```
reports/README.md:19:| [`rapport-gold-reel-50.md`](rapport-gold-reel-50.md) | **R0.7** — le gold réel : 452 phrases, 50 ratées, le « 200+ » obsolète |
  ```

- **bash** `{"command": "git diff --stat -- reports/ | cat; echo ===; git log -1 --format='%h %ad %s' --date=iso", "description": "Check modified report files"}`

  ```
reports/INDEX.md                        |   3 +-
 reports/README.md                       |   1 +
 reports/pensee-coherence-fiches-v7.json |  19 +
 reports/pensee-dev-test-v10.json        |   2 +-
 reports/pensee-quatre-modes.json        | 734 ++++++++++++++++++--------------
 reports/rapport-audit-v7.md             |   6 +-
 reports/rapport-coherence-fiches-v7.md  |  17 +-
 reports/rapport-dev-test-v10.md         |   2 +-
 reports/rapport-pensee-v12.md           |   4 +-
 reports/rapport-spans-chunker.md        |  13 +-
 10 files changed, 463 insertions(+), 338 deletions(-)
===
e42bac4f 2026-11-15 04:48:44 -0500 JOURNAL — 2026-11-15 : D1, LES EXEMPLES --tagger (441 TOKENS, 3,7 S) ET --reel (452 PHRASES) SONT DANS LA DOC ; 5/5 REJOUÉS, MUTATION 4/5
  ```

- **bash** `{"command": "git diff -- reports/pensee-quatre-modes.json | head -40; echo ===; git diff -- reports/pensee-dev-test-v10.json | head -20; echo ===; git diff -- reports/rapport-audit-v7.md | head -40", "description": "Inspect unrelated report diffs"}`

  ```
diff --git a/reports/pensee-quatre-modes.json b/reports/pensee-quatre-modes.json
index 555c0a45..436f1eba 100644
--- a/reports/pensee-quatre-modes.json
+++ b/reports/pensee-quatre-modes.json
@@ -1,115 +1,66 @@
 {
-  "date": "2026-11-03 16:57 EST",
+  "date": "2026-11-04 10:37 EST",
   "gold": {
-    "phrases": 432,
-    "tokens": 2375,
+    "phrases": 3,
+    "tokens": 14,
     "modalite": "api-deepseek (deepseek-chat), aucun serveur local"
   },
   "modes": {
     "heuristique": {
       "all": {
         "pos": {
-          "exactitude": 0.7394,
-          "exactitude_ferme": 0.885,
-          "exactitude_ouvert": 0.5864,
-          "tokens": 2375,
+          "exactitude": 0.8571,
+          "exactitude_ferme": 1.0,
+          "exactitude_ouvert": 0.75,
+          "tokens": 14,
           "confusions": {
-            "ADJ": {
-              "NOUN": 26,
-              "ADJ": 47,
-              "VERB": 4
-            },
-            "ADV": {
-              "ADV": 69,
-              "NOUN": 21,
-              "PREP": 1,
-              "ADJ": 1,
-              "?": 1
-            },
===
diff --git a/reports/pensee-dev-test-v10.json b/reports/pensee-dev-test-v10.json
index 29223569..f
… [2773 caractères tronqués]
  ```

- **bash** `{"command": "git diff -- journal/2026-11-15/mesures.md | head -80; echo ===; sed -n '1,120p' journal/2026-11-15/mesures.md", "description": "Read day journal and diff"}`

  ```
diff --git a/journal/2026-11-15/mesures.md b/journal/2026-11-15/mesures.md
index 44e2a5aa..c0617f10 100644
--- a/journal/2026-11-15/mesures.md
+++ b/journal/2026-11-15/mesures.md
@@ -39,4 +39,19 @@
 
 <!-- notes -->
 
+### D2 — la restitution v2 : les rôles se lisent, leur fidélité ne suit pas
+
+La v2 devait passer de la surface (v0) et de la forme canonique (v1) aux **rôles**. Elle le fait
+comme **forme** : `restituer --roles` rend un cadre `agent / prédicat / lieu`, 198 segments de rôle,
+**198/198** spans dans la source, et `relire_roles(rendre_roles(a))` redonne le cadre **46/46**.
+Mais la **fidélité** ne suit pas. Sur un or écrit à la main (46 cadres, 65 variantes), **19/46**
+cadres sont exacts — **16/46** non vides —, **91/138** cellules exactes, mais **F1 0,5270**
+(précision 0,5493, rappel 0,5065, **32 faux positifs / 38 faux négatifs**) ; **agent 0,6000**,
+**prédicat 0,4872**, **lieu 0,4000**. Les planchers : vide **7/46**, constant par type **6/46**,
+rôles mélangés **3/46**. Le contrôle externe (gold S, 61 phrases) vaut **139/144 = 0,9653** :
+l'instrument n'est pas cassé ; c'est la lecture des rôles de l'annotation qui ne tient pas.
+`f03` lit `Comment / Bonjour`, 
… [4724 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '160,360p' tools/revue_documentation.py", "description": "Read remaining documentation review checks"}`

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
… [8348 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport pathlib\nprint('md',len(list(pathlib.Path('reports').glob('*.md'))))\nprint('json',len(list(pathlib.Path('reports').glob('*.json'))))\nprint('docs',len([p for p in pathlib.Path('docs').rglob('*.md') if 'archive' not in p.parts and p.name!='README.md' and not (p. … [182 caractères tronqués]`

  ```
md 744
json 838
docs 123
portes 85
  ```

- **bash** `{"command": "python3 tools/drave.py analyser \"Le livre que j'ai lu est intéressant.\" --json 2>/dev/null | python3 -c \"\nimport json,sys\nd=json.load(sys.stdin)\nfor e in d['etiquettes']:\n    if e['niveau']=='syntagme':\n        print(e['type'],e.get('meta',{}).get('role'),e.get('meta',{}).get('a … [154 caractères tronqués]`

  ```
GN agent {'segment': 'Le livre', 'cible': 'intéressant'} NoneType
REL qualite {'segment': "que j'ai lu", 'cible': 'livre'} NoneType
REL qualité {'segment': "que j'ai lu est intéressant", 'cible': 'livre'} NoneType
GV predicat {'segment': 'est intéressant', 'cible': 'livre'} NoneType
  ```

- **bash** `{"command": "grep -n \"http.server\\|--sortie\\|sys.stdin\\|def _lire_entree\" tools/drave.py | head; sed -n '315,334p' tools/drave.py", "description": "Check absent CLI features"}`

  ```
327:def _lire_entree(args: argparse.Namespace) -> str:
            + " · ".join(f"{n}={couverture[n]:.2f}" for n in ordre),
        ))
    if tagger and a.refus:
        lignes.extend(_envelopper("REFUS TAGGER  ", a.refus))
    if stats is not None:
        lignes.extend(_envelopper("TAGGER API  ", _ligne_tagger(stats)))
    return "\n".join(lignes)


# --------------------------------------------------------------------------- commandes


def _lire_entree(args: argparse.Namespace) -> str:
    """Le texte : l'argument, ou le **fichier** (`--fichier`)."""
    if getattr(args, "fichier", None):
        return pathlib.Path(args.fichier).read_text(encoding="utf-8", errors="replace")
    return args.texte or ""


def _analyser_jsonl(texte: str, args: argparse.Namespace, h: bl.Heuristique, bloc,
  ```

- **bash** `{"command": "python3 tools/drave.py analyser \"Le livre que j'ai lu est intéressant.\" --json 2>/dev/null | python3 -c \"\nimport json,sys\nd=json.load(sys.stdin)\nfor e in d['etiquettes']:\n    if e['niveau']=='syntagme':\n        print(json.dumps(e,ensure_ascii=False,indent=1)[:900]); break\n\"",  … [45 caractères tronqués]`

  ```
{
 "niveau": "syntagme",
 "type": "GN",
 "valeur": "Le livre",
 "debut": 0,
 "fin": 8,
 "source": "heuristique",
 "confiance": 0.55,
 "candidats": [
  "« que j'ai lu » → Le livre",
  "intéressant",
  "livre"
 ],
 "langue": "fr",
 "script": "Latn",
 "meta": {
  "role": "agent",
  "niveau": 1,
  "attachement": {
   "segment": "Le livre",
   "cible": "intéressant"
  }
 }
}
  ```

- **bash** `{"command": "python3 tools/drave.py analyser \"She said that she would come yesterday.\" --json 2>/dev/null | python3 -c \"\nimport json,sys\nd=json.load(sys.stdin)\nfor e in d['etiquettes']:\n    if e['niveau']=='syntagme':\n        print(e['type'],e['debut'],e['fin'],repr(e['valeur']),e.get('meta' … [75 caractères tronqués]`

  ```
GN 0 3 'She' {'segment': 'She', 'cible': 'said'}
GV 4 8 'said' None
SUB 9 38 'that she would come yesterday' {'segment': 'that she would come yesterday', 'cible': 'said'}
  ```

- **bash** `{"command": "python3 -c \"import json; d=json.load(open('reports/pensee-g017.json')); print(json.dumps(d,ensure_ascii=False,indent=1)[:2500])\"", "description": "Inspect g017 JSON evidence"}`

  ```
{
 "date": "2026-11-14",
 "ligne": "B13",
 "tache": "J6.1",
 "objet": "g017 — la règle de l'adverbe final de temps hors de la SUB est mesurée puis rejetée",
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
 "dispositif": {
  "gold": "tools/tests/linguistique/evaluer_gold.py::charger (612 phrases, 239 cibles)",
  "split": "tools/tests/linguistique/gold_split.py (crc32(id) % 3)",
  "module_base": "tools/bloc_linguistique.py (lecture seule, non modifié)",
  "copies": {
   "regle": "/tmp/g017/bloc_g017.py",
   "adv_large": "/tmp/g017/bloc_adv_large.py",
   "garde": "/tmp/g017/bloc_garde.py",
   "placebo": "/tmp/g017/bloc_placebo.py"
  },
  "note_copie": "chaque copie remplace RACINE par le dépôt, sinon generateur.py (le générateur S) n
… [1300 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/verifier_schema_produit.py --gold 20 --json >/tmp/faq-schema20.json 2>/dev/null; echo exit=$?; python3 -c \"\nimport json;d=json.load(open('/tmp/faq-schema20.json'));print(len(d['cas']),sum(c['ok'] for c in d['cas']),d['versions_lues'],d['retrocompatibilite'])\"", "descrip … [50 caractères tronqués]`

  ```
exit=0
26 26 [1, 2] {'v1_lue': True, 'v2_refuse_v1': True}
  ```

- **bash** `{"command": "python3 tools/drave.py restituer --banc reports/pensee-fiabilite-produit.json --canonique --json > /tmp/faq-rest-v1.json 2>/dev/null; echo exit=$?; python3 -c \"\nimport json;d=json.load(open('/tmp/faq-rest-v1.json'));print(json.dumps(d['synthese'],ensure_ascii=False,indent=1))\"", "des … [45 caractères tronqués]`

  ```
exit=0
{
 "n": 50,
 "annotations": 46,
 "refus": 4,
 "refus_ids": [
  "f14",
  "f15",
  "f16",
  "f17"
 ],
 "strict": {
  "exacts": 5,
  "fidelite": 0.1087
 },
 "canonique": {
  "exacts": 46,
  "fidelite": 1.0,
  "fidelite_caractere": 1.0
 },
 "strict_sur_canonique": {
  "exacts": 1,
  "fidelite": 0.0217,
  "fidelite_caractere": 0.8566
 },
 "structure": {
  "segments": 395,
  "segments_avec_role": 395,
  "attachements": 315,
  "cibles_resolues": 315,
  "cibles_dans_un_segment": 313,
  "couverture_caracteres": 0.7519,
  "couverture_jetons": 0.6584,
  "taux_roles": 1.0,
  "taux_cibles_resolues": 1.0,
  "taux_cibles_dans_un_segment": 0.9937
 },
 "stabilite": {
  "squelette_identique": 18,
  "jetons_identiques": 46,
  "fidelite": 0.3913
 },
 "controle_negatif_canonique": {
  "melange_exacts": 0,
  "melange_fidelite_caractere": 0.3865,
  "tronque_exacts": 0,
  "tronque_fidelite_caractere": 0.7998,
  "detectes": 46
 },
 "controle_negatif_structure": {
  "eligibles": 43,
  "detectes": 43,
  "cle_changee": 43,
  "roles_retires": 395,
  "cibles_retirees": 315
 }
}
  ```

- **bash** `{"command": "python3 -c \"import json; d=json.load(open('reports/rapport-exemples-tagger.json')); print(json.dumps(d,ensure_ascii=False,indent=1)[:2200])\" 2>/dev/null || ls reports/*exemples*tagger*", "description": "Inspect examples tagger JSON cost"}`

  ```
{
 "tache": "D1",
 "titre": "Les exemples avec le tagger et la base réelle",
 "date": "2026-11-15",
 "head": "ee04ea9134d8f9fab62c8728fd1ab7857ded4dd3",
 "code": {
  "cli": "drave 0.1.0",
  "schema": 2,
  "commande": "python3 tools/drave.py"
 },
 "dispositif": {
  "cle": "~/.config/drave/deepseek.key (jamais affichée)",
  "cache": "/tmp/drave-exemples-tagger-cache (neuf au premier appel)",
  "modele_demande": "deepseek-chat",
  "reseau": true,
  "date_execution": "2026-11-15",
  "note": "les trois exemples --tagger ont été lancés avec un cache disque vide ; les appels suivants du rejeu sont servis par le cache (réseau=0, tokens=0)"
 },
 "tagger": {
  "exemples": [
   {
    "id": "g001",
    "entree": "Le chat dort.",
    "langue": "fr",
    "commande": "python3 tools/drave.py analyser \"Le chat dort.\" --tagger",
    "sortie": "drave 0.1.0 — analyse cascade POS (tagger API DeepSeek, réseau)\nlangue=fr script=Latn source=cascade · 20 étiquettes · unités sémantiques=2 (61.5% du texte)\nPOS  Le/DET chat/NOUN dort/VERB ./PONCT\nSYNTAGMES\n  GN   [0:7]   Le chat  rôle=agent     → dort\n  GV   [8:12]  dort     rôle=predicat  → chat\nPRAGMATIQUE\n  phrase [0:13] déclarative · acte=asserti
… [1000 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"441\\|3,7\\|3.7\" reports/rapport-exemples-tagger.md | head", "description": "Locate examples cost in report"}`

  ```
8:> **3 appels**, **441 tokens**, **3,7 s**. Les deux `--reel` donnent **452 phrases**, POS
59:| **total** | **3** | **3** | **0** | **441** | **3,7 s** |
62:la suppression du tagger de syntagmes), **441 tokens** valent **~0,0004 $** : une **estimation**,
148:- [`docs/produit/README.md`](../docs/produit/README.md) § 3.7 — recalé sur le code courant :
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/rapport-exemples-tagger.json'))\nprint(list(d))\nfor k,v in d.items():\n    if 'cout' in k or 'total' in k: print(k, json.dumps(v,ensure_ascii=False)[:800])\nPY", "description": "Find examples total cost"}`

  ```
['tache', 'titre', 'date', 'head', 'code', 'dispositif', 'tagger', 'reel', 'verification', 'controle_negatif', 'limites', 'fichiers']
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/rapport-exemples-tagger.json'))\nprint(json.dumps(d['tagger'],ensure_ascii=False,indent=1)[-2000:])\nPY", "description": "Print tagger examples tail"}`

  ```
tools/drave.py analyser \"The day when we left was beautiful.\" --langue en --tagger",
   "sortie": "drave 0.1.0 — analyse cascade POS (tagger API DeepSeek, réseau)\nlangue=en script=Latn source=cascade · 38 étiquettes · unités sémantiques=3 (45.7% du texte)\nPOS  The/DET day/NOUN when/PRON we/PRON left/VERB was/AUX beautiful/ADJ ./PONCT\nSYNTAGMES\n  GN   [0:7]    The day        rôle=groupe nominal  → beautiful\n  REL  [8:20]   when we left   rôle=qualité         → day\n  GV   [21:34]  was beautiful  rôle=prédicat        → —\nPRAGMATIQUE\n  phrase [0:35] déclarative · acte=assertion · négation=non · modalité=non · double sens=non\nCOUVERTURE  (confiance max par niveau)  graphème=0.99 · morphème=0.32 · mot=0.98 · pos=0.95 ·\n            syntagme=0.35 · phrase=0.85 · discours=0.50 · pragmatique=0.45 · document=0.70\nTAGGER API  modèle=deepseek-chat · appels=1 · réseau=1 · cache=0 · tokens=154 · latence=1.1 s",
   "pos": "The/DET day/NOUN when/PRON we/PRON left/VERB was/AUX beautiful/ADJ ./PONCT",
   "pos_heuristique": "The/DET day/NOUN when/CONJ we/PRON left/VERB was/AUX beautiful/ADJ ./PONCT",
   "pos_gold": "The/DET day/NOUN when/PRON we/PRON left/VERB was/AUX beautiful/ADJ",
   "
… [799 caractères tronqués]
  ```

- **bash** `{"command": "ls reports/*audit*v10*; grep -n \"42.14\\|42,14\\|1.997\\|0.908\\|0,908\" reports/rapport-audit-v10.md reports/*audit*v10*.json 2>/dev/null | head -20", "description": "Locate audit v10 controls"}`

  ```
reports/pensee-audit-v10.json
reports/rapport-audit-v10.md
reports/rapport-audit-v10.md:214:| **permutation globale des cibles** (top-1) | **220/220 = 1,0** | moyenne **1,997/220 = 0,908 %** ; médiane 2 ; max 10 ; p95 5 | **0/2 000** |
reports/rapport-audit-v10.md:215:| **candidat aléatoire** (top-1) | **220/220 = 1,0** | moyenne **92,7/220 = 42,14 %** (585 candidats, 2,66/label) | **0/2 000** |
reports/rapport-audit-v10.md:221:aléatoire » est haut (42,14 %) parce que les listes de candidats contiennent presque toujours
reports/rapport-audit-v10.md:224:1,17 % de réussite ; le top-1 aléatoire, lui, vaut 42,14 %. Les deux contrôles donnent p = 0.
reports/rapport-audit-v10.md:227:(**2,04/212**, p = 0). Notre mesure (**1,997/220**, p = 0) est du même ordre et la confirme.
reports/rapport-audit-v10.md:341:    courant (220). Notre contrôle (1,997/220, p = 0) le confirme, mais la fiche ne publie
reports/rapport-audit-v10.md:370:  candidats laisse 1,17 % de réussite, le top-1 aléatoire 42,14 % ; les deux donnent p = 0.
reports/pensee-audit-v10.json:310:    "couverture": 0.908,
reports/pensee-audit-v10.json:706:    "couverture": 0.908,
reports/pensee-audit-v10.json:728:   "moyenne": 1.997,

… [528 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"candidat aléatoire\\|permutation\" reports/rapport-audit-v10.md | head -10", "description": "Read audit v10 control wording"}`

  ```
214:| **permutation globale des cibles** (top-1) | **220/220 = 1,0** | moyenne **1,997/220 = 0,908 %** ; médiane 2 ; max 10 ; p95 5 | **0/2 000** |
215:| **candidat aléatoire** (top-1) | **220/220 = 1,0** | moyenne **92,7/220 = 42,14 %** (585 candidats, 2,66/label) | **0/2 000** |
216:| **permutation des listes de candidats** (top-k, égalité) | **219/220 = 0,9955** | moyenne **2,18/220 = 0,99 %** ; max 8 | **0/2 000** |
217:| **permutation des listes de candidats** (top-k, sous-chaîne) | **219/220 = 0,9955** | moyenne **2,58/220 = 1,17 %** ; max 9 | **0/2 000** |
219:**Lecture.** L'attachement n'est pas un artefact du hasard : la permutation des cibles divise
220:l'exact par 110, le candidat aléatoire par 2,4, le top-k par 85. Le contrôle « candidat
369:- **Le top-k officiel (sous-chaîne) est peu discriminant** : la permutation des listes de
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/pensee-audit-v10.json'))\nprint(list(d))\n# find keys with permutation\ndef find(o,p=''):\n    if isinstance(o,dict):\n        for k,v in o.items():\n            if isinstance(v,(dict,list)): find(v,p+'/'+k)\n            elif 'per … [135 caractères tronqués]`

  ```
['rapport', 'ligne', 'branche', 'commit_audite', 'commit_parent', 'date', 'objet', 'methode', 'verdict', 'rejeu', 'ablations', 'controle_negatif', 'spans_19', 'dev_test', 'portes_autotest', 'ecarts', 'limites', 'fichiers_ecrits', 'commit']
/controle_negatif/candidat_aleatoire/avec_candidats = 220
/controle_negatif/candidat_aleatoire/candidats_total = 585
  ```

- **bash** `{"command": "python3 -c \"import json; d=json.load(open('reports/pensee-audit-v10.json')); print(json.dumps(d['controle_negatif'],ensure_ascii=False,indent=1))\"", "description": "Print audit v10 negative controls"}`

  ```
{
 "permutation_globale": {
  "n": 220,
  "observe": 220,
  "tirages": 2000,
  "graine": 0,
  "moyenne": 1.997,
  "mediane": 2.0,
  "max": 10,
  "p95": 5,
  "p": 0.0,
  "taux_moyen": 0.00908,
  "lecture": "0,908 % en moyenne contre 100 % observé"
 },
 "candidat_aleatoire": {
  "n": 220,
  "avec_candidats": 220,
  "candidats_total": 585,
  "tirages": 2000,
  "graine": 0,
  "top1_moyen": 92.7,
  "top1_taux": 0.4214,
  "observe_top1": 220,
  "p_top1": 0.0,
  "lecture": "42,14 % en moyenne contre 100 % observé"
 },
 "permutation_candidats_topk_exact": {
  "n": 220,
  "observe": 219,
  "tirages": 2000,
  "graine": 0,
  "moyenne": 2.18,
  "taux": 0.0099,
  "max": 8,
  "p": 0.0,
  "lecture": "0,99 % en moyenne contre 99,55 % observé (critère = égalité)"
 },
 "permutation_candidats_topk_souschaine": {
  "n": 220,
  "observe": 219,
  "tirages": 2000,
  "graine": 0,
  "moyenne": 2.58,
  "taux": 0.0117,
  "max": 9,
  "p": 0.0,
  "lecture": "1,17 % en moyenne contre 99,55 % observé (critère officiel = sous-chaîne)"
 },
 "spans_19_verifies": true
}
  ```

- **bash** `{"command": "date '+%Y-%m-%d %H:%M %Z'; git status --short | wc -l", "description": "Check system date"}`

  ```
2026-11-15 05:58 EST
34
  ```

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_faq.py", "content": "#!/usr/bin/env python3\n\"\"\"verifier_faq.py — les dix réponses de la FAQ produit, vérifiées contre le code courant.\n\nLa FAQ de `docs/produit/README.md` (§ 8) ne doit pas être une prose recopiée : c … [23112 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_faq.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "python3 tools/verifier_faq.py; echo \"exit=$?\"", "description": "Run FAQ verifier"}`

  ```
FAQ produit — 9/10 réponses vérifiées · contrôle négatif détecté
  ✅  1. Quelles langues le produit reconnaît-il ?
  ✅  2. Est-ce que ça marche hors ligne ?
  ✅  3. Combien ça coûte ?
  ✅  4. Qu'est-ce que --tagger change ?
  ❌  5. Quel est le format de sortie, et est-il stable ?
      KeyError : 'meta'
  ✅  6. Que veut dire « attachement », et à quel point est-il fiable ?
  ✅  7. Pourquoi reste-t-il un span inatteignable ?
  ✅  8. Que peut-on restituer : la surface, la forme, les rôles ?
  ✅  9. Quelles limites faut-il connaître avant de s'en servir ?
  ✅ 10. Comment l'installer et le lancer ?
❌ FAQ non vérifiée
exit=1
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('tools/schemas/drave-annotation-v2.json'))\nprint(list(d['properties']))\nprint(list(d['properties']['etiquettes']['items']['properties']))\nprint(list(d['properties']['etiquettes']['items']['properties']['meta']['properties']))\nPY", "des … [45 caractères tronqués]`

  ```
['schema', 'version', 'texte', 'langue', 'script', 'source', 'refus', 'etiquettes', 'unites_semantiques', 'fraction_semantique', 'trace', 'cout', 'contexte']
['niveau', 'type', 'valeur', 'debut', 'fin', 'source', 'confiance', 'candidats', 'langue', 'script', 'meta']
['partition', 'alternative']
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_faq.py", "old_string": "    assert \"partition\" in v2[\"properties\"][\"meta\"][\"properties\"]\n    assert \"alternative\" in v2[\"properties\"][\"meta\"][\"properties\"]", "new_string": "    meta = v2[\"properties\"][\" … [154 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_faq.py has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/verifier_faq.py; echo \"exit=$?\"", "description": "Re-run FAQ verifier"}`

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

- **bash** `{"command": "python3 tools/verifier_faq.py --json > reports/faq.json; echo exit=$?; python3 -c \"import json; d=json.load(open('reports/faq.json')); print(d['ok'], len(d['questions']), d['controle_negatif'])\"; wc -l reports/faq.json", "description": "Generate FAQ verification JSON"}`

  ```
exit=0
True 10 {'affirmations_fausses': ['le CLI accepte --langue de (il sort 2)', "le schéma v2 accepte l'annotation v1 (il la refuse)"], 'observe': {'--langue de': 'code 2', 'v2_refuse_v1': True}, 'detecte': True}
316 reports/faq.json
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "old_string": "## 8. Où aller ensuite", "new_string": "## 8. FAQ — dix questions\n\n> **Vérifié le 2026-11-15** contre le code courant (`drave 0.1.0`) par\n> [`tools/verifier_faq.py`](../../tools/verifier_faq.py) … [7171 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **write** `{"content": "# B13 / D3 — la FAQ du produit : dix questions, dix réponses vérifiées\n\n> **Ligne de roadmap** : **B13** (produit) · **Tâche** : **D3** · **Date** : 2026-11-15 ·\n> **Verdict** : ✅ **10/10 réponses vérifiées** contre le code courant (`drave 0.1.0`) ;\n> **contrôle négatif détecté** (d … [10133 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-faq.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "grep -n \"744\\|838\\|D2\\|D1\\|restitution v2\" docs/pilotage/en-cours.md | head -20", "description": "Locate state lines to edit"}`

  ```
3:**Mis à jour : 2026-11-15, 05 h 30 HNE (D2)**
64:- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/239 (0,9958)**, **F1 0,7902**, **1 span** ; **`s065`** et **`r035`** réglés, **convention des GV** ; **restitution v1** (46/46 canonique, strict 0,1087 ; [fiche](../../reports/rapport-restitution-v1.md)) ; **J11.1–J11.4** ([exemples](../../reports/rapport-exemples-rejoues.md), [par-langue](../../reports/rapport-evaluer-langue.md), [robustesse](../../reports/rapport-robustesse-semaine.md), [schéma](../../reports/rapport-schema-v2-doc.md)) ; **D1** ([fiche](../../reports/rapport-exemples-tagger.md)).
90:- **Pensée — B13 (actif)** : **183/183** ; `r035` (238/238), convention GV (0,7902), `s065` (238/238), **J6.1 rejeté** (g017 à trancher), schéma v2, **restitution v2** **16/46** ([fiche](../../reports/rapport-restitution-v2.md)), **J9.1**, **D1** ; [s065](../../reports/rapport-s065.md), [J9.1](../../reports/rapport-passe-honnetete.md).
109:| fichiers / JSON de résultats | **744** / **838** | `reports/*.md` / `reports/*.json` |
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**Mis à jour : 2026-11-15, 06 h 00 HNE (D3)**", "old_string": "**Mis à jour : 2026-11-15, 05 h 30 HNE (D2)**"}`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md": file has not been read — read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "limit": 120}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
1: # En ce moment
2: 
3: **Mis à jour : 2026-11-15, 05 h 30 HNE (D2)**
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
21: > [`journal/sessions/`](../../journal/sessions/)
… [9544 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "**Mis à jour : 2026-11-15, 06 h 00 HNE (D3)**", "old_string": "**Mis à jour : 2026-11-15, 05 h 30 HNE (D2)**"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/239 (0,9958)**, **F1 0,7902**, **1 span** ; **`s065`** et **`r035`** réglés, **convention des GV** ; **restitution v1** (46/46 c … [1472 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Pensée — B13 (actif)** : **183/183** ; `r035` (238/238), convention GV (0,7902), `s065` (238/238), **J6.1 rejeté** (`g017` inatteignable), schéma v2, **restitution v2** **19/46** cadres (**1 … [600 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "| fichiers / JSON de résultats | **745** / **839** | `reports/*.md` / `reports/*.json` |", "old_string": "| fichiers / JSON de résultats | **744** / **838** | `reports/*.md` / `reports/*.json` | … [2 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md", "new_string": "> § 3.5 ont été relancées le 07/11 pour le format v2 ; les mesures chiffrées du § 2 datent du\n> **06/11**, et l'`evaluer` du § 3.3 a été relancé le **14/11** (gold vivant 612, `--par-langue\n> fr/ … [535 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/produit/README.md has been updated successfully.
  ```

- **bash** `{"command": "grep -n \"rapport-gold-reel-50\\|rapport-restitution-v2\\|rapport-faq\\|rapport-s-paragraphes\" reports/INDEX.md reports/README.md", "description": "Check index entries for pending reports"}`

  ```
reports/INDEX.md:198:| [rapport-gold-reel-50.md](rapport-gold-reel-50.md) | R0.7 / B13 — le gold réel étendu : 50 phrases que l'heuristique rate, et ce qu'elles disent |
reports/INDEX.md:690:| [rapport-restitution-v2.md](rapport-restitution-v2.md) | B13 — la restitution v2 : les rôles se lisent, leur fidélité ne suit pas |
reports/INDEX.md:707:| [rapport-s-paragraphes.md](rapport-s-paragraphes.md) | S — La banque de paragraphes passe à neuf : six paires d'Alice, sources anglaises et référents |
reports/README.md:19:| [`rapport-gold-reel-50.md`](rapport-gold-reel-50.md) | **R0.7** — le gold réel : 452 phrases, 50 ratées, le « 200+ » obsolète |
reports/README.md:60:| [`rapport-restitution-v2.md`](rapport-restitution-v2.md) | **B13** — restitution v2 : rôles **16/46**, F1 **0,5270** |
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -40; echo \"exit=${PIPESTATUS[0]}\"", "description": "Run documentation review"}`

  ```
revue de documentation · 745 fiche(s) · 839 JSON · 123 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
exit=0
  ```

- **bash** `{"command": "bash tools/porte-tableaux.sh 2>&1 | tail -20; echo \"exit=${PIPESTATUS[0]}\"", "description": "Run table gate"}`

  ```
✅ 1817 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4433 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-15)
exit=0
  ```

- **bash** `{"command": "python3 tools/verifier_schemas.py 2>&1 | tail -10; echo \"exit=${PIPESTATUS[0]}\"; python3 tools/verifie_en_cours.py 2>&1 | tail -10; echo \"exit=${PIPESTATUS[0]}\"", "description": "Run schema and state checks"}`

  ```
schémas · 463 document(s) · 67 SVG · 2 source(s)
  ✅ aucun ASCII art, SVG valides et référencés, blocs PlantUML inline valides,
     sources et images relatives.
exit=0
  en-cours · 1644 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
exit=0
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -20; echo \"exit=${PIPESTATUS[0]}\"", "description": "Run context budget check"}`

  ```
3072    341 DATÉ      0  docs/implantation/convertisseur.md
    2962    364   T1   5000  docs/theorie/glossaire/02-modeles-et-architectures.md
    2896    352 DATÉ      0  docs/implantation/configuration-nvme-raid-amd.md
    2496    171   T1   2500  docs/pilotage/references-non-regression.md
    2476    222   T1   2800  reports/README.md
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/format-flux.md
    1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4014 mots (budget 4 000)

  avertissements :
     · 56 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-f
… [118 caractères tronqués]
  ```

- **bash** `{"command": "bash tools/porte-produit.sh 2>&1 | tail -30; echo \"exit=${PIPESTATUS[0]}\"", "description": "Run product gate"}`

  ```
[still running after 60000ms; moved to background job bash-98]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | sed -n '1,40p'", "description": "Inspect T0 composition"}`

  ```
budget de contexte · documents chargeables
    mots lignes  cat budget  document
    9000    493   T1   9000  docs/pilotage/roadmap.md
    5999    597 DATÉ      0  docs/implantation/contexte-long.md
    4858    515   T1   5000  docs/theorie/glossaire/10-le-pont-linguistico-semantique-le-vocabu.md
    4085    431 DATÉ      0  docs/implantation/numa-segregation.md
    3310    317   T1   3500  README.md
    3072    341 DATÉ      0  docs/implantation/convertisseur.md
    2962    364   T1   5000  docs/theorie/glossaire/02-modeles-et-architectures.md
    2896    352 DATÉ      0  docs/implantation/configuration-nvme-raid-amd.md
    2496    171   T1   2500  docs/pilotage/references-non-regression.md
    2476    222   T1   2800  reports/README.md
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/form
… [519 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"T0\\|4014\\|AGENTS\\|en-cours\" tools/taille_documents.py | head -40; sed -n '1,140p' tools/taille_documents.py", "description": "Inspect context budget tool"}`

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
… [5796 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport sys, pathlib\nsys.path.insert(0,'tools')\nimport taille_documents as t\nrac=pathlib.Path('.')\ndef w(p): return t.mots_hors_diagrammes(pathlib.Path(p).read_text())\nprint('AGENTS',w('AGENTS.md'))\nprint('en-cours',w('docs/pilotage/en-cours.md'))\nbest=max(((w(st … [295 caractères tronqués]`

  ```
AGENTS 1196
en-cours 1644
best tache (1174, 'docs/methode/continuite.md')
T0 4014
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Fait** : B13 **183/183** ; **POS 86,25 %**, **attachement 238/239 (0,9958)**, **F1 0,7902**, **1 span** ; **`s065`**, **`r035`**, **GV** réglés ; **restitution v1** (46/46 canonique, strict  … [1537 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Pensée — B13 (actif)** : **183/183** ; `r035` (238/238), `s065` (238/238), **J6.1 rejeté** (`g017` inatteignable), schéma v2, **v2** **19/46** (**16** non vides, F1 **0,5270**) ([fiche](../. … [644 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | tail -8; echo \"exit=${PIPESTATUS[0]}\"", "description": "Re-run context budget"}`

  ```
1833    210   T1   5000  docs/theorie/glossaire/06-repartition-materiel-et-energie.md
  T0 max : 4001 mots (budget 4 000)

  avertissements :
     · 56 fiche(s) > 300 lignes : lire le verdict + une section, jamais tout (plus longues : 888 l. rapport-modele-drave.md, 759 l. rapport-vision-qwen2vl.md, 754 l. rapport-frontieres-phrase.md, 730 l. rapport-partition-syntagmes.md, 662 l. rapport-fiabilite-produit.md)

  ❌ 1 violation(s) :
     · T0 : 4001 mots (AGENTS + en-cours + une tâche) > budget 4 000
exit=1
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "new_string": "- **Pensée — B13 (actif)** : **183/183** ; `r035` (238/238), `s065` (238/238), **J6.1 rejeté** (`g017` inatteignable), schéma v2, **v2** **19/46** (**16** non vides, F1 **0,5270**) ([fiche](../. … [578 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | grep -E \"T0 max|violation|✅|❌\" | tail -5; echo \"exit=${PIPESTATUS[0]}\"", "description": "Re-check context budget"}`

  ```
T0 max : 4000 mots (budget 4 000)
  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
exit=0
  ```

- **job_output** `{"job_id": "bash-98", "timeout_ms": 1000}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -6; echo \"exit=${PIPESTATUS[0]}\"; python3 tools/verifie_en_cours.py 2>&1 | tail -3; echo \"exit=${PIPESTATUS[0]}\"", "description": "Re-run docs and state checks"}`

  ```
revue de documentation · 745 fiche(s) · 839 JSON · 123 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
exit=0
  en-cours · 1630 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
exit=0
  ```

- **bash** `{"command": "bash tools/porte-tableaux.sh 2>&1 | tail -5; echo \"exit=${PIPESTATUS[0]}\"", "description": "Re-run table gate"}`

  ```
✅ 1817 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4433 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-15)
exit=0
  ```

- **bash** `{"command": "python3 tools/verifier_faq.py --autotest; echo \"exit=$?\"; python3 tools/verifier_faq.py; echo \"exit=$?\"", "description": "Test verifier negative control and full run"}`

  ```
✅ autotest : l'affirmation fausse est rejetée
exit=0
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

- **job_output** `{"job_id": "bash-98", "timeout_ms": 1000}`

  ```
(no new output)
[status: running]
  ```

- **bash** `{"command": "ps -o pid,etime,cmd -C python3 | tail -10; job_list 2>/dev/null || true", "description": "Check running python processes"}`

  ```
2997720    01:27:47 python3 tools/chantier/superviseur.py boucle --budget 14400 --timeout 3600
3306376       01:42 python3 -m tools.pensee.autotest
3306379       01:42 python3 -m tools.pensee.autotest
3306380       01:42 python3 -m tools.pensee.autotest
3306381       01:42 python3 -m tools.pensee.autotest
3306382       01:42 python3 -m tools.pensee.autotest
3306383       01:42 python3 -m tools.pensee.autotest
3306384       01:42 python3 -m tools.pensee.autotest
3306385       01:42 python3 -m tools.pensee.autotest
3306386       01:42 python3 -m tools.pensee.autotest
  ```

- **bash** `{"command": "python3 tools/tests/test_restitution_v2.py 2>&1 | tail -5; echo \"exit=${PIPESTATUS[0]}\"", "description": "Run restitution v2 tests"}`

  ```
----------------------------------------------------------------------
Ran 17 tests in 1.146s

OK
exit=0
  ```

- **bash** `{"command": "grep -rn \"0\\.12\\|seuil.*langue\\|SEUIL\" tools/bloc_linguistique.py | head -20; grep -n \"398\\|0,9687\\|0.9687\" reports/rapport-evaluer-langue.md | head", "description": "Verify language threshold and 398 figures"}`

  ```
802:                 seuil_ouvert: float = 0.55, seuil_langue: float = 0.12,
807:        self.seuil_langue = seuil_langue
822:        if conf < self.seuil_langue:
2862:        return Cascade(h, n, seuil=args.seuil).analyser(texte, args.langue, args.contexte)
  ```

- **bash** `{"command": "grep -n \"398\\|9687\\|96,87\" reports/rapport-evaluer-langue.md | head -20; grep -rn \"398\" reports/*.md | head -10", "description": "Find 398 language provenance"}`

  ```
reports/INDEX.md:86:| [rapport-bloc-linguistique.md](rapport-bloc-linguistique.md) | Le bloc linguistique — 398 langues au niveau langue, un contrat pour l'heuristique et le neuronal |
reports/rapport-b102bis-decodeur.md:62:| 1500 | 15.5 | 10.8 | 15.4 | 11.3 | 0.398 / 0.317 |
reports/rapport-b13-porte-138.md:40:| T110 (segmenteur) | 0,1683 / 0,1398 | **0,2739 / 0,1398** | ✅ |
reports/rapport-b13-porte-140.md:41:| T110 (segmenteur) | 0,1683 / 0,1398 | **0,2739 / 0,1398** | ✅ |
reports/rapport-bloc-linguistique.md:1:# Le bloc linguistique — 398 langues au niveau langue, un contrat pour l'heuristique et le neuronal
reports/rapport-bloc-linguistique.md:6:> **langue** est mesurée à **0,9687** sur **398 langues** (script **1,0000**, profils permutés
reports/rapport-bloc-linguistique.md:42:## 3. La langue et le script : 398 langues
reports/rapport-bloc-linguistique.md:49:| langues avec profil | **398** |
reports/rapport-bloc-linguistique.md:56:**Ce que ça prouve** : un CPU, sans modèle, identifie la langue et le script de 398 langues UDHR
reports/rapport-bloc-linguistique.md:156:- **la langue et le script ne sont pas la traduction** : 398 langues identifiées ne veulent pas
[stderr]
grep: 
… [24 caractères tronqués]
  ```

### 👤 Utilisateur

background job bash-98 (bash: bash tools/porte-produit.sh 2>&1 | tail -30; echo "exit=${PIPESTATUS[0]}") finished [status: completed, exit code: 0]. Read its output with job_output.

- **job_output** `{"job_id": "bash-98", "timeout_ms": 1000}`

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
exit=0
[status: completed, exit code: 0]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_faq.py", "new_string": "    refus = _run([\"analyser\", \"Le chat dort.\", \"--langue\", \"de\"])\n    assert de[\"langue\"] == \"de\", de[\"langue\"]\n    assert es[\"langue\"] == \"es\", es[\"langue\"]\n    assert und[\" … [1927 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_faq.py has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/verifier_faq.py --json > reports/faq.json; echo exit=$?; python3 tools/verifier_faq.py | tail -3", "description": "Regenerate JSON after q1 hardening"}`

  ```
exit=0
  ✅  9. Quelles limites faut-il connaître avant de s'en servir ?
  ✅ 10. Comment l'installer et le lancer ?
✅ FAQ vérifiée
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('reports/faq.json'))\nprint(json.dumps(d['questions'][0],ensure_ascii=False,indent=1))\nprint('tail keys',list(d))\nprint('ok',d['ok'])\nPY", "description": "Inspect final JSON top question"}`

  ```
{
 "id": 1,
 "question": "Quelles langues le produit reconnaît-il ?",
 "observe": {
  "detection": {
   "Der Hund schläft.": "de",
   "El perro duerme.": "es"
  },
  "und": {
   "Élodie sourit.": "und",
   "avec --langue fr": "und"
  },
  "indice_cli": {
   "choix": [
    "fr",
    "en"
   ],
   "--langue de": "code 2"
  },
  "profils_udhr": {
   "langues": 398,
   "exactitude": 0.9687,
   "seuil": 0.12,
   "source": "reports/rapport-bloc-linguistique.md"
  }
 },
 "ok": true,
 "erreur": ""
}
tail keys ['schema', 'version', 'date', 'produit', 'fichier', 'questions', 'controle_negatif', 'ok']
ok True
  ```

- **bash** `{"command": "git ls-files data | head -5; echo \"count=$(git ls-files data | wc -l)\"; ls -d data 2>/dev/null && ls data | head", "description": "Check whether data is versioned"}`

  ```
count=0
data
adaptateurs
alignement
composition-etats.npz
composition-verne-14b-etats.npz
composition-verne-7b-etats.npz
composition-verne-etats.npz
composition-verne-large-etats.npz
composition-verne-plan-etats.npz
consignes_train.jsonl
consignes_val.jsonl
  ```

- **bash** `{"command": "python3 tools/drave.py analyser \"Le chat de la voisine qui dort sur le toit se réveille.\" --json 2>/dev/null | python3 -c \"\nimport json,sys\nd=json.load(sys.stdin)\nroles=[e.get('meta',{}).get('role') for e in d['etiquettes'] if e['niveau']=='syntagme']\nprint(sorted(set(r for r in  … [66 caractères tronqués]`

  ```
['agent', 'possession', 'predicat', 'qualite', 'qualité']
  ```

- **bash** `{"command": "grep -n 'role.*prédicat\\|\"prédicat\"\\|prédicat' tools/bloc_linguistique.py | head -20; grep -n '\"predicat\"' tools/bloc_linguistique.py | head -10", "description": "Check role literal spellings in code"}`

  ```
946:                # le prédicat peut commencer par un clitique élidé (« elle s'ouvre »,
1317:                    predicat_vu = False   # un prédicat a déjà été vu dans la clause
1323:                                break      # un AUX après un prédicat ouvre la principale
1336:                                break  # second prédicat : la principale commence
1409:                # le GV s'arrête à la préposition, au déterminant, au relatif : un prédicat
1429:                segments.append({"type": "GV", "role": "prédicat", "niveau": 0,
  ```

- **bash** `{"command": "sed -n '1415,1435p' tools/bloc_linguistique.py; grep -n '\"role\": \"predicat\"' tools/bloc_linguistique.py | head", "description": "Inspect GV role emission"}`

  ```
and _normaliser(mots[j][2]) not in SUBORDONNANTS
                       # l'adverbe **final** de la phrase n'est pas dans le GV
                       # (« viens | demain »), sauf la négation (« ne dort pas »)
                       and not (_normaliser(mots[j][2]) in ADVERBES_TEMPS
                                and (j + 1 >= len(mots) or mots[j + 1][3] != "mot"))
                       # un marqueur **élidé** arrête aussi le GV (« sais | qu'il vient ») :
                       # le radical « qu » + « e » = « que »
                       and (_normaliser(mots[j][2]).split("'")[0] + "e"
                            if _normaliser(mots[j][2]).split("'")[0] == "qu" else
                            _normaliser(mots[j][2])) not in RELATIFS
                       and (_normaliser(mots[j][2]).split("'")[0] + "e"
                            if _normaliser(mots[j][2]).split("'")[0] == "qu" else
                            _normaliser(mots[j][2])) not in SUBORDONNANTS):
                    j += 1
                segments.append({"type": "GV", "role": "prédicat", "niveau": 0,
                                 "debut": d, "fin": mots[j - 1][1],
                                 "texte": texte[d
… [191 caractères tronqués]
  ```

- **bash** `{"command": "grep -n 'predicat\"' tools/bloc_linguistique.py | head -20; grep -n \"'predicat'\\|\\\"predicat\\\"\" tools/bloc_linguistique.py | head -20", "description": "Find unaccented predicat literal"}`

  ```
(no output)
  ```

- **bash** `{"command": "grep -rn '\"predicat\"' tools/*.py | head -20; grep -rn \"predicat\" tools/bloc_linguistique.py | head -30", "description": "Find role definition source"}`

  ```
tools/restitution_v2.py:42:ROLES = ("agent", "predicat", "lieu")
tools/restitution_v2.py:43:LIBELLES = {"agent": "agent", "predicat": "prédicat", "lieu": "lieu"}
tools/restitution_v2.py:57:    return {"agent": "agent", "prédicat": "predicat", "predicat": "predicat",
tools/restitution_v2.py:98:        "agent": "", "predicat": "", "lieu": "",
tools/restitution_v2.py:149:        "predicat": predicat["valeur"],
tools/restitution_v2.py:172:        if e["role_normalise"] != "predicat":
tools/restitution_v2.py:236:            "predicats": sum(1 for e in segments if e["role_normalise"] == "predicat"),
tools/restitution_v2.py:251:    cadre = {"agent": "", "predicat": "", "lieu": ""}
tools/restitution_v2.py:274:        variantes = [{"agent": "", "predicat": "", "lieu": ""}]
tools/restitution_v2.py:320:    return {"agent": premier("GN"), "predicat": premier("GV"), "lieu": premier("GP")}
tools/restitution_v2.py:325:    return {"agent": cadre.get("predicat", ""),
tools/restitution_v2.py:326:            "predicat": cadre.get("lieu", ""),
tools/restitution_v2.py:351:            if sans and role == "predicat":
tools/restitution_v2.py:356:            if not sans and role == "predicat":
tools/restit
… [924 caractères tronqués]
  ```

- **bash** `{"command": "grep -n '\"role\"' tools/bloc_linguistique.py | head -40", "description": "Find all role assignments"}`

  ```
974:                        gn.update({"type": "GN", "role": "agent", "niveau": 0,
1345:                                     "role": "complément" if stype == "SUB" else "qualité",
1372:                segments.append({"type": "GN", "role": role, "niveau": 0,
1380:                    segments.append({"type": "REL", "role": "qualité", "niveau": 1,
1394:                segments.append({"type": "GN", "role": "agent", "niveau": 0,
1402:                segments.append({"type": "GN", "role": "agent", "niveau": 0,
1429:                segments.append({"type": "GV", "role": "prédicat", "niveau": 0,
1446:                segments.append({"type": "GP", "role": _role_gp(t), "niveau": 1,
1701:                    meta = {"role": s.get("role", ""), "niveau": s.get("niveau", 0)}
1724:                meta = {"role": s["role"], "niveau": s["niveau"]}
1751:                meta = {"role": s["role"], "niveau": s["niveau"], "union": True}
1878:                                        script=script, meta={"role": s["role"], "niveau": s["niveau"]}))
2016:        corps = {"messages": [{"role": "user", "content": invite}], "temperature": 0,
2150:        corps = {"messages": [{"role": "user", "content": invite
… [215 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/drave.py analyser \"Le chat de la voisine qui dort sur le toit se réveille.\" --json 2>/dev/null | python3 -c \"\nimport json,sys\nd=json.load(sys.stdin)\nfor e in d['etiquettes']:\n    if e['niveau']=='syntagme':\n        print(json.dumps(e,ensure_ascii=False))\n\" | head … [52 caractères tronqués]`

  ```
{"niveau": "syntagme", "type": "GN", "valeur": "Le chat", "debut": 0, "fin": 7, "source": "heuristique", "confiance": 0.4, "candidats": ["« qui dort sur le toit » → voisine", "« qui dort sur le toit » → Le chat", "réveille", "voisine", "chat"], "langue": "fr", "script": "Latn", "meta": {"role": "agent", "niveau": 1, "attachement": {"segment": "Le chat", "cible": "réveille"}}}
{"niveau": "syntagme", "type": "GP", "valeur": "de la voisine", "debut": 8, "fin": 21, "source": "heuristique", "confiance": 0.4, "candidats": ["« qui dort sur le toit » → voisine", "« qui dort sur le toit » → Le chat", "réveille", "voisine", "chat"], "langue": "fr", "script": "Latn", "meta": {"role": "possession", "niveau": 2, "attachement": {"segment": "de la voisine", "cible": "réveille"}}}
{"niveau": "syntagme", "type": "REL", "valeur": "qui dort sur le toit", "debut": 22, "fin": 42, "source": "heuristique", "confiance": 0.4, "candidats": ["« qui dort sur le toit » → voisine", "« qui dort sur le toit » → Le chat", "réveille", "voisine", "chat"], "langue": "fr", "script": "Latn", "meta": {"role": "qualite", "niveau": 2, "attachement": {"segment": "qui dort sur le toit", "cible": "voisine"}, "partition": {"g
… [2242 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"prédicat.*predicat\\|predicat.*prédicat\\|role_normalise\\|normaliser_role\" tools/*.py | head -30", "description": "Find role normalization"}`

  ```
tools/bloc_linguistique.py:1317:                    predicat_vu = False   # un prédicat a déjà été vu dans la clause
tools/restitution_v2.py:43:LIBELLES = {"agent": "agent", "predicat": "prédicat", "lieu": "lieu"}
tools/restitution_v2.py:48:_ROLE_LIGNE = re.compile(r"^\s*(agent|prédicat|predicat|lieu)\s*:\s?(.*)$",
tools/restitution_v2.py:52:def normaliser_role(role: str) -> str:
tools/restitution_v2.py:53:    """`prédicat` → `predicat` ; les autres rôles sont rendus en minuscules."""
tools/restitution_v2.py:57:    return {"agent": "agent", "prédicat": "predicat", "predicat": "predicat",
tools/restitution_v2.py:82:            "role_normalise": normaliser_role(meta.get("role", "")),
tools/restitution_v2.py:172:        if e["role_normalise"] != "predicat":
tools/restitution_v2.py:182:    agents = [e for e in segments if e["role_normalise"] == "agent"]
tools/restitution_v2.py:183:    lieux = [e for e in segments if e["role_normalise"] == "lieu"]
tools/restitution_v2.py:185:               and e["role_normalise"] in ("", "groupe nominal")]
tools/restitution_v2.py:209:    roles_segments = [e for e in segments if e["role_normalise"] in ROLES]
tools/restitution_v2.py:210:    autres = [e fo
… [1244 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"predicat\" tools/bloc_linguistique.py | sed -n '1,80p'", "description": "List all predicat occurrences"}`

  ```
1317:                    predicat_vu = False   # un prédicat a déjà été vu dans la clause
1322:                            if predicat_vu and not prec_aux:
1330:                                predicat_vu = True
1335:                            if predicat_vu or verbes_vus == 2:
1337:                            predicat_vu = True
1340:                                predicat_vu = True   # « is red » : copule + attribut
  ```

- **bash** `{"command": "grep -n \"replace(.*é\\|translate\\|accent\\|unidecode\\|é.*e\" tools/bloc_linguistique.py | head -40", "description": "Search accent normalization"}`

  ```
2:"""bloc_linguistique.py — le bloc d'étiquetage linguistique, du graphème à la pragmatique.
4:Un seul contrat (`BlocLinguistique.analyser`) et **plusieurs implémentations** :
6:  - `Heuristique` : CPU, déterministe, ultra-rapide ; elle étiquette la surface et produit des
7:    **candidats** pour l'ambigu ; elle déclare sa couverture et sa confiance ;
8:  - `MockNeuronal` : une implémentation neuronale **de contrat**, déterministe, pour tester la
10:  - `NeuronalLLM` : l'adaptateur réel, qui interroge un modèle local (`llama-cli`) et rend le
12:  - `NeuronalLLMPOS` : le **tagger** neuronal réel — un modèle local, une liste de tokens, des
13:    POS alignés par grammaire GBNF ; c'est l'implémentation qualifiée sur le gold ;
15:    étiquettes par confiance ; la cascade n'envoie au neuronal que le **résidu** des niveaux
18:La sortie est une **annotation typée** — pas le corps de la RSN : chaque étiquette porte son
20:La couche sémantique ne reçoit que `unites_semantiques` ; l'heuristique peut donc l'activer à
23:    python3 tools/bloc_linguistique.py --texte "Le chat de la voisine qui dort sur le toit se réveille."
93:# chevauchent). Le format reste additif ; le vérificateur lit encor
… [2899 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1680,1760p' tools/bloc_linguistique.py", "description": "Inspect label construction"}`

  ```
if x.get("fin", 0) <= s.get("debut", 0)]
                        if avant:
                            g = max(avant, key=lambda x: x["fin"])
                            if g.get("type") == "GV" and not _est_adverbe_seul(g):
                                cible = self._verbe_dans(texte, g["debut"], g["fin"], verbes)
                            elif g.get("type") == "GN":
                                cible = self._tete_nom(texte, g["debut"], g["fin"])
                    if not cible and s.get("type") == "GP":
                        cible = self._cible_proche(texte, s, gvs, verbes, cache_gv)
                    if not cible and brute and _normaliser(brute) not in ADVERBES_SEULS:
                        i = texte.find(brute)
                        if i >= 0:
                            cible = self._verbe_dans(texte, i, i + len(brute), verbes)
                    if cible and _normaliser(cible) in AUXILIAIRES:
                        cible = None  # « a » / « est » ne sont pas des cibles
                    if not cible:
                        gns_s = [x for x in c.get("segments", []) if x.get("type") == "GN"]
                        cible = (self._repli_cible_gp(texte, s, gns
… [4044 caractères tronqués]
  ```

- **bash** `{"command": "for p in alternative brut filtrer; do echo \"== $p\"; python3 tools/drave.py analyser \"Le chat de la voisine qui dort sur le toit se réveille.\" --partition $p --json 2>/dev/null | python3 -c \"\nimport json,sys\nd=json.load(sys.stdin)\nprint(sorted(set(e.get('meta',{}).get('role') for … [149 caractères tronqués]`

  ```
== alternative
['agent', 'possession', 'predicat', 'qualite', 'qualité']
== brut
['agent', 'possession', 'predicat', 'qualite', 'qualité']
== filtrer
['agent', 'possession', 'qualité']
  ```

- **bash** `{"command": "grep -n \"class Heuristique\\|def __init__\" tools/bloc_linguistique.py | head -20; sed -n '1580,1620p' tools/bloc_linguistique.py", "description": "Inspect Heuristique init and union"}`

  ```
796:class Heuristique:
801:    def __init__(self, profils: dict[str, dict] | None = None, segmenter_s: bool = True,
1842:    def __init__(self, profils: dict[str, dict] | None = None):
1898:    def __init__(self, modele: str | pathlib.Path, llama_cli: str = "llama-cli",
1987:    def __init__(self, modele: str | pathlib.Path, endpoint: str = "http://127.0.0.1:18081",
2116:    def __init__(self, modele: str | pathlib.Path, endpoint: str = "http://127.0.0.1:18082",
2246:    def __init__(self, pos: BlocLinguistique, chunks: BlocLinguistique,
2296:    def __init__(self, modele: str | pathlib.Path, endpoint: str = "http://127.0.0.1:18082",
2644:    def __init__(self, blocs: Sequence[BlocLinguistique],
2669:    def __init__(self, heuristique: BlocLinguistique, neuronal: BlocLinguistique,
2709:    def __init__(self, cout_par_octet: float = 1.0):
                if _k == 0 or _e.type != "NOUN" or _e.confiance > 0.45:
                    continue
                _av = etiquettes[pos_idx[_k - 1]]
                if _normaliser(_av.valeur) in _copules:
                    etiquettes[_i] = Etiquette("pos", "ADJ", _e.valeur, _e.debut, _e.fin, self.nom,
                                           
… [2261 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"predicat\" tools/generateur.py tools/*.py 2>/dev/null | grep -v \"restitution_v2\\|verifier_faq\" | head -20; ls tools/generateur.py 2>/dev/null || find tools -name '*generateur*' -maxdepth 2", "description": "Find S generator role"}`

  ```
tools/bloc_linguistique.py:1317:                    predicat_vu = False   # un prédicat a déjà été vu dans la clause
tools/bloc_linguistique.py:1322:                            if predicat_vu and not prec_aux:
tools/bloc_linguistique.py:1330:                                predicat_vu = True
tools/bloc_linguistique.py:1335:                            if predicat_vu or verbes_vus == 2:
tools/bloc_linguistique.py:1337:                            predicat_vu = True
tools/bloc_linguistique.py:1340:                                predicat_vu = True   # « is red » : copule + attribut
tools/structures/generateur.py
  ```

- **bash** `{"command": "grep -rn \"predicat\\|prédicat\" tools/structures/generateur.py | head -20", "description": "Search S generator roles"}`

  ```
472:                            "GV", "predicat", 0))
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_faq.py", "new_string": "    source = DRAVE.read_text(encoding=\"utf-8\")\n    for interdit in (\"http.server\", \"transformers\", \"torch\", \"sys.stdin\"):\n        assert interdit not in source, interdit\n    for nom in  … [3008 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/verifier_faq.py has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/verifier_faq.py; echo exit=$?; python3 tools/verifier_faq.py --json > reports/faq.json; echo json_exit=$?", "description": "Run verifier after q9 hardening"}`

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
json_exit=0
  ```

- **bash** `{"command": "git diff -- tools/chantier/plan.json | head -60", "description": "Inspect plan.json changes"}`

  ```
diff --git a/tools/chantier/plan.json b/tools/chantier/plan.json
index 7d2004b5..af52ed5c 100644
--- a/tools/chantier/plan.json
+++ b/tools/chantier/plan.json
@@ -418,6 +418,127 @@
      "attendu": "REVUE-0"
     }
    ]
+  },
+  {
+   "id": "C1",
+   "jour": 15,
+   "titre": "Coordination N2 — la commande validée",
+   "mandat": "Tâche C1 : la coordination N2, suite de J4.1 — écris `reports/rapport-coordination-n2-v2.md` + JSON : la commande **validée** `python3 work/n2ac/eval_longueurs.py --rope --canal-dir <dir>` (le correctif mesuré 2,79), la commande à ne PAS utiliser (`--rope` seul : 40,07), le test de non-régression proposé (`porte-n2.sh` : la porte à 3,09 doit rester à 3,09), et la mise à jour de la ligne N2 de `docs/pilotage/en-cours.md`. **Ne modifie rien dans `tools/n2/` ni `work/n2ac/`.**",
+   "budget_min": 90,
+   "acceptation": [
+    {
+     "commande": "test -f reports/rapport-coordination-n2-v2.md && echo FICHE-OK",
+     "attendu": "FICHE-OK"
+    }
+   ]
+  },
+  {
+   "id": "C2",
+   "jour": 15,
+   "titre": "Coordination S — la page / et la v7",
+   "mandat": "Tâche C2 : la coordination S, suite de J4.2 — écris `reports/rapport-coordination-s-v2.md` + JSON : l
… [1773 caractères tronqués]
  ```

- **bash** `{"command": "git diff -- docs/pilotage/roadmap.md | head -40", "description": "Inspect roadmap changes"}`

  ```
diff --git a/docs/pilotage/roadmap.md b/docs/pilotage/roadmap.md
index 8f9d4f12..07119bf7 100644
--- a/docs/pilotage/roadmap.md
+++ b/docs/pilotage/roadmap.md
@@ -35,13 +35,13 @@
 | **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 langues à 0,9687**, script 1,0000 ; analyse heuristique (5 schémas) ; **contrat de substitution écrit** ([`contrat-bloc-langue.md`](../theorie/contrat-bloc-langue.md)) ; **frontière : script 1,0, langue 0,137 (libellés) / 0,9687 (texte long)** ; **porte des quatre modes : neuronal 0,9309/0,8226/0,8784 ; fusion 0,928/0,802/0,857** ; **fusion réparée par niveau : 0,9309/0,8226/0,8784/0,9954 (le max)** ([fiche](../../reports/rapport-pensee-fusion-reparee.md)) ; **corpus commun UDHR : 21 textes, 418/438 paires exactes (95,4 %), 20 écarts exclus** ([fiche](../../reports/rapport-corpus-commun.md)) ; **J3.1 retrieval à époque contrôlée : l'écriture domine (+0,609), l'époque ne pèse pas à écriture contrôlée (−0,034/siècle, p=0,19), le brut est un effet de composition (0,238 vs 0,427)** ([fiche](../../reports/rapport-retrieval-epoque.md)) ; **J3.2 
… [6519 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '50,75p' docs/pilotage/roadmap.md", "description": "Read roadmap day-15 section"}`

  ```
**J10.1 — le bilan du chantier.** **20 tâches sur 21** passent l'acceptation ; **5 timeouts**
(J1.2, J2.2, J3.1, J5.2, J8.1), dont **4 récupérés** par une acceptation verte ou le commit de la
tâche suivante, et **1 vrai échec** (J5.2, le tag absent). Le produit gagne **2 attachements**
(236 → 238 labels) et **+0,0369 de F1** (0,7533 → 0,7902), la POS ne bouge pas ; Panini est
**mesuré et borné** (table 14/14, corpus 418/438, retrieval J3.1, généalogie J3.2, familles
J7.1) ; la coordination N2/S/R/A est **datée**. La **clôture formelle** est faite en **J14.1** : sans refaire la passe, les trois rouges sont revérifiées et le tag `chantier-2026-11-14` est posé sur le dernier commit vert. Le détail — chiffres, décisions
D1–D20, rejets R1–R30, échecs, reste — est dans
[`rapport-bilan-chantier.md`](../../reports/rapport-bilan-chantier.md) + JSON.

**J11.1 — les exemples rejoués.** Les **5 blocs** de `docs/produit/exemples.md` sont reproduits
avec le code courant ; **4 sont corrigés** : la ponctuation finale entre dans le POS (`g001`,
`r241`), le refus sort en **3** et `r035` — l'ancien échec connu — rend exactement le gold
(`REL [9:24] « she talks about » → film`). Le seul bloc identique
… [1082 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "new_string": "CEGEP **91 scans uniques**, 1 982 p). **Passe** : 84 portes, **81/3**, 1 h 30 (00 h 30) ; les rouges tolérées sont `indice` et `melange` (structurelles), `sessions` est revérifiée verte ; compteu … [273 caractères tronqués]`

  ```
Error: cannot modify "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md": file has not been read — read the file, then retry
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "limit": 80}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md</path>
<type>file</type>
<content>
1: # La roadmap de [Drave](../theorie/glossaire/entrees/drave.md) — un seul plan, quatre chantiers
2: 
3: > **Un seul document de plan.** Le **moteur** (A), l'**intelligence** (B), le **natif** (N) et le **lecteur** (R).
4: > L'ordre se décide par la **valeur** et les **dépendances**, jamais par une date. Les chiffres, les séries et les
5: > contrôles vivent dans [`reports/`](../../reports/) ; ici : l'[état](../theorie/glossaire/entrees/etat.md), la prochaine action, et ce qui bloque.
6: >
7: > **Détail et histoire** : l'ancien plan [A/B](../theorie/glossaire/entrees/a-b.md) est archivé dans
8: > [`roadmap-detail-2026-10-29.md`](../archive/roadmap-detail-2026-10-29.md), le détail N dans
9: > [`roadmap-native-2026-10-29.md`](../archive/roadmap-native-2026-10-29.md). Les **fiches de fonctionnalité** sont
10: > dans [`backlog/index.md`](backlog/index.md) ; le **graphe des dépendances** est dans
11: > [`backlog/dependances.md`](backlog/dependances.md). La **page vivante** est [`en-cours.md`](en-cours.md).
12: 
13: ## Comment lire cette roadmap
14: 
15: - **Les états** : ✅ m
… [15497 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md", "new_string": "CEGEP **91 scans uniques**, 1 982 p). **Passe** : 84 portes, **81/3**, 1 h 30 (00 h 30) ; les rouges tolérées sont `indice` et `melange` (structurelles), `sessions` est revérifiée verte ; compteu … [273 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/roadmap.md has been updated successfully.
  ```

- **bash** `{"command": "git diff --check; echo \"exit=$?\"; python3 -m py_compile tools/verifier_faq.py tools/restitution_v2.py tools/mesurer_restitution_v2.py; echo \"compile=$?\"", "description": "Check whitespace and compile"}`

  ```
journal/sessions/session-e73a3601-e2c6-417c-a009-88ffadca4e61/digest.md:2883: new blank line at EOF.
exit=2
compile=0
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | grep -E \"T0 max|roadmap.md|violation|✅|❌\" | tail -8; echo \"exit=${PIPESTATUS[0]}\"", "description": "Check budgets after roadmap edit"}`

  ```
9000    493   T1   9000  docs/pilotage/roadmap.md
  T0 max : 4000 mots (budget 4 000)
  ✅ tous les documents chargeables sont dans leur budget et ont un résumé.
exit=0
  ```

- **bash** `{"command": "bash tools/porte-tableaux.sh 2>&1 | tail -4; echo \"exit=${PIPESTATUS[0]}\"", "description": "Re-run table gate"}`

  ```
✅ 1817 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4433 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-15)
exit=0
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py 2>&1 | tail -4; echo \"exit=${PIPESTATUS[0]}\"", "description": "Re-run docs review"}`

  ```
revue de documentation · 745 fiche(s) · 839 JSON · 123 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
exit=0
  ```

- **bash** `{"command": "python3 tools/verifier_faq.py | tail -2; echo \"exit=${PIPESTATUS[0]}\"", "description": "Final FAQ verifier run"}`

  ```
✅ 10. Comment l'installer et le lancer ?
✅ FAQ vérifiée
exit=0
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-15/mesures.md", "offset": 35, "limit": 40}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-15/mesures.md</path>
<type>file</type>
<content>
35: - [reports/rapport-cic-v2.md](../../reports/rapport-cic-v2.md)
36: - [reports/rapport-coordination-n2-v2.md](../../reports/rapport-coordination-n2-v2.md)
37: - [reports/rapport-exemples-tagger.md](../../reports/rapport-exemples-tagger.md)
38: - [reports/rapport-tagger-option.md](../../reports/rapport-tagger-option.md)
39: 
40: <!-- notes -->
41: 
42: ### D2 — la restitution v2 : les rôles se lisent, leur fidélité ne suit pas
43: 
44: La v2 devait passer de la surface (v0) et de la forme canonique (v1) aux **rôles**. Elle le fait
45: comme **forme** : `restituer --roles` rend un cadre `agent / prédicat / lieu`, 198 segments de rôle,
46: **198/198** spans dans la source, et `relire_roles(rendre_roles(a))` redonne le cadre **46/46**.
47: Mais la **fidélité** ne suit pas. Sur un or écrit à la main (46 cadres, 65 variantes), **19/46**
48: cadres sont exacts — **16/46** non vides —, **91/138** cellules exactes, mais **F1 0,5270**
49: (précision 0,5493, rappel 0,5065, **32 faux positifs / 38 faux négatifs**) ; **agent 0,6000**,
50: **prédicat 0,4872**, **lieu 0,4000**
… [632 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-15/mesures.md", "new_string": "[`fiche`](../../reports/rapport-restitution-v2.md) · [`JSON`](../../reports/pensee-restitution-v2.json).\n\n### D3 — la FAQ : dix questions, dix réponses vérifiées\n\nLa notice produit gagne … [1016 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-15/mesures.md has been updated successfully.
  ```

- **bash** `{"command": "git add docs/produit/README.md docs/pilotage/en-cours.md docs/pilotage/roadmap.md \\\n  reports/rapport-faq.md reports/faq.json tools/verifier_faq.py \\\n  reports/rapport-restitution-v2.md reports/pensee-restitution-v2.json \\\n  tools/restitution_v2.py tools/mesurer_restitution_v2.py  … [213 caractères tronqués]`

  ```
M  docs/pilotage/en-cours.md
M  docs/pilotage/roadmap.md
M  docs/produit/README.md
 M journal/2026-11-15/mesures.md
 M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md
 M journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md
 M journal/sessions/session-e73a3601-e2c6-417c-a009-88ffadca4e61/digest.md
 M journal/sessions/session-e73a3601-e2c6-417c-a009-88ffadca4e61/rapport.md
 M reports/INDEX.md
 M reports/README.md
A  reports/faq.json
 M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
A  reports/pensee-restitution-v2.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
A  reports/rapport-faq.md
 M reports/rapport-pensee-v12.md
A  reports/rapport-restitution-v2.md
 M reports/rapport-spans-chunker.md
 M tools/chantier/plan.json
M  tools/drave.py
A  tools/mesurer_restitution_v2.py
M  tools/porte-produit.sh
A  tools/restitution_v2.py
A  tools/tests/linguistique/gold_restitution_v2.json
A  tools/tests/test_restitution_v2.py
A  tools/verifier_faq.py
?? journal/sessions/session-53896e61-4a68
… [176 caractères tronqués]
  ```

- **bash** `{"command": "git diff --cached --check; echo \"check=$?\"; python3 tools/verifie_etat_a_jour.py --index; echo \"etat=$?\"", "description": "Check staged diff and state hook"}`

  ```
check=0
  ✅ index : aucun fait stagé sans état
etat=0
  ```

- **bash** `{"command": "git commit -m \"D3 — LA FAQ DU PRODUIT : 10/10 RÉPONSES VÉRIFIÉES CONTRE LE CODE (10 CONTRÔLES, NÉGATIF DÉTECTÉ) ; D2 — LA RESTITUTION V2 (19/46 CADRES, F1 0,5270)\" -m \"- FAQ §8 de docs/produit/README.md : langue, hors-ligne, coût, tagger, schéma, attachement, g017, restitution v0/v1/ … [486 caractères tronqués]`
