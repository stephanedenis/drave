# Session DSH — relecture

- identifiant : `c7e46dba-11cb-456b-a3b6-715428927f99`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-18 08:58:22
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet Drave, en français).

TÂCHE : une RECONNAISSANCE de la ligne A2.6 (« les experts et la tête » du moteur GGUF), pour que la session coordinatrice décide quoi implémenter. Tu ne modifies AUCUN code du moteur ; tu produis un document.

À lire (dans cet ordre, sans tout charger) :
- docs/pilotage/roadmap.md — le programme A, la ligne A2.6 et la file « jamais en attente » ;
- docs/pilotage/en-cours.md — l'état (ligne A) ;
- les fiches reports/ qui parlent des experts / du MoE / de A6.2 (cherche « expert », « MoE », « A6.2 » dans reports/*.md et docs/pilotage/backlog/) ;
- drave-core/src/model.rs — le chemin des experts (grep « expert », « rout », « topk », « sparse ») ;
- drave-core/src/materiel.rs et placement.rs si le placement des experts y est décrit.

À produire : reports/rapport-a2.6-reconnaissance.md (crée-le), avec :
1. **Ce qui existe** (chemins de code + numéros de ligne, ce qui est mesuré et où) ;
2. **Ce qui manque** pour clore A2.6 (précisément) ;
3. **La prochaine expérience** : la commande exacte, le contrôle négatif, ce qui pourrait la rendre fausse, le chiffre attendu ;
4. **Les fichiers à modifier** et le risque (taille du diff, tests à relancer, portes concernées).

CONTRAINTES STRICTES :
- ne touche pas à docs/pilotage/en-cours.md, docs/pilotage/roadmap.md, AGENTS.md ;
- ne modifie pas le code (lecture seule) ;
- ne committe pas ; laisse ton rapport non committé ;
- n'écris que reports/rapport-a2.6-reconnaissance.md ;
- si une commande est nécessaire, elle doit être locale et courte (pas d'entraînement, pas de GPU long).

Rends à la fin : un résumé de 10 lignes maximum (ce qui existe, ce qui manque, la prochaine expérience, le risque) et le chemin du rapport.
Your parent agent id is "d67a9bb1-090e-4f69-baf2-a831c00aa275". Before you finish, send your result to that agent with send_message({ agent_id: "d67a9bb1-090e-4f69-baf2-a831c00aa275", message: "<self-contained result>" }). The parent shares your workspace but does not automatically receive your transcript, tool output, or reasoning. Send earlier messages as well when a finding changes what the parent should do next; sending a message does not end your turn.

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

12. **La tarification de l'API a deux fenêtres** : **remisé** pendant **UTC 16:30 → 00:30**
    (la Chine 00:30 → 08:30), soit au Canada **11:30 → 19:30** ; **plein tarif** le reste.
    **L'API en remisée** (le tagger, la distillation), **le local en pleine** (l'entraînement, les
    tests, les docs) ; **deux files** par chantier. → [`plans-tarif.md`](docs/pilotage/plans-tarif.md)

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

⏵ Lecture de la roadmap et de l'état pour cadrer la ligne A2.6

- **bash** `{"command": "git status --short && git log --oneline -5 && ls", "description": "Check repo state and recent commits"}`

  ```
52b0b78d N4 — LE 100 M MESURÉ À RÉGLAGES APPARIÉS : LA RÉPÉTITION TOMBE DE 9 À 6, LE VOCABULAIRE NE GAGNE RIEN (0,882 CONTRE 0,884)
d649467c CONSIGNES — LA RÈGLE 12 POUR TOUS LES AGENTS : L'API EN FENÊTRE REMISÉE (11 h 30 → 19 h 30 EST), LE LOCAL EN PLEINE, DEUX FILES PAR CHANTIER ; LE PLAN DÉTAILLÉ LIÉ
e6fa9c0d PASSE — 90 PORTES, 87 VERTES, 3 ROUGES, AUCUNE NOUVELLE (116 MIN DE CALCUL LOCAL)
18d49ce7 PROFILS SUR CINQ MODÈLES : BLOQUE ±0,04 % (LE CONTRAT NE BIAISE PAS) · FLOU +1,1 À +7,0 % (TOUJOURS UNE PERTE) · COURT −12,1 À +4,6 % (LE SENS DÉPEND DU MODÈLE)
02cc66d4 PLANS — LES FILES PAR FENÊTRE TARIFAIRE : L'API EN REMISÉE (11 h 30 → 19 h 30 EST), LE LOCAL EN PLEINE (19 h 30 → 11 h 30) ; LES TROIS CHANTIERS QUI GAGNENT (N, R, B13) ET CEUX QUI SONT LOCAUX PAR NATURE
AGENTS.md
bench
build
colab
data
dist
docs
drave-core
drave.egg-info
journal
models
__pycache__
pyproject.toml
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

- **grep** `{"pattern": "A2\\.6|A2\\.5|A6\\.2", "path": "docs/pilotage/roadmap.md"}`

  ```
Found 11 matches

docs/pilotage/roadmap.md
Line 30: | **A — le moteur** | formats, placement, transport, [rejeu](../theorie/glossaire/entrees/rejeu.md), matériels, ordonnanceur | ✅ A1–A8 ; **A3.4, A5.4 bloqués** ; **A6.2 libre** (MoE local 18 Go) ; A2.6 partiel ; A3.2/A3.3 mesurées ; **A8.3c/d expliqués** ; **A2.6/A8.3 : le [lot](../theorie/glossaire/entrees/lot.md) ne divise pas les lectures denses (+27 % calcul, PPL −0,006 %)** | **A2.6** (experts : A6.2 bloqué) ; le lot ≥ 2 assumé |
Line 36: | **D — les données** | inventaire, corpus 10 langues, texte intégral, PDF/[OCR](../theorie/glossaire/entrees/ocr.md), documents, genres | ✅ inventaire ; **10 corpus texte intégral** (20,53 M art., 67,73 G car., 81,2 Go, **8 Ko 0**) ; **PDF** (1 927 doc., 322 Mo) ; **documents** (3 384 doc., 872 M car., 8 Ko 2,07 %) ; **OCR** (20 livres, 7 381 p, 15,36 M, 8 Ko 0 ; [CEGEP](../theorie/glossaire/entrees/cegep.md) **91 scans uniques**, 60 documents, 1 982 p, 4,41 M car., 8 Ko 0) ; **genres** mesurés | **l'OCR est clos** (limite : 8 scans `.PDF`, 58 p) ; la préparation **R1.1/R1.2** (N2) et **A2.6** (A) |
Line 221: 8. **Les bloqués** : A3.4 ([Colab](../theorie/glossaire/entrees/colab-notebook-tun
… [1221 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 1,60p docs/pilotage/roadmap.md", "description": "Read roadmap header and program A"}`

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
… [14152 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"A2\\.6\" docs/pilotage/en-cours.md docs/pilotage/backlog/*.md reports/*.md 2>/dev/null | head -60", "description": "Grep A2.6 across state, backlog and reports"}`

  ```
docs/pilotage/en-cours.md:113:| **A — le moteur** | **A2.6** | A3.4 Colab ; A5.4 rig+ring ; **A6.2 libre** (MoE 18,56 Go, PPL 37,2013 ; résidence 16 GiB) | **A2.6** (experts et tête) ; **A6.2** rapport + A8.3b2 |
docs/pilotage/backlog/A2.6-ordonnanceur.md:1:# A2.6 — Ordonnanceur : experts et tête
docs/pilotage/backlog/A2.6-ordonnanceur.md:4:> **Ligne de roadmap** : A2.6 · **Fiche de résultat** :
docs/pilotage/backlog/dependances.md:63:| **A2.6** | partiel | A2 (acquis) | — | — | [A2.6-ordonnanceur.md](A2.6-ordonnanceur.md) |
docs/pilotage/backlog/dependances.md:162:| **A2.6** | partiel | `A2` mesuré ; `A6.2` est un plafond, pas une arête ; tête **refusée par décision**, `placement.rs` a **8 tests** | experts et placement dans la règle `choisir` |
docs/pilotage/backlog/dependances.md:205:| **P2** | `N3`, `B11.10`, `B12.10`, `A2.6`, `A3.2`, `A8.0` | lignes autonomes, utiles, non bloquantes |
docs/pilotage/backlog/index.md:89:| A2.6 | [Ordonnanceur : experts et tête](A2.6-ordonnanceur.md) | partiel | P2 | A2 | A2.6 |
docs/pilotage/backlog/N3-operations-natives.md:47:le rejeu et le placement (A2.6). La profondeur routée (dessin B) est **exécutée par le
reports/INDEX.md:22:| [rapport-a2
… [7576 caractères tronqués]
  ```

- **bash** `{"command": "cat docs/pilotage/backlog/A2.6-ordonnanceur.md", "description": "Read the A2.6 backlog fiche"}`

  ```
# A2.6 — Ordonnanceur : experts et tête

> **Statut** : partiel · **Priorité** : P2 · **Programme** : A · **Dépend de** : A2
> **Ligne de roadmap** : A2.6 · **Fiche de résultat** :
> [`placement-kv-8k`](../../../reports/rapport-placement-kv-8k.md).
> **Résumé** : chaque opérateur là où son flux coûte le moins cher — et **seulement** là où
> la qualité le permet.

## Le besoin

Le placement n'est pas un choix de confort : un opérateur mal placé paie le flux à chaque
passe. La règle doit dire, pour un opérateur, **où il tient** et **ce qu'il coûte** — et
refuser une place qui coûte la qualité. Aujourd'hui la règle existe pour le KV ; les experts
et la tête ne sont pas encore ordonnancés.

## L'état

**Partiel** — `drave-core/src/placement.rs` porte les **bandes mesurées**, `cout`,
`classement`, `kv_en_vram` et la règle générale `choisir` (**4 tests verts**) : le moins cher
**où ça tient**. Le **KV l'applique** : à 8 k, **×1,93 / ×5,8**
([fiche](../../../reports/rapport-placement-kv-8k.md)). La **tête** a été essayée par la règle
puis **revertée** : le 4 bits y coûte **+10 % de PPL** — la place n'est pas la qualité.
**Restent les experts et la tête** comme objets de l'ordonnanceur.

#
… [1494 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 100,135p docs/pilotage/en-cours.md; echo ---; grep -n \"A2\\b\\|A2\\.\\|experts\" docs/pilotage/en-cours.md | head -40", "description": "Read en-cours A line and expert mentions"}`

  ```
| portes | **90** (dont `porte-n3-variante`, `-route`, `-moteurs`, `-court` le 17/11) | `tools/porte-*.sh` |
| chapitres de la synthèse | **8** | `docs/theorie/synthese/0*.md` |
| fichiers / JSON de résultats | **790** / **882** | `reports/*.md` / `reports/*.json` |
| documents de `docs/` | **128** (hors archive et README) | `docs/**/*.md` |
| dernière passe | **17/11 20 h 42 → 22 h 39** : **90** portes, **87/3** ; rouges `indice` (862 s) et `melange` (106 s) **structurelles**, `sessions` **circonstance** (heartbeat `e181ce02` à 1 896 min) → **aucune rouge nouvelle** ; cumul **6 981 s** | `work/portes/roue-1117-2042/registre.txt` |

## Les chantiers et leurs bloquants

**Dépendances** : [le graphe](backlog/dependances.md) ; cette table ne garde que les **bloquants
externes** et la **prochaine action**.

| chantier | frontière (graphe) | bloquant (ressource) | prochaine action |
|---|---|---|---|
| **A — le moteur** | **A2.6** | A3.4 Colab ; A5.4 rig+ring ; **A6.2 libre** (MoE 18,56 Go, PPL 37,2013 ; résidence 16 GiB) | **A2.6** (experts et tête) ; **A6.2** rapport + A8.3b2 |
| **B — l'intelligence** | **B13** | **B13 : 183/183, F1 0,7902, 238/239** ; le produit installable (roue, q
… [2745 caractères tronqués]
  ```

- **bash** `{"command": "grep -n -i \"expert\\|rout\\|topk\\|top_k\\|sparse\\|moe\\|n_expert\\|n_ff_exp\\|expert_used\\|ffn_gate_exps\\|ffn_down_exps\\|ffn_up_exps\" drave-core/src/model.rs | head -120", "description": "Grep expert/MoE path in model.rs"}`

  ```
16:use crate::engine::{Pool, SparseVec};
26:/// Convention de routage des experts — quatre familles, et une seule
27:/// implémentation partagée par le jeton seul et le lot (voir [`router`]).
30:    /// `softmax` sur TOUS les logits, top-k, renormalisation. Qwen3-MoE, et le
34:    /// Kimi-K2.7 (`expert_gating_func = 2`), GLM-5.3 et GLM-5.3-Flash.
41:    /// renormalisation. DeepSeek V4-Flash (`expert_gating_func = 4`) et V4.1.
46:    /// Numéro `expert_gating_func` du GGUF, tel que llama.cpp le définit.
80:/// (`hc_*`), attention par index (`indexer`), routage par table (`tid2eid`) et
96:    // sous-couche est le mélange des `hc` copies, la sortie se route par `comb`
109:    // (`res_mix`, `PetitesK3`), MoE latent (`MoeK3`), SiTU (`situ`), et la
115:    // K3 est un instrument de vérification qui déquantifie les experts en f32
116:    // (une couche MoE = 1 366 ms/jeton, et 93 couches en f32 demanderaient
124:déquantifie les experts en f32 — il sert à VÉRIFIER, pas encore à faire tourner le modèle");
127:    // sert QUE si la séquence dépasse `index_topk` — en deçà, llama.cpp garde
131:        // La clé s'appelle `attention.indexer.top_k` dans les GGUF de V4
132:        // (`index
… [7986 caractères tronqués]
  ```

- **bash** `{"command": "wc -l drave-core/src/model.rs drave-core/src/placement.rs drave-core/src/materiel.rs; echo ---; grep -n -i \"expert\\|rout\\|topk\\|top_k\\|sparse\\|moe\" drave-core/src/placement.rs drave-core/src/materiel.rs | head -60", "description": "Sizes and expert refs in placement/materiel"}`

  ```
10346 drave-core/src/model.rs
   253 drave-core/src/placement.rs
   501 drave-core/src/materiel.rs
 11100 total
---
drave-core/src/placement.rs:86:/// experts, la tête) : on parcourt les supports par coût croissant et on prend
drave-core/src/materiel.rs:80:    pub cache_experts_go: f64,
drave-core/src/materiel.rs:311:    pub fn plan(&self, ctx: usize, taille_modele_go: f64, n_experts: usize,
drave-core/src/materiel.rs:312:                mo_par_expert: f64) -> Plan {
drave-core/src/materiel.rs:350:        // --- cache d'experts en VRAM : ce qui reste après le commun.
drave-core/src/materiel.rs:354:        let cache_experts_go = (vram - reserve - commun_go).max(0.0);
drave-core/src/materiel.rs:357:                "cache d'experts VRAM = {:.1} Go — {:.1} Go libres moins {:.0} de \
drave-core/src/materiel.rs:359:                cache_experts_go, vram, reserve, commun_go));
drave-core/src/materiel.rs:369:        // 96,6 Go à 1 M de jetons — plus que les 71 Go d'experts. En int8,
drave-core/src/materiel.rs:380:        let experts_go = n_experts as f64 * mo_par_expert / 1000.0;
drave-core/src/materiel.rs:382:        if experts_go > pour_ram && pour_ram > 0.0 {
drave-core/src/materiel.rs:
… [1275 caractères tronqués]
  ```

- **read** `{"file_path": "drave-core/src/placement.rs"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/placement.rs</path>
<type>file</type>
<content>
1: //! Le placement des opérateurs — la règle de coût, **mesurée**.
2: //!
3: //! La vision (axe 2) : « on place un opérateur là où son flux coûte le moins
4: //! cher ». Cet axe était réglé par des `if` codés en dur et des seuils choisis
5: //! à la main ; ce module porte la **règle** et ses constantes mesurées
6: //! (`reports/rapport-placement-kv-8k.md`) :
7: //!
8: //! | support | bande mesurée | ce qu'on y met |
9: //! |---|---:|---|
10: //! | VRAM | 84,9 Go/s | le KV au-delà de ~2-4 k jetons, l'attention, la tête |
11: //! | RAM | 22,5 Go/s | les poids (mmap, non copiés), le KV court |
12: //! | NVMe | 3,5 Go/s | les poids qui ne tiennent pas en RAM (streaming) |
13: //! | réseau | 0,25 Mbit/s | les activations seules (jamais les poids) |
14: //!
15: //! Le coût d'un opérateur est **ses octets lus par jeton divisés par la bande
16: //! du support** ; le placement est le minimum sous la contrainte de place. La
17: //! mesure du 24/10 valide la première ligne : le KV en VRAM donne ×1,93 sur le
18: //! préremplissage à 8 k et ×5,8 sur l'attention.
19: 
20: /// La 
… [10994 caractères tronqués]
  ```

- **bash** `{"command": "ls reports | grep -i \"expert\\|moe\\|a26\\|a6\\|a62\" ; echo ---; grep -rln -i \"expert\" reports/*.md docs/pilotage/backlog/*.md | head -30", "description": "List expert-related reports"}`

  ```
a26-bilan.json
a26-lot-disque.json
rapport-a26-bilan.md
rapport-a26-lot-disque.md
rapport-c9-echange-experts.md
rapport-cache-experts-vram.md
rapport-decoupage-moe.md
rapport-mla-experts.md
rapport-morcellement-experts.md
rapport-prefill-par-experts.md
rapport-reutilisation-experts.md
rapport-routage-experts.md
---
reports/campagne-benefices.md
reports/fiche-modele-natif.md
reports/historique-passes-portes.md
reports/INDEX.md
reports/rapport-a26-bilan.md
reports/rapport-a26-lot-disque.md
reports/rapport-a80-audit-final.md
reports/rapport-a80-porte-reparti.md
reports/rapport-a83c-lot.md
reports/rapport-aiguille.md
reports/rapport-architecture-memoire.md
reports/rapport-bilan-chantier.md
reports/rapport-budget-decision.md
reports/rapport-budget-kimi-k3.md
reports/rapport-c9-echange-experts.md
reports/rapport-c9-lateralite.md
reports/rapport-cache-experts-vram.md
reports/rapport-coherence-docs.md
reports/rapport-coherence-vision.md
reports/rapport-consolidation-structure-partagee.md
reports/rapport-coordination-a.md
reports/rapport-coordination-n2.md
reports/rapport-decoupage-moe.md
reports/rapport-deepseek.md
reports/rapport-dessin-B-poids-creux.md
reports/rapport-drapeaux-ignores.md
… [154 caractères tronqués]
  ```

- **bash** `{"command": "for f in rapport-a26-bilan rapport-cache-experts-vram rapport-morcellement-experts rapport-prefill-par-experts rapport-reutilisation-experts rapport-routage-experts rapport-c9-echange-experts rapport-decoupage-moe rapport-mla-experts; do echo \"=== $f\"; head -22 reports/$f.md; echo; do … [53 caractères tronqués]`

  ```
=== rapport-a26-bilan
# A2.6 — l'ordonnanceur est partiel : le générique et le KV sont faits, la tête est refusée, les experts bloqués

> **Ligne de roadmap** : A2.6 · **Date** : 2026-10-29 · **Verdict** : ⚠️ **partielle** — la règle
> générique et le KV sont mesurés ; la tête 4 bits est refusée par la perte ; les experts attendent
> **A6.2** (pas de MoE local). A2.6 ne peut pas être « complétée » sans cette brique.
>
> **Dispositif** : bilan des mesures existantes (`placement.rs`, `rapport-placement-kv-8k.md`,
> `rapport-regle-placement-perte.md`, A8.3) ; **pas de nouvelle mesure** ; données
> [`a26-bilan.json`](a26-bilan.json).

## Le bilan

| partie | état | preuve |
|---|---|---|
| `choisir` générique | ✅ fait | `placement.rs`, 4 tests ; `kv_en_vram` appliqué dans `model.rs` |
| KV en VRAM | ✅ mesuré | ×1,93 au préremplissage 8 k, ×5,8 sur l’attention |
| tête 4 bits | ❌ refusée | +10 % de PPL ; `choisir_avec_perte` la refuse à 5 % |
| experts | 🧱 bloqué | **A6.2** — pas de MoE local à router |
| place + perte | 🔬 opt-in | A8.3 : le défaut déplace les portes ; **A8.3a** à venir |

## Le contrôle négatif


=== rapport-cache-experts-vram
# Rapport — un cache d'experts en VRAM pou
… [9466 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn -i \"A6\\.2\" docs/pilotage/backlog/*.md docs/pilotage/*.md | head -30; echo ---; ls docs/pilotage/backlog | head -60", "description": "Find A6.2 backlog fiche and mentions"}`

  ```
docs/pilotage/backlog/A6.2-moe-local.md:1:# A6.2 — Routage MoE appris (MoE local)
docs/pilotage/backlog/A6.2-moe-local.md:4:> **Ligne de roadmap** : A6.2 · **Fiche de résultat attendue** : rapport-a62-moe.md (à créer dans `reports/`)
docs/pilotage/backlog/A6.2-moe-local.md:14:A6.1 et A6.3 ont rendu leurs négatifs ; A6.2 bloqué par le matériel.
docs/pilotage/backlog/dependances.md:68:| **A6.2** | libre | A6 (acquis) | **pas** « aucun MoE local » : le MoE existe (Qwen3-30B-A3B Q4, 18 Go) ; le blocage est la **résidence mono-GPU 16 Go**, relevé le 06/11 | — | [A6.2-moe-local.md](A6.2-moe-local.md) |
docs/pilotage/backlog/dependances.md:162:| **A2.6** | partiel | `A2` mesuré ; `A6.2` est un plafond, pas une arête ; tête **refusée par décision**, `placement.rs` a **8 tests** | experts et placement dans la règle `choisir` |
docs/pilotage/backlog/dependances.md:167:**Ce qui n'y est pas, et pourquoi** : `A3.4`, `A5.4`, `A6.2`, `B1.5` sont bloqués par une
docs/pilotage/backlog/dependances.md:208:| **bloqués** | `A3.4`, `A5.4`, `B1.5` | ressource externe nommée : on prend la ligne suivante (`A6.2` est **libre** — voir l'état A du 06/11) |
docs/pilotage/backlog/index.md:86:| A6.2 | [Routage M
… [5121 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 20,60p reports/rapport-a26-bilan.md; echo ===; cat docs/pilotage/backlog/A6.2-moe-local.md", "description": "Read A2.6 bilan body and A6.2 fiche"}`

  ```
## Le contrôle négatif

- `choisir_avec_perte` refuse la tête 4 bits à un budget de 5 % : la place ne suffit pas, la perte
  décide. C’est le test qui a invalidé le 4 bits.
- Sans MoE local, les experts ne sont **pas mesurables** : ce n’est pas un échec de la règle, c’est
  une brique absente.

## Ce que ça change

A2.6 n’est plus une ligne « ouverte » : elle est **partielle et bloquée** pour sa partie experts.
La partie tête est **décidée** (refusée), la partie KV est **faite**, la partie générique est
**testée**. La suite est **A6.2** (bloqué) ou **A8.3a** (épingler le régime 1 %), pas un nouveau
code d’ordonnanceur.

## Ce qui pourrait le rendre faux

- **Bilan, pas une mesure** : les chiffres viennent des fiches existantes, pas d’un nouveau run.
- **La tête 4 bits** a été essayée puis revertée ; il n’y a pas de chiffre courant.
- **Les experts** ne sont pas mesurables sans A6.2 ; le jour où le MoE local existe, A2.6 rouvre.
- **Un autre modèle** peut déplacer la frontière KV/tête.

## Fichiers

- `reports/a26-bilan.json` — le bilan machine.
- `reports/rapport-a26-bilan.md` — cette fiche.
===
# A6.2 — Routage MoE appris (MoE local)

> **Statut** : bloquée · **Priorité** : P3 · *
… [1115 caractères tronqués]
  ```

- **bash** `{"command": "ls -la models/*.gguf 2>/dev/null | head -20; echo ---; ls tools | grep -i \"expert\\|moe\\|lot\\|placement\" ", "description": "List local models and expert tools"}`

  ```
-rw-r--r--. 1 stephane stephane 352972352 25 sep 17:13 models/Qwen2.5-0.5B-Q4_0.gguf
-rw-r--r--. 1 stephane stephane 531068480 25 sep 16:52 models/Qwen2.5-0.5B-Q8_0.gguf
---
analyse_experts_statique.py
analyse_reutilisation_experts.py
analyse_union_experts.py
banc-experts.py
clusters_moe.py
mesure_lot_disque.sh
mesure-prefill-lot.sh
mesurer_lecture_experts.py
porte-echange-experts.sh
porte-n3-placement.sh
v41_experts_reference.py
  ```

- **bash** `{"command": "grep -rn \"18,56\\|18.56\\|Qwen3-30B-A3B\" reports/rapport-etat-a.md docs/pilotage/*.md reports/rapport-a62* 2>/dev/null | head -20; echo ---; find / -maxdepth 4 -name \"*Qwen3-30B*\" 2>/dev/null | head; echo ---; ls /media 2>/dev/null; df -h | head -12", "description": "Locate the loca … [18 caractères tronqués]`

  ```
reports/rapport-etat-a.md:10:> l'absence d'un MoE : un **Qwen3-30B-A3B Q4 de 18 Go est présent et tourne**. Les **deux seuls
reports/rapport-etat-a.md:94:  `modeles/gguf/Qwen3-30B-A3B-Instruct-2507-Q4_K_M.gguf` (18 Go) est présent ; la machine a
docs/pilotage/en-cours.md:113:| **A — le moteur** | **A2.6** | A3.4 Colab ; A5.4 rig+ring ; **A6.2 libre** (MoE 18,56 Go, PPL 37,2013 ; résidence 16 GiB) | **A2.6** (experts et tête) ; **A6.2** rapport + A8.3b2 |
docs/pilotage/semaine-autonome.md:201:| **J4** | après-midi : coordination A | ✅ fiche (13/11) | A6.2 **libre** (MoE 18,56 Go, PPL **37,2013**, porte **54,5202**) ; A8.3b2 libre hors graphe | `commit J5.1` | rapport A6.2, harnais A8.3b2, D1–D8 |
---
---
Filesystem               Size  Used Avail Use% Mounted on
/dev/nvme0n1p2           828G  123G  705G  15% /
devtmpfs                  63G  8,0K   63G   1% /dev
tmpfs                     63G     0   63G   0% /dev/shm
efivarfs                 256K  140K  112K  56% /sys/firmware/efi/efivars
tmpfs                     26G  3,8M   26G   1% /run
none                     1,0M     0  1,0M   0% /run/credentials/systemd-journald.service
/dev/nvme0n1p2           828G  123G  705G  15% /.snapshots
… [215 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 60,120p reports/rapport-etat-a.md; echo ===; sed -n 215,235p reports/rapport-etat-a.md", "description": "Read etat-a A2.6 section"}`

  ```
| **A2.6** | **partiel, libre (P2)** | A2 acquis ; **pas** A6.2 pour les experts ; tête décidée | KV ×1,93/×5,8 ; lot **503/502 Mio**, **24,0 → 30,5 tok/s** (+27 %), PPL **15,8452 → 15,8443** (−0,006 %) ; tête **+10 % PPL** (constante, pas de run courant) | `cargo test placement` (8/8) ; `bash tools/mesure_lot_disque.sh models/Qwen2.5-0.5B-Q8_0.gguf <ids>` | règle générique + KV **faits** ; tête **refusée par décision** ; experts **non mesurés** mais **mesurables** sur le MoE local |
| **A3.2** | mesurée | A3 | **1 608 octets/flux** à 256 jetons ; **1,5 vs 3,5 ko** (÷2,3) | `bash tools/porte-flux.sh` (modes 2/4) | listes i16, échelles par bloc, indices par écarts, rejouées |
| **A3.3** | mesurée | A3.2 | attente ≈ calcul distant + **3,2 × latence** ; **1,01 / 1,99 / 4,89** ; débit **0,25 Mbit/s** | `bash tools/porte-topologie.sh` | le seuil est un chiffre, pas une intuition |
| **A3.4** | **bloquée** | A3 | — | aucune (compte Colab) | préremplissage réparti fait et fidèle ; runtime absent |
| **A5.4** | **bloquée** | A5 | — | aucune (carte Stratix V) | PE et lecteur DDR3 vérifiés ; carte absente |
| **A6.2** | **« bloquée » — faux** | A6 | aucun chiffre A6.2 ; MoE local : PPL **37,
… [6311 caractères tronqués]
  ```

- **bash** `{"command": "ls -la $HOME/IA/modeles/*.gguf 2>/dev/null; echo ---; nvidia-smi --query-gpu=name,memory.total --format=csv 2>/dev/null; echo ---; free -g | head -3; nproc", "description": "Verify MoE file, GPU, RAM, cores"}`

  ```
-rw-r--r--. 1 stephane stephane 18556686752  3 oct 13:17 /home/stephane/IA/modeles/qwen3-30b-a3b-Q4_K_M.gguf
---
name, memory.total [MiB]
Quadro RTX 5000, 16384 MiB
Quadro RTX 5000, 16384 MiB
---
               total        used        free      shared  buff/cache   available
Mem:             125          32          47          17          63          93
Swap:             62           4          58
40
  ```

- **bash** `{"command": "grep -n \"fn router\\|fn choix_experts\\|ts_experts\\|trace_experts\\|moe\\.\\|Moe\\|forward_lot\\|fn forward\\|fn matvec_expert\\|expert\" drave-core/src/model.rs | sed -n 1,200p", "description": "Map expert code paths with line numbers"}`

  ```
26:/// Convention de routage des experts — quatre familles, et une seule
34:    /// Kimi-K2.7 (`expert_gating_func = 2`), GLM-5.3 et GLM-5.3-Flash.
41:    /// renormalisation. DeepSeek V4-Flash (`expert_gating_func = 4`) et V4.1.
46:    /// Numéro `expert_gating_func` du GGUF, tel que llama.cpp le définit.
109:    // (`res_mix`, `PetitesK3`), MoE latent (`MoeK3`), SiTU (`situ`), et la
115:    // K3 est un instrument de vérification qui déquantifie les experts en f32
124:déquantifie les experts en f32 — il sert à VÉRIFIER, pas encore à faire tourner le modèle");
243:(+0,009 / +0,372 / +0,611 puis +4,070 nat à la position 3 — voir reports/rapport-mla-experts.md §7).");
264:    // Modèle à experts dont les tenseurs d'experts sont absents : ce n'est pas
266:    // Sauf en mode CLUSTERS : les experts y sont préfixés (`cl0/blk.0.…`), donc
270:    if !clusters && cfg.n_expert > 0 && g.tensor("blk.0.ffn_gate_exps.weight").is_none()
274:            "le modèle déclare {} experts mais aucun tenseur d'experts n'est lisible \
276:incomplet", cfg.n_expert));
307:    pub n_expert: usize,
308:    pub n_expert_used: usize,
311:    /// D'où vient `gating` : `expert_gating_func`, le JSON, ou le défau
… [13916 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"DRAVE_EXPERTS_RAM\\|DRAVE_GPU_EXPERTS\\|DRAVE_EXPERTS_GARDES\\|DRAVE_POIDS_CREUX\\|cache_experts\\|CacheExperts\" drave-core/src/*.rs src/*.rs 2>/dev/null | head -40", "description": "Find expert placement env vars usage"}`

  ```
drave-core/src/main.rs:1746:    if let Some(c) = mdl.cache_experts.as_ref() {
drave-core/src/main.rs:3647:    println!("  cache experts    : {:.1} Go en VRAM", plan.cache_experts_go);
drave-core/src/materiel.rs:80:    pub cache_experts_go: f64,
drave-core/src/materiel.rs:354:        let cache_experts_go = (vram - reserve - commun_go).max(0.0);
drave-core/src/materiel.rs:359:                cache_experts_go, vram, reserve, commun_go));
drave-core/src/materiel.rs:395:        Plan { threads, epinglage, lecteurs, cache_experts_go, kv_bits, raisons }
drave-core/src/model.rs:402:/// `DRAVE_EXPERTS_GARDES=<fichier>` : une ligne par couche, `couche e1 e2 …`,
drave-core/src/model.rs:416:        let chemin = std::env::var("DRAVE_EXPERTS_GARDES").ok()?;
drave-core/src/model.rs:1522:    /// **Formes creuses des experts** (`DRAVE_POIDS_CREUX=1`) : une par expert et par projection,
drave-core/src/model.rs:1547:    /// `-inf` élagué). Rempli depuis `DRAVE_EXPERTS_GARDES=<fichier>`, une ligne
drave-core/src/model.rs:1583:/// **Cache RAM des experts** (`DRAVE_EXPERTS_RAM` en Mo).
drave-core/src/model.rs:1603:pub struct CacheExpertsRam {
drave-core/src/model.rs:1610:impl CacheExpertsRam {
drave-core
… [1870 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 300,400p drave-core/src/materiel.rs", "description": "Read materiel.rs plan function"}`

  ```
let cpu = detecter_cpu();
        let gpus = detecter_gpus();
        let (ram_totale_go, ram_libre_go) = detecter_ram();
        let disques = detecter_disques();
        Materiel { cpu, gpus, ram_totale_go, ram_libre_go, disques }
    }

    /// Le plan de configuration, avec la raison de chaque choix.
    ///
    /// `ctx` et `taille_modele_go` orientent deux décisions : la quantification
    /// du cache KV et la répartition entre mémoire et disque.
    pub fn plan(&self, ctx: usize, taille_modele_go: f64, n_experts: usize,
                mo_par_expert: f64) -> Plan {
        let mut raisons = Vec::new();

        // --- threads : les cœurs PHYSIQUES, et les paires HT si on est pauvre.
        //
        // Mesuré : 20 cœurs = 22,5 Go/s, 20 cœurs + HT = 18,9 (rien de plus,
        // la bande passante sature) ; mais 10 cœurs = 14,7 contre 18,7 avec
        // leurs hyperthreads (+27 %, la latence mémoire est masquée et le L2
        // de 256 Ko est partagé). Trois fils par cœur régresse (15,0).
        let threads = self.cpu.physiques;
        raisons.push(format!(
            "threads = {} cœurs physiques ({} logiques détectés) — au-delà, la \
bande passante mémoire sature :
… [3963 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 1575,1700p drave-core/src/model.rs", "description": "Read RAM expert cache doc and behaviour"}`

  ```
///
/// L'attention ne voit plus que sa fenêtre brute (128 jetons) et le chemin
/// compressé (compresseur, blocs, cache partagé des consommatrices) n'est plus
/// exercé. Ce n'est PLUS V4.1 : c'est l'ablation qui dit si le défaut du modèle
/// vient de là. La rotation (YaRN des couches compressées) reste celle du
/// fichier, pour ne changer QU'UNE chose.
static SANS_COMPRESSION_EXERCICE: std::sync::OnceLock<bool> = std::sync::OnceLock::new();

/// **Cache RAM des experts** (`DRAVE_EXPERTS_RAM` en Mo).
///
/// Les octets d'un expert sont lus une fois depuis le NVMe et gardés en
/// mémoire. Le noyau en garde déjà une partie en `buff/cache`, mais il les
/// évince au rythme des ~330 Go lus par passe ; ici la résidence est explicite
/// et bornée.
///
/// **Ce que ça ne fait pas** : aucun octet n'est modifié, aucun ordre de
/// sommation ne change — un expert lu en RAM rend exactement ce que le mmap
/// rendait. Vérifié : 2 544 vides identiques au bit près, perplexité inchangée.
///
/// **MESURÉ PLUS LENT, et c'est le résultat qui compte.** La trace de routage
/// rendait l'idée plausible (63 jetons de wiki réel : 15 360 lectures, 3 817
/// experts distincts, 50 % des lectures dans 
… [4967 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 4940,5075p drave-core/src/model.rs", "description": "Read cache setup at model load"}`

  ```
trop long pour la VRAM — cache KV gardé en RAM",
                             machines.len(), caches_kv.first().map(|c| c.ctx).unwrap_or(0));
                    None
                }
            }
        } else { None };
        // ---- MLA : reconnu à ses tenseurs, sans aucune clé de configuration
        // (les rangs se lisent dans les FORMES, ce qui évite d'ajouter cinq
        // champs à `Cfg` et de les tenir à jour).
        let mla_cache = match mla.as_ref() {
            Some(v) => v.iter().map(|m| (vec![0f32; ctx * m.kv_lora], vec![0f32; ctx * m.qkr])).collect(),
            None => Vec::new(),
        };

        // Cache VRAM des experts : opt-in, et seulement sur un modèle à experts
        // au format MXFP4 (les autres formats ont leurs propres noyaux).
        let cache_experts = if std::env::var("DRAVE_GPU_EXPERTS").is_ok()
                               && crate::gpu::instance().is_some()
                               && cfg.n_expert > 0 {
            // Budget par défaut : ce que la VRAM peut donner sans étrangler le
            // reste. Mesuré : la VRAM lit à 84,9 Go/s contre 22,5 pour la RAM,
            // et un cache de 25 % de l'empreinte sert 80 % des 
… [6588 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"tete_gpu\\|DRAVE_TETE\\|tete_quantifiee\\|tete_restreinte\\|tete_garantie\\|tete_partielle\" drave-core/src/model.rs drave-core/src/main.rs | head -50", "description": "Find head placement flags and code"}`

  ```
drave-core/src/model.rs:2942:    pub tete_garantie: Option<Vec<u32>>,
drave-core/src/model.rs:2949:    pub tete_gpu: Option<crate::gpu::MatriceGpu>,
drave-core/src/model.rs:2967:    pub tete_restreinte: Option<Vec<u32>>,
drave-core/src/model.rs:2972:    pub tete_gpu_q6k: bool,
drave-core/src/model.rs:3020:    pub tete_partielle: bool,
drave-core/src/model.rs:4844:        let tete_quantifiee = g.q6k_blocks(&tete).is_some() || g.q4k_blocks(&tete).is_some()
drave-core/src/model.rs:4859:        let mut tete_gpu_q6k = false;
drave-core/src/model.rs:4860:        let tete_gpu = if std::env::var("DRAVE_GPU_TETE").is_ok()
drave-core/src/model.rs:4865:                tete_gpu_q6k = true;
drave-core/src/model.rs:4874:                         if tete_gpu_q6k { "Q6_K" } else { "Q8_0" },
drave-core/src/model.rs:4990:        let head4 = if q4 & 4 != 0 || tete_quantifiee {
drave-core/src/model.rs:5041:            tete_gpu, tete_gpu_q6k, head4, tete_restreinte: None,
drave-core/src/model.rs:5042:            normes_tete: None, ordre_normes: None, tete_garantie: None,
drave-core/src/model.rs:5050:            flux_brut: false, tete_partielle: false,
drave-core/src/model.rs:6538:        if self.flux_br
… [3050 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"tête\" reports/rapport-placement-kv-8k.md reports/rapport-regle-placement-perte.md | head -20; echo ===; head -40 reports/rapport-regle-placement-perte.md", "description": "Read head/rule placement reports"}`

  ```
reports/rapport-placement-kv-8k.md:10:est le cas type : sa **lecture par jeton** croît linéairement avec le contexte (5 337 jetons × 24 couches × 2 têtes
reports/rapport-placement-kv-8k.md:44:| VRAM | **84,9 Go/s** | le KV au-delà de ~2-4 k jetons, l'attention, la tête |
reports/rapport-placement-kv-8k.md:54:tête l'utiliseront par la même fonction. Quatre tests la couvrent (le gros KV → RAM, le petit → VRAM, le trop-gros →
reports/rapport-placement-kv-8k.md:57:**La tête : la règle de place a été essayée, puis revertée — et c'est une leçon.** La tête quantifiée tient en VRAM
reports/rapport-placement-kv-8k.md:59:33,8230** — **+10 %**. La règle de **place** ne dit rien de la **qualité** : le 4 bits de la tête est un choix de
reports/rapport-placement-kv-8k.md:65:- **Un seul modèle** (0,5 B) et **un seul prompt** ; le 3 B et le 14 B ont des poids et des têtes plus gros, et le
reports/rapport-regle-placement-perte.md:9:`DRAVE_KV_BITS_COUCHES="12-23:8"` **calculé au lieu d'être écrit** — la leçon de la tête (le 4 bits « qui tient »
reports/rapport-regle-placement-perte.md:24:- **La leçon de la tête est appliquée** : la règle ne choisit pas « ce qui tient » (la place) mais « ce qui tient
… [2487 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 4838,4900p drave-core/src/model.rs", "description": "Read head GPU placement code"}`

  ```
// Tête en 4 bits : la plus grosse matrice du modèle, donc le plus gros
        // gain possible sur un noyau déjà au mur de la bande passante.
        // La tête emprunte dès que la source est déjà quantifiée sur 4 ou
        // 6 bits : c'est exact (aucune requantification) et six fois plus
        // rapide que le chemin scalaire Q6_K, qui coûtait 42 % du temps par
        // jeton sur un 7B.
        let tete_quantifiee = g.q6k_blocks(&tete).is_some() || g.q4k_blocks(&tete).is_some()
            || g.mxfp4_blocks(&tete).is_some() || g.q4_blocks(&tete).is_some();
        // --- chemin GPU : la tête Q8_0 est copiée UNE fois dans la mémoire vidéo
        // La tête N'EST PAS déportée en l'état : mesuré sur gpt-oss, elle passe
        // de 23 à 159 ms. Le noyau lit une ligne par fil, donc des adresses
        // distantes de 34 octets : chaque accès d'une même warp tombe dans une
        // ligne de cache différente. Il faut une warp par ligne avec réduction
        // — à écrire avant de réactiver.
        // Le noyau « une warp par ligne » rend le déport de la tête enfin
        // rentable : l'ancien lisait une ligne par fil (23 → 159 ms mesurés).
        // Opt-in : `DRAVE_GPU_
… [2959 caractères tronqués]
  ```

- **bash** `{"command": "grep -rln \"DRAVE_GPU_TETE\" reports/*.md tools/*.sh docs/**/*.md 2>/dev/null | head; echo ---; grep -rn \"tête.*GPU\\|GPU.*tête\" reports/*.md | head -15", "description": "Find head-on-GPU measurements"}`

  ```
reports/rapport-coherence-docs.md
reports/rapport-drapeaux-ignores.md
reports/rapport-prefill-par-lots.md
docs/theorie/histoire.md
---
reports/bilan-multi-materiel.md:122:Le bon découpage, mesuré : **GPU** pour l'attention, les normes, la tête et
reports/rapport-architecture-memoire.md:13:| **VRAM** (noyau `warp par ligne`) | **84,9 Go/s** | banc GPU, tête de 144,6 Mo en 1,7 ms |
reports/rapport-etat-r.md:54:**Ce que je n'ai pas rejoué** : le modèle du banc R0.3 (GPU, Qwen2.5-0.5B), la tête de survol
reports/rapport-gpu-tandem.md:119:0,134 s du banc ne comptaient ni les têtes ni le `lot`. **Le GPU devient le levier aux paliers
reports/rapport-gpu-tandem-nvlink.md:41:du moteur l'annonce lui-même (« `[tête 4 bits] … 0 Mo` »). Les GPU sont au repos
reports/rapport-gpu-tandem-nvlink.md:112:   moteur a déjà un banc GPU (`--gpu-banc`) et un noyau de tête : la mécanique
reports/rapport-gpu-topk-selection.md:45:`--banc-topk N` avec `DRAVE_GPU=1`, Qwen2.5-0.5B Q4_0, k = 256, 2 têtes KV ×
reports/rapport-modele-drave.md:41:| **1** | **têtes précoces** : entraîner le 2 M en octets avec 3 têtes ✓ | l'**accord** par profondeur ✓ (aujourd'hui 0 % / 8,3 % ✗) | `n4_dessin_b.py --accord` ✓, `export
… [62 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"placement::\" drave-core/src/*.rs src/*.rs 2>/dev/null | head -40", "description": "List all placement rule call sites"}`

  ```
drave-core/src/model.rs:4720:                let (bits, _) = crate::placement::kv_precision(l, cfg.n_layer, budget_pct);
drave-core/src/model.rs:4889:            if !machines.is_empty() && !crate::placement::kv_en_vram(octets_kv, libre_vram) {
drave-core/src/model.rs:4893:                         crate::placement::RESERVE_VRAM >> 20);
drave-core/src/model.rs:4988:        let _tete_tient = crate::placement::choisir(octets_tete, octets_tete, libre_vram, 64 << 30)
drave-core/src/model.rs:4989:            == crate::placement::Support::Vram;
  ```

- **bash** `{"command": "grep -rn \"mod placement\\|placement\" drave-core/src/lib.rs drave-core/Cargo.toml 2>/dev/null | head; echo ---; ls drave-core/src | head -40; echo ---; grep -n \"\\[\\[bin\\]\\]\\|^name\" drave-core/Cargo.toml | head", "description": "Check crate layout for placement module"}`

  ```
---
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
---
2:name = "drave-core"
7:[[bin]]
8:name = "drave"
  ```

- **bash** `{"command": "grep -rn \"145,1\\|145.1 s\\|151,2\\|175,5\" reports/*.md | head -10", "description": "Find source of RAM cache timings"}`

  ```
reports/rapport-cache-chunker-applique.md:38:| 80 | 157,3 | 151,2 | ×1,0 |
reports/rapport-vitesse-v41.md:51:| **cache RAM des experts** (justifié par une trace : 50 % des lectures dans 394 experts, 31,9 % de réutilisation entre jetons consécutifs) | **plus lent** : passe ctx 32 = 145,1 s sans, 151,2 s à 4 Go (+4 %), 175,5 s à 32 Go (+21 %). Le noyau fait déjà ce travail (`buff/cache`, ~95 Go) : la copie ajoute un second exemplaire et du `memcpy` sans retirer les lectures NVMe. Drapeau éteint, verdict dans son annonce |
  ```

- **bash** `{"command": "sed -n 1,40p tools/porte-echange-experts.sh; echo ===; sed -n 1,40p tools/porte-n3-placement.sh", "description": "Read expert gate scripts"}`

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
… [3189 caractères tronqués]
  ```

- **bash** `{"command": "find /home/stephane/IA /home/stephane/Data13TB -maxdepth 6 -name '*.gguf' -size +1G 2>/dev/null | head -20; echo ---; ls -la /home/stephane/IA/modeles/ 2>/dev/null | head -30", "description": "Inventory local GGUF models"}`
