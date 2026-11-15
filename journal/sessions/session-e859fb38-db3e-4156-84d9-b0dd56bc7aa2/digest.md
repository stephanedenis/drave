# Session DSH — relecture

- identifiant : `session-e859fb38-db3e-4156-84d9-b0dd56bc7aa2`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-15 07:43:11
- agent : None


## Tour 1

### 👤 Utilisateur

Tâche F1 : le plan de la **semaine 2** (16 → 22/11) — lis le bilan de la semaine (`reports/rapport-bilan-semaine.md`), `docs/pilotage/en-cours.md` et les fiches des tâches C/B/D/E, puis écris `docs/pilotage/semaine-2.md` (120 lignes max) : les 5 jours × 2 vagues, les tâches par jour (le gold réel 452 à annoter, la page `/` de S, le corpus à date contrôlée de Panini, la restitution v3, le tagger par défaut ?), les dépendances, les risques, les livrables. **Ne modifie pas `semaine-autonome.md`** (le plan de la semaine 1, qui reste l'archive).

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

- **bash** `{"command": "pwd && ls && git status --short | head -50 && git log --oneline -5", "description": "Inspect repository root and git state"}`

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
?? tools/tests/linguistique/gold_reel_50.py
49011807 ÉTAT — T0 VERT (LA LIGNE FAIT NETTOYÉE, COQUILLE CORRIGÉE)
2b7e520b ÉTAT — T0 VERT
cf2d1fb1 ÉTAT — T0 DANS LE BUDGET
cd4d1060 FINITION — E1-E2 (LA FAQ AU SOMMAIRE, LES CAS D'ERREUR DU TAGGER) ; LE PLAN ET LE JOURNAL À JOUR
7ee92dd9 JOURNAL — 2026-11-15 : E2, LES CAS D'ERREUR DU TAGGER (REFUS D'AUTHENTIFICATION → CODE 4, RÉSEAU ET RÉPONSE NON CONFORME → REPLI 0 ; 18/18)
  ```

- **bash** `{"command": "ls docs/pilotage/ reports/ 2>/dev/null | head -80", "description": "List pilotage and reports directories"}`

  ```
docs/pilotage/:
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

reports/:
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
atomes-niveaux.json
atomes-prediction.json
atomes-prediction-mesures.json
b102bis-capacite.json
b102bis-corpus-jw.json
b102bis-decodeur.json
b10-decodeu
… [324 caractères tronqués]
  ```

- **bash** `{"command": "ls reports/ | grep -i -E \"bilan|semaine|panini|gold|tagger|restitution\" | head -60; echo ---; ls docs/pilotage/backlog/ 2>/dev/null | head -40", "description": "Locate week report and task sheets"}`

  ```
a26-bilan.json
bilan-b11.md
bilan-multi-materiel.md
note-panini-334.md
panini-334.json
pensee-anaphore-bilan.json
pensee-bilan-nuit.json
pensee-gold-200.json
pensee-gold-342.json
pensee-gold-anglais.json
pensee-gold-cascade-200.json
pensee-gold-cascade.json
pensee-gold-complexes100.json
pensee-gold-complexes20.json
pensee-gold-complexes50.json
pensee-gold-complexes.json
pensee-gold-discours.json
pensee-gold-gele.json
pensee-gold-gp-corrige.json
pensee-gold-linguistique.json
pensee-gold-neuronal.json
pensee-gold-pragmatique.json
pensee-gold-reel-cascade.json
pensee-gold-split.json
pensee-gold-subsets.json
pensee-gold-syntagmes.json
pensee-inventaire-panini.json
pensee-restitution-v0.json
pensee-restitution-v1.json
pensee-restitution-v2.json
pensee-robustesse-semaine.json
pensee-tagger-option.json
rapport-a26-bilan.md
rapport-bilan-chantier.json
rapport-bilan-chantier.md
rapport-bilan-nuit.md
rapport-bilan-semaine.md
rapport-exemples-tagger.json
rapport-exemples-tagger.md
rapport-gold-anglais.md
rapport-gold-gp-corrige.md
rapport-gold-reel-50.json
rapport-gold-reel-50.md
rapport-gold-split.md
rapport-inventaire-panini.md
rapport-panini-334.md
rapport-pensee-anaphore-bilan.md
rapport-
… [1292 caractères tronqués]
  ```

- **bash** `{"command": "wc -l docs/pilotage/en-cours.md docs/pilotage/semaine-autonome.md reports/rapport-bilan-semaine.md 2>&1", "description": "Check sizes of core files"}`

  ```
147 docs/pilotage/en-cours.md
  288 docs/pilotage/semaine-autonome.md
   91 reports/rapport-bilan-semaine.md
  526 total
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-semaine.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-bilan-semaine.md</path>
<type>file</type>
<content>
1: # Le bilan de la semaine (07 → 15/11) — le produit gagne 3,7 points, Panini est borné, le harnais tient
2: 
3: > **Ce que ce bilan est.** La **synthèse de la semaine** : le produit, Panini, la coordination, le
4: > méta-harnais. **Aucune mesure nouvelle** : chaque chiffre renvoie à sa fiche. Il est écrit pour
5: > être lu en 5 minutes, pas pour remplacer les fiches.
6: 
7: ## 1. Le produit — les chiffres, avec leur base
8: 
9: | mesure | avant (07/11) | **après (15/11)** | base |
10: |---|---:|---:|---|
11: | **F1 syntagmes** | 0,7533 | **0,7902** (+3,69) | vivant 612 |
12: | F1 syntagmes (réel) | — | **0,7906** | réel 452 |
13: | **POS** | 0,8625 | 0,8625 | vivant 612 |
14: | POS (réel) | — | **0,8891** | réel 452 |
15: | POS avec `--tagger` | — | **0,9575** (612) · **0,9500** (réel) | API |
16: | **attachement exact** | 236/237 | **238/239** (0,9958) | vivant 612 |
17: | attachement (réel) | — | **99,46 %** | réel 452 |
18: | exact sur span | 1,0000 | **1,0000** | vivant 612 |
19: | spans perdus | 2 | **1** (`g017`, inatteignable) | vivant 612 |
20: 
21: **
… [4330 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
1: # En ce moment
2: 
3: **Mis à jour : 2026-11-15, 07 h 30 HNE (finition : E1-E2, le tagger et ses cas d'erreur)**
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
21: > [
… [12263 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-autonome.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-autonome.md</path>
<type>file</type>
<content>
1: # Le chantier autonome — une semaine (7 → 14 novembre 2026)
2: 
3: > **Ce que ce document est.** Le **plan du chantier d'une semaine** : tous les travaux ouverts du
4: > dépôt et l'**intégration avec l'écosystème Panini**. Il dit **quoi**, **dans quel ordre**, **avec
5: > quels sous-agents**, **comment on mesure**, et **ce qui peut faire échouer**. L'état courant est
6: > dans [`en-cours.md`](en-cours.md) ; la théorie de la généalogie dans
7: > [`../theorie/genealogie-des-langues.md`](../theorie/genealogie-des-langues.md) ; la méthode
8: > Panini/Nipada dans [`../methode/panini-nipada.md`](../methode/panini-nipada.md).
9: > *À relire chaque matin du chantier.*
10: >
11: > **Bilan J10.1 (14/11).** Le chantier est **mesuré et écrit** ; la **clôture formelle** (tag,
12: > release) reste à faire (J5.2, reprise par J14.1). Les chiffres avant/après, les décisions, les
13: > rejets et les échecs sont dans
14: > [`rapport-bilan-chantier.md`](../../reports/rapport-bilan-chantier.md) + JSON ; l'état courant
15: > est dans [`en-cours.md`](en-cours.md).
16: 
17: ## 1. L
… [22577 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn -i -E \"t[âa]che [CBE D][0-9]?|gold r[ée]el|452|semaine 2|semaine-2\" docs/pilotage/ journal/ --include=*.md | head -80", "description": "Search for task C/B/D/E references"}`

  ```
docs/pilotage/backlog/R31-restitution-sft.md:10:La PPL ne prouve pas la lecture. Le SFT actuel mémorise (24/24 vus, 0/4 tenus). Il faut une tâche de restitution avec un partage par document, pas par exemple.
docs/pilotage/README.md:22:| 5 | [`programme-r.md`](programme-r.md) | le **lecteur** (R0–R5), ses phases et ses lois | pour une tâche du programme R |
docs/pilotage/plan-travail.md:362:| session | territoire | tâche de la nuit | ressource | livrable | arrêt |
docs/pilotage/chantiers.md:225:| une **tâche bornée** (une mesure, un outil, une fiche, un audit) | **sous-agent** (2 à 4, AGENTS § 10) | il rend un diff, la session intègre et commite ; il ne touche ni `en-cours` ni la roadmap |
docs/pilotage/semaine-autonome.md:281:| C3 **R** | ✅ | le « gold 200+ » **défini** (452 phrases), 50 ratées sélectionnées |
docs/pilotage/en-cours.md:121:| **B — l'intelligence** | **B13** | B1.5 corpus ; B10.3 attend un encodeur ; **B13 : 183/183, F1 0,7902, 238/239, schéma v2, restit v1, produit (J11)** | **`g017` tranché** ; T132/T133, gold 452 ; **B10.3 bloquée** |
docs/pilotage/en-cours.md:123:| **R — le lecteur** | **R0.7** | **R0.7 — tagger 612 : 0,9575 (+9,5) ; réel 452 : 0,9500 (+6,1)** ;
… [19617 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn -i \"semaine-2\\|semaine 2\\|16/11\\|17/11\\|18/11\\|19/11\\|20/11\\|21/11\\|22/11\" --include=*.md --include=*.json --include=*.txt docs reports journal tools 2>/dev/null | grep -v \"digest.md\" | head -60", "description": "Search for week 2 references"}`

  ```
docs/pilotage/roadmap.md:156:commit vert `0e75f101` (J13.1) ; le tag de semaine `semaine-2026-11-14` (J5.2, resté en échec) est
reports/07/p9.md:61:* **LE PLAN FIGÉ EST FAIBLE** ✓✗ : 0,20-0,22 in-langue, cohérent avec les mesures 116/119 (~0,2) ✓✗ ;
reports/rapport-pensee-segmenteur-defaut.md:4:> **116/116 portes** : l'**union** des segmenteurs entre dans l'**analyseur par défaut**
reports/rapport-pensee-segmenteur-defaut.md:55:- [`autotest.py`](../tools/pensee/autotest.py) — T113, 116/116.
reports/pensee-segmenteur-defaut.json:4: "portes": "116/116",
reports/rapport-pensee-cascade-union.md:4:> **117/117 portes** : la **cascade** (heuristique + mock neuronal) est mesurée avec l'union :
reports/rapport-pensee-cascade-union.md:61:- [`autotest.py`](../tools/pensee/autotest.py) — T114, 117/117.
reports/pensee-cascade-union.json:4: "portes": "117/117",
reports/rapport-pensee-cascade-tete.md:4:> **118/118 portes** : la correction « garder la tête de l'union quand le mock ajoute un
reports/rapport-pensee-cascade-tete.md:56:- [`autotest.py`](../tools/pensee/autotest.py) — T115, 118/118.
reports/pensee-cascade-tete.json:4: "portes": "118/118",
reports/rapport-pensee-miroir.md:4:> · **Verdic
… [7439 caractères tronqués]
  ```

- **bash** `{"command": "ls journal/ | tail -20; echo ---; ls docs/pilotage/backlog/ | head -60; echo ---; grep -rn \"C1\\|C2\\|C3\\|D1\\|D2\\|D3\\|E1\\|E2\" journal/sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/plan.md 2>/dev/null | head -40", "description": "List journal and session plan references"}`

  ```
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
---
A2.6-ordonnanceur.md
A3.2-granularite.md
A3.3-seuil.md
A3.4-colab.md
A5.4-fpga.md
A6.2-moe-local.md
A8.0-portes-ppl.md
A8.3-defaut.md
B10.2bis-decodeur-attention-croisee.md
B10.3-raisonnement-z.md
B11.10-cartes-ambiguites.md
B12.10-pipeline-m1-m4-m8.md
B1.5-prose-scientifique.md
dependances.md
index.md
_modele.md
N0.3b-parite-ppl.md
N2-distillation.md
N3-operations-natives.md
N4-usage-sft.md
R01-graphe-document.md
R02-controleur-lecture.md
R03-banc-lecture-rapide.md
R04-tete-survol.md
R05-tete-balayage.md
R06-tete-relecture.md
R07-routeur-extractif-generatif.md
R11-contexte-hierarchique.md
R12-curriculum-contexte.md
R13-tokenisation-bpe.md
R21-memoire-travail-gist.md
R22-memoire-episodique.md
R31-restitution-sft.md
R32-citations-provenance.md
R41-bloc-tableaux.md
R42-bloc-code.md
R43-bloc-maths.md
R44-encodeur-visuel.md
R51-lecture-croisee.md
R52-multilingue-decodeur.md
---
  ```

- **bash** `{"command": "ls journal/2026-11-15/ journal/2026-11-14/ 2>/dev/null; echo ---; grep -rn -E \"\\b(C1|C2|C3|B1|B2|B3|D1|D2|D3|E1|E2)\\b\" journal/2026-11-15/ journal/2026-11-14/ 2>/dev/null | head -60", "description": "Inspect journal entries for task letters"}`

  ```
journal/2026-11-14/:
distribue.md
docs.md
memoire.md
mesures.md
moteur.md
portes.md
README.md

journal/2026-11-15/:
distribue.md
docs.md
mesures.md
modele.md
outils.md
portes.md
README.md
---
journal/2026-11-15/distribue.md:11:| 02:27 | `f926b5bc` | C2 — LA PAGE / NE SERT PAS LA V7 : 369 CANDIDATS SANS PROFONDEUR, 41 VERDICTS À RE-JUGER ; PORT 8765 PRIS, PARE-FEU ACTIF ; LES 11 VERDICTS COMMITTÉS (389b99f) | `en-cours.md`, `roadmap.md`, `README.md` (+17) |
journal/2026-11-15/distribue.md:12:| 03:04 | `c37fed06` | B1 — LE PROTOCOLE À DATE CONTRÔLÉE GELÉ : 60 PAIRES (20/20/20), 59 TEXTES, 26 À SIGNER ; LE §334 N'EN FOURNIT QU'UNE DÉJÀ SIGNÉE | `en-cours.md`, `README.md`, `distribue.md` (+16) |
journal/2026-11-15/distribue.md:14:| 06:31 | `7d4e3bc5` | E1 — LA FAQ AU SOMMAIRE ET SES LIENS : 9/9 ANCRES, 5/5 LIENS, 0 MORT ; LA LIGNE FAQ DANS docs/README, LES RÉPONSES INCHANGÉES | `README.md`, `en-cours.md`, `README.md` (+17) |
journal/2026-11-15/README.md:35:| 02:13 | `292c70b5` | C1 — LA COMMANDE N2 VALIDÉE : --rope + canal (2,7856), JAMAIS --rope SEUL (40,0658), TÉMOIN 3,09 |
journal/2026-11-15/README.md:36:| 02:27 | `f926b5bc` | C2 — LA PAGE / NE SERT PAS LA V7 : 369 CANDIDATS SANS PR
… [5807 caractères tronqués]
  ```

- **bash** `{"command": "ls reports/ | grep -E \"coordination|protocole|restitution|faq|tagger|atomes-prediction|cic-v2|gold-reel\" ", "description": "List candidate task reports"}`

  ```
atomes-prediction.json
atomes-prediction-mesures.json
faq.json
faq-sommaire.json
pensee-gold-reel-cascade.json
pensee-restitution-v0.json
pensee-restitution-v1.json
pensee-restitution-v2.json
pensee-tagger-option.json
protocole-date.json
rapport-atomes-prediction.md
rapport-cic-v2.md
rapport-coordination-a.json
rapport-coordination-a.md
rapport-coordination-n2.json
rapport-coordination-n2.md
rapport-coordination-n2-v2.json
rapport-coordination-n2-v2.md
rapport-coordination-r.json
rapport-coordination-r.md
rapport-coordination-s.json
rapport-coordination-s.md
rapport-coordination-s-v2.json
rapport-coordination-s-v2.md
rapport-exemples-tagger.json
rapport-exemples-tagger.md
rapport-faq.md
rapport-faq-sommaire.md
rapport-gold-reel-50.json
rapport-gold-reel-50.md
rapport-pensee-seuils-gold-reel.md
rapport-protocole-date.md
rapport-restitution.md
rapport-restitution-v0.md
rapport-restitution-v1.md
rapport-restitution-v2.md
rapport-tagger-erreurs.json
rapport-tagger-erreurs.md
rapport-tagger-option.md
restitution-fra-flux.json
restitution-fra.json
restitution.json
restitution-mesures.json
restitution-udhr-flux.json
restitution-udhr.json
tagger-612.json
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-15/README.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/2026-11-15/README.md</path>
<type>file</type>
<content>
1: # 2026-11-15
2: 
3: > **Généré** par `tools/journal_auto.py` — index de la journée, dans le dossier
4: > [`journal/2026-11-15/`](README.md). Le récit écrit à la main est conservé plus bas, dans
5: > le bloc « notes » (marqueurs HTML). Retour : [l'index du journal](../README.md) ·
6: > [l'index des sessions](../README.md#sessions).
7: 
8: **24 commits** · **1 session(s)** · **6 thème(s)**
9: 
10: ## Thèmes du jour
11: 
12: | thème | commits | fichier |
13: |---|---|---|
14: | distribue | 5 | [distribue.md](distribue.md) |
15: | docs | 5 | [docs.md](docs.md) |
16: | mesures | 10 | [mesures.md](mesures.md) |
17: | modele | 2 | [modele.md](modele.md) |
18: | outils | 1 | [outils.md](outils.md) |
19: | portes | 1 | [portes.md](portes.md) |
20: 
21: ## Sessions DSH
22: 
23: | session | titre | début | durée | liens |
24: |---|---|---|---|---|
25: | `e181ce02-cd50-488a-a6be-e84b79d40dcc` | Documentation Drave avec diagrammes et implémentation | 2026-10-31 17:40 | 350.9 h | [rapport](../sessions/e181ce02-cd50-488a-a6be-e84b79d40dcc/rapport.md) · [digest](../sessions/e181
… [7100 caractères tronqués]
  ```

- **bash** `{"command": "grep -n -i -E \"C3|gold|452|D2|D3|E2|restitution|Panini|semaine|vague\" docs/pilotage/plan-travail.md | head -80", "description": "Search plan-travail for relevant lines"}`

  ```
39:| **L/B13 — Pensée (session `e181ce02`)** | le bloc langue (contrat heuristique + neuronal), la cascade, la pragmatique ; B13 | L, B13, la couche heuristique | **CPU**, 2–8 cœurs | **166/166** (6 S fixés ; T132/T133 2/5), gold **432**, 116 liens ; **gold neuronal** (POS **0,9415** / syntagmes **0,7539** / acte **1,0**) ; **DRVM/native** règle (**3 nœuds**) ; **DRVM N0.1 6/6** ; **pragmatique 130 : 1,0 / 1,0 / 0,9846 / 0,9769** — elle qualifie ; **gold 432 : acte 0,9954** ; **fusion par sous-type : le double sens 0,9884 (+0,0208) ; variance du sous-type : 0,9838 ; tirages : 0,9838 ×3 (déterministe sur ces invites) ; attachement : top1 0,3431, exact 0,0042 ; cibles : 1863 segments, 1624 sans cible (87,2 %), couverture réelle 0,1283 ; cibles 500 : 294 GN / 206 GV ; relation GN → GV : 221/637 ; rôles par position : 301/322, relation 0,8195 (522/637) surévaluée ; correctif `par` → agent (partiel : le générateur S garde `moyen`) ; sans `par` : le chunker 3/3, le générateur S ignore ; cible par proximité : exact 0,0042 → 0,0544 ; candidats verbes : top-k 0,4686, tête 0,7655 ; échecs qualifiés : 127 = 94 span + 33 cible** (négation/modalité sous l'heuristique). Prochaine : **T132/T133**
… [3754 caractères tronqués]
  ```

- **bash** `{"command": "for f in reports/rapport-coordination-r.md reports/rapport-coordination-r-v2.md reports/rapport-gold-reel-50.md reports/rapport-coordination-s-v2.md reports/rapport-protocole-date.md reports/rapport-restitution-v2.md reports/rapport-exemples-tagger.md reports/rapport-tagger-erreurs.md r … [177 caractères tronqués]`

  ```
===== reports/rapport-coordination-r.md (401 l.)
# R — le tagger POS sur le gold 612 : **+8,49 pts**, la règle dit **intégrer**

> **Ligne de roadmap** : **R0.7** (le bloc linguistique) · **Date** : 2026-11-13 · **HEAD mesuré** :
> `ced21933` · **Verdict** : le tagger POS par **API DeepSeek** mesure **0,9475** (**3012/3179**)
> sur le gold **612**, contre **0,8625** (**2742/3179**) pour l'heuristique du HEAD : **+8,49 pts**,
> IC95 bootstrap par phrase **[+7,23 ; +9,74]**, McNemar **344/74**, **p = 1,1 × 10⁻⁴²**. La règle
> de décision (**≥ +5 pts → intégrer**) donne : **intégrer via l'API**, jamais le 7B local
> (règle 11). La prémisse « clé absente » est **fausse** : la clé est dans
> `~/.config/drave/deepseek.key` (0600) et l'API répond **200** ; c'est `DEEPSEEK_API_KEY` qui
> manque. Coût mesuré : **1 218 appels, 358 962 tokens, 21 min**, **~0,04 $** hors pointe.

**En trois lignes.** (1) La mesure est **réelle**, faite le 2026-11-13 avec un **cache neuf** :
`deepseek-chat` est servi par `deepseek-flash` (DeepSeek-V4.1-Flash-1017), 1 218 appels,
358 962 tokens, 20 min 59 s, **0 refus POS**. (2) La baseline publiée **0,8500** est **datée** :
elle reproduit exactement au commit `
… [19426 caractères tronqués]
  ```

- **bash** `{"command": "echo \"===== C2 tail\"; tail -90 reports/rapport-coordination-s-v2.md; echo; echo \"===== C3 tail\"; tail -100 reports/rapport-gold-reel-50.md", "description": "Read conclusions of C2 and C3"}`

  ```
===== C2 tail

```bash
PYTHONDONTWRITEBYTECODE=1 python3 serveur.py --hote 0.0.0.0 --port 9000
```

Voir § 5.3 pour le pare-feu et le tunnel. Le serveur imprime
`banc de structures · http://0.0.0.0:9000 · 207 phrases` ; l'URL réelle est
`http://192.168.1.101:9000/` (ou `.155`).

## 7. Ce qui reste à S

| # | chantier | état mesuré | prochaine action |
|---:|---|---|---|
| 1 | **Page `/` en v7** (A1) | `work/banque-v7/` **absent** ; `phrases_generees.json` du **02/11** (200 phrases / 355 candidats, 0 `profondeur`) ; `app.js` lit `niveau` | décider : **garder l'ancien banc** ou **régénérer** ; si régénération, signature + **106 conservés** + **41 en quarantaine** ; ne pas migrer par index |
| 2 | **Référents** (A2) | **9/16** mappings uniques faux (12/28 occurrences), **0 note** ; a008 = 0/5 | corriger les 14 occurrences / 12 formes, avec note ; forcer la résolution avant le verdict |
| 3 | **Rétro-traduction** (A3) | **0/9**, aucun harnais FR→EN→FR ; `DEEPSEEK_API_KEY` et `DEEPSEEK_KEY_FILE` **absents de l'env** ; fichier `~/.config/drave/deepseek.key` **présent** (36 o, 0600, 03/11), **non testé** | écrire `work/retro-traduction/` (9 prompts, 18 appels), passer la clé par `DEEPSEEK
… [12129 caractères tronqués]
  ```

- **bash** `{"command": "echo \"===== B1 tail\"; tail -80 reports/rapport-protocole-date.md; echo; echo \"===== D2 tail\"; tail -80 reports/rapport-restitution-v2.md", "description": "Read conclusions of B1 and D2"}`

  ```
===== B1 tail
  --panini /chemin/vers/Panini \
  --signatures /tmp/v14.json \
  --sortie /tmp/protocole-resultats.json
```

Le fichier de signatures attendu est un JSON de la forme :

```json
{
  "instrument": "V14 — extracteur du commit e10d695e (ou successeur compatible)",
  "commit": "…",
  "signatures": {
    "baudhayana_dharmasutra": {"ÊTRE": 0.12, "DIFFÉRENCE": 0.03, "...": 0.0},
    "...": {"...": 0.0}
  }
}
```

Les 14 clés doivent être exactement celles de la liste ; chaque signature doit sommer à 1 ± 10⁻⁶.
Le script calcule `d_sig`, décrit les 60 paires, puis exécute P1/P2 et le contrôle positif G1
**seulement si les 60 paires sont complètes**. Sinon il écrit `statut: incomplet`, la liste des
paires manquantes et les statistiques descriptives du noyau — sans p-value, pour ne pas faire croire
à un test sur un sous-ensemble choisi par la disponibilité.

**Ce que Panini doit faire, concrètement.** Signer les **26 textes** listés dans
`protocole-date.json` → `a_signer`, avec **le même** extracteur V14 que `analytic_sigs_v1.json`, et
fournir le JSON ci-dessus. Les 26 sources sont toutes acquises (`ok = true`) ; aucune ne demande une
nouvelle acquisition. La calibration sur les
… [9087 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn -i -E \"tagger.*d[ée]faut|d[ée]faut.*tagger|par d[ée]faut\" reports/rapport-tagger-option.md reports/rapport-tagger-erreurs.md reports/rapport-exemples-tagger.md docs/produit/*.md docs/pilotage/roadmap.md 2>/dev/null | head -40", "description": "Search tagger-default decision c … [8 caractères tronqués]`

  ```
reports/rapport-tagger-option.md:1:# R0.7 / 1A — le tagger POS en option : +8,57 pts sur 20 phrases, +8,49 sur le gold 612 ; le défaut reste hors ligne
reports/rapport-tagger-option.md:112:- **Le défaut est inchangé** : `drave analyser "Le chat dort." --json` sans `--tagger` rend
reports/rapport-tagger-option.md:152:  « hors ligne par défaut ».
reports/rapport-tagger-erreurs.md:22:| **clé invalide** (HTTP 401/403) | refuse de démarrer, **sans repli** | **4** | vide (0 octet) | `drave: dépendance absente : clé DeepSeek refusée (HTTP 401) : vérifiez DEEPSEEK_KEY_FILE, ~/.config/drave/deepseek.key ou DEEPSEEK_API_KEY. Sans --tagger, le défaut reste l'heuristique hors ligne.` | `TestErreursTagger.test_cle_invalide_code_4` |
reports/rapport-tagger-erreurs.md:112:| **défaut inchangé** | `analyser --json` sans `--tagger` | JSON **identique** à l'heuristique (`TestDefaultInchange.test_analyser_json_sans_tagger`) |
docs/produit/README.md:12:> § 3.7) : clé et réseau pour qui le demande, **heuristique hors ligne par défaut**. Le format
docs/produit/README.md:47:aucun accès réseau **par défaut** (le tagger en option, lui, appelle l'API DeepSeek, § 3.7). Les
docs/produit/README.md:422:| **clé i
… [1997 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,120p' docs/pilotage/roadmap.md", "description": "Read roadmap top"}`

  ```
# La roadmap de [Drave](../theorie/glossaire/entrees/drave.md) — un seul plan, quatre chantiers

> **Un seul document de plan.** Le **moteur** (A), l'**intelligence** (B), le **natif** (N) et le **lecteur** (R).
> L'ordre se décide par la **valeur** et les **dépendances**, jamais par une date. Les chiffres, les séries et les
> contrôles vivent dans [`reports/`](../../reports/) ; ici : l'[état](../theorie/glossaire/entrees/etat.md), la prochaine action, et ce qui bloque.
>
> **Détail et histoire** : l'ancien plan [A/B](../theorie/glossaire/entrees/a-b.md) est archivé dans
> [`roadmap-detail-2026-10-29.md`](../archive/roadmap-detail-2026-10-29.md), le détail N dans
> [`roadmap-native-2026-10-29.md`](../archive/roadmap-native-2026-10-29.md). Les **fiches de fonctionnalité** sont
> dans [`backlog/index.md`](backlog/index.md) ; le **graphe des dépendances** est dans
> [`backlog/dependances.md`](backlog/dependances.md). La **page vivante** est [`en-cours.md`](en-cours.md).

## Comment lire cette roadmap

- **Les états** : ✅ mesuré et écrit · 🔬 en cours · ⏳ à faire · 🧱 bloqué par une infra absente.
- **Le carpe diem** : pas d'échéance. Un chantier est **[fait](../theorie/glossaire/entrees
… [19669 caractères tronqués]
  ```

- **bash** `{"command": "ls -la tools/chantier/ 2>/dev/null | head; echo ---; python3 - <<'PY'\nimport json\np='tools/chantier/plan.json'\ntry:\n    d=json.load(open(p))\n    print(type(d))\n    print(json.dumps(d, ensure_ascii=False, indent=1)[:4000])\nexcept Exception as e:\n    print(e)\nPY", "description":  … [29 caractères tronqués]`

  ```
total 44
drwxr-xr-x. 1 stephane stephane    46 14 nov 06:25 .
drwxr-xr-x. 1 stephane stephane 18032 15 nov 06:37 ..
-rw-r--r--. 1 stephane stephane 25748 15 nov 07:43 plan.json
-rw-r--r--. 1 stephane stephane 13560 14 nov 04:14 superviseur.py
---
<class 'dict'>
{
 "nom": "Semaine 07/11 → 14/11 — le produit et l'intégration Panini",
 "principe": "Une tâche n'est finie que si son acceptation passe ; l'agent commite, le superviseur vérifie.",
 "taches": [
  {
   "id": "J0",
   "jour": 0,
   "titre": "Le contrôle du superviseur",
   "mandat": "Réponds exactement le mot OK, sans autre texte. C'est un test de liaison du superviseur.",
   "budget_min": 2,
   "acceptation": [
    {
     "commande": "python3 -c \"print('LIAISON-OK')\"",
     "attendu": "LIAISON-OK"
    }
   ]
  },
  {
   "id": "J1.1",
   "jour": 1,
   "titre": "r035 : la relative zéro",
   "mandat": "Tâche J1.1 du chantier : la relative zéro (r035, « The film she talks about is out. »). Reproduis, explique, propose UNE règle générale mesurée sur dev/test ; si elle tient (attachement 236→237, POS/F1 stables), intègre-la et commite avec une fiche `reports/rapport-r035.md` + `reports/pensee-r035.json`. Sinon, écris la fiche du
… [3062 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn -E \"Tâche C|Tâche B|Tâche D|Tâche E|tâche C|tâche D|tâche E|Gold réel 452|gold réel 452\" docs reports --include=*.md | head -40", "description": "Search exact task-sheet phrasing"}`

  ```
reports/rapport-coordination-n2-v2.md:40:Le plan de la tâche C1 a fusionné les deux en
reports/rapport-gold-reel-50.md:408:   ambigu (T15). Le remplacer par **« gold réel 452 »** + **« lot dur H50 »** + **« cibles 184 »**.
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('tools/chantier/plan.json'))\nfor t in d.get('taches',[]):\n    print(t['id'], '|', t.get('jour'), '|', t.get('titre'), '|', t.get('budget_min'))\nPY", "description": "List all plan task ids and titles"}`

  ```
J0 | 0 | Le contrôle du superviseur | 2
J1.1 | 1 | r035 : la relative zéro | 90
J1.2 | 1 | La convention des GV | 90
J1.3 | 1 | Le schéma v2 | 90
J1.4 | 1 | La restitution v0 | 90
J2.1 | 2 | Panini I — la table atomes ↔ niveaux | 90
J2.2 | 2 | Panini I — le corpus commun | 90
J3.1 | 3 | Panini II — le retrieval à époque contrôlée | 90
J3.2 | 3 | Panini II — la généalogie à deux faces | 90
J4.1 | 4 | Coordination N2 — le mètre RoPE | 90
J4.2 | 4 | Coordination S — les 11 verdicts | 90
J4.3 | 4 | Coordination R — le tagger sur 612 | 90
J4.4 | 4 | Coordination A — A6.2 et A8.3b2 | 90
J5.1 | 5 | Le rapport de semaine | 90
J5.2 | 5 | La passe complète et le tag | 90
J6.1 | 6 | Le dernier span g017 | 90
J6.2 | 6 | La cible s065 | 90
J7.1 | 7 | Panini — le retrieval approfondi | 90
J8.1 | 8 | La restitution v1 | 90
J9.1 | 9 | La passe d'honnêteté des fiches | 90
J10.1 | 10 | Le bilan de la semaine | 90
J11.1 | 11 | Le produit — les exemples rejoués | 90
J11.2 | 11 | Le produit — la mesure par langue | 90
J11.3 | 11 | Le produit — la robustesse des 50 textes | 90
J11.4 | 11 | Le contrat — le schéma v2 documenté | 90
J12.1 | 12 | Panini — le §334 et les 44 œuvres | 90
J12.2 | 12 | Panini — 
… [721 caractères tronqués]
  ```

- **bash** `{"command": "python3 - <<'PY'\nimport json\nd=json.load(open('tools/chantier/plan.json'))\nfor t in d['taches']:\n    if t['id']=='F1':\n        print(json.dumps(t, ensure_ascii=False, indent=2))\nPY", "description": "Print F1 task definition"}`

  ```
{
  "id": "F1",
  "jour": 16,
  "titre": "Le plan de la semaine 2",
  "mandat": "Tâche F1 : le plan de la **semaine 2** (16 → 22/11) — lis le bilan de la semaine (`reports/rapport-bilan-semaine.md`), `docs/pilotage/en-cours.md` et les fiches des tâches C/B/D/E, puis écris `docs/pilotage/semaine-2.md` (120 lignes max) : les 5 jours × 2 vagues, les tâches par jour (le gold réel 452 à annoter, la page `/` de S, le corpus à date contrôlée de Panini, la restitution v3, le tagger par défaut ?), les dépendances, les risques, les livrables. **Ne modifie pas `semaine-autonome.md`** (le plan de la semaine 1, qui reste l'archive).",
  "budget_min": 90,
  "acceptation": [
    {
      "commande": "test -f docs/pilotage/semaine-2.md && echo PLAN-OK",
      "attendu": "PLAN-OK"
    },
    {
      "commande": "python3 tools/revue_documentation.py >/dev/null 2>&1; echo REVUE-$?",
      "attendu": "REVUE-0"
    }
  ]
}
  ```

- **bash** `{"command": "git show --stat --oneline 4d6cffc4 | head -40; echo ---; git show 4d6cffc4 -- tools/chantier/plan.json | head -80", "description": "Inspect phase 4 plan commit"}`

  ```
4d6cffc4 PHASE 4 — D1-D3 (LES EXEMPLES DU TAGGER, LA RESTITUTION v2, LA FAQ 10/10) ; L'INDEX, LA FICHE C3 ORPHELINE (GOLD RÉEL 50) ET LE PLAN COMMITTÉS
 docs/pilotage/en-cours.md                          |    2 +-
 journal/2026-11-15/README.md                       |    7 +-
 journal/2026-11-15/distribue.md                    |    2 +-
 journal/2026-11-15/docs.md                         |    2 +-
 journal/2026-11-15/mesures.md                      |    9 +-
 journal/2026-11-15/portes.md                       |    2 +-
 journal/README.md                                  |    4 +-
 journal/THEMES.md                                  |    2 +-
 journal/sessions/MANIFEST.md                       |    4 +-
 .../e181ce02-cd50-488a-a6be-e84b79d40dcc/digest.md |   76 +
 .../rapport.md                                     |   17 +-
 .../digest.md                                      |  170 +
 .../rapport.md                                     |   44 +-
 reports/INDEX.md                                   |    3 +-
 reports/README.md                                  |    1 +
 reports/rapport-gold-reel-50.json                  | 7595 ++++++++++++++++++++
 reports/rapport-gold-reel-50.md         
… [4031 caractères tronqués]
  ```

- **bash** `{"command": "git log --oneline --all -- docs/pilotage/semaine-2.md; echo ---; git log --oneline --all -- tools/chantier/plan.json | head -10; echo ---; git diff -- tools/chantier/plan.json | head -60", "description": "Check history of week 2 plan and plan.json changes"}`

  ```
---
cd4d1060 FINITION — E1-E2 (LA FAQ AU SOMMAIRE, LES CAS D'ERREUR DU TAGGER) ; LE PLAN ET LE JOURNAL À JOUR
4d6cffc4 PHASE 4 — D1-D3 (LES EXEMPLES DU TAGGER, LA RESTITUTION v2, LA FAQ 10/10) ; L'INDEX, LA FICHE C3 ORPHELINE (GOLD RÉEL 50) ET LE PLAN COMMITTÉS
883ce817 CHANTIER — LE PLAN RESTAURÉ (29 TÂCHES, J11-J14 RÉINTÉGRÉES) ; ÉTAT HORODATÉ
ced21933 CHANTIER — PHASE 2 (12 H) : LE VERDICT ACCEPTATION D'ABORD (TIMEOUT APRÈS COMMIT = FAIT), 12 TÂCHES AJOUTÉES (J4 COORDINATION, J6 SPANS, J7-J10 PANINI/BILAN), ÉTAT CORRIGÉ
c49367e0 CHANTIER AUTONOME — LE MÉTA-HARNAIS : FILE DE 15 TÂCHES, SUPERVISEUR QUI LANCE dsh headless (CLÉ LUE), VÉRIFIE L'ACCEPTATION, PERSISTE L'ÉTAT ET S'ARRÊTE PROPREMENT ; DOCTRINE ET MODES DE PANNE
---
diff --git a/tools/chantier/plan.json b/tools/chantier/plan.json
index d81b3cbb..fcd1b1c7 100644
--- a/tools/chantier/plan.json
+++ b/tools/chantier/plan.json
@@ -573,6 +573,23 @@
      "attendu": "OK"
     }
    ]
+  },
+  {
+   "id": "F1",
+   "jour": 16,
+   "titre": "Le plan de la semaine 2",
+   "mandat": "Tâche F1 : le plan de la **semaine 2** (16 → 22/11) — lis le bilan de la semaine (`reports/rapport-bilan-semaine.md`), `docs/pilotage/en-cours.md` et l
… [702 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/README.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/README.md</path>
<type>file</type>
<content>
1: # Le dossier pilotage — carte et ordre de lecture
2: 
3: > **Ce que ce dossier est.** Le **pilotage** du projet : l'état courant, l'ordre des chantiers,
4: > le plan de travail multi-sessions, les relations entre chantiers, les contrats du backlog, les
5: > manques et les références de non-régression. **Ce n'est pas** la documentation de conception
6: > (celle-ci est dans `docs/theorie/`, `docs/implantation/`, `docs/methode/`) ni les résultats
7: > (`reports/`) ni le récit (`journal/`).
8: >
9: > **Machine** : une seule ; plusieurs sessions travaillent en parallèle sur le même arbre de
10: > travail. Les territoires et la surveillance sont dans [`plan-travail.md`](plan-travail.md) ; le
11: > registre des ressources machine (GPU, CPU, RAM, IO) et son protocole sont au **§ 10** du même
12: > plan, outillé par `tools/ressources.py`.
13: 
14: ## L'ordre de lecture
15: 
16: | ordre | document | ce qu'il répond | quand le lire |
17: |---|---|---|---|
18: | 1 | [`en-cours.md`](en-cours.md) | que se passe-t-il **maintenant** ? | au début de chaque session |
19: | 2 | [`plan-t
… [3515 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,220p' tools/revue_documentation.py", "description": "Inspect documentation review rules"}`

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
… [7540 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '220,420p' tools/revue_documentation.py", "description": "Read rest of documentation review"}`

  ```
and lab.endswith((".md", ".json", ".sh"))):
                continue
            p = (f.parent / cible).resolve()
            lp = (RACINE / lab).resolve()
            if p.exists() and lp != p:
                alertes.append(
                    f"libellé : {f.relative_to(RACINE)} annonce « {lab} » mais pointe {cible}"
                )

    # 7a. chemins morts en code inline (hors gabarits)
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
                ligne = texte[: m.start()].count("\n") + 1
                alertes.append(f"chemin mort : {f.relative_to(RACINE)}:{ligne} → {p}")

    # 7b. orphelins : tout document vivant doit avoir au moins un lien entrant
    entrants: set[pathlib.Path] = set()
    for f in sources_nav():
        try:
            texte = f.read_text(encoding="utf-8", errors="ignore")
        except OSErro
… [6228 caractères tronqués]
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py; echo \"EXIT=$?\"", "description": "Run documentation review baseline"}`

  ```
revue de documentation · 748 fiche(s) · 841 JSON · 123 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
EXIT=0
  ```

- **bash** `{"command": "date '+%Y-%m-%d %H:%M %Z'; git log -1 --format='%ad' --date=iso", "description": "Check current date and last commit date"}`

  ```
2026-11-15 07:44 EST
2026-11-15 07:35:38 -0500
  ```

- **bash** `{"command": "sed -n '1,160p' tools/verifie_en_cours.py; echo ---; sed -n '1,120p' tools/taille_documents.py", "description": "Inspect state and document budget checks"}`

  ```
#!/usr/bin/env python3
"""verifie_en_cours.py — l'état doit rester court, structuré, reprenable et multi-session.

Le fichier `docs/pilotage/en-cours.md` est la seule source de l'état. Ce contrôle vérifie :
  1. un budget de **2 000 mots** ;
  2. les **sept sections** du template ;
  3. « Sessions en cours » : une sous-section `### Session ...` par session active, avec
     **Id**, **Rôle**, **Plan**, **Ambition**, **Stratégie**, **Objectif final**,
     **Ce qu'elle fait**, **Ce que font les autres**, **Prochaine action**, **Bloquants** et
     **Journal** ;
  4. **10 puces au plus** dans « Ce qui est en cours », sans doublon et sans puce de plus de 80 mots ;
  5. « Les chantiers et leurs bloquants » : une ligne **A**, **B**, **N**, **R** avec un bloquant
     **non vide** (le mot « aucun » est une information, une cellule vide est un oubli) ;
  6. **5 questions ouvertes au plus**, chacune avec ce qui la débloque (`→`) ;
  7. une **prochaine action nommée** dans « Ce qui reste » (A/B/C/N/R) ;
  8. aucune ligne de journal A7.x dans l'état (les mesures vont dans `reports/`).

Usage : python3 tools/verifie_en_cours.py   (code 0 = l'état est reprenable)
"""
from __future__ import anno
… [9945 caractères tronqués]
  ```

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-2.md", "content": "# La semaine 2 — cinq jours, deux vagues, quatre chantiers et une décision\n\n> **Ce que ce document est.** Le plan du **16 au 22 novembre 2026** : ce qui se fait, dans quel\n> ordre, avec quelles … [11127 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-2.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "wc -l docs/pilotage/semaine-2.md; python3 tools/revue_documentation.py; echo \"EXIT=$?\"", "description": "Check line count and run documentation review"}`

  ```
103 docs/pilotage/semaine-2.md
  revue de documentation · 748 fiche(s) · 841 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ❌ 2 anomalie(s) :
     · compteurs : en-cours.md dit 123 documents, le disque en a 124
     · navigation : docs/pilotage/semaine-2.md n'a aucun lien entrant
EXIT=1
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "**Mis à jour : 2026-11-15, 07 h 30 HNE (finition : E1-E2, le tagger et ses cas d'erreur)**", "new_string": "**Mis à jour : 2026-11-15, 07 h 55 HNE (finition E1-E2 ; plan de la semaine 2)**"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "| documents de `docs/` | **123** (hors archive et README) | `docs/**/*.md` |", "new_string": "| documents de `docs/` | **124** (hors archive et README) | `docs/**/*.md` |"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "- Méthode : [contexte](../methode/contexte.md) · [continuité](../methode/continuite.md) ·\n  [résultats](../methode/resultats.md) · [portes](../methode/portes.md) · plan : [roadmap](roadmap.md)  … [447 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "python3 tools/revue_documentation.py; echo \"REVUE=$?\"; python3 tools/verifie_en_cours.py; echo \"ETAT=$?\"", "description": "Run doc review and state checks"}`

  ```
revue de documentation · 748 fiche(s) · 841 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
REVUE=0
  en-cours · 1629 mots · 7 sections · 4 session(s) · 9 puces · 5 questions
  ✅ état court, structuré, multi-session et reprenable
ETAT=0
  ```

- **bash** `{"command": "python3 tools/taille_documents.py 2>&1 | head -30; echo \"TAILLE=${PIPESTATUS[0]}\"; wc -l docs/pilotage/semaine-2.md", "description": "Check context budget and line count"}`

  ```
budget de contexte · documents chargeables
    mots lignes  cat budget  document
    8999    493   T1   9000  docs/pilotage/roadmap.md
    5999    597 DATÉ      0  docs/implantation/contexte-long.md
    4858    515   T1   5000  docs/theorie/glossaire/10-le-pont-linguistico-semantique-le-vocabu.md
    4085    431 DATÉ      0  docs/implantation/numa-segregation.md
    3310    317   T1   3500  README.md
    3072    341 DATÉ      0  docs/implantation/convertisseur.md
    2962    364   T1   5000  docs/theorie/glossaire/02-modeles-et-architectures.md
    2896    352 DATÉ      0  docs/implantation/configuration-nvme-raid-amd.md
    2496    171   T1   2500  docs/pilotage/references-non-regression.md
    2495    223   T1   2800  reports/README.md
    2111    218   T1   2500  docs/pilotage/utilisation.md
    2013    183   T1   2500  docs/theorie/jeux-symboliques.md
    2010    219   T1   5000  docs/theorie/glossaire/01-le-projet-ses-noms-sa-methode.md
    1942    218   T1   5000  docs/theorie/glossaire/04-le-moteur-drave-execution-structures-out.md
    1942    172   T1   2000  REPRISE.md
    1932    108   T1   2500  docs/pilotage/manques.md
    1931    185   T1   2500  docs/implantation/form
… [544 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-2.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-2.md</path>
<type>file</type>
<content>
1: # La semaine 2 — cinq jours, deux vagues, quatre chantiers et une décision
2: 
3: > **Ce que ce document est.** Le plan du **16 au 22 novembre 2026** : ce qui se fait, dans quel
4: > ordre, avec quelles dépendances, quels contrôles et quels livrables. Il **succède** à
5: > [`semaine-autonome.md`](semaine-autonome.md), qui reste l'**archive** de la semaine 1 et n'est
6: > **pas modifié**. L'état courant est dans [`en-cours.md`](en-cours.md) ; les chiffres sont dans
7: > les fiches citées, jamais recopiés ici.
8: >
9: > **Sources.** Le [bilan de la semaine](../../reports/rapport-bilan-semaine.md) et les fiches des
10: > tâches C/B/D/E : [C1](../../reports/rapport-coordination-n2-v2.md), [C2](../../reports/rapport-coordination-s-v2.md),
11: > [C3](../../reports/rapport-gold-reel-50.md), [B1](../../reports/rapport-protocole-date.md),
12: > [B2](../../reports/rapport-atomes-prediction.md), [B3](../../reports/rapport-cic-v2.md),
13: > [D1](../../reports/rapport-exemples-tagger.md), [D2](../../reports/rapport-restitution-v2.md),
14: > [D3](../../reports/rapport-faq.md), [
… [10584 caractères tronqués]
  ```

- **bash** `{"command": "ls -la .git/hooks/pre-commit 2>/dev/null && sed -n '1,160p' .git/hooks/pre-commit 2>/dev/null | head -80; echo ---; git status --short | head -30", "description": "Inspect pre-commit hook and working tree"}`

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
… [769 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-2.md", "old_string": "**Le gold n'est pas à recompter.** 452 est le **nombre** ; H50 est le **statut de test** ; les\n10 GP/SUB sont le **levier**. Ajouter 50 phrases ne servirait à rien : c'est la **discrimination* … [646 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-2.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-2.md", "old_string": "| | après-midi | **La clôture** : passe complète, revue, rapport de semaine 2, état, roadmap, journal, tag. **21–22 = réserve** pour les décalages. | pilote | rapport semaine 2 + JSON ; portes  … [440 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-2.md has been updated successfully.
  ```

- **bash** `{"command": "wc -l docs/pilotage/semaine-2.md; python3 tools/revue_documentation.py; echo \"REVUE=$?\"; python3 tools/verifie_en_cours.py >/dev/null; echo \"ETAT=$?\"", "description": "Re-run checks after edits"}`

  ```
108 docs/pilotage/semaine-2.md
  revue de documentation · 748 fiche(s) · 841 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
REVUE=0
ETAT=0
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-2.md", "old_string": "| | après-midi | **La clôture** : passe complète, revue, rapport de semaine 2, état, roadmap, journal, tag. **21–22 = réserve** pour les décalages. | pilote | rapport semaine 2 + JSON ; portes  … [843 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/semaine-2.md has been updated successfully.
  ```

- **bash** `{"command": "wc -l docs/pilotage/semaine-2.md; python3 tools/revue_documentation.py; echo \"REVUE=$?\"", "description": "Check final line count and review"}`

  ```
113 docs/pilotage/semaine-2.md
  revue de documentation · 748 fiche(s) · 841 JSON · 124 doc(s) · 85 porte(s) · 8 chapitre(s)
  ✅ tout passe : classement, structure, annotation, fraîcheur, compteurs, cohérence, vocabulaire, navigation
REVUE=0
  ```

- **bash** `{"command": "bash tools/porte-tableaux.sh 2>&1 | tail -30; echo \"PORTE_TABLEAUX=${PIPESTATUS[0]}\"", "description": "Run table formatting gate"}`

  ```
✅ 1823 fichier(s) : chaque tableau a le même nombre de cellules partout (en-tête, séparateur, lignes), et aucun « \| » ne s'affichera
  ✅ 4464 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
  ✅ la page vivante date du dernier commit (2026-11-15)
PORTE_TABLEAUX=0
  ```

- **bash** `{"command": "grep -n -E \"git commit|commit|git add|acceptation|accep\" tools/chantier/superviseur.py | head -60", "description": "See supervisor commit behavior"}`

  ```
6:plusieurs jours : file de tâches persistante, vérification d'acceptation **indépendante** de
10:1. **Une tâche n'est finie que si son acceptation passe** — une commande, un attendu, exécutés par
15:   tâches) arrête la boucle ; l'agent n'est jamais tué au milieu d'un commit.
20:    python3 tools/chantier/superviseur.py executer      # exécute UNE tâche (agent + acceptation)
92:# ------------------------------------------------------------------ acceptation
94:def verifier_acceptation(tache: dict) -> tuple[bool, list[str]]:
95:    """Exécute les commandes d'acceptation de la tâche ; rend (ok, détails)."""
97:    for test in tache.get("acceptation", []):
124:    vérifier, après la tâche, qu'un commit a bien été produit.
136:    """Lance l'agent sur le mandat, puis vérifie l'acceptation. Rend le résultat."""
150:                "acceptation": ["clé DeepSeek absente"], "sortie_agent": "", "cle": False}
160:    ok, details = verifier_acceptation(tache)
161:    # l'acceptation **prime** : un agent qui a fini son travail (fiche + portes) puis dépasse le
166:                "acceptation": details, "sortie_agent": sortie[-1500:]}
194:    for a in t.get("acceptation", []):
195:        prin
… [154 caractères tronqués]
  ```

- **bash** `{"command": "git diff -- docs/pilotage/en-cours.md; echo ---; git status --short docs/pilotage/semaine-2.md docs/pilotage/en-cours.md", "description": "Review state diff before commit"}`

  ```
diff --git a/docs/pilotage/en-cours.md b/docs/pilotage/en-cours.md
index 0389604e..daa6a46b 100644
--- a/docs/pilotage/en-cours.md
+++ b/docs/pilotage/en-cours.md
@@ -1,6 +1,6 @@
 # En ce moment
 
-**Mis à jour : 2026-11-15, 07 h 30 HNE (finition : E1-E2, le tagger et ses cas d'erreur)**
+**Mis à jour : 2026-11-15, 07 h 55 HNE (finition E1-E2 ; plan de la semaine 2)**
 
 > **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
 > plan plus bas (**La carte**).
@@ -107,7 +107,7 @@
 | portes | **85** (dont `porte-cic` le 14/11) | `tools/porte-*.sh` |
 | chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |
 | fichiers / JSON de résultats | **748** / **841** | `reports/*.md` / `reports/*.json` |
-| documents de `docs/` | **123** (hors archive et README) | `docs/**/*.md` |
+| documents de `docs/` | **124** (hors archive et README) | `docs/**/*.md` |
 | dernière passe | **14/11 00 h 30** (84, **81/3**) ; rouges tolérées `indice`, `melange` ; `sessions` **revérifiée verte** le 14/11 06 h 55 | `docs/pilotage/references-non-regression.md` |
 
 ## Les chantiers et leurs bloquants
@@ -144,4 +144,5 @@ externes** et la **prochaine action**.
 
… [491 caractères tronqués]
  ```

- **bash** `{"command": "date '+%H:%M %Z'", "description": "Check current time"}`

  ```
07:47 EST
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md", "old_string": "**Mis à jour : 2026-11-15, 07 h 55 HNE (finition E1-E2 ; plan de la semaine 2)**", "new_string": "**Mis à jour : 2026-11-15, 07 h 47 HNE (finition E1-E2 ; plan de la semaine 2)**"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md has been updated successfully.
  ```

- **bash** `{"command": "git add docs/pilotage/semaine-2.md docs/pilotage/en-cours.md && git commit -m \"PLAN — LA SEMAINE 2 (16 → 22/11) : GOLD 452, PAGE / DE S, PANINI À DATE CONTRÔLÉE, RESTITUTION V3, TAGGER PAR DÉFAUT ?\" 2>&1 | tail -40; echo \"COMMIT_EXIT=${PIPESTATUS[0]}\"", "description": "Commit week 2 … [25 caractères tronqués]`
