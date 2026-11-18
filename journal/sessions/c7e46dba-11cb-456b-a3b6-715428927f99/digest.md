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

  ```
/home/stephane/IA/modeles/qwen3-30b-a3b-Q4_K_M.gguf
/home/stephane/IA/modeles-lourds/DeepSeek-V4.1-Flash-Q2.gguf
/home/stephane/IA/artefacts/modeles-optimises/qwen3-30b-8clusters-v2/cluster-01.gguf
/home/stephane/IA/artefacts/modeles-optimises/qwen3-30b-8clusters-v2/cluster-03.gguf
/home/stephane/IA/artefacts/modeles-optimises/qwen3-30b-8clusters-v2/cluster-02.gguf
/home/stephane/IA/artefacts/modeles-optimises/qwen3-30b-8clusters-v2/cluster-07.gguf
/home/stephane/IA/artefacts/modeles-optimises/qwen3-30b-8clusters-v2/cluster-04.gguf
/home/stephane/IA/artefacts/modeles-optimises/qwen3-30b-8clusters-v2/cluster-00.gguf
/home/stephane/IA/artefacts/modeles-optimises/qwen3-30b-8clusters-v2/cluster-06.gguf
/home/stephane/IA/artefacts/modeles-optimises/qwen3-30b-8clusters-v2/cluster-05.gguf
/home/stephane/IA/artefacts/modeles-optimises/qwen3-30b-8clusters/cluster-01.gguf
/home/stephane/IA/artefacts/modeles-optimises/qwen3-30b-8clusters/cluster-03.gguf
/home/stephane/IA/artefacts/modeles-optimises/qwen3-30b-8clusters/cluster-02.gguf
/home/stephane/IA/artefacts/modeles-optimises/qwen3-30b-8clusters/cluster-07.gguf
/home/stephane/IA/artefacts/modeles-optimises/qwen3-30b-8clusters/cluster-04.gg
… [614 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"gpt-oss\\|MXFP4\\|mxfp4\" reports/rapport-cache-experts-vram.md reports/rapport-etat-a.md | head -10; echo ---; sed -n 22,70p reports/rapport-cache-experts-vram.md", "description": "Read VRAM expert cache report body"}`

  ```
reports/rapport-etat-a.md:46:| **A4** rejouer, comparer | ✅ fait | A1, A2 | Qwen ctx 256 = **19,3885** ; gpt-oss = **15,6017** ; MLA **5,2e-7** contre numpy, **0,999024** contre llama.cpp ; divergence KV 8 bits : couche 1, jeton 1, 857 neurones, **9,3e-5** | `bash tools/porte-diff-couche.sh` ; `bash tools/porte-harnais-invariants.sh` |
---

Un cache d'experts ne peut retirer **que** les 25,83 Go routés. Donc :

| taux de succès | gain |
|---|---:|
| 100 % (impossible) | **×1,41** |
| 70 % | ×1,26 |
| 47 % | ×1,16 |
| 25 % | ×1,08 |

## 2. Ce que la VRAM peut tenir

2 × 16 Go = 32 Go. Une matrice d'expert K3 (3 × 3072 × 3584 à 4,25 bits) pèse
**17,5 Mo** → **1 828 matrices**, soit **19,7 par couche sur 896**.

Un jeton en choisit **16**. Le cache tient donc **1,2 jeton** — à peine plus que
le besoin d'un seul. C'est la différence de fond avec Strata : chez eux 512
experts par couche et 34-50 Go de experts **tiennent tous en RAM** ; ici 896 par
couche et 1 508 Go au total.

## 3. Le taux de succès, mesuré sur le routage RÉEL de K3

Trace de routage obtenue du moteur (`DRAVE_K3_TRACE_EXPERTS`), 23 couches MoE ×
24 jetons de texte réel = 552 relevés, 16 experts par jeton :

| | K3 (896
… [958 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"DRAVE_GPU_EXPERTS\\|cache d'experts\" reports/*.md | head -20", "description": "Find VRAM expert cache experiments"}`

  ```
reports/INDEX.md:111:| [rapport-cache-experts-vram.md](rapport-cache-experts-vram.md) | Rapport — un cache d'experts en VRAM pour Kimi-K3 : mesuré, et pourquoi c'est non |
reports/rapport-budget-kimi-k3.md:25:   cache d'experts, routage — laisse donc **56 % du trafic** de côté.
reports/rapport-budget-kimi-k3.md:46:| **dense en RAM + cache d'experts (80 %)** | 40 + 3,4 Go/s | 1,6 + 1,5 = **3,1 s** | c'est le scénario que la mesure du bloc 30 rend crédible |
reports/rapport-cache-experts-vram.md:1:# Rapport — un cache d'experts en VRAM pour Kimi-K3 : mesuré, et pourquoi c'est non
reports/rapport-cache-experts-vram.md:23:Un cache d'experts ne peut retirer **que** les 25,83 Go routés. Donc :
reports/rapport-cache-experts-vram.md:85:1. **cache d'experts en VRAM** — mesuré ici, ×1,09 : non ;
reports/rapport-coordination-a.md:73:- **Précision qui change la décision** : le cache VRAM d'experts (`DRAVE_GPU_EXPERTS`) n'est
reports/rapport-drapeaux-ignores.md:113:| `DRAVE_GPU_TETE` · `DRAVE_GPU_KV` · `DRAVE_GPU_EXPERTS` · `DRAVE_GPU_EXPERTS_GO` | `Model::load` : 1391, 1413, 1505, 1508 | Inutiles sans `DRAVE_GPU` ; sans objet en BK/GB (bancs dédiés) | — |
reports/rapport-empreinte-memoire.md:4
… [1490 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 1983,2015p drave-core/src/model.rs; echo ...; sed -n 2026,2100p drave-core/src/model.rs", "description": "Read CacheExperts format support"}`

  ```
/// Cache VRAM des experts MoE (MXFP4), à éviction LRU.
///
/// Pourquoi un cache et pas un simple déport : un expert pèse 4,4 Mo et
/// gpt-oss en a 4 608 (36 couches × 128) — 60 Go, la VRAM n'en tient pas le
/// quart. Mais un expert SÉLECTIONNÉ est réutilisé d'un jeton à l'autre : c'est
/// exactement ce qu'un cache attrape. La mesure d'activation
/// (`reports/rapport-localite-activation.md`) dit qu'un préchargement STATIQUE
/// ne paie pas ; une résidence dynamique, si.
pub struct CacheExperts {
    /// Une entrée par (couche, expert) : ses trois matrices (gate, up, down).
    cartes: std::collections::HashMap<(usize, usize), (crate::gpu::MatriceGpu,
                                                       crate::gpu::MatriceGpu,
                                                       crate::gpu::MatriceGpu, u64)>,
    pub octets: usize,
    pub budget: usize,
    pub demandes: u64,
    pub manques: u64,
    pub evictions: u64,
    pub octets_envoyes: u64,
    ticks: u64,
    /// **Tampons libérés, réutilisables.** Deux raisons, mesurées le 12/10 :
    ///   * `charger_mxfp4` ALLOUE à chaque montage, et l'allocation est **37 %** (Q4_K) à **91 %**
    ///     (MXFP4) du coût d'un 
… [4642 caractères tronqués]
  ```

### 👤 Utilisateur

background job bash-290 (bash: find /home/stephane/IA /home/stephane/Data13TB -maxdepth 6 -name '*.gguf' -size +1G 2>/dev/null | head -20; echo ---; ls -la /home/stephane/IA/modeles/ 2>/dev/null | head -30) finished [status: completed, exit code: 0]. Read its output with job_output.

- **job_output** `{"job_id": "bash-290"}`

  ```
---
total 18121784
drwxr-xr-x.  3 stephane stephane        4096 12 oct 15:50 .
drwxr-xr-x  14 stephane stephane        4096 21 oct 16:30 ..
drwxr-xr-x.  4 stephane stephane        4096 12 oct 16:04 ollama
-rw-r--r--.  1 stephane stephane 18556686752  3 oct 13:17 qwen3-30b-a3b-Q4_K_M.gguf
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "sed -n 70,110p reports/rapport-vram-transfert.md; echo ===; sed -n 195,205p reports/rapport-etat-a.md; echo ===; sed -n 60,80p reports/rapport-coordination-a.md", "description": "Read VRAM transfer report and coordination note"}`

  ```
ligne « copie seule » ne s'imprimait pas. **Un silence qui ressemble à un succès** : c'est la
  même famille que « une mesure à un seul moment ne dit pas où ça casse » (`REPRISE.md` § 4).

---

## 5. Le pool, mesuré dans le moteur (13/10, 00 h 17)

Le **pool de tampons VRAM** est entré dans `CacheExperts` : les évictions rendent leurs matrices au
pool au lieu de les jeter, et un montage réutilise un tampon de la bonne forme (`gpu::recopier`),
sinon il alloue. Le budget compte **aussi** le pool, sans quoi on dépasserait la carte en croyant la
respecter.

Mesures — gpt-oss-120b MXFP4, 2 jetons, `DRAVE_GPU_EXPERTS_GO=8`, mêmes identifiants, données
chaudes en page cache (ce qui rend la comparaison **propre** : elle porte sur les montages, pas sur
le disque) :

| | temps mural | demandes | manques | montés sur le bus | **perplexité** |
|---|---|---|---|---|---|
| avant (allocation par montage) | 5,60 s | 288 | 264 (8,3 %) | 3,49 Go | 27736,1204 |
| **après (pool)** | **4,95 s** | 288 | 264 (8,3 %) | 3,49 Go | 27736,1204 |

**−11,6 % à travail identique** (mêmes 264 montages, mêmes 3,49 Go) : ~**2,5 ms par montage** de
13,2 Mo, là où le banc annonçait l'allocation à ~10 ms sur un tampon
… [3426 caractères tronqués]
  ```

- **bash** `{"command": "wc -l reports/rapport-coordination-a.md; sed -n 1,60p reports/rapport-coordination-a.md", "description": "Read coordination A report start"}`

  ```
474 reports/rapport-coordination-a.md
# A — coordination : A6.2 est libre, A8.3b2 est nommée mais hors du graphe

> **Ligne de roadmap** : A (le moteur) · **Tâche** : J4.4 · **Date** : 2026-11-13, 22 h 45 HNE
> · **Branche** : `s/v7` · **HEAD** : `dc78f223`
>
> **Verdict** : **A6.2 n'est pas bloquée.** Le MoE local de 18 Go existe et tourne — la porte
> de l'échange d'experts est **tenue** au HEAD, et `--ppl` redonne **37,2013**. Le seul blocage
> est la **résidence mono-GPU 16 Go** (17,28 GiB > 16 GiB), avec une précision : le cache VRAM
> d'experts n'est câblé que pour **MXFP4**, pas pour le **Q4_K** du modèle local. **A8.3b2 est
> nommée** par A8.3b (« instrumenter `forward_lot` »), mais elle est **absente du backlog, de la
> roadmap et du graphe** ; elle est libre. **Aucun fichier de A modifié** (ni `drave-core/`, ni
> `data/`, ni `work/`) : deux fichiers neufs, celui-ci et son JSON.

**En trois lignes.** (1) Le MoE `qwen3-30b-a3b-Q4_K_M` (18 556 686 752 o, 17,28 GiB,
`sha256 6c997b8a…`) est présent, chargé en **9,82 s**, et rend **37,2013** de perplexité à
`--limit 32` ; la porte `porte-echange-experts` rend **54,5202** à `N=16`, avec **768** décisions
de routage, l'invariant 
… [3226 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 80,140p reports/rapport-coordination-a.md", "description": "Read coordination A report recommendations"}`

  ```
- **Le cache RAM n'est pas la solution** : `DRAVE_EXPERTS_RAM` est mesuré **perdant** (+4 % à
  4 Go, +21 % à 32 Go) — le noyau garde déjà les pages ; le cache ajoute un second exemplaire.
- **Le cache VRAM n'est pas la solution immédiate** : `rapport-cache-experts-vram.md` donne un
  plafond de **×1,09** (pour un cache qui capte 28,7 % des lectures), contre ×3,1 pour le dense.

### 1.4 Ce qui est déjà mesuré pour A6.2 (et ce qui manque)

| mesure | résultat | source |
|---|---|---|
| regroupement par expert, **lot 192** | **74 496 → 4 804** lectures d'experts, **÷15,51** ; borne à l'infini **÷12,1** | `rapport-prefill-par-experts.md` § 2 |
| regroupement, **lot 64** | **÷7,08** | idem |
| regroupement, **lot 8** | **÷2,27** | idem |
| temps de préremplissage, **lot 192** | **×1,58** (le calcul dense et l'ordonnancement deviennent le mur) | idem § 1 |
| découpage en **8 clusters** | ventilation **3,08** nœuds contre **5,32** au hasard (**÷1,73**) ; couverture **0,607** | `rapport-decoupage-moe.md` |
| cache LRU, **25 %** des experts (32/128) | **74,8 à 87 %** des lectures servies | `rapport-reutilisation-experts.md` § 2 |
| cache LRU, **50 %** (64/128) | **92 à 93 %** | idem |
| ca
… [2438 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 100,125p reports/rapport-drapeaux-ignores.md; echo ===; grep -rn \"DRAVE_GPU_TETE\" reports/rapport-prefill-par-lots.md | head; echo ===; grep -rln \"Q6_K\" reports/*.md | head -10", "description": "Check head GPU flags measurements"}`

  ```
| `--patch` | I (643) · P (2746) | Ailleurs : *sans objet* | — |
| `--hebbian` | I (648) · P (2774) | Ailleurs : *sans objet* | — |
| `--hebb-q` | I (648) | **P : `Hebb::new(…, 0.1)` en dur (2774)** — la valeur passée est ignorée | 🟠 |
| `--hebb-out` | I (772) | **P : écrit `/tmp/act_log.bin` et `/tmp/loss_log.bin` en dur (2955-2957)** — le chemin demandé est ignoré | 🟡 |
| `--ffn-gain` | P : 2750 | **I : jamais déstructuré** (bloc 535-542) ni appliqué. Vérifié empiriquement (§7.2) | 🔴 |
| `--matrix` | D (68) · GB (2053-2063) | Ailleurs : *sans objet* (hérité du banc d'origine) | — |
| `--couches-locales` `--flux-liste` `--flux-blocs` | PR seulement (1670, 1677-1679) | Ailleurs : *sans objet* | — |

## 5. Variables d'environnement `DRAVE_*` (26)

| Variable | Appliquée dans (fichier:ligne) | Modes où elle est ignorée / inerte | Gravité |
|---|---|---|---|
| `DRAVE_GPU` | Portail de `gpu::instance()` (gpu.rs:788, 813) | Tous les modes qui ne demandent pas de GPU (PL, T, TE, D, BV, BM) ; les autres variables GPU ne font RIEN sans elle — documenté (REPRISE.md:229) mais silencieux à l'exécution | 🟡 |
| `DRAVE_GPU_TETE` · `DRAVE_GPU_KV` · `DRAVE_GPU_EXPERTS` · `DRAVE_GPU_EXPERTS_GO` | `
… [1713 caractères tronqués]
  ```

- **bash** `{"command": "head -40 tools/mesurer_lecture_experts.py; echo ===; head -30 tools/analyse_experts_statique.py", "description": "Read expert measurement tools"}`

  ```
#!/usr/bin/env python3
"""Lectures d'experts : série contre parallèle, sur un VRAI fichier froid.

    tools/mesurer_lecture_experts.py <shard.gguf> [nb_blocs] [nb_fils]

Pourquoi : le chargeur d'experts lit aujourd'hui les blocs un par un, en
s'appuyant sur le défaut de page du mmap. Le disque de cette machine a été
mesuré à **5,37 Go/s avec un lecteur et 31 Go/s avec seize** — donc si le défaut
de page sérialise, il y a un facteur 5 à prendre. Mais « il y a un facteur à
prendre » n'est pas une mesure, et le cache de pages a déjà fait mentir quatre
mécanismes de prélecture sur des modèles qui tenaient en RAM.

Ici on force le froid avec `posix_fadvise(DONTNEED)` sur les plages visées, et on
compare deux passes sur des blocs DIFFÉRENTS de même taille (comparaison
appariée) : une en touchant les pages une par une, l'autre en répartissant les
blocs entre `nb_fils` fils.
"""
import mmap
import os
import sys
import threading
import time

PAGE = 4096


def toucher(mm, base, octets):
    """Force la lecture des pages d'une plage (défaut de page, un par page)."""
    total = 0
    for off in range(base, base + octets, PAGE):
        total += mm[off]
    return total


def main():
    chem
… [1557 caractères tronqués]
  ```

- **bash** `{"command": "ls -la drave-core/target/release/drave 2>/dev/null; ls $HOME/IA/scratch/prerequis/ 2>/dev/null | head -20; echo ---; ls tools | grep -i \"ids\\|jetons\\|token\" | head", "description": "Check binary and token-id fixtures"}`

  ```
-rwxr-xr-x. 2 stephane stephane 3241600 17 nov 14:21 drave-core/target/release/drave
ids_0.5B_wt2_8192.txt
ids_0.5B_wt2_off0.txt
ids_0.5B_wt2_off10000.txt
ids_0.5B_wt2_off20000.txt
ids_0.5B_wt2_off30000.txt
ids_0.5B_wt2_off40000.txt
ids_0.5B_wt2_off50000.txt
ids_0.5B_wt2_off60000.txt
ids_oss_wt2.txt
ids_qwen05_wt2.txt
ids_qwen3_30b_wt2_off2.txt
ids_qwen3_30b_wt2_off3.txt
ids_qwen3_30b_wt2_off.txt
ids_qwen3_30b_wt2.txt
niah_4096_0.5.txt
---
entrainer_native_tokens.py
occupation_poids.py
porte-poids-creux.sh
porte-tokenizer-kimi.sh
tokenize_llama
tokenize_llama.cpp
tokenizer_bpe.py
tokenizer_kimi
  ```

- **bash** `{"command": "nvidia-smi --query-gpu=index,memory.used,utilization.gpu --format=csv; echo ---; sed -n 1,40p tools/mesure_lot_disque.sh", "description": "Check GPU idle state and lot measurement script"}`

  ```
index, memory.used [MiB], utilization.gpu [%]
0, 1 MiB, 0 %
1, 1 MiB, 0 %
---
#!/bin/bash
# mesure_lot_disque.sh — le préremplissage par LOTS, mesuré sur le DISQUE.
#
# POURQUOI CE SCRIPT EXISTE. Le batch 5 avait comparé `--lot 1` à `--lot 4..64`
# sur le 30B : la première passe avait lu 10,9 Go et les suivantes ZÉRO octet. Le
# protocole mesurait donc le cache de pages, pas le lot (§ 14 du rapport). Ce qui
# manquait n'était pas le modèle : c'était **l'éviction**. On l'obtient sans être
# root avec `posix_fadvise(POSIX_FADV_DONTNEED)` sur le fichier du modèle, qui
# jette ses pages du cache — donc chaque réglage de lot repart à froid.
#
# CE QUI EST MESURÉ, PAR RÉGLAGE : les octets réellement lus (`File system
# inputs`), le temps mur, le débit et la perplexité. Le lot doit diviser les
# LECTURES ; s'il ne les divise pas, la mesure le dira.
#
# Usage :
#   mesure_lot_disque.sh <modele.gguf> <ids> [--lots "1 2 4 8 16"] [--limit 192]
#                        [--ctx 512] [--threads 20] [--journal F]
set -u
D=${D:-./drave-core/target/release/drave}
MODELE=""; IDS=""; LOTS="1 2 4 8 16"; LIMIT=192; CTX=512; THREADS=20; JOURNAL=""
while [ $# -gt 0 ]; do
    case "$1" in
        --lots) L
… [786 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 22,90p reports/rapport-prefill-par-experts.md", "description": "Read prefill-by-experts timings"}`

  ```
| 2 | 24,51 | 7,83 | 889 | 51,1 | 1,36× |
| 4 | 23,29 | 8,27 | 864 | 50,3 | 1,43× |
| 8 | 23,17 | 8,27 | 854 | 50,6 | 1,43× |
| 16 | 22,45 | 8,53 | 851 | 49,3 | 1,48× |
| 32 | 21,91 | 8,77 | 839 | 48,9 | 1,52× |
| 64 | 21,27 | 9,03 | 831 | 48,2 | 1,56× |
| 192 | 21,00 | 9,20 | 827 | 47,8 | **1,58×** |

`mur_s` inclut le chargement du modèle (~27 s) : le gain porte bien sur
`prompt_s`, la seule colonne qui mesure le préremplissage.

## 2. Les octets

`tools/analyse_union_experts.py` lit la trace de routage réelle
(`DRAVE_TRACE_EXPERTS`, 48 couches × 194 jetons) et compte les matrices lues —
pas une estimation, un compte :

| bloc | lectures mode jeton | lectures mode groupe | gain | exp-éq/jeton |
|---|---|---|---|---|
| 1 | 74 496 | 74 496 | 1,00× | 8,000 |
| 2 | 74 496 | 56 904 | 1,31× | 6,111 |
| 4 | 74 496 | 43 427 | 1,72× | 4,664 |
| 8 | 74 496 | 32 847 | 2,27× | 3,527 |
| 16 | 74 496 | 23 946 | 3,11× | 2,572 |
| 32 | 74 496 | 16 446 | 4,53× | 1,766 |
| 64 | 74 496 | 10 526 | 7,08× | 1,130 |
| 192 | 74 496 | 4 804 | **15,51×** | 0,516 |

Borne (N → ∞) : 128 experts-équivalents par couche, soit 0,660 par jeton pour
cette invite — **12,1×** moins que le mode jeton. Le bloc de 192
… [1521 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"prof\\b\\|self.prof\\|provenance\\|profil_neurones\" drave-core/src/model.rs | head -30; echo ---; grep -n \"profil\\|prof\" drave-core/src/main.rs | head -20", "description": "Check timing profiler exposure"}`

  ```
300:/// Décision de **routage** lue dans les métadonnées, avec sa provenance.
302:/// La provenance compte : « sigmoïde » peut venir d'une clef GGUF explicite, du
2829:    /// provenance : 0 = attention, 1 = experts routés, 2 = partagé (FFN dense,
2890:    pub profil_neurones: Option<(Vec<u64>, Vec<f64>)>,   // (tirs, somme des |a|)
2922:    pub prof: [f64; 6],
5022:            profil_neurones: None,
5039:            stop_id: None, stop_id2: None, prof: [0.0; 6],
5400:    pub fn activer_profil_neurones(&mut self) {
5402:        self.profil_neurones = Some((vec![0u64; self.cfg.n_layer * largeur],
5405:            self.profil_experts = Some(vec![0u64; self.cfg.n_layer * self.cfg.n_expert]);
5407:        self.profil_jetons = 0;
5446:        let (tirs, poids) = self.profil_neurones.as_ref()?;
5448:        let n_tok = self.profil_jetons.max(1);
5505:        if let Some(exp) = self.profil_experts.as_ref() {
5507:            let n_tok = self.profil_jetons.max(1) as f64;
5535:        let Some((tirs, poids)) = self.profil_neurones.as_ref() else { return Ok(0) };
5537:        let n_tok = self.profil_jetons.max(1) as f32;
6170:            self.prof[0] += t_proj.elapsed().as_secs_f64();
6317: 
… [2363 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 2125,2155p drave-core/src/main.rs; echo ===; sed -n 6160,6175p drave-core/src/model.rs; echo ===; sed -n 6525,6545p drave-core/src/model.rs", "description": "Read prof printing and attribution sites"}`

  ```
for v in &hd.d { fic.write_all(&v.to_le_bytes()).unwrap(); }
        eprintln!("[hebb-diff] D sauvé dans {f} : {} valeurs", hd.d.len());
    }
    if let Some(hb) = mdl.hebb.as_ref() {
        use std::io::Write;
        let mut f = std::fs::File::create(&hebb_out).expect("création du fichier hebbien");
        for v in &hb.h { f.write_all(&v.to_le_bytes()).unwrap(); }
        f.flush().unwrap();
        let hb_ms = 0.0;   // le coût est mesuré à part
        let _ = hb_ms;
        println!("capteur hebbien : {} activations sur {} tokens, trace écrite dans {} ({:.1} Mo)",
                 hb.n_fire, hb.n_token,
                 hebb_out, (hb.h.len() * 4) as f64 / 1e6);
    }
    let n_tok = (st.n_prompt + st.n_gen) as f64;
    let p = mdl.prof;
    println!("postes (ms/token) : matvec-attn {:.1} | rope {:.1} | attention {:.1} | matvec+mlp {:.1} | total mesuré {:.1}",
             p[0] / n_tok * 1e3, p[1] / n_tok * 1e3, p[2] / n_tok * 1e3, p[3] / n_tok * 1e3,
             (p[0] + p[1] + p[2] + p[3]) / n_tok * 1e3);

    {
        use std::sync::atomic::Ordering;
        let a = model::TETE_ACTIFS.load(Ordering::Relaxed);
        let t = model::TETE_TOTAL.load(Ordering::Relaxed);
   
… [2341 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"6,2 ms\\|6.2 ms\" reports/*.md | head -10; echo ===; grep -rn -i \"tête.*Q6_K\\|Q6_K.*tête\\|tête.*Q8_0\" reports/*.md | head -10", "description": "Find head GPU timing source"}`

  ```
reports/rapport-cache-chunker.md:496:  (66,2 ms à 160, 266,2 ms à 320) ; lire les temps, pas les ratios.
reports/rapport-etat-a.md:44:| **A2** placement machine, KV, top-k, ordonnanceur | ✅ / ⚠️ **A2.6 partiel** | A1 | KV ×**1,93** préremplissage / ×**5,8** attention à 8 k ; KV paginé 968 → **13,2 ms** ; attention 22,16 → **3,29 ms/jeton** ; projections 15,6 → **6,2 ms** ; top-k **9,7e-7** à 1 M | `bash tools/porte-flux.sh` ; `bash tools/porte-topologie.sh` ; A2.6 : `cargo test placement` |
reports/rapport-prefill-par-lots.md:137:   le déport GPU (`DRAVE_GPU_TETE=1`, déjà mesuré à 6,2 ms/jeton contre 15,6 pour
reports/rapport-v41-couches-brouillon.md:31:**V4.1** — `deepseek41`, **1 046 tenseurs**, **365,70 Go** de poids, en-têtes lus en **66,2 ms**
===
reports/rapport-architecture-memoire.md:80:| 3 | rien — déjà là (`charger_tete`, `charger_proj`, Q4_K/Q6_K/Q8_0/MXFP4) | tête + embeddings | −95 ms |
reports/rapport-architecture-memoire.md:85:**Ce que le moteur sait déjà déporter** : Q4_K, Q6_K, Q8_0, MXFP4 (tête,
reports/rapport-c8-tete-entrainee.md:15:> `ids_0.5B-Q8.txt`, 8 192 jetons, tête liée `token_embd.weight` (Q8_0, gelée) + `output_norm`.
reports/rapport-etat-a.md:60:| **A2
… [999 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"TETE_ACTIFS\\|TETE_TOTAL\\|TETE_APPELS\" drave-core/src/model.rs | head -10; echo ===; grep -rn \"densite de l'entree\" -A3 -B10 drave-core/src/model.rs | head -40", "description": "Check head sparsity instrumentation"}`

  ```
3838:pub static TETE_ACTIFS: std::sync::atomic::AtomicU64 = std::sync::atomic::AtomicU64::new(0);
3839:pub static TETE_TOTAL: std::sync::atomic::AtomicU64 = std::sync::atomic::AtomicU64::new(0);
3840:pub static TETE_APPELS: std::sync::atomic::AtomicU64 = std::sync::atomic::AtomicU64::new(0);
9166:        TETE_ACTIFS.fetch_add(sv.idx.len() as u64, std::sync::atomic::Ordering::Relaxed);
9167:        TETE_TOTAL.fetch_add(h.len() as u64, std::sync::atomic::Ordering::Relaxed);
9168:        TETE_APPELS.fetch_add(1, std::sync::atomic::Ordering::Relaxed);
===
  ```

- **bash** `{"command": "sed -n 1,60p reports/rapport-logits-gpu-vs-cpu.md", "description": "Read GPU vs CPU logits report"}`

  ```
# Rapport — pourquoi le déport des projections change (ou non) la perplexité

**En une ligne** : sur un modèle **dense**, le déport des projections donne des
logits **identiques** au CPU (écart moyen 0,0000, fichiers bit à bit égaux) ; sur un
**MoE**, il les décale de **0,038 nat** en moyenne — **497 jetons sur 511 gardent le
même top-1** (14 divergent), et cela suffit à déplacer la perplexité de 1,2 %. L'hypothèse la plus simple, fortement étayée par ce contraste, est que de
minuscules écarts numériques **changent le routage des experts** (top-8 sur 128).

## Le doute, et d'où il vient

Au sprint 2, gpt-oss-120b MXFP4 à `--ctx 1024`, 511 jetons :

| chemin | perplexité | écart vs CPU |
|---|---|---|
| CPU | 18,5803 | — |
| GPU, miroir KV seul (`DRAVE_GPU_KV`) | 18,3074 | −1,47 % |
| GPU, projections seules (`DRAVE_GPU`) | 18,3538 | −1,22 % |

Ajouter le miroir KV aux projections ne pèse que **0,25 % de plus** : l'essentiel
(1,22 %) vient du déport des **projections** lui-même. Or les noyaux GPU sont exacts
(2e-7 sur la tête Q8_0, **0,00e0** bit à bit sur un expert MXFP4 — `REPRISE.md` §6,
huit chantiers, noyaux GPU). Une erreur de 1e-7 ne devrait pas peser
1,2 % de perplexité — d'
… [1745 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 25,60p reports/rapport-tete-garantie.md", "description": "Read head guarantee report"}`

  ```
la réponse juste, pas une réponse rapide et fausse.

**Exactitude vérifiée** : mêmes jetons générés avec et sans l'option, sur
Qwen2.5-0.5B, prompt « Le ciel est bleu parce que », 8 jetons gloutons :

```
sans  : [512, 13309, 321, 1788, 12422, 84, 13, 356]
avec  : [512, 13309, 321, 1788, 12422, 84, 13, 356]
```

C'est le contrat : la sortie ne change **pas**.

## 2. Ce qui est mesuré, et qui condamne la méthode

Sur la vraie matrice de tête (Qwen2.5-0.5B, 151 936 × 896 en Q8_0, 2 048 lignes
échantillonnées, activation aléatoire de même dimension) :

| grandeur | valeur |
|---|---|
| logit maximal | **+1,4283** |
| borne globale `max ‖w_i‖·‖h‖` | 18,0381 — **×12,6** le logit max |
| borne par blocs de 32 `Σ_b ‖w_b‖·‖h_b‖` | 17,6646 — ×12,4 |
| lignes encore candidates (globale) | **2 048 / 2 048 = 100 %** |
| lignes encore candidates (par blocs) | **2 048 / 2 048 = 100 %** |

Le raffinement par blocs n'apporte rien : la perte dominante est l'**alignement**
entre `w` et `h`, pas la structure par blocs. Et à l'exécution, la boucle de
paliers a effectivement calculé **151 936 lignes sur 151 936** à chaque jeton.

C'est le même verdict que la session précédente (borne « 5 à 20× trop lâc
… [260 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Test à blanc de la commande « tête » (PPL CPU de référence)

- **bash** `{"command": "ls -la $HOME/IA/scratch/prerequis/ids_0.5B_wt2_8192.txt; head -c 120 $HOME/IA/scratch/prerequis/ids_0.5B_wt2_8192.txt; echo; grep -n \"DRAVE_GPU\\b\" drave-core/src/gpu.rs | head -10", "description": "Inspect ids file and GPU gate"}`

  ```
-rw-r--r--. 1 stephane stephane 394684 13 oct 02:37 /home/stephane/IA/scratch/prerequis/ids_0.5B_wt2_8192.txt
198,284,8397,425,10965,465,284,14731,8397,425,10965,465,374,458,6364,4531,1154,12425,323,33496,12089,659,1260,1030,264,8
1549:/// Instance unique du processus. `DRAVE_GPU` active le déport ; sans lui, aucune
1559:        if std::env::var("DRAVE_GPU").is_err() { return None; }
1585:        // `DRAVE_GPU=0` force le CPU ; `DRAVE_GPU=1` force la tentative GPU.
1586:        if std::env::var("DRAVE_GPU").map(|v| v.trim() == "0").unwrap_or(false) {
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && time ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --ppl $HOME/IA/scratch/prerequis/ids_0.5B_wt2_8192.txt --ctx 512 --limit 32 --threads 8 2>&1 | tail -12", "description": "Baseline PPL and per-token timings on 0.5B … [23 caractères tronqués]`

  ```
=== perplexité 56.7642 sur 31 tokens (0 événements, 1.3 s) ===
    24.6 tok/s effectifs (avant + tête)
    attention : 0.01 M paires (requête, clé) par token
    projections : 0.0 M événements par token
    paires (poids × activation) par token : attention 45.5 M · experts 0.0 M · partagé 460.0 M · scores 6 K · total 505.5 M
    occupation des poids : 99.2 % de non-nuls (489995762 sur 493961216) — attention 99.1 % · experts 0.0 %
    ⇒ si la représentation était CREUSE (non-nuls × activations vivantes, hypothèse) : 501.4 M paires par token au lieu de 505.5 M (÷1.01)
    dont en listes (une paire y est un événement) : 0.0 M — le reste est dense (déquantifié ou f32)
    part de l'attention dans le flux total : 9.0 %
    postes (ms/token) : projets-attn 3.01 | rope 0.65 | attention 4.10 | proj+mlp 27.43 | somme 35.19 | reste (tête + échantillonnage) 8.87
    dont tête de sortie 7.43 | notation log-sum-exp 1.42 (le reste du « reste » n'est pas chronométré)
    dont attention : scores 0.12 | softmax 0.07 | somme pondérée + écriture KV 3.91
[stderr]

real	0m2,871s
user	0m15,179s
sys	0m0,798s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && time env DRAVE_GPU=1 DRAVE_GPU_TETE=1 ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --ppl $HOME/IA/scratch/prerequis/ids_0.5B_wt2_8192.txt --ctx 512 --limit 32 --threads 8 2>&1 | tail -14", "description": "Head on G … [42 caractères tronqués]`

  ```
31 tokens notés — perplexité cumulée 56.764  (28.4 tok/s)

=== perplexité 56.7642 sur 31 tokens (0 événements, 1.1 s) ===
    28.4 tok/s effectifs (avant + tête)
    attention : 0.01 M paires (requête, clé) par token
    projections : 0.0 M événements par token
    paires (poids × activation) par token : attention 45.5 M · experts 0.0 M · partagé 460.0 M · scores 6 K · total 505.5 M
    occupation des poids : 99.2 % de non-nuls (489995762 sur 493961216) — attention 99.1 % · experts 0.0 %
    ⇒ si la représentation était CREUSE (non-nuls × activations vivantes, hypothèse) : 501.4 M paires par token au lieu de 505.5 M (÷1.01)
    dont en listes (une paire y est un événement) : 0.0 M — le reste est dense (déquantifié ou f32)
    part de l'attention dans le flux total : 9.0 %
    postes (ms/token) : projets-attn 2.91 | rope 0.64 | attention 4.02 | proj+mlp 27.92 | somme 35.49 | reste (tête + échantillonnage) 2.97
    dont tête de sortie 1.82 | notation log-sum-exp 1.28 (le reste du « reste » n'est pas chronométré)
    dont attention : scores 0.21 | softmax 0.07 | somme pondérée + écriture KV 3.73
[stderr]

real	0m2,679s
user	0m12,534s
sys	0m0,767s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && env DRAVE_GPU=1 DRAVE_GPU_TETE=1 ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --ppl $HOME/IA/scratch/prerequis/ids_0.5B_wt2_8192.txt --ctx 512 --limit 32 --threads 8 2>&1 | grep -i \"gpu\\|tête\\|perplex\" | head - … [54 caractères tronqués]`

  ```
[gpu] GPU 1 · tête 151936 × 896 (Q8_0) sur le GPU : 145 Mo résidents, 16571 Mo libres
      31 tokens notés — perplexité cumulée 56.764  (28.3 tok/s)
=== perplexité 56.7642 sur 31 tokens (0 événements, 1.1 s) ===
    28.3 tok/s effectifs (avant + tête)
    postes (ms/token) : projets-attn 2.92 | rope 0.68 | attention 3.97 | proj+mlp 28.18 | somme 35.74 | reste (tête + échantillonnage) 2.91
    dont tête de sortie 1.80 | notation log-sum-exp 1.27 (le reste du « reste » n'est pas chronométré)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for m in models/Qwen2.5-0.5B-Q8_0.gguf models/Qwen2.5-0.5B-Q4_0.gguf; do echo \"== $m\"; ./drave-core/target/release/drave \"$m\" --tensors 2>/dev/null | grep -E \"output|token_embd\" | head -4; done; echo ---; grep -n '\"\\-q\"\\|q4 … [109 caractères tronqués]`

  ```
== models/Qwen2.5-0.5B-Q8_0.gguf
  Q8_0     token_embd.weight                      [151936, 896] · 136.1 M poids · fichier 0
  Q8_0     blk.0.attn_output.weight               [896, 896] · 0.8 M poids · fichier 0
  Q8_0     blk.1.attn_output.weight               [896, 896] · 0.8 M poids · fichier 0
  Q8_0     blk.10.attn_output.weight              [896, 896] · 0.8 M poids · fichier 0
== models/Qwen2.5-0.5B-Q4_0.gguf
  Q8_0     token_embd.weight                      [151936, 896] · 136.1 M poids · fichier 0
  Q4_0     blk.0.attn_output.weight               [896, 896] · 0.8 M poids · fichier 0
  Q4_0     blk.1.attn_output.weight               [896, 896] · 0.8 M poids · fichier 0
  Q4_0     blk.10.attn_output.weight              [896, 896] · 0.8 M poids · fichier 0
---
1696:            "--q4" => { o.q4 |= 3; 1 }
1697:            "--q4-ffn" => { o.q4 = (o.q4 & 4) | 1; 1 }
1698:            "--q4-attn" => { o.q4 = (o.q4 & 4) | 2; 1 }
1699:            "--q4-tout" => { o.q4 |= 7; 1 }
[stderr]
grep: warning: stray \ before -
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && env ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --ppl $HOME/IA/scratch/prerequis/ids_0.5B_wt2_8192.txt --ctx 512 --limit 32 --threads 8 --q4-tout 2>&1 | grep -E \"tête|perplexité\" | head -8", "description": "Nega … [41 caractères tronqués]`

  ```
[tête 4 bits] 151936 × 896 → 4.50 b/poids, 72 Mo, 1.3 s
      31 tokens notés — perplexité cumulée 79.949  (42.4 tok/s)
=== perplexité 79.9488 sur 31 tokens (0 événements, 0.7 s) ===
    42.4 tok/s effectifs (avant + tête)
    postes (ms/token) : projets-attn 1.91 | rope 0.37 | attention 2.62 | proj+mlp 12.96 | somme 17.85 | reste (tête + échantillonnage) 9.40
    dont tête de sortie 6.50 | notation log-sum-exp 1.31 (le reste du « reste » n'est pas chronométré)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short | head; echo ---; git log -1 --format='%h %ad' --date=iso; echo ---; wc -l reports/INDEX.md; head -8 reports/INDEX.md", "description": "Check clean tree and INDEX format"}`

  ```
M tools/entrainer_native.py
?? reports/banc-grammaticalite-100m.json
---
bb57604c 2026-11-18 09:00:52 -0500
---
786 reports/INDEX.md
# Index des fiches de reports/

> **Généré** par `tools/index_reports.py` — **778 fiches**. Les fichiers
> d'infrastructure (`README.md`, `INDEX.md`, `historique-*`) sont exclus du tableau ;
> la page d'état, elle, compte tous les `.md` de `reports/`.

| fiche | titre |
|---|---|
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -3; echo ---; grep -n '\"-q\"\\|q4:' drave-core/src/main.rs | head; grep -n \"q4\" drave-core/src/main.rs | sed -n 1,15p", "description": "Check HEAD movement and q4 flag"}`

  ```
bb57604c N — LE CORPUS D'ENTRAÎNEMENT EST ÉPINGLÉ : TRAIN 0876b608… (1 017 487 092 o, 2 480 766 lignes), VAL fbddef91…, MANIFESTE fae5bb73…
52b0b78d N4 — LE 100 M MESURÉ À RÉGLAGES APPARIÉS : LA RÉPÉTITION TOMBE DE 9 À 6, LE VOCABULAIRE NE GAGNE RIEN (0,882 CONTRE 0,884)
d649467c CONSIGNES — LA RÈGLE 12 POUR TOUS LES AGENTS : L'API EN FENÊTRE REMISÉE (11 h 30 → 19 h 30 EST), LE LOCAL EN PLEINE, DEUX FILES PAR CHANTIER ; LE PLAN DÉTAILLÉ LIÉ
---
1346:    q4: u8, b6: u8, keep: f32, bits: u32, moe_topk: usize, pin: bool,
843:        let y4 = pool.matvec_dense_q4(&d4, &xv, 1.0);
1346:    q4: u8, b6: u8, keep: f32, bits: u32, moe_topk: usize, pin: bool,
1696:            "--q4" => { o.q4 |= 3; 1 }
1697:            "--q4-ffn" => { o.q4 = (o.q4 & 4) | 1; 1 }
1698:            "--q4-attn" => { o.q4 = (o.q4 & 4) | 2; 1 }
1699:            "--q4-tout" => { o.q4 |= 7; 1 }
1768:        ctx_impose, threads_impose, abits_impose, dense, auto, q4, b6, attn_sinks_impose,
1783:    let mut mdl = model::Model::load_partiel(path, ctx, n_threads, dense, keep, auto, q4, b6,
6590:    let nom_q4k = opt.matrix.clone();
6591:    if !mx && nom_q4k != "output.weight" && nom_q4k != "token_embd.weight"
6592:       
… [320 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -1 --format='%h %s' -- drave-core/target/release/drave 2>/dev/null; ls -la drave-core/target/release/drave; git show -s --format='%h %ad' --date=iso HEAD", "description": "Compare binary timestamp to HEAD"}`

  ```
a44414d2 Hygiène : sortir les artefacts de compilation du dépôt, et committer la sentinelle
-rwxr-xr-x. 2 stephane stephane 3241600 17 nov 14:21 drave-core/target/release/drave
bb57604c 2026-11-18 09:00:52 -0500
  ```

- **bash** `{"command": "cat /proc/loadavg; pgrep -af \"drave|llama-server\" | head -5; echo ---; free -g | sed -n 2p", "description": "Check machine load before expert run"}`

  ```
15.91 7.01 4.43 24/2658 319390
319383 bash -c cat /proc/loadavg; pgrep -af "drave|llama-server" | head -5; echo ---; free -g | sed -n 2p
---
Mem:             125          42          37          17          64          83
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"n_expert\\|expert_feed\\|moe_intermediate\" drave-core/src/model.rs | sed -n 1,5p; echo ---; M=\"$HOME/IA/modeles/qwen3-30b-a3b-Q4_K_M.gguf\"; ./drave-core/target/release/drave \"$M\" --config 2>/dev/null | head -30", "desc … [43 caractères tronqués]`

  ```
270:    if !clusters && cfg.n_expert > 0 && g.tensor("blk.0.ffn_gate_exps.weight").is_none()
276:incomplet", cfg.n_expert));
307:    pub n_expert: usize,
308:    pub n_expert_used: usize,
326:    // pris pour un modèle dense (`n_expert = 0`), donc exécuté sans un seul
---
modèle        : /home/stephane/IA/modeles/qwen3-30b-a3b-Q4_K_M.gguf
architecture  : qwen3moe
couches       : 48 · cachés 2048
experts       : 128 par couche, 8 par jeton · FFN expert 768
routage       : softmax (source : défaut du moteur) · renormalisation oui · échelle aucune
calculable    : oui (passe avant implémentée)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"self\\.prof\\[\" drave-core/src/model.rs", "description": "List profiler attribution sites"}`

  ```
6170:            self.prof[0] += t_proj.elapsed().as_secs_f64();
6317:            self.prof[2] += t_att.elapsed().as_secs_f64();
6535:            self.prof[3] += t_ffn.elapsed().as_secs_f64();
7943:                self.prof[0] += tm.elapsed().as_secs_f64();
7977:                self.prof[1] += tr.elapsed().as_secs_f64();
8036:                    self.prof[4] += t_scores.elapsed().as_secs_f64();
8054:                    self.prof[5] += t_soft.elapsed().as_secs_f64();
8295:            self.prof[2] += ta.elapsed().as_secs_f64();
8607:                self.prof[3] += tf.elapsed().as_secs_f64();
8676:            self.prof[3] += tf.elapsed().as_secs_f64();
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"fn forward\\b\\|fn forward_lot\\|fn forward_jeton\\|pub fn forward\" drave-core/src/model.rs | head", "description": "Locate forward functions"}`

  ```
5967:    pub fn forward_lot(&mut self, toks: &[u32], pos0: usize) -> Vec<Vec<f32>> {
7363:    pub fn forward_mla(&mut self, tok: u32, pos: usize) -> Vec<f32> {
7496:    pub fn forward(&mut self, tok: u32, pos: usize) -> Vec<f32> {
  ```

### 🤖 Assistant

⏵ Mesure courte du coût par jeton des experts sur le MoE local

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && M=\"$HOME/IA/modeles/qwen3-30b-a3b-Q4_K_M.gguf\" && IDS=\"$HOME/IA/scratch/prerequis/ids_qwen3_30b_wt2.txt\" && time env DRAVE_TAMPONS=1 ./drave-core/target/release/drave \"$M\" --ppl \"$IDS\" --ctx 512 --limit 8 --threads 8 2>&1 | g … [156 caractères tronqués]`

  ```
[modele] 48 couches chargées en 8.616415621s — listes 0.91 Go , 8 threads
[config] mélanges d'experts chargés : 48/48 couches · mapping absent (experts en clair dans le fichier)
[config] puits appris sur 0/48 couches · n_rot 128 · ffn 6144 · experts 128
[tête 4 bits] 151936 × 2048 → 6.56 b/poids, 0 Mo, 0.0 s
[tampons] lecture séquentielle des experts dans nos tampons (les experts retenus sont lus en `pread`, par offset croissant, puis le calcul lit ces octets)
       7 tokens notés — perplexité cumulée 799.856  (2.0 tok/s)
=== perplexité 799.8557 sur 7 tokens (0 événements, 3.5 s) ===
    2.0 tok/s effectifs (avant + tête)
    attention : 0.01 M paires (requête, clé) par token
    paires (poids × activation) par token : attention 1035.4 M · experts 2070.8 M · partagé 311.2 M · scores 8 K · total 3417.4 M
    occupation des poids : 100.0 % de non-nuls (12582912 sur 12582912) — attention 0.0 % · experts 0.0 %
    ⇒ si la représentation était CREUSE (non-nuls × activations vivantes, hypothèse) : 3417.3 M paires par token au lieu de 3417.3 M (÷1.00)
    ⚠ 28991029248 poids d'experts NON comptés (format 4 bits sans décodeur d'occupation) : le chiffre est PARTIEL
    dont en listes (une 
… [380 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && M=\"$HOME/IA/modeles/qwen3-30b-a3b-Q4_K_M.gguf\" && IDS=\"$HOME/IA/scratch/prerequis/ids_qwen3_30b_wt2.txt\" && time env DRAVE_TAMPONS=1 ./drave-core/target/release/drave \"$M\" --ppl \"$IDS\" --ctx 512 --limit 8 --threads 8 2>&1 | g … [133 caractères tronqués]`

  ```
7 tokens notés — perplexité cumulée 799.856  (2.1 tok/s)
=== perplexité 799.8557 sur 7 tokens (0 événements, 3.4 s) ===
    2.1 tok/s effectifs (avant + tête)
    postes (ms/token) : projets-attn 99.20 | rope 4.67 | attention 106.62 | proj+mlp 352.80 | somme 563.29 | reste (tête + échantillonnage) -78.41
    dont tête de sortie 21.15 | notation log-sum-exp 2.11 (le reste du « reste » n'est pas chronométré)
[stderr]

real	0m13,597s
user	0m39,031s
sys	0m6,142s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && M=\"$HOME/IA/modeles/qwen3-30b-a3b-Q4_K_M.gguf\" && IDS=\"$HOME/IA/scratch/prerequis/ids_qwen3_30b_wt2.txt\" && for T in 4 16 40; do echo \"== threads $T\"; env DRAVE_TAMPONS=1 ./drave-core/target/release/drave \"$M\" --ppl \"$IDS\"  … [156 caractères tronqués]`

  ```
== threads 4
    postes (ms/token) : projets-attn 149.19 | rope 4.58 | attention 156.25 | proj+mlp 433.64 | somme 743.66 | reste (tête + échantillonnage) -117.25
== threads 16
    postes (ms/token) : projets-attn 77.35 | rope 4.70 | attention 85.44 | proj+mlp 462.67 | somme 630.16 | reste (tête + échantillonnage) -59.46
== threads 40
    postes (ms/token) : projets-attn 692.59 | rope 5.68 | attention 700.60 | proj+mlp 6112.42 | somme 7511.29 | reste (tête + échantillonnage) -675.00
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && M=\"$HOME/IA/modeles/qwen3-30b-a3b-Q4_K_M.gguf\" && IDS=\"$HOME/IA/scratch/prerequis/ids_qwen3_30b_wt2.txt\" && for V in \"\" \"DRAVE_EXPERTS_RAM=4096\"; do echo \"== env: ${V:-defaut}\"; env $V ./drave-core/target/release/drave \"$M … [215 caractères tronqués]`

  ```
== env: defaut
[config] cache KV : 32 bits, 0.10 Go pour 512 jetons
    postes (ms/token) : projets-attn 65.68 | rope 3.89 | attention 71.50 | proj+mlp 194.82 | somme 335.89 | reste (tête + échantillonnage) -47.97
== env: DRAVE_EXPERTS_RAM=4096
[config] cache KV : 32 bits, 0.10 Go pour 512 jetons
[experts] cache RAM des experts : 4096 Mo — ATTENTION, mesuré PLUS LENT que le cache de pages du noyau (ctx 32 : +4 % à 4 Go, +21 % à 32 Go ; voir `CacheExpertsRam`). Aucun octet du calcul ne change, mais le temps, si.
    postes (ms/token) : projets-attn 65.02 | rope 3.56 | attention 70.46 | proj+mlp 567.91 | somme 706.95 | reste (tête + échantillonnage) -44.72
31.37 20.98 10.65 4/2585 343314
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && M=\"$HOME/IA/modeles/qwen3-30b-a3b-Q4_K_M.gguf\" && IDS=\"$HOME/IA/scratch/prerequis/ids_qwen3_30b_wt2.txt\" && for T in 4 16; do echo \"== defaut, threads $T\"; ./drave-core/target/release/drave \"$M\" --ppl \"$IDS\" --ctx 512 --lim … [149 caractères tronqués]`

  ```
== defaut, threads 4
    postes (ms/token) : projets-attn 120.96 | rope 3.56 | attention 126.25 | proj+mlp 279.09 | somme 529.86 | reste (tête + échantillonnage) -93.50
== defaut, threads 16
    postes (ms/token) : projets-attn 52.48 | rope 3.60 | attention 57.74 | proj+mlp 188.82 | somme 302.64 | reste (tête + échantillonnage) -39.40
13.67 17.77 10.19 5/2583 349972
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ./drave-core/target/release/drave $HOME/IA/modeles/qwen3-30b-a3b-Q4_K_M.gguf --tensors 2>/dev/null | grep -E \"blk\\.(0|1)\\.ffn_(gate|up|down)_exps\" | head -6; echo ---; ./drave-core/target/release/drave $HOME/IA/modeles/qwen3-30b- … [116 caractères tronqués]`

  ```
Q6_K     blk.0.ffn_down_exps.weight             [128, 2048, 768] · 201.3 M poids · fichier 0
  Q4_K     blk.0.ffn_gate_exps.weight             [128, 768, 2048] · 201.3 M poids · fichier 0
  Q4_K     blk.0.ffn_up_exps.weight               [128, 768, 2048] · 201.3 M poids · fichier 0
  Q6_K     blk.1.ffn_down_exps.weight             [128, 2048, 768] · 201.3 M poids · fichier 0
  Q4_K     blk.1.ffn_gate_exps.weight             [128, 768, 2048] · 201.3 M poids · fichier 0
  Q4_K     blk.1.ffn_up_exps.weight               [128, 768, 2048] · 201.3 M poids · fichier 0
---
144
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ./drave-core/target/release/drave $HOME/IA/modeles/qwen3-30b-a3b-Q4_K_M.gguf --tensors 2>/dev/null | head -5", "description": "Inspect tensors listing format"}`

  ```
qwen3moe · 1 fichiers · 579 tenseurs · 18.55 Go de poids · en-têtes lus en 62.260496ms
 · block_count 48 · embedding_length 2048 · feed_forward_length 6144 · attention.head_count 32 · attention.head_count_kv 4 · expert_count 128 · expert_used_count 8 · context_length 262144
  Q6_K     output.weight                          [151936, 2048] · 311.2 M poids · fichier 0
  F32      output_norm.weight                     [2048] · 0.0 M poids · fichier 0
  Q4_K     token_embd.weight                      [151936, 2048] · 311.2 M poids · fichier 0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,45p tools/budget_execution_locale.py", "description": "Read budget tool header and usage"}`

  ```
#!/usr/bin/env python3
"""budget_execution_locale.py — ce qu'un placement implique, en jetons/s.

Pour un GGUF (découpé ou non, **complet ou en cours de téléchargement**), calcule
les octets de poids lus par jeton, puis ce que chaque placement permet :

    tout sur disque dur · tout sur NVMe · tout en RAM · deux nœuds (moitié chacun)
    · grappes dimensionnées pour tenir en RAM

Les débits sont ceux **mesurés sur cette machine** (02-03/10) :
    disque dur 12 To (WDC WD120EFGX, ROTATEUR)   ~0,2 Go/s, aléatoire bien pire
    NVMe Fanxiang S660 (node NUMA 0)             2,3 Go/s à 1 flux · **3,4 Go/s à 4**
    RAM                                          9,6 Go/s à 1 fil · **40 Go/s à 8 fils**
    bus PCIe x8                                 6,5 Go/s (chiffre du dépôt, non remesuré)
    NVLink entre les deux GPU                    25,8 Go/s (nvidia-smi nvlink)

Les chiffres de RAM et de NVMe ont été **remesurés** le 03/10 (bloc 30) parce que
celui de la RAM (« 20 Go/s ») venait du dépôt, sans méthode : la somme d'un
tableau de 32 Go donne 9,6 Go/s à UN fil et **40,3 Go/s à 16 fils** — c'est le
débit agrégé qui compte pour un moteur à 16 fils. Le NVMe, lui, passe de 2,26 à
3,39 Go/s 
… [657 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,30p tools/analyse_octets_par_jeton.py; echo ===; /home/stephane/gpu-env/bin/python tools/analyse_octets_par_jeton.py $HOME/IA/modeles/qwen3-30b-a3b-Q4_K_M.gguf 2>&1 | head -40", "description": "Exact expert bytes per token f … [10 caractères tronqués]`

  ```
#!/usr/bin/env python3
"""analyse_octets_par_jeton.py — combien d'octets de POIDS un jeton fait-il lire ?

Lit l'en-tête d'un GGUF (sans lire les données), repère les tenseurs d'experts,
et calcule le volume lu par jeton :

    octets/jeton = Σ_couches [ (k_routés / n_experts) × octets(exps)
                               + octets(expert partagé) ]

C'est le chiffre qui décide de trois choses :
  - si un modèle tient en RAM (sinon chaque passe relit ces octets du disque) ;
  - ce que coûterait un chemin GPU qui streame les poids (PCIe) au lieu de les
    garder en VRAM ;
  - ce que coûte un découpage en nœuds (chaque nœud ne lit que sa part).

Usage : analyse_octets_par_jeton.py <modele.gguf> [--experts-par-jeton N]
                                    [--tous]
"""
import struct
import sys

# Éléments par bloc et octets par bloc des formats ggml (le strict nécessaire ;
# un type absent est signalé, jamais deviné).
TYPES = {
    0: ("F32", 1, 4), 1: ("F16", 1, 2), 2: ("Q4_0", 32, 18), 3: ("Q4_1", 32, 20),
    6: ("Q5_0", 32, 22), 7: ("Q5_1", 32, 24), 8: ("Q8_0", 32, 34), 9: ("Q8_1", 32, 36),
    10: ("Q2_K", 256, 84), 11: ("Q3_K", 256, 110), 12: ("Q4_K", 256, 144),
    13: ("Q5_K", 2
… [829 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && /home/stephane/gpu-env/bin/python tools/analyse_octets_par_jeton.py $HOME/IA/modeles/qwen3-30b-a3b-Q4_K_M.gguf --experts-par-jeton 8 2>&1 | sed -n 1,12p", "description": "Exact expert bytes/token at 8 experts"}`

  ```
/home/stephane/IA/modeles/qwen3-30b-a3b-Q4_K_M.gguf : version 3, 579 tenseurs

48 couches à experts · 128 experts · 8 routés par jeton
  poids totaux du fichier      :    18.55 Go
  dont experts (toutes couches):    17.55 Go
  dont expert partagé          :     0.00 Go
  formats                      : Q4_K 14.26 Go · Q6_K 4.24 Go · F32 0.05 Go

  ⇒ OCTETS DE POIDS PAR JETON  :    1.097 Go
     à 6,5 Go/s sur le bus (PCIe x8, chiffre du dépôt) :    169 ms/jeton
     à 20 Go/s (lecture CPU mesurée)                   :     55 ms/jeton
     à 200 Mo/s (disque dur, lectures non cachées)     :    5.5 s/jeton
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,30p reports/rapport-placement-kv-8k.md; echo ===; sed -n 40,60p reports/rapport-placement-kv-8k.md", "description": "Read placement bands report"}`

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
… [1805 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"O_DIRECT\\|lire_en_tampons\\|fn pread\\|pread\" drave-core/src/gguf.rs | head -12; echo ---; grep -n \"evincer\\|fadvise\\|DONTNEED\" drave-core/src/gguf.rs drave-core/src/main.rs | head -8", "description": "Check direct IO … [31 caractères tronqués]`

  ```
60:/// | demande | plage entière | **par tranches de 1 Mio** | 8 fils en `pread` |
290:// ×3,5 — et un `pread` explicite depuis huit fils **3 995 Mo/s** (`tools/banc-experts.py`).
292:// page fait une lecture par page, `pread` lit des plages entières dans une mémoire à nous.
326:/// Un descripteur par fichier, ouvert une fois : `pread` sur un descripteur déjà ouvert ne
411:pub fn lire_en_tampons(plages: &[(usize, usize)], fils: usize) -> Vec<Option<Box<[u8]>>> {
482:            // FICHIER et l'OFFSET d'une adresse (lecture en tampons, `lire_en_tampons`).
---
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"tampons_voulus\\|DRAVE_TAMPONS\" drave-core/src/*.rs | head -8; echo ---; sed -n 1,25p drave-core/src/gguf.rs | head -25", "description": "Read buffer-mode gate"}`

  ```
drave-core/src/gguf.rs:342:/// `DRAVE_TAMPONS=1` : lire les experts retenus en séquentiel dans des tampons, et faire
drave-core/src/gguf.rs:344:pub fn tampons_voulus() -> bool {
drave-core/src/gguf.rs:345:    matches!(std::env::var("DRAVE_TAMPONS").as_deref(), Ok("1") | Ok("oui") | Ok("true"))
drave-core/src/gguf.rs:348:/// Nombre de fils de lecture des tampons (`DRAVE_TAMPONS_FILS`, défaut : `DRAVE_PRELIRE_FILS`).
drave-core/src/gguf.rs:350:    match std::env::var("DRAVE_TAMPONS_FILS") {
drave-core/src/model.rs:5053:            cache_ram: if crate::gguf::tampons_voulus() {
drave-core/src/model.rs:8432:                let tampons_on = crate::gguf::tampons_voulus();
---
//! Lecteur GGUF minimal (std seul).
//!
#![allow(dead_code)] // lecteur générique : tous les formats ne servent pas au moteur

//! Ne lit que ce dont le moteur a besoin : métadonnées, descripteurs de tenseurs,
//! et les niveaux quantifiés (Q8_0 / Q4_0) ou les flottants (F32 / F16).

use std::collections::HashMap;
use std::fs::File;
use std::io::{Read, Seek, SeekFrom};
use std::ops::Deref;
use std::path::Path;

/// Résultat empruntant à `self`. Écrit à la main parce qu'un tenseur peut vivre
/// dans n'importe lequel
… [506 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 8455,8510p drave-core/src/model.rs", "description": "Check VRAM expert cache call site gating"}`

  ```
if fils == 0 && !tampons_on {
                    for &e in &idx {
                        if let Some((k, loc)) = moe.ou(e) {
                            moe.gate[k].prelire_expert(loc);
                            moe.up[k].prelire_expert(loc);
                            moe.down[k].prelire_expert(loc);
                        }
                    }
                } else if crate::gguf::prelecture_active() {
                    let mut plages: Vec<(usize, usize)> = Vec::with_capacity(idx.len() * 3);
                    for &e in &idx {
                        if let Some((k, loc)) = moe.ou(e) {
                            plages.push(moe.gate[k].plage_expert(loc));
                            plages.push(moe.up[k].plage_expert(loc));
                            plages.push(moe.down[k].plage_expert(loc));
                        }
                    }
                    crate::gguf::prelecture_parallele(&plages, fils);
                }
                for (&e, &poids_exp) in idx.iter().zip(poids.iter()) {
                    let w_exp = poids_exp;
                    // Traduction pour les modèles en clusters : l'expert global
                    // `e` n'est pas forcément d
… [2291 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 8595,8612p drave-core/src/model.rs; echo ...; sed -n 8660,8682p drave-core/src/model.rs", "description": "Identify prof[3] sites in token path"}`

  ```
x = suite;
                    }
                    _ => for i in 0..h { x[i] = o[i] + down[i]; },
                }
                Self::vider_couche(self.dump_couches.as_deref(), "l_last", l, pos, &x);
                if debug_etat {
                    let n2: f32 = x.iter().map(|v| v * v).sum();
                    let na: f32 = att.iter().map(|v| v * v).sum();
                    let nd: f32 = down.iter().map(|v| v * v).sum();
                    eprintln!("[etat] couche {l:3} pos {pos} : |x| {:.4e} · |att| {:.4e} · \
|ffn| {:.4e}", n2.sqrt(), na.sqrt(), nd.sqrt());
                }
                self.prof[3] += tf.elapsed().as_secs_f64();
                continue;
            }
            Self::matvec(pool, g, &lay.wgate, &hn, &mut gate, events, &mut paires[2], self.act_levels, self.act_thresh, tk(4), self.act_renorm, &mut scratch, self.seuil_push);
            // --- capteur hebbien : espionne la co-activation (entrée, sortie)
            // de la projection gate. Aucun effet sur le calcul.
...
                    x = suite;
                }
                _ => for i in 0..h { x[i] = o[i] + down[i]; },
            }
            Self::vider_couche(self.dump_couches.as
… [1091 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"fn la_\\|fn le_\\|fn choisir_\\|fn un_\\|#\\[test\\]\" drave-core/src/placement.rs | head -20; echo ---; grep -n \"placement\\|expert\" tools/toutes-les-portes.sh | head -10", "description": "Count placement tests and find  … [15 caractères tronqués]`

  ```
136:pub fn choisir_avec_perte(
180:    #[test]
181:    fn la_vram_est_le_support_le_moins_cher_pour_un_gros_lecteur() {
190:    #[test]
191:    fn le_kv_tient_si_la_reserve_est_respectee() {
198:    #[test]
199:    fn choisir_respecte_la_place() {
208:    #[test]
209:    fn la_perte_decide_aussi() {
218:    #[test]
219:    fn un_budget_nul_interdit_toute_quantification() {
224:    #[test]
225:    fn la_tete_en_4_bits_est_refusee_par_un_budget_de_5_pour_cent() {
234:    #[test]
235:    fn la_regle_place_perte_choisit_le_kv_par_couche() {
247:    #[test]
248:    fn le_cout_est_proportionnel_aux_octets() {
---
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"porte-echange-experts\\|porte-flux\\|porte-pont\\|porte-coupe\" tools/toutes-les-portes.sh | head; echo ---; grep -c \"\" tools/toutes-les-portes.sh; grep -n \"^PORTES\\|^LISTE\\|registre\" tools/toutes-les-portes.sh | head … [45 caractères tronqués]`

  ```
25:# NOTE DE MESURE : les portes de latence et de gigue (`porte-delais`, `porte-flux`) mesurent
---
89
75:    printf '%s %s %s\n' "$nom" "$code" "$dt" >> "$JOURNAUX/registre.txt"
78:echo "--- $vertes vertes, $rouges rouges ---" | tee -a "$JOURNAUX/registre.txt"
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1,74p tools/toutes-les-portes.sh", "description": "Read gate runner"}`

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
… [2548 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && env DRAVE_GPU_TETE=1 ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --ppl $HOME/IA/scratch/prerequis/ids_0.5B_wt2_8192.txt --ctx 512 --limit 32 --threads 8 2>&1 | grep -E \"gpu|perplexité|postes|tête de sortie\" | he … [70 caractères tronqués]`

  ```
[gpu] GPU 1 · tête 151936 × 896 (Q8_0) sur le GPU : 145 Mo résidents, 16571 Mo libres
      31 tokens notés — perplexité cumulée 56.764  (28.2 tok/s)
=== perplexité 56.7642 sur 31 tokens (0 événements, 1.1 s) ===
    postes (ms/token) : projets-attn 3.00 | rope 0.64 | attention 4.09 | proj+mlp 28.14 | somme 35.88 | reste (tête + échantillonnage) 3.14
    dont tête de sortie 1.84 | notation log-sum-exp 1.26 (le reste du « reste » n'est pas chronométré)
  ```

- **bash** `{"command": "env | grep -i drave; echo \"---\"; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1545,1600p drave-core/src/gpu.rs", "description": "Check env vars and GPU gate code"}`

  ```
---
        }
    }
}

/// Instance unique du processus. `DRAVE_GPU` active le déport ; sans lui, aucune
/// ressource vidéo n'est touchée et le moteur reste strictement sur CPU.
static INSTANCE: std::sync::OnceLock<Option<Gpu>> = std::sync::OnceLock::new();

/// Le SECOND périphérique, s'il y en a un (deux Quadro sur cette machine). Il
/// sert au KV déporté : la moitié des couches d'un côté, la moitié de l'autre.
static SECOND: std::sync::OnceLock<Option<Gpu>> = std::sync::OnceLock::new();

pub fn second() -> Option<&'static Gpu> {
    SECOND.get_or_init(|| {
        if std::env::var("DRAVE_GPU").is_err() { return None; }
        let premier = instance().map(|g| g.ordinal).unwrap_or(0);
        for ord in 0..4 {
            if ord == premier { continue; }
            if let Some(g) = Gpu::ouvrir(ord) { return Some(g); }
        }
        None
    }).as_ref()
}

static MACHINES: std::sync::OnceLock<Vec<&'static Gpu>> = std::sync::OnceLock::new();

/// Les périphériques disponibles, dans l'ordre — un seul si la seconde carte est
/// absente ou occupée.
pub fn machines() -> &'static [&'static Gpu] {
    MACHINES.get_or_init(|| {
        let mut v: Vec<&'static Gpu> = Vec::new();
   
… [628 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && env DRAVE_GPU=0 DRAVE_GPU_TETE=1 ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --ppl $HOME/IA/scratch/prerequis/ids_0.5B_wt2_8192.txt --ctx 512 --limit 32 --threads 8 2>&1 | grep -E \"\\[gpu\\]|perplexité|postes|têt … [86 caractères tronqués]`

  ```
31 tokens notés — perplexité cumulée 56.764  (24.0 tok/s)
=== perplexité 56.7642 sur 31 tokens (0 événements, 1.3 s) ===
    postes (ms/token) : projets-attn 3.12 | rope 0.65 | attention 4.15 | proj+mlp 28.22 | somme 36.14 | reste (tête + échantillonnage) 8.98
    dont tête de sortie 7.75 | notation log-sum-exp 1.33 (le reste du « reste » n'est pas chronométré)
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"gpu::instance()\" drave-core/src/*.rs | head -20", "description": "List GPU instance call sites"}`

  ```
drave-core/src/main.rs:6515:    let Some(machine) = gpu::instance() else { println!("  GPU absent"); return };
drave-core/src/main.rs:6636:    let Some(machine) = gpu::instance() else {
drave-core/src/main.rs:6773:    let Some(machine) = gpu::instance() else { println!("  GPU absent"); return };
drave-core/src/main.rs:6832:    let Some(machine) = gpu::instance() else { println!("  GPU absent"); return };
drave-core/src/main.rs:6896:    let Some(machine) = gpu::instance() else { println!("  GPU absent"); return };
drave-core/src/model.rs:1967:        let gpu = match (&d, crate::gpu::instance()) {
drave-core/src/model.rs:4861:                          && crate::gpu::instance().is_some() {
drave-core/src/model.rs:4862:            let machine = crate::gpu::instance();
drave-core/src/model.rs:4957:                               && crate::gpu::instance().is_some()
drave-core/src/model.rs:5211:        if let (Some(machine), Some(mg)) = (crate::gpu::instance(), p.gpu.as_ref()) {
drave-core/src/model.rs:8488:                                (crate::gpu::instance(), self.cache_experts.as_mut()) {
drave-core/src/model.rs:8894:        let machine = crate::gpu::instance()?;
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 1935,1985p drave-core/src/model.rs", "description": "Check auto GPU placement for projections"}`

  ```
if keep >= 1.0 && !crate::gguf::push_tot_voulu() {
                (None, Some(dense8), None)
            } else {
                (Some(PushMat::build(&w, n_out, n_in)), Some(dense8), None)
            }
        } else {
            (Some(PushMat::build(&w, n_out, n_in)), None, None)
        };
        // La forme push est-elle paresseuse ? Alors on garde le NOM : c'est lui qui
        // permettra de la construire depuis le fichier au premier usage réel.
        // ATTENTION — `auto && !dense` est indispensable : en mode `--dense`, la forme push
        // n'était PAS chargée, donc `use_dense` valait toujours vrai. Rendre la forme
        // paresseuse « disponible » y ferait basculer les couches creuses sur le chemin push
        // — et le calcul change : la porte du flux l'a vu (58,8636 au lieu de 61,9920, et le
        // mode « listes par blocs » est passé rouge). Une paresse ne doit pas élargir ce que
        // le chargement avait décidé.
        let nom_push_ou = if auto && !dense && m.is_none() && q4v.is_none() && d.is_some()
                             && keep >= 1.0 && !crate::gguf::push_tot_voulu() {
            Some(name.to_string())
        } else { None };
       
… [1705 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 396,440p drave-core/src/materiel.rs; echo ---; grep -n \"SUCCES\" drave-core/src/materiel.rs", "description": "Read the second cost model in materiel.rs"}`

  ```
}

    /// Ce que coûtera un jeton, d'après les débits **mesurés** sur cette machine.
    ///
    /// Ce n'est pas une prédiction de performance : c'est la somme des trafics
    /// divisée par les débits, pour voir où passe le temps et ce qu'un
    /// déplacement changerait. Les débits viennent du banc (`--gpu-banc`) et des
    /// mesures de disque, pas d'une fiche technique.
    pub fn cout_par_jeton(&self, plan: &Plan, go_experts_par_jeton: f64,
                          go_tete: f64, go_commun: f64) -> String {
        const VRAM: f64 = 84.9;
        const RAM: f64 = 22.5;
        const NVME: f64 = 31.0;      // 16 lecteurs parallèles, mesuré
        // Taux de succès du cache d'experts : mesuré, 25 % de l'empreinte sert
        // 80 % des appels. On l'applique au trafic, pas à la place occupée.
        const SUCCES: f64 = 0.80;

        let vram_totale: f64 = self.gpus.iter().map(|g| g.vram_libre_go).sum();
        // Le commun et la tête sont RELUS à chaque jeton : ils restent en VRAM.
        let fixes = go_commun + go_tete;
        let cache = (vram_totale - fixes).max(0.0);
        // Ce qui manque au cache se lit sur le disque, en parallèle.
        let experts_disque 
… [1242 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 3620,3660p drave-core/src/main.rs; echo ---; grep -n \"\\.plan(\\|cout_par_jeton\\|plan\\.threads\\|plan\\.lecteurs\" drave-core/src/main.rs | head", "description": "Check whether materiel::plan drives decisions"}`

  ```
utilisera 9,95 Mo par expert, valeur de DeepSeek-V4.1");
            }
            let mo = if mo > 0.0 { mo } else { 9.95 };
            let _ = (ffn, embd);
            let total = g.octets_poids() as f64 / 1e9;
            let _ = couches;
            if n_exp > 0 {
                println!("Modèle : {} · {:.1} Go · {} experts de {:.2} Mo\n",
                         arch, total, n_exp, mo);
            } else {
                println!("Modèle : {} · {:.1} Go · dense (aucun expert)\n", arch, total);
            }
            (total, n_exp, mo, arch)
        }
        Err(_) => (0.0, 384, 9.95, String::from("DeepSeek-V4.1 (défaut)")),
    };
    let _ = arch;
    let plan = m.plan(ctx, taille_go, n_experts, mo_expert);
    println!();
    println!("Plan pour un contexte de {ctx} jetons, d'après les dimensions du modèle :");
    println!("  threads          : {}", plan.threads);
    if let Some(e) = &plan.epinglage {
        println!("  épinglage        : {} processeurs ({})", e.len(),
                 if e.len() > 8 { format!("{}..{}", e[0], e[e.len()-1]) } else {
                     e.iter().map(|c| c.to_string()).collect::<Vec<_>>().join(",") });
    }
    println!("  lecteur
… [1030 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Rédaction du rapport de reconnaissance A2.6

- **write** `{"file_path": "reports/rapport-a2.6-reconnaissance.md", "content": "# A2.6 — reconnaissance : les experts et la tête du moteur\n\n> **Ligne de roadmap** : A2.6 (ordonnanceur : experts et tête) · **Date** : 2026-11-18\n> · **HEAD** : `bb57604c` · **Binaire mesuré** : `drave-core/target/release/drave` … [21376 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-a2.6-reconnaissance.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

### 👤 Utilisateur

Agent d67a9bb1-090e-4f69-baf2-a831c00aa275 sent a message: 
Point de coordination : tu tournes depuis un moment. Donne-moi un point d'étape MAINTENANT en 5 lignes (ce que tu as trouvé, ce qui reste à lire), puis termine `reports/rapport-a2.6-reconnaissance.md` dans les 15 minutes — même partiel : (1) ce qui existe dans model.rs pour les experts (chemins + lignes), (2) ce qui manque pour clore A2.6, (3) la prochaine expérience exacte (commande + contrôle négatif + ce qui pourrait la rendre fausse). Ne lis pas tout model.rs : grep ciblé (`expert`, `rout`, `topk`, `sparse`, `E7`, `E8`) et les fiches reports/ suffisent. Ne touche à rien d'autre.

### 🤖 Assistant

⏵ Point d'étape au coordinateur puis vérification du rapport

- **send_message** `{"agent_id": "d67a9bb1-090e-4f69-baf2-a831c00aa275", "message": "Point d'étape A2.6 — le rapport est DÉJÀ ÉCRIT (reports/rapport-a2.6-reconnaissance.md, non committé), je vérifie les lignes citées.\n\n1. Existe : `placement.rs` (8 tests, pas 4) mais la règle n'est le chemin de décision QUE du KV ; e … [1186 caractères tronqués]`

  ```
message delivered to agent d67a9bb1-090e-4f69-baf2-a831c00aa275
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"const SEUIL_GPU\\|Source::Mxfp4 && moe.local\\|const RAM: f64\\|const VRAM: f64\\|const NVME: f64\\|const SUCCES\" drave-core/src/model.rs drave-core/src/materiel.rs; echo ---; grep -n \"pub fn instance\" drave-core/src/gpu … [125 caractères tronqués]`

  ```
drave-core/src/model.rs:1966:        const SEUIL_GPU: usize = 8 << 20;
drave-core/src/model.rs:8486:                    if moe.gate[0].src == crate::list::Source::Mxfp4 && moe.local.is_none() {
drave-core/src/materiel.rs:406:        const VRAM: f64 = 84.9;
drave-core/src/materiel.rs:407:        const RAM: f64 = 22.5;
drave-core/src/materiel.rs:408:        const NVME: f64 = 31.0;      // 16 lecteurs parallèles, mesuré
drave-core/src/materiel.rs:411:        const SUCCES: f64 = 0.80;
---
1582:pub fn instance() -> Option<&'static Gpu> {
---
8607:                self.prof[3] += tf.elapsed().as_secs_f64();
8676:            self.prof[3] += tf.elapsed().as_secs_f64();
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"trace_experts:\\|DRAVE_TRACE_EXPERTS\\|\\\"postes (ms/token)\" drave-core/src/model.rs drave-core/src/main.rs | head -8; echo ---; grep -n \"SEUIL_GPU\" drave-core/src/model.rs", "description": "Verify trace field and SEUIL … [12 caractères tronqués]`

  ```
drave-core/src/model.rs:432:/// **Le routage imposé — C9 sur un modèle routé.** `DRAVE_TRACE_EXPERTS` écrit depuis toujours
drave-core/src/model.rs:457:/// `DRAVE_TRACE_EXPERTS_ORDRE=1` : écrire les experts dans l'ORDRE DE SÉLECTION au lieu de les
drave-core/src/model.rs:461:    matches!(std::env::var("DRAVE_TRACE_EXPERTS_ORDRE").as_deref(), Ok("1") | Ok("oui"))
drave-core/src/model.rs:2896:    /// **Trace de routage** (`DRAVE_TRACE_EXPERTS=chemin`) : une ligne par
drave-core/src/model.rs:2900:    pub trace_experts: Option<std::io::BufWriter<std::fs::File>>,
drave-core/src/model.rs:5028:            trace_experts: std::env::var("DRAVE_TRACE_EXPERTS").ok().and_then(|c| {
drave-core/src/model.rs:8407:                    // `DRAVE_TRACE_EXPERTS_ORDRE=1`, la trace garde l'ordre de sélection et
drave-core/src/model.rs:10318:        // Le format est EXACTEMENT celui qu'écrit `DRAVE_TRACE_EXPERTS` : « couche cle e0 e1 … »,
---
1966:        const SEUIL_GPU: usize = 8 << 20;
1970:                   && n_out * d8.nb_ligne * 34 >= SEUIL_GPU => {
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n 'postes (ms/token)' drave-core/src/main.rs; grep -n 'let kv_gpu = if std::env::var(\"DRAVE_GPU_KV\")' drave-core/src/model.rs; grep -n 'let tete_gpu = if std::env::var(\"DRAVE_GPU_TETE\")' drave-core/src/model.rs; grep -n '_t … [216 caractères tronqués]`

  ```
2141:    println!("postes (ms/token) : matvec-attn {:.1} | rope {:.1} | attention {:.1} | matvec+mlp {:.1} | total mesuré {:.1}",
8651:    println!("    postes (ms/token) : projets-attn {:.2} | rope {:.2} | attention {:.2} | proj+mlp {:.2} | somme {:.2} | reste (tête + échantillonnage) {:.2}",
4882:        let kv_gpu = if std::env::var("DRAVE_GPU_KV").is_ok() {
4860:        let tete_gpu = if std::env::var("DRAVE_GPU_TETE").is_ok()
4988:        let _tete_tient = crate::placement::choisir(octets_tete, octets_tete, libre_vram, 64 << 30)
4956:        let cache_experts = if std::env::var("DRAVE_GPU_EXPERTS").is_ok()
5053:            cache_ram: if crate::gguf::tampons_voulus() {
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"8485\\|407-411\\|1588-1596\\|2897-2900\\|8596-8607\\|2140-2143\\|4881-4905\\|l. 406\" reports/rapport-a2.6-reconnaissance.md", "description": "Locate citations to correct in report"}`

  ```
50:| KV | `DRAVE_GPU_KV` (opt-in) + la règle | `model.rs:4881-4905` |
63:| `materiel.rs:407-411` | 84,9 | 22,5 (**jamais utilisée**) | **31,0** (16 lecteurs) | `SUCCES = 0,80` |
76:| trace de routage (`DRAVE_TRACE_EXPERTS`, `_ORDRE`) | 432-460, `trace_experts` 2897-2900 | fait |
83:| garde de format du cache VRAM | `model.rs:8485` `if moe.gate[0].src == Source::Mxfp4` | Q4_K/Q6_K **ne passent pas** : CPU |
85:| profilage par provenance (`proj+mlp`) | `model.rs:8596-8607` (MoE), `8607`+`8676` ; impression `main.rs:2140-2143` | fait |
108:**Drapeaux périmés** : `gpu::instance()` est passé en **AUTO** (`gpu.rs:1588-1596` : le GPU est
268:| `drave-core/src/materiel.rs` | `plan()` délègue à la règle (au lieu de `vram − 2,0 − 8,0`) ; `cout_par_jeton` prend les bandes de `placement.rs` (aujourd'hui 3 tables) | **+20 à 30 lignes** | `plan()` n'est qu'un **imprimé** (`main.rs:3637`) : le risque est de **déplacer les chiffres affichés** que des fiches citent ; `cout_par_jeton` a `RAM` **mort** (l. 406) |
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport io\np = \"reports/rapport-a2.6-reconnaissance.md\"\ns = io.open(p, encoding=\"utf-8\").read()\nsubs = [\n (\"`model.rs:4881-4905`\", \"`model.rs:4882-4905`\"),\n (\"`materiel.rs:407-411`\", \"`materiel.rs:406 … [737 caractères tronqués]`

  ```
ok x1: `model.rs:4881-4905`
ok x1: `materiel.rs:407-411`
ok x1: `trace_experts` 2897-2900
ok x1: `model.rs:8485` `if moe.gate[0].src
ok x1: `model.rs:8596-8607` (MoE), `8607`+`8676` ; impres
ok x1: `gpu.rs:1588-1596`
ok x1: (l. 406)
ok x1: garde `Source::Mxfp4`
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --short; echo ---; wc -l reports/rapport-a2.6-reconnaissance.md; echo ---; grep -n \"8486\\|4882-4905\\|406-411\\|1582-1591\\|2896-2900\\|2141\\|l. 407\" reports/rapport-a2.6-reconnaissance.md | head", "description": "Veri … [30 caractères tronqués]`

  ```
M journal/README.md
 M journal/sessions/8c024745-95cb-4885-9d0b-865142606b6d/digest.md
 M journal/sessions/8c024745-95cb-4885-9d0b-865142606b6d/rapport.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/c7e46dba-11cb-456b-a3b6-715428927f99/digest.md
 M journal/sessions/c7e46dba-11cb-456b-a3b6-715428927f99/rapport.md
 M journal/sessions/d67a9bb1-090e-4f69-baf2-a831c00aa275/digest.md
 M journal/sessions/d67a9bb1-090e-4f69-baf2-a831c00aa275/rapport.md
?? bench/checkpoint_bench.sh
?? journal/sessions/174fd5ef-1163-4983-85b5-9101752ad711/
?? journal/sessions/da0f2984-32d0-459d-a761-d3faf6a10b8a/
?? reports/banc-grammaticalite-100m.json
?? reports/rapport-a2.6-reconnaissance.md
---
301 reports/rapport-a2.6-reconnaissance.md
---
50:| KV | `DRAVE_GPU_KV` (opt-in) + la règle | `model.rs:4882-4905` |
63:| `materiel.rs:406-411` | 84,9 | 22,5 (**jamais utilisée**) | **31,0** (16 lecteurs) | `SUCCES = 0,80` |
76:| trace de routage (`DRAVE_TRACE_EXPERTS`, `_ORDRE`) | 432-460, `trace_experts` 2896-2900 | fait |
83:| garde de format du cache VRAM | `model.rs:8486` `if moe.gate[0].src == Source::Mxfp4` | Q4_K/Q6_K **ne passent pas** : CPU |
85:| profilage par provenance (`proj+mlp`) | `model.rs
… [653 caractères tronqués]
  ```

- **read** `{"file_path": "reports/rapport-a2.6-reconnaissance.md", "offset": 118, "limit": 100}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-a2.6-reconnaissance.md</path>
<type>file</type>
<content>
118: 2. **Le refus nommé.** `choisir` **ne peut pas refuser** : il retombe sur `Support::Nvme` (l. 96-102),
119:    et le test `choisir_respecte_la_place` (l. 199-206) **exige** ce repli. Le contrat de la fiche
120:    (« un opérateur qui ne tient nulle part : refus nommé, pas de placement silencieux ») n'est donc
121:    pas tenu — seul le KV a un refus imprimé, codé à la main dans `model.rs:4889`.
122: 3. **La bande de l'opérateur experts.** Mesurée **5,6 Go/s** (§ 3) ; aucune constante ne la porte.
123:    Sans elle, la règle place au hasard entre 35 ms et 313 ms : **la mesure du § 3 est le préalable**.
124: 4. **La réutilisation dans le coût.** 47 % de réutilisation immédiate, 87 % à LRU 32/128 : `cout()`
125:    lit tout, chaque jeton. `materiel::cout_par_jeton` a un `SUCCES = 0,80` en dur mais **n'est pas
126:    branché**. Il faut un seul modèle de coût, réutilisation comprise.
127: 5. **La trace.** `classement`/`cout` ne sont **imprimés nulle part** ; la porte 3 de la fiche
128:    (« trace : le classement et le coût retenu sont imprimés et testés 
… [5310 caractères tronqués]
  ```

- **read** `{"file_path": "reports/rapport-a2.6-reconnaissance.md", "limit": 90, "offset": 218}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-a2.6-reconnaissance.md</path>
<type>file</type>
<content>
218:   (`posix_fadvise(DONTNEED)`, `tools/mesure_lot_disque.sh`) ;
219: - **`--limit 8` est court** (7 jetons) : le premier jeton paie la lecture froide ; `--limit 32`
220:   dilue cet effet, c'est pourquoi le protocole le demande ;
221: - **`proj+mlp` n'est pas que les experts** : il inclut le routeur et les normes (quelques %) ;
222: - **le noyau Q4_K du GPU n'est pas câblé** : aucune mesure de VRAM n'est possible sur ce modèle
223:   aujourd'hui (§ 2.7, garde `Source::Mxfp4` (`model.rs:8486`)), donc « le cache VRAM ne paie pas » **n'est pas
224:   démontré ici** — seul le plafond K3 (×1,09) l'est, et il ne se transpose pas (K3 a 55 % de dense
225:   dans son trafic, le 30B a 95 % d'experts).
226: 
227: ### 3.3 La décision que cette mesure tranche
228: 
229: | si… | alors l'implémentation A2.6 est… | diff |
230: |---|---|---|
231: | `proj+mlp` sature à 8 fils (≈ 195 ms) | **la bande `experts` entre dans `placement.rs`** (5,6 Go/s), avec `lecteurs` et refus nommé ; le levier est le regroupement (÷15,5 au lot 192), pas le support | ~120 lignes |
232: | `pr
… [5906 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport io\np = \"reports/rapport-a2.6-reconnaissance.md\"\ns = io.open(p, encoding=\"utf-8\").read()\nsubs = [\n ('2>&1 | grep -E \"postes|perplexit|tete de sortie\"',\n  '2>&1 | grep -E \"postes|perplexit\"'),\n (\ … [895 caractères tronqués]`

  ```
ok x1: 2>&1 | grep -E "postes|perplexit|tete de sortie"
ok x1: La conclusion attendue : **la bande de l'opérateur expe
ok x1: aujourd'hui (§ 2.7, garde `Source::Mxfp4` (`model.rs:84
ok x1: — c'est la porte 1 et 2 de la fiche ;
  ```

- **read** `{"file_path": "reports/rapport-a2.6-reconnaissance.md", "limit": 80, "offset": 38}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-a2.6-reconnaissance.md</path>
<type>file</type>
<content>
38: | site | ce qu'il décide |
39: |---|---|
40: | `model.rs:4720` `kv_precision` | la précision du KV couche par couche, **sous `DRAVE_PERTE_MAX`** (opt-in, A8.3) |
41: | `model.rs:4889` `kv_en_vram` | le miroir VRAM du KV, **sous `DRAVE_GPU_KV`** ; seul endroit du dépôt qui imprime un **refus nommé** (« KV déporté REFUSÉ par la règle de placement ») |
42: | `model.rs:4988` `choisir` | la tête : le choix est **calculé puis jeté** (`let _tete_tient = …`) — le commentaire dit pourquoi (place ≠ qualité) |
43: | **—** | **aucun appel pour les experts** |
44: 
45: ### 1.2 Le placement réel : drapeaux et seuils, pas la règle
46: 
47: | opérateur | ce qui décide **aujourd'hui** | lieu |
48: |---|---|---|
49: | projections | seuil **codé en dur** `SEUIL_GPU = 8 Mio`, Q8_0 seulement, **GPU en auto** | `model.rs:1959-1977` |
50: | KV | `DRAVE_GPU_KV` (opt-in) + la règle | `model.rs:4882-4905` |
51: | tête | `DRAVE_GPU_TETE` (opt-in) ; 4 bits = `--q4-tout` (bit 4 de `q4`), pas de drapeau isolé | `model.rs:4859-4885`, `main.rs:1696-1699` |
52: | cache VRAM des expert
… [5964 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n 24,50p drave-core/src/model.rs; echo ---; grep -n \"Qwen2.5-0.5B Q\" reports/rapport-regle-placement-perte.md reports/rapport-placement-kv-8k.md", "description": "Check Gating variants and 4-bit head model"}`

  ```
// --------------------------------------------------------------------------- //

/// Convention de routage des experts — quatre familles, et une seule
/// implémentation partagée par le jeton seul et le lot (voir [`router`]).
#[derive(Clone, Copy, PartialEq, Eq, Debug)]
pub enum Gating {
    /// `softmax` sur TOUS les logits, top-k, renormalisation. Qwen3-MoE, et le
    /// défaut de llama.cpp quand un modèle ne déclare rien.
    Softmax,
    /// `sigmoid` sur chaque logit, top-k sur ces scores, renormalisation.
    /// Kimi-K2.7 (`expert_gating_func = 2`), GLM-5.3 et GLM-5.3-Flash.
    Sigmoid,
    /// Top-k sur les logits **bruts** (plus le biais de sélection s'il existe),
    /// puis `softmax` sur les seuls k retenus — et **pas** de renormalisation
    /// ensuite, le softmax s'en charge. gpt-oss.
    SoftmaxPoids,
    /// `sqrt(softplus(x)) = sqrt(log(1+e^x))` sur chaque logit, top-k,
    /// renormalisation. DeepSeek V4-Flash (`expert_gating_func = 4`) et V4.1.
    SqrtSoftplus,
}

impl Gating {
    /// Numéro `expert_gating_func` du GGUF, tel que llama.cpp le définit.
    pub fn du_numero(n: u64) -> Option<Gating> {
        match n {
            1 => Some(Gating::Softmax),
… [336 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\nimport io\np = \"reports/rapport-a2.6-reconnaissance.md\"\ns = io.open(p, encoding=\"utf-8\").read()\nsubs = [\n (\"| fait, 5 familles |\", \"| fait, **quatre familles** (softmax, sigmoïde, top-k brut puis softmax,  … [665 caractères tronqués]`

  ```
ok x1: | fait, 5 familles |
ok x1: **+10 %** de PPL (30,7660 → 33,8230, 0,5 B Q4_0, 2
ok x1: 4 bits = `--q4-tout` (bit 4 de `q4`), pas de drape
51:| tête | `DRAVE_GPU_TETE` (opt-in) ; 4 bits = `--q4-tout` (seul à poser le bit `4` de `q4`), pas de drapeau isolé | `model.rs:4859-4885`, `main.rs:1696-1699` |
73:| convention de routage lue du GGUF (softmax, sigmoïde, racine de softplus, gpt-oss) | `model.rs:26-46`, `Routage` 306-311, `routage_du_gguf` 320-369 | fait, **quatre familles** (softmax, sigmoïde, top-k brut puis softmax, racine de softplus) |
104:| tête 4 bits | **+10 %** de PPL (30,7660 → 33,8230, 0,5 B, 255 jetons) — **historique, non rejouable isolément** : `--q4-tout` quantifie aussi attention et FFN (+40,8 % mesuré ici) | `rapport-placement-kv-8k.md` ; ce rapport |
  ```

- **send_message** `{"agent_id": "d67a9bb1-090e-4f69-baf2-a831c00aa275", "message": "A2.6 — reconnaissance terminée. Rapport : `reports/rapport-a2.6-reconnaissance.md` (302 lignes, NON committé ; `en-cours`, `roadmap`, `AGENTS` et le code non touchés).\n\n1. **Existe** : `placement.rs` (8 tests, pas 4) mais la règle n' … [1869 caractères tronqués]`

  ```
message delivered to agent d67a9bb1-090e-4f69-baf2-a831c00aa275
  ```

### 🤖 Assistant

⏵ Reconnaissance A2.6 terminée, rapport écrit

**Résumé (A2.6 — experts et tête)**

1. **Existe** : `placement.rs` (253 l., **8 tests**) mais la règle ne décide **que du KV** ; experts et tête sont placés par drapeaux/seuils durs (`SEUIL_GPU` 8 Mio, `DRAVE_GPU_EXPERTS_GO` = VRAM−2 Go, `DRAVE_EXPERTS_RAM`, `materiel::plan` imprimé, jamais appliqué).
2. Le chemin experts est déjà riche : 4 conventions de routage (`model.rs:26-46`), trace/imposition/élagage (`432-480`), `Moe` (`1504-1553`), caches RAM (`1583-1700`) et VRAM MXFP4 seulement (`1983-2100`, garde `8486`), prélecture 8 fils, noyau GPU Q4_K mesuré mais **non branché**.
3. **Manque** : coût « experts » (réutilisation + nb de lecteurs), **refus nommé** (`choisir` retombe sur NVMe en silence), trace du classement et test de reproductibilité, `Precision` tête à perte 0, et **une bande experts** — trois tables contradictoires (3,5 vs 31 Go/s) donnent 313 ou 35 ms pour le même opérateur.
4. **Mesuré ici** : 1,097 Go d'experts/jeton ; `proj+mlp` 194,8 ms à 8 fils (**5,6 Go/s**), 188,8 à 16 (saturation), 279,1 à 4 ; cache RAM 567,9 ms et tampons 362,8 ms (plus lents) ; PPL 799,8557 invariante.
5. **Bonus** : tête Q8_0 en VRAM → PPL **56,7642 = 56,7642**, tête **7,43 → 1,80 ms/jeton** (÷4,1), contrôle `DRAVE_GPU=0` = 7,75 ms.
6. **Prochaine expérience** : bande experts au `--limit 32` sur 4/8/16 fils, contrôles « cache RAM et tampons plus lents » + « PPL 37,2013 invariante » ; attendu 195 ms à 8 fils = **un lecteur**, pas 31 Go/s.
7. **Risque** : ≈ 200 lignes (3 fichiers) ; le risque est le chemin de chargement et le défaut → opt-in `DRAVE_PERTE_MAX`, portes `flux`/`pont`/`coupe`, `porte-echange-experts`, `cargo test placement`.

**Rapport** : `reports/rapport-a2.6-reconnaissance.md` — non committé, aucun autre fichier modifié.

