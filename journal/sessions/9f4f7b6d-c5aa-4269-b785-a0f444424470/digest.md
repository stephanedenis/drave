# Session DSH — relecture

- identifiant : `9f4f7b6d-c5aa-4269-b785-a0f444424470`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-11-18 10:17:36
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet (Drave, en français). Machine dédiée. La reconnaissance `reports/rapport-a2.6-reconnaissance.md` a montré que `drave-core/src/placement.rs` n'a **aucune entrée `Precision` pour la tête** en Q8_0/Q6_K (la table a f32, int8 tardif, int4 tardif, « tête 4 bits +10 % », int4 global +364 %), alors qu'une mesure de la reconnaissance donne la tête Q8_0 en VRAM à PPL **identique** (56,7642 = 56,7642) et **7,43 → 1,80 ms/jeton** (÷4,1).

TÂCHE (petite, sûre, testée) : ajouter à `placement.rs` **une entrée de précision** pour la tête en Q8_0 et Q6_K, à perte **0**, sans toucher au chemin de chargement du modèle ni au comportement par défaut.

Exigences :
1. Lis `placement.rs` en entier (253 lignes) et `cargo test placement` (8 tests) avant de toucher quoi que ce soit.
2. Ajoute les variantes `Precision` (par exemple `TeteQ8_0`, `TeteQ6_K`) avec `perte: 0.0` et le bon `bits`/`octets_par_poids` si la structure le permet — **sans casser** les variantes existantes ni les 8 tests.
3. Ajoute **un** test unitaire qui prouve que `choisir_avec_perte` (ou `classement`) place la tête Q8_0 exactement comme la f32 à perte 0, et qu'une perte < 0.0 la refuse — le test doit échouer si on retire l'entrée (vérifie-le en le faisant temporairement, puis remets-la).
4. Ne branche RIEN dans `model.rs` : la mesure Q8_0 est déjà faite, le câblage est une autre tâche.
5. Écris `reports/rapport-a2.6-tete-q8.md` : le diff (fichier, lignes), le test, la justification (la mesure de la reconnaissance), ce qui pourrait le rendre faux (la mesure a été prise machine chargée, à rejouer).
6. Lance `cargo test placement` et `cargo test` (tout) et donne le compte.

CONTRAINTES : n'écris que `drave-core/src/placement.rs` et `reports/rapport-a2.6-tete-q8.md` ; ne touche pas à en-cours/roadmap/AGENTS, ni à `model.rs`, ni au binaire ; ne committe pas.

Rends : le diff (résumé), le compte des tests, et le chemin du rapport.
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

⏵ Lecture de placement.rs et de la reconnaissance avant modification

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/placement.rs"}`

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

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls && git status --short | head -20", "description": "Vue du dépôt et état git"}`

  ```
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
 M journal/sessions/MANIFEST.md
 M journal/sessions/d67a9bb1-090e-4f69-baf2-a831c00aa275/digest.md
  ```

### 🤖 Assistant

⏵ Lecture de la reconnaissance A2.6 et lancement des tests de base

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cargo test placement 2>&1 | tail -25", "description": "Lancer cargo test placement (état de base)", "timeoutMs": 300000}`

  ```
error: could not find `Cargo.toml` in `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` or any parent directory
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls reports/ | head -30 && echo '---' && wc -l reports/rapport-a2.6-reconnaissance.md", "description": "Lister reports et taille du rapport de reconnaissance"}`

  ```
07
07-mesures-couche-commune.md
a2.6-bande-experts.json
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
---
302 reports/rapport-a2.6-reconnaissance.md
[stderr]
ls: write error: Broken pipe
  ```

### 🤖 Assistant

⏵ Localisation du manifeste cargo et lecture du rapport de reconnaissance

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls drave-core/ && echo '---' && head -5 drave-core/Cargo.toml 2>/dev/null; find . -maxdepth 3 -name Cargo.toml -not -path '*/target/*' 2>/dev/null", "description": "Trouver le Cargo.toml du crate"}`

  ```
Cargo.lock
Cargo.toml
gpu
README.md
src
target
tests
---
[package]
name = "drave-core"
version = "0.1.0"
edition = "2021"
description = "Drave — moteur d'exécution par listes d'activation (stream of logs) pour modèles quantifiés"
./drave-core/Cargo.toml
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-a2.6-reconnaissance.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-a2.6-reconnaissance.md</path>
<type>file</type>
<content>
1: # A2.6 — reconnaissance : les experts et la tête du moteur
2: 
3: > **Ligne de roadmap** : A2.6 (ordonnanceur : experts et tête) · **Date** : 2026-11-18
4: > · **HEAD** : `bb57604c` · **Binaire mesuré** : `drave-core/target/release/drave`, 2026-11-17 14 h 21
5: > · **Nature** : **reconnaissance en lecture seule** — aucun fichier du moteur modifié, aucun commit.
6: > **Machine** : 2 × Quadro RTX 5000 (16 384 Mio), 125 Go de RAM, 40 fils ; **charge 13,7 → 31,4**
7: > pendant les mesures (d'autres sessions lisaient un modèle lourd) → les **temps absolus** sont
8: > bruités, les **écarts** de ×2 à ×5 ne le sont pas. Toute reprise doit se faire **machine au repos**.
9: >
10: > **Verdict** : A2.6 n'est **pas** bloquée par A6.2, et sa fiche est en retard de deux mesures.
11: > La règle existe (`placement.rs`, **8** tests, pas 4) mais elle n'est **le chemin de décision
12: > d'aucun opérateur sauf le KV** ; les experts et la tête sont placés par des **drapeaux et des
13: > seuils codés en dur**. Le chiffre qui manque n'est pas le débit des experts — il est mesu
… [21727 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Exécution des tests de base (placement puis crate complet) dans drave-core

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core && cargo test placement 2>&1 | tail -25", "description": "cargo test placement état de base", "timeoutMs": 600000}`

  ```
warning: the `ids:` in this pattern is redundant
    --> src/main.rs:1766:9
     |
1766 |         ids: mut ids, ids_file, prompt, n: n_new, temp, top_p, topk, rep_pen, hist,
     |         ^^^^^^^^^^^^ help: use shorthand field pattern: `mut ids`
     |
     = note: `#[warn(non_shorthand_field_patterns)]` on by default

warning: `drave-core` (bin "drave" test) generated 66 warnings (run `cargo fix --bin "drave" -p drave-core --tests` to apply 37 suggestions)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.01s
     Running unittests src/main.rs (target/debug/deps/drave-0fde18393e99a236)

running 8 tests
test placement::tests::la_regle_place_perte_choisit_le_kv_par_couche ... ok
test placement::tests::choisir_respecte_la_place ... ok
test placement::tests::la_perte_decide_aussi ... ok
test placement::tests::la_tete_en_4_bits_est_refusee_par_un_budget_de_5_pour_cent ... ok
test placement::tests::la_vram_est_le_support_le_moins_cher_pour_un_gros_lecteur ... ok
test placement::tests::le_cout_est_proportionnel_aux_octets ... ok
test placement::tests::le_kv_tient_si_la_reserve_est_respectee ... ok
test placement::tests::un_budget_nul_interdit_toute_quantification ... 
… [99 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"TETE_4BIT\\|PRECISIONS\\|choisir_avec_perte\" --include=*.rs . | grep -v target/", "description": "Chercher les usages de PRECISIONS et choisir_avec_perte"}`

  ```
./drave-core/src/placement.rs:122:pub const TETE_4BIT: Precision = Precision { nom: "tête 4 bits", octets_par_valeur: 0.5, perte_ppl: 10.0 };
./drave-core/src/placement.rs:127:pub const PRECISIONS: [Precision; 5] = [F32, INT8_TARDIF, INT4_TARDIF, TETE_4BIT, INT4_GLOBAL];
./drave-core/src/placement.rs:136:pub fn choisir_avec_perte(
./drave-core/src/placement.rs:144:    for p in PRECISIONS {
./drave-core/src/placement.rs:211:        let (_, p8) = choisir_avec_perte(100 << 20, 100 << 20, 4 << 30, 64 << 30, 1.0).unwrap();
./drave-core/src/placement.rs:213:        let (_, p4) = choisir_avec_perte(100 << 20, 100 << 20, 4 << 30, 64 << 30, 5.0).unwrap();
./drave-core/src/placement.rs:220:        let (_, p0) = choisir_avec_perte(100 << 20, 100 << 20, 4 << 30, 64 << 30, 0.0).unwrap();
./drave-core/src/placement.rs:227:        let choisi = choisir_avec_perte(100 << 20, 100 << 20, 4 << 30, 64 << 30, 5.0).unwrap();
./drave-core/src/placement.rs:230:        let encore = choisir_avec_perte(100 << 20, 100 << 20, 4 << 30, 64 << 30, 10.0).unwrap();
  ```

### 🤖 Assistant

⏵ Tests placement 8/8 confirmés ; lancement du `cargo test` de référence et inspection des types ggml

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core && cargo test 2>&1 | tail -40", "description": "cargo test complet de référence", "timeoutMs": 900000, "run_in_background": true}`

  ```
started background job bash-573
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core && grep -n \"Q8_0\\|Q6_K\\|Q6K\\|enum Source\" src/model.rs src/gguf.rs | head -40", "description": "Repérer les codes/types Q8_0 et Q6_K"}`

  ```
src/model.rs:11://! produits scalaires sur les lignes Q8_0 d'origine. En mode push il faudrait un
src/model.rs:770:    /// Copie GPU des poids (sources Q8_0), si le déport est actif.
src/model.rs:802:                      GGML_MXFP4, GGML_Q4_0, GGML_Q4_K, GGML_Q6_K};
src/model.rs:806:        GGML_Q6_K => Some(Source::Q6_K),
src/model.rs:887:            let bloc = if t.ttype == crate::gguf::GGML_Q4_K || t.ttype == crate::gguf::GGML_Q6_K { 256 } else { 32 };
src/model.rs:915:        let bloc = if t.ttype == crate::gguf::GGML_Q4_K || t.ttype == crate::gguf::GGML_Q6_K { 256 } else { 32 };
src/model.rs:1339:    /// formats sauf Q4_K/Q6_K, alors que `pas()` d'une grille (`Dequant`) est la
src/model.rs:1349:            // Super-blocs de 256 poids : `DenseQ4` pour Q4_K/Q6_K, et
src/model.rs:1351:            Q4_K | Q6_K | Dequant(_) => self.n_out * (self.n_in / 256) * self.pas(),
src/model.rs:1361:            Q6_K => crate::gguf::TAILLE_Q6K,
src/model.rs:1490:                crate::list::Source::Q6_K =>
src/model.rs:1765:/// Les autres formats 4 bits (Q4_K, Q6_K, MXFP4) ne sont PAS comptés ici : ils demandent chacun
src/model.rs:1828:/// la disposition de Q8_0) ou une par ligne (défaut hist
… [2466 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification des constantes ggml et du site tête dans model.rs (lecture seule)

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/gguf.rs", "offset": 575, "limit": 70}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/gguf.rs</path>
<type>file</type>
<content>
575: pub const GGML_Q4_0: u32 = 2;
576: pub const GGML_MXFP4: u32 = 39;
577: pub const GGML_Q2_K: u32 = 10;
578: pub const GGML_BF16: u32 = 30;
579: pub const GGML_Q3_K: u32 = 11;
580: pub const GGML_Q4_K: u32 = 12;
581: /// Bloc **Q5_0** (22 octets, 32 poids) et **Q5_1** (24 octets, 32 poids) :
582: /// échelle f16 (+ minimum f16 pour Q5_1), 4 octets de bits hauts, 16 octets de
583: /// quants 4 bits. Q5_0 est le type de `token_embd` et des `ffn_gate/up` de
584: /// Qwen2.5-0.5B en Q4_K_M — 62 % des poids de ce fichier : sans lui, le modèle
585: /// ne se charge pas du tout.
586: pub const GGML_Q5_0: u32 = 6;
587: pub const GGML_Q5_1: u32 = 7;
588: pub const GGML_Q5_K: u32 = 13;
589: pub const GGML_Q6_K: u32 = 14;
590: /// Types des experts de DeepSeek : IQ2_XXS (V4.1), IQ1_M (V4-Flash).
591: /// Sans ces constantes, `--bloc` les appelait « type 16 » et le lecteur les
592: /// refusait — un numéro en clair ne dit pas de quel encodage il s'agit.
593: pub const GGML_IQ2_XXS: u32 = 16;
594: /// IQ3_XXS : 98 octets par super-bloc de 256 poids (30 % des poids de Kimi,
595: //
… [2427 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core && sed -n '4840,4900p;4960,5000p' src/model.rs", "description": "Lire le site tête de model.rs en lecture seule"}`

  ```
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
        // Opt-in : `DRAVE_GPU_TETE=1`.
        // Têtes liées de la famille Qwen en Q4_K_M : elles sont en **Q6_K**, pas
        // en Q8_0 — sans cette reconnaissance, `DRAVE_GPU_TE
… [5387 caractères tronqués]
  ```

### 👤 Utilisateur

background job bash-573 (bash: cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core && cargo test 2>&1 | tail -40) finished [status: completed, exit code: 0]. Read its output with job_output.

### 🤖 Assistant

⏵ Lecture du résultat `cargo test` de référence

- **job_output** `{"job_id": "bash-573"}`

  ```
test topologie::tests::refuse_une_cle_inconnue ... ok
test trace_globale::tests::derive_horloges_mesure_l_ecart_sans_le_corriger ... ok
test trace_globale::tests::aller_retour_v2_conserve_source_mode_et_horodatage ... ok
test trace_globale::tests::empreinte_change_avec_un_bit ... ok
test episodique::tests::ecrire_une_fois_puis_relire_cent_fois ... ok
test tokenizer::tests_kimi::les_lettres_se_coupent_par_casse_en_excluant_les_han ... ok
test trace_globale::tests::allez_retour_ecriture_lecture ... ok
test trace_globale::tests::fusion_ordonne_par_le_temps_mural ... ok
test trace_globale::tests::fusion_est_deterministe_a_horodatage_egal ... ok
test trace_globale::tests::fusion_refuse_une_seule_source_et_une_trace_vide ... ok
test trace_globale::tests::fusion_refuse_une_trace_sans_horodatage ... ok
test tests_plafond::un_lot_dement_grand_est_refuse_avant_allocation ... ok
test trace_globale::tests::la_v1_reste_lisible_et_perd_seulement_son_horodatage ... ok
test trace_globale::tests::lien_non_verifiable_en_encodage_avec_perte ... ok
test trace_globale::tests::liens_divergents_detectes_en_mode_dense ... ok
test tests_plafond::mode4_prefixe_incoherent_est_refuse ... ok
test topologie::te
… [1528 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification des politiques d'avertissements et de la constante GGML_F32

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core && grep -n \"deny\\|allow(dead_code)\\|GGML_F32\\b\\|GGML_F16\\b\" src/main.rs src/gguf.rs src/placement.rs | head -20 && echo '--- mod placement ---' && grep -n \"mod placement\" src/main.rs", "description": "Vérifier deny/a … [28 caractères tronqués]`

  ```
src/gguf.rs:3:#![allow(dead_code)] // lecteur générique : tous les formats ne servent pas au moteur
src/gguf.rs:573:pub const GGML_F32: u32 = 0;
src/gguf.rs:574:pub const GGML_F16: u32 = 1;
src/gguf.rs:1754:            GGML_F32 => {
src/gguf.rs:1760:            GGML_F16 => {
src/gguf.rs:2104:            GGML_F32 => {
src/gguf.rs:2109:            GGML_F16 => {
src/gguf.rs:2355:            b.extend_from_slice(&GGML_F32.to_le_bytes());
src/gguf.rs:2624:        for (ttype, attendu) in [(GGML_F32, 4 * 1024u64), (GGML_Q8_0, 34 * 32),
--- mod placement ---
83:mod placement;
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -3 && git status --porcelain drave-core/ | head", "description": "Vérifier HEAD et propreté du crate"}`

  ```
8bec3cc8 ÉTAT — LA PUCE N4 SOUS 80 MOTS (LE DÉTAIL EST DANS LES QUATRE FICHES)
b3354bd8 N4 — LE DÉCODAGE : TOP-40 À T=0,5 BAT LE GREEDY SUR TOUS LES AXES (VALIDES 0,907 · RÉPÉTITION 1,7 CONTRE 5,7 · ÉCHO 0,075 CONTRE 0,149)
d37e46e7 N4 — LE 73 M À 13 000 PAS : L'ÉCHANTILLONNAGE DÉCOLLE (TOP-40 0,551 → 0,831), LE GREEDY SE DÉGRADE (RÉP 6 → 11, ÉCHO 0,149)
  ```

### 🤖 Assistant

⏵ Ajout des entrées tête Q8_0/Q6_K et du test dans placement.rs

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/placement.rs", "old_string": "    meilleur.map(|(s, p, _)| (s, p))\n}\n\n/// La perte **mesurée** de l'int8 sur le KV selon la couche (A5.3, 0,5 B, 255 jetons) :", "new_string": "    meilleur.map(|(s, p, _)| (s, p))\n}\n\n … [3232 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/placement.rs has been updated successfully.
  ```

### 🤖 Assistant

⏵ Ajout du test unitaire de placement de la tête

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/placement.rs", "new_string": "    #[test]\n    fn la_tete_q8_0_se_place_comme_le_f32_a_perte_nulle() {\n        // La mesure de la reconnaissance (18/11, § 3.4) : tête Q8_0 en VRAM, même\n        // PPL qu'en RAM (56,7642  … [2248 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/placement.rs has been updated successfully.
  ```

### 🤖 Assistant

⏵ Compilation et exécution des 9 tests placement

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core && cargo test placement 2>&1 | grep -E \"warning: (function|constant|unused)|placement|test result|error\" | tail -30", "description": "cargo test placement après ajout", "timeoutMs": 600000}`

  ```
warning: unused variable: `arch`
warning: unused variable: `arch`
warning: unused variable: `q_lora`
warning: unused variable: `tk5`
warning: unused variable: `attn_all`
warning: unused variable: `attn_idx`
warning: unused variable: `mg`
warning: unused variable: `mu`
warning: unused variable: `md`
warning: unused variable: `bg`
warning: unused variable: `base_rot`
warning: unused variable: `jeton`
warning: unused variable: `charge`
warning: unused variable: `ua`
warning: function `expert_mxfp4_dans` is never used
warning: constant `RAM` is never used
warning: function `nnz_q4_0` is never used
warning: function `sample` is never used
  --> src/placement.rs:52:12
warning: function `existe` is never used
test placement::tests::la_regle_place_perte_choisit_le_kv_par_couche ... ok
test placement::tests::la_perte_decide_aussi ... ok
test placement::tests::choisir_respecte_la_place ... ok
test placement::tests::la_tete_q8_0_se_place_comme_le_f32_a_perte_nulle ... ok
test placement::tests::la_tete_en_4_bits_est_refusee_par_un_budget_de_5_pour_cent ... ok
test placement::tests::le_cout_est_proportionnel_aux_octets ... ok
test placement::tests::le_kv_tient_si_la_reserve_est_respectee ... ok
… [258 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Contrôle des avertissements introduits dans placement.rs

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core && touch src/placement.rs && cargo build 2>&1 | grep -B2 -A3 \"placement.rs\" | head -60", "description": "Avertissements liés à placement.rs en build normal", "timeoutMs": 300000}`

  ```
warning: method `nom` is never used
  --> src/placement.rs:52:12
   |
40 | impl Support {
   | ------------ method in this implementation
--

warning: constant `INT8_TARDIF` is never used
   --> src/placement.rs:117:11
    |
117 | pub const INT8_TARDIF: Precision = Precision { nom: "int8 tardif", octets_par_valeur: 1.0, perte_ppl: 0.03 };
    |           ^^^^^^^^^^^

warning: constant `INT4_TARDIF` is never used
   --> src/placement.rs:119:11
    |
119 | pub const INT4_TARDIF: Precision = Precision { nom: "int4 tardif", octets_par_valeur: 0.5, perte_ppl: 2.7 };
    |           ^^^^^^^^^^^

warning: constant `TETE_4BIT` is never used
   --> src/placement.rs:122:11
    |
122 | pub const TETE_4BIT: Precision = Precision { nom: "tête 4 bits", octets_par_valeur: 0.5, perte_ppl: 10.0 };
    |           ^^^^^^^^^

warning: constant `INT4_GLOBAL` is never used
   --> src/placement.rs:124:11
    |
124 | pub const INT4_GLOBAL: Precision = Precision { nom: "int4 global", octets_par_valeur: 0.5, perte_ppl: 364.0 };
    |           ^^^^^^^^^^^

warning: constant `PRECISIONS` is never used
   --> src/placement.rs:127:11
    |
127 | pub const PRECISIONS: [Precision; 5] = [F32, INT8_TARDIF, INT4_T
… [213 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification que le test échoue sans l'entrée Q8_0 (retrait temporaire)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff --stat drave-core/src/placement.rs && git diff drave-core/src/placement.rs | head -140", "description": "Voir le diff courant de placement.rs"}`

  ```
drave-core/src/placement.rs | 116 ++++++++++++++++++++++++++++++++++++++++++++
 1 file changed, 116 insertions(+)
diff --git a/drave-core/src/placement.rs b/drave-core/src/placement.rs
index 1b2a5b8d..65c4ef39 100644
--- a/drave-core/src/placement.rs
+++ b/drave-core/src/placement.rs
@@ -157,6 +157,73 @@ pub fn choisir_avec_perte(
     meilleur.map(|(s, p, _)| (s, p))
 }
 
+// --- La tête : son format est celui du fichier, pas une requantification -----
+//
+// La mesure du 18/11 (`reports/rapport-a2.6-reconnaissance.md` § 3.4) : la tête
+// Q8_0 du fichier, posée en VRAM, donne la **même** perplexité qu'en RAM
+// (56,7642 = 56,7642) et passe de 7,43 à 1,80 ms/jeton. Ce n'est pas un choix de
+// précision : le fichier est déjà quantifié, on ne choisit que la **place**. La
+// table `PRECISIONS` reste donc la carte des **requantifications** d'un opérateur
+// f32 (budget nul ⇒ f32) ; la tête a ses entrées à part, à perte nulle.
+
+/// La tête **telle que le fichier la stocke**, en Q8_0 : 34 octets par bloc de
+/// 32 poids (une échelle f16 + 32 quants), soit **1,0625 octet par valeur**.
+/// Mesurée en VRAM à perte nulle (voir ci-dessus) : aucune requantification.
+pub const TETE_Q
… [5096 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/placement.rs", "old_string": "        GGML_F32 => Some(F32),\n        GGML_Q8_0 => Some(TETE_Q8_0),\n        GGML_Q6_K => Some(TETE_Q6_K),", "new_string": "        GGML_F32 => Some(F32),\n        GGML_Q6_K => Some(TETE_Q6_ … [5 caractères tronqués]`

  ```
Error: cannot edit "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/placement.rs": file changed since it was read — re-read the file, then retry
  ```

### 🤖 Assistant

⏵ Relecture du fichier (touch a changé l'horodatage) avant le test de retrait

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/placement.rs", "limit": 40, "offset": 180}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/placement.rs</path>
<type>file</type>
<content>
180: /// des têtes liées des Qwen en Q4_K_M (`model.rs:4855`) ; le gain VRAM n'a été
181: /// mesuré qu'en Q8_0 — Q6_K est à **rejouer** avant d'être cité comme mesuré.
182: pub const TETE_Q6_K: Precision = Precision {
183:     nom: "tête Q6_K",
184:     octets_par_valeur: 210.0 / 256.0,
185:     perte_ppl: 0.0,
186: };
187: 
188: /// La précision de la tête lue du **type ggml** du tenseur (`GGML_F32`,
189: /// `GGML_Q8_0`, `GGML_Q6_K`). `None` pour tout autre type : la règle ne connaît
190: /// pas de tête à perte nulle dans ce format et **n'invente rien** — l'appelant
191: /// garde alors son défaut. Les formats 4 bits restent `TETE_4BIT` (+10 % mesurés).
192: #[allow(dead_code)] // pas encore branché : le câblage est la tâche A2.6 suivante
193: pub fn precision_tete(type_ggml: u32) -> Option<Precision> {
194:     use crate::gguf::{GGML_F32, GGML_Q6_K, GGML_Q8_0};
195:     match type_ggml {
196:         GGML_F32 => Some(F32),
197:         GGML_Q8_0 => Some(TETE_Q8_0),
198:         GGML_Q6_K => Some(TETE_Q6_K),
199:         _ => None,
200:     }
201: }
202: 
203: //
… [982 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/placement.rs", "new_string": "        GGML_F32 => Some(F32),\n        GGML_Q6_K => Some(TETE_Q6_K),", "old_string": "        GGML_F32 => Some(F32),\n        GGML_Q8_0 => Some(TETE_Q8_0),\n        GGML_Q6_K => Some(TETE_Q6_ … [5 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/placement.rs has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core && cargo test placement 2>&1 | grep -E \"la_tete_q8_0|test result|panicked|FAILED|failures:\" | head -20; echo \"EXIT=${PIPESTATUS[0]}\"", "description": "Prouver l'échec du test sans l'entrée Q8_0", "timeoutMs": 600000}`

  ```
test placement::tests::la_tete_q8_0_se_place_comme_le_f32_a_perte_nulle ... FAILED
failures:
---- placement::tests::la_tete_q8_0_se_place_comme_le_f32_a_perte_nulle stdout ----
thread 'placement::tests::la_tete_q8_0_se_place_comme_le_f32_a_perte_nulle' (494206) panicked at src/placement.rs:323:78:
failures:
    placement::tests::la_tete_q8_0_se_place_comme_le_f32_a_perte_nulle
test result: FAILED. 8 passed; 1 failed; 0 ignored; 0 measured; 131 filtered out; finished in 0.00s
EXIT=101
  ```

### 🤖 Assistant

⏵ Entrée Q8_0 restaurée, vérification du retour au vert

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/placement.rs", "new_string": "        GGML_F32 => Some(F32),\n        GGML_Q8_0 => Some(TETE_Q8_0),\n        GGML_Q6_K => Some(TETE_Q6_K),", "old_string": "        GGML_F32 => Some(F32),\n        GGML_Q6_K => Some(TETE_Q6_ … [5 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/placement.rs has been updated successfully.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core && cargo test placement 2>&1 | grep -E \"test result|running|FAILED\" ; echo \"---\"; cd .. && git diff --stat drave-core/src/placement.rs", "description": "Retour au vert et contrôle du diff", "timeoutMs": 600000}`

  ```
running 9 tests
test result: ok. 9 passed; 0 failed; 0 ignored; 0 measured; 131 filtered out; finished in 0.00s
---
 drave-core/src/placement.rs | 116 ++++++++++++++++++++++++++++++++++++++++++++
 1 file changed, 116 insertions(+)
  ```

### 🤖 Assistant

⏵ Exécution du `cargo test` complet et relevé des lignes du diff

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core && cargo test 2>&1 | grep -E \"^running|test result|FAILED|error\\[\" | tail -10", "description": "cargo test complet après ajout", "timeoutMs": 900000}`

  ```
running 140 tests
test result: ok. 140 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 2.47s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"La tête : son format\\|pub const TETE_Q8_0\\|pub const TETE_Q6_K\\|pub fn precision_tete\\|pub fn choisir_tete\\|fn la_tete_q8_0_se_place\\|^}\" drave-core/src/placement.rs | sed -n '1,40p' && echo '--- total ---' && wc -l  … [92 caractères tronqués]`

  ```
38:}
60:}
66:}
74:}
81:}
103:}
112:}
158:}
160:// --- La tête : son format est celui du fichier, pas une requantification -----
172:pub const TETE_Q8_0: Precision = Precision {
176:};
182:pub const TETE_Q6_K: Precision = Precision {
186:};
193:pub fn precision_tete(type_ggml: u32) -> Option<Precision> {
201:}
212:pub fn choisir_tete(
225:}
232:}
241:}
302:    fn la_tete_q8_0_se_place_comme_le_f32_a_perte_nulle() {
369:}
--- total ---
369 drave-core/src/placement.rs
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/placement.rs", "limit": 60, "offset": 296}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/placement.rs</path>
<type>file</type>
<content>
296:         // Et l'int4 global (+364 %) ne passe aucun budget raisonnable.
297:         let encore = choisir_avec_perte(100 << 20, 100 << 20, 4 << 30, 64 << 30, 10.0).unwrap();
298:         assert_ne!(encore.1.nom, "int4 global");
299:     }
300: 
301:     #[test]
302:     fn la_tete_q8_0_se_place_comme_le_f32_a_perte_nulle() {
303:         // La mesure de la reconnaissance (18/11, § 3.4) : tête Q8_0 en VRAM, même
304:         // PPL qu'en RAM (56,7642 = 56,7642), 7,43 → 1,80 ms/jeton. La règle ne doit
305:         // donc pas déplacer la tête Q8_0 : elle la pose où le f32 se poserait.
306:         let n = 151_936u64 * 896;               // la tête d'un 0,5 B (vocab × caché)
307:         let octets_f32 = n * 4;
308: 
309:         // La référence : le f32 à budget nul, par la règle générique.
310:         let (sup_f32, p_f32) = choisir_avec_perte(octets_f32, octets_f32, 16 << 30, 64 << 30, 0.0)
311:             .unwrap();
312:         assert_eq!(p_f32, F32);
313: 
314:         // En f32, le nouveau chemin rend EXACTEMENT la réponse du chemin générique :
315:        
… [2062 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Contrôle complet des avertissements `dead_code` du nouveau bloc

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core && touch src/placement.rs && cargo build 2>&1 | grep -E \"placement.rs:(1[6-9][0-9]|2[0-2][0-9])\" -B3", "description": "Chercher des avertissements sur les lignes 160-225", "timeoutMs": 300000}`

  ```
(no output)
[exit code: 1]
  ```

### 🤖 Assistant

⏵ Collecte de la date, du HEAD et de l'état git pour le rapport

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date '+%Y-%m-%d %H:%M %Z' && git rev-parse --short HEAD && git status --porcelain | head -10 && echo '---' && git diff --numstat drave-core/src/placement.rs", "description": "Date, HEAD, état git et numstat"}`

  ```
2026-11-18 10:26 EST
8bec3cc8
 M drave-core/src/placement.rs
 M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/d67a9bb1-090e-4f69-baf2-a831c00aa275/digest.md
 M journal/sessions/d67a9bb1-090e-4f69-baf2-a831c00aa275/rapport.md
?? journal/sessions/9f4f7b6d-c5aa-4269-b785-a0f444424470/
?? journal/sessions/cbf7ca71-5b38-428e-9f19-298be1720918/
---
116	0	drave-core/src/placement.rs
  ```

### 🤖 Assistant

⏵ Vérification du format des rapports existants et de l'absence du fichier cible

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls reports/rapport-a2.6-tete-q8.md 2>&1; echo '---'; sed -n '1,35p' reports/rapport-a26-lot-disque.md", "description": "Vérifier existence et style d'un rapport voisin"}`

  ```
ls: cannot access 'reports/rapport-a2.6-tete-q8.md': No such file or directory
---
# A2.6 / A8.3 — le lot sur le disque : il accélère le calcul, il ne divise pas les lectures

> **Verdict.** Sur un modèle **dense** de 0,5 Go (Qwen2.5-0.5B-Q8), avec l'**éviction du cache**
> (`posix_fadvise(DONTNEED)`) : le lot **ne divise pas** les lectures du disque — **503 Mio** au lot 1,
> **502 Mio** aux lots 2, 4 et 8 (le modèle est lu une fois, quel que soit le lot). Le lot
> **accélère le calcul** : **24,0 → 30,5 tok/s** (+27 %) dès le lot 2, et le temps mural passe de
> **12,04 s à 9,96 s**. La **PPL** ne bouge presque pas : **15,8452** (lot 1) → **15,8443** (lot 2+),
> soit **−0,006 %**.
>
> **Date** : 2026-11-01. **Lignes** : A2.6 (ordonnanceur) et A8.3 (le lot). **Machine** : CPU seul.
> **Dispositif** : `tools/mesure_lot_disque.sh`, 192 jetons (les 85 626 jetons de
> `data/wikitext2_test.txt`), ctx 512, 20 fils, cache du modèle évincé avant chaque lot.

## 1. La question

A2.6 : « réduire le lot » — le lot réduit-il les lectures du disque ? A8.3c avait montré, sur le
français en f32, que le lot déplace la PPL à lui seul (61,9920 au lot 1, 60,8135 au lot ≥ 2). Ici :
le lot, sur l'**angla
… [740 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Repérage précis du site `_tete_tient` pour le rapport

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"_tete_tient\\|let octets_tete\" drave-core/src/model.rs && grep -n \"GGML_Q8_0: u32\\|GGML_Q6_K: u32\\|GGML_F32: u32\" drave-core/src/gguf.rs", "description": "Lignes exactes de _tete_tient et des constantes ggml"}`

  ```
4978:        let octets_tete = (cfg.vocab as u64 * cfg.hidden as u64) * 5 / 8;
4988:        let _tete_tient = crate::placement::choisir(octets_tete, octets_tete, libre_vram, 64 << 30)
573:pub const GGML_F32: u32 = 0;
589:pub const GGML_Q6_K: u32 = 14;
630:pub const GGML_Q8_0: u32 = 8;
  ```

### 🤖 Assistant

⏵ Vérification que `placement.rs` n'a pas bougé depuis le HEAD de la mesure

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline bb57604c..HEAD -- drave-core/src/placement.rs | head && echo \"--- commits suivants touchant placement.rs (tous) ---\" && git log --oneline -3 -- drave-core/src/placement.rs", "description": "Historique de placement … [22 caractères tronqués]`

  ```
--- commits suivants touchant placement.rs (tous) ---
b22b7097 A8.3 — LA REGLE PLACE ET PERTE EST BRANCHEE : placement::kv_precision choisit la precision du KV par couche selon le budget DRAVE_PERTE_MAX (defaut 1 %) — l'int8 si sa perte mesuree tient (+2,28 % sur les premieres, +0,03 % sur les dernieres), le f32 sinon. La regle rend EXACTEMENT le choix de la main : 30,7286 des deux cotes (contre 30,7660 en f32), memes couches en int8. Deux tests ajoutes (8/8). La lecon de la tete devient la regle du KV
976d55e4 A7.2 + A8.2 — LE RELAIS A CHIFFRE EGAL, ET LA PERTE ENTRE DANS LA REGLE. A7.2 etabli : porte-topologie (92 s, 42.5477) — une couche executee ailleurs rend la meme sortie, le flux coute 1 608 octets/flux, 0,25 Mbit/s, latence <= 20 ms ; reste la grappe intra-couche (A7.3). A8.2 code : choisir_avec_perte + 3 tests — l'int8 tardif (+0,03 %) passe a 1 %, l'int4 tardif (+2,7 %) exige 5 %, la tete 4 bits (+10 %) est refusee a 5 %, l'int4 global (+364 %) jamais : la lecon de la tete devient une regle testee
63ee9413 A2.6 — LA REGLE DE PLACEMENT DEVIENT GENERALE : placement::choisir(octets_par_jeton, octets_total, libre_vram, libre_ram) parcourt les supports par cout croissant et re
… [180 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Rédaction du rapport `reports/rapport-a2.6-tete-q8.md`

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-a2.6-tete-q8.md", "content": "# A2.6 — la tête Q8_0/Q6_K entre dans la règle, à perte nulle\n\n> **Verdict.** `placement.rs` porte désormais la **tête du fichier** comme précision :\n> `TETE_Q8_0` (**1,0625** octet par va … [14452 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-a2.6-tete-q8.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

### 🤖 Assistant

⏵ Précision du vocabulaire « perte » (format du fichier vs requantification)

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/placement.rs", "limit": 18, "offset": 186}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/placement.rs", "limit": 12, "offset": 340}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/placement.rs</path>
<type>file</type>
<content>
186: };
187: 
188: /// La précision de la tête lue du **type ggml** du tenseur (`GGML_F32`,
189: /// `GGML_Q8_0`, `GGML_Q6_K`). `None` pour tout autre type : la règle ne connaît
190: /// pas de tête à perte nulle dans ce format et **n'invente rien** — l'appelant
191: /// garde alors son défaut. Les formats 4 bits restent `TETE_4BIT` (+10 % mesurés).
192: #[allow(dead_code)] // pas encore branché : le câblage est la tâche A2.6 suivante
193: pub fn precision_tete(type_ggml: u32) -> Option<Precision> {
194:     use crate::gguf::{GGML_F32, GGML_Q6_K, GGML_Q8_0};
195:     match type_ggml {
196:         GGML_F32 => Some(F32),
197:         GGML_Q8_0 => Some(TETE_Q8_0),
198:         GGML_Q6_K => Some(TETE_Q6_K),
199:         _ => None,
200:     }
201: }
202: 
203: /// Place la **tête dans le format du fichier** : le support le moins cher où elle

(Showing lines 186-203 of 369. Use offset=204 to continue.)
</content>
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/placement.rs</path>
<type>file</type>
<content>
340:         );
341: 
342:         // Contrôle négatif : un type que la règle ne connaît pas (Q4_K, +10 %)
343:         // n'invente pas une tête à perte nulle.
344:         assert_eq!(
345:             choisir_tete(crate::gguf::GGML_Q4_K, n, 16 << 30, 64 << 30, 0.0),
346:             None
347:         );
348:     }
349: 
350:     #[test]
351:     fn la_regle_place_perte_choisit_le_kv_par_couche() {

(Showing lines 340-351 of 369. Use offset=352 to continue.)
</content>
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/placement.rs", "new_string": "/// La précision de la tête lue du **type ggml** du tenseur (`GGML_F32`,\n/// `GGML_Q8_0`, `GGML_Q6_K`). Ces entrées décrivent le **format du fichier** :\n/// placer ne requantifie pas, d'où l … [550 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/placement.rs has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/placement.rs", "new_string": "        // Contrôle négatif : un type sans entrée (Q4_K) rend None — la règle\n        // ne devine pas les octets d'un format qu'elle ne porte pas.", "old_string": "        // Contrôle négati … [105 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/placement.rs has been updated successfully.
  ```

### 🤖 Assistant

⏵ Mise à jour du rapport pour le même vocabulaire

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-a2.6-tete-q8.md", "new_string": "- **Le type ggml est celui du fichier**, pas un numéro inventé : `GGML_F32 = 0`,\n  `GGML_Q8_0 = 8`, `GGML_Q6_K = 14` (`drave-core/src/gguf.rs:573,630,589`). Un type\n  **sans entrée** ren … [514 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-a2.6-tete-q8.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-a2.6-tete-q8.md", "new_string": "5. **contrôle négatif** : un format **sans entrée** (`GGML_Q4_K`) → `None` : la règle\n   ne devine pas les octets d'un format qu'elle ne porte pas.", "old_string": "5. **contrôle négatif* … [115 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-a2.6-tete-q8.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-a2.6-tete-q8.md", "new_string": "    // Contrôle négatif : un type sans entrée (Q4_K) rend None — la règle\n    // ne devine pas les octets d'un format qu'elle ne porte pas.", "old_string": "    // Contrôle négatif : un t … [43 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-a2.6-tete-q8.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-a2.6-tete-q8.md", "new_string": "- **Les formats non couverts** : Q4_K, Q5_K, F16 rendent `None` — la règle ne les place\n  pas (voulu : elle ne porte que les entrées du fichier qu'elle documente). Une tête\n  Q4_K reste  … [351 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-a2.6-tete-q8.md has been updated successfully.
  ```

### 🤖 Assistant

⏵ Vérification finale : tests, diff, et intégrité des deux seuls fichiers

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core && cargo test placement 2>&1 | grep -E \"^running|test result\"; echo '=== tout ==='; cargo test 2>&1 | grep -E \"^running|test result\"", "description": "Tests placement et crate complet (final)", "timeoutMs": 900000}`

  ```
running 9 tests
test result: ok. 9 passed; 0 failed; 0 ignored; 0 measured; 131 filtered out; finished in 0.00s
=== tout ===
running 140 tests
test result: ok. 140 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 3.04s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --porcelain -- drave-core reports/rapport-a2.6-tete-q8.md && echo '---' && git diff --numstat -- drave-core && echo '--- model.rs/main.rs non touchés ---' && git diff --stat -- drave-core/src/model.rs drave-core/src/main.r … [104 caractères tronqués]`

  ```
M drave-core/src/placement.rs
?? reports/rapport-a2.6-tete-q8.md
---
117	0	drave-core/src/placement.rs
--- model.rs/main.rs non touchés ---
(vide = intact)
  ```

### 🤖 Assistant

⏵ Le commentaire ajouté décale le diff (+117) : relèvement des lignes exactes

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && wc -l drave-core/src/placement.rs && grep -n \"La tête : son format\\|pub const TETE_Q8_0\\|pub const TETE_Q6_K\\|pub fn precision_tete\\|pub fn choisir_tete\\|fn la_tete_q8_0_se_place\\|^}\" drave-core/src/placement.rs | sed -n '1,2 … [147 caractères tronqués]`

  ```
370 drave-core/src/placement.rs
38:}
60:}
66:}
74:}
81:}
103:}
112:}
158:}
160:// --- La tête : son format est celui du fichier, pas une requantification -----
172:pub const TETE_Q8_0: Precision = Precision {
176:};
182:pub const TETE_Q6_K: Precision = Precision {
186:};
194:pub fn precision_tete(type_ggml: u32) -> Option<Precision> {
202:}
213:pub fn choisir_tete(
226:}
233:}
242:}
303:    fn la_tete_q8_0_se_place_comme_le_f32_a_perte_nulle() {
---
    perte_ppl: 0.0,
};

/// La précision de la tête lue du **type ggml** du tenseur (`GGML_F32`,
/// `GGML_Q8_0`, `GGML_Q6_K`). Ces entrées décrivent le **format du fichier** :
/// placer ne requantifie pas, d'où la perte nulle. `None` pour un type **sans
/// entrée** : la règle ne devine ni les octets ni la perte, l'appelant garde son
/// défaut. La **requantification** 4 bits, elle, reste `TETE_4BIT` (+10 % mesurés).
#[allow(dead_code)] // pas encore branché : le câblage est la tâche A2.6 suivante
pub fn precision_tete(type_ggml: u32) -> Option<Precision> {
    use crate::gguf::{GGML_F32, GGML_Q6_K, GGML_Q8_0};
    match type_ggml {
        GGML_F32 => Some(F32),
        GGML_Q8_0 => Some(TETE_Q8_0),
        GGML_Q6_K => Some(TETE_Q6_
… [860 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Relevé des références numériques du rapport à corriger

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"116\\|369\\|160-225\\|188-201\\|203-225\\|301-348\\|323\\|324\\|160-225\" reports/rapport-a2.6-tete-q8.md", "description": "Lister les chiffres à actualiser dans le rapport"}`

  ```
9:> Le diff est **+116 / −0** lignes ; **aucun câblage** : `model.rs` n'est pas touché, le
49:`git diff --numstat drave-core/src/placement.rs` → **116 ajouts, 0 suppression**
50:(fichier de 253 → **369** lignes), uniquement des ajouts.
54:| bloc tête (commentaire de section + tout ce qui suit) | **160-225** | le format du fichier, pas une requantification |
57:| `precision_tete(type_ggml)` | 188-201 | type ggml → `Precision` ; `None` sinon |
58:| `choisir_tete(...)` | 203-225 | place la tête **dans son format**, sous budget de perte |
59:| test `la_tete_q8_0_se_place_comme_le_f32_a_perte_nulle` | **301-348** | le test demandé |
129:`placement.rs:301-348`, un seul test :
196:| entrée retirée | **8 passed, 1 failed** (`test result: FAILED`, code 101) — panique sur le `.unwrap()` de `choisir_tete(GGML_Q8_0, …)` à `placement.rs:323` (323 pendant le retrait, 324 une fois l'entrée remise) |
248:| lignes de `placement.rs` | 253 | **369** |
249:| diff | — | **+116 / −0**, 1 fichier |
254:- Build : **pas de nouvel avertissement** sur les lignes 160-225 (vérifié par
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-a2.6-tete-q8.md", "new_string": "> Le diff est **+117 / −0** lignes ; **aucun câblage** : `model.rs` n'est pas touché, le", "old_string": "> Le diff est **+116 / −0** lignes ; **aucun câblage** : `model.rs` n'est pas touc … [8 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-a2.6-tete-q8.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-a2.6-tete-q8.md", "new_string": "`git diff --numstat drave-core/src/placement.rs` → **117 ajouts, 0 suppression**\n(fichier de 253 → **370** lignes), uniquement des ajouts.\n\n| élément | lignes | rôle |\n|---|---:|---|\n … [1392 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-a2.6-tete-q8.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-a2.6-tete-q8.md", "new_string": "`placement.rs:302-349`, un seul test :", "old_string": "`placement.rs:301-348`, un seul test :"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-a2.6-tete-q8.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-a2.6-tete-q8.md", "new_string": "| entrée retirée | **8 passed, 1 failed** (`test result: FAILED`, code 101) — panique sur le `.unwrap()` de `choisir_tete(GGML_Q8_0, …)` |", "old_string": "| entrée retirée | **8 passed, 1 … [184 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-a2.6-tete-q8.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-a2.6-tete-q8.md", "new_string": "| lignes de `placement.rs` | 253 | **370** |\n| diff | — | **+117 / −0**, 1 fichier |", "old_string": "| lignes de `placement.rs` | 253 | **369** |\n| diff | — | **+116 / −0**, 1 fichier | … [2 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-a2.6-tete-q8.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-a2.6-tete-q8.md", "new_string": "- Build : **pas de nouvel avertissement** sur les lignes 160-226 (vérifié par", "old_string": "- Build : **pas de nouvel avertissement** sur les lignes 160-225 (vérifié par"}`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-a2.6-tete-q8.md has been updated successfully.
  ```

### 🤖 Assistant

⏵ Contrôle final : re-test de retrait, cohérence du code cité, chiffres du rapport

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '302,349p' drave-core/src/placement.rs", "description": "Extraire le test final pour comparaison"}`

  ```
#[test]
    fn la_tete_q8_0_se_place_comme_le_f32_a_perte_nulle() {
        // La mesure de la reconnaissance (18/11, § 3.4) : tête Q8_0 en VRAM, même
        // PPL qu'en RAM (56,7642 = 56,7642), 7,43 → 1,80 ms/jeton. La règle ne doit
        // donc pas déplacer la tête Q8_0 : elle la pose où le f32 se poserait.
        let n = 151_936u64 * 896;               // la tête d'un 0,5 B (vocab × caché)
        let octets_f32 = n * 4;

        // La référence : le f32 à budget nul, par la règle générique.
        let (sup_f32, p_f32) = choisir_avec_perte(octets_f32, octets_f32, 16 << 30, 64 << 30, 0.0)
            .unwrap();
        assert_eq!(p_f32, F32);

        // En f32, le nouveau chemin rend EXACTEMENT la réponse du chemin générique :
        // il ne réinvente pas le placement.
        assert_eq!(
            choisir_tete(crate::gguf::GGML_F32, n, 16 << 30, 64 << 30, 0.0),
            choisir_avec_perte(octets_f32, octets_f32, 16 << 30, 64 << 30, 0.0)
        );

        // La tête Q8_0 : la même place que la référence, perte nulle, et le bon
        // format du fichier (8 bits utiles + l'échelle de bloc).
        let (sup_q8, p_q8) =
            choisir_tete(crate::gguf::GGML_
… [1046 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"116\\|369\\|160-225\\|188-201\\|203-225\\|301-348\\|placement.rs:323\" reports/rapport-a2.6-tete-q8.md; echo \"(vide = plus de chiffre périmé)\"", "description": "Vérifier qu'aucun chiffre périmé ne reste"}`

  ```
(vide = plus de chiffre périmé)
  ```

### 🤖 Assistant

⏵ Relecture complète du rapport avant remise

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-a2.6-tete-q8.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-a2.6-tete-q8.md</path>
<type>file</type>
<content>
1: # A2.6 — la tête Q8_0/Q6_K entre dans la règle, à perte nulle
2: 
3: > **Verdict.** `placement.rs` porte désormais la **tête du fichier** comme précision :
4: > `TETE_Q8_0` (**1,0625** octet par valeur, 34 octets par bloc de 32) et `TETE_Q6_K`
5: > (**0,8203** octet par valeur, 210 octets par super-bloc de 256), toutes deux à
6: > **perte 0,0**. Ce n'est **pas** une requantification : la mesure de la reconnaissance
7: > (18/11, § 3.4) pose la tête **Q8_0 du fichier** en VRAM sans bouger la perplexité
8: > (**56,7642 = 56,7642**) et en divisant son temps par **4,1** (7,43 → **1,80 ms/jeton**).
9: > Le diff est **+117 / −0** lignes ; **aucun câblage** : `model.rs` n'est pas touché, le
10: > défaut ne bouge pas, le comportement à l'exécution est identique (les points d'entrée
11: > neufs ne sont appelés que par le test).
12: >
13: > **Date** : 2026-11-18. **Ligne de roadmap** : A2.6 (ordonnanceur : la tête).
14: > **HEAD** : `8bec3cc8`. **Nature** : implémentation **testée**, **sans commit**.
15: > **Fichiers écrits** : `drave-core/src/placement.rs` (seule modifi
… [14594 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification du nom exact du garde-fou et ajustement de la recommandation

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"DRAVE_PERTE_MAX\" drave-core/src/model.rs | head -5", "description": "Confirmer le nom DRAVE_PERTE_MAX"}`

  ```
4709:        // premières couches, +0,03 % sur les dernières (A5.3) — le budget `DRAVE_PERTE_MAX`
4711:        // La règle s'active **explicitement** (`DRAVE_PERTE_MAX`) : un changement de défaut
4715:            && std::env::var("DRAVE_PERTE_MAX").is_ok() {
4716:            let budget_pct: f64 = std::env::var("DRAVE_PERTE_MAX").ok()
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-a2.6-tete-q8.md", "new_string": "1. **Brancher** `choisir_tete` à `model.rs:4988`, là où `_tete_tient` est aujourd'hui un\n   calcul jeté : passer le **type ggml** de la tête (`tete.ttype`) et\n   `cfg.vocab × cfg.hidden` … [663 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-a2.6-tete-q8.md has been updated successfully.
  ```

### 🤖 Assistant

⏵ Vérification finale des tests et de l'état du dépôt

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core && cargo test placement 2>&1 | grep -E \"^running|test result\" && cargo test 2>&1 | grep -E \"^running|test result\"", "description": "Comptes finaux des tests", "timeoutMs": 900000}`

  ```
running 9 tests
test result: ok. 9 passed; 0 failed; 0 ignored; 0 measured; 131 filtered out; finished in 0.00s
running 140 tests
test result: ok. 140 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 2.58s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --porcelain -- drave-core reports/rapport-a2.6-tete-q8.md && git diff --numstat -- drave-core && wc -l drave-core/src/placement.rs reports/rapport-a2.6-tete-q8.md && git diff --stat -- drave-core/src/model.rs drave-core/sr … [99 caractères tronqués]`

  ```
M drave-core/src/placement.rs
?? reports/rapport-a2.6-tete-q8.md
117	0	drave-core/src/placement.rs
  370 drave-core/src/placement.rs
  268 reports/rapport-a2.6-tete-q8.md
  638 total
(model.rs/main.rs : vide = intacts)
  ```

### 🤖 Assistant

⏵ Envoi du résultat au parent

- **send_message** `{"agent_id": "d67a9bb1-090e-4f69-baf2-a831c00aa275", "message": "A2.6 tête Q8_0/Q6_K — terminé, testé, aucun commit.\n\nDIFF : `drave-core/src/placement.rs` seul fichier de code modifié, **+117 / −0** (253 → 370 lignes). Ajouts : section tête (l.160-226) avec `TETE_Q8_0` (1,0625 o/valeur = 34/32, pe … [1781 caractères tronqués]`

  ```
message delivered to agent d67a9bb1-090e-4f69-baf2-a831c00aa275
  ```

### 🤖 Assistant

⏵ Tâche terminée : entrées tête Q8_0/Q6_K ajoutées et testées

## Diff (résumé)

**`drave-core/src/placement.rs`** — seul fichier de code modifié : **+117 / −0** lignes (253 → 370), aucun commit.

| élément | lignes | contenu |
|---|---:|---|
| `TETE_Q8_0` | 172-176 | `1,0625` o/valeur (34 o / bloc de 32), **perte 0,0** |
| `TETE_Q6_K` | 182-186 | `0,8203125` o/valeur (210 o / bloc de 256), **perte 0,0** |
| `precision_tete(type_ggml)` | 188-202 | `GGML_F32/GGML_Q8_0/GGML_Q6_K` → `Precision`, sinon `None` |
| `choisir_tete(...)` | 204-226 | place la tête **dans son format** ; `perte_max` négatif ⇒ `None` |
| test `la_tete_q8_0_se_place_comme_le_f32_a_perte_nulle` | 302-349 | le test demandé |

**Choix assumé** : les entrées sont **hors de `PRECISIONS`**, car `choisir_avec_perte` prend le moins cher sous budget — une entrée à perte 0 y gagnerait à budget nul contre f32 (et dès 1 % contre int8), cassant 2 des 8 tests. La table générique, ses 5 constantes et `choisir_avec_perte` sont inchangés au caractère près. `perte_ppl: 0.0` signifie **aucune perte due au placement** (même format du fichier), pas « Q8_0 = f32 ».

## Comptes

| commande | avant | après |
|---|---:|---:|
| `cargo test placement` | 8/8 | **9/9**, 0 échec |
| `cargo test` (crate) | 139/139 | **140/140**, 0 échec |

**Contrôle de retrait** : sans la ligne `GGML_Q8_0 => Some(TETE_Q8_0)`, `cargo test placement` donne **8 passed, 1 failed** (exit 101, panique sur l'`unwrap`) ; entrée remise → 9/9. `model.rs` et `main.rs` sont intacts : aucun câblage, aucun changement de défaut.

## Rapport

**`reports/rapport-a2.6-tete-q8.md`** (268 lignes) : la mesure de la reconnaissance (56,7642 = 56,7642 ; 7,43 → 1,80 ms/jeton ; contrôle `DRAVE_GPU=0`), le diff et ses lignes, le test, les comptes, et ce qui pourrait le rendre faux — **machine chargée** (13,7 → 31,4, à rejouer au repos), égalité de PPL imprimée à 4 décimales, **Q6_K jamais mesuré** (0,0 par construction, signalé comme à rejouer), octets nominaux/alignement des blocs, repli NVMe silencieux préexistant.

