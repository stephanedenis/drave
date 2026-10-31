# Session DSH — relecture

- identifiant : `d622230d-649c-43cf-9202-da1eeb230259`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-10-29 22:25:45
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu es dans /home/stephane/Data13TB/stephane/GitHub/Qtrinet (dépôt Drave, Rust + Python). Tâche de RECHERCHE/PLAN, sans modifier en-cours/roadmap/AGENTS et sans commit.

Objectif N3 : prototype natif distribué à deux processus. Lis drave-core/src/native.rs (Native::open, pas, pas_profondeur, generer, servir), drave-core/src/main.rs (modes --drvm-serve, --drvm-forward, --drvm-generate, --drvm-native-ppl) et tools/porte-n3-service.sh, tools/porte-n3-profondeur.sh, tools/porte-n3-composition.sh.

Question : quel est le plus petit changement Rust honnête pour exécuter un DRVM en DEUX régions (blocs 0..k puis k..n) avec transfert d'état entre deux processus, et une porte qui compare au modèle local plein ? Précise :
- les fonctions à refactorer (pas/pas_profondeur), les structures Cache, le format d'état à transférer (hidden + cache K/V ou pas de cache) ;
- un protocole minimal (fichier ou TCP localhost) et le CLI exact ;
- les pièges (positions, cache, tête, pont, thought_steps) ;
- une estimation de complexité et un chemin de repli si le cache K/V est trop lourd ;
- les commandes de test et le contrôle négatif.
Réponds en un plan concret avec signatures Rust proposées et fichiers touchés. Ne modifie aucun fichier. Ne lis pas tout le dépôt : cible les fichiers cités.
Your parent agent id is "71d57f53-8b41-4220-84dd-7bb9eedc88d9". Before you finish, send your result to that agent with send_message({ agent_id: "71d57f53-8b41-4220-84dd-7bb9eedc88d9", message: "<self-contained result>" }). The parent shares your workspace but does not automatically receive your transcript, tool output, or reasoning. Send earlier messages as well when a finding changes what the parent should do next; sending a message does not end your turn.

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
réseau sont des **faits** regroupés en **listes valuées poussées** vers leurs lecteurs : le coût du calcul devient proportionnel à l'**activité**, et le modèle devient **décomposable**, **répartissable** et **observable**. Le projet a pour principe que la structure bat la taille. Construire le moteur et modèle optimisé qui rend cette structure observable, décomposable, répartissable et rejouable permet d'atteindre de nouveaux sommets. Bref, révolutionner l'IA avec une approche par bus d'événements où chaque bloc fonctionnel est optimisable, comparable et substituable par des alternatives ayant des architectures différentes. e.g. Blocs neuronaux là où l'intuition est un avantage, blocs computationnels classiques pour les opérations où l'informatique classique est plus fiable et performante.

Le projet est né du besoin de faire tourner des modèles **de types différents** sur des machines **limitées**, de
les **combiner**, de les **décomposer en couches et grappes de neurones** exécutables par du matériel divers, voire
**distribué en réseau**, de les **diagnostiquer et faire évoluer** en étudiant leurs **flux**, et de **rejouer à
volonté** des événements.


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

⏵ Lecture des fichiers ciblés (native.rs, main.rs, portes N3)

- **bash** `{"command": "wc -l drave-core/src/native.rs drave-core/src/main.rs tools/porte-n3-service.sh tools/porte-n3-profondeur.sh tools/porte-n3-composition.sh 2>&1", "description": "Count lines of targeted files"}`

  ```
465 drave-core/src/native.rs
  8801 drave-core/src/main.rs
    82 tools/porte-n3-service.sh
    73 tools/porte-n3-profondeur.sh
    80 tools/porte-n3-composition.sh
  9501 total
  ```

- **bash** `{"command": "ls -la drave-core/src/ tools/ | head -80", "description": "List source and tools directories"}`

  ```
drave-core/src/:
total 1848
drwxr-xr-x. 1 stephane stephane    380 28 oct 15:26 .
drwxr-xr-x. 1 stephane stephane     92 28 oct 16:25 ..
-rw-r--r--. 1 stephane stephane   7223  9 oct 21:38 bus.rs
-rw-------. 1 stephane stephane  24376  1 oct 12:08 clusters.rs
-rw-r--r--. 1 stephane stephane  16476 28 oct 15:26 drvm.rs
-rw-r--r--. 1 stephane stephane  48545  3 oct 15:36 engine.rs
-rw-r--r--. 1 stephane stephane  24423  2 oct 17:26 engram.rs
-rw-------. 1 stephane stephane  36720  9 oct 22:54 episodique.rs
-rw-r--r--. 1 stephane stephane  81296  2 oct 23:55 formats.rs
-rw-r--r--. 1 stephane stephane 129074 28 oct 12:28 gguf.rs
-rw-r--r--. 1 stephane stephane  79840 21 oct 16:34 gpu.rs
-rw-------. 1 stephane stephane  97544 24 oct 19:01 kimi_k3.rs
-rw-------. 1 stephane stephane  75095  2 oct 23:55 list.rs
-rw-r--r--. 1 stephane stephane 487518 29 oct 20:23 main.rs
-rw-------. 1 stephane stephane  22791 12 oct 20:12 materiel.rs
-rw-r--r--. 1 stephane stephane 586000 28 oct 12:28 model.rs
-rw-------. 1 stephane stephane  12831 16 oct 03:04 mrope.rs
-rw-r--r--. 1 stephane stephane  22298 29 oct 20:40 native.rs
-rw-r--r--. 1 stephane stephane  11016 24 oct 16:28 placement.rs
-rw-------. 
… [4003 caractères tronqués]
  ```

- **read** `{"file_path": "drave-core/src/native.rs"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/native.rs</path>
<type>file</type>
<content>
1: //! Exécution native d'un `drave-n0` DRVM : les tenseurs sont lus dans le
2: //! conteneur, sans GGUF intermédiaire. C'est volontairement simple (f32, une
3: //! séquence, pas de cache KV) : le but est de prouver que le format natif
4: //! s'exécute, pas d'être rapide.
5: 
6: use std::collections::HashMap;
7: use std::sync::atomic::{AtomicUsize, Ordering};
8: 
9: use crate::drvm::{Drvm, ErreurDrvm, Json};
10: 
11: #[derive(Debug, Clone)]
12: pub struct Cfg {
13:     pub vocab: usize,
14:     pub d: usize,
15:     pub n_blocks: usize,
16:     pub n_heads: usize,
17:     pub expert_hidden: usize,
18:     pub n_experts: usize,
19:     pub top_k: usize,
20:     pub kwta: f64,
21:     pub window: usize,
22:     pub thought_steps: usize,
23: }
24: 
25: fn champ<'a>(j: &'a Json, k: &str) -> Result<&'a Json, ErreurDrvm> {
26:     j.get(k).ok_or_else(|| ErreurDrvm(format!("architecture.{k} absent")))
27: }
28: 
29: fn u(j: &Json, k: &str) -> Result<usize, ErreurDrvm> {
30:     champ(j, k)?.as_u64().map(|x| x as usize).ok_or_else(|| ErreurDrvm(format!("architecture.{k} non ent
… [23403 caractères tronqués]
  ```

- **read** `{"file_path": "tools/porte-n3-service.sh"}`
- **read** `{"file_path": "tools/porte-n3-profondeur.sh"}`
- **read** `{"file_path": "tools/porte-n3-composition.sh"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-n3-service.sh</path>
<type>file</type>
<content>
1: #!/bin/bash
2: # porte-n3-service.sh — N3.2a : le service natif (`--drvm-serve`) répond-il, et le même
3: # modèle donne-t-il la même génération que le chemin CLI ?
4: #
5: # LA QUESTION. N3 demande que les briques natives tournent **dans le moteur**, pas seulement
6: # dans un outil. Le service `--drvm-serve` est le chemin de production ; cette porte le fait
7: # tourner sur un DRVM **reproductible** (petit modèle généré par `tools/native_model.py`,
8: # graine fixe), vérifie `/sante`, deux générations identiques, une génération différente pour
9: # un autre prompt, et un 404. Elle ne prétend pas tester la sortie précoce (le service ne
10: # l'a pas encore) : c'est N3.2a, le service et le routage/k-WTA du modèle natif.
11: set -u
12: cd "$(dirname "$0")/.."
13: D=${D:-./drave-core/target/release/drave}
14: PY=${PY:-/home/stephane/gpu-env/bin/python}
15: PORT=${PORT:-$((61000 + RANDOM % 2000))}
16: T=$(mktemp -d "${TMPDIR:-/tmp}/porte-n3-service-XXXXXX")
17: trap 'kill ${SRV:-} 2>/dev/null; wait ${SRV:-} 2>/dev/null; rm -rf "$T"' EXIT
18: [ -x "$D" ] || { echo "  ❌ 
… [3273 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-n3-profondeur.sh</path>
<type>file</type>
<content>
1: #!/bin/bash
2: # porte-n3-profondeur.sh — N3.2b0 : la profondeur de service change-t-elle la génération ?
3: #
4: # `DRAVE_NATIVE_PROFONDEUR=N` coupe le calcul natif après N blocs (défaut : tous).
5: # C'est une sortie précoce FIXE, sans seuil de confiance : N3.2b0 mesure le CHEMIN
6: # de service, pas la qualité. La porte vérifie que le même modèle à profondeur 1
7: # et à profondeur pleine donne des sorties différentes, que chaque profondeur est
8: # déterministe, et que /sante ne change pas.
9: set -u
10: cd "$(dirname "$0")/.."
11: D=${D:-./drave-core/target/release/drave}
12: PY=${PY:-/home/stephane/gpu-env/bin/python}
13: T=$(mktemp -d "${TMPDIR:-/tmp}/porte-n3-profondeur-XXXXXX")
14: trap 'kill ${SRV:-} 2>/dev/null; wait ${SRV:-} 2>/dev/null; rm -rf "$T"' EXIT
15: [ -x "$D" ] || { echo "  ❌ $D absent"; exit 2; }
16: "$PY" -c "import torch" 2>/dev/null || { echo "  ❌ $PY n'a pas torch"; exit 2; }
17: 
18: echo "=== 1. un DRVM à 2 blocs, graine 7 ==="
19: "$PY" - "$T/modele.drvm" "$T/params" <<'PY' || exit 2
20: import sys, torch
21: sys.path.insert(0, ".")

… [3055 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-n3-composition.sh</path>
<type>file</type>
<content>
1: #!/bin/bash
2: # porte-n3-composition.sh — N3.4a : les briques natives composent-elles sur UN modèle ?
3: #
4: # N3.2a (service), N3.2b0 (profondeur), N3.3a (routage) et N3.3c (comptage) ont
5: # chacun leur porte. Ici tout tourne sur les MÊMES deux modèles (A/B, mêmes poids,
6: # top_k différent) : le service, la profondeur 1, la génération et les compteurs.
7: # Ce n'est pas encore la composition avec seuil de confiance (N3.2b) ni avec le
8: # pont/placement ; c'est N3.4a, la composition des briques déjà branchées.
9: set -u
10: cd "$(dirname "$0")/.."
11: D=${D:-./drave-core/target/release/drave}
12: PY=${PY:-/home/stephane/gpu-env/bin/python}
13: T=$(mktemp -d "${TMPDIR:-/tmp}/porte-n3-composition-XXXXXX")
14: trap 'kill ${SRV:-} 2>/dev/null; wait ${SRV:-} 2>/dev/null; rm -rf "$T"' EXIT
15: [ -x "$D" ] || { echo "  ❌ $D absent"; exit 2; }
16: "$PY" -c "import torch" 2>/dev/null || { echo "  ❌ $PY n'a pas torch"; exit 2; }
17: 
18: echo "=== 1. deux modèles à 2 blocs, mêmes poids ==="
19: "$PY" - "$T" <<'PY' || exit 2
20: import sys, torch
21: sys.path.insert
… [3466 caractères tronqués]
  ```

- **bash** `{"command": "grep -n -- '--drvm-serve\\|--drvm-forward\\|--drvm-generate\\|--drvm-native-ppl\\|--drvm-sparsite\\|drvm-native' drave-core/src/main.rs | head -60", "description": "Locate DRVM CLI modes in main.rs"}`

  ```
170:    if args[1] == "--drvm-serve" {
176:    if args[1] == "--drvm-native-ppl" {
190:    if args[1] == "--drvm-generate-full" {
202:    if args[1] == "--drvm-generate" {
203:        let f = match args.get(2) { Some(f) => f.clone(), None => { eprintln!("--drvm-generate attend un DRVM"); std::process::exit(2); } };
214:    if args[1] == "--drvm-sparsite" {
225:    if args[1] == "--drvm-forward" {
226:        let f = match args.get(2) { Some(f) => f.clone(), None => { eprintln!("--drvm-forward attend un DRVM"); std::process::exit(2); } };
  ```

- **bash** `{"command": "grep -n 'fn main\\|^fn \\|^pub fn ' drave-core/src/main.rs | head -80", "description": "List top-level functions in main.rs"}`

  ```
90:fn fmt_bits(b: u64, n: usize) -> String {
103:fn rapport_hebb_diff(mdl: &model::Model) {
113:fn main() {
657:fn modele_chemin() -> String { MODELE.get().cloned().unwrap_or_default() }
670:fn appliquer_fusion(mdl: &mut model::Model, fusion_etat: Option<String>, fusion_alpha: f32,
699:fn poser_tete_partielle(mdl: &mut model::Model) {
712:fn appliquer_adaptateur(mdl: &mut model::Model, chemin: Option<&str>, tete_partielle: bool) {
742:fn poser_plage(mdl: &mut model::Model, tete_partielle: bool, adaptateur: Option<&str>) {
768:fn avertir_puits_inertes(mdl: &model::Model, impose: bool) {
777:fn options_actives(mdl: &model::Model, mode: &str, ctx_impose: bool, dense: bool, keep: f32,
865:fn fils(opt: &Options) -> usize {
1132:fn analyser(args: &[String]) -> Options {
1443:fn stats_tampons() {
1452:fn stats_experts(mdl: &model::Model) {
1464:fn run_infer(opt: Options) {
1872:fn all_ids_of(v: &[u32]) -> Vec<u32> { v.to_vec() }
1874:fn meta_strings(g: &Gguf, key: &str) -> Vec<String> {
1881:fn meta_ints(g: &Gguf, key: &str) -> Vec<i32> {
1888:fn build_tokenizer(g: &Gguf) -> tokenizer::Tokenizer {
1902:fn poser_tete_restreinte(mdl: &mut model::Model, fichier: &str) -> bool {
1921:fn cfg_d
… [3144 caractères tronqués]
  ```

- **read** `{"file_path": "drave-core/src/main.rs", "offset": 113, "limit": 190}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
113: fn main() {
114:     let args: Vec<String> = std::env::args().collect();
115:     if args.len() < 2 {
116:         eprintln!("usage: drave <modele.gguf|dossier-de-clusters> [--matrix NOM] [--threads N]");
117:         eprintln!("       drave --drvm-inspect MODELE.drvm  en-tête, graphe et tenseurs DRVM");
118:         eprintln!("       drave <modele> --infer (--ids 1,2,3 | --prompt TEXTE | --ids-file F)");
119:         eprintln!("             [--n 32] [--temp 0] [--ctx 512] [--threads N]");
120:         eprintln!("       drave <modele> --ppl FICHIER-IDS [--ctx N] [--limit N] [--dense]");
121:         eprintln!("       drave --fusionner-trace T1 T2 [...] [--fusion-sortie F]");
122:         eprintln!("                                     fusionne des traces de plusieurs processus,");
123:         eprintln!("                                     ordonnées par le TEMPS MURAL, mesure la");
124:         eprintln!("                                     dérive des horloges et confronte les deux");
125:         eprintln!("                                     bouts de chaque lien
… [12254 caractères tronqués]
  ```

- **read** `{"file_path": "drave-core/src/drvm.rs"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/drvm.rs</path>
<type>file</type>
<content>
1: //! DRVM v0 — lecteur du conteneur natif de modèle Drave.
2: //!
3: //! Ce n'est pas un GGUF amélioré : le manifeste porte un **graphe** (blocs,
4: //! ports, routes, têtes, pont) et le payload porte des tenseurs alignés par
5: //! bloc. Le lecteur refuse une version, un type de bloc ou une section qu'il ne
6: //! connaît pas ; il n'exécute jamais un fichier à moitié compris.
7: //!
8: //! Le crate reste **std seul** : le JSON minimal est analysé à la main.
9: 
10: use std::collections::BTreeSet;
11: use std::fs;
12: use std::path::Path;
13: 
14: pub const MAGIC: &[u8; 4] = b"DRVM";
15: pub const VERSION: u16 = 0;
16: pub const HEADER_SIZE: usize = 92;
17: pub const ALIGNEMENT: usize = 64;
18: pub const BLOCS_CONNUS: &[&str] = &[
19:     "input", "local_mixer", "sparse_ffn", "state", "early_head",
20:     "thought", "bridge", "output",
21: ];
22: 
23: #[derive(Debug, Clone)]
24: pub enum Json {
25:     Null,
26:     Bool(bool),
27:     Nombre(f64),
28:     Chaine(String),
29:     Tableau(Vec<Json>),
30:     Objet(Vec<(String, Json)>),
31: }
32: 
33: impl Json {
34:    
… [17143 caractères tronqués]
  ```

- **bash** `{"command": "grep -n 'def \\|class \\|bridge\\|thought\\|early\\|head_byte\\|rsn\\|n_blocks' tools/native_model.py | head -80; echo ---; wc -l tools/native_model.py", "description": "Inspect native_model.py structure"}`

  ```
25:class NativeConfig:
28:    n_blocks: int = 6
36:    thought_steps: int = 2
37:    early_blocks: tuple[int, ...] = (1, 3, 5)  # 0-based : après 2, 4, 6
38:    rsn_dim: int = 120
41:class SparseFFN(nn.Module):
42:    def __init__(self, cfg: NativeConfig):
50:    def forward(self, x):
70:class Block(nn.Module):
71:    def __init__(self, cfg: NativeConfig):
80:    def forward(self, x):
96:class NativeModel(nn.Module):
97:    def __init__(self, cfg: NativeConfig | None = None):
102:        self.blocks = nn.ModuleList([Block(self.cfg) for _ in range(self.cfg.n_blocks)])
103:        self.early_heads = nn.ModuleList([nn.Linear(self.cfg.d_model, self.cfg.vocab)
104:                                          for _ in self.cfg.early_blocks])
109:                                          for _ in range(self.cfg.n_blocks)])
110:        self.bridge = nn.Linear(self.cfg.d_model, self.cfg.d_model)
111:        self.thought = nn.Linear(self.cfg.d_model, self.cfg.d_model)
112:        self.thought_in = nn.Linear(self.cfg.d_model, self.cfg.d_model)
113:        self.head_byte = nn.Linear(self.cfg.d_model, self.cfg.vocab)
114:        self.head_rsn = nn.Linear(self.cfg.d_model, self.cfg.rsn_dim)
116:   
… [2392 caractères tronqués]
  ```

- **read** `{"file_path": "tools/native_model.py", "offset": 96, "limit": 109}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/native_model.py</path>
<type>file</type>
<content>
96: class NativeModel(nn.Module):
97:     def __init__(self, cfg: NativeConfig | None = None):
98:         super().__init__()
99:         self.cfg = cfg or NativeConfig()
100:         self.embed = nn.Embedding(self.cfg.vocab, self.cfg.d_model)
101:         self.pos = nn.Embedding(self.cfg.max_pos, self.cfg.d_model)
102:         self.blocks = nn.ModuleList([Block(self.cfg) for _ in range(self.cfg.n_blocks)])
103:         self.early_heads = nn.ModuleList([nn.Linear(self.cfg.d_model, self.cfg.vocab)
104:                                           for _ in self.cfg.early_blocks])
105:         # Têtes LOCALES : une sortie après CHAQUE bloc, pour la supervision
106:         # profonde. Elles n'existaient pas dans les checkpoints antérieurs :
107:         # le chargement se fait en strict=False et elles apprennent.
108:         self.local_heads = nn.ModuleList([nn.Linear(self.cfg.d_model, self.cfg.vocab)
109:                                           for _ in range(self.cfg.n_blocks)])
110:         self.bridge = nn.Linear(self.cfg.d_model, self.cfg.d_model)
111:         self.thoug
… [5467 caractères tronqués]
  ```

- **bash** `{"command": "grep -n 'porte-n3\\|registre\\|PORTES' tools/toutes-les-portes.sh | head -40; echo ---; ls tools/ | grep -i 'porte-n3'", "description": "Inspect gates registry and N3 gate family"}`

  ```
22:#   PORTES="gain topologie" tools/toutes-les-portes.sh    # un sous-ensemble (filtre)
31:FILTRE=${PORTES:-}
47:echo "=== PASSE COMPLÈTE DES PORTES ($(printf '%s\n' $portes | grep -c . ) portes, borne ${DELAI} s) ==="
71:    printf '%s %s %s\n' "$nom" "$code" "$dt" >> "$JOURNAUX/registre.txt"
74:echo "--- $vertes vertes, $rouges rouges ---" | tee -a "$JOURNAUX/registre.txt"
84:echo "TOUTES LES PORTES SONT VERTES — et elles ont TOUTES tourné, ce que rien ne garantissait avant."
---
porte-n3-cache.sh
porte-n3-composition.sh
porte-n3-placement.sh
porte-n3-pont.sh
porte-n3-profondeur.sh
porte-n3-routes.sh
porte-n3-service.sh
porte-n3-seuil.sh
porte-n3-sparsite-compte.sh
porte-n3-sparsite.sh
  ```

- **read** `{"file_path": "drave-core/src/main.rs", "offset": 3872, "limit": 70}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
3872: fn envoyer_lot(s: &mut std::net::TcpStream, debut: u32, fin: u32, pos0: u32,
3873:                etats: &[f32], t: usize, mdl: &model::Model) -> std::io::Result<usize> {
3874:     use std::io::Write;
3875:     let tete = tete_flux(MODE_LOT, debut, fin, pos0, t, 0.0, Some(mdl));
3876:     // Le préfixe v6 (`np` + `pre`) manquait ICI : le décodeur du pair le lisait
3877:     // dans le premier état du lot et décalait tout le reste de quatre octets.
3878:     let prefixe = prefixe_premix(Some(mdl), t);
3879:     let mut corps = Vec::with_capacity(prefixe.len() + etats.len() * 4);
3880:     corps.extend_from_slice(&prefixe);
3881:     for v in etats { corps.extend_from_slice(&v.to_le_bytes()); }
3882:     // UNE SEULE ÉCRITURE, et ce n'est pas de la cosmétique : le protocole écrivait la trame en
3883:     // DEUX fois (en-tête puis corps), donc un pas coûtait QUATRE messages sur un lien qui facture
3884:     // par message — mesuré par la pente délai → pas médian : 4,24 à 2 ms, 4,01 à 5 ms. Une trame,
3885:     // un envoi : le pas retombe à ~2 messages, soit −29 % de 
… [3120 caractères tronqués]
  ```

- **read** `{"file_path": "tools/porte-n3-cache.sh"}`
- **read** `{"file_path": "tools/toutes-les-portes.sh", "offset": 1, "limit": 90}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-n3-cache.sh</path>
<type>file</type>
<content>
1: #!/bin/bash
2: # porte-n3-cache.sh — N3.2b2 : que gagne-t-on à couper la profondeur en génération ?
3: #
4: # Le service peut calculer à profondeur 1 (`DRAVE_NATIVE_PROFONDEUR=1`) ou pleine.
5: # La porte mesure le TEMPS et la SORTIE des deux, sur un modèle à 8 blocs :
6: #   - la profondeur 1 est plus rapide ;
7: #   - elle change la génération ;
8: #   - ce n'est pas une sortie précoce gratuite : les couches sautées ne fournissent
9: #     plus leurs K/V aux jetons suivants. La porte nomme la condition, elle ne
10: #     prétend pas que le saut de calcul se transpose tel quel au cache.
11: set -u
12: cd "$(dirname "$0")/.."
13: D=${D:-./drave-core/target/release/drave}
14: PY=${PY:-/home/stephane/gpu-env/bin/python}
15: T=$(mktemp -d "${TMPDIR:-/tmp}/porte-n3-cache-XXXXXX")
16: trap 'kill ${SRV:-} 2>/dev/null; wait ${SRV:-} 2>/dev/null; rm -rf "$T"' EXIT
17: [ -x "$D" ] || { echo "  ❌ $D absent"; exit 2; }
18: "$PY" -c "import torch" 2>/dev/null || { echo "  ❌ $PY n'a pas torch"; exit 2; }
19: 
20: echo "=== 1. DRVM à 8 blocs, graine 7 ==="
21: "$PY" - "$T/m.drvm" "
… [2944 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/toutes-les-portes.sh</path>
<type>file</type>
<content>
1: #!/bin/bash
2: # toutes-les-portes.sh — LA PASSE COMPLÈTE, et l'instrument qui manquait.
3: #
4: # POURQUOI CETTE PORTE EXISTE. Le 12 octobre, `tools/porte-gain.sh` §9 exigeait un REFUS
5: # (`--attn-window` en réparti) que le v7 avait **délibérément retiré** en faisant voyager les
6: # trois réglages dans la trame (`main.rs:4432`). La porte ne pouvait donc plus passer — et
7: # personne ne l'a vu, parce que les portes étaient lancées **une par une**, à la main, quand
8: # on touchait la fonctionnalité du jour. Une porte qu'on croit verte et qui n'a pas tourné est
9: # exactement le défaut que ce dépôt traque (un drapeau inerte, une mesure qui ne mesure rien) :
10: # ici, appliqué aux instruments eux-mêmes.
11: #
12: # Ce que fait ce script, et ce qu'aucun autre ne faisait :
13: #   1. il lance **TOUTES** les `tools/porte-*.sh`, séquentiellement ;
14: #   2. il ne s'arrête PAS à la première rouge — il veut le tableau, pas la première tuile ;
15: #   3. il borne chaque porte dans le temps (`DELAI`, 1800 s par défaut) : une porte qui pend
16: #      est une porte ROU
… [3473 caractères tronqués]
  ```

- **bash** `{"command": "sed -n 1,40p tools/porte-n3-pont.sh; echo '=== PLACEMENT ==='; sed -n 1,30p tools/porte-n3-placement.sh", "description": "Read bridge and placement gate headers"}`

  ```
#!/bin/bash
# porte-n3-pont.sh — N3.4b : le PONT natif agit-il dans la génération ?
#
# Deux DRVM de mêmes poids (graine 7), sauf le pont : B a `bridge.weight` et
# `bridge.bias` mis à zéro. Si le pont est branché, la génération doit différer ;
# A deux fois doit être identique. C'est la brique « pont » de N3, dans le moteur.
set -u
cd "$(dirname "$0")/.."
D=${D:-./drave-core/target/release/drave}
PY=${PY:-/home/stephane/gpu-env/bin/python}
T=$(mktemp -d "${TMPDIR:-/tmp}/porte-n3-pont-XXXXXX")
trap 'rm -rf "$T"' EXIT
[ -x "$D" ] || { echo "  ❌ $D absent"; exit 2; }
"$PY" -c "import torch" 2>/dev/null || { echo "  ❌ $PY n'a pas torch"; exit 2; }

echo "=== 1. deux DRVM, mêmes poids, pont nul dans B ==="
"$PY" - "$T" <<'PY' || exit 2
import sys, torch
sys.path.insert(0, ".")
from tools.native_model import NativeConfig, NativeModel, exporter_drvm
base = dict(vocab=256, d_model=64, n_blocks=4, n_heads=4, expert_hidden=32,
            n_experts=4, top_k=2, kwta=0.5, window=32, max_pos=2048,
            thought_steps=1, early_blocks=(1,), rsn_dim=8)
torch.manual_seed(7); a = NativeModel(NativeConfig(**base))
torch.manual_seed(7); b = NativeModel(NativeConfig(**base))
zero = 0
for nom, p 
… [2121 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn 'drvm' tools/*.sh | grep -v 'porte-n3-' | head -20; echo ---; ls drave-core/tests/fixtures/ 2>/dev/null | head", "description": "Find other DRVM scripts and fixtures"}`

  ```
---
tiny_n0.drvm
  ```

- **bash** `{"command": "sed -n 1,40p drave-core/Cargo.toml; echo ---; grep -n '^mod \\|^pub mod ' drave-core/src/main.rs | head -30", "description": "Check crate config and module declarations"}`

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
66:mod clusters;
67:mod kimi_k3;
68:mod drvm;
69:mod native;
70:mod engine;
71:mod engram;
72:mod formats;
73:mod gguf;
74:mod list;
75:mod materiel;
76:mod model;
77:mod gpu;
78:mod placement;
79:mod tokenizer;
80:mod topologie;
81:mod trace_globale;
82:mod episodique;
83:mod bus;
8384:mod tests_niveaux {
8405:mod tests_flux {
8477:mod tests_plafond {
8745:mod tests_vars {
  ```

- **bash** `{"command": "grep -rn 'cargo test\\|cargo build' docs/methode/portes.md AGENTS.md tools/porte-n3-*.sh 2>/dev/null | head; echo ---; sed -n 1,40p docs/methode/portes.md", "description": "Check build/test commands conventions"}`

  ```
---
# Les portes : lancer, lire le verdict, ne pas se tromper de rouge

> Document de tâche, chargé depuis [`AGENTS.md`](../../AGENTS.md). À lire **avant de lancer ou de lire les portes**.

## La commande

```bash
bash tools/toutes-les-portes.sh
```

Elle lance **toutes** les `tools/porte-*.sh`, séquentiellement, **sans s'arrêter à la première rouge** (on veut le
tableau, pas la première tuile), et borne **chaque** porte à `DELAI=1800` s. Durée observée d'une passe complète :
**1 h 30 – 2 h** sur Hauru (**49 portes** ; certaines entraînent de petits modèles, d'autres utilisent les GPU ;
`porte-deepseek` est **hors réseau** et rapide). La dernière passe complète à **49 portes** (28/10 00 h 12) a donné
**46 vertes, 3 rouges** ; la liste et le diagnostic sont dans
[`references-non-regression.md`](../pilotage/references-non-regression.md). `porte-deepseek` est **incluse** et verte.

## Où est le registre (et comment lire le verdict)

Le registre n'est **pas** à la racine : il est écrit dans le dossier des journaux, par défaut
`/tmp/portes-<date>-<heure>/registre.txt` (variable `JOURNAUX`). Chaque ligne vaut :

```
nom-de-la-porte   code-de-sortie   durée-en-secondes
```

On lit le verd
… [595 caractères tronqués]
  ```

- **bash** `{"command": "ls -la drave-core/target/release/drave 2>/dev/null; ./drave-core/target/release/drave --drvm-inspect drave-core/tests/fixtures/tiny_n0.drvm 2>&1 | head -25", "description": "Inspect tiny fixture header"}`

  ```
-rwxr-xr-x. 2 stephane stephane 3147456 29 oct 22:27 drave-core/target/release/drave
DRVM v0 · 6 blocs · 30 tenseurs · payload 31488 o
  bloc input        input
  bloc b0           local_mixer
  bloc early0       early_head
  bloc bridge       bridge
  bloc thought      thought
  bloc output       output
  tenseur blocks.0.ffn.down.bias   bloc b0         32 o  f32
  tenseur blocks.0.ffn.down.weight bloc b0         256 o  f32
  tenseur blocks.0.ffn.gate.bias   bloc b0         32 o  f32
  tenseur blocks.0.ffn.gate.weight bloc b0         256 o  f32
  tenseur blocks.0.ffn.router.bias bloc b0         8 o  f32
  tenseur blocks.0.ffn.router.weight bloc b0         64 o  f32
  tenseur blocks.0.ffn.up.bias     bloc b0         32 o  f32
  tenseur blocks.0.ffn.up.weight   bloc b0         256 o  f32
  tenseur blocks.0.ln1.bias        bloc b0         32 o  f32
  tenseur blocks.0.ln1.weight      bloc b0         32 o  f32
  tenseur blocks.0.ln2.bias        bloc b0         32 o  f32
  tenseur blocks.0.ln2.weight      bloc b0         32 o  f32
  tenseur blocks.0.out.bias        bloc b0         32 o  f32
  tenseur blocks.0.out.weight      bloc b0         256 o  f32
  tenseur blocks.0.qkv.bias        
… [210 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\nF=drave-core/tests/fixtures/tiny_n0.drvm\necho \"--- cached ---\"; ./drave-core/target/release/drave --drvm-generate $F abc 8 2>/dev/null | xxd | head -2\necho \"--- cacheless ---\"; ./drave-core/target/release/drave --drvm-generate-fu … [328 caractères tronqués]`

  ```
--- cached ---
00000000: 6162 634f efbf bdef bfbd 5252 526f efbf  abcO......RRRo..
00000010: bd                                       .
--- cacheless ---
00000000: 6162 634f efbf bdef bfbd 5252 526f efbf  abcO......RRRo..
00000010: bd                                       .
--- forward ---
DRVM natif · prompt "abc" · 3 octets
  octet  79 'O' · logit 1.2928
  octet   8 '\u{8}' · logit 1.2371
  octet 165 '¥' · logit 1.2361
  octet   2 '\u{2}' · logit 1.1282
  octet 209 'Ñ' · logit 1.1039
--- ppl ---
[stderr]

thread 'main' (1436689) panicked at src/native.rs:236:61:
index out of bounds: the len is 256 but the index is 256
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
[killed by signal: SIGABRT]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\npython3 - <<'PY'\nimport json,struct\nb=open('drave-core/tests/fixtures/tiny_n0.drvm','rb').read()\nhsize=struct.unpack_from('<H',b,6)[0]; mlen=struct.unpack_from('<I',b,8)[0]\nm=json.loads(b[hsize:hsize+mlen])\nprint(json.dumps(m['mod … [214 caractères tronqués]`

  ```
{
 "d_model": 8,
 "early_blocks": [
  0
 ],
 "expert_hidden": 4,
 "kind": "drave-n0",
 "kwta": 0.5,
 "n_blocks": 1,
 "n_experts": 2,
 "n_heads": 2,
 "thought_steps": 1,
 "top_k": 1,
 "vocab": 256,
 "window": 8
}
tensors: [('embed.weight', 8192), ('pos.weight', 1024)]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; ls drave-core/target/debug/drave 2>/dev/null && ./drave-core/target/debug/drave --drvm-generate drave-core/tests/fixtures/tiny_n0.drvm abc 4 2>&1 | head -5", "description": "Check debug build for overflow behavior"}`

  ```
(no output)
[exit code: 2]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; grep -rn 'native::\\|Cache' drave-core/src/main.rs | head -20; echo ---; grep -rn 'DRAVE_NATIVE_PROFONDEUR' --include=*.rs --include=*.sh --include=*.md . | head", "description": "Find Cache and native API usages"}`

  ```
173:        if let Err(e) = native::servir(&f, port) { eprintln!("serveur : {e}"); std::process::exit(3); }
185:        let nat = native::Native::open(&d).expect("natif");
195:        let nat = native::Native::open(&d).expect("natif");
207:        let nat = match native::Native::open(&d) { Ok(n)=>n, Err(e)=>{eprintln!("{e}"); std::process::exit(3);} };
218:        let n = native::Native::open(&d).expect("natif");
229:        let n = match native::Native::open(&d) { Ok(n)=>n, Err(e)=>{eprintln!("{e}"); std::process::exit(3);} };
4449:                    // son contexte, `KvCache::assurer` ne peut pas agrandir et
5505:    let mut cache = model::KvCache::new(bits, n_kv, n, hd);
6105:    use crate::model::{KvCache, Model};
6124:    // 1. Cache CPU d'UNE couche, rempli de façon déterministe.
6125:    let mut cache = KvCache::new(bits, n_kv, n, hd);
8665:    /// Le livelock du contexte : `KvCache::assurer(besoin)` avec `besoin > ctx`
8670:        let mut c = model::KvCache::new(32, 2, 16, 8);   // ctx = 16 positions
8679:        let mut grand = model::KvCache::new(32, 2, 4096, 8);
8687:        let mut c2 = model::KvCache::new(32, 2, 4, 8);
---
./reports/rapport-n3.2b0-profondeur.md:4:> s
… [1384 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core && timeout 280 cargo build 2>&1 | tail -5", "description": "Build debug binary to verify overflow", "run_in_background": true}`

  ```
started background job bash-785
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; grep -n 'N3' docs/pilotage/roadmap.md | head -30", "description": "Read N3 roadmap lines"}`

  ```
53:7. **N3, R13** — les autonomes restants, qui remplissent la file « jamais en attente ».
118:| **N3** | les opérations natives : k-WTA, routes, sortie précoce, pont, rejeu, placement | 🔬 **couvert par brique** | **N3.2a/b0/b1/b2 · N3.3a/b/c · N3.4a/b/c ✅ · N3.4d couverture ✅** ; composition native complète = condition (placement distribué absent) |
251:  **N2** (la hiérarchie) ; **N4** (consigne courte) ; **N3/R13** (natif/lecteur) ;
252:  **N3** (opérations natives) ; **R13** (octets ou BPE) ; **A8.3b** (mode de lot) ;
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; ls reports/ | grep -i 'n3' | head -20", "description": "List N3 reports"}`

  ```
n3.1-etat.json
n3.2a-service.json
n3.2b0-profondeur.json
n3.2b1-seuil.json
n3.2b2-cache.json
n3.3a-routes.json
n3.3b-sparsite.json
n3.3c-sparsite-compte.json
n3.4a-composition.json
n3.4b-pont.json
n3.4c-placement.json
n3.4d-couverture.json
rapport-n3.1-etat.md
rapport-n3.2a-service.md
rapport-n3.2b0-profondeur.md
rapport-n3.2b1-seuil.md
rapport-n3.2b2-cache.md
rapport-n3.3a-routes.md
rapport-n3.3b-sparsite.md
rapport-n3.3c-sparsite-compte.md
  ```

### 👤 Utilisateur

background job bash-785 (bash: cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core && timeout 280 cargo build 2>&1 | tail -5) finished [status: completed, exit code: 0]. Read its output with job_output.

- **job_output** `{"job_id": "bash-785"}`

  ```
|
     = note: `#[warn(non_shorthand_field_patterns)]` on by default

warning: `drave-core` (bin "drave") generated 74 warnings (run `cargo fix --bin "drave" -p drave-core` to apply 30 suggestions)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 9.24s
[status: completed, exit code: 0]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet; ./drave-core/target/debug/drave --drvm-generate drave-core/tests/fixtures/tiny_n0.drvm abc 4 2>&1 | head -6; echo \"code=${PIPESTATUS[0]}\"", "description": "Run debug binary to observe overflow"}`

  ```
thread 'main' (1501272) panicked at src/native.rs:270:21:
attempt to subtract with overflow
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
code=101
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core && timeout 200 cargo test --bin drave native::tests 2>&1 | tail -15", "description": "Run the native fixture unit test"}`

  ```
failures:

---- native::tests::execute_une_petite_fixture_drvm stdout ----

thread 'native::tests::execute_une_petite_fixture_drvm' (1503682) panicked at src/native.rs:186:21:
attempt to subtract with overflow
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace


failures:
    native::tests::execute_une_petite_fixture_drvm

test result: FAILED. 0 passed; 1 failed; 0 ignored; 0 measured; 134 filtered out; finished in 0.00s

error: test failed, to rerun pass `--bin drave`
  ```

### 🤖 Assistant

⏵ Vérification des deux défauts latents, puis rédaction du plan

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet\necho \"== A) underflow (debug) ==\"; ./drave-core/target/debug/drave --drvm-generate drave-core/tests/fixtures/tiny_n0.drvm abc 4 2>&1 | head -2\necho \"== B) max_pos codé en dur ==\"; ./drave-core/target/release/drave --drvm-native-pp … [328 caractères tronqués]`

  ```
== A) underflow (debug) ==

thread 'main' (1535986) panicked at src/native.rs:270:21:
== B) max_pos codé en dur ==

thread 'main' (1535988) panicked at src/native.rs:236:61:
== C) release: pont jamais appliqué à n_blocks=1 ? ==
DRVM natif · prompt "abc" · 3 octets
  octet  79 'O' · logit 1.2928
  octet   8 '\u{8}' · logit 1.2371
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --porcelain | head -10; echo \"[fin]\"", "description": "Confirm no files modified"}`

  ```
M  docs/pilotage/en-cours.md
M  docs/pilotage/roadmap.md
MM journal/2026-10-29/README.md
D  journal/2026-10-29/attention.md
MM journal/2026-10-29/distribue.md
MM journal/2026-10-29/docs.md
MM journal/2026-10-29/memoire.md
MM journal/2026-10-29/mesures.md
MM journal/2026-10-29/modele.md
MM journal/2026-10-29/moteur.md
[fin]
  ```

### 🤖 Assistant

⏵ Rédaction du plan et envoi au parent

- **send_message** `{"agent_id": "71d57f53-8b41-4220-84dd-7bb9eedc88d9", "message": "# Plan N3.5 — DRVM en deux régions, deux processus (recherche seule, aucun fichier modifié)\n\nVérifié sur place : `cargo build` (debug) OK ; deux défauts latents **reproduits** (voir § 0) ; aucun fichier touché par moi (le `git status … [16811 caractères tronqués]`

  ```
message delivered to agent 71d57f53-8b41-4220-84dd-7bb9eedc88d9
  ```

### 🤖 Assistant

⏵ Plan livré au parent

# Plan N3.5 — DRVM en deux régions, deux processus (recherche seule, aucun fichier modifié)

Vérifié sur place : `cargo build` (debug) OK ; deux défauts latents **reproduits** ; aucun fichier touché par moi (le `git status` sale est celui de la session en cours).

## 0. Verdict

Le plus petit changement honnête n'est **pas** un nouveau format ni un découpage du DRVM : le conteneur déclare déjà `graph.regions` et chaque tenseur porte son `bloc`. C'est un **découpage à l'exécution** : extraire de `pas_profondeur` trois morceaux (`entree`, `traverser`, `tete`), exposer `pas_amont(k)` / `pas_aval(k)`, et faire traverser **le seul hidden de frontière** (d f32) par un fil TCP localhost. Le cache K/V **ne traverse pas** : chaque région garde le sien. Coût : ~500 lignes, 3 fichiers + 1 porte, 1,5–2 j.

Deux prérequis, car ils bloquent les tests unitaires que ce travail ajoute :

1. **`native.rs:186` et `:270`** — `if b == c.n_blocks / 2 - 1` **sous-déborde** quand `n_blocks == 1` (fixture `tiny_n0.drvm`, modèles 1 bloc de `porte-n3-service`). En debug : panic `attempt to subtract with overflow` (reproduit, code 101) → **`cargo test --bin drave native::tests` est déjà ROUGE aujourd'hui**. En release ça *wrap* en `usize::MAX` : le pont n'est jamais appliqué, ce que fait aussi Python (`i == -1`) → écrire `n_blocks >= 2 && b == n_blocks / 2 - 1` **ne change rien** en release, et corrige les deux endroits.
2. **`native.rs:236`** — `pos.min(2047)` code en dur la taille de `pos.weight`. La fixture a **32 positions** : `--drvm-native-ppl tiny_n0.drvm "La France est un pays de la couche"` panique `index out of bounds: len 256, index 256` (reproduit). Ajouter `max_pos` à `Cfg` (`poids["pos.weight"].len() / cfg.d`) et `pos.min(c.max_pos - 1)`.

## 1. Refactor de `native.rs` (extraction pure, ordre **verbatim**)

```rust
pub struct Cfg { /* … */ pub thought_steps: usize, pub max_pos: usize }
pub struct Native { cfg: Cfg, poids: HashMap<String, Vec<f32>>, empreinte: u64, /* … */ }

impl Native {
    /// Entrée de la région 0 : embedding + position. Seul endroit qui lit
    /// `embed.weight` et `pos.weight` — la région aval ne ré-embedde JAMAIS.
    fn entree(&self, id: u32, pos: usize) -> Vec<f32>;

    /// Traverse les blocs `blocs` (indices **ABSOLUS**) en écrivant K/V dans
    /// `cache[b]`. Ni embedding, ni tête. Le pont est appliqué à l'indice
    /// absolu `n_blocks/2 - 1` : une seule des deux régions le porte.
    fn traverser(&self, x: &mut [f32], pos: usize,
                 blocs: std::ops::Range<usize>, cache: &mut Cache);

    /// Tête terminale : `thought_steps` puis `head_byte`. Seule la DERNIÈRE
    /// région l'exécute ; `h0` est l'état APRÈS le dernier bloc.
    fn tete(&self, x: &[f32]) -> Vec<f32>;

    fn pas_profondeur(&self, id: u32, pos: usize, cache: &mut Cache, profondeur: usize) -> Vec<f32> {
        let p = profondeur.clamp(1, self.cfg.n_blocks);
        let mut x = self.entree(id, pos);
        self.traverser(&mut x, pos, 0..p, cache);
        self.tete(&x)
    }

    pub fn config(&self) -> &Cfg;
    pub fn empreinte(&self) -> u64;   // FNV-1a 64 sur les poids triés par nom

    /// Région AMONT : blocs `0..k`, rend le hidden de frontière. k == 0 est
    /// légitime (frontière = embedding) : pas de `clamp(1, …)` ici.
    pub fn pas_amont(&self, id: u32, pos: usize, cache: &mut Cache, k: usize)
        -> Result<Vec<f32>, ErreurDrvm>;

    /// Région AVAL : blocs `k..n`, puis thought et tête. Le cache doit déjà
    /// contenir exactement `pos` positions (garde-fou anti-désynchronisation).
    pub fn pas_aval(&self, frontiere: &[f32], pos: usize, cache: &mut Cache, k: usize)
        -> Result<Vec<f32>, ErreurDrvm>;
}

impl Cache {
    fn assurer(&mut self, n_blocks: usize, n_heads: usize); // remplace le `if cache.k.is_empty()`
    /// Positions déjà écrites, lues sur la 1re tête non vide (les blocs hors
    /// région restent vides) ; None = cache neuf.
    pub fn position(&self, dh: usize) -> Option<usize>;
    pub fn exiger_position(&self, dh: usize, pos: usize) -> Result<(), ErreurDrvm>;
    pub fn vider(&mut self);
    pub fn octets(&self) -> usize;
}
```

`pas_profondeur` reste privé, identique au bit près : extraction mécanique, +80 lignes nettes. Ne pas toucher `forward` (référence de `--drvm-forward` / `--drvm-sparsite`), sauf la garde du pont.

**Pourquoi `Result`** : `panic = "abort"` en release — un panic dans le serveur aval le tue sans nettoyage. La désync de cache doit être une erreur de protocole, pas un `assert`.

## 2. État transféré

| | contenu | taille / pas (d=64, vocab=256) |
|---|---|---|
| **MVP (retenu)** | `pos` + hidden de frontière `d f32`, retour `vocab f32` | 276 o montée, 1054 o descente |
| Repli F1 | hidden de frontière **de toutes les positions du préfixe** (s·d f32), aval sans état | 4·s·d o |
| Rejeté F2 | cache K/V des blocs `k..n` | 8·(n−k)·pos·d o = **19 Mo** à d=768, n−k=6, pos=512 |

F2 est rejeté **par l'arithmétique** : à `pos ≈ s`, il coûte `2(n−k)` fois F1. Aucun cache sur le fil. Format d'état : `[u32 pos][u32 d][d × f32 LE]` (24 + 4d o), utilisable pour F1 ou un rejeu hors ligne.

## 3. Protocole (TCP 127.0.0.1, en-tête texte + corps binaire LE)

```text
OUVRE <session> <k> <n> <d> <vocab> <empreinte>\r\n   →  OK <k> <n> <d> <vocab>\r\n
                                                       →  REFUS <motif>\r\n
PAS <session> <pos>\r\n<d × f32 LE>                    →  LOGITS <session> <pos> <vocab>\r\n<vocab × f32 LE>
                                                       →  REFUS <motif>\r\n
FERMER <session>\r\n                                   →  OK\r\n
```

Un `BufReader` par connexion **réutilisé** ; `read_exact` pour le corps (leçon `native.rs:406`) ; **un seul `write_all` par trame** (leçon `main.rs:3882`) ; `TCP_NODELAY`, `read_timeout(30 s)`. Une session = une connexion = un `Cache` ; **aucun retry** d'un `PAS` (l'ajout K/V n'est pas idempotent). Le serveur refuse si `(k,n,d,vocab,empreinte)` diffèrent, si `pos` ne suit pas, si un corps a la mauvaise longueur ; stdout vide (stdout du pilote = charge utile).

## 4. CLI exacte

```bash
drave --drvm-serve-aval    MODELE.drvm K PORT                  # blocs K..n
drave --drvm-generate-amont MODELE.drvm K PROMPT N [ADRESSE]   # blocs 0..K, pilote, hex sur stdout
drave --drvm-generate-split MODELE.drvm K PROMPT N             # mêmes régions, EN UN PROCESSUS
```

`ADRESSE` défaut `127.0.0.1:7101` ; `K` obligatoire (exit 2, jamais de défaut silencieux) ; sortie **hex** (échappe à l'UTF-8 lossy de `--drvm-generate`) ; codes 2 usage / 3 modèle / 4 paire. `servir()` gagne `"hex":"…"` dans `/generer` (2 lignes) : référence locale exacte de la porte.

Boucle écrite **une seule fois** avec une closure `pas(id,pos) -> logits` : split local et distribué ne diffèrent que par elle.

```rust
// native_dist.rs (nouveau, ~250 lignes)
fn boucle(mut pas: impl FnMut(u32, usize) -> Result<Vec<f32>, String>,
          cfg: &Cfg, prompt: &[u8], n: usize) -> Result<Vec<u8>, String>;
pub fn generer_split(nat: &Native, k: usize, prompt: &[u8], n: usize) -> Result<Vec<u8>, String>;
pub fn servir_aval(chemin: &str, k: usize, port: u16) -> std::io::Result<()>;
pub fn generer_amont(chemin: &str, k: usize, prompt: &[u8], n: usize, adresse: &str) -> std::io::Result<Vec<u8>>;
```

## 5. Pièges

1. **Indices absolus** : `traverser` reçoit `k..n`, teste le pont et indexe `cache[b]` en absolu. Un `b - k` relatif fait disparaître le pont ou le fait tirer deux fois, silencieusement.
2. **Sous-débordement** `n_blocks/2 - 1` (§ 0.1).
3. **Positions** : `pos` absolu depuis 0, seule chose qui relie les deux caches ; serveur redémarré à `pos > 0` → **refus**. L'aval ne ré-embedde jamais (double `pe`).
4. **`max_pos` en dur** (§ 0.2).
5. **`DRAVE_NATIVE_PROFONDEUR`** : le split ne passe pas par `pas`, et les 3 modes **refusent** si la variable est posée.
6. **`thought_steps`/tête** : `pas_profondeur` les applique à *chaque* appel, même à profondeur k. Une seule fois, dans la dernière région, `h0` = après le dernier bloc.
7. **Cache, double ajout** : le code suppose exactement `pos` entrées ; deux `PAS` à la même position corrompent en silence → `exiger_position`, un cache par connexion.
8. **Tête perdue / repli silencieux** : aval absent ⇒ échec, stdout vide, jamais de génération locale plausible.
9. **Pont** : à `n_blocks=4`, l'indice 1 est en fin d'amont pour K=2 et en début d'aval pour K=1 : tester les deux.
10. **`early_blocks`/`local_heads`** : non exécutés par `Native` ; une future tête précoce devra vivre dans sa région.
11. **Fil** : `BufReader` réutilisé, `read_exact`, un `write_all`, bannière avant connexion, 127.0.0.1 seul (pas d'auth : ce n'est pas une frontière de sécurité).
12. **`vocab > 256`** : `generer` fait `i as u8` ; garder 256 et refuser un vocabulaire différent entre les deux bouts.
13. **`panic = "abort"`** : EOF = « session rompue », pas de réponse tronquée.
14. **Honnêteté** : les deux processus chargent tous les poids — partage de *calcul*, pas de mémoire ; calcul total identique.

## 6. Complexité et fichiers

| lot | contenu | lignes | risque | durée |
|---|---|---|---|---|
| P0 | garde pont (×2), `max_pos` | ~8 | très bas | 0,5 h |
| P1 | `entree`/`traverser`/`tete`, `Cache`, `pas_amont`/`pas_aval`, `config`, `empreinte` | ~+120 `native.rs` | bas | 2–3 h |
| P2 | `--drvm-generate-split` + test bit-exact | ~35 | bas | 1 h |
| P3 | `native_dist.rs` | ~250 | moyen (fil/désync) | 3–4 h |
| P4 | 2 modes CLI + `"hex"` + usage | ~57 | bas | 1 h |
| P5 | `tools/porte-n3-deux-regions.sh` | ~120 | bas | 1,5 h |

Fichiers : `native.rs`, **`native_dist.rs`** (nouveau, `mod native_dist;`), `main.rs`, `tools/porte-n3-deux-regions.sh` (découverte automatique par `ls tools/porte-*.sh`, aucun registre à éditer). À la clôture seulement : fiche + JSON, journal, `en-cours`, `roadmap` (la ligne N3 dit « placement distribué absent » : c'est ce que N3.5 ferme).

## 7. Repli

Le MVP ne transfère **aucun** cache ; le repli est « plus d'état persistant du tout » :

- **F1 — rejeu du préfixe sans cache** : l'amont envoie les hiddens de frontière de toutes les positions, l'aval rejoue `k..n` avec un cache neuf. Exact par construction, 4·s·d o/pas, O(s²). Repli recommandé : aucune classe de bug d'alignement.
- **F3 — fenêtre** : `debut = pos.saturating_sub((n−k)·window − 1)`, exact mais à prouver.
- F2 (cache K/V) : le pire des trois en octets, ne pas l'implémenter.

## 8. Tests et contrôles négatifs

```bash
cd drave-core && cargo build --release
cargo test --bin drave native::        # ROUGE aujourd'hui (underflow) ; vert après P0
cargo test --bin drave native_dist::
bash tools/porte-n3-deux-regions.sh
PORTES="n3" bash tools/toutes-les-portes.sh
```

Test unitaire bit-exact :

```rust
for k in 0..=n.config().n_blocks {
    let (mut ca, mut cv, mut cp) = (Cache::default(), Cache::default(), Cache::default());
    for pos in 0..6 {
        let id = b"abcdef"[pos] as u32;
        let attendu = n.pas(id, pos, &mut cp);
        let h = n.pas_amont(id, pos, &mut ca, k)?;
        assert_eq!(attendu, n.pas_aval(&h, pos, &mut cv, k)?, "k={k} pos={pos}");
    }
}
```

Porte (modèle **4 blocs**, d=64, vocab=256, window=32, thought_steps=1, graine 7, « abc », n=12) :

1. Référence locale : `--drvm-serve`, `/generer?n=12` → `hex` **H0**.
2. Balayage **K = 0,1,2,3,4** (`--drvm-generate-split`) : les 5 valent H0 (K=1 met le pont dans l'aval, K=2 dans l'amont).
3. Paire réelle K=1 puis K=2 → hex == H0.
4. **Tête vivante** : modèle C `thought.*`+`thought_in.*` nuls ⇒ `tanh(0)=0`, sortie locale **indépendante du prompt** (`abc` == `zzz`), et le split reproduit le même hex — seul contrôle qui attrape une extraction perdant `tete` (aucune porte existante ne couvre thought).
5. **Refus** aval sur B (mêmes formes, pont nul) → empreinte.
6. **Refus** K désaccordé.
7. **Refus** pair absent (port du serveur juste tué) : exit ≠ 0, **stdout vide**.
8. **Refus** `DRAVE_NATIVE_PROFONDEUR=1`.
9. Stats + `PORTE TENUE`.

Option : committer une fixture **4 blocs** (~50 Ko, d=16) pour que `cargo test` couvre le pont hors des portes.

## 9. Ce que la fiche devra dire

Deux processus, deux régions de **calcul**, poids entiers des deux côtés ; 276 o + 1054 o par pas sur localhost ; sortie **bit-identique** au modèle plein (pas « proche ») ; le cache K/V ne traverse pas et pourquoi ; les 4 refus comme contrôle négatif. Ligne : **N3.5**.

Rien n'a été modifié : ni `en-cours`, ni `roadmap`, ni `AGENTS`, aucun commit.

