# Session DSH — relecture

- identifiant : `538288b3-117b-4daf-8d16-0cd8d6b0090d`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-06 21:13:31
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7). Mission : **état du chantier A** (le moteur) — lecture seule, aucun code.

Contexte : `docs/pilotage/roadmap.md` (A : A2.6 experts/tête, A6.2, A8.3a, A17, A23, A24…), `docs/pilotage/en-cours.md`, `docs/pilotage/backlog/index.md` + `dependances.md`, les fiches `reports/rapport-a*.md`. A23 a noté : « A2.6 n'est pas libre : experts bloqués A6.2, tête refusée, A8.3a fait, lot répondu ; à retirer de la frontière ».

À faire :
1. **Inventaire** des lignes A : état (fait / bloqué / à faire), dépendance, chiffre publié, commande de vérification.
2. **Vérifie** A2.6 (experts, tête), A6.2, A8.3a, A17, A23, A24 : les fiches et les artefacts ; ce qui est vraiment fait vs listé.
3. **La frontière** : quelles lignes A sont réellement libres (sans dépendance) et pourraient être prises en autonomie ; lesquelles restent bloquées et pourquoi.
4. **Propose** les 3 prochaines actions de A, mesurables.
5. Écris **uniquement** deux fichiers neufs : `reports/rapport-etat-a.md` et `reports/pensee-etat-a.json`.
6. Ne commite rien ; ne modifie aucun existant ; pas de `docs/pilotage/`, `AGENTS.md`, `journal/`, `tools/structures/`, `data/`, natifs.

Rends un résumé : l'état des lignes A, la frontière réelle, les 3 prochaines actions.
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

⏵ Inventaire du dépôt et lecture des documents de pilotage
Je commence par cartographier les documents de pilotage et les fiches A.

- **bash** `{"command": "pwd && git branch --show-current && git log --oneline -5 && ls", "description": "Show repo root, branch, recent commits"}`

  ```
/home/stephane/Data13TB/stephane/GitHub/Qtrinet
s/v7
d31aa9a2 PRODUIT — --partition DANS LA CLI (alternative PAR DÉFAUT, filtrer EN OPTION), 10 TESTS, DOC À JOUR
6a1148c2 B13 — L'ÉLISION « que » → « qu » DANS LE TEST DES MARQUEURS (AUCUN EFFET MESURÉ, ROBUSTESSE) ; 183/183
4e6de0ee P0-3 — LES RAPPORTS FINAUX DE LA PARTITION (MESURES ÉPINGLÉES À fa1b0c6e) ; README DANS LE BUDGET
97f41554 B13 — LE STRIP DE LA FUSION : PLUS DE RÉFÉRENCE MORTE VERS UN SEGMENT DÉDUPLIQUÉ ; MESURES INCHANGÉES (0,85 / 0,6482 / 235-236)
5c0d5329 FICHE — LES PERTES DE R4 DITES HONNÊTEMENT (5/8 FAUX EN FRANÇAIS, NOMS NUS, PARTICIPES) ; README DANS LE BUDGET T1
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
  ```

- **glob** `{"pattern": "reports/rapport-a*.md"}`

  ```
reports/rapport-aiguille.md
reports/rapport-attribution-kv.md
reports/rapport-aiguille-topk.md
reports/rapport-architecture-memoire.md
reports/rapport-attention-creuse.md
reports/rapport-analyse-flux.md
reports/rapport-a80-porte-flux.md
reports/rapport-a80-porte-pont.md
reports/rapport-a80-porte-topologie.md
reports/rapport-a83-defaut.md
reports/rapport-a26-bilan.md
reports/rapport-a80-porte-reparti.md
reports/rapport-a80-porte-budget.md
reports/rapport-a83a-flux.md
reports/rapport-a83a-pont.md
reports/rapport-a83a-coupe.md
reports/rapport-a80-porte-adaptateur.md
reports/rapport-a83b-regimes.md
reports/rapport-a80-porte-gain.md
reports/rapport-a80-porte-cycle-c2.md
reports/rapport-a83b-lot.md
reports/rapport-a80-porte-consolidation.md
reports/rapport-a80-porte-fusion.md
reports/rapport-a80-porte-trace.md
reports/rapport-a80-porte-reflexe.md
reports/rapport-a80-porte-c4-retard.md
reports/rapport-a80-porte-bus.md
reports/rapport-a80-porte-delais.md
reports/rapport-a80-porte-bus-socket.md
reports/rapport-a83c-ctx.md
reports/rapport-a80-porte-profondeur.md
reports/rapport-a80-portes-ppl.md
reports/rapport-a83b-decision.md
reports/rapport-a80-melange-qualifie.md
reports/rapport-a80-indi
… [414 caractères tronqués]
  ```

- **glob** `{"pattern": "docs/pilotage/backlog/*.md"}`

  ```
docs/pilotage/backlog/R12-curriculum-contexte.md
docs/pilotage/backlog/R21-memoire-travail-gist.md
docs/pilotage/backlog/R22-memoire-episodique.md
docs/pilotage/backlog/R32-citations-provenance.md
docs/pilotage/backlog/R51-lecture-croisee.md
docs/pilotage/backlog/R52-multilingue-decodeur.md
docs/pilotage/backlog/A3.4-colab.md
docs/pilotage/backlog/A5.4-fpga.md
docs/pilotage/backlog/A6.2-moe-local.md
docs/pilotage/backlog/B1.5-prose-scientifique.md
docs/pilotage/backlog/_modele.md
docs/pilotage/backlog/R11-contexte-hierarchique.md
docs/pilotage/backlog/N4-usage-sft.md
docs/pilotage/backlog/R31-restitution-sft.md
docs/pilotage/backlog/R01-graphe-document.md
docs/pilotage/backlog/R02-controleur-lecture.md
docs/pilotage/backlog/N0.3b-parite-ppl.md
docs/pilotage/backlog/B12.10-pipeline-m1-m4-m8.md
docs/pilotage/backlog/R41-bloc-tableaux.md
docs/pilotage/backlog/R42-bloc-code.md
docs/pilotage/backlog/R43-bloc-maths.md
docs/pilotage/backlog/A3.2-granularite.md
docs/pilotage/backlog/A3.3-seuil.md
docs/pilotage/backlog/A8.0-portes-ppl.md
docs/pilotage/backlog/B10.3-raisonnement-z.md
docs/pilotage/backlog/R03-banc-lecture-rapide.md
docs/pilotage/backlog/A2.6-ordonnanceur.md
docs/pilotage/bac
… [562 caractères tronqués]
  ```

- **bash** `{"command": "wc -l docs/pilotage/roadmap.md docs/pilotage/en-cours.md docs/pilotage/backlog/index.md docs/pilotage/backlog/dependances.md reports/rapport-a26-bilan.md reports/rapport-a26-lot-disque.md reports/rapport-a83a-flux.md reports/rapport-a83a-pont.md reports/rapport-a83a-coupe.md reports/rap … [199 caractères tronqués]`

  ```
382 docs/pilotage/roadmap.md
   145 docs/pilotage/en-cours.md
   134 docs/pilotage/backlog/index.md
   244 docs/pilotage/backlog/dependances.md
    45 reports/rapport-a26-bilan.md
    65 reports/rapport-a26-lot-disque.md
    55 reports/rapport-a83a-flux.md
    47 reports/rapport-a83a-pont.md
    54 reports/rapport-a83a-coupe.md
    76 reports/rapport-a83-defaut.md
    63 docs/pilotage/backlog/A2.6-ordonnanceur.md
    31 docs/pilotage/backlog/A6.2-moe-local.md
    60 docs/pilotage/backlog/A8.3-defaut.md
  1401 total
  ```

- **grep** `{"pattern": "^\\|?\\s*A\\d+(\\.\\d+)?[a-z]?\\b", "path": "docs/pilotage/roadmap.md"}`

  ```
Found 3 matches

docs/pilotage/roadmap.md
Line 351: | A3.4 Colab | le compte et le runtime Colab | un compte (la recette est dans `docs/archive/colab-reparti.md`) |
Line 352: | A5.4 FPGA | l'accès au matériel Stratix V | la carte (le design existe) |
Line 353: | A6.2 MoE local | aucun MoE local ne tient dans 16 Go de VRAM | un MoE qui tient, ou une machine plus grande |
  ```

- **read** `{"file_path": "docs/pilotage/roadmap.md"}`

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
… [44819 caractères tronqués]
  ```

- **read** `{"file_path": "docs/pilotage/en-cours.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/en-cours.md</path>
<type>file</type>
<content>
1: # En ce moment
2: 
3: **Mis à jour : 2026-11-06, 21 h 20 HNE (heure locale, EST).**
4: 
5: > **État courant, pas histoire** : une sous-section par **session active** ; méthode, preuves et
6: > plan plus bas (**La carte**).
7: >
8: > **Reboot du 03/11 19 h 33** : la nuit a été coupée (`kd2` **8 250/30 000**, `rope2048`
9: > **3 350/20 000**, sans checkpoint) ; les quatre sessions ont été mises en pause. **Reprise du
10: > 04/11** : hub `1e7ef596` (08 h 50), N2 09 h 41, S 09 h 46, L/B13 10 h 14 ; **N3** clos en
11: > session courte (11 h 30–11 h 38). Runbook [`plan-travail.md`](plan-travail.md) § 9 et § 12.
12: 
13: ### Session `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — le hub de reprise du 04/11
14: 
15: - **Id** : `1e7ef596-93e6-45f1-b7f2-2940044b6e3a` — [`plan.md`](../../journal/sessions/1e7ef596-93e6-45f1-b7f2-2940044b6e3a/plan.md).
16: - **Rôle** : **Hub de reprise** — état, docs, intégration, passe.
17: - **Fait** : index réparé ; **N3 intégré** ; N2/S/L actifs ; suivi docs (revue, liens, tableaux).
18: - **Prochaine action** : **suivi docs**, puis la **passe** ap
… [10827 caractères tronqués]
  ```

- **read** `{"file_path": "docs/pilotage/backlog/index.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/backlog/index.md</path>
<type>file</type>
<content>
1: # Le backlog des fonctionnalités — index
2: 
3: > **Ce que ce dossier est.** Une **fiche par fonctionnalité** à documenter et à implémenter : le programme
4: > **R (le lecteur)** et les lignes ouvertes des programmes A, B et N. Une fiche n'est **pas** un résultat :
5: > elle porte le besoin, le contrat, la porte, les contrôles négatifs et ce qui pourrait la rendre fausse. Le
6: > résultat, quand il existe, vit dans `reports/`.
7: >
8: > **La roadmap** est [`../roadmap.md`](../roadmap.md) ; l'**analyse** qui a ouvert le programme R est
9: > [`../../theorie/lecture-rapide.md`](../../theorie/lecture-rapide.md) ; l'**état courant** est
10: > [`../en-cours.md`](../en-cours.md). **Chargement** : une fiche à la fois, jamais le dossier entier. **37 fiches** : 20 pour R, 17 pour les lignes
11: > ouvertes A/B/N ; le **graphe** des dépendances est dans [`dependances.md`](dependances.md).
12: 
13: ## Comment utiliser une fiche
14: 
15: 1. **Lire le besoin et le contrat** — c'est ce qui dit si la fonctionnalité est prête à être codée.
16: 2. **Vérifier la porte et les contr
… [8239 caractères tronqués]
  ```

- **read** `{"file_path": "docs/pilotage/backlog/dependances.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/backlog/dependances.md</path>
<type>file</type>
<content>
1: # Le graphe des dépendances du backlog
2: 
3: > **Ce que ce document est.** Le **graphe** que l'index ne peut pas porter : pour chaque item des
4: > quatre chantiers (A, B, N, R), ce qu'il attend, ce qu'il débloque, et de **quel type** est
5: > l'arête. Il est **vérifié** par `tools/verifie_backlog.py` (arêtes mortes, cycles, priorités
6: > inversées, frontière) et **dessiné** dans
7: > [`backlog-dependances.svg`](../../schemas/backlog-dependances.svg).
8: >
9: > **Relevé du 2026-10-31.** 37 fiches, 1 ligne ouverte **sans fiche**, 43 arêtes dures,
10: > 3 plafonds. La roadmap donne l'ordre, l'index donne le statut, ce document donne le graphe ;
11: > les trois se contredisent s'ils sont écrits trois fois — d'où l'outil.
12: 
13: ## 1. Trois types d'arête, et pourquoi un seul ne suffit pas
14: 
15: | type | clé de la fiche | ce que ça veut dire | effet |
16: |---|---|---|---|
17: | **dure** | `Dépend de` | l'artefact d'entrée n'existe pas encore | la fiche est bloquée, elle ne peut pas être mesurée |
18: | **douce** | `Plafonné par` | le travail peut avanc
… [17392 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Recherche des lignes A17, A23, A24 et des fiches A
Les lignes A17/A23/A24 n'apparaissent pas dans la roadmap actuelle ; je cherche où elles vivent.

- **grep** `{"pattern": "\\bA17\\b|\\bA23\\b|\\bA24\\b", "path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet", "include": "*.md"}`

  ```
Found 250 of 372 matches

journal/2026-11-06/docs.md
Line 11: | 01:29 | `5523de51` | JOURNAL ET ROADMAP — LA CIBLE DE A17 ATTEINTE : 222/222, COUVERTURE 0,9289, 17 SPANS INATTEIGNABLES | `en-cours.md`, `roadmap.md`, `README.md` (+6) |

journal/2026-11-06/distribue.md
Line 20: | 10:54 | `f6c8132b` | A23 — LES 6 CORRECTIONS FACTUELLES DE LA FILE (GOLD 200+ = 13 OCCURRENCES, PASSES 2 H 11 À 2 H 29) ; T0 DANS LE BUDGET | `en-cours.md`, `README.md`, `distribue.md` (+16) |
Line 22: | 11:43 | `1962eb15` | PRODUIT — LA ROBUSTESSE : SURROGATE ET NON-STR FERMÉS (refus non_texte), 8 TESTS ; L'AUDIT A24 (50 PHRASES, 132 CHEVAUCHEMENTS, 18 CORRECTIFS) | `en-cours.md`, `README.md`, `distribue.md` (+23) |
Line 23: | 11:45 | `3601764a` | ÉTAT — T0 DANS LE BUDGET (AUDIT A24) | `en-cours.md`, `README.md`, `distribue.md` (+13) |

journal/2026-11-06/README.md
Line 49: | 01:29 | `5523de51` | JOURNAL ET ROADMAP — LA CIBLE DE A17 ATTEINTE : 222/222, COUVERTURE 0,9289, 17 SPANS INATTEIGNABLES |
Line 71: | 10:54 | `f6c8132b` | A23 — LES 6 CORRECTIONS FACTUELLES DE LA FILE (GOLD 200+ = 13 OCCURRENCES, PASSES 2 H 11 À 2 H 29) ; T0 DANS LE BUDGET |
Line 78: | 11:43 | `1962eb15` | PRODUIT — LA ROBUSTESSE : SUR
… [34306 caractères tronqués]
  ```

- **bash** `{"command": "ls reports/ | grep -Ei 'a17|a23|a24|a26|a83|a2\\.6|a8\\.3' ; echo '---json---'; ls reports/ | grep -Ei 'a17|a23|a24'", "description": "List report files matching A-numbered variants"}`

  ```
a26-bilan.json
a26-lot-disque.json
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
rapport-a26-bilan.md
rapport-a26-lot-disque.md
rapport-a83a-coupe.md
rapport-a83a-flux.md
rapport-a83a-pont.md
rapport-a83b-decision.md
rapport-a83b-lot.md
rapport-a83b-regimes.md
rapport-a83c-ctx.md
rapport-a83c-lot.md
rapport-a83-defaut.md
rapport-a83d-lot-threads.md
---json---
[exit code: 1]
  ```

- **bash** `{"command": "ls -l reports/rapport-etat-a.md reports/pensee-etat-a.json 2>&1; echo '---'; git status --porcelain | head -40; echo '---'; ls journal/sessions/538288b3-117b-4daf-8d16-0cd8d6b0090d/ 2>/dev/null", "description": "Check for existing target files and git status"}`

  ```
ls: cannot access 'reports/rapport-etat-a.md': No such file or directory
ls: cannot access 'reports/pensee-etat-a.json': No such file or directory
---
M  docs/pilotage/en-cours.md
MM journal/2026-11-05/README.md
D  journal/2026-11-05/attention.md
MM journal/2026-11-05/distribue.md
MM journal/2026-11-05/docs.md
MM journal/2026-11-05/memoire.md
MM journal/2026-11-05/mesures.md
MM journal/2026-11-05/modele.md
MM journal/2026-11-05/moteur.md
MM journal/2026-11-05/portes.md
M  journal/2026-11-06/README.md
D  journal/2026-11-06/distribue.md
D  journal/2026-11-06/docs.md
D  journal/2026-11-06/memoire.md
D  journal/2026-11-06/mesures.md
D  journal/2026-11-06/modele.md
D  journal/2026-11-06/outils.md
D  journal/2026-11-06/portes.md
MM journal/README.md
MM journal/THEMES.md
MM journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/digest.md
MM journal/sessions/0733c5bb-f90b-4f58-9241-3364fa32e46c/rapport.md
D  journal/sessions/082fe8ca-3e1e-4454-b91b-12586843e880/digest.md
D  journal/sessions/082fe8ca-3e1e-4454-b91b-12586843e880/rapport.md
D  journal/sessions/14114f3d-ae0d-416e-ad8e-4d4eaa04c36c/digest.md
D  journal/sessions/14114f3d-ae0d-416e-ad8e-4d4eaa04c36c/rapport.md
D  journal/sessions/
… [971 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,80p' journal/sessions/538288b3-117b-4daf-8d16-0cd8d6b0090d/digest.md 2>/dev/null", "description": "Read prior sibling session digest"}`

  ```
# Session DSH — relecture

- identifiant : `538288b3-117b-4daf-8d16-0cd8d6b0090d`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-06 21:13:31
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7). Mission : **état du chantier A** (le moteur) — lecture seule, aucun code.

Contexte : `docs/pilotage/roadmap.md` (A : A2.6 experts/tête, A6.2, A8.3a, A17, A23, A24…), `docs/pilotage/en-cours.md`, `docs/pilotage/backlog/index.md` + `dependances.md`, les fiches `reports/rapport-a*.md`. A23 a noté : « A2.6 n'est pas libre : experts bloqués A6.2, tête refusée, A8.3a fait, lot répondu ; à retirer de la frontière ».

À faire :
1. **Inventaire** des lignes A : état (fait / bloqué / à faire), dépendance, chiffre publié, commande de vérification.
2. **Vérifie** A2.6 (experts, tête), A6.2, A8.3a, A17, A23, A24 : les fiches et les artefacts ; ce qui est vraiment fait vs listé.
3. **La frontière** : quelles lignes A sont réellement libres (sans dépendance) et pourraient être prises en autonomie ; lesquelles restent bloquées et pourquoi.
4. **Propose** les 3 prochaines actions de A, mesurable
… [5726 caractères tronqués]
  ```

- **bash** `{"command": "ls -l journal/sessions/538288b3-117b-4daf-8d16-0cd8d6b0090d/rapport.md; echo '--- tail digest ---'; tail -c 4000 journal/sessions/538288b3-117b-4daf-8d16-0cd8d6b0090d/digest.md", "description": "Inspect prior sibling session outcome"}`

  ```
-rw-r--r--. 1 stephane stephane 2258  6 nov 21:15 journal/sessions/538288b3-117b-4daf-8d16-0cd8d6b0090d/rapport.md
--- tail digest ---
lus grande |
  ```

- **read** `{"file_path": "docs/pilotage/roadmap.md"}`

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
10: > dans [`backlog/index.md`](backlog/index.md) ; le 
… [2859 caractères tronqués]
  ```

- **bash** `{"command": "git status --porcelain | grep -E 'rapport-etat|pensee-etat' ; echo \"exit=$?\"; git log --all --oneline -- reports/rapport-etat-a.md | head", "description": "Check if target files ever existed in git"}`

  ```
exit=1
  ```

- **read** `{"file_path": "journal/sessions/538288b3-117b-4daf-8d16-0cd8d6b0090d/rapport.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/journal/sessions/538288b3-117b-4daf-8d16-0cd8d6b0090d/rapport.md</path>
<type>file</type>
<content>
1: # Session 538288b3 — Tu travailles dans /home/stephane/Data13
2: 
3: > **Journaux :** [le jour](../../2026-11-06/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).
4: 
5: | | |
6: |---|---|
7: | Identifiant | `538288b3-117b-4daf-8d16-0cd8d6b0090d` |
8: | Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
9: | Début | 2026-11-06 21:13 |
10: | Durée | 0.0 h |
11: | Tours | 1 |
12: | Messages | 11 |
13: | Appels d'outils | 11 |
14: | Fichiers touchés | 0 |
15: | Commandes | 3 |
16: | Sous-agents | 0 |
17: | Commits | 0 |
18: | Compactages de contexte | 0 |
19: 
20: ## 1. Ce qui a été demandé
21: 
22: **Tour 1** — Tu travailles dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet (branche s/v7). Mission : **état du chantier A** (le moteur) — lecture seule, aucun code.  Contexte : `docs/pilotage/roadmap.md` (A : A2.6 experts/tête, A6.2, A8.3a, A17, A23, A24…), `docs/pilotage/en-cours.md`, `docs/pilotage/backlog/index.md` + `dependances.md`, les fiches `reports/rap
… [1429 caractères tronqués]
  ```

- **bash** `{"command": "ls -l reports/rapport-file-taches.md reports/pensee-file-taches.json reports/rapport-produit-bloc-l.md reports/rapport-fiabilite-produit.md reports/rapport-robustesse-produit.md reports/rapport-spans-v7.md reports/rapport-pensee-v12.md 2>&1", "description": "Check artifacts for A17/A23/ … [5 caractères tronqués]`

  ```
-rw-r--r--. 1 stephane stephane 28685  6 nov 10:44 reports/pensee-file-taches.json
-rw-r--r--. 1 stephane stephane 39588  6 nov 12:56 reports/rapport-fiabilite-produit.md
-rw-r--r--. 1 stephane stephane 29755  6 nov 10:44 reports/rapport-file-taches.md
-rw-r--r--. 1 stephane stephane  3939  6 nov 19:06 reports/rapport-pensee-v12.md
-rw-------. 1 stephane stephane 34549  6 nov 11:31 reports/rapport-produit-bloc-l.md
-rw-r--r--. 1 stephane stephane  3115  6 nov 11:42 reports/rapport-robustesse-produit.md
-rw-r--r--. 1 stephane stephane 38231  5 nov 20:50 reports/rapport-spans-v7.md
  ```

### 🤖 Assistant

⏵ Lecture des fiches A2.6 et A8.3a
Je lis maintenant les fiches et artefacts de A2.6, A8.3a et A6.2.

- **read** `{"file_path": "reports/rapport-a26-bilan.md"}`
- **read** `{"file_path": "reports/rapport-a26-lot-disque.md"}`
- **read** `{"file_path": "docs/pilotage/backlog/A2.6-ordonnanceur.md"}`
- **read** `{"file_path": "docs/pilotage/backlog/A6.2-moe-local.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-a26-bilan.md</path>
<type>file</type>
<content>
1: # A2.6 — l'ordonnanceur est partiel : le générique et le KV sont faits, la tête est refusée, les experts bloqués
2: 
3: > **Ligne de roadmap** : A2.6 · **Date** : 2026-10-29 · **Verdict** : ⚠️ **partielle** — la règle
4: > générique et le KV sont mesurés ; la tête 4 bits est refusée par la perte ; les experts attendent
5: > **A6.2** (pas de MoE local). A2.6 ne peut pas être « complétée » sans cette brique.
6: >
7: > **Dispositif** : bilan des mesures existantes (`placement.rs`, `rapport-placement-kv-8k.md`,
8: > `rapport-regle-placement-perte.md`, A8.3) ; **pas de nouvelle mesure** ; données
9: > [`a26-bilan.json`](a26-bilan.json).
10: 
11: ## Le bilan
12: 
13: | partie | état | preuve |
14: |---|---|---|
15: | `choisir` générique | ✅ fait | `placement.rs`, 4 tests ; `kv_en_vram` appliqué dans `model.rs` |
16: | KV en VRAM | ✅ mesuré | ×1,93 au préremplissage 8 k, ×5,8 sur l’attention |
17: | tête 4 bits | ❌ refusée | +10 % de PPL ; `choisir_avec_perte` la refuse à 5 % |
18: | experts | 🧱 bloqué | **A6.2** — pas de MoE local à router |
19: | place + perte | 🔬 opt
… [1320 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-a26-lot-disque.md</path>
<type>file</type>
<content>
1: # A2.6 / A8.3 — le lot sur le disque : il accélère le calcul, il ne divise pas les lectures
2: 
3: > **Verdict.** Sur un modèle **dense** de 0,5 Go (Qwen2.5-0.5B-Q8), avec l'**éviction du cache**
4: > (`posix_fadvise(DONTNEED)`) : le lot **ne divise pas** les lectures du disque — **503 Mio** au lot 1,
5: > **502 Mio** aux lots 2, 4 et 8 (le modèle est lu une fois, quel que soit le lot). Le lot
6: > **accélère le calcul** : **24,0 → 30,5 tok/s** (+27 %) dès le lot 2, et le temps mural passe de
7: > **12,04 s à 9,96 s**. La **PPL** ne bouge presque pas : **15,8452** (lot 1) → **15,8443** (lot 2+),
8: > soit **−0,006 %**.
9: >
10: > **Date** : 2026-11-01. **Lignes** : A2.6 (ordonnanceur) et A8.3 (le lot). **Machine** : CPU seul.
11: > **Dispositif** : `tools/mesure_lot_disque.sh`, 192 jetons (les 85 626 jetons de
12: > `data/wikitext2_test.txt`), ctx 512, 20 fils, cache du modèle évincé avant chaque lot.
13: 
14: ## 1. La question
15: 
16: A2.6 : « réduire le lot » — le lot réduit-il les lectures du disque ? A8.3c avait montré, sur le
17: français en f32, que l
… [2742 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/backlog/A2.6-ordonnanceur.md</path>
<type>file</type>
<content>
1: # A2.6 — Ordonnanceur : experts et tête
2: 
3: > **Statut** : partiel · **Priorité** : P2 · **Programme** : A · **Dépend de** : A2
4: > **Ligne de roadmap** : A2.6 · **Fiche de résultat** :
5: > [`placement-kv-8k`](../../../reports/rapport-placement-kv-8k.md).
6: > **Résumé** : chaque opérateur là où son flux coûte le moins cher — et **seulement** là où
7: > la qualité le permet.
8: 
9: ## Le besoin
10: 
11: Le placement n'est pas un choix de confort : un opérateur mal placé paie le flux à chaque
12: passe. La règle doit dire, pour un opérateur, **où il tient** et **ce qu'il coûte** — et
13: refuser une place qui coûte la qualité. Aujourd'hui la règle existe pour le KV ; les experts
14: et la tête ne sont pas encore ordonnancés.
15: 
16: ## L'état
17: 
18: **Partiel** — `drave-core/src/placement.rs` porte les **bandes mesurées**, `cout`,
19: `classement`, `kv_en_vram` et la règle générale `choisir` (**4 tests verts**) : le moins cher
20: **où ça tient**. Le **KV l'applique** : à 8 k, **×1,93 / ×5,8**
21: ([fiche](../../../reports/rapport-placement-k
… [1912 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/backlog/A6.2-moe-local.md</path>
<type>file</type>
<content>
1: # A6.2 — Routage MoE appris (MoE local)
2: 
3: > **Statut** : bloquée · **Priorité** : P3 · **Programme** : A · **Dépend de** : A6 · **Bloqué par** : aucun MoE local dans 16 Go de VRAM
4: > **Ligne de roadmap** : A6.2 · **Fiche de résultat attendue** : rapport-a62-moe.md (à créer dans `reports/`)
5: > **Résumé** : Faire choisir les experts par les logs, avec une qualité égale et un coût de routage divisé.
6: > **Glossaire** : [MoE](../../theorie/glossaire/entrees/moe.md) · [expert](../../theorie/glossaire/entrees/expert.md) · [routeur](../../theorie/glossaire/entrees/routeur.md) · [k-WTA](../../theorie/glossaire/entrees/k-wta.md).
7: 
8: ## Le besoin
9: 
10: Aucun MoE local ne tient dans 16 Go de VRAM ; le routage appris reste donc non mesuré.
11: 
12: ## L'état
13: 
14: A6.1 et A6.3 ont rendu leurs négatifs ; A6.2 bloqué par le matériel.
15: 
16: ## La porte
17: 
18: Qualité égale, coût de routage ÷10, sur un MoE qui tient.
19: 
20: ## Contrôles négatifs
21: 
22: - routage aléatoire ; routage dense ; même budget
23: 
24: ## Prochaine action
25: 
26: D
… [289 caractères tronqués]
  ```

- **read** `{"file_path": "reports/rapport-a83a-flux.md"}`
- **read** `{"file_path": "reports/rapport-a83a-pont.md"}`
- **read** `{"file_path": "reports/rapport-a83a-coupe.md"}`
- **read** `{"file_path": "docs/pilotage/backlog/A8.3-defaut.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-a83a-flux.md</path>
<type>file</type>
<content>
1: # A8.3a — `porte-flux` : le régime 1 % a ses propres références
2: 
3: > **Ligne de roadmap** : A8.3a · **Date** : 2026-10-29 · **Verdict** : ✅ **le régime 1 % est
4: > épinglé pour `porte-flux`** — le même gate passe en f32 et avec `DRAVE_PERTE_MAX=1`, avec des
5: > références et des plafonds distincts. A8.3a reste **partielle** : pont et coupe à faire.
6: >
7: > **Dispositif** : `tools/porte-flux.sh`, Qwen2.5-0.5B Q8_0 ; deux régimes, cinq modes ;
8: > références f32 **61,9920 / 60,8135** et 1 % **58,3200 / 62,7357** ; données
9: > [`a83a-flux.json`](a83a-flux.json).
10: 
11: ## Ce qui est mesuré
12: 
13: | mode | f32 réf / écart | 1 % réf / écart | 1 % plafond | état |
14: |---|---:|---:|---:|---|
15: | 0 — f32 dense | 61,9920 / 0 | **58,3200 / 0** | 0 | ✅ |
16: | 1 — listes quantifiées | 61,9920 / 0 | **58,3200 / 0** | 0 | ✅ |
17: | 2 — listes par blocs | 61,9920 / 3,65e-2 | **58,3200 / 1,14e-1** | 1,2e-1 | ✅ |
18: | 3 — lot dense f32 | 60,8135 / 0 | **62,7357 / 0** | 0 | ✅ |
19: | 4 — lot en listes | 60,8135 / 4,45e-3 | **62,7357 / 3,49e-2** | 4e-2 | ✅ |
20:
… [1749 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-a83a-pont.md</path>
<type>file</type>
<content>
1: # A8.3a — `porte-pont` : le régime 1 % change la falaise
2: 
3: > **Ligne de roadmap** : A8.3a · **Date** : 2026-10-29 · **Verdict** : ✅ **le régime 1 % est
4: > épinglé pour `porte-pont`** — le gate passe en f32 et avec `DRAVE_PERTE_MAX=1`, avec deux
5: > références et deux falaises distinctes. A8.3a reste **partielle** : coupe à faire.
6: >
7: > **Dispositif** : `tools/porte-pont.sh`, Qwen2.5-0.5B Q8_0 ; deux régimes ; données
8: > [`a83a-pont.json`](a83a-pont.json).
9: 
10: ## Ce qui est mesuré
11: 
12: | mesure | f32 | 1 % | écart |
13: |---|---:|---:|---:|
14: | PPL dense | **113,0068** | **111,8003** | −1,1 % |
15: | PPL blocs | **111,9225** | **115,6406** | +3,3 % |
16: | falaise 448 fibres | **+2,81 %** | **+5,88 %** | ×2,1 |
17: | falaise 392 fibres | **+25,35 %** | **+25,75 %** | +0,4 pt |
18: 
19: Les deux gates **exit 0**. Le mode dual choisit les références selon `DRAVE_PERTE_MAX=1` ; sans
20: lui, le gate 1 % échouait sur la PPL dense (111,8003 au lieu de 113,0068) et sur 448 fibres
21: (5,88 % > 5 %).
22: 
23: ## Le contrôle négatif
24: 
25: - **f3
… [1039 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-a83a-coupe.md</path>
<type>file</type>
<content>
1: # A8.3a — `porte-coupe` : le régime 1 % écrase la variance du point de coupe
2: 
3: > **Ligne de roadmap** : A8.3a · **Date** : 2026-10-29 · **Verdict** : ✅ **le régime 1 % est
4: > épinglé pour `porte-coupe`** — le gate passe en f32 et avec `DRAVE_PERTE_MAX=1`, avec des
5: > références distinctes. A8.3a est **complet** pour les trois portes clés ; A8.3b (défaut) reste.
6: >
7: > **Dispositif** : `tools/porte-coupe.sh`, Qwen2.5-0.5B Q8_0 ; deux régimes ; données
8: > [`a83a-coupe.json`](a83a-coupe.json).
9: 
10: ## Ce qui est mesuré
11: 
12: | mesure | f32 | 1 % |
13: |---|---:|---:|
14: | PPL sans perte | **113,0068** | **111,8003** |
15: | encoded 4/20 | 116,3407 | 114,1178 |
16: | encoded 6/18 | 108,8721 | 116,8011 |
17: | encoded 12/12 | 111,9225 | 115,6406 |
18: | encoded 18/6 | 118,5275 | 114,5345 |
19: | **variance encodée** | **8,9 %** | **2,4 %** |
20: | coût du pont 12/12 | +2,81 % | +5,88 % |
21: | coût du pont 15/9 | +17,09 % | +11,56 % |
22: | coût du pont 18/6 | +0,52 % | +8,04 % |
23: 
24: Les deux gates **exit 0**. Le mode dual choisit les référe
… [1449 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/backlog/A8.3-defaut.md</path>
<type>file</type>
<content>
1: # A8.3 — Passer la règle place+perte par défaut
2: 
3: > **Statut** : mesurée · **Priorité** : P3 · **Programme** : A · **Dépend de** : A8.0
4: > **Ligne de roadmap** : A8.3 · **Fiches de résultat** :
5: > [`a83-defaut`](../../../reports/rapport-a83-defaut.md) et
6: > [`a83b-regimes`](../../../reports/rapport-a83b-regimes.md).
7: > **Résumé** : décider si `DRAVE_PERTE_MAX` devient le défaut ; la mesure dit **non**, pas
8: > encore.
9: 
10: ## Le besoin
11: 
12: La règle choisit la précision du KV par couche selon la perte mesurée. Elle payait (+0,03 %
13: sur les dernières couches) et rendait le choix de la main. La passer par défaut ferait
14: bénéficier tout le monde de l'int8 tardif — à condition de ne pas déplacer les chiffres.
15: 
16: ## L'état
17: 
18: **Mesurée négative** — le défaut déplace les portes épinglées de **−5,9 % à +19,5 %** ; trois
19: régimes sont reproductibles (f32, mélange tardif 1 %, int8 partout), et le **mélange** est un
20: troisième point : il **améliore deux mesures sur trois** et dégrade le mode de lot. La cause du
21: signe
… [1581 caractères tronqués]
  ```

