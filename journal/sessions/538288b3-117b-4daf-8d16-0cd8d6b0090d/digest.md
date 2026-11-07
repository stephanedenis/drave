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

- **grep** `{"path": "reports/rapport-file-taches.md", "pattern": "A2\\.6|frontière|experts|tête"}`

  ```
Found 8 matches

reports/rapport-file-taches.md
Line 16: - **A2.6 n'est pas une ligne libre** : ses experts sont bloqués par A6.2, sa tête est refusée, A8.3a est fait et la question du lot est répondue. Le graphe la garde pourtant à la frontière.
Line 60: | T18 | A2.6 | Trancher la frontière : A2.6 n'est pas libre (experts bloqués A6.2, tête refusée, A8.3a fait, lot répondu) ; le retirer de la frontière du graphe | docs/pilotage/backlog/dependances.md ; backlog/A2.6-ordonnanceur.md ; reports/rapport-a26-bilan.md | A6.2 | A6.2 (MoE local) | python3 tools/verifie_backlog.py | P1 |
Line 61: | T19 | DOC | Appliquer les 42 écarts de cohérence v8 (5 lignes README, en-têtes historiques) | reports/README.md ; 8 fiches et 8 JSON | hub | fiches existantes à modifier (hors fenêtre) | python3 tools/revue_documentation.py | P2 |
Line 72: | T23 | A2.6 | Experts de l'ordonnanceur | A6.2 (MoE local) | un MoE local (A6.2) | rapport-a26-bilan.md:30 |
Line 91: | D6 | A2.6 experts | roadmap:30 et 146 ; chantiers:84 ; dependances:162 ; en-cours:120 ; backlog/A2.6 | rapport-a26-bilan.md:30 | Une seule ligne, bloquée A6.2 ; retirer de la frontière |
Line 111: | P13 | A2.6 libre : experts et tête | roadma
… [366 caractères tronqués]
  ```

- **bash** `{"command": "grep -n -o '.\\{0,300\\}A2\\.6.\\{0,500\\}' reports/rapport-file-taches.md | head -20", "description": "Extract A2.6 mentions with context from A23 report"}`

  ```
16:- **A2.6 n'est pas une ligne libre** : ses experts sont bloqués par A6.2, sa tête est refusée, A8.3a est fait et la question du lot est répondue. Le graphe la garde pourtant à la frontière.
60:| T18 | A2.6 | Trancher la frontière : A2.6 n'est pas libre (experts bloqués A6.2, tête refusée, A8.3a fait, lot répondu) ; le retirer de la frontière du graphe | docs/pilotage/backlog/dependances.md ; backlog/A2.6-ordonnanceur.md ; reports/rapport-a26-bilan.md | A6.2 | A6.2 (MoE local) | python3 tools/verifie_backlog.py | P1 |
72:| T23 | A2.6 | Experts de l'ordonnanceur | A6.2 (MoE local) | un MoE local (A6.2) | rapport-a26-bilan.md:30 |
91:| D6 | A2.6 experts | roadmap:30 et 146 ; chantiers:84 ; dependances:162 ; en-cours:120 ; backlog/A2.6 | rapport-a26-bilan.md:30 | Une seule ligne, bloquée A6.2 ; retirer de la frontière |
111:| P13 | A2.6 libre : experts et tête | roadmap:30 ; dependances:162 | rapport-a26-bilan ; a26-lot-disque | Experts bloqués ; tête refusée ; A8.3a fait ; lot répondu |
125:| H2 | A2.6 est à la frontière mais son action est bloquée | rapport-a26-bilan.md:30 | Le graphe annonce 3 items libres, dont un bloqué |
190:| python3 tools/verifie_backlog.py | oui | oui | exi
… [34 caractères tronqués]
  ```

- **bash** `{"command": "ls tools/ | grep -Ei 'a26|a8|lot|porte-flux|porte-pont|porte-coupe|file_taches|file-taches|fiabilite|produit|spans|gold|pensee' | head -60; echo '--- drave-core placement ---'; ls drave-core/src/ | head -40; grep -rn \"fn test\" drave-core/src/placement.rs | head -20", "description": "L … [44 caractères tronqués]`

  ```
hebbien_produits.py
index_spans.py
mesure_lot_disque.sh
mesure-prefill-lot.sh
operateur_pensee.py
pas_de_pensee_contracte.py
pas_de_pensee_corrige.py
pas_de_pensee_mlp.py
pas_de_pensee_non_lineaire.py
pas_de_pensee.py
pas_de_pensee_recurrent.py
pensee
pensee_multilingue.py
pensee_silencieuse.py
porte-coupe.sh
porte-flux.sh
porte-pont.sh
porte-produit.sh
verifier_schema_produit.py
--- drave-core placement ---
bus.rs
clusters.rs
drvm.rs
engine.rs
engram.rs
episodique.rs
formats.rs
gguf.rs
gpu.rs
kimi_k3.rs
list.rs
main.rs
materiel.rs
model.rs
mrope.rs
native.rs
placement.rs
tokenizer.rs
topologie.rs
trace_globale.rs
  ```

- **bash** `{"command": "python3 tools/verifie_backlog.py 2>&1 | tail -40; echo \"exit=$?\"", "description": "Run backlog verification read-only"}`

  ```
=== GRAPHE DU BACKLOG ===
  fiches 37 · lignes sans fiche 1 · arêtes dures 43 · plafonds 3
  profondeur 5 : R01 → R02 → R03 → R31 → R32 → R51
  frontière (3) : A2.6, N2, N4

✅ le graphe est cohérent : aucune arête morte, aucun cycle, aucune priorité inversée.
exit=0
  ```

- **bash** `{"command": "grep -n \"mod tests\" -A80 drave-core/src/placement.rs | head -120", "description": "Inspect placement tests"}`

  ```
177:mod tests {
178-    use super::*;
179-
180-    #[test]
181-    fn la_vram_est_le_support_le_moins_cher_pour_un_gros_lecteur() {
182-        // Un KV de 1 M de jetons sur un 0,5 B : ~100 Mo lus par jeton.
183-        let octets = 100 * 1024 * 1024u64;
184-        let c = classement(octets);
185-        assert_eq!(c[0], Support::Vram);
186-        assert_eq!(c[3], Support::Reseau);
187-        assert!(cout(octets, Support::Vram) < cout(octets, Support::Ram));
188-    }
189-
190-    #[test]
191-    fn le_kv_tient_si_la_reserve_est_respectee() {
192-        assert!(kv_en_vram(4 << 30, 8 << 30));
193-        assert!(kv_en_vram(7 << 30, 8 << 30));      // 7 + 1 = 8 : la réserve tient juste
194-        assert!(!kv_en_vram(8 << 30, 8 << 30));     // 8 + 1 > 8
195-        assert!(!kv_en_vram((7 << 30) + 1, 8 << 30));
196-    }
197-
198-    #[test]
199-    fn choisir_respecte_la_place() {
200-        // Le KV d'un contexte de 1 M (~25 Go) ne tient pas en VRAM (16 Go) : RAM.
201-        assert_eq!(choisir(25 << 30, 25 << 30, 16 << 30, 64 << 30), Support::Ram);
202-        // Un petit KV (100 Mo) va en VRAM.
203-        assert_eq!(choisir(100 << 20, 100 << 20, 4 << 30, 64 << 30), Support::
… [2354 caractères tronqués]
  ```

- **bash** `{"command": "cat reports/a26-bilan.json; echo '---'; cat reports/a83a-flux.json | head -60", "description": "Read A2.6 and A8.3a JSON artifacts"}`

  ```
{
 "date": "2026-10-29",
 "ligne": "A2.6",
 "verdict": "partielle",
 "parties": {
  "choisir_generique": {
   "etat": "fait",
   "preuve": "placement.rs, 4 tests ; kv_en_vram appliqué dans model.rs"
  },
  "kv_vram": {
   "etat": "fait",
   "preuve": "rapport-placement-kv-8k.md, ×1,93 / ×5,8"
  },
  "tete_4bits": {
   "etat": "refusee",
   "preuve": "TETE_4BIT +10 % PPL ; choisir_avec_perte la refuse à 5 %"
  },
  "experts": {
   "etat": "bloque",
   "preuve": "A6.2 — pas de MoE local"
  },
  "place_et_perte": {
   "etat": "opt-in",
   "preuve": "A8.3 refusé par la mesure ; A8.3a à venir"
  }
 },
 "controle": "choisir_avec_perte refuse la tête 4 bits à 5 % (test) ; sans MoE local, les experts ne sont pas mesurables",
 "limites": [
  "bilan, pas une nouvelle mesure",
  "la tête 4 bits a été essayée puis revertée ; pas de chiffre courant",
  "experts non mesurables sans A6.2"
 ]
}
---
{
 "date": "2026-10-29",
 "ligne": "A8.3a",
 "porte": "porte-flux.sh",
 "regime": "DRAVE_PERTE_MAX=1",
 "f32": {
  "mode0": {
   "ref": 61.992,
   "ecart": 0.0
  },
  "mode1": {
   "ref": 61.992,
   "ecart": 0.0
  },
  "mode2": {
   "ref": 61.992,
   "ecart": 0.0365
  },
  "mode3": {
   "ref": 60.8135,

… [724 caractères tronqués]
  ```

- **bash** `{"command": "head -40 drave-core/Cargo.toml; echo '---'; ls reports/ | grep -E 'placement|regle-placement|a8'", "description": "Inspect cargo package and placement reports"}`

  ```
[package]
name = "drave-core"
version = "0.1.0"
edition = "2021"
description = "Drave — moteur d'exécution par listes d'activation (stream of logs) pour modèles quantifiés"

[[bin]]
name = "drave"
path = "src/main.rs"

[dependencies]
# aucune : std seul, pour rester sans dépendance réseau

[profile.release]
opt-level = 3
lto = true
codegen-units = 1
panic = "abort"
---
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
n3.4c-placement.json
rapport-a80-audit-final.md
rapport-a80-indice-qualifie.md
rapport-a80-melange-qualifie.md
rapport-a80-pannes-ppl.md
rapport-a80-porte-adapt
… [836 caractères tronqués]
  ```

- **bash** `{"command": "head -30 reports/rapport-placement-kv-8k.md; echo '=== regle ==='; head -40 reports/rapport-regle-placement-perte.md", "description": "Read placement KV and loss rule reports"}`

  ```
# Le placement du KV à 8 k : ×1,93 sur le préremplissage, ×5,8 sur l'attention

> Mesure du 24/10/2026, Qwen2.5-0.5B Q8_0, contexte 8192, **5 337 jetons** de prompt, 8 jetons générés,
> 20 fils, binaire du dépôt. Deux exécutions, même prompt, même contexte : seul le **placement du cache KV** change
> (RAM par défaut, VRAM avec `DRAVE_GPU_KV=1`).

## La question

L'axe 2 de la vision tient en une règle : **on place un opérateur là où son flux coûte le moins cher**. Le cache KV
est le cas type : sa **lecture par jeton** croît linéairement avec le contexte (5 337 jetons × 24 couches × 2 têtes
KV × 64 dim × 4 octets ≈ **65,6 Mo par jeton**), et la bande passante de la RAM (~22,5 Go/s mesurés) contre celle
de la VRAM (~84,9 Go/s mesurés) décide du coût. À quel point la règle se voit-elle sur un contexte long ?

## La mesure

| | KV en RAM (défaut) | KV en VRAM | gain |
|---|---:|---:|---:|
| **préremplissage** (5 337 jetons) | 297,0 s (18,0 tok/s) | **153,7 s (34,7 tok/s)** | **×1,93** |
| **attention** (par jeton) | 32,3 ms | **5,6 ms** | **×5,8** |
| décodage (8 jetons) | 0,696 s (11,5 tok/s) | **0,278 s (28,7 tok/s)** | ×2,5 |
| total mesuré (par jeton) | 59,0 ms | **32,2 ms** | ×1,8
… [2802 caractères tronqués]
  ```

- **read** `{"file_path": "reports/rapport-a83-defaut.md"}`
- **read** `{"file_path": "reports/rapport-a83b-regimes.md"}`
- **read** `{"file_path": "reports/rapport-a83c-lot.md"}`
- **read** `{"file_path": "reports/rapport-a83d-lot-threads.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-a83-defaut.md</path>
<type>file</type>
<content>
1: # A8.3 — le défaut place+perte n'est pas neutre : les portes épinglées bougent de −5,9 % à +19,5 %
2: 
3: > **Ligne de roadmap** : A8.3 (et A8.0) · **Date** : 2026-10-29 · **Verdict** : ❌ **le
4: > passage par défaut est refusé, chiffres en main** — la règle place+perte déplace la PPL
5: > des portes épinglées de **−5,9 %** (flux mode 0, budget 1 %) à **+19,5 %** (flux mode 3,
6: > budget 10 %). Elle **reste opt-in** ; ce qui manque n'est pas une porte, c'est un
7: > **régime** de référence.
8: >
9: > **Dispositif** : `DRAVE_PERTE_MAX` (budget en %) sur les portes déjà épinglées par A8.0 ;
10: > trois budgets — **0,001 %** (aucune couche ne passe en int8), **1 %** (le défaut prévu),
11: > **10 %** (toutes les couches) ; CPU/GPU comme les portes ; JSON
12: > [`a83-defaut.json`](a83-defaut.json) ; porte
13: > [`porte-flux.sh`](../tools/porte-flux.sh) et [`porte-pont.sh`](../tools/porte-pont.sh).
14: 
15: ## La question
16: 
17: A8.0 a épinglé deux portes qui mesurent une PPL (flux **61,9920 / 60,8135**, pont
18: **113,0068**). A8.3 demandait : la règle **place et 
… [3495 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-a83b-regimes.md</path>
<type>file</type>
<content>
1: # A8.3b — les trois régimes de KV : le mélange tardif est meilleur que le f32, l'int8 partout est pire
2: 
3: > **Ligne de roadmap** : A8.3 (suite d'A8.3 et d'A8.0) · **Date** : 2026-10-29 · **Verdict** :
4: > ✅ **la non-monotonie est réelle et reproductible** — trois régimes, trois chiffres :
5: > f32 (**61,9920 / 60,8135 / 113,0068**), mélange tardif 1 % (**58,3200 / 62,7357 / 111,8003**),
6: > int8 partout (**66,6195 / 72,6501 / 120,0813**). Le mélange améliore **deux mesures sur
7: > trois** ; l'int8 partout dégrade **partout**. Ce n'est pas un artefact de la règle : le
8: > chemin explicite (`DRAVE_KV_BITS=8`) redonne exactement les chiffres du budget 10 %.
9: >
10: > **Dispositif** : Qwen2.5-0.5B-Q8_0, portes `porte-flux` et `porte-pont`, GPU ; trois régimes
11: > par variable d'environnement (`DRAVE_KV_BITS`, `DRAVE_PERTE_MAX`) ; JSON
12: > [`a83b-regimes.json`](a83b-regimes.json) ; suite d'[A8.3](rapport-a83-defaut.md).
13: 
14: ## La question
15: 
16: A8.3 a montré que le défaut place+perte déplace les portes de −5,9 % à +19,5 %. Le signe
17: positif 
… [3708 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-a83c-lot.md</path>
<type>file</type>
<content>
1: # A8.3c — le lot n'est pas neutre : la « non-monotonie » du KV était un effet de chemin
2: 
3: > **Ligne de roadmap** : A8.3 (suite d'A8.3b) · **Date** : 2026-10-29 · **Verdict** : ✅
4: > **expliqué** — le régime du KV a un effet **cohérent sur chaque chemin** : **−5,9 %** sur le
5: > chemin jeton par jeton, **+3,2 %** sur le chemin par lots. La « non-monotonie » d'A8.3b
6: > n'était pas la règle : c'étaient **deux chemins différents**, et le lot déplace à lui seul la
7: > PPL de **1,90 %** (61,9920 à lot 1 contre 60,8135 à lot ≥ 2, en f32).
8: >
9: > **Dispositif** : `porte-flux`, mode 3 (`--lot`), deux régimes de KV (f32 ; mélange 1 % par
10: > `DRAVE_PERTE_MAX=1`), trois lots (1, 2, 4) ; Qwen2.5-0.5B-Q8_0, GPU ; JSON
11: > [`a83c-lot.json`](a83c-lot.json) ; suite d'[A8.3](rapport-a83-defaut.md) et
12: > [A8.3b](rapport-a83b-regimes.md).
13: 
14: ## La question
15: 
16: A8.3b a montré que le mélange KV « améliore » le mode 0 (−5,9 %) et « dégrade » le mode 3
17: (+3,2 %) — un signe qui n'est pas celui d'une quantification. D'où vient-il : de la règle, du
18: nom
… [3443 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-a83d-lot-threads.md</path>
<type>file</type>
<content>
1: # A8.3d — le lot n'est pas les threads : l'écart de 1,90 % survit à 1 thread
2: 
3: > **Ligne de roadmap** : A8.3 (suite d'A8.3c) · **Date** : 2026-10-30 · **Verdict** : ✅
4: > **condition affinée** — l'écart de PPL entre lot 1 et lot 4 (**1,90 %**) est **le même à 1 et à
5: > 8 threads**. Ce n'est donc pas le pool de threads : c'est le **noyau par lots** lui-même.
6: >
7: > **Dispositif** : `tools/porte-flux.sh` (mode 3, `--lot`), quatre réglages `THREADS` 1/8 ×
8: > `LOT` 1/4, Qwen2.5-0.5B-Q8_0, 24 ids, ctx 64 ; JSON
9: > [`a83d-lot-threads.json`](a83d-lot-threads.json).
10: 
11: ## La question
12: 
13: A8.3c a montré que le lot déplace la PPL à lui seul : **61,9920** au lot 1 contre **60,8135** au lot
14: ≥ 2 (−1,90 %), et l'a attribué aux « sommes réordonnées ». Deux causes restaient possibles : le
15: **pool de threads** (8 par défaut) ou le **noyau par lots** (sommes par bloc). Passer à **1 thread**
16: sépare les deux.
17: 
18: ## Ce qui est mesuré
19: 
20: | threads | lot 1 | lot 4 | écart |
21: |---:|---:|---:|---:|
22: | **8** | **61,9920** | **6
… [2238 caractères tronqués]
  ```

- **read** `{"file_path": "reports/rapport-a83b-decision.md"}`
- **read** `{"file_path": "reports/rapport-a83b-lot.md"}`
- **read** `{"file_path": "reports/rapport-a83c-ctx.md"}`
- **read** `{"file_path": "docs/pilotage/backlog/A8.0-portes-ppl.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-a83b-decision.md</path>
<type>file</type>
<content>
1: # A8.3b/c — décision : le défaut reste opt-in, la cause est le chemin lot
2: 
3: > **Ligne de roadmap** : A8.3b/c · **Date** : 2026-10-29 · **Verdict** : ⛔ **défaut refusé** —
4: > le signe du mélange 1 % bascule avec le **chemin lot binaire** (lot 1 contre lot ≥ 2), pas
5: > avec la taille du cache (ctx 64/256/512 identiques). A8.3 reste **opt-in**.
6: >
7: > **Dispositif** : synthèse des mesures A8.3a/b/c, aucun nouveau run ; données
8: > [`a83b-decision.json`](a83b-decision.json).
9: 
10: ## Les chiffres qui décident
11: 
12: | régime | lot 1 | lot 2 | lot 4 |
13: |---|---:|---:|---:|
14: | f32 | **61,9920** | **60,8135** | **60,8135** |
15: | 1 % | **58,3200** | **62,7357** | **62,7357** |
16: 
17: - **Lot 1 = pas de lot** : les chiffres redonnent le mode 0.
18: - **Lot ≥ 2** : identiques ; la taille de lot ne porte pas l’effet.
19: - **Ctx 64/256/512** : 24 exécutions, aucune ligne ne bouge — le cache n’est pas la cause.
20: - Le signe **bascule avec le chemin** : f32 lotte mieux, 1 % lotte moins bien.
21: 
22: ## Pourquoi le défaut est refusé
23: 
24: -
… [1672 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-a83b-lot.md</path>
<type>file</type>
<content>
1: # A8.3b.1 — le signe du mélange vient du **chemin lot**, pas de la taille de lot
2: 
3: > **Ligne de roadmap** : A8.3b · **Date** : 2026-10-29 · **Verdict** : ✅ **le basculement est
4: > binaire** — `--lot 1` (pas de lot) et `--lot ≥ 2` sont deux régimes ; à l’intérieur de `≥ 2`, la
5: > taille ne change rien à quatre décimales. Le signe du mélange 1 % bascule avec ce chemin.
6: >
7: > **Dispositif** : `drave --ppl-reparti`, Qwen2.5-0.5B Q8_0, 12 couches locales, 24 jetons,
8: > ctx 64 ; cinq tailles de lot × deux régimes ; données [`a83b-lot.json`](a83b-lot.json).
9: 
10: ## Ce qui est mesuré
11: 
12: | lot | f32 | mélange 1 % |
13: |---:|---:|---:|
14: | **1** | **61,9920** | **58,3200** |
15: | 2 | **60,8135** | **62,7357** |
16: | 4 | **60,8135** | **62,7357** |
17: | 8 | **60,8135** | **62,7357** |
18: | 16 | **60,8135** | **62,7357** |
19: 
20: - **Lot 1 = pas de lot** : les valeurs sont exactement celles du mode 0 de `porte-flux`.
21: - **Lot ≥ 2** : identiques à quatre décimales dans chaque régime ; la taille de lot ne porte pas
22:   l’effet.
23: - En f32
… [1549 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-a83c-ctx.md</path>
<type>file</type>
<content>
1: # A8.3c.1 — le signe du mélange ne dépend pas de la taille du contexte
2: 
3: > **Ligne de roadmap** : A8.3b/c · **Date** : 2026-10-29 · **Verdict** : ✅ **le cache n’est pas
4: > la cause** — à ctx 64, 256 et 512, les PPL sont **identiques** : f32 lot 0/1 = **61,9920**,
5: > lot 2/4 = **60,8135** ; 1 % lot 0/1 = **58,3200**, lot 2/4 = **62,7357**. Le basculement est
6: > le **chemin lot** (lot 1 contre lot ≥ 2), pas la capacité du cache.
7: >
8: > **Dispositif** : `--ppl-reparti`, Qwen2.5-0.5B Q8_0, 12 couches locales, 24 jetons, ctx variable ;
9: > 24 exécutions ; données [`a83c-ctx.json`](a83c-ctx.json).
10: 
11: ## Ce qui est mesuré
12: 
13: | régime | ctx | lot 0 | lot 1 | lot 2 | lot 4 |
14: |---|---:|---:|---:|---:|---:|
15: | f32 | 64 | 61,9920 | 61,9920 | 60,8135 | 60,8135 |
16: | f32 | 256 | 61,9920 | 61,9920 | 60,8135 | 60,8135 |
17: | f32 | 512 | 61,9920 | 61,9920 | 60,8135 | 60,8135 |
18: | 1 % | 64 | 58,3200 | 58,3200 | 62,7357 | 62,7357 |
19: | 1 % | 256 | 58,3200 | 58,3200 | 62,7357 | 62,7357 |
20: | 1 % | 512 | 58,3200 | 58,3200 | 62,7357 | 62,7357
… [1162 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/pilotage/backlog/A8.0-portes-ppl.md</path>
<type>file</type>
<content>
1: # A8.0 — Épingler les portes qui mesurent une PPL
2: 
3: > **Statut** : mesurée · **Priorité** : P2 · **Programme** : A · **Dépend de** : A8
4: > **Ligne de roadmap** : A8.0 · **Fiches de résultat** :
5: > [`a80-flux`](../../../reports/rapport-a80-porte-flux.md),
6: > [`a80-pont`](../../../reports/rapport-a80-porte-pont.md),
7: > [`a80-topologie`](../../../reports/rapport-a80-porte-topologie.md).
8: > **Résumé** : une porte qui mesure une PPL doit avoir une **référence chiffrée** avant qu'on
9: > touche à un défaut — sinon on ne sait pas ce qu'on casse.
10: 
11: ## Le besoin
12: 
13: A8.3 (« opt-in → défaut ») exigeait d'épingler les portes qui mesurent une PPL. Cette
14: condition n'avait ni identifiant ni fiche : un changement de défaut déplaçait des chiffres
15: sans qu'aucune porte ne le dise. A8.0 est cette condition, nommée.
16: 
17: ## L'état
18: 
19: **Mesurée** — les portes qui mesurent une PPL sont épinglées :
20: 
21: | porte | référence épinglée |
22: |---|---|
23: | [`porte-flux`](../../../tools/porte-flux.sh) | **61,9920 / 60,8135** (mod
… [1751 caractères tronqués]
  ```

- **bash** `{"command": "ls reports/rapport-a80-porte-*.md | wc -l; ls reports/rapport-a80-porte-*.md | sed 's#reports/rapport-a80-porte-##;s#\\.md##' | tr '\\n' ' '; echo; echo '--- tools porte list ---'; ls tools/porte-*.sh | wc -l; echo '--- a80 audit counts ---'; grep -n -E \"18|portes|PPL\" reports/rapport … [91 caractères tronqués]`

  ```
17
adaptateur budget bus bus-socket c4-retard consolidation cycle-c2 delais flux fusion gain pont profondeur reflexe reparti topologie trace 
--- tools porte list ---
84
--- a80 audit counts ---
4:> portes PPL épinglées**, **14 restantes classées** : 3 comparatifs intra-run non épinglés,
5:> 2 rouges qualifiées, 1 verte sans PPL, 8 sans PPL. Aucune porte mesurable n’est laissée dans
8:> **Dispositif** : inventaire statique des 33 portes, recoupé avec les 19 fiches de pin ; données
19:| catégorie | portes | raison |
22:| verte sans PPL | `homeostasie` | mesure des normes, pas une perplexité |
24:| sans PPL | `diff-couche`, `echange-experts`, `harnais-invariants`, `jumeaux`, `mistral`, `occupation-moteur`, `prechargement`, `push-paresseux` | aucune PPL à épingler |
32:- **Les 8 sans PPL** ne peuvent pas être épinglées sans changer ce qu’elles mesurent.
41:- **La PPL n’est pas la qualité** : 19 pins protègent une valeur, pas un jugement.
46:qualifiées, 8 sans PPL. A8.3 reste opt-in ; la condition duale pour les 19 pins n’est pas remplie.
  ```

- **bash** `{"command": "grep -rn \"DRAVE_PERTE_MAX\" tools/porte-*.sh | cut -d: -f1 | sort -u; echo '--- refs in tools ---'; grep -ln \"61.9920\\|113.0068\\|17.4702\" tools/porte-*.sh | tr '\\n' ' '; echo; echo '--- audit final head ---'; head -50 reports/rapport-a80-audit-final.md", "description": "Check whic … [29 caractères tronqués]`

  ```
tools/porte-coupe.sh
tools/porte-flux.sh
tools/porte-pont.sh
--- refs in tools ---
tools/porte-bus-socket.sh tools/porte-coupe.sh tools/porte-flux.sh tools/porte-fusion.sh tools/porte-pont.sh tools/porte-topologie.sh 
--- audit final head ---
# A8.0 — audit final : 19/33, les 14 restantes classées

> **Ligne de roadmap** : A8.0 · **Date** : 2026-10-30 · **Verdict** : ✅ **audit clos** — **19
> portes PPL épinglées**, **14 restantes classées** : 3 comparatifs intra-run non épinglés,
> 2 rouges qualifiées, 1 verte sans PPL, 8 sans PPL. Aucune porte mesurable n’est laissée dans
> un flou non nommé.
>
> **Dispositif** : inventaire statique des 33 portes, recoupé avec les 19 fiches de pin ; données
> [`a80-audit-final.json`](a80-audit-final.json).

## Les 19 épinglées

`adaptateur-sortie`, `budget`, `bus-socket`, `bus`, `c4-retard`, `consolidation`, `coupe`,
`cycle-c2`, `delais`, `flux`, `fusion`, `gain`, `pannes`, `pont`, `profondeur-routee`, `reflexe`,
`reparti-moteur`, `topologie`, `trace`.

## Les 14 restantes

| catégorie | portes | raison |
|---|---|---|
| comparatif intra-run, non épinglé | `horloge`, `poids-creux`, `registre` | compare deux bras, pas une valeur externe |
| verte 
… [1405 caractères tronqués]
  ```

- **read** `{"file_path": "reports/rapport-file-taches.md", "limit": 70}`
- **read** `{"file_path": "reports/rapport-robustesse-produit.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-file-taches.md</path>
<type>file</type>
<content>
1: # La file des tâches — inventaire, trois files et ordre pour 09 h 30 → 12 h
2: 
3: > **Ligne de roadmap** : B13 (moteur de pensée) · **Date** : 2026-11-06, 10 h 20 HNE · **Branche** : `s/v7` · **HEAD mesuré** : `7679a2d4`.
4: > **Mission** : inventer toutes les prochaines actions nommées dans `roadmap.md`, `en-cours.md`, `plan-travail.md` § 9 et § 12, `backlog/index.md`, `backlog/dependances.md`, `references-non-regression.md` et les 12 fiches récentes ; les classer en trois files ; détecter doublons et périmées ; proposer l'ordre de la fenêtre.
5: > **Verdict** : **29 tâches** — **8 autonomes**, **11 en coordination**, **10 bloquées** ; **6 doublons**, **18 périmées**, **12 dépendances cachées**.
6: > **Ce que cette fiche n'est pas** : un commit, une modification d'existant, ou une mesure nouvelle sur S/D/N2. Elle ne crée que deux fichiers neufs.
7: 
8: ## 1. Résumé exécutif
9: 
10: La file est **courte** une fois les doublons retirés : **8 tâches sont exécutables en autonomie** dans le territoire L/B13 et le pilotage, **11 demandent une coordination** (S, D, 
… [11375 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-robustesse-produit.md</path>
<type>file</type>
<content>
1: # B13 — la robustesse du produit : un surrogate ne plante plus, une entrée non-str est refusée
2: 
3: > **Ligne de roadmap** : **B13** (produit) · **Date** : 2026-11-06 · **Verdict** : ✅ **deux bugs
4: > produit fermés** — un **surrogate isolé** faisait planter `analyser` (`UnicodeEncodeError` sur
5: > `len(texte.encode())`) et une entrée **non-str** (`bytes`, `int`, `list`) levait
6: > `AttributeError`. Désormais : l'encodage utilise `errors="replace"` et une entrée non textuelle
7: > rend `refus="non_texte"` (0 étiquette, pas d'exception). **Huit tests** produit passent.
8: >
9: > **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`analyser`,
10: > encodages), [`test_produit.py`](../tools/tests/test_produit.py) (`TestRobustesse`) ; audit
11: > amont [`rapport-produit-bloc-l.md`](rapport-produit-bloc-l.md) (A24 : 50 phrases libres, 18
12: > correctifs) ; JSON [`pensee-robustesse-produit.json`](pensee-robustesse-produit.json).
13: 
14: ## 1. Les deux bugs
15: 
16: | entrée | avant | après |
17: |---|---|---|
18: | `"Le chat \ud800 
… [2226 caractères tronqués]
  ```

- **bash** `{"command": "head -60 reports/rapport-produit-bloc-l.md; echo '=== grep reproduce ==='; grep -n -A12 \"Reproduire\\|Vérifier\\|Commande\" reports/rapport-produit-bloc-l.md | head -60", "description": "Read A24 audit report head and commands"}`

  ```
# Audit produit du bloc linguistique — 0 plantage sur 50 phrases, 34/50 avec une anomalie de contrat

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Branche** : `s/v7` ·
> **Commit mesuré** : `fa1b0c6e` (2026-11-06 09:16) · **HEAD vérifié en fin d'audit** : `c6904284`
> (le HEAD a bougé pendant l'audit ; module `bloc_linguistique.py` inchangé ; `evaluer_gold.py`
> modifié en `7f73c17f`) ·
> **Date** : 2026-11-06 ·
> **Verdict** : ⚠️ **la surface est utilisable en autonomie ; la structure ne l'est pas encore.**
> **Aucun fichier existant modifié par cet audit ; aucun commit.** Sorties : ce rapport et
> [`pensee-produit-bloc-l.json`](pensee-produit-bloc-l.json).
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py),
> [`evaluer_gold.py`](../tools/tests/linguistique/evaluer_gold.py),
> [`gold_split.py`](../tools/tests/linguistique/gold_split.py) ; **50 phrases libres** écrites pour
> l'audit (textes dans le JSON) ; harnais local non committé dans `/tmp/audit_produit_bl`.
> **Porte** : `bash tools/porte-bloc-linguistique.sh` → **verte** (16 tests, autotest UDHR
> **0,9687**, profils permutés **0,0022**).

**En une phrase.** Sur 50 phrases libres
… [3567 caractères tronqués]
  ```

- **bash** `{"command": "head -70 reports/rapport-spans-v7.md; echo '=== grep reproduce ==='; grep -n -A10 \"Reproduire\\|Vérifier\\|commande\" reports/rapport-spans-v7.md | head -40", "description": "Read A17 spans report head and commands"}`

  ```
# Rapport — les 43 spans non prédits de l'attachement v7

> **Ligne de roadmap** : **B13** (attachement, règle 6) · **Date** : 2026-11-05 ·
> **Commit de départ** : `69bd865ec1bae1958b6f617bde4bf685a15d7d67` (branche `s/v7`) ·
> **Périmètre** : `tools/bloc_linguistique.py` (`Heuristique`, `_syntagmes_simple`,
> `_cible_precedent`), `tools/tests/linguistique/evaluer_gold.py` (`charger`, `evaluer_bloc`),
> `tools/tests/linguistique/gold_split.py` (`dev`, `test`).
> **Livrables** : ce rapport + [`pensee-spans-v7.json`](pensee-spans-v7.json).
> **Aucun fichier existant n'a été modifié par cette session** ; les mesures viennent d'une copie locale
> (`/tmp/spans/sim3.py`, sous-classe de `Heuristique` + copie instrumentée de
> `_syntagmes_simple`), non commitée. Le dispositif officiel (`evaluer_bloc`) redonne
> **exactement** la ligne de base 196/195 et F1 0,5555 sur le gold vivant 612.

## 1. Résumé

**État de départ** : 239 cibles, **196 labels au bon span**, **195 exacts / 196** (0,9949),
43 non prédits = **21 REL, 17 SUB, 5 GP**. **État final** de la meilleure combinaison :
**222 labels, 222 exacts / 222** (1,0000), soit **222/239 = 0,9289** des cibles ; il reste
**17 cibles non couve
… [3289 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification en exécution des chiffres A17/A23
Je rejoue les mesures citées (gold, autotest) pour distinguer le publié du réel.

- **bash** `{"command": "python3 tools/tests/linguistique/evaluer_gold.py --help 2>&1 | head -20; echo '---'; head -50 tools/tests/linguistique/evaluer_gold.py", "description": "Inspect gold evaluator usage"}`

  ```
usage: evaluer_gold.py [-h] [--json JSON] [--reel]

evaluer_gold.py — mesure le bloc linguistique sur le gold réel (20) +
synthétique (160). Trois niveaux : POS (token, exact), syntagmes (exact +
**par tête**), pragmatique. Quatre lectures : heuristique, mock neuronal,
parallèle, cascade. Le vrai modèle est optionnel (`--reel`) : s'il ne répond
pas, il est refusé, pas simulé.

options:
  -h, --help   show this help message and exit
  --json JSON
  --reel
---
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
SYNTH = pathli
… [951 caractères tronqués]
  ```

- **bash** `{"command": "python3 -m tools.pensee.autotest 2>&1 | tail -8; echo \"exit=$?\"", "description": "Run thought engine autotest"}`

  ```
[still running after 60000ms; moved to background job bash-3979]
The command keeps running in the background. You will be notified when it finishes; read newer output with job_output, stop it with job_kill.
  ```

- **bash** `{"command": "timeout 300 python3 tools/tests/linguistique/evaluer_gold.py --json /tmp/etat-a-gold.json > /tmp/etat-a-gold.txt 2>&1; echo \"exit=$?\"; tail -5 /tmp/etat-a-gold.txt", "description": "Run gold evaluator to /tmp", "run_in_background": true}`

  ```
started background job bash-3994
  ```

- **bash** `{"command": "grep -n \"fronti\\|libre\\|bloqu\\|Dépend de\\|plafond\" tools/verifie_backlog.py | head -50", "description": "Inspect frontier computation logic"}`

  ```
13:  1. chaque identifiant cité dans « Dépend de » existe (fiche, ligne acquise, ou ligne
15:  2. le graphe est acyclique (les arêtes dures et les plafonds) ;
19:  6. il calcule la **frontière** : ce qui est réellement non bloqué aujourd'hui, et la
23:  - **dure** (`Dépend de`)   : l'artefact d'entrée n'existe pas ; la fiche est bloquée ;
26:    rien. Confondre « fait » et « dure » fait croire bloqué ce qui est libre : `R21`
46:    "bloquée", "abandonnée",
61:# (elles bloquent des fiches) mais elles ne portent ni porte ni contrôle négatif : c'est un
123:            "dures": liste(c.get("Dépend de")),
128:            "bloque": c.get("Bloqué par", ""),
136:            "bloque": "", "sans_fiche": True, "note": note,
204:    # 3. acyclicité (arêtes dures + plafonds)
256:def frontiere(noeuds: dict) -> list[str]:
259:    non bloquée ne veut pas dire non commencée."""
263:        if d["statut"] in leve or d["statut"] == "bloquée" or d["bloque"]:
265:        libre = True
268:                libre = False
269:        if libre:
351:    # Chaque arête reçoit un couloir : les segments horizontaux vivent dans la bande libre
398:        "pleines sont des dépendances dures, les pointillés des pla
… [913 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '240,280p' tools/verifie_backlog.py; echo '--- parse champs ---'; sed -n '100,145p' tools/verifie_backlog.py", "description": "Read frontier and fiche parsing logic"}`

  ```
if int(noeuds[cible]["prio"][1]) > int(d["prio"][1]):
                    avert.append(
                        f"priorité : {n} ({d['prio']}) dépend de {cible} "
                        f"({noeuds[cible]['prio']}) — l'urgent attend le moins urgent"
                    )

    # 6. les dépendances dures sans fiche : un trou nommé, pas une erreur
    for n, d in noeuds.items():
        for cible, _ in d["dures"]:
            if cible in noeuds and noeuds[cible]["sans_fiche"]:
                avert.append(f"trou : {n} dépend de {cible}, qui n'a pas de fiche")

    controler_index(noeuds, erreurs)
    return erreurs, avert, niveau


def frontiere(noeuds: dict) -> list[str]:
    """Ce sur quoi on peut travailler aujourd'hui : aucune dépendance dure non levée, et
    aucun blocage externe nommé. Une ligne « en cours » ou « partielle » en fait partie :
    non bloquée ne veut pas dire non commencée."""
    leve = {"mesurée", "abandonnée"}
    out = []
    for n, d in sorted(noeuds.items()):
        if d["statut"] in leve or d["statut"] == "bloquée" or d["bloque"]:
            continue
        libre = True
        for cible, _ in d["dures"]:
            if cible in noeuds and noeuds[cible]
… [2201 caractères tronqués]
  ```

### 👤 Utilisateur

background job bash-3994 (bash: timeout 300 python3 tools/tests/linguistique/evaluer_gold.py --json /tmp/etat-a-gold.json > /tmp/etat-a-gold.txt 2>&1; echo "exit=$?"; tail -5 /tmp/etat-a-gold.txt) finished [status: completed, exit code: 0]. Read its output with job_output.

- **job_output** `{"job_id": "bash-3994", "wait": true, "timeout_ms": 120000}`

  ```
exit=0
    "cibles": 236,
    "labels": 236,
    "top1": 235,
    "topk": 234
heuristique all: {"pos": {"exactitude": 0.85, "exactitude_ferme": 0.9295, "exactitude_ouvert": 0.7746, "tokens": 3179, "confusions": {"ADJ": {"ADJ": 62, "NOUN": 68, "VERB": 4}, "ADV": {"ADV": 131, "NOUN": 7, "PREP": 1, "ADJ": 1, "?": 1}, "AUX": {"PREP": 4, "AUX": 119, "?": 3, "NOUN": 1, "VERB": 1}, "CONJ": {"CONJ": 55, "PRON": 28, "?": 13, "PREP": 2}, "DET": {"DET": 586, "?": 2}, "NOUN": {"NOUN": 657, "ADJ": 17, "VERB": 7, "?": 1}, "NUM": {"NUM": 2}, "PONCT": {"?": 25}, "PREP": {"PREP": 114}, "PRON": {"PRON": 430, "?": 30, "CONJ": 1, "DET": 14}, "VERB": {"VERB": 546, "NOUN": 218, "PREP": 2, "ADJ": 2, "?": 16, "AUX": 7, "ADV": 1}}}, "syntagme": {"precision": 0.6715, "rappel": 0.6264, "f1": 0.6482, "tp": 1167, "fp": 571, "fn": 696, "tete": {"precision": 0.8208, "rappel": 0.7203, "f1": 0.7673, "tp": 1342, "fp": 293, "fn": 521}}, "pragmatique": {"acte": 0.9967, "negation": 0.9771, "modalite": 0.9886, "double_sens": 0.9444}, "fraction_semantique": 0.5482}
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "cat /tmp/etat-a-gold.txt 2>/dev/null | tail -40", "description": "Read gold evaluator output"}`

  ```
"top1_taux_span": 0.9958,
    "topk_taux_span": 0.9915,
    "topk_exact": 234,
    "topk_exact_taux": 0.9791,
    "topk_exact_taux_span": 0.9915,
    "exact_taux_span": 0.9958,
    "verbe": {
     "cibles": 157,
     "justes": 157,
     "taux": 1.0
    },
    "nom": {
     "cibles": 79,
     "justes": 78,
     "taux": 0.9873
    },
    "couverture": 0.9874,
    "par_langue": {
     "fr": {
      "cibles": 151,
      "labels": 150,
      "exact": 149,
      "topk": 148,
      "exact_taux_span": 0.9933
     },
     "en": {
      "cibles": 88,
      "labels": 86,
      "exact": 86,
      "topk": 86,
      "exact_taux_span": 1.0
     }
    }
   },
   "attachement_tete": {
    "cibles": 236,
    "labels": 236,
    "top1": 235,
    "topk": 234
heuristique all: {"pos": {"exactitude": 0.85, "exactitude_ferme": 0.9295, "exactitude_ouvert": 0.7746, "tokens": 3179, "confusions": {"ADJ": {"ADJ": 62, "NOUN": 68, "VERB": 4}, "ADV": {"ADV": 131, "NOUN": 7, "PREP": 1, "ADJ": 1, "?": 1}, "AUX": {"PREP": 4, "AUX": 119, "?": 3, "NOUN": 1, "VERB": 1}, "CONJ": {"CONJ": 55, "PRON": 28, "?": 13, "PREP": 2}, "DET": {"DET": 586, "?": 2}, "NOUN": {"NOUN": 657, "ADJ": 17, "VERB": 7, "?": 1}, "NUM": {"NUM": 2
… [512 caractères tronqués]
  ```

- **bash** `{"command": "head -40 reports/rapport-pensee-v12.md; echo '=== file taches verification ==='; sed -n '175,215p' reports/rapport-file-taches.md", "description": "Read v12 verdict and A23 verification section"}`

  ```
# B13 — 222/222 (1,0000) : le dernier marqueur ambigu, et 17 spans inatteignables

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Date** : 2026-11-06 ·
> **Instantané historique** · **Verdict** : ✅ — **la cible de A17 est atteinte**.
> *Depuis, le gold a été corrigé (4 GP sans préposition) : l'état courant est **226/226**, couverture
> **0,9456**, 13 spans — voir [le gold corrigé](rapport-gold-gp-corrige.md).*
> **183/183 portes** : le dernier écart était un **marqueur ambigu** — « when » après un GN est
> une **relative** (« The day when we left »), ailleurs une **subordonnée** (« When it rains »).
> Résultat : **222 labels** sur 239, **exact 222/222 = 1,0000** (fr **136/136**, en **86/86**),
> **couverture 0,9289**, **F1 0,5893** (union ; S 0,5014, chunker 0,6203), tête **0,7392** ;
> **17 spans** restants (8 REL, 5 SUB, 4 GP) — **tous inatteignables** sans corriger le gold ou
> le lexique (12 formes synthétiques, 4 GP du gold sans préposition, une tokenisation `qu'il`).
> **dev 153/153, test 69/69.**
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`AMBIGUES_REL`,
> branche REL/SUB), [`autotest.py`](../tools/pensee/autotest.py) (16 
… [5034 caractères tronqués]
  ```

- **bash** `{"command": "ls -l reports/pensee-produit-bloc-l.json reports/pensee-spans-v7.json reports/pensee-file-taches.json 2>&1; echo '--- test produit ---'; grep -n \"class TestRobustesse\\|def test_\" tools/tests/test_produit.py | head -20", "description": "Check A17/A23/A24 JSON artifacts and product tes … [4 caractères tronqués]`

  ```
-rw-r--r--. 1 stephane stephane 28685  6 nov 10:44 reports/pensee-file-taches.json
-rw-r--r--. 1 stephane stephane 82893  6 nov 11:33 reports/pensee-produit-bloc-l.json
-rw-r--r--. 1 stephane stephane 39678  5 nov 20:50 reports/pensee-spans-v7.json
--- test produit ---
41:    def test_version_et_aide(self) -> None:
52:    def test_analyser_francais(self) -> None:
64:    def test_analyser_anglais(self) -> None:
73:    def test_json_valide_et_deterministe(self) -> None:
90:    def test_rejouer_deterministe(self) -> None:
99:    def test_codes_usage(self) -> None:
109:class TestRobustesse(unittest.TestCase):
112:    def test_surrogate_isole(self):
119:    def test_entrees_non_textuelles(self):
133:    def test_filtrer_donne_une_vue_lineaire(self):
142:    def test_alternative_etiquette_les_chevauchements(self):
  ```

- **bash** `{"command": "grep -n -E \"18 |18\\b|correctif|132|50 phrases|0 plantage\" reports/rapport-produit-bloc-l.md | head -40", "description": "Locate A24 key figures and fixes"}`

  ```
1:# Audit produit du bloc linguistique — 0 plantage sur 50 phrases, 34/50 avec une anomalie de contrat
14:> [`gold_split.py`](../tools/tests/linguistique/gold_split.py) ; **50 phrases libres** écrites pour
19:**En une phrase.** Sur 50 phrases libres, le bloc **ne plante pas**, **ne refuse pas**, **ne rend
32:| syntagme | ❌ | **132 paires** de chevauchement dans **31/50** textes, **188/362** étiquettes ; F1 gold **0,5849** |
36:| compositions | ❌ | refus et contexte perdus, cascade **50/50** appels ; POS **0,7465 < 0,7581** (verdict `cascade_pos` vert par plancher 0,70 depuis `7f73c17f`, pas par correctif) |
41:- **Banc libre** : 50 phrases écrites à la main pour cet audit — 29 françaises, 14 anglaises,
46:  `MockNeuronal`, `Parallele`, `Cascade` pour les compositions. Les 50 phrases passent par
106:  un correctif.
113:## 3. Robustesse hors gold : les 50 phrases libres
141:| **chevauchement de syntagmes** | **132 paires** | **31/50** | f02 : `GP 29-51` et `GP 29-60` ; `GV 80-96` et `GV 90-96` |
148:**Le chevauchement de syntagmes est le problème n° 1.** 132 paires, **188 des 362 étiquettes
215:| parallèle | 1,51 ms | 6,18 ms | 27,22 ms | 0,136 |
218:- **Débit** : 923 phrases/s à 10 
… [1881 caractères tronqués]
  ```

- **bash** `{"command": "grep -n -A25 \"correctifs\" reports/rapport-produit-bloc-l.md | head -80", "description": "Read A24 fixes list"}`

  ```
399:  limites, les 18 correctifs, tous les chiffres et les contrôles.
400-- Harnais local **non committé** : `/tmp/audit_produit_bl/` (`phrases.py`, `audit.py`,
401-  `performance_final.py`, `extra.py`, `construire_json.py`).
402-- Rejeu : `PYTHONPATH=. python3 tools/tests/linguistique/evaluer_gold.py` ;
403-  `bash tools/porte-bloc-linguistique.sh` (verte).
404-- **Aucun fichier existant modifié par cet audit, aucun commit, `reports/README.md` non modifié**
405-  (consigne).
406-
407:## 11. Les 5 correctifs prioritaires
408-
409-1. **P0-1 — Expliciter les alternatives de syntagmes** : 132 paires dans 31/50 textes, 188/362
410-   étiquettes ; ne pas dédupliquer en silence — `meta.alternative` + vue « partition » mesurée
411-   (F1 +0,0292, mais 222 → 208 attachements exacts).
412-2. **P0-2 — Réparer les frontières de phrase** (décimaux, dates, URL/emails, abréviations, espace
413-   initial) et les types `url`/`emoji` morts : une URL crée 3–4 phrases, `12.5` coupe une phrase
414-   en deux fragments (`12.03.2024` en trois), `M./Dr./etc.` duplique la phrase.
415-3. **P0-3 — Compositions** : propager `refus` et `contexte`, rattraper `RefusNeuronal`, garder
416-   `MockNeuronal` sur v
… [748 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '336,365p' reports/rapport-produit-bloc-l.md; echo '=== section 8/9 ==='; sed -n '280,305p' reports/rapport-produit-bloc-l.md", "description": "Read A24 before/after table and sections"}`

  ```
- **Les 6 mutations sont détectées (6/6)** : span hors texte, cible absente, chevauchement,
  confiance 1,7, valeur hors span, fraction incohérente. Le détecteur d'anomalies n'est pas
  complaisant ; noter que l'annotation de base porte déjà un chevauchement, donc le test de
  mutation ajoute une anomalie à un état déjà imparfait.
- **Le chunker seul ne chevauche pas** : 0 paire avec `segmenter_s=False, union=False`, contre 132
  avec le générateur S + union. Le défaut vient bien de la composition des segments, pas du
  détecteur.
- **La déduplication simulée** (`_supprimer_chevauchements`, politique actuelle de la fusion) :

| base | paires | syntagmes | attachements | F1 | P | R | tête | exact | couverture |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 50 phrases, avant | 132 | 362 | 265 | — | — | — | — | — | — |
| 50 phrases, après | **0** | 292 | 215 | — | — | — | — | — | — |
| gold 612, avant | — | — | — | **0,5849** | 0,6292 | 0,5464 | 0,7336 | **222** | **0,9289** |
| gold 612, après | — | — | — | **0,6141** | 0,7283 | 0,5309 | 0,7432 | **208** | **0,8703** |

La déduplication **gagne 0,0292 de F1 et 0,0096 de tête**, mais **perd 14 spans d'attachement
exacts** (222 
… [3255 caractères tronqués]
  ```

- **bash** `{"command": "head -45 docs/pilotage/backlog/A3.2-granularite.md; echo '=== A3.3 ==='; head -45 docs/pilotage/backlog/A3.3-seuil.md", "description": "Read A3.2 and A3.3 fiches"}`

  ```
# A3.2 — Granularité du flux : par couche, par bloc, par expert

> **Statut** : mesurée · **Priorité** : P2 · **Programme** : A · **Dépend de** : A3
> **Ligne de roadmap** : A3.2 · **Fiche de résultat** : archive
> [`roadmap-detail-2026-10-29.md`](../../archive/roadmap-detail-2026-10-29.md) · rapports
> [`compacite-trace`](../../../reports/rapport-compacite-trace.md) et
> [`engram-etat`](../../../reports/rapport-engram-etat.md).
> **Résumé** : ce qui traverse le lien est une **liste valuée** (indices par écarts, valeurs
> i16, une échelle par bloc), pas un vecteur dense.

## Le besoin

Un flux d'activations transporté en dense coûte 3,5 ko par jeton. La vision dit que le coût
doit être proportionnel à l'**activité** : seules les activations non nulles doivent voyager,
et leur précision doit suivre leur importance. La granularité (couche, bloc, expert) décide de
ce qui est encodé ensemble.

## L'état

**Mesurée** — listes i16, échelles **par bloc de 32 canaux**, indices par écarts : **1 608
octets par flux** à 256 jetons ; le mode « lot en listes » : **1,5 ko/jeton contre 3,5 en
dense (÷2,3)**. La liste est réversible et rejouée par la porte
[`porte-flux`](../../../tools/porte-flux.
… [2786 caractères tronqués]
  ```

- **bash** `{"command": "grep -n -E \"^\\| \\*\\*A[1-8]|^## A|A[1-8]\\b\" docs/archive/roadmap-detail-2026-10-29.md | head -60", "description": "Locate A details in archived roadmap"}`

  ```
28:| **A — le moteur** | A1–A8 : les formats, le placement, le transport, le rejeu, les matériels | A3.4 (Colab), A5.4 (FPGA), A6.2 (MoE local) — **bloqués** |
39:### A1 — Observer et régler, neurone par neurone
45:| A1.1 | **Format de trace** (DRVF v2/v3) : par couche et position, les neurones actifs (indice + valeur) | ✅ | 132 Mo pour 512 jetons (258 ko/jeton) et +8 % de temps ; la v3 (i8, échelle par bloc de 32) fait 45,1 Mo contre 66,4, au prix de +0,074 % de perplexité au rejeu |
46:| A1.2 | **Diff par couche** : où deux exécutions divergent, à quel jeton, quels neurones | ✅ | KV f32 contre int8 → première divergence **couche 1, jeton 0**, 896 neurones, 2,9e-3 de dynamique ; couche la plus touchée : FFN 2 |
47:| A1.3 | **Le format EST le contrat d'échange** (A3) : versionné, en-tête + paires | ✅ | codec de référence : aller-retour identique sur 132 Mo ; le rejeu redonne les mêmes logits |
48:| A1.4 | **Profilage par neurone** : densité par couche, part des 10 % les plus forts, neurones dominants | ✅ | densité **20 à 56 %** selon la couche ; top 10 % → **33,1 %** de la magnitude ; **0,08 %** de neurones chauds > 90 % du temps |
49:| A1.5 | **La décision par couche** : la quanti
… [10393 caractères tronqués]
  ```

- **bash** `{"command": "ls -lt reports/ | head -30; echo '--- gold reports ---'; ls reports/ | grep -Ei 'gold|pensee-v1[2-9]|spans'", "description": "List latest reports and gold-related fiches"}`

  ```
total 20320
-rw-r--r--. 1 stephane stephane   23652  6 nov 20:52 README.md
-rw-r--r--. 1 stephane stephane    3765  6 nov 20:49 rapport-partition-integree.md
-rw-------. 1 stephane stephane   41402  6 nov 20:46 rapport-partition-syntagmes.md
-rw-r--r--. 1 stephane stephane    3949  6 nov 20:42 rapport-pos-r4-integre.md
-rw-r--r--. 1 stephane stephane   44454  6 nov 20:40 pensee-partition-syntagmes.json
-rw-r--r--. 1 stephane stephane   95817  6 nov 20:39 INDEX.md
-rw-r--r--. 1 stephane stephane     959  6 nov 20:39 pensee-partition-integrees.json
-rw-r--r--. 1 stephane stephane   33905  6 nov 20:38 rapport-pos-r4.md
-rw-r--r--. 1 stephane stephane  171282  6 nov 20:38 pensee-pos-r4.json
-rw-r--r--. 1 stephane stephane     816  6 nov 20:25 pensee-frontieres-integrees.json
-rw-r--r--. 1 stephane stephane    3328  6 nov 20:25 rapport-frontieres-integrees.md
-rw-r--r--. 1 stephane stephane  142486  6 nov 20:18 pensee-frontieres-phrase.json
-rw-r--r--. 1 stephane stephane   36124  6 nov 20:18 rapport-frontieres-phrase.md
-rw-r--r--. 1 stephane stephane     676  6 nov 20:17 pensee-pos-r4-integration.json
-rw-r--r--. 1 stephane stephane     778  6 nov 19:56 pensee-composition-sans-perte.j
… [2407 caractères tronqués]
  ```

- **bash** `{"command": "head -30 reports/rapport-gold-gp-corrige.md 2>/dev/null; echo '=== v13? ==='; head -25 reports/rapport-pensee-v13.md 2>/dev/null", "description": "Read latest gold correction report"}`

  ```
# B13 — le gold corrigé : 4 GP retrouvés, exact 226/226, couverture 0,9456

> **Ligne de roadmap** : **B13** (moteur de pensée) · **Date** : 2026-11-06 · **Verdict** : ✅
> **Un défaut du générateur de gold**, pas du bloc : dans le mode `sv` de
> `gold_synthetique.py`, le span d'un GP partait **après** la préposition (`i = v + index(prep) + 1`)
> alors que le mode `sv_gp` l'inclut (`i - 1`). Quatre GP du gold étaient donc **sans préposition** —
> inatteignables par construction. Corrigé, le gold garde **les mêmes 160 phrases** (mêmes ids,
> mêmes segments) et **4 GP** sont réparés : l'attachement passe de **222/222 à 226/226**,
> la **couverture de 0,9289 à 0,9456**, les **spans perdus de 17 à 13** (les 4 GP ont disparu de
> la liste). **dev 155/155, test 71/71.**
>
> **Dispositif** : [`gold_synthetique.py`](../tools/tests/linguistique/gold_synthetique.py) (mode
> `sv`), [`gold_synthetique.json`](../tools/tests/linguistique/gold_synthetique.json) régénéré
> (graine 42, 160 phrases), [`autotest.py`](../tools/pensee/autotest.py) (14 assertions) ;
> JSON [`pensee-gold-gp-corrige.json`](pensee-gold-gp-corrige.json).

## 1. Le défaut

```python
# avant (mode sv) : le span commence après 
… [443 caractères tronqués]
  ```

- **job_output** `{"job_id": "bash-3979", "wait": true, "timeout_ms": 120000}`

  ```
✅ T174 convention documentée convention : ['GN', 'GP', 'GV', 'REL', 'SUB'] documentée
  ✅ T175 audit attachement audit : 14/14, écarts 0
  ✅ T176 segment précédent segment précédent : s052 ouvre, s012 écoute
  ✅ T177 candidats têtes   candidats têtes : 234/236 (0.9915)
  ✅ T178 cache chunker     cache : 1 chunking chunker, 1 défaut (1+2S avant)
  ✅ T179 multi-cibles      multi-cibles : exact 235/236, exact_any 235/236
  ✅ T180 par langue        langues : fr 149/150, en 86/86 (86/88 labels)
  183/183 portes tenues
exit=0
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "grep -n -E \"183|portes|172|spans\" reports/rapport-pensee-v12.md | head -20; echo '=== current partition report ==='; head -30 reports/rapport-partition-integree.md", "description": "Check autotest and latest partition state"}`

  ```
1:# B13 — 222/222 (1,0000) : le dernier marqueur ambigu, et 17 spans inatteignables
6:> **0,9456**, 13 spans — voir [le gold corrigé](rapport-gold-gp-corrige.md).*
7:> **183/183 portes** : le dernier écart était un **marqueur ambigu** — « when » après un GN est
11:> **17 spans** restants (8 REL, 5 SUB, 4 GP) — **tous inatteignables** sans corriger le gold ou
36:| spans perdus | 18 | **17** (8 REL, 5 SUB, 4 GP) |
42:- **Les 17 spans restants sont inatteignables** : 12 formes synthétiques (le lexique du gold
57:- **Les 17 spans** : non prédits, donc hors mesure d'attachement.
70:1. **Les 17 spans** : corriger le gold (GP sans préposition) et étendre le lexique réel, ou les
77:- [`autotest.py`](../tools/pensee/autotest.py) — 183/183.
=== current partition report ===
# B13 — la partition des syntagmes : les alternatives sont étiquetées, les mesures ne bougent pas

> **Ligne de roadmap** : **B13** (produit) · **Date** : 2026-11-06 · **Verdict** : ✅
> **Le P0-3 est fermé sans perte** : les **239 paires** de chevauchement des deux audits sont
> **toutes** des paires S × chunker (53,1 % de S qui contient le chunker, 33,5 % l'inverse,
> 2,5 % de mêmes bornes, 10,9 % de croisements). Le mode
… [1297 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"TETE_4BIT\\|perte\" drave-core/src/placement.rs | head -30; echo '--- script head ---'; head -40 tools/mesure_lot_disque.sh", "description": "Inspect head 4-bit constant and lot script"}`

  ```
105:/// Une précision et **son coût mesuré** : les octets par valeur et la perte de
111:    pub perte_ppl: f64,
114:/// Le f32 : la référence, aucune perte.
115:pub const F32: Precision = Precision { nom: "f32", octets_par_valeur: 4.0, perte_ppl: 0.0 };
117:pub const INT8_TARDIF: Precision = Precision { nom: "int8 tardif", octets_par_valeur: 1.0, perte_ppl: 0.03 };
119:pub const INT4_TARDIF: Precision = Precision { nom: "int4 tardif", octets_par_valeur: 0.5, perte_ppl: 2.7 };
122:pub const TETE_4BIT: Precision = Precision { nom: "tête 4 bits", octets_par_valeur: 0.5, perte_ppl: 10.0 };
124:pub const INT4_GLOBAL: Precision = Precision { nom: "int4 global", octets_par_valeur: 0.5, perte_ppl: 364.0 };
127:pub const PRECISIONS: [Precision; 5] = [F32, INT8_TARDIF, INT4_TARDIF, TETE_4BIT, INT4_GLOBAL];
129:/// Choisit **(support, précision)** : le moins cher **dont la perte tient dans
133:/// ici on répond à « où ça tient **sans payer plus que `perte_max`** ». Un 4 bits
136:pub fn choisir_avec_perte(
141:    perte_max: f64,
145:        if p.perte_ppl > perte_max {
160:/// La perte **mesurée** de l'int8 sur le KV selon la couche (A5.3, 0,5 B, 255 jetons) :
163:pub fn perte_kv_int8(couche:
… [2768 caractères tronqués]
  ```

- **bash** `{"command": "cargo --version 2>&1; rustc --version 2>&1; wc -l drave-core/src/placement.rs", "description": "Check Rust toolchain availability"}`

  ```
cargo 1.99.1 (5f94df478 2026-08-27)
rustc 1.99.1 (58cf8f9c3 2026-10-13)
253 drave-core/src/placement.rs
  ```

- **bash** `{"command": "CARGO_TARGET_DIR=/tmp/etat-a-target timeout 300 cargo test --manifest-path drave-core/Cargo.toml placement -- --nocapture 2>&1 | tail -25; echo \"exit=${PIPESTATUS[0]}\"", "description": "Run placement unit tests in /tmp target", "run_in_background": true}`

  ```
started background job bash-4046
  ```

- **bash** `{"command": "ls -lh models/ 2>/dev/null | head; find /home/stephane/Data13TB/stephane/GitHub/Qtrinet -maxdepth 3 -iname '*.gguf' -printf '%p %s\\n' 2>/dev/null | head -10", "description": "Locate local GGUF models"}`

  ```
total 844M
-rw-r--r--. 1 stephane stephane 337M 25 sep 17:13 Qwen2.5-0.5B-Q4_0.gguf
-rw-r--r--. 1 stephane stephane 507M 25 sep 16:52 Qwen2.5-0.5B-Q8_0.gguf
drwxr-xr-x. 1 stephane stephane  138 15 oct 09:02 vision
/home/stephane/Data13TB/stephane/GitHub/Qtrinet/models/Qwen2.5-0.5B-Q8_0.gguf 531068480
/home/stephane/Data13TB/stephane/GitHub/Qtrinet/models/Qwen2.5-0.5B-Q4_0.gguf 352972352
/home/stephane/Data13TB/stephane/GitHub/Qtrinet/models/vision/Qwen2-VL-2B-Instruct-Q4_K_M.gguf 986046944
/home/stephane/Data13TB/stephane/GitHub/Qtrinet/models/vision/mmproj-Qwen2-VL-2B-Instruct-Q8_0.gguf 709883360
  ```

- **bash** `{"command": "sed -n '1,80p' tools/porte-flux.sh", "description": "Inspect porte-flux script"}`

  ```
#!/bin/bash
# Porte du DÉCOUPAGE : deux nœuds, un petit modèle, cinq modes de flux.
#
# Pourquoi elle existe : le défaut de la `pre` reçue (sprint 13) a vécu jusqu'à
# ce qu'on compare des tenseurs à la main sur un modèle de 365 Go et quatre
# minutes par passe. Aucune porte ne couvrait un COUPLE DE NŒUDS ; celle-ci le
# fait en quelques secondes, sur Qwen2.5-0.5B, et elle attrape trois familles de
# défauts d'un coup :
#   · la couture (l'état rendu par le second nœud doit être celui de la passe
#     complète — pour les modes exacts, au bit près) ;
#   · le cadriciel de flux lui-même (en-tête, mode, compte `np`, positions) ;
#   · l'accord entre les modes (un mode avec perte ne doit pas coûter plus que
#     son codec).
#
# Les modes 0 (f32 dense), 1 et 3 (lot dense) sont EXACTS : écart attendu 0,00e0.
# Les modes 2 et 4 passent par le codec quantifié (indices par écarts, valeurs i8,
# une échelle par bloc de 32 canaux) : leur écart est une perte assumée, et la
# porte vérifie qu'il reste sous un plafond mesuré, pas qu'il est nul.
#
#   THREADS=N (défaut 8) : nombre de threads ; A8.3d a montré que l'écart de lot
#   survit à 1 thread — ce n'est pas le pool, c'est le noyau par lot
… [2481 caractères tronqués]
  ```

### 👤 Utilisateur

background job bash-4046 (bash: CARGO_TARGET_DIR=/tmp/etat-a-target timeout 300 cargo test --manifest-path drave-core/Cargo.toml placement -- --nocapture 2>&1 | tail -25; echo "exit=${PIPESTATUS[0]}") finished [status: completed, exit code: 0]. Read its output with job_output.

- **job_output** `{"job_id": "bash-4046", "wait": true, "timeout_ms": 60000}`

  ```
warning: the `ids:` in this pattern is redundant
    --> src/main.rs:1751:9
     |
1751 |         ids: mut ids, ids_file, prompt, n: n_new, temp, top_p, topk, rep_pen, hist,
     |         ^^^^^^^^^^^^ help: use shorthand field pattern: `mut ids`
     |
     = note: `#[warn(non_shorthand_field_patterns)]` on by default

warning: `drave-core` (bin "drave" test) generated 65 warnings (run `cargo fix --bin "drave" -p drave-core --tests` to apply 37 suggestions)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 8.57s
     Running unittests src/main.rs (/tmp/etat-a-target/debug/deps/drave-0fde18393e99a236)

running 8 tests
test placement::tests::choisir_respecte_la_place ... ok
test placement::tests::la_regle_place_perte_choisit_le_kv_par_couche ... ok
test placement::tests::la_perte_decide_aussi ... ok
test placement::tests::la_tete_en_4_bits_est_refusee_par_un_budget_de_5_pour_cent ... ok
test placement::tests::la_vram_est_le_support_le_moins_cher_pour_un_gros_lecteur ... ok
test placement::tests::le_cout_est_proportionnel_aux_octets ... ok
test placement::tests::un_budget_nul_interdit_toute_quantification ... ok
test placement::tests::le_kv_tient_si_la_reserve_est_re
… [153 caractères tronqués]
  ```

- **bash** `{"command": "ls -l drave-core/target/release/drave 2>&1; nvidia-smi --query-gpu=index,memory.used,memory.total,utilization.gpu --format=csv,noheader 2>&1 | head", "description": "Check release binary and GPU state"}`

  ```
-rwxr-xr-x. 2 stephane stephane 3187480 30 oct 08:39 drave-core/target/release/drave
0, 154 MiB, 16384 MiB, 0 %
1, 4 MiB, 16384 MiB, 0 %
  ```

### 🤖 Assistant

⏵ Rejeu d'une porte A8.3a en régime 1 % pour vérifier le chiffre épinglé
Le code compile et les 8 tests de placement passent ; je lance `porte-flux` en régime 1 %.

- **bash** `{"command": "DRAVE_PERTE_MAX=1 timeout 300 bash tools/porte-flux.sh > /tmp/etat-a-porte-flux.txt 2>&1; echo \"exit=$?\"; tail -20 /tmp/etat-a-porte-flux.txt", "description": "Run porte-flux with 1% loss regime", "run_in_background": true}`

  ```
started background job bash-4059
  ```

- **bash** `{"command": "cat reports/a83a-flux.json | python3 -c \"import json,sys; d=json.load(sys.stdin); print(d['gates'], d['decision'])\"; echo '--- a80 audit json ---'; python3 -c \"import json; d=json.load(open('reports/a80-audit-final.json')); print(type(d), list(d)[:10])\"", "description": "Inspect A8. … [28 caractères tronqués]`

  ```
{'f32': 'exit 0', 'perte1': 'exit 0'} A8.3a flux fait ; pont/coupe restent ; A8.3 opt-in
--- a80 audit json ---
<class 'dict'> ['date', 'ligne', 'total', 'epinglees', 'restantes', 'pinned', 'restantes_categories', 'verdict', 'controle', 'limites']
  ```

- **bash** `{"command": "python3 -c \"\nimport json\nd=json.load(open('reports/a80-audit-final.json'))\nprint('date',d['date']); print('total',d['total']); print('epinglees',len(d['epinglees']) if isinstance(d['epinglees'],list) else d['epinglees']); print('pinned',d.get('pinned')); print('restantes',d.get('res … [92 caractères tronqués]`

  ```
date 2026-10-30
total 33
epinglees 19
pinned ['adaptateur-sortie', 'budget', 'bus-socket', 'bus', 'c4-retard', 'consolidation', 'coupe', 'cycle-c2', 'delais', 'flux', 'fusion', 'gain', 'pannes', 'pont', 'profondeur-routee', 'reflexe', 'reparti-moteur', 'topologie', 'trace']
restantes 14
verdict 19/33 épinglées ; 3 comparatifs intra-run, 2 rouges qualifiées, 1 verte sans PPL, 8 sans PPL
  ```

- **bash** `{"command": "python3 -c \"\nimport json\nfor f in ['a26-bilan.json','a83-defaut.json','a83b-decision.json','a83c-lot.json','a83d-lot-threads.json']:\n    d=json.load(open('reports/'+f))\n    print('==',f)\n    print({k:v for k,v in d.items() if k in ('date','ligne','verdict','decision','controle')}) … [58 caractères tronqués]`

  ```
== a26-bilan.json
{'date': '2026-10-29', 'ligne': 'A2.6', 'verdict': 'partielle', 'controle': 'choisir_avec_perte refuse la tête 4 bits à 5 % (test) ; sans MoE local, les experts ne sont pas mesurables'}
== a83-defaut.json
{'date': '2026-10-29', 'ligne': 'A8.3', 'verdict': 'opt-in conserve'}
== a83b-decision.json
{'date': '2026-10-29', 'ligne': 'A8.3b/c', 'decision': 'opt-in maintenu', 'controle': '24 exécutions ctx × lot × régime ; lot 1 = mode 0 ; lot ≥2 identique'}
== a83c-lot.json
{'date': '2026-10-29', 'ligne': 'A8.3c', 'verdict': 'non-monotonie expliquée : effet par chemin, pas anomalie de la règle'}
== a83d-lot-threads.json
{'ligne': 'A8.3d', 'date': '2026-10-30', 'verdict': "le lot n'est pas les threads : l'ecart de 1,90 % survit a 1 thread"}
  ```

- **bash** `{"command": "grep -rn \"A3B\\|OLMoE\\|DeepSeek-V2-Lite\\|Mixtral\\|MoE local\" docs/pilotage/backlog/A6.2-moe-local.md reports/rapport-a26-bilan.md docs/pilotage/roadmap.md reports/rapport-a83c-lot.md 2>/dev/null | head -20; echo '--- model files ---'; find models data -maxdepth 4 -iname '*moe*' -o  … [97 caractères tronqués]`

  ```
docs/pilotage/backlog/A6.2-moe-local.md:1:# A6.2 — Routage MoE appris (MoE local)
docs/pilotage/backlog/A6.2-moe-local.md:3:> **Statut** : bloquée · **Priorité** : P3 · **Programme** : A · **Dépend de** : A6 · **Bloqué par** : aucun MoE local dans 16 Go de VRAM
docs/pilotage/backlog/A6.2-moe-local.md:10:Aucun MoE local ne tient dans 16 Go de VRAM ; le routage appris reste donc non mesuré.
reports/rapport-a26-bilan.md:5:> **A6.2** (pas de MoE local). A2.6 ne peut pas être « complétée » sans cette brique.
reports/rapport-a26-bilan.md:18:| experts | 🧱 bloqué | **A6.2** — pas de MoE local à router |
reports/rapport-a26-bilan.md:25:- Sans MoE local, les experts ne sont **pas mesurables** : ce n’est pas un échec de la règle, c’est
reports/rapport-a26-bilan.md:39:- **Les experts** ne sont pas mesurables sans A6.2 ; le jour où le MoE local existe, A2.6 rouvre.
docs/pilotage/roadmap.md:150:| **A6** | apprendre des flux : capteur hebbien, routage MoE, [élagage](../theorie/glossaire/entrees/elagage.md) | ✅ / ⏳ | **A6.2 bloqué** (pas de MoE local) ; A6.1/A6.3 ont rendu leurs négatifs |
docs/pilotage/roadmap.md:341:- **bloqué, nommé** : B1.5 (corpus d'articles), A3.4 (compte Colab), A5.4 (FPGA)
… [1205 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"Qwen3-30B-A3B\" reports/*.md | head -10; echo '--- df ---'; df -h /home/stephane/Data13TB | tail -1", "description": "Find Qwen3-30B-A3B evidence and disk space"}`

  ```
reports/aiguille-30b.md:1:# aiguille v2 — /home/stephane/Data13TB/stephane/modeles/gguf/Qwen3-30B-A3B-Instruct-2507-Q4_K_M.gguf
reports/INDEX.md:10:| [aiguille-30b.md](aiguille-30b.md) | aiguille v2 — /home/stephane/Data13TB/stephane/modeles/gguf/Qwen3-30B-A3B-Instruct-2507-Q4_K_M.gguf |
reports/rapport-a83c-lot.md:40:Mesuré sur Qwen3-30B-A3B : PPL **19,143 contre 19,172** (0,15 %), argmax identique sur
reports/rapport-aiguille.md:13:échec sur Qwen3-30B-A3B. Le test a été arrêté à l'époque, faute de budget.
reports/rapport-aiguille.md:61:* **Qwen3-30B-A3B-Instruct-2507** (MoE, 3 B actifs), contexte 2048, `--lot 256`,
reports/rapport-aiguille.md:71:| **Qwen3-30B-A3B** | 2 048 | ✅ | ✅ | ✅ | 651-691 |
reports/rapport-aiguille-topk.md:30:| Qwen3-30B-A3B | 2 048 | ~670 |
reports/rapport-c9-echange-experts.md:15:> Protocole : Qwen3-30B-A3B (48 couches, 128 experts, 8 utilisés), `--ppl --ctx 512 --limit 32`,
reports/rapport-cache-experts-vram.md:47:| | K3 (896 experts/couche, 16/jeton) | Qwen3-30B-A3B (128, 8/jeton) |
reports/rapport-chargement-paresseux.md:24:| Qwen3-30B-A3B | défaut (auto) | **26,95 s** | 2,69 Go |
--- df ---
/dev/mapper/system-root   11T  9,0T  1,9T  83% /home/stephane
… [9 caractères tronqués]
  ```

### 👤 Utilisateur

background job bash-4059 (bash: DRAVE_PERTE_MAX=1 timeout 300 bash tools/porte-flux.sh > /tmp/etat-a-porte-flux.txt 2>&1; echo "exit=$?"; tail -20 /tmp/etat-a-porte-flux.txt) finished [status: completed, exit code: 0]. Read its output with job_output.

- **job_output** `{"job_id": "bash-4059", "wait": true, "timeout_ms": 60000}`

  ```
exit=0
  mode 0 — f32 dense               0.00e0  ✅  (réf 58.3200 / deux nœuds 58.3200)
  mode 1 — listes quantifiées     0.00e0  ✅  (réf 58.3200 / deux nœuds 58.3200)
  mode 2 — listes par blocs        1.14e-1  ✅  (réf 58.3200 / deux nœuds 64.9975)
  mode 3 — lot dense f32           0.00e0  ✅  (réf 62.7357 / deux nœuds 62.7357)
  mode 4 — lot en listes           3.49e-2  ✅  (réf 62.7357 / deux nœuds 64.9228)
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "ls -lh /home/stephane/Data13TB/stephane/modeles/gguf/Qwen3-30B-A3B-Instruct-2507-Q4_K_M.gguf 2>&1; echo '--- chargement paresseux ---'; sed -n '1,45p' reports/rapport-chargement-paresseux.md", "description": "Verify local MoE model and lazy-load report"}`

  ```
-rw-r--r--. 1 stephane stephane 18G 25 sep 08:26 /home/stephane/Data13TB/stephane/modeles/gguf/Qwen3-30B-A3B-Instruct-2507-Q4_K_M.gguf
--- chargement paresseux ---
# Le chargement construisait 2,7 Go de « listes » que personne ne lisait

> Campagne : **machine et moteur** · expérience 01 — le coût du chargement
> Question : une passe `--ppl` sur Qwen3-30B passe **27 s** à charger avant de calculer 1 s par
> jeton. Que fait le chargeur pendant ces 27 s, et le faut-il ?
> Verdict : **non, il ne le faut pas.** Le chargeur construisait **par défaut** la représentation
> « listes » des projections (`PushMat`), **2,69 Go** pour Qwen3-30B et **0,71 Go** pour
> Qwen2.5-0.5B — alors que le chemin qui l'utilise n'est choisi que si la densité d'activation
> passe sous `seuil_push` (0,22), et que les passes mesurées ne l'utilisent **jamais**
> (« dont en listes : 0,0 M », dit le moteur lui-même). Rendre cette construction **paresseuse**
> (au premier usage réel) fait passer le chargement de **26,95 s à 7,36 s** (Qwen3-30B) et de
> **6,85 s à 0,60 s** (Qwen2.5-0.5B), **sans déplacer un chiffre**.
> Date réelle : 2026-10-12, 22 h 30-22 h 47 HAE (heure lue sur la machine ; source : git, commits `
… [1695 caractères tronqués]
  ```

- **bash** `{"command": "head -35 reports/rapport-c9-echange-experts.md; echo '=== cache experts ==='; head -35 reports/rapport-cache-experts-vram.md", "description": "Read MoE exchange and cache reports"}`

  ```
# C9 sur un modèle routé : échanger les choix d'experts ne transfère RIEN d'utilisable

> Campagne : **cerveau** · expérience : `--echange experts` (la « variante la plus plausible » du § 6.8)
> Question : la latéralité entre deux instances jumelles ne gagnait rien en échangeant des **états**
> (`rapport-c9-lateralite.md`). La suite nommée était d'échanger des **choix d'experts** sur un
> modèle **routé** : là, les deux instances voient des choses différentes, donc leurs routages
> pourraient porter une information que l'autre n'a pas.
> Verdict : **non — et la mesure a d'abord menti.** Le premier essai donnait **×0,81** (une
> amélioration de 19 % !) en imposant à A le routage de B à la dernière couche. Les contrôles l'ont
> démonté : **tout** routage différent y fait varier la perplexité de ±20 à 50 %, **le signe dépend
> du texte** (A : ×0,81 · A2 : ×1,46 · B en sens inverse : ×1,26), et l'ordre « le routage réel fait
> moins de mal que l'aléatoire » ne tient que **2 fois sur 3** (le sens inverse l'inverse : aléatoire
> ×0,94 contre réel ×1,26). Il n'y a **pas** de gain latéral.
> Date réelle : **2026-10-13, 12 h 57-13 h 20 HAE** (heure lue sur la machine)
> Protocole : Qwen3-30
… [2731 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"A6.2\\|routage\" reports/rapport-c9-echange-experts.md reports/rapport-cache-experts-vram.md reports/rapport-chargement-paresseux.md | head -20; echo '--- expert flags ---'; grep -n \"expert\" drave-core/src/main.rs | head -20", "description": "Check MoE routing support and A … [14 caractères tronqués]`

  ```
reports/rapport-c9-echange-experts.md:6:> modèle **routé** : là, les deux instances voient des choses différentes, donc leurs routages
reports/rapport-c9-echange-experts.md:9:> amélioration de 19 % !) en imposant à A le routage de B à la dernière couche. Les contrôles l'ont
reports/rapport-c9-echange-experts.md:10:> démonté : **tout** routage différent y fait varier la perplexité de ±20 à 50 %, **le signe dépend
reports/rapport-c9-echange-experts.md:11:> du texte** (A : ×0,81 · A2 : ×1,46 · B en sens inverse : ×1,26), et l'ordre « le routage réel fait
reports/rapport-c9-echange-experts.md:16:> textes A/B/A2 tirés de trois fenêtres du même corpus ; routage **capturé** par
reports/rapport-c9-echange-experts.md:28:**L'invariant, et il a fallu le rendre EXACT** : imposer à une instance **son propre** routage doit
reports/rapport-c9-echange-experts.md:41:| A avec **son** routage (référence) | **37,2013** | ×1,00 |
reports/rapport-c9-echange-experts.md:42:| A + le routage de **B** (autre texte) | **3 445,03** | **×92,6** |
reports/rapport-c9-echange-experts.md:43:| A + routage **aléatoire** | 13 958,96 | ×375 |
reports/rapport-c9-echange-experts.md:44:| A + routage de B **décalé d'une co
… [3015 caractères tronqués]
  ```

- **bash** `{"command": "timeout 180 bash tools/porte-bloc-linguistique.sh > /tmp/etat-a-porte-bloc.txt 2>&1; echo \"exit=$?\"; tail -15 /tmp/etat-a-porte-bloc.txt", "description": "Run language block gate", "run_in_background": true}`

  ```
started background job bash-4101
  ```

- **bash** `{"command": "timeout 180 bash tools/porte-produit.sh > /tmp/etat-a-porte-produit.txt 2>&1; echo \"exit=$?\"; tail -20 /tmp/etat-a-porte-produit.txt", "description": "Run product gate", "run_in_background": true}`

  ```
started background job bash-4102
  ```

- **bash** `{"command": "git log --oneline -15", "description": "List latest commits"}`

  ```
9e4cde3b README — LA SECTION « ESSAYEZ » : LA CLI drave, LE FORMAT VERSIONNÉ, LA PORTE PRODUIT, LES CHIFFRES DU 06/11
ea1a68a2 ÉTAT — T0 DANS LE BUDGET (NUIT DES P0)
bb67dd59 ÉTAT ET JOURNAL — LA NUIT DES P0 : POS 85,00 %, ATTACHEMENT 235/236, FRONTIÈRES 0/40, PARTITION ÉTIQUETÉE, CONTRAT V1
d31aa9a2 PRODUIT — --partition DANS LA CLI (alternative PAR DÉFAUT, filtrer EN OPTION), 10 TESTS, DOC À JOUR
6a1148c2 B13 — L'ÉLISION « que » → « qu » DANS LE TEST DES MARQUEURS (AUCUN EFFET MESURÉ, ROBUSTESSE) ; 183/183
4e6de0ee P0-3 — LES RAPPORTS FINAUX DE LA PARTITION (MESURES ÉPINGLÉES À fa1b0c6e) ; README DANS LE BUDGET
97f41554 B13 — LE STRIP DE LA FUSION : PLUS DE RÉFÉRENCE MORTE VERS UN SEGMENT DÉDUPLIQUÉ ; MESURES INCHANGÉES (0,85 / 0,6482 / 235-236)
5c0d5329 FICHE — LES PERTES DE R4 DITES HONNÊTEMENT (5/8 FAUX EN FRANÇAIS, NOMS NUS, PARTICIPES) ; README DANS LE BUDGET T1
015d7c56 B13 — LA PARTITION DES SYNTAGMES (P0-3) : meta.alternative PAR DÉFAUT (MESURES INCHANGÉES), filtrer EN OPTION (F1 +0,047) ; outside/feel CORRIGÉS, POS 85,00 %
ba39a7b1 B13 — LES FRONTIÈRES DE PHRASE (P0-4) : 32/40 TEXTES FAUX → 0/40, 102 → 59 PHRASES, GOLD INCHANGÉ (POS 84,96, 235/236) ; 183/183
5c5d3b52 B13
… [592 caractères tronqués]
  ```

- **bash** `{"command": "grep -rln \"3 spans\" reports/*.md | head; echo '---'; grep -rn \"3 spans\\|235/236\" reports/rapport-morphologie-verbes.md reports/rapport-pensee-v12.md reports/rapport-partition-integree.md 2>/dev/null | head -10", "description": "Locate current 3-spans state report"}`

  ```
reports/INDEX.md
reports/rapport-audit-attachement.md
reports/rapport-audit-r1r3.md
reports/rapport-audit-v10.md
reports/rapport-audit-v7.md
reports/rapport-coherence-fiches.md
reports/rapport-coherence-fiches-v7.md
reports/rapport-dev-test-v7.md
reports/rapport-gold-gp-corrige.md
reports/rapport-morphologie-verbes.md
---
reports/rapport-morphologie-verbes.md:7:> (~60 verbes du français usuel), l'attachement passe de **226/226 (couv. 0,9456, 13 spans)** à
reports/rapport-morphologie-verbes.md:8:> **235/236 (couv. 0,9874, 3 spans)** ; la **F1 syntagmes** de 0,6198 à **0,6474** ; le POS reste
reports/rapport-morphologie-verbes.md:41:| exact / labels | 226/226 | **235/236** |
reports/rapport-morphologie-verbes.md:56:- **Il reste 3 spans** : `g017` (arbitrage d'adverbe), `r035` (relative zéro), `r264` (tokenisation
reports/rapport-morphologie-verbes.md:63:- **Contrôle négatif** : les 3 spans restants sont antérieurs à la règle et inchangés.
reports/rapport-morphologie-verbes.md:71:- **Les 3 spans restants** ne sont pas près de tomber (relative zéro, tokenisation).
reports/rapport-pensee-v12.md:6:> **0,9456**, 13 spans — voir [le gold corrigé](rapport-gold-gp-corrige.md).*
reports/rappo
… [331 caractères tronqués]
  ```

- **bash** `{"command": "git status --porcelain | grep -E '^.. reports/' | head -20; echo '--- HEAD now ---'; git log -1 --format='%h %s'", "description": "Check reports modifications in tree"}`

  ```
M reports/pensee-coherence-fiches-v7.json
 M reports/pensee-dev-test-v10.json
 M reports/pensee-quatre-modes.json
 M reports/rapport-audit-v7.md
 M reports/rapport-coherence-fiches-v7.md
 M reports/rapport-dev-test-v10.md
M  reports/rapport-pensee-v12.md
 M reports/rapport-spans-chunker.md
?? reports/rapport-s-paragraphes.md
--- HEAD now ---
bfd98892 DOC PRODUIT — RESYNCHRONISÉE : POS 85,00 %, F1 0,6482, ATTACHEMENT 235/236, GELÉ 85,32 / 0,6511 ; SORTIE D'EVALUER REJOUÉE
  ```

### 👤 Utilisateur

background job bash-4101 (bash: timeout 180 bash tools/porte-bloc-linguistique.sh > /tmp/etat-a-porte-bloc.txt 2>&1; echo "exit=$?"; tail -15 /tmp/etat-a-porte-bloc.txt) finished [status: completed, exit code: 0]. Read its output with job_output.

- **job_output** `{"job_id": "bash-4101", "wait": true, "timeout_ms": 60000}`

  ```
exit=0
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
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "tail -25 /tmp/etat-a-porte-bloc.txt", "description": "Read language gate output"}`

  ```
"syntagme"
 ],
 "niveaux_manquants": [],
 "controles": {
  "vide_refus": "vide",
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

- **job_output** `{"job_id": "bash-4102", "wait": true, "timeout_ms": 120000}`

  ```
exit=0
  ✅ version : drave 0.1.0
  ✅ analyser fr : JSON valide, étiquettes et syntagmes
  ✅ analyser en : JSON valide, étiquettes et syntagmes
  ✅ rejeu : sha256 f387bcab5d90d528 deux fois
  ✅ smoke test : Ran 10 tests
  ✅ schéma v1 validé (5 cas + 20 phrases du gold)
  ✅ schéma v1 : Ran 6 tests
  ✅ refus : JSON avec refus, code 3
  ✅ autotest parallèle : 183/183 portes tenues
✅ porte produit verte
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "tail -25 /tmp/etat-a-porte-produit.txt 2>/dev/null", "description": "Read product gate output"}`

  ```
✅ version : drave 0.1.0
  ✅ analyser fr : JSON valide, étiquettes et syntagmes
  ✅ analyser en : JSON valide, étiquettes et syntagmes
  ✅ rejeu : sha256 f387bcab5d90d528 deux fois
  ✅ smoke test : Ran 10 tests
  ✅ schéma v1 validé (5 cas + 20 phrases du gold)
  ✅ schéma v1 : Ran 6 tests
  ✅ refus : JSON avec refus, code 3
  ✅ autotest parallèle : 183/183 portes tenues
✅ porte produit verte
  ```

- **bash** `{"command": "ls tools/porte-*.sh | sed 's#tools/porte-##;s#\\.sh##' | tr '\\n' ' '; echo", "description": "List all gate names"}`

  ```
adaptateur-sortie audit-drapeaux b1110-hybride balayage bloc-code bloc-linguistique bloc-maths bloc-tableaux budget bus bus-socket c4-retard cerveau consolidation coupe cycle-c2 deepseek delais diff-couche document echange-experts episodique etat flux fusion gain greffe harnais-invariants homeostasie horloge indice jeux jumeaux lecteur lecture m5-brouillon melange memoire miroir-blocs mistral n3-cache n3-composition n3-deux-processus n3-deux-regions n3-generation n3-inventaire n3-placement n3-pont n3-positions n3-profondeur n3-refus n3-reseau n3-routes n3-service-briques n3-service n3-seuil n3-sparsite-compte n3-sparsite occupation-elagage occupation-moteur ocr-scans ocr pannes peripherie poids-creux pont prechargement produit profondeur-routee push-paresseux r13-bpe recurrence reflexe registre reparti-moteur ressources sauvegarde-modele sessions speculatif tableaux tokenizer-kimi topologie trace vision
  ```

- **bash** `{"command": "grep -rn \"porte-\" docs/archive/roadmap-detail-2026-10-29.md | grep -oE 'porte-[a-z0-9-]+' | sort -u | tr '\\n' ' '; echo", "description": "List gates cited in archived A roadmap"}`

  ```
porte-coupe porte-deepseek porte-diff-couche porte-topologie
  ```

- **bash** `{"command": "head -35 docs/pilotage/backlog/A3.4-colab.md; echo '=== A5.4 ==='; head -35 docs/pilotage/backlog/A5.4-fpga.md", "description": "Read A3.4 and A5.4 blocker fiches"}`

  ```
# A3.4 — Démonstration Colab (préremplissage réparti)

> **Statut** : bloquée · **Priorité** : P3 · **Programme** : A · **Dépend de** : A3 · **Bloqué par** : le compte et le runtime Colab
> **Ligne de roadmap** : A3.4 · **Fiche de résultat attendue** : rapport-a34-colab.md (à créer dans `reports/`)
> **Résumé** : Exécuter le préremplissage réparti sur un runtime Colab.
> **Glossaire** : [préremplissage](../../theorie/glossaire/entrees/preremplissage.md) · [Colab](../../theorie/glossaire/entrees/colab-notebook-tunnel.md) · [fidélité](../../theorie/glossaire/entrees/fidelite.md).

## Le besoin

Le préremplissage par lots est fidèle (0,00e0) ; il reste à le faire tourner sur le runtime Colab. La ligne est bloquée par le compte.

## L'état

Préremplissage par lots fait et fidèle ; runtime absent.

## La porte

Le même résultat local/distant sur le même lot, avec la trace et le débit.

## Contrôles négatifs

- même lot local ; réseau simulé ; version incompatible refusée

## Prochaine action

Dès qu'un compte est disponible, rejouer la recette de `docs/archive/colab-reparti.md` et écrire la fiche.

## Voir aussi

- [Programme A](../roadmap.md#programme-a--le-moteur-la-drave-les-flux)
- 
… [1233 caractères tronqués]
  ```

- **bash** `{"command": "head -30 docs/pilotage/backlog/A3.4-colab.md | grep -n \"Bloqué\\|Dépend\\|Ligne\"; echo '---'; head -30 docs/pilotage/backlog/A5.4-fpga.md | grep -n \"Bloqué\\|Dépend\\|Ligne\"", "description": "Extract blocker fields"}`

  ```
3:> **Statut** : bloquée · **Priorité** : P3 · **Programme** : A · **Dépend de** : A3 · **Bloqué par** : le compte et le runtime Colab
4:> **Ligne de roadmap** : A3.4 · **Fiche de résultat attendue** : rapport-a34-colab.md (à créer dans `reports/`)
---
3:> **Statut** : bloquée · **Priorité** : P3 · **Programme** : A · **Dépend de** : A5 · **Bloqué par** : la carte Stratix V
4:> **Ligne de roadmap** : A5.4 · **Fiche de résultat attendue** : rapport-a54-fpga.md (à créer dans `reports/`)
  ```

- **bash** `{"command": "head -45 tools/porte-echange-experts.sh; echo '=== A6.2 mentions in gate ==='; grep -n \"A6\\.2\\|routage\\|expert\" tools/porte-echange-experts.sh | head -20", "description": "Read expert exchange gate"}`

  ```
#!/bin/bash
# porte-echange-experts.sh — le routage imposé fait-il EXACTEMENT ce qu'il annonce ?
#
# POURQUOI CETTE PORTE. `DRAVE_ROUTAGE_FORCER` (13/10) permet d'imposer à un modèle routé les
# experts qu'une autre instance a choisis — c'est l'expérience C9 « échange d'experts »
# (`reports/rapport-c9-echange-experts.md`). Toute la mesure repose sur **un** invariant :
# **imposer à une instance SON PROPRE routage doit rendre la perplexité de référence, au bit près.**
# S'il est faux, les effets mesurés (±20 %) baignent dans un artefact — et c'est arrivé : la
# première version donnait 37,2013 contre 37,1990, parce que la trace TRIE les experts et que
# l'accumulation flottante change avec l'ordre (`DRAVE_TRACE_EXPERTS_ORDRE=1` corrige ça).
#
# CE QU'ELLE VÉRIFIE (trois conditions, dans cet ordre) :
#   1. **inerte par défaut** : sans variable, la trace ne change RIEN à la perplexité ;
#   2. **exact sur son propre routage** : capturé puis imposé, même perplexité au chiffre près ;
#   3. **vivant sur un autre routage** : avec les experts d'une autre couche, la perplexité CHANGE
#      (sinon la porte ne mesure pas ce qu'elle croit — un mécanisme mort passerait les deux
#      premi
… [2989 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"A2.6\\|A6.2\" reports/rapport-c9-echange-experts.md reports/rapport-cache-experts-vram.md reports/rapport-chargement-paresseux.md reports/rapport-aiguille-30b.md 2>/dev/null | head", "description": "Check A2.6/A6.2 cross-references in MoE reports"}`

  ```
(no output)
  ```

- **bash** `{"command": "ls -lh /home/stephane/IA/modeles/qwen3-30b-a3b-Q4_K_M.gguf /home/stephane/IA/scratch/prerequis/ids_qwen3_30b_wt2.txt 2>&1; echo '---'; ls -ld /home/stephane/IA 2>&1", "description": "Check gate default MoE path"}`

  ```
-rw-r--r--. 1 stephane stephane  18G  3 oct 13:17 /home/stephane/IA/modeles/qwen3-30b-a3b-Q4_K_M.gguf
-rw-r--r--. 1 stephane stephane 386K 12 oct 19:56 /home/stephane/IA/scratch/prerequis/ids_qwen3_30b_wt2.txt
---
drwxr-xr-x 14 stephane stephane 4096 21 oct 16:30 /home/stephane/IA
  ```

- **bash** `{"command": "grep -n \"expert\" docs/archive/roadmap-detail-2026-10-29.md | head -20; echo '--- n3 inventaire ---'; head -30 reports/rapport-n3-inventaire.md 2>/dev/null", "description": "Check expert placement in archived roadmap"}`

  ```
60:| A2.4 | **Cache d'experts MXFP4** | ✅ mesuré, **verdict : non** | +6 % — on ne l'active pas tel quel, et c'est écrit |
62:| A2.6 | **Ordonnanceur de placement** : chaque opérateur là où son flux coûte le moins cher (2 GPU, CPU, VRAM, RAM, NVMe) | 🔬 — la règle écrite **et appliquée** | le module [`placement.rs`](../../drave-core/src/placement.rs) (les bandes mesurées, `cout`, `classement`, `kv_en_vram`, et la **règle générale `choisir`** — le moins cher **où ça tient**, **4 tests verts**) ; la décision du **KV** y passe ; la **tête** a été essayée par la règle puis **revertée** (le 4 bits coûte +10 % de PPL : la place n'est pas la qualité) ; la mesure à 8 k : **×1,93** / **×5,8** — [`reports/rapport-placement-kv-8k.md`](../../reports/rapport-placement-kv-8k.md) ; reste l'ordonnanceur complet (experts, tête) |
71:| A3.2 | **Granularité** : par couche, par bloc, par expert | ✅ | listes i16, échelles par bloc, indices par écarts : **1 608 octets par flux** à 256 jetons ; le mode « lot en listes » : 1,5 ko/jeton contre 3,5 en dense (÷2,3) |
109:| A6.2 | **Routage appris** (MoE) : les experts choisis par les logs | ⏳ | qualité égale, coût de routage ÷10 |
143:place reste à appliquer 
… [2403 caractères tronqués]
  ```

- **bash** `{"command": "free -g; echo '--- gpu ---'; nvidia-smi --query-gpu=index,name,memory.total --format=csv,noheader; echo '--- engine gpu default ---'; grep -n \"DRAVE_GPU\\|CUDA_VISIBLE\\|n_gpu\\|multi\" drave-core/src/gpu.rs | head -20", "description": "Check RAM, GPUs, and multi-GPU support"}`

  ```
total        used        free      shared  buff/cache   available
Mem:             125          22           3           8         109         103
Swap:             62           0          62
--- gpu ---
0, Quadro RTX 5000, 16384 MiB
1, Quadro RTX 5000, 16384 MiB
--- engine gpu default ---
197:            // Piège courant : `CUDA_VISIBLE_DEVICES=` (vide) masque TOUS les
200:            if std::env::var("CUDA_VISIBLE_DEVICES").map(|v| v.trim().is_empty()).unwrap_or(false) {
201:                std::env::remove_var("CUDA_VISIBLE_DEVICES");
202:                eprintln!("[gpu] CUDA_VISIBLE_DEVICES vide : ignoré (les GPU redeviennent visibles)");
586:        // `q` doit être un multiple exact de n_kv × hd : une division tronquée
1549:/// Instance unique du processus. `DRAVE_GPU` active le déport ; sans lui, aucune
1559:        if std::env::var("DRAVE_GPU").is_err() { return None; }
1585:        // `DRAVE_GPU=0` force le CPU ; `DRAVE_GPU=1` force la tentative GPU.
1586:        if std::env::var("DRAVE_GPU").map(|v| v.trim() == "0").unwrap_or(false) {
  ```

- **bash** `{"command": "grep -n \"18\\|30B\\|mémoire\\|RAM\\|VRAM\\|CPU\" reports/rapport-c9-echange-experts.md | head -15", "description": "Check C9 execution context"}`

  ```
15:> Protocole : Qwen3-30B-A3B (48 couches, 128 experts, 8 utilisés), `--ppl --ctx 512 --limit 32`,
57:| 24 | 37,1813 | ×1,00 |
  ```

- **bash** `{"command": "date '+%Y-%m-%d %H:%M:%S %Z'; echo '--- HEAD ---'; git log -1 --format='%h %s'; echo '--- branch ---'; git branch --show-current; echo '--- dirty count ---'; git status --porcelain | wc -l", "description": "Get current date, HEAD, branch"}`

  ```
2026-11-06 21:51:08 EST
--- HEAD ---
7a876f70 PRODUIT — RE-TEST DES 50 TEXTES : filtrer = 0 CHEVAUCHEMENT (297 SEGMENTS), LES 5 SANS SYNTAGME SONT NON LINGUISTIQUES
--- branch ---
s/v7
--- dirty count ---
159
  ```

- **bash** `{"command": "git show --stat --oneline 7a876f70 | head -20; echo '--- latest reports ---'; ls -lt reports/*.md | head -5", "description": "Inspect latest commit and reports"}`

  ```
7a876f70 PRODUIT — RE-TEST DES 50 TEXTES : filtrer = 0 CHEVAUCHEMENT (297 SEGMENTS), LES 5 SANS SYNTAGME SONT NON LINGUISTIQUES
 docs/pilotage/en-cours.md                          |   4 +-
 journal/2026-11-06/README.md                       |  13 +-
 journal/2026-11-06/distribue.md                    |   8 +-
 journal/2026-11-06/docs.md                         |   8 +-
 journal/2026-11-06/memoire.md                      |   8 +-
 journal/2026-11-06/mesures.md                      |  12 +-
 journal/2026-11-06/modele.md                       |   8 +-
 journal/2026-11-06/outils.md                       |   8 +-
 journal/2026-11-06/portes.md                       |   8 +-
 journal/README.md                                  |  10 +-
 .../538288b3-117b-4daf-8d16-0cd8d6b0090d/digest.md |  28 +++
 .../rapport.md                                     |  15 +-
 .../599e9c0e-4252-43ca-a89a-3886d723c379/digest.md | 107 ++++++++++
 .../rapport.md                                     |  12 +-
 .../7635f5f5-11b8-4d10-bea5-50a90e536e31/digest.md | 202 ++++++++++++++++++
 .../rapport.md                                     |  34 ++-
 journal/sessions/MANIFEST.md                       |  12 +-
 .../cdc1
… [586 caractères tronqués]
  ```

- **bash** `{"command": "grep -n -E \"0 chevauchement|297|filtrer|5 sans\" reports/rapport-partition-syntagmes.md reports/rapport-partition-integree.md 2>/dev/null | head -15", "description": "Check latest partition figures"}`

  ```
reports/rapport-partition-syntagmes.md:173:| **B1 — filtrer_union** | **0,6163** | 0,7122 | 0,5432 | 0,7545 | 0,7581 | 0,5537 | **217** | 0,9079 | 216 |
reports/rapport-partition-syntagmes.md:174:| **B2 — filtrer** | **0,6172** | **0,7445** | 0,5271 | **0,7605** | 0,7581 | 0,5537 | **205** | 0,8577 | 204 |
reports/rapport-partition-syntagmes.md:288:2. **Option « vue partition » : B2 — `partition="filtrer"`.** 0 paire, F1 0,6172, exact 205/239,
reports/rapport-partition-syntagmes.md:291:3. **Option économique : B1 — `partition="filtrer_union"`.** Le filtre union du P0-3 : F1 0,6163,
reports/rapport-partition-syntagmes.md:306:| moins de chevauchements, coût minimal | `filtrer_union` | 0,6163 | 217/239 | 91 | +7,2 % |
reports/rapport-partition-syntagmes.md:307:| partition stricte, F1 d'abord | `filtrer` | 0,6172 | 205/239 | 0 | +2,0 % |
reports/rapport-partition-syntagmes.md:313:Le patch ajoute un paramètre `partition` (`brut`, `alternative` par défaut, `filtrer_union`,
reports/rapport-partition-syntagmes.md:314:`filtrer`), quatre fonctions (`_relation_partition`, `_cle_preferee`, `_groupes_partition`,
reports/rapport-partition-syntagmes.md:335:+        # "filtrer_union" : on retire l
… [804 caractères tronqués]
  ```

- **read** `{"file_path": "reports/rapport-re-test-produit.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-re-test-produit.md</path>
<type>file</type>
<content>
1: # B13 — re-test produit : 50 textes libres, la vue linéaire supprime les chevauchements
2: 
3: > **Ligne de roadmap** : **B13** (produit) · **Date** : 2026-11-06 · **Verdict** : ✅
4: > **Ce que le produit fait sur les 50 textes de l'audit A26**, rejoués sur le code du 06/11 21 h :
5: > en vue **`alternative`** (défaut), 405 segments et **145 chevauchements** ; en vue **`filtrer`**,
6: > 297 segments et **0 chevauchement**. Les **5 textes sans syntagme** sont l'emoji, le texte vide,
7: > les espaces, `...` et un nombre nu — des entrées **non linguistiques**, pas des échecs.
8: >
9: > **Dispositif** : `tools/bloc_linguistique.py` (`Heuristique(partition=...)`), les 50 textes de
10: > [`pensee-fiabilite-produit.json`](pensee-fiabilite-produit.json) ; JSON
11: > [`pensee-re-test-produit.json`](pensee-re-test-produit.json).
12: 
13: ## 1. Les chiffres
14: 
15: | vue | segments | chevauchements | textes sans syntagme |
16: |---|---:|---:|---:|
17: | **`alternative`** (défaut) | 405 | **145** | 5 |
18: | **`filtrer`** (linéaire) | 297 | **0** | 5 |
19: 
20: **Ce q
… [1466 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1,35p' reports/rapport-pos-nombres.md", "description": "Read latest POS numbers report"}`

  ```
# B13 — les nombres ont une POS : 45 tokens réparés, zéro perte

> **Ligne de roadmap** : **B13** (produit) · **Date** : 2026-11-06 · **Verdict** : ✅
> **Le P1-6 de l'audit produit** : les **nombres** n'avaient aucun POS (`typ == "nombre"` n'entrait
> pas dans la boucle POS). Ils sont désormais **NUM** (confiance 0,90) ; le gold est **inchangé**
> (POS 0,85 ; F1 0,6482 ; attachement 235/236 ; **183/183**).
>
> **Dispositif** : [`bloc_linguistique.py`](../tools/bloc_linguistique.py) (`_pos` : règle
> `\d+([.,]\d+)*` ; la boucle POS accepte `typ == "nombre"`) ; JSON
> [`pensee-pos-nombres.json`](pensee-pos-nombres.json).

## 1. Ce que ça répare

| avant | après |
|---|---|
| `12`, `2024` : aucun POS | **NUM** (0,90) |
| l'audit : **45 nombres** sans POS sur 1 068 tokens | 0 (hors ponctuation) |

**Ce que ça ne répare pas** : `12.5` est encore **tokenisé** `12` `.` `5` (la frontière de phrase
est protégée, pas le token) — c'est le patch B de la fiche des frontières, non intégré.

## 2. Ce que ce banc ne dit pas

- **Le gold n'a que 2 NUM** : le gain n'est pas mesuré sur le gold, il est **produit**.
- **`a`** reste PREP dans « il y a 12.5 euros » (l'ambiguïté avoir/préposition n'est pa
… [385 caractères tronqués]
  ```

- **bash** `{"command": "head -20 reports/rapport-fiabilite-produit.md; echo '=== audit A26? ==='; grep -rn \"audit A26\\|A29\\|A24\" reports/rapport-fiabilite-produit.md reports/rapport-re-test-produit.md reports/rapport-partition-syntagmes.md | head -10", "description": "Check audit ID labels for A24/A26/A29" … [1 caractères tronqués]`

  ```
# Fiabilité du produit hors gold — 0 plantage sur 50 phrases, 4 refus sans JSON, 23/46 textes à chevauchement de syntagmes

> **Ligne de roadmap** : **B13** (moteur de pensée, règle 6) · **Branche** : `s/v7` ·
> **Commit mesuré** : `56eb43af` (module `c1a08588`, `tools/drave.py` `59a06f3e`) ·
> **Date** : 2026-11-06 · **Verdict** : ⚠️ **la surface est fiable ; le contrat ne l'est pas encore.**
> **Aucun fichier existant modifié ; aucun commit.** Sorties : ce rapport et
> [`pensee-fiabilite-produit.json`](pensee-fiabilite-produit.json).
>
> **Dispositif** : [`tools/drave.py`](../tools/drave.py) (CLI : `analyser`, `evaluer`, `rejouer`,
> `--version`) et [`tools/bloc_linguistique.py`](../tools/bloc_linguistique.py) ;
> **50 phrases libres** écrites pour l'audit (textes dans le JSON) ; harnais local non committé
> dans `/tmp` ; machine **Xeon E5-2687W v3**, Python **3.13.16**.
>
> **Snapshot.** HEAD a bougé pendant l'audit (`6ef2a3f5` → `56eb43af`). Le module a reçu à
> **11 h 34** le correctif « non-str / surrogate » (`c1a08588`) ; le banc a tourné à **11 h 40**,
> après ce correctif, et `drave.py` n'a pas changé. Les chiffres portent sur ce couple de hash ;
> un audit futur doit repa
… [760 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"A17\\|A23\\|A24\\|A26\\|A29\" journal/2026-11-06/README.md | head -20", "description": "Check audit ID usage in journal"}`

  ```
53:| 01:29 | `5523de51` | JOURNAL ET ROADMAP — LA CIBLE DE A17 ATTEINTE : 222/222, COUVERTURE 0,9289, 17 SPANS INATTEIGNABLES |
75:| 10:54 | `f6c8132b` | A23 — LES 6 CORRECTIONS FACTUELLES DE LA FILE (GOLD 200+ = 13 OCCURRENCES, PASSES 2 H 11 À 2 H 29) ; T0 DANS LE BUDGET |
82:| 11:43 | `1962eb15` | PRODUIT — LA ROBUSTESSE : SURROGATE ET NON-STR FERMÉS (refus non_texte), 8 TESTS ; L'AUDIT A24 (50 PHRASES, 132 CHEVAUCHEMENTS, 18 CORRECTIFS) |
83:| 11:45 | `3601764a` | ÉTAT — T0 DANS LE BUDGET (AUDIT A24) |
136:**La cible de A17 (1 h 30).** Le dernier écart était un marqueur ambigu : « when » après un GN est
  ```

### 🤖 Assistant

⏵ Rédaction du rapport d'état A et du JSON de pensée
J'ai les vérifications ; je rédige les deux fichiers neufs, sans toucher au reste.

- **write** `{"file_path": "reports/rapport-etat-a.md", "content": "# État du chantier A — le moteur : deux bloqués réels, un faux bloqué, une frontière à requalifier\n\n> **Ligne de roadmap** : **A** (le moteur) · **Date** : 2026-11-06, 21 h 51 HNE · **Branche** : `s/v7` ·\n> **HEAD** : `7a876f70` (le HEAD a bo … [20225 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-etat-a.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **write** `{"content": "{\n  \"date\": \"2026-11-06T21:51:00-05:00\",\n  \"branche\": \"s/v7\",\n  \"head\": \"7a876f70\",\n  \"head_note\": \"le HEAD a bougé pendant l'audit (d31aa9a2 → 7a876f70) ; les chiffres sont horodatés\",\n  \"mission\": \"état du chantier A (le moteur) — lecture seule, aucun code, deu … [20948 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-etat-a.json</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "python3 -m json.tool reports/pensee-etat-a.json > /tmp/etat-a-json-check.txt 2>&1; echo \"json_exit=$?\"; tail -3 /tmp/etat-a-json-check.txt; echo '--- new files ---'; git status --porcelain -- reports/rapport-etat-a.md reports/pensee-etat-a.json; echo '--- other new untracked (top) --- … [112 caractères tronqués]`

  ```
json_exit=0
        "reports/pensee-etat-a.json"
    ]
}
--- new files ---
?? reports/pensee-etat-a.json
?? reports/rapport-etat-a.md
--- other new untracked (top) ---
?? journal/2026-11-05/attention.md
?? journal/2026-11-06/distribue.md
?? journal/2026-11-06/docs.md
?? journal/2026-11-06/memoire.md
?? journal/2026-11-06/mesures.md
?? journal/2026-11-06/modele.md
?? journal/2026-11-06/outils.md
?? journal/2026-11-06/portes.md
?? journal/sessions/082fe8ca-3e1e-4454-b91b-12586843e880/
?? journal/sessions/14114f3d-ae0d-416e-ad8e-4d4eaa04c36c/
?? journal/sessions/1555bdd3-27e9-4779-b1e7-716e32399c11/
?? journal/sessions/1b0cf09a-a77a-443d-82e2-68a5d6cacdf0/
?? journal/sessions/24001907-4f19-4ea5-87f6-98334496719f/
?? journal/sessions/24529ced-6556-4491-9633-9401c2dffb0c/
?? journal/sessions/2cc1ad4a-373e-4362-a341-3c4a630c2e0c/
?? journal/sessions/3144cf23-6004-46ef-bc3d-f05d81c0cff6/
?? journal/sessions/338f8b55-bcd5-464a-a63e-b97381eff55d/
?? journal/sessions/3ccd8d09-9820-4da4-963b-6d84a0ffb141/
?? journal/sessions/3f8f2bb8-781b-44a6-9e14-58025004b6fc/
?? journal/sessions/3fb87dc7-7d24-42e2-a68e-e37e2734b755/
  ```

- **bash** `{"command": "python3 tools/verifier_liens.py 2>&1 | tail -15; echo \"liens_exit=$?\"", "description": "Check links resolve"}`

  ```
✅ 3716 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
liens_exit=0
  ```

- **bash** `{"command": "find tools reports -name '__pycache__' -newermt '2026-11-06 21:30' -print 2>/dev/null | head; echo '--- new files in reports (untracked) ---'; git status --porcelain -- reports/ | grep '^??' | head -20; echo '--- new files in docs ---'; git status --porcelain -- docs/ | grep '^??' | hea … [64 caractères tronqués]`

  ```
tools/__pycache__
--- new files in reports (untracked) ---
?? reports/pensee-etat-a.json
?? reports/pensee-etat-n2.json
?? reports/rapport-etat-a.md
?? reports/rapport-etat-n2.md
?? reports/rapport-s-paragraphes.md
--- new files in docs ---
  ```

- **bash** `{"command": "wc -l reports/rapport-etat-a.md reports/pensee-etat-a.json; echo '--- report head ---'; head -20 reports/rapport-etat-a.md", "description": "Check report size and head"}`

  ```
246 reports/rapport-etat-a.md
  398 reports/pensee-etat-a.json
  644 total
--- report head ---
# État du chantier A — le moteur : deux bloqués réels, un faux bloqué, une frontière à requalifier

> **Ligne de roadmap** : **A** (le moteur) · **Date** : 2026-11-06, 21 h 51 HNE · **Branche** : `s/v7` ·
> **HEAD** : `7a876f70` (le HEAD a bougé pendant l'audit : `d31aa9a2` → `7a876f70`) ·
> **Mission** : lecture seule, aucun code, aucun fichier existant modifié ; deux fichiers neufs.
>
> **Verdict** : ⚠️ **l'état A est sain, le récit A est en retard.** Les lignes fermées le sont
> réellement ; **A8.3a est fait pour 3 portes sur 19** (et non « fait » tout court) ; **A2.6 est
> partiel mais libre** — sa tête est **décidée** (refusée), ses experts ne sont **pas** bloqués par
> l'absence d'un MoE : un **Qwen3-30B-A3B Q4 de 18 Go est présent et tourne**. Les **deux seuls
> bloqués réels** de A sont **A3.4** (compte Colab) et **A5.4** (carte Stratix V). **A6.2 est
> mal classé** : il est libre, pas bloqué. **A23 a raison sur l'effet** (A2.6 ne doit pas être la
> tête de frontière) **mais tort sur la cause** (les experts ne sont pas bloqués par A6.2).
>
> **Dispositif** : lecture de `docs/pilot
… [483 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Ajustement de la formulation sur A6.2 et les tests de placement
Je précise deux nuances (A6.2 « ressource absente » vs « résidence mono-GPU » ; 8 tests vs 4) avant de rendre.

- **edit** `{"file_path": "reports/rapport-etat-a.md", "old_string": "bloqués réels** de A sont **A3.4** (compte Colab) et **A5.4** (carte Stratix V). **A6.2 est\n> mal classé** : il est libre, pas bloqué. **A23 a raison sur l'effet** (A2.6 ne doit pas être la", "new_string": "bloqués réels** de A sont **A3.4** … [233 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-etat-a.md has been updated successfully.
  ```

- **edit** `{"file_path": "reports/rapport-etat-a.md", "old_string": "- **Chiffre à corriger** : la fiche et le JSON disent **4 tests** ; il y en a **8**.", "new_string": "- **Chiffre à corriger** : la fiche et le JSON disent **4 tests** ; `placement.rs` en a **8**\n  (les 4 de `choisir` + 4 autres), tous verts … [11 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-etat-a.md has been updated successfully.
  ```

- **edit** `{"file_path": "reports/rapport-etat-a.md", "old_string": "| **A6.2** | **oui** | MoE local 18 Go, 2×16 Go VRAM, 125 Go RAM ; trace et imposition du routage existent | **action 2** |", "new_string": "| **A6.2** | **oui** | MoE local 18 Go, 2×16 Go VRAM, 125 Go RAM ; trace et imposition du routage exi … [104 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-etat-a.md has been updated successfully.
  ```

- **edit** `{"file_path": "reports/pensee-etat-a.json", "new_string": "  \"verdict\": \"A est sain dans ses lignes fermées et faux dans sa frontière : A8.3a est fait pour 3 portes sur 19, A2.6 est partiel mais libre (tête décidée, experts mesurables sur le MoE local), A6.2 est mal classé (aucune ressource ne ma … [390 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-etat-a.json has been updated successfully.
  ```

- **edit** `{"file_path": "reports/pensee-etat-a.json", "new_string": "      \"etat\": \"libre de ressource (mal classé bloqué)\",", "old_string": "      \"etat\": \"libre (mal classé bloqué)\","}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/pensee-etat-a.json has been updated successfully.
  ```

- **bash** `{"command": "python3 -m json.tool reports/pensee-etat-a.json > /dev/null 2>&1; echo \"json_exit=$?\"; python3 tools/verifier_liens.py 2>&1 | tail -2; echo '--- status ---'; git status --porcelain -- reports/rapport-etat-a.md reports/pensee-etat-a.json", "description": "Revalidate JSON and links"}`

  ```
json_exit=0
  ✅ 3719 lien(s) relatif(s) résolvent (docs + reports, hors blocs de code)
--- status ---
 M reports/pensee-etat-a.json
 M reports/rapport-etat-a.md
  ```

- **bash** `{"command": "grep -n \"A6.2\\|8 tests\\|4 tests\" reports/rapport-etat-a.md | head -20; echo '---'; grep -c \"A2.6\" reports/rapport-etat-a.md", "description": "Spot-check edited report"}`

  ```
11:> bloqués réels** de A sont **A3.4** (compte Colab) et **A5.4** (carte Stratix V). **A6.2 est
14:> tête de frontière) **mais tort sur la cause** (les experts ne sont pas bloqués par A6.2).
27:| `CARGO_TARGET_DIR=/tmp/etat-a-target cargo test --manifest-path drave-core/Cargo.toml placement` | **8/8**, exit 0 | la règle `choisir` / `choisir_avec_perte` / `kv_precision` est testée — **8 tests, pas 4** |
48:| **A6** apprendre des flux | ✅ / ⏳ **A6.2 mal classé** | A1, A2 | hebbien +**3,0 %**, produits **+0,0045** de R² ; **0 neurone mort** sur 116 736 ; 63 % < 0,1 % ; top 10 % → **19 %** de la masse | `bash tools/porte-echange-experts.sh` ; `bash tools/porte-occupation-elagage.sh` |
60:| **A2.6** | **partiel, libre (P2)** | A2 acquis ; **pas** A6.2 pour les experts ; tête décidée | KV ×1,93/×5,8 ; lot **503/502 Mio**, **24,0 → 30,5 tok/s** (+27 %), PPL **15,8452 → 15,8443** (−0,006 %) ; tête **+10 % PPL** (constante, pas de run courant) | `cargo test placement` (8/8) ; `bash tools/mesure_lot_disque.sh models/Qwen2.5-0.5B-Q8_0.gguf <ids>` | règle générique + KV **faits** ; tête **refusée par décision** ; experts **non mesurés** mais **mesurables** sur le MoE local |
65:| **A6.2** | *
… [1957 caractères tronqués]
  ```

- **bash** `{"command": "git status --porcelain | grep -E 'etat-a|rapport-etat' ; echo '--- cached ---'; git diff --cached --stat -- reports/rapport-etat-a.md reports/pensee-etat-a.json; echo '--- unstaged ---'; git diff --stat -- reports/rapport-etat-a.md reports/pensee-etat-a.json", "description": "Check stag … [24 caractères tronqués]`

  ```
--- cached ---
--- unstaged ---
 reports/pensee-etat-a.json | 4 ++--
 reports/rapport-etat-a.md  | 8 +++++---
 2 files changed, 7 insertions(+), 5 deletions(-)
  ```

- **bash** `{"command": "git ls-files --stage reports/rapport-etat-a.md reports/pensee-etat-a.json; echo '--- log ---'; git log --oneline -3 -- reports/rapport-etat-a.md reports/pensee-etat-a.json; echo '--- status short ---'; git status --short -- reports/rapport-etat-a.md reports/pensee-etat-a.json", "descrip … [58 caractères tronqués]`

  ```
100644 f222f05a7cd3a5bef33484325868dd1c0efc985b 0	reports/pensee-etat-a.json
100644 3bfdb02826190afa887a94aaeebfa610a0dc4f11 0	reports/rapport-etat-a.md
--- log ---
3caa8938 ÉTATS — N2 (PORTE PROPRE 2,97/2,86, PROPOSITION porte-n2.sh) ET A (FRONTIÈRE CORRIGÉE : A2.6/A6.2 LIBRES, A3.4/A5.4 SEULS BLOQUÉS)
--- status short ---
 M reports/pensee-etat-a.json
 M reports/rapport-etat-a.md
  ```

- **bash** `{"command": "git log -1 --format='%h %ci %s'; git status --porcelain | head -3", "description": "Check latest commit and status"}`

  ```
3caa8938 2026-11-06 22:08:15 -0500 ÉTATS — N2 (PORTE PROPRE 2,97/2,86, PROPOSITION porte-n2.sh) ET A (FRONTIÈRE CORRIGÉE : A2.6/A6.2 LIBRES, A3.4/A5.4 SEULS BLOQUÉS)
M  docs/pilotage/en-cours.md
MM journal/2026-11-05/README.md
D  journal/2026-11-05/attention.md
  ```

- **bash** `{"command": "git diff -- reports/rapport-etat-a.md reports/pensee-etat-a.json | head -80", "description": "Review unstaged edits to the two files"}`

  ```
diff --git a/reports/pensee-etat-a.json b/reports/pensee-etat-a.json
index f222f05a..65220ccd 100644
--- a/reports/pensee-etat-a.json
+++ b/reports/pensee-etat-a.json
@@ -4,7 +4,7 @@
   "head": "7a876f70",
   "head_note": "le HEAD a bougé pendant l'audit (d31aa9a2 → 7a876f70) ; les chiffres sont horodatés",
   "mission": "état du chantier A (le moteur) — lecture seule, aucun code, deux fichiers neufs",
-  "verdict": "A est sain dans ses lignes fermées et faux dans sa frontière : A8.3a est fait pour 3 portes sur 19, A2.6 est partiel mais libre (tête décidée, experts mesurables sur le MoE local), A6.2 est mal classé (le MoE local existe), A3.4 et A5.4 sont les deux seuls bloqués réels.",
+  "verdict": "A est sain dans ses lignes fermées et faux dans sa frontière : A8.3a est fait pour 3 portes sur 19, A2.6 est partiel mais libre (tête décidée, experts mesurables sur le MoE local), A6.2 est mal classé (aucune ressource ne manque : le MoE local existe), A3.4 et A5.4 sont les deux seuls bloqués réels.",
   "methode": {
     "lecture": [
       "docs/pilotage/roadmap.md",
@@ -196,7 +196,7 @@
     },
     {
       "id": "A6.2",
-      "etat": "libre (mal classé bloqué)",
+      "etat": "li
… [2726 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Envoi du résultat au parent et clôture
Les deux fichiers sont écrits et validés ; je transmets la synthèse au parent.

- **send_message** `{"agent_id": "e181ce02-cd50-488a-a6be-e84b79d40dcc", "message": "ÉTAT A — terminé. Deux fichiers neufs : `reports/rapport-etat-a.md` (246 l.) et `reports/pensee-etat-a.json` (JSON valide). Ils ont été commités par une autre session dans `3caa8938` avant mes deux dernières nuances (A6.2 « ressource a … [3816 caractères tronqués]`

  ```
message delivered to agent e181ce02-cd50-488a-a6be-e84b79d40dcc
  ```

