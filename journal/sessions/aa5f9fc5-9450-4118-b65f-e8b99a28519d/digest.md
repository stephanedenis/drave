# Session DSH — relecture

- identifiant : `aa5f9fc5-9450-4118-b65f-e8b99a28519d`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-09-30 15:07:58
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu es vérificateur de documentation dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave » : moteur d'inférence LLM en Rust, `std` seul, binaire `drave`). Tout est en FRANÇAIS : écris en français.

CONTEXTE : la journée a produit ~50 commits qui ont changé beaucoup de choses : protocole de flux passé en **version 4** (en-tête de **79 octets**, quatre modes : dense, listes, blocs, lot), format de trace disque en **v2** (défaut, indices par écarts, sans perte) et **v3** (`DRAVE_TRACE_BLOCS=1`, avec perte), tableau de bord `--options-actives`, plafond réseau R4 (256 Mo), nouvelle variable `DRAVE_KV_K_F16=1`, et une campagne de mesures du cache KV (rapport `reports/rapport-placement-bits-kv.md`). Un audit de cohérence a déjà été fait en début d'après-midi (`reports/rapport-coherence-docs.md`) et corrigé — mais les corrections et les nouveaux documents ont pu créer de NOUVELLES incohérences.

TA MISSION : produire `reports/rapport-coherence-docs-2.md`, un second passage qui vérifie **l'état APRÈS** les changements du jour.

Méthode (la même que l'audit précédent, dont tu peux lire le rapport pour la forme) :
1. Vérifie contre le CODE (`grep`, lecture) les affirmations chiffrées et les noms : versions (`VERSION_FLUX` dans `main.rs`, la version écrite par `TraceFlux::nouveau` dans `model.rs`), taille d'en-tête (`TAILLE_TETE`), modes et sémantique de `n` par mode, variables d'environnement (chaque `DRAVE_*` du code est-il documenté ? chaque `DRAVE_*` documenté existe-t-il ?), drapeaux (`--options-actives`, `--lot`, `--flux-liste`, `--flux-blocs`…).
2. Vérifie les CHIFFRES publiés dans les documents de référence (`README.md`, `REPRISE.md`, `docs/*.md`) contre les rapports qui les portent (`reports/*.md`) : les octets par flux, les tailles de trace, les perplexités de référence, les pourcentages du cache KV, les accélérations. Un chiffre cité dans deux documents avec deux valeurs différentes est un défaut.
3. Vérifie les RENVOIS : chaque `[texte](chemin)` vers un fichier existant, et chaque rapport cité existe.
4. Cherche les affirmations « vérifié » ou « mesuré » qui ne sont plus vraies, et les sections qui décrivent un travail « à faire » alors qu'il est fait (ou l'inverse).
5. Signale aussi les **manques** : une chose du code que les documents ignorent.

LIVRABLE : `reports/rapport-coherence-docs-2.md`, en français, avec un tableau `| document | affirmation | ce que dit le code/la mesure | verdict |` (verdicts : PÉRIMÉ, CONTRADICTOIRE, MANQUANT, OK), puis la liste ordonnée des corrections à faire — **sans les appliquer** (un autre agent s'en chargera). Termine par un résumé de 10 lignes.

INTERDIT : modifier un autre fichier que ton rapport. Pas de `cargo build`. Les exécutions du moteur sont interdites en mode serveur (`--flux-serveur`, `--ppl-reparti`) ; les commandes courtes (`grep`, `ls`, `python3`, et au plus deux exécutions `--limit 4`) sont autorisées. **Une campagne de mesure tourne** (`pgrep -x drave`) : ne lance rien qui prenne plus de 30 secondes de CPU.
Your parent agent id is "bbd6969f-0f70-42b2-8951-64d1f2f36d2e". Before you finish, send your result to that agent with send_message({ agent_id: "bbd6969f-0f70-42b2-8951-64d1f2f36d2e", message: "<self-contained result>" }). The parent shares your workspace but does not automatically receive your transcript, tool output, or reasoning. Send earlier messages as well when a finding changes what the parent should do next; sending a message does not end your turn.

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

⏵ Je commence par explorer le dépôt et lire l'audit précédent.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la && echo \"---DOCS---\" && ls -la docs/ 2>/dev/null && echo \"---REPORTS---\" && ls -la reports/ 2>/dev/null", "description": "List repo, docs and reports directories"}`

  ```
total 220
drwxr-xr-x. 1 stephane stephane   598 30 sep 12:19 .
drwxr-xr-x. 1 stephane stephane  2350 25 sep 11:55 ..
drwxr-xr-x. 1 stephane stephane    40 25 sep 15:38 bench
drwxr-xr-x. 1 stephane stephane    56 30 sep 12:20 colab
drwxr-xr-x. 1 stephane stephane    52 25 sep 17:53 data
drwxr-xr-x. 1 stephane stephane   394 30 sep 11:53 docs
drwxr-xr-x. 1 stephane stephane    82 28 sep 11:58 drave-core
drwxr-xr-x. 1 stephane stephane   146 30 sep 14:10 .git
-rw-r--r--. 1 stephane stephane   399 30 sep 10:01 .gitignore
drwxr-xr-x. 1 stephane stephane    34 27 sep 11:39 journal
drwxr-xr-x. 1 stephane stephane    88 25 sep 17:13 models
drwxr-xr-x. 1 stephane stephane   114 25 sep 15:24 __pycache__
-rw-r--r--. 1 stephane stephane  4992 25 sep 10:54 Qtrinet-bootstrap.md
-rw-------. 1 stephane stephane 26857 30 sep 13:08 README.md
drwxr-xr-x. 1 stephane stephane  1902 30 sep 13:13 reports
-rw-------. 1 stephane stephane 36993 30 sep 14:09 REPRISE.md
-rw-------. 1 stephane stephane  8566 30 sep 08:44 run_8bit_perfection.py
-rw-------. 1 stephane stephane 10507 30 sep 08:44 run_clusters.py
-rw-------. 1 stephane stephane 12507 30 sep 08:44 run_cpu.py
-rw-------. 1 stephane stephane 11462 30
… [4730 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && pgrep -x drave | head; echo \"---\"; ls src/ 2>/dev/null | head -50", "description": "Check for running drave and list sources"}`

  ```
654414
---
bpe_np.py
encoding.py
gguf_min.py
__pycache__
roofline.py
sparsity.py
ternary.py
tiny_model.py
transformer_np.py
  ```

### 🤖 Assistant

⏵ Je localise le code Rust et lis l'audit de cohérence précédent.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && find . -name \"*.rs\" -not -path \"./.git/*\" | head -50; echo \"---\"; ls -la drave-core/ 2>/dev/null; echo \"---git log---\"; git log --oneline -60 2>/dev/null | head -70", "description": "Find Rust sources and recent git log"}`

  ```
./drave-core/src/list.rs
./drave-core/src/tokenizer.rs
./drave-core/src/gpu.rs
./drave-core/src/gguf.rs
./drave-core/src/engine.rs
./drave-core/src/main.rs
./drave-core/src/model.rs
---
total 16
drwxr-xr-x. 1 stephane stephane   82 28 sep 11:58 .
drwxr-xr-x. 1 stephane stephane  598 30 sep 12:19 ..
-rw-r--r--. 1 stephane stephane  154 30 sep 08:44 Cargo.lock
-rw-r--r--. 1 stephane stephane  375 30 sep 08:44 Cargo.toml
drwxr-xr-x. 1 stephane stephane   94 30 sep 08:44 gpu
-rw-r--r--. 1 stephane stephane 4351 30 sep 08:44 README.md
drwxr-xr-x. 1 stephane stephane  112 30 sep 11:13 src
drwxr-xr-x. 1 stephane stephane   70 25 sep 18:32 target
---git log---
6c1aecf REPRISE : la frontière du cache KV et les deux gains du mode lot
0fb9c93 Dernières mesures : clés f16 + valeurs int4, et le mode lot 7× plus rapide par jeton
fcda4ff Tests de trame forgée : un délai de lecture, pour qu'ils échouent au lieu de pendre
dc8a193 Feuille de route : les clés f16 mesurées (+0,018 % pour 39 % de la taille du f32)
528639c Cache KV : les clés en f16 sont le meilleur réglage mesuré (+0,018 % pour 39 % de la taille)
e092c0e Handoff et index : la seconde relecture, et treize tests
25cfe12 Deux tests de plu
… [4213 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && wc -l reports/rapport-coherence-docs.md && head -120 reports/rapport-coherence-docs.md", "description": "Read start of previous coherence report"}`

  ```
229 reports/rapport-coherence-docs.md
# Cohérence des documents avec le code — audit

**En une ligne** : **80 affirmations** vérifiées une par une contre le code (et
contre les traces réelles du disque) ; **38 sont fausses (PÉRIMÉ)**, **15 se
contredisent entre documents (CONTRADICTOIRE)**, **10 existent dans le code et
manquent aux documents (MANQUANT)**, **17 tiennent (OK)** — les trois plus graves
touchent la **version du protocole de flux** (deux binaires « v3 » aux contrats
différents se croient compatibles), un **échappement d'indice écrit sur 4 octets et
lu sur 2** en mode blocs, et `REPRISE.md` §6bis (pourtant écrit il y a une heure)
déjà faux sur quatre points.

## Révision auditée, méthode, réserves

| | |
|---|---|
| Commit de référence | `ae85043` (2026-09-30 12:30) |
| `drave-core/src/main.rs` | sha256 `d5e90136…` · 3 112 lignes |
| `drave-core/src/model.rs` | sha256 `3e5dde2d…` · 3 872 lignes |
| Traces relues | `/tmp/flux_v2.bin` (66 370 408 o, en-tête `DRVF` version **2**), `/tmp/flux_v3.bin` (version **3**) |

Deux réserves de méthode, parce qu'elles changent la portée des constats :

1. **L'arbre de travail a bougé pendant l'audit.** Quand il a commencé, HEAD étai
… [13436 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je lis la fin de l'audit précédent et l'état git actuel.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '120,229p' reports/rapport-coherence-docs.md", "description": "Read rest of previous audit report"}`

  ```
| # | document | affirmation | ce que dit le code / la mesure | verdict |
|---|---|---|---|---|
| 57 | `REPRISE.md:298-300` (§6bis, chantier 1) | « Préremplissage par LOTS sur le fil : le vrai bloqueur » | fait et mesuré au commit `cda3162` (12:02), **23 minutes après** l'écriture de §6bis | PÉRIMÉ |
| 58 | `REPRISE.md:304-306` (§6bis, chantier 3) | « l'écart **croît** avec la longueur : chercher pourquoi » | le commit `976cb81` et `rapport-transport-liste.md:141-152` : il **décroît** (1,37e-1 à 64 → 1,32e-2 à 1 024) | PÉRIMÉ |
| 59 | `docs/colab-reparti.md:28,32` | « préremplissage par lots sur le fil : ❌ un flux par jeton aujourd'hui », « le chantier suivant » | `MODE_LOT`, `envoyer_lot`, `--lot T` sont dans le code, et le document a été retouché à 12:20, **18 minutes après** la phase 3.4 | PÉRIMÉ |
| 60 | `reports/rapport-phase3-reparti.md:61-64` | « c'est le prochain chantier (3.2) : faire voyager la LISTE » | fait : `--flux-liste`, `--flux-blocs`, 3 623 → 1 568 octets (`cb37c83`, `af18f29`) | PÉRIMÉ |
| 61 | `docs/colab-reparti.md:103` | « `--flux-blocs --act-thresh 0.02` (÷2 sur le fil pour **0,2 %**) » | le rapport que ce document cite réfute explicitement cette formulation 
… [10384 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git status --porcelain && echo \"---HEAD---\" && git log -1 --format='%H %ad %s' --date=iso && echo \"---counts---\" && wc -l drave-core/src/*.rs", "description": "Check git status and Rust line counts"}`

  ```
M journal/README.md
 M journal/sessions/MANIFEST.md
 M journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md
 M journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md
---HEAD---
6c1aecf2fb92eafd4b6faa9eb4010f395c7222f2 2026-09-30 14:09:49 -0400 REPRISE : la frontière du cache KV et les deux gains du mode lot
---counts---
   976 drave-core/src/engine.rs
   721 drave-core/src/gguf.rs
   821 drave-core/src/gpu.rs
  1440 drave-core/src/list.rs
  3508 drave-core/src/main.rs
  3928 drave-core/src/model.rs
   507 drave-core/src/tokenizer.rs
 11901 total
  ```

### 🤖 Assistant

⏵ J'extrais les faits du code : version, en-tête, modes, variables et drapeaux.

- **todo_write** `{"todos": [{"content": "Extraire les faits du code (VERSION_FLUX, TAILLE_TETE, modes, DRAVE_*, drapeaux)", "status": "in_progress"}, {"content": "Vérifier versions & en-tête dans README/REPRISE/docs", "status": "pending"}, {"content": "Croiser les chiffres publiés avec les rapports (octets, traces,  … [341 caractères tronqués]`

  ```
Updated todo list: 5 pending, 1 in progress, 0 completed.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src && grep -n \"VERSION_FLUX\\|TAILLE_TETE\\|MODE_LOT\\|MODE_LISTE\\|MODE_BLOCS\\|MODE_DENSE\\|const MODE\" main.rs | head -60", "description": "Grep protocol constants in main.rs"}`

  ```
1376:const VERSION_FLUX: u8 = 4;
1378:const MODE_DENSE: u8 = 0;
1382:const MODE_LISTE: u8 = 1;
1387:const MODE_BLOCS: u8 = 2;
1393:const MODE_LOT: u8 = 3;
1404:const TAILLE_TETE: usize = 4 + 1 + 1 + 4 + 4 + 4 + 4 + 4 + 4 + 4 + 4 + 1
1609:    let (n, echelle, corps): (usize, f32, Vec<u8>) = if mode == MODE_BLOCS {
1627:    } else if mode == MODE_LISTE {
1641:    let mut tete = Vec::with_capacity(TAILLE_TETE);
1643:    tete.push(VERSION_FLUX);
1658:    assert_eq!(tete.len(), TAILLE_TETE,
1659:               "en-tête de flux de {} octets pour {TAILLE_TETE}", tete.len());
1663:    Ok((TAILLE_TETE + corps.len(), n))
1675:    let mut tete = Vec::with_capacity(TAILLE_TETE);
1677:    tete.push(VERSION_FLUX);
1678:    tete.push(MODE_LOT);
1696:    assert_eq!(tete.len(), TAILLE_TETE,
1697:               "en-tête de lot de {} octets pour {TAILLE_TETE}", tete.len());
1703:    Ok(TAILLE_TETE + corps.len())
1709:    let mut tete = [0u8; TAILLE_TETE];
1718:    if version != VERSION_FLUX {
1721:            format!("flux en version {version}, cette build parle la {VERSION_FLUX} \
1740:        MODE_LOT => {
1753:        MODE_BLOCS => {
1787:        MODE_DENSE => ChargeFlux::Dense((0..n).map(|k| f32:
… [1301 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je lis le bloc de constantes et les décodeurs du protocole.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs", "offset": 1370, "limit": 80}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
1370: /// les niveaux et le seuil, dont le correctif était resté incomplet.
1371: ///
1372: /// Version 3 : ajoute le mode LOT. Le passage à 3 n'est pas cosmétique — un pair
1373: /// en version 2 lirait `n × 4` octets d'un corps qui en fait `n × hidden × 4`,
1374: /// se désynchroniserait, puis dirait « mode inconnu » : un refus exact mais tardif
1375: /// et muet sur la cause. Ici il est immédiat et nommé.
1376: const VERSION_FLUX: u8 = 4;
1377: /// Vecteur dense en f32 : 4 octets par canal, toute la dimension.
1378: const MODE_DENSE: u8 = 0;
1379: /// LISTE creuse quantifiée : indice u16 + valeur i16, plus une échelle. C'est le
1380: /// même encodage que la trace sur le disque — la mise en réseau ne réinvente
1381: /// rien, elle réutilise le format de la phase 0.
1382: const MODE_LISTE: u8 = 1;
1383: /// LISTE à **échelle par bloc de 32 canaux** : indice u16, valeur i8, et une
1384: /// échelle f32 par bloc — 3 octets par neurone actif au lieu de 4, avec une
1385: /// erreur relative bornée DANS le bloc (le résidu brut a une dynamique trop
1386: /// large pour une éc
… [3169 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src && grep -n \"DRAVE_[A-Z0-9_]*\" -o main.rs model.rs engine.rs list.rs gpu.rs gguf.rs tokenizer.rs | sed 's/.*://' | sort -u", "description": "List all DRAVE_ env vars in code"}`

  ```
DRAVE_
DRAVE_BANC_KV_DEBUG
DRAVE_BANC_KV_GPU_SEUL
DRAVE_BANC_KV_GRAD
DRAVE_BANC_KV_K0
DRAVE_BANC_KV_KUNIT
DRAVE_BANC_KV_UNIT
DRAVE_BANC_KV_V1
DRAVE_DEBUG_FLUX
DRAVE_FLUX_VERIF
DRAVE_GPU
DRAVE_GPU_EXPERTS
DRAVE_GPU_EXPERTS_GO
DRAVE_GPU_KV
DRAVE_GPU_TETE
DRAVE_HARMONY_TRACE
DRAVE_KV_BITS
DRAVE_KV_F16
DRAVE_KV_K_F16
DRAVE_KV_K_F32
DRAVE_KV_V_F32
DRAVE_Q8_BLOCS
DRAVE_SANS_EMPRUNT
DRAVE_TRACE_BLOCS
DRAVE_VISION_TEXTE
DRAVE_YARN
DRAVE_YARN_MSCALE
DRAVE_YARN_NON
DRAVE_YARN_RAMPE
  ```

### 🤖 Assistant

⏵ Je détaille l'usage des variables d'environnement et des drapeaux CLI.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src && grep -n 'DRAVE_' main.rs model.rs engine.rs | grep -v '^\\s*//' | head -80", "description": "Show DRAVE_ env var usages with context"}`

  ```
main.rs:38:    // Les variables d'environnement ont été renommées QT_* -> DRAVE_* : un
main.rs:43:elles s'appellent maintenant DRAVE_* (voir docs/histoire.md). Rien n'a été appliqué.");
main.rs:1290:    // `DRAVE_VISION_TEXTE=<modele.gguf>` charge le modèle de texte et lui impose le
main.rs:1299:        let chemin = std::env::var("DRAVE_VISION_TEXTE").unwrap_or_default();
main.rs:1866:                    if std::env::var("DRAVE_DEBUG_FLUX").is_ok() {
main.rs:2171:    let bits = std::env::var("DRAVE_KV_BITS").ok().and_then(|v| v.parse().ok()).unwrap_or(32u32);
main.rs:2188:    let k_nul = std::env::var("DRAVE_BANC_KV_K0").is_ok();
main.rs:2189:    let v_un = std::env::var("DRAVE_BANC_KV_V1").is_ok();
main.rs:2193:    let v_unitaire = std::env::var("DRAVE_BANC_KV_UNIT").is_ok();
main.rs:2198:    let pente = std::env::var("DRAVE_BANC_KV_GRAD").is_ok();
main.rs:2201:    let k_unitaire = std::env::var("DRAVE_BANC_KV_KUNIT").is_ok();
main.rs:2227:    //    `DRAVE_BANC_KV_GPU_SEUL=1` la saute : à 1 M de clés elle coûte 3 à 16
main.rs:2229:    let gpu_seul = std::env::var("DRAVE_BANC_KV_GPU_SEUL").is_ok();
main.rs:2269:        println!("  CPU non mesuré (DRAVE_BANC_KV_GPU_SEUL) · {:.2} Go 
… [3840 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src && grep -n 'options-actives\\|options_strict\\|options-actives-strict\\|\"--lot\"\\|\"--flux-liste\"\\|\"--flux-blocs\"\\|\"--flux-serveur\"\\|\"--ppl-reparti\"' main.rs | head -40", "description": "Grep CLI flags in main … [5 caractères tronqués]`

  ```
51:        (opt.flux_serveur.is_some(), "--flux-serveur"),
52:        (opt.ppl_reparti.is_some(), "--ppl-reparti"),
340:/// **Tableau de bord des réglages en vigueur** (`--options-actives`), lus sur le
408:    /// `--options-actives` : imprime, APRÈS toutes les affectations, les réglages
506:            "--flux-serveur" => { o.flux_serveur = Some(suivant(i).clone()); 2 }
507:            "--options-actives" => { o.options_actives = true; 1 }
508:            "--ppl-reparti" => { o.ppl_reparti = Some(suivant(i).clone()); 2 }
537:            "--lot" => { o.lot = suivant(i).parse().unwrap(); 2 }
565:            "--flux-liste" => { o.flux_liste = true; 1 }
566:            "--flux-blocs" => { o.flux_blocs = true; 1 }
605:        eprintln!("[options] (une faute de frappe suffit — `--options-actives` montre \
  ```

### 🤖 Assistant

⏵ Je vérifie le plafond R4, le mode lot et la gestion des drapeaux inconnus.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src && grep -n \"256\\|PLAFOND\\|plafond\\|Mo\\b\" main.rs | head -40; echo \"=== context ===\"; grep -n \"PLAFOND\" main.rs", "description": "Grep R4 cap constant"}`

  ```
24:    format!("{:8.3} b/poids  ({:7.2} Mo)", b as f64 / n as f64, b as f64 / 8.0 / 1e6)
153:    println!("  listes fusionnées {:.2} Mo ({:.2} b/poids) | anciennes {:.2} Mo ({:.2}) | bitmap {:.2} Mo ({:.2})\n",
192:                // être un vrai plafond de débit, sinon on conclut à tort qu'un
205:    println!("  bande passante mémoire mesurée : {:.1} Go/s ({} Mo lus, {} threads, somme {} )",
300:        println!("           pull : {:.1} Go/s de poids lus ({:.1} Mo), soit {:.0} % du repère mémoire",
442:    /// diffèrent selon le mode (256 jetons et 16 bits en perplexité, 512 et
490:        // sur un contexte de 256 en croyant mesurer 8 fils sur 128 — et la
906:        println!("capteur hebbien : {} activations sur {} tokens, trace écrite dans {} ({:.1} Mo)",
1390:/// C'est le mode du préremplissage réparti : sans lui, un lot de 256 jetons
1391:/// payait 256 allers-retours. Le corps fait `n × hidden × 4` octets ; la
1463:/// contrôle : jusqu'à ~15 To demandés au noyau. 256 Mo couvrent largement un lot
1464:/// de 8 192 jetons × 8 192 canaux (268 Mo... soit un lot par fenêtre maximale).
1465:const PLAFOND_FLUX: usize = 256 << 20;
1467:/// Refuse une taille de corps au-delà du plafo
… [2425 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src && sed -n '1700,1800p' main.rs", "description": "Read receiving code around validation"}`

  ```
for v in etats { corps.extend_from_slice(&v.to_le_bytes()); }
    s.write_all(&corps)?;
    s.flush()?;
    Ok(TAILLE_TETE + corps.len())
}

/// Reçoit un flux : `(debut, fin, pos, mode, charge utile)`.
fn recevoir_flux(s: &mut std::net::TcpStream, hidden: usize) -> std::io::Result<Flux> {
    use std::io::Read;
    let mut tete = [0u8; TAILLE_TETE];
    s.read_exact(&mut tete)?;
    let u = |o: usize| u32::from_le_bytes([tete[o], tete[o+1], tete[o+2], tete[o+3]]);
    if u(0) != MAGIE_FLUX {
        return Err(std::io::Error::new(std::io::ErrorKind::InvalidData,
                                       "magie de flux absente"));
    }
    let version = tete[4];
    let mode = tete[5];
    if version != VERSION_FLUX {
        // Refus EXPLICITE : on ne devine pas la version du pair, on la nomme.
        return Err(std::io::Error::new(std::io::ErrorKind::InvalidData,
            format!("flux en version {version}, cette build parle la {VERSION_FLUX} \
                     (pair incompatible : rien n'a été interprété)")));
    }
    let (debut, fin, pos) = (u(6), u(10), u(14));
    let n = u(18) as usize;
    let echelle = f32::from_le_bytes([tete[22], tete[23], tete[24], tete[25]]);
 
… [3736 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je vérifie l'échappement des écarts et l'émetteur du mode blocs.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src && sed -n '1500,1620p' main.rs", "description": "Read encodage mode blocs emitter"}`

  ```
for (&i, &v) in idx.iter().zip(val.iter()) {
                    // Une trame FORGÉE ne doit pas tuer le nœud : un indice hors
                    // dimension était un `index out of bounds` → SIGABRT (mesuré
                    // par la relecture adversariale, trame LISTE n=1 indice 5000).
                    if (i as usize) < hidden { x[i as usize] = v as f32 * echelle; }
                    else { hors += 1; }
                }
                if hors > 0 {
                    eprintln!("[flux] {hors} indice(s) hors dimension ignorés (flux reçu \
de {hidden} canaux) — pair bogué ou hostile ?");
                }
                x
            }
            ChargeFlux::Blocs { idx, val, echelles } => {
                let mut x = vec![0f32; hidden];
                let mut hors = 0usize;
                for (&i, &v) in idx.iter().zip(val.iter()) {
                    let b = i as usize / 32;
                    if (i as usize) < hidden && b < echelles.len() {
                        x[i as usize] = v as f32 * echelles[b];
                    } else { hors += 1; }
                }
                if hors > 0 {
                    eprintln!("[flux] {hors} indice(s) hors dimension 
… [4537 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src && grep -n \"decoder_paires_blocs\\|encoder_paires_blocs\\|fn encoder\\|fn decoder\" main.rs model.rs | head -20", "description": "Find pair codec functions"}`

  ```
main.rs:1548:fn encoder_paires_blocs(idx: &[u16], val: &[i8]) -> Vec<u8> {
main.rs:1565:/// Décode `n` paires écrites par `encoder_paires_blocs`.
main.rs:1566:fn decoder_paires_blocs(corps: &[u8], n: usize) -> Result<(Vec<u16>, Vec<i8>), String> {
main.rs:1620:        let paires = encoder_paires_blocs(&idx, &val);
main.rs:1773:            let (idx, val) = match decoder_paires_blocs(&corps, n) {
main.rs:3354:        let octets = encoder_paires_blocs(&idx, &val);
main.rs:3356:        let (i2, v2) = decoder_paires_blocs(&octets, idx.len()).unwrap();
main.rs:3365:        let octets = encoder_paires_blocs(&idx, &val);
main.rs:3366:        assert!(decoder_paires_blocs(&octets[..octets.len() - 1], 2).is_err(),
main.rs:3368:        assert!(decoder_paires_blocs(&[255], 1).is_err(),
main.rs:3429:    fn decoder_une_trame(mode: u8, n: u32, corps: Vec<u8>, hidden: usize) -> std::io::Result<Flux> {
  ```

### 🤖 Assistant

⏵ Je lis la spécification du format de flux.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/format-flux.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/format-flux.md</path>
<type>file</type>
<content>
1: # Le format de flux (DRVF) — spécification
2: 
3: Ce format sert **trois choses à la fois**, et c'est délibéré :
4: 
5: 1. la **trace** d'exécution (`--trace-flux`) : ce qui s'est passé, couche par
6:    couche ;
7: 2. le **rejeu** (`--flux-forcer`) : on réinjecte les activations enregistrées et
8:    le calcul repart de là ;
9: 3. le **transport** (phase 3, `--flux-serveur` / `--ppl-reparti`) : ce qu'un nœud
10:    distant reçoit pour continuer le calcul.
11: 
12: Un seul format pour les trois, parce que ce sont les mêmes octets : une liste
13: d'activation est une liste d'activation, qu'elle aille sur le disque ou sur le
14: réseau.
15: 
16: ## Fichier (trace, `.bin`)
17: 
18: ```
19: en-tête   "DRVF"                    4 octets
20:           version      u16          = 1
21:           n_couches    u32
22:           cachés       u32
23: liste     couche       u16          < 1000 : entrée d'attention
24:                                     >= 1000 : entrée de FFN (couche - 1000)
25:           jeton        u32          COMPTEUR GLOBAL de jeton, pas la position
26:        
… [9294 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je lis le commentaire de version et l'écrivain/lecteur de trace dans model.rs.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs", "limit": 30, "offset": 1345}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
1345:     mdl.act_levels = ((1u32 << (abits - 1)) - 1) as f32;
1346:     mdl.act_thresh = opt.act_thresh;
1347:     mdl.act_topk = opt.act_topk;
1348:     mdl.act_renorm = opt.act_renorm;
1349:     // Les top-k étaient PUREMENT ignorés dans les modes flux (audit
1350:     // `reports/rapport-drapeaux-ignores.md`, défaut n°1) : ils s'appliquent ici,
1351:     // et ils voyagent dans l'en-tête pour que les deux nœuds fassent pareil.
1352:     mdl.act_topk_proj = opt.topk_proj;
1353:     mdl.attn_topk = opt.attn_topk;
1354:     mdl.qk_topk = opt.qk_topk;
1355:     mdl.moe_topk = opt.moe_topk;
1356: }
1357: 
1358: /// ---- Phase 3 : le flux passe d'un nœud à l'autre ----------------------------
1359: ///
1360: /// Cadriciel : `u32` magie, `u32` plage (debut, fin), `u32` position, `u32`
1361: /// dimension, puis les activations en f32. C'est le même contenu que le format
1362: /// de trace, réduit à ce qu'un nœud a besoin de recevoir pour continuer.
1363: const MAGIE_FLUX: u32 = 0x4452_5631;   // "DRV1"
1364: /// Version du protocole de flux. Elle est dans CHAQUE en-tête : un 
… [860 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src && sed -n '515,700p' model.rs", "description": "Read trace writer and reader in model.rs"}`

  ```
} else if e == 31 { (s << 31) | 0x7f80_0000 | (m << 13) }
    else { (s << 31) | ((e + 127 - 15) << 23) | (m << 13) };
    f32::from_bits(bits)
}

/// Trace du **flux d'activation** : par (couche, position), la liste des
/// neurones actifs — indice, valeur — avec son échelle. C'est le cœur de la
/// vision mis sur disque : on peut rejouer, comparer, et c'est aussi le format
/// qu'un nœud distant devrait recevoir pour continuer le calcul.
pub struct TraceFlux {
    /// Version écrite : 2 (indices par écarts, valeurs i16 — SANS PERTE) ou
    /// 3 (`DRAVE_TRACE_BLOCS=1` : valeurs i8 et une échelle f16 par bloc de 32
    /// canaux, ~22 % plus petit, avec perte).
    pub version: u16,
    /// Nombre de canaux par bloc d'échelle en v3.
    pub bloc: usize,
    pub fichier: std::io::BufWriter<std::fs::File>,
    /// Couches à tracer (toutes si vide).
    pub couches: Vec<usize>,
    pub octets: u64,
    pub enregistrements: u64,
    pub actifs: u64,
}

impl TraceFlux {
    pub fn nouveau(chemin: &str, couches: Vec<usize>, hidden: usize, n_layer: usize)
        -> std::io::Result<Self> {
        use std::io::Write;
        let mut f = std::io::BufWriter::new(std::fs::File::create(chemi
… [7741 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je mesure la taille des documents de référence et commence le README.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && wc -l README.md REPRISE.md docs/*.md reports/rapport-placement-bits-kv.md reports/rapport-session-2026-09-30.md reports/rapport-compacite-trace.md reports/rapport-transport-liste.md reports/rapport-prefill-reparti.md reports/rapport- … [100 caractères tronqués]`

  ```
494 README.md
   501 REPRISE.md
   127 docs/colab-reparti.md
   145 docs/comparaison-spiking.md
   522 docs/contexte-long.md
   317 docs/convertisseur.md
   171 docs/format-flux.md
    78 docs/histoire.md
   725 docs/plan-mla-vision.md
   424 docs/plan-prefill-reparti.md
   212 docs/programme-recherche.md
   307 docs/roadmap.md
   247 docs/vision.md
    92 reports/rapport-placement-bits-kv.md
    67 reports/rapport-session-2026-09-30.md
   263 reports/rapport-compacite-trace.md
   234 reports/rapport-transport-liste.md
   107 reports/rapport-prefill-reparti.md
    66 reports/rapport-phase3-reparti.md
    53 reports/rapport-attribution-kv.md
  5152 total
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"v3\\|v4\\|79 octets\\|39 octets\\|3 663\\|3623\\|3 623\\|1 568\\|1 589\\|917\\|mode 4\\|mode lot\\|MODE_LOT\\|--lot\\|--options-actives\\|DRAVE_KV_K_F16\\|DRAVE_TRACE_BLOCS\\|256 Mo\\|R4\" README.md REPRISE.md docs/*.md | h … [65 caractères tronqués]`

  ```
REPRISE.md:33:> **Revérifiées le 30/09 après tous les changements de la journée** (mode lot,
REPRISE.md:34:> protocole v4, DRVF v2/v3, plafond R4, tableau de bord) : Qwen ctx 256 =
REPRISE.md:247:| `DRAVE_KV_K_F16=1` | clés en **f16** (2 octets/valeur, précision relative) | **le meilleur réglage mesuré** : à 8 192 jetons, clés f16 + valeurs int8 = **+0,018 %** pour **39 % de la taille f32** — contre +0,023 % pour les clés f32 (64 % de la taille) et +3,04 % pour l'int8 complet (28 %) |
REPRISE.md:248:| `DRAVE_TRACE_BLOCS=1` | trace DRVF **v3** : valeurs i8, échelle f16 par bloc de 32 | 45 079 930 o contre 66 370 408 en v2 (−32 %), rejeu 19,4029 contre 19,3885 (+0,074 %) |
REPRISE.md:249:| `DRAVE_FLUX_VERIF=1` | vérifie l'écart entre l'activation calculée et celle que la trace impose | 1,5e-5 en v2 ; **muet dès que `--lot > 1`** (le rejeu par lots passe par `flux_lot`) |
REPRISE.md:256:| `DRAVE_DEBUG_FLUX=1` | le nœud moteur imprime ce qu'il reçoit (n, positions, octets) | diagnostic du mode lot |
REPRISE.md:284:**Le protocole de flux est en v4** (`docs/format-flux.md`) : en-tête de **79
REPRISE.md:297:| dense f32 | 3 623 | **0,00e0** |
REPRISE.md:324:**écart 0,00e0** (18,0851 = 18,0
… [9616 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je lis les rapports produits aujourd'hui (KV, session, préremplissage).

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-placement-bits-kv.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-session-2026-09-30.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-placement-bits-kv.md</path>
<type>file</type>
<content>
1: # Où mettre les bits du cache KV : la courbe complète
2: 
3: **En une ligne** : à taille ÉGALE, mettre les bits sur les **clés** plutôt que sur
4: les valeurs change l'erreur d'un facteur **130 à 840** — et les clés en f16
5: donnent 39 % de la taille f32 pour +0,06 %.
6: 
7: ## Le tableau
8: 
9: Qwen2.5-0.5B-Q8_0, 8 191 jetons notés, contexte 8 192. « Octets par élément » =
10: octets par position et par dimension de tête, pour la paire clé + valeur (échelle
11: par bloc de 32 comprise).
12: 
13: | clés | valeurs | octets/élément | % du f32 | perplexité | écart |
14: |---|---|---|---|---|---|
15: | f32 | f32 | 8 | 100 % | **14,2339** | référence |
16: | **f32** | **int8** | 5,125 | 64 % | **14,2372** | **+0,023 %** |
17: | **int8** | **f32** | 5,125 | 64 % | 14,6622 | **+3,01 %** |
18: | f32 | int4 | 4,625 | 58 % | 14,2994 | +0,46 % |
19: | int4 | f32 | 4,625 | 58 % | 69,0464 | **+385 %** |
20: | int8 | int8 | 2,25 | 28 % | 14,6667 | +3,04 % |
21: | **f16** | **int8** | **3,125** | **39 %** | **14,2365** | **+0,018 %** |
22: | int4 | int4 | 1,25 | 16 % |
… [4055 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-session-2026-09-30.md</path>
<type>file</type>
<content>
1: # Session du 30/09 — index des chantiers
2: 
3: Deux créneaux : 10h06–11h42 (time-box de 2 h) puis 11h46–15h00 (autonomie et
4: parallélisme). Trente-cinq commits, deux campagnes de mesure lourdes, cinq
5: relectures déléguées. Chaque chiffre a son rapport ; ceci est l'index.
6: 
7: ## Ce qui est livré
8: 
9: | chantier | résultat | rapport |
10: |---|---|---|
11: | **Calcul réparti fidèle** | écart local/réparti **0,00e0** — 144,8289 des deux côtés à 40 jetons, 9,5146 à 1 024 | `rapport-phase3-reparti.md` |
12: | **Préremplissage par LOTS** (mode 3) | 256 jetons en **4 lots** (ou 1 seul) → 0,00e0 ; **18× plus rapide** qu'un flux par jeton sur un lien à 20 ms | `rapport-prefill-reparti.md` |
13: | **Transport en listes** | dense 3 663 octets → **1 629** par flux (÷2,3) pour 1,3 % d'écart à 1 024 jetons | `rapport-transport-liste.md` |
14: | **où mettre les bits du cache KV** | à taille ÉGALE : clés f32 + valeurs int8 **+0,023 %** contre **+3,01 %** pour l'inverse (facteur **130**) ; 4 bits : +0,46 % contre **+385 %** (facteur **840**) | `rapport-placemen
… [3628 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je lis les rapports transport, préremplissage réparti et compacité.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-prefill-reparti.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-transport-liste.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-prefill-reparti.md</path>
<type>file</type>
<content>
1: # Phase 3.4 — le préremplissage par LOTS sur le fil
2: 
3: **En une ligne** : un préremplissage de 256 jetons traverse désormais le réseau en
4: **4 lots** (ou un seul) au lieu de 255 flux, et le calcul coupé redonne exactement
5: le calcul local — **écart 0,00e0**.
6: 
7: ## Le problème
8: 
9: Le transport était séquentiel : un flux par jeton, donc un aller-retour par jeton.
10: Un préremplissage de N jetons payait N fois la latence, alors que la latence est
11: précisément le seul poste qui compte (`attente ≈ calcul distant + 3,2 × latence
12: par message`, mesuré dans `reports/rapport-transport-liste.md`). Avec 60 ms
13: d'aller-retour, 256 jetons coûtaient 15 secondes d'attente pure.
14: 
15: ## Le mode 3 du protocole
16: 
17: ```
18: en-tête   magie u32 · version u8 (4) · mode u8 (3 = LOT) · plage (2 × u32)
19:           position u32 (celle du PREMIER jeton) · n u32 (nombre d'ÉTATS)
20:           échelle f32 · et le contrat d'activation (niveaux, seuil, top-k,
21:           renorm, 7 top-k par projection, attn/qk/moe top-k)
22: corps     n × dimension 
… [4487 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-transport-liste.md</path>
<type>file</type>
<content>
1: # Phase 3.2 — transporter la LISTE au lieu du vecteur
2: 
3: **En une ligne** : le flux peut voyager en liste creuse — **897 octets au lieu de
4: 3 623** à seuil 5 %, et **1 568** avec des indices par écarts — mais jeter des
5: canaux coûte cher (**×1,8 de perplexité** à ce seuil), et la courbe est là pour
6: dire où.
7: 
8: ## Le protocole, mesuré
9: 
10: Deux modes dans le même en-tête de 39 octets — magie, version, mode, plage,
11: position, dimension, échelle, **et les réglages d'activation** :
12: 
13: | mode | contenu | octets par flux (Qwen2.5-0.5B, 896 canaux) |
14: |---|---|---|
15: | 0 · dense f32 | `896 × f32` | **3 623** (39 + 3 584) |
16: | 1 · listes | `n × (indice u16 · valeur i16)` | 39 + 4 × actifs |
17: 
18: Le mode 1 est le format du disque, à l'octet près. La réponse est encodée comme
19: la demande : un pair qui parle en listes reçoit des listes.
20: 
21: ## La courbe (40 jetons, 12 couches de chaque côté)
22: 
23: | seuil | activité | octets/flux (aller) | octets/flux (retour) | perplexité locale | perplexité répartie | écart |
24: |--
… [11845 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je lis REPRISE.md en entier par blocs ciblés.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/REPRISE.md", "limit": 130, "offset": 1}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/REPRISE.md</path>
<type>file</type>
<content>
1: # Reprise — état du projet et mode d'emploi pour une nouvelle session
2: 
3: > Rédigé à la fin d'une session longue. Tout ce qui suit est **mesuré**, pas
4: > déduit. Les valeurs de perplexité sont des **références de non-régression** :
5: > si une modification les change, c'est qu'elle a changé le calcul.
6: >
7: > **Nom** : le projet s'appelle **Drave** (binaire `drave`, paquet `drave-core`,
8: > variables `DRAVE_*`, histoire du renommage dans `docs/histoire.md`). Le dossier
9: > de travail, lui, s'appelle encore `Qtrinet` — les chemins ci-dessous sont ceux
10: > qui existent.
11: 
12: ---
13: 
14: ## 1. En une phrase
15: 
16: `drave-core` est un moteur d'inférence Rust (~11 440 lignes, `std` seul) qui
17: charge les GGUF **en place** (aucune copie, aucune requantification), exécute les
18: projections soit en listes d'événements, soit en produit scalaire dense, gère les
19: MoE, tient une conversation, et déporte au GPU ce qui y gagne. Il fait tourner du
20: 0,5 B au 120 B sur le CPU de cette machine.
21: 
22: ```bash
23: cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave
… [7994 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je poursuis REPRISE (variables, transports, trace, KV).

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/REPRISE.md", "limit": 180, "offset": 225}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/REPRISE.md</path>
<type>file</type>
<content>
225:    (234,88 contre 298,56 à 2 048) mais repasse aujourd'hui par le CPU : le noyau
226:    GPU ne le gère pas.
227: 6. ~~Experts MXFP4 dans le préremplissage par lots~~ **MESURÉ, À NE PAS FAIRE
228:    TEL QUEL** : le cache LRU donne +6 % en décodage (5,12 → 5,43 jetons/s,
229:    53,5 % de succès, 10,64 Go montés) — le chemin CPU des experts est déjà AVX2
230:    et le coût par expert est faible. Il faudrait supprimer les trois lancements
231:    et copies par expert, ou grouper les projections.
232: 7. **Mesure de qualité à contexte long** (`reports/rapport-aiguille.md`) :
233:    étendre la grille à 8 192 et 16 384, plusieurs codes par sonde, et croiser avec
234:    `--attn-topk`.
235: 
236: ### Les variables d'environnement, et leurs pièges
237: 
238: | variable | ce qu'elle fait | le piège |
239: |---|---|---|
240: | `DRAVE_GPU=1` | ouvre le pilote CUDA (`gpu::instance`) | **c'est elle qui commande tout** ; sans elle, les autres ne font RIEN et rien ne le dit |
241: | `DRAVE_GPU_TETE=1` | déporte la tête (Q8_0 ou Q6_K) | inutile sans `DRAVE_GPU` |
242: | `DRAVE_GPU_KV=1` | ti
… [11788 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je compare systématiquement les variables DRAVE_* du code et des documents.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rhoE 'DRAVE_[A-Z0-9_]+' --include='*.md' --include='*.rs' --include='*.py' . 2>/dev/null | sort -u > /tmp/all_vars.txt && echo \"=== CODE RS ===\" && grep -rhoE 'DRAVE_[A-Z0-9_]+' drave-core/src/*.rs | sort -u > /tmp/code_vars. … [175 caractères tronqués]`

  ```
=== CODE RS ===
DRAVE_BANC_KV_DEBUG
DRAVE_BANC_KV_GPU_SEUL
DRAVE_BANC_KV_GRAD
DRAVE_BANC_KV_K0
DRAVE_BANC_KV_KUNIT
DRAVE_BANC_KV_UNIT
DRAVE_BANC_KV_V1
DRAVE_DEBUG_FLUX
DRAVE_FLUX_VERIF
DRAVE_GPU
DRAVE_GPU_EXPERTS
DRAVE_GPU_EXPERTS_GO
DRAVE_GPU_KV
DRAVE_GPU_TETE
DRAVE_HARMONY_TRACE
DRAVE_KV_BITS
DRAVE_KV_F16
DRAVE_KV_K_F16
DRAVE_KV_K_F32
DRAVE_KV_V_F32
DRAVE_Q8_BLOCS
DRAVE_SANS_EMPRUNT
DRAVE_TRACE_BLOCS
DRAVE_VISION_TEXTE
DRAVE_YARN
DRAVE_YARN_MSCALE
DRAVE_YARN_NON
DRAVE_YARN_RAMPE
=== DOCS ONLY (absent du code) ===
DRAVE_BANC_KV_
DRAVE_BANC_KV_BITS
DRAVE_FLUX_POS
DRAVE_FLUX_VER
DRAVE_KV
DRAVE_KV_
DRAVE_VISIO
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn 'DRAVE_' --include='*.md' . | grep -vE 'DRAVE_(GPU|GPU_TETE|GPU_KV|GPU_EXPERTS|GPU_EXPERTS_GO|KV_BITS|KV_K_F32|KV_V_F32|KV_K_F16|KV_F16|TRACE_BLOCS|FLUX_VERIF|HARMONY_TRACE|VISION_TEXTE|Q8_BLOCS|SANS_EMPRUNT|YARN|YARN_NON|YA … [114 caractères tronqués]`

  ```
./reports/rapport-drapeaux-ignores.md:22:`DRAVE_*` (27 chaînes, dont le préfixe cité dans un message). Pour chacun : recherche du **site
./reports/rapport-drapeaux-ignores.md:98:## 5. Variables d'environnement `DRAVE_*` (26)
./reports/rapport-drapeaux-ignores.md:230:- **110 options auditées** : 84 drapeaux de ligne de commande + 26 variables `DRAVE_*`.
./reports/rapport-coherence-docs.md:139:| 68 | `docs/plan-prefill-reparti.md:256` | `DRAVE_FLUX_POS=1` imprime `[flux] lot pos …` | variable absente du code | PÉRIMÉ |
./README.md:13:`drave`, les variables `DRAVE_*` (table de conversion dans `docs/histoire.md`) ;
./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:21413:2. **commit de renommage dédié** : crate `drave-core`, binaire `drave`, variables `DRAVE_*` **avec alias `QT_*` conservés** — le journal archivé n'est pas réécrit ;
./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:21486:- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date +%Y-%m-%d && grep -rhoE '\"(DRAVE_[A-Z0-9_]+)\"' drave-core/src/*.rs | sort -u | tr '\\n' ' '", "description": "Get date and env var list"}`
./journal/sessions/bbd6969f-0f70-42b2-8951-64d1
… [7592 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je refais le diff des variables hors journal et vérifie les renvois de fichiers.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rhoE 'DRAVE_[A-Z0-9_]+' README.md REPRISE.md docs/*.md reports/*.md colab/*.md tools/*.py 2>/dev/null | sort -u > /tmp/docs_vars.txt && echo \"=== dans les docs, absentes du code ===\" && comm -23 /tmp/docs_vars.txt /tmp/code_v … [310 caractères tronqués]`

  ```
=== dans les docs, absentes du code ===
DRAVE_BANC_KV_
DRAVE_FLUX_POS
DRAVE_KV_
=== dans le code, absentes des docs ===
DRAVE_BANC_KV_DEBUG
DRAVE_BANC_KV_GRAD
DRAVE_BANC_KV_KUNIT
DRAVE_BANC_KV_V1
=== DRAVE_FLUX_POS ? ===
REPRISE.md:249:| `DRAVE_FLUX_VERIF=1` | vérifie l'écart entre l'activation calculée et celle que la trace impose | 1,5e-5 en v2 ; **muet dès que `--lot > 1`** (le rejeu par lots passe par `flux_lot`) |
docs/format-flux.md:165:| la fidélité de l'encodage est chiffrée | `DRAVE_FLUX_VERIF=1` : écart relatif **1,5e-5**, soit la quantification 16 bits |
docs/plan-prefill-reparti.md:266:3. *En diagnostic* : `DRAVE_FLUX_POS=1` fait imprimer `[flux] lot pos .. pos+t-1`
docs/roadmap.md:208:Identique. Et le diagnostic (`DRAVE_FLUX_VERIF=1`) chiffre la fidélité de
reports/rapport-coherence-docs.md:139:| 68 | `docs/plan-prefill-reparti.md:256` | `DRAVE_FLUX_POS=1` imprime `[flux] lot pos …` | variable absente du code | PÉRIMÉ |
reports/rapport-coherence-docs.md:149:| 78 | `docs/format-flux.md:139` | `DRAVE_FLUX_VERIF=1` chiffre la fidélité | présente (model.rs), mais muette dès `--lot > 1` (`rapport-drapeaux-ignores.md:109`) — le document ne le dit pas | MANQUANT |
reports/rap
… [791 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport re, os, glob\nfiles = ['README.md','REPRISE.md'] + glob.glob('docs/*.md') + glob.glob('reports/*.md') + glob.glob('colab/*.md')\nmissing = []\ntodo = []\nfor f in files:\n    txt = open(f, encoding='utf-8',  … [699 caractères tronqués]`

  ```
=== LIENS MORTS ===
  ```

### 🤖 Assistant

⏵ Je lis le README en entier (première moitié).

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/README.md", "limit": 260}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/README.md</path>
<type>file</type>
<content>
1: # Drave
2: 
3: *Anciennement `Qtrinet`.* **La drave**, c'est le flux qu'on conduit : ici, celui
4: des **listes d'activation** (*stream of logs*) — le moteur ne lit pas des
5: matrices, il pousse des faits valués vers leurs destinations. La vision complète
6: est dans [`docs/vision.md`](docs/vision.md).
7: 
8: Origine du projet : inférence de LLM en **ternaire / multi-bits** sur un cluster
9: de cartes **Stratix V** (Microsoft Storey Peak) — 100 % logique, sans DSP.
10: Le cahier des charges d'origine est dans [`Qtrinet-bootstrap.md`](Qtrinet-bootstrap.md)
11: ⚠️ **il a été audité et corrigé** : voir la section « Écarts avec le CDC » ci-dessous.
12: Le renommage est FAIT : le crate et le binaire s'appellent `drave-core` et
13: `drave`, les variables `DRAVE_*` (table de conversion dans `docs/histoire.md`) ;
14: le journal de sessions, archivé, n'est pas réécrit.
15: 
16: ---
17: 
18: ## État du projet
19: 
20: | Étape | État |
21: |-------|------|
22: | Audit du cahier des charges | ✅ (corrections ci-dessous) |
23: | **Test de principe : quantification d'un modèle minimal** | ✅ **fa
… [13492 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je lis la seconde moitié du README (moteur, chiffres, renvois).

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/README.md", "offset": 261}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/README.md</path>
<type>file</type>
<content>
261: 
262: 1. **Exploiter l'ordre naturel** (par source, listes de deltas) : 7,79 G év/s, le meilleur
263:    résultat mesuré. Pas de tri.
264: 2. **Multi-plans : décaler l'activation**, pas fusionner les listes. La contribution du
265:    plan *b* vaut `x[src] << b` : l'accumulation les somme naturellement, sans aucun
266:    dédoublonnage. Un seul accumulateur suffit.
267: 3. **Le dédoublonnage ne se justifie que pour la sémantique** : fusion de sommes
268:    partielles venant de plusieurs cartes (ring), ou déterminisme du résultat. Dans ce cas,
269:    utiliser un **réseau de combinaison à compartiments par destination** (ce que font les
270:    routeurs AER), jamais un tri global.
271: 
272: > ⚠️ Le tri mesuré est un radix naïf mono-thread ; un tri parallèle irait ~10× plus vite,
273: > mais resterait 5× plus cher que l'accumulation qu'il optimise.
274: 
275: ---
276: 
277: ## Moteur d'événements Rust (`drave-core`)
278: 
279: Le moteur d'exécution par listes est maintenant écrit en Rust — **std seul, zéro
280: dépendance** (crates.io est inaccessible depuis cette machine, et c'e
… [12656 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je lis la fin de REPRISE et vérifie le nombre de tests dans le code.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/REPRISE.md", "offset": 405}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/REPRISE.md</path>
<type>file</type>
<content>
405:   allouait sur le `n` du fil (12 Gio avant de dire « tronqué »), une trame forgée
406:   hors dimension TUAIT le nœud (SIGABRT), l'envoi paniquait encore sur un pair
407:   fermé, `-keep` (un seul tiret) était avalé, `--flux-forcer` ignoré en inférence,
408:   `--banc-mla` muet sur la trace.
409: - **Treize tests** : les sept du protocole et du plafond, dont deux qui envoient
410:   une VRAIE trame forgée dans une socket (indice hors dimension, 100 millions de
411:   blocs).
412: 
413: ### Les prochains chantiers, dans l'ordre
414: 
415: 0. **Noyau GPU de top-k** (phase 1.1) : le seul poste de la feuille de route qui
416:    demande du travail GPU *neuf* ; les deux Quadro sont libres et le cadre existe
417:    (`gpu/compiler.sh`, `drave_gpu.cu`, sm_75). Vient ensuite le **second GPU**
418:    (16 Go dormants : cache d'experts MXFP4 et KV à 1 M paginé).
419: 1. ~~Préremplissage par LOTS sur le fil~~ **FAIT** (mode 3 : 256 jetons en 4 lots,
420:    écart 0,00e0 ; `reports/rapport-prefill-reparti.md`). Le suivant dans cette
421:    veine : le **lot en listes** (mode 4), chaque état
… [4782 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src && grep -c '#\\[test\\]' main.rs model.rs engine.rs list.rs gpu.rs gguf.rs tokenizer.rs | cat; echo \"total:\"; grep -h '#\\[test\\]' *.rs | wc -l", "description": "Count test functions in Rust code"}`

  ```
main.rs:7
model.rs:1
engine.rs:2
list.rs:3
gpu.rs:0
gguf.rs:0
tokenizer.rs:0
total:
13
  ```

### 🤖 Assistant

⏵ Je lis la feuille de route (statuts, journal des mesures, reste à faire).

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/roadmap.md", "limit": 130}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/roadmap.md</path>
<type>file</type>
<content>
1: # Roadmap
2: 
3: > Suite de [`docs/vision.md`](vision.md). Cinq phases, de ce qui se fait **tout de
4: > suite sur cette machine** à ce qui demande une infra (Colab, FPGA). Chaque
5: > phase a un critère de succès **mesurable**, et l'état de chaque chantier est
6: > marqué : ✅ fait · 🔬 en cours · ⏳ à faire · 🧱 bloqué par une infra absente.
7: 
8: ## Phase 0 — La drave observable (aucune infra)
9: 
10: **Objectif** : faire du flux de listes un objet de première classe, qu'on
11: enregistre et qu'on compare. Sans cela, tout le reste se débugue à l'aveugle.
12: 
13: | # | chantier | état | critère de succès |
14: |---|---|---|---|
15: | 0.1 | **Format de trace du flux** : par (couche, position), la liste des neurones actifs (indice + valeur), l'échelle, le nombre | ✅ | écrit et relu sans perte ; **132 Mo pour 512 jetons** (258 ko/jeton), **+8 % de temps** — mesuré |
16: | 0.2 | **Diff par couche** (`tools/diff_flux.py`) : où deux exécutions divergent, à quel jeton, quels neurones | ✅ | démontré : KV f32 contre int8 → première divergence **couche 1, jeton 0**, 896 neurones, 2,9e-
… [11110 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je lis la fin de la roadmap (prochaines étapes, conclusion).

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/roadmap.md", "offset": 240}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/roadmap.md</path>
<type>file</type>
<content>
240:    d'échec « analysé mais jamais appliqué » du dépôt produit.
241: 2. **La norme finale était appliquée deux fois.** Le nœud moteur recevait
242:    `fin = n_layer`, donc son `forward` normait (`couche_fin >= n_layer`), et le
243:    pilote normait ensuite avec `norme_finale()`. La règle est maintenant portée
244:    par un drapeau explicite, `flux_brut` : un nœud intermédiaire rend TOUJOURS un
245:    flux résiduel brut, et la norme appartient au nœud qui possède la tête de
246:    sortie — une seule fois.
247: 
248: Le protocole, lui, n'a pas changé d'un octet : c'est le moteur qui était faux.
249: 
250: **Puis le transport lui-même** : `--flux-liste` fait voyager la LISTE (indice
251: u16, valeur i16, une échelle), c'est-à-dire le format du disque, au lieu du
252: vecteur dense f32. Mesuré à 40 jetons, par flux (aller) :
253: 
254: | mode | octets | écart de perplexité |
255: |---|---|---|
256: | dense f32 | 3 623 | **0,00e0** |
257: | listes, seuil 0,00 | 3 622 | 2,6e-2 |
258: | listes, seuil 0,02 | 2 203 | 4,9e-2 |
259: | listes, seuil 0,05 | 897 | 8,1e-1 |
260: 
261: 
… [3360 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je lis la recette Colab et le rapport de la phase 3.1.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/colab-reparti.md"}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-phase3-reparti.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/colab-reparti.md</path>
<type>file</type>
<content>
1: # Répétition Colab — la phase 3.4, pas à pas
2: 
3: Objectif : deux machines qui se passent des **listes d'activation**, l'une sur le
4: runtime Colab, l'autre en local, et **les mêmes logits** qu'en local.
5: 
6: Ce document est la recette ; l'état du protocole et les chiffres qui la
7: dimensionnent sont dans `docs/format-flux.md` et
8: `reports/rapport-transport-liste.md`.
9: 
10: ## Mise en place, concrètement
11: 
12: `tools/preparer_colab.sh` produit le dépôt en **un fichier** (`drave.bundle`, 4,5 Mo
13: avec tout l'historique) et affiche l'empreinte SHA-256 du modèle — les deux nœuds
14: doivent charger le même GGUF, la dimension ne voyage pas. `colab/README.md` donne
15: la marche à suivre (tunnel, téléversements) et `colab/Drave-reparti.ipynb` est le
16: notebook prêt à ouvrir, avec la vérification d'empreinte et la lecture du résultat.
17: 
18: ## Ce qui est déjà vérifié, et ce qui ne l'est pas
19: 
20: | point | état |
21: |---|---|
22: | fidélité du découpage | ✅ écart **0,00e0** entre local et deux nœuds (40 et 200 jetons) |
23: | version du protocole | ✅ d
… [5876 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-phase3-reparti.md</path>
<type>file</type>
<content>
1: # Phase 3 — le calcul réparti redevient fidèle
2: 
3: **En une ligne** : deux processus qui se passent des flux calculent maintenant
4: **exactement** la même perplexité qu'un seul — écart **0,00e0** — après deux
5: corrections qui n'étaient pas celle que je croyais.
6: 
7: ## Le banc
8: 
9: Deux processus, localhost, modèle Qwen2.5-0.5B-Q8_0, 12 couches chacun, contexte
10: 256. Le pilote garde les couches 0..12, le nœud moteur applique 12..24 et renvoie
11: le flux ; le pilote norme, applique la tête et note la perplexité. La référence
12: est le même modèle calculé entièrement en local. Reproductible :
13: 
14: ```bash
15: ./drave models/Qwen2.5-0.5B-Q8_0.gguf --flux-serveur 45733 &
16: ./drave models/Qwen2.5-0.5B-Q8_0.gguf --ppl-reparti 127.0.0.1:45733 \
17:         --couches-locales 12 --limit 40 --ctx 256
18: ```
19: 
20: 40 jetons suffisent à trancher : la locale vaut 144,8289, et un découpage fidèle
21: doit redonner ce chiffre, pas un chiffre « proche ».
22: 
23: ## Le défaut que je croyais, et le défaut réel
24: 
25: Je suis parti d'une hypothèse l
… [2502 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je lis l'en-tête du plan de préremplissage réparti et ses renvois.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/plan-prefill-reparti.md", "limit": 110}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/plan-prefill-reparti.md</path>
<type>file</type>
<content>
1: # Plan — le préremplissage par lots sur le fil (phase 3.4)
2: 
3: > **État (30/09, après mise en œuvre).** Ce plan a été suivi : le mode 3 existe,
4: > le préremplissage par lots est fidèle (écart **0,00e0** en 4 lots de 64 comme en
5: > un seul lot) et `reports/rapport-prefill-reparti.md` consigne les mesures. Trois
6: > écarts au plan, tous volontaires : la version du protocole est passée à **4** (et
7: > non 3) parce que le contrat d'activation transporte désormais aussi les top-k ;
8: > l'échappement d'indice du mode blocs s'écrit sur **deux** octets (le plan le
9: > disait, le code en écrivait quatre) ; et la règle R4 (plafond de 256 Mo) est
10: > maintenant DANS le code, avec son test. Les sections ci-dessous restent le plan
11: > d'origine — elles ne sont pas réécrites, pour qu'on puisse comparer.
12: 
13: **En une ligne** : aujourd'hui un flux = un jeton, donc un préremplissage de N
14: jetons paie N allers-retours ; on ajoute un **mode 3** qui transporte N états
15: dans **un seul** message, et le banc réparti doit rendre **0,00e0**.
16: 
17: Ce document
… [5553 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je vérifie la règle R1 dans le code et l'historique du plan.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '249,285p' docs/plan-prefill-reparti.md; echo \"=== git log plan ===\"; git log --oneline -5 -- docs/plan-prefill-reparti.md", "description": "Read plan diagnostic section and its git history"}`

  ```
**Ce qui est vérifié.**

1. *Avant le calcul, côté serveur* : `pos + n ≤ mdl.ctx`, sinon arrêt nommé (§2.4).
   Sans ce test, `KvCache::assurer` (model.rs:907) **boucle indéfiniment** : il
   plafonne `cap` à `self.ctx` dans un `while cap < besoin`, donc `besoin > ctx`
   ne termine jamais. Ajouter en défense `assert!(besoin <= self.ctx, …)` dans
   `assurer` — une panique nommée vaut mieux qu'une attente active (le dépôt a
   déjà payé 27 minutes de blocage muet, cf. `reports/rapport-prefill-par-lots.md`
   §4.ter).
2. *Après réception, côté pilote* — l'**écho** : `rep.mode == MODE_LOT`,
   `rep.pos == pos0`, `rep.n == chunk.len()`, `rep.debut == couches_locales`,
   `rep.fin == n_layer`. Sans ces cinq égalités, un lot décalé corrompt le cache
   des deux nœuds **en silence** : les positions ne servent qu'à la lecture
   suivante, donc l'erreur n'apparaîtrait qu'à la génération, loin de sa cause.
   C'est la même classe que la clé `(couche, position)` de la phase 0, qui avait
   donné 356 694 de perplexité.
3. *En diagnostic* : `DRAVE_FLUX_POS=1` fait imprimer `[flux] lot pos .. pos+t-1`
   des deux côtés ; deux lignes qui divergent désignent le découpage fautif.

**Dépassement de
… [915 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src && sed -n '2090,2160p' main.rs", "description": "Read run_ppl_reparti lot sending logic"}`

  ```
println!("  transport         : LOTS de {lot} jetons · {:.0} octets par lot (aller) · \
                  {:.1} ko par jeton · {} lots (au lieu de {} flux)",
                 octets_envoyes as f64 / nflux as f64,
                 octets_envoyes as f64 / nflux as f64 / 1024.0 / lot as f64,
                 nflux, ids.len() - 1);
        println!("  temps             : {:.1} ms par LOT en local · {:.1} ms à attendre le pair · \
                  soit {:.2}× le calcul local seul",
                 1000.0 * t_local / nflux as f64, 1000.0 * t_pair / nflux as f64,
                 t_pair / t_local.max(1e-9));
    } else {
    println!("  transport         : {} · {:.0} octets par flux (aller) · {:.0} au retour · \
              {:.1} % d'activité ({:.0} neurones par flux) · {} flux",
             match mode { MODE_BLOCS => "listes à échelle par bloc (2 octets/actif, écarts)",
                          MODE_LISTE => "listes quantifiées",
                          _ => "dense f32" },
             octets_envoyes as f64 / nflux as f64, octets_recus as f64 / nflux as f64,
             100.0 * actifs_envoyes as f64 / (nflux as f64 * mdl.cfg.hidden as f64),
             actifs_envoyes as f64 / n
… [2696 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je cherche la logique de découpage en lots côté pilote.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src && grep -n \"envoyer_lot\\|chunk\\|lot\\b\" main.rs | sed -n '1,60p'", "description": "Grep lot chunking in main.rs"}`

  ```
195:                for c in b[lo..hi].chunks_exact(8) {
361:    println!("[options] fenêtre {} · motif {} · seuil push {} · lot {} · ffn_gain {:?} · hebb {}",
362:             mdl.attn_window, mdl.swa_pattern, mdl.seuil_push, mdl.lot,
456:    /// Taille du lot de préremplissage : 1 = jeton par jeton (défaut).
457:    lot: usize,
537:            "--lot" => { o.lot = suivant(i).parse().unwrap(); 2 }
635:        hebb_layer, hebb_q, hebb_out, sans_yarn, lot, ffn_gain,
650:    mdl.lot = lot.max(1);
1390:/// C'est le mode du préremplissage réparti : sans lui, un lot de 256 jetons
1447:    /// Nombre du mode : canaux (dense, listes), actifs (blocs) ou ÉTATS (lot).
1463:/// contrôle : jusqu'à ~15 To demandés au noyau. 256 Mo couvrent largement un lot
1464:/// de 8 192 jetons × 8 192 canaux (268 Mo... soit un lot par fenêtre maximale).
1493:            // Un lot n'a pas UN vecteur dense : c'est `plat()` qui le sert, et
1494:            // `forward_lot` qui le consomme. L'appeler ici serait une erreur de
1496:            ChargeFlux::Lot(_) => panic!("un lot d'états n'est pas un vecteur dense"),
1537:    /// Le lot aplati, pour le nœud qui doit le rendre à `forward_lot`.
1668:/// Le lot voya
… [2926 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src && sed -n '1980,2050p' main.rs", "description": "Read ppl_reparti lot loop"}`

  ```
let t1 = Instant::now();
    let mut nll = 0f64;
    if lot > 1 {
        // PRÉREMPLISSAGE RÉPARTI : un lot par aller-retour au lieu d'un flux par
        // jeton. C'est ce que la phase 3.4 doit démontrer — le découpage doit
        // coûter la latence d'UN message par lot, pas par jeton.
        if mode != MODE_DENSE {
            eprintln!("[flux] --flux-liste / --flux-blocs ne s'appliquent PAS aux lots \
(mode 4 non écrit) : le lot part en f32 dense. À --lot 1, le mode choisi s'applique.");
        }
        let mut pos = 0usize;
        while pos + 1 < ids.len() {
            let t = lot.min(ids.len() - pos);
            let horloge = Instant::now();
            let hs = mdl.forward_lot(&ids[pos..pos + t], pos);
            let plat: Vec<f32> = hs.concat();
            t_local += horloge.elapsed().as_secs_f64();
            let horloge = Instant::now();
            let o = match envoyer_lot(&mut sock, couches_locales as u32, n_layer as u32,
                                      pos as u32, &plat, t, &mdl) {
                            Ok(o) => o,
                            Err(e) => {
                                eprintln!("[flux] le nœud moteur a fermé la connexion \
pe
… [2351 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je lis le rapport de compacité de trace et le rapport d'attribution KV.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-compacite-trace.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-compacite-trace.md</path>
<type>file</type>
<content>
1: # Compacité de la trace — le disque paie trois fois le câble
2: 
3: > **Fait depuis (même jour).** La variante « écarts » est **implémentée et
4: > mesurée** dans le moteur (DRVF v2, lecteur rétrocompatible v1) : trace dense de
5: > 512 jetons **132 396 736 → 66 370 408 octets (−49,87 %)**, rejeu `--flux-forcer`
6: > **identique** (perplexité 19,3885 dans les deux cas), et la relecture par
7: > `tools/flux_codec.py` — l'implémentation indépendante — donne exactement les
8: > mêmes 24 576 listes et 22 008 776 neurones actifs. Le rejeu annonce maintenant
9: > ses compteurs (`N listes servies, M manquantes`), ce qui a mis au jour une
10: > trace ancienne dont les clés étaient décalées d'un jeton : elle se rejouait en
11: > silence avec une perplexité fausse (1958,72 au lieu de 19,3885).
12: >
13: > **Et la v3 est faite** (`DRAVE_TRACE_BLOCS=1`) : valeurs i8 + échelle f16 par
14: > bloc de 32 canaux. Mesuré sur la même trace dense : **45 079 930 octets**
15: > (−65,9 % par rapport à la v1, −32,1 % par rapport à la v2), au prix de
16: > **+0,074 % de perplexité 
… [15264 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je vérifie le codec Python et les chiffres KV dans les autres documents.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"version\" tools/flux_codec.py | head -20; echo \"=== KV numbers across docs ===\"; grep -rn \"75 %\\|64 %\\|39 %\\|28 %\\|+0,018\\|+0,023\\|+0,057\\|+0,06\\|3,125\\|5,125\\|2,25\\|+364\\|+384\\|+385\" README.md REPRISE.md d … [124 caractères tronqués]`

  ```
11:    en-tête   "DRVF" · u16 version · u32 n_layer · u32 hidden
39:def encoder(n_layer, hidden, listes, version=VERSION):
41:    out = bytearray(ENTETE.pack(MAGIE, version, n_layer, hidden))
46:            if version == 1:
60:    magie, version, n_layer, hidden = ENTETE.unpack_from(blob, 0)
62:    assert version in (1, 2, 3), f"version {version} inconnue (ce lecteur lit la 1, la 2 et la 3)"
76:        if version == 3:
85:            if version == 3:
95:            if version == 1:
=== KV numbers across docs ===
REPRISE.md:158:| 3 | KV int8 puis int4 | **fait, jusqu'à 8 192** | **échelles par bloc de 32** : int8 +**1,5 %** à 512 (était +7,1 %), **+3,0 % à 8 192** (llama.cpp +0,8 %) ; int4 **+364 % à 8 192** contre +494 % pour llama.cpp — meilleur que la référence, et 1 M tient en int4 (9,7 Go). Prix caché : la passe coûte 864 s (f32) / 1 144 (int8) / 1 461 (int4), la déquantification par élément — c'est ce que le noyau GPU de E4 supprime |
REPRISE.md:180:| KV int4, échelles par bloc | +219 % (512) et +287 % (4 591) — était +384 % et +450 % |
REPRISE.md:181:| KV à 8 192 jetons (longueur de la référence llama.cpp) | f32 **14,2339** · int8 **14,6667 (+3,0 %)** contre +0,8 % chez llama
… [6019 caractères tronqués]
  ```

### 🤖 Assistant

⏵ J'examine le rapport d'attribution KV et la contradiction des 75 %.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-attribution-kv.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-attribution-kv.md</path>
<type>file</type>
<content>
1: # Phase 1.4 — l'écart du cache KV int8 est ENTIÈREMENT dû aux clés
2: 
3: **En une ligne** : à 8 192 jetons, les **valeurs** en int8 ne coûtent rien
4: (1 % de l'écart) et les **clés** coûtent tout (99 %) — l'expérience était écrite
5: dans la feuille de route, la voici faite.
6: 
7: ## Les quatre mesures
8: 
9: Qwen2.5-0.5B-Q8_0, 8 191 jetons notés, contexte 8 192, `--dense --lot 512` :
10: 
11: | configuration | perplexité | écart au f32 | part de l'écart |
12: |---|---|---|---|
13: | cache f32 (référence) | **14,2339** | — | — |
14: | cache int8 complet | 14,6667 | +3,04 % | 100 % |
15: | **clés f32** · valeurs int8 | **14,2372** | **+0,023 %** | **99,2 % expliqué** |
16: | clés int8 · **valeurs f32** | 14,6622 | +3,01 % | 1,0 % seulement |
17: 
18: Reproductible :
19: 
20: ```bash
21: DRAVE_KV_BITS=8 DRAVE_KV_K_F32=1 ./drave models/Qwen2.5-0.5B-Q8_0.gguf \
22:     --ppl /tmp/ids_qwen_long.txt --ctx 8192 --limit 8192 --dense --threads 16 --lot 512
23: ```
24: 
25: ## Ce que ça veut dire
26: 
27: Les deux moitiés du cache n'ont pas du tout le même rôle : u
… [1559 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '150,200p' docs/roadmap.md", "description": "Read roadmap KV attribution section"}`

  ```
Réserve écrite : la ligne « seuil 0,05 » a une perplexité de 2 445 — c'est un
relevé de COÛT, pas de qualité ; le seuil est volontairement brutal.


### Phase 1.4 — l'attribution de l'écart int8 : FAITE

L'écart avec llama.cpp à 8 192 (+3,0 % contre +0,8 %) est attribué. Les deux
drapeaux annoncés (`DRAVE_KV_V_F32`, `DRAVE_KV_K_F32`) ont été terminés, et
l'expérience tournée sur 8 191 jetons :

| configuration | perplexité | écart au f32 | part de l'écart |
|---|---|---|---|
| cache f32 (référence) | **14,2339** | — | — |
| cache int8 complet | 14,6667 | +3,04 % | 100 % |
| **clés f32** · valeurs int8 | **14,2372** | **+0,023 %** | **99,2 % expliqué** |
| clés int8 · **valeurs f32** | 14,6622 | +3,01 % | 1,0 % seulement |

**Tout l'écart est dans les clés.** C'est cohérent avec leur rôle : une clé entre
dans le score, donc dans le softmax — une erreur de clé déplace le poids relatif
d'une position entière ; une valeur ne fait que pondérer la sortie, son erreur se
moyenne.

Conséquence utilisable tout de suite : `DRAVE_KV_BITS=8 DRAVE_KV_K_F32=1` donne un
cache à **75 % de la taille f32** pour +0,02 % de perplexité, là où l'int8 complet
(50 %) coûte +3,0 %. Notre quantificateur de V
… [1467 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je vérifie contexte-long.md (statuts, KV) et vision.md/histoire.md.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '90,175p' docs/contexte-long.md", "description": "Read contexte-long E-series table"}`

  ```
implémentations de référence.

Au-delà du facteur déclaré, la seule réponse honnête reste « extrapolation,
qualité non garantie » — et désormais, ce n'est plus la rotation qui limite le
plus tôt : c'est le préremplissage (§3.a).


## 4. Plan par étapes

| # | étape | état | débloque | coût |
|---|---|---|---|---|
| E1 | **Préremplissage par lots** | **fait** : `gemm_dense_i8` et `gemm_dense_q4` (produits matrice-matrice par tranches), `forward_lot` juste sur dense **et** sur MoE avec regroupement des jetons par expert ; débit bout en bout à chiffrer | 32 k utilisable ; TTFT | le noyau est là ; reste à mesurer et à élargir les tranches |
| E2 | **KV int8** | **fait** (échelle par vecteur, dequantification à la lecture) | ÷4 sur le KV ; 128 k confortable | mesuré : +7,1 % de perplexité (llama.cpp q8_0 : +3,1 %) |
| E3 | **KV int4** | **fait** (nibbles empaquetés) | 1 M tient en RAM (9,7 Go) et en VRAM | mesuré : **+384 %** à 512 jetons, **+364 % à 8 192** — llama.cpp q4_0 : +411 % puis +494 % ; à réserver aux cas où la mémoire manque |
| E4 | **KV déporté sur les 2 GPU** (pagination, préchargement) | **fait** : noyau `attn_kv_*` (tuiles de 32 clés en mémoire partagée, une passe par (
… [4239 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"à faire\\|Rien n'existe\\|rien\\b\\|v2\\|v3\\|v4\\|39 octets\\|10 %\\|22 %\\|f16\\|DRAVE\" docs/vision.md docs/histoire.md docs/contexte-long.md | head -60", "description": "Grep stale statuses in vision/histoire/contexte-l … [5 caractères tronqués]`

  ```
docs/vision.md:12:**mesuré**, ce qui est **raisonné**, et ce qui est **à faire**.
docs/vision.md:46:**mesuré** : en dessous d'environ **22 % de densité**, le push (listes) bat le
docs/vision.md:62:comparer, sans rien reconstruire.
docs/vision.md:76:* **top 10 % des neurones portent 33,1 % de la magnitude** ; seuls **0,08 %** sont
docs/vision.md:121:Deux processus se passent des flux (protocole v4 : version, modes dense / listes /
docs/vision.md:139:   croisement push/pull à ~22 % donne déjà l'ordre de grandeur de ce qu'on
docs/vision.md:147:5. **les mesures à faire** : débit d'un flux sérialisé, latence aller-retour,
docs/vision.md:204:* **ce n'est pas « le sparse gagne toujours »** : le croisement à ~22 % de densité
docs/vision.md:210:  avec ses mesures à faire, et le décodage restera séquentiel ;
docs/vision.md:222:| **3. Répartir sur machines** | **rien** — hypothèse écrite | contrat d'échange, granularité, mesures de débit |
docs/vision.md:236:`drave`, variables `DRAVE_*`, noyaux `drave_gpu.*`, et « Drave » dans les rapports
docs/vision.md:246:anciennes variables ne font plus rien, mais le moteur **le dit** au lieu de
docs/histoire.md:12:| **le virage événementiel** | l'idée qu
… [3497 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je lis les sections concernées de vision.md.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '110,150p' docs/vision.md; echo \"=== 195-247 ===\"; sed -n '195,247p' docs/vision.md", "description": "Read vision sections on distribution status"}`

  ```
(`reports/bilan-multi-materiel.md`) donne le cadre CPU / FPGA / GPU.

Ce qui reste ouvert : la **politique** de placement (aujourd'hui : des seuils
codés en dur, réglés à la main par la mesure) et le **déport du top-k** dans le
noyau d'attention — le dernier chemin qui retombe sur le CPU.

---

## 4. Axe 3 — Répartir sur plusieurs machines

**Le transport existe, et c'est l'axe où le projet a le plus avancé depuis.**
Deux processus se passent des flux (protocole v4 : version, modes dense / listes /
blocs / **lot**, contrat d'activation complet), le découpage est fidèle au bit
près (`0,00e0`), le préremplissage par lots tient en un aller-retour par lot, et
`colab/` contient de quoi faire la démonstration sur un runtime distant. Ce qui
reste : le lot en listes, l'ordonnanceur de placement, le flux de poids depuis le
NVMe. La
raison est dans la nature de la représentation : si le calcul est un flux de
listes adressées, alors **une liste est une unité de travail autonome**, avec ses
entrées (les activations), sa sortie (les activations produites) et sa
dépendance (les poids d'une couche). Distribuer, c'est router des listes.

Ce qu'il faut définir, dans l'ordre :

1. **le contrat d'éch
… [3698 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je vérifie la couverture du transport et des nouveaux drapeaux dans les documents de référence.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== README mentions ===\"; grep -n \"réparti\\|transport\\|flux-serveur\\|colab\\|--lot\\|options-actives\\|DRVF\\|trace-flux\\|KV_K_F16\" README.md | head -20; echo \"=== options-actives dans docs/ ===\"; grep -rn \"options-a … [327 caractères tronqués]`

  ```
=== README mentions ===
226:| **4 cartes FPGA** (modèle réparti) | **10,8** | **92,8** |
=== options-actives dans docs/ ===
REPRISE.md:357:recommandation de fond — un `--options-actives` qui imprime les réglages
REPRISE.md:383:- **`--options-actives`** : un tableau de bord qui imprime, APRÈS toutes les
REPRISE.md:402:  bord `--options-actives` s'exécutait AVANT les affectations en perplexité (il
reports/rapport-drapeaux-ignores.md:196:## 8. Recommandation : un tableau de bord `--options-actives`, et trois garde-fous
reports/rapport-drapeaux-ignores.md:198:**L'idée simple** : un drapeau `--options-actives` (et `--options-strict`) qui imprime, au
reports/rapport-session-2026-09-30.md:17:| **Drapeaux ignorés** | **46 sur 110** l'étaient dans au moins un mode ; neuf corrigés, tableau de bord `--options-actives` ajouté | `rapport-drapeaux-ignores.md` |
=== --lot / --flux-liste / --flux-blocs dans docs ===
REPRISE.md:249:| `DRAVE_FLUX_VERIF=1` | vérifie l'écart entre l'activation calculée et celle que la trace impose | 1,5e-5 en v2 ; **muet dès que `--lot > 1`** (le rejeu par lots passe par `flux_lot`) |
REPRISE.md:398:  `--lot`, pair factice qui ne lisait pas le mode lot, modes sparse i
… [4014 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Un nouveau document est apparu — je liste les fichiers récents et l'examine.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la docs/ reports/ | head -60; echo \"=== git status ===\"; git status --porcelain | head -20; echo \"=== date ===\"; date", "description": "Re-list docs and reports for new files"}`

  ```
docs/:
total 248
drwxr-xr-x. 1 stephane stephane   474 30 sep 15:12 .
drwxr-xr-x. 1 stephane stephane   598 30 sep 12:19 ..
-rw-r--r--. 1 stephane stephane  6630 30 sep 13:00 colab-reparti.md
-rw-------. 1 stephane stephane  8505 30 sep 08:44 comparaison-spiking.md
-rw-------. 1 stephane stephane 28893 30 sep 13:08 contexte-long.md
-rw-------. 1 stephane stephane 16030 28 sep 11:57 convertisseur.md
-rw-r--r--. 1 stephane stephane  9888 30 sep 13:42 format-flux.md
-rw-------. 1 stephane stephane  4360 30 sep 13:08 histoire.md
-rw-r--r--. 1 stephane stephane  6261 30 sep 15:11 plan-gpu-topk.md
-rw-------. 1 stephane stephane 38716 30 sep 08:44 plan-mla-vision.md
-rw-------. 1 stephane stephane 29270 30 sep 15:12 plan-mode4-lot-listes.md
-rw-------. 1 stephane stephane 23413 30 sep 13:07 plan-prefill-reparti.md
-rw-------. 1 stephane stephane 11951 27 sep 16:09 programme-recherche.md
-rw-------. 1 stephane stephane 22099 30 sep 13:41 roadmap.md
-rw-------. 1 stephane stephane   108 30 sep 10:34 .roadmap.md.kate-swp
-rw-------. 1 stephane stephane 13057 30 sep 13:08 vision.md

reports/:
total 348
drwxr-xr-x. 1 stephane stephane  1902 30 sep 13:13 .
drwxr-xr-x. 1 stephane stephane   598
… [2933 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je lis les deux plans apparus à l'instant (mode 4, GPU top-k).

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && head -60 docs/plan-mode4-lot-listes.md; echo \"=================== GPU TOPK ===================\"; head -60 docs/plan-gpu-topk.md", "description": "Read headers of the two new plan docs"}`

  ```
# Spécification — mode 4 : le **lot en listes** (protocole v5)

> **État : non écrit.** Ce document est la spécification à implémenter ; aucun
> fichier de code n'a été touché pour l'écrire. Il suppose connus
> `docs/format-flux.md` (protocole v4, modes 0–3) et `docs/plan-prefill-reparti.md`
> (le mode 3, mis en œuvre, et ses leçons). Les numéros de ligne sont ceux de
> l'arbre au moment de la rédaction (`VERSION_FLUX = 4`, `TAILLE_TETE = 79`,
> `MODE_LOT = 3`).

**En une ligne** : le mode 3 transporte `t` états en f32 dense — 3 589 octets par
jeton à `t = 16` pour Qwen2.5-0.5B ; le mode 4 transporte **les mêmes `t` états
encodés en listes à échelle par bloc de 32 canaux**, soit ≈ 1 530 octets par état
au seuil 0,01, **÷2,3 sur le fil**, au prix exact que le mode 2 paie déjà
(2,7e-2 d'écart à 256 jetons, 1,3e-2 à 1 024). Le mode 4 ne touche ni au calcul,
ni au cache KV, ni à la norme finale : il s'arrête au transport.

## 0. Décisions d'architecture (à ne pas rediscuter)

| question | décision | pourquoi |
|---|---|---|
| nouveau mode ou nouveau champ ? | **mode 4** (`MODE_LOT_LISTES`), en-tête **inchangé** (79 octets) | le corps est variable par construction (chaque état a son nom
… [6637 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je vérifie systématiquement les chemins cités en backticks et les rapports référencés.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport re, os, glob\nfiles = ['README.md','REPRISE.md','Qtrinet-bootstrap.md'] + glob.glob('docs/*.md') + glob.glob('reports/*.md') + glob.glob('colab/*.md')\npat = re.compile(r'`([^`\\s]+\\.(?:md|sh|py|rs|cu|ptx|c … [745 caractères tronqués]`

  ```
=== CHEMINS CITÉS INTROUVABLES (hors .md, liens déjà vérifiés) ===
bpe_np.py  <-  reports/rapport-inference.md:162, reports/bilan-multi-materiel.md:94
clip.cpp  <-  docs/plan-mla-vision.md:482, docs/plan-mla-vision.md:493, docs/plan-mla-vision.md:558, docs/plan-mla-vision.md:675
colab-reparti.md  <-  reports/rapport-coherence-docs.md:223
comparaison-spiking.md  <-  docs/programme-recherche.md:57
config.json  <-  reports/rapport-gpt-oss-perplexite.md:34
drave_gpu.cu  <-  REPRISE.md:417
flux_codec.py  <-  reports/rapport-compacite-trace.md:222, reports/rapport-compacite-trace.md:228, reports/rapport-coherence-docs.md:27, reports/rapport-coherence-docs.md:226
ggml/src/ggml-cpu/ops.cpp  <-  docs/plan-mla-vision.md:575
gpt_oss/torch/model.py  <-  reports/rapport-gpt-oss-perplexite.md:102
gpu.rs  <-  reports/rapport-drapeaux-ignores.md:66
gpu/qtrinet_gpu.cu  <-  docs/histoire.md:34
llama.cpp  <-  docs/convertisseur.md:206
main.rs  <-  docs/plan-prefill-reparti.md:355, docs/plan-mode4-lot-listes.md:409, docs/plan-mode4-lot-listes.md:410, docs/plan-mode4-lot-listes.md:411
model.rs  <-  docs/plan-gpu-topk.md:83, docs/plan-mode4-lot-listes.md:272, reports/rapport-coherence-docs.md:24, report
… [1628 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"=== rapports cités ===\"; grep -rhoE '`?reports/[a-z0-9-]+\\.md' README.md REPRISE.md docs/*.md reports/rapport-session-2026-09-30.md | tr -d '`' | sort -u | while read f; do [ -f \"$f\" ] && echo \"OK   $f\" || echo \"MORT $f … [58 caractères tronqués]`

  ```
=== rapports cités ===
OK   reports/bilan-multi-materiel.md
OK   reports/rapport-aiguille.md
OK   reports/rapport-analyse-flux.md
OK   reports/rapport-attention-creuse.md
OK   reports/rapport-attribution-kv.md
OK   reports/rapport-campagne-parcimonie.md
OK   reports/rapport-capteur-hebbien.md
OK   reports/rapport-cpu-aer.md
OK   reports/rapport-croisement-push-pull.md
OK   reports/rapport-drapeaux-ignores.md
OK   reports/rapport-encodage.md
OK   reports/rapport-eparsite.md
OK   reports/rapport-gpt-oss-perplexite.md
OK   reports/rapport-greffon.md
OK   reports/rapport-inference.md
OK   reports/rapport-localite-activation.md
OK   reports/rapport-minimal.md
MORT reports/rapport-mode4-lot-listes.md
OK   reports/rapport-mur-memoire-4bits.md
OK   reports/rapport-optimisations.md
OK   reports/rapport-parcimonie-imposee.md
OK   reports/rapport-passage-a-l-echelle.md
MORT reports/rapport-pe-evenementiel.md
OK   reports/rapport-phase3-reparti.md
OK   reports/rapport-placement-bits-kv.md
OK   reports/rapport-precision.md
OK   reports/rapport-prefill-par-lots.md
OK   reports/rapport-prefill-reparti.md
OK   reports/rapport-programme-evolutif.md
OK   reports/rapport-transport-liste.md
OK   repor
… [26 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je vérifie les renvois FPGA dans vision.md et le plan mode 4.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '100,112p' docs/vision.md; echo \"=== histoire 28-40 ===\"; sed -n '28,40p' docs/histoire.md; echo \"=== plan mode4 fin ===\"; sed -n '400,424p' docs/plan-mode4-lot-listes.md", "description": "Check FPGA refs and mode4 report  … [5 caractères tronqués]`

  ```
| attention complète | noyau GPU, décodage **et** préremplissage | 22,16 → **3,29 ms/jeton** (÷6,7) ; préremplissage **×2,8** |
| projections Q8_0 (> 8 Mo) | GPU, opt-in | tête : 15,6 → 6,2 ms/jeton |
| tête Q6_K | GPU | 7,58 → **3,60 ms/jeton** |
| experts MXFP4 | cache VRAM LRU | **+6 %** — mesuré, verdict : ne pas activer tel quel |
| cache KV (hôte) | pagination à la demande | contexte 1 M : **0,03 Go** au lieu de 25,77 Go |

La leçon de cet axe est une règle de placement : **on place un opérateur là où
son flux coûte le moins cher**, et on le vérifie. Le même raisonnement mène au
FPGA : le projecteur événementiel sur Stratix V existe et a été synthétisé
(`reports/rapport-pe-evenementiel.md`), et le bilan multi-matériel
(`reports/bilan-multi-materiel.md`) donne le cadre CPU / FPGA / GPU.

Ce qui reste ouvert : la **politique** de placement (aujourd'hui : des seuils
=== histoire 28-40 ===
**Changé, partout** (61 fichiers de contenu, plus les chemins) :

| avant | après |
|---|---|
| crate `qtrinet-core/` | `drave-core/` |
| binaire `qtrinet-core` | **`drave`** |
| noyaux `gpu/qtrinet_gpu.cu` / `.ptx` | `gpu/drave_gpu.cu` / `.ptx` |
| variables `QT_*` | **`DRAVE_*`** (voir le tab
… [3395 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je vérifie le tableau de bord --options-actives et l'absence de --options-strict.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src && grep -n \"options_actives\\|options_strict\\|options-actives\\|options-strict\" main.rs; echo \"=== appels ===\"; grep -n \"tableau_bord\\|fn options\" main.rs | head", "description": "Check options-actives implementat … [11 caractères tronqués]`

  ```
340:/// **Tableau de bord des réglages en vigueur** (`--options-actives`), lus sur le
350:fn options_actives(mdl: &model::Model, mode: &str, ctx_impose: bool, dense: bool, keep: f32) {
408:    /// `--options-actives` : imprime, APRÈS toutes les affectations, les réglages
412:    options_actives: bool,
507:            "--options-actives" => { o.options_actives = true; 1 }
605:        eprintln!("[options] (une faute de frappe suffit — `--options-actives` montre \
626:    let montre_options = opt.options_actives;
699:        options_actives(&mdl, "inférence", ctx_impose, dense, keep);
1822:    if opt.options_actives { options_actives(&mdl, "nœud moteur du flux", opt.ctx_impose, true, opt.keep); }
1923:    if opt.options_actives { options_actives(&mdl, "pilote du flux", opt.ctx_impose, true, opt.keep); }
2957:    let montre_options = opt.options_actives;
3080:        options_actives(&mdl, "perplexité", ctx_impose, dense, keep);
=== appels ===
350:fn options_actives(mdl: &model::Model, mode: &str, ctx_impose: bool, dense: bool, keep: f32) {
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src && sed -n '1070,1115p' model.rs", "description": "Read KV K f16 code"}`

  ```
pub cap: usize,
    pub hd: usize,
    kf: Vec<f32>,
    vf: Vec<f32>,
    /// `DRAVE_KV_K_F16=1` : les CLÉS sont stockées en f16, sans quantification
    /// par bloc. Deux octets par valeur — plus que l'int8 (1,125 avec son échelle)
    /// mais bien moins que le f32 (4) — et une précision RELATIVE de 2⁻¹¹ par
    /// valeur, là où l'int8 à échelle par bloc a une erreur ABSOLUE de bloc/254
    /// qui écrase les petits canaux. C'est le « meilleur quantificateur de clés »
    /// que la feuille de route appelle, sans rotation ni échelle par tête.
    kp: Vec<u16>,
    pub k_f16: bool,
    /// Quantifié : un octet par valeur en 8 bits, **deux nibbles par octet en
    /// 4 bits** (même disposition que Q4_0/MXFP4 : nibble bas = indice pair).
    kq: Vec<u8>,
    vq: Vec<u8>,
    /// Échelles **par bloc de 32**, comme Q8_0 — et non une par vecteur : c'est
    /// ce qui explique l'écart mesuré avec llama.cpp (+5,2 % de perplexité
    /// contre +0,8 % pour son cache q8_0).
    sk: Vec<f32>,
    sv: Vec<f32>,
    nb: usize,
}

impl KvCache {
    pub fn new(bits: u32, n_kv: usize, ctx: usize, hd: usize) -> Self {
        let bits = if bits >= 32 { 32 } else if bits > 4 { 8 } else { 4 }
… [986 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je balaie tous les documents pour les chiffres périmés (versions, en-tête, octets).

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"39 octets\\|3 623\\|3623\\|2 268\\|1 568\\|1 589\\|917 543\\|917 583\\|protocole v2\\|protocole v3\\|DRVF v1\\|version 2 par défaut\\|VERSION_FLUX\" --include='*.md' . | grep -v journal/ | grep -v \"rapport-coherence-docs\ … [74 caractères tronqués]`

  ```
./reports/rapport-minimal.md:72:| 70B — 4 bits | 35000.0 Mo | 3623.188 | 0.3 | 156 | 4680 |
./reports/rapport-transport-liste.md:4:3 623** à seuil 5 %, et **1 568** avec des indices par écarts — mais jeter des
./reports/rapport-transport-liste.md:10:Deux modes dans le même en-tête de 39 octets — magie, version, mode, plage,
./reports/rapport-transport-liste.md:15:| 0 · dense f32 | `896 × f32` | **3 623** (39 + 3 584) |
./reports/rapport-transport-liste.md:25:| dense f32 | 100 % | 3 623 | 3 623 | 144,8289 | **144,8289** | **0,00e0** |
./reports/rapport-transport-liste.md:26:| listes 0,00 | 100,0 % (896) | 3 623 | 3 623 | 144,8289 | 141,0539 | 2,6e-2 |
./reports/rapport-transport-liste.md:118:octets contre 3 623, et les deux modes sont de toute façon « taille du dense ».
./reports/rapport-transport-liste.md:132:| dense f32 | — | 100 % | 3 623 | **0,00e0** |
./reports/rapport-transport-liste.md:133:| blocs | 0,01 | 78,6 % | 2 268 | 2,7e-2 |
./reports/rapport-transport-liste.md:151:| 256 | 2,74e-2 | 2 268 | 78,6 % |
./reports/rapport-transport-liste.md:152:| **1 024** | **1,32e-2** | **1 589** | 79,8 % |
./reports/rapport-transport-liste.md:176:| dense f32 | 3 623 | 0,00e0 | 18,0206 |

… [3889 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && head -30 reports/rapport-drapeaux-ignores.md; echo \"=== mentions options-actives dans le rapport drapeaux ===\"; sed -n '190,235p' reports/rapport-drapeaux-ignores.md", "description": "Check drapeaux report banner and recommendation … [2 caractères tronqués]`

  ```
# Drapeaux et variables « analysés mais jamais appliqués » — audit systématique
> **Addendum (mêmes jour, après l'audit).** Les défauts n°1 (top-k non transportés
> ni appliqués dans les modes flux), n°2 (`--keep` en `--ppl`), n°3 (`--ffn-gain`
> en `--infer`) et la moitié basse du tableau (`--threads` en FS/PR/BM, `--hebb-q`,
> `--hebb-out`, `--plan` sans `--ctx`, précédence de fenêtre, pas de 2 du mode par
> défaut) ont été **corrigés** dans les commits `7522289` et le suivant. Le
> protocole de flux passe en **version 4** : le contrat d'activation transporte
> désormais aussi les sept top-k par projection, `--attn-topk`, `--qk-topk` et
> `--moe-topk`. Les sections ci-dessous décrivent l'état AVANT correction — elles
> restent la référence de ce qui a été trouvé, et la liste de ce qui reste
> (`--banc-vision` sans `Options`, `--bits` du noyau GPU, etc.).


**Révision auditée** : `drave-core/src/main.rs` sha256 `1726f9ac3665c3ce…` (2 999 lignes),
`drave-core/src/model.rs` sha256 `1d7eacc506db6cab…` (3 675 lignes), 30/09 11:54.
Le dépôt était en cours d'édition pendant l'audit (zone flux / préremplissage réparti) :
les numéros de ligne cités sont ceux de cette révision, et **les ch
… [3664 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je lis la section 5 de REPRISE (résultats, KV, contexte long).

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/REPRISE.md", "limit": 95, "offset": 131}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/REPRISE.md</path>
<type>file</type>
<content>
131: ---
132: 
133: ## 5. Règles de méthode (chacune a coûté une erreur)
134: 
135: 1. **Mesurer avant de conclure.** Le croisement push/pull était annoncé à 10 %,
136:    il est à 22 %. Dérouler un noyau « évident » n'a rien donné : le chemin était
137:    au mur mémoire, pas mal écrit.
138: 2. **La double quantification est le piège le plus cher** : +12 % de perplexité
139:    sur Q4_0, et une simulation de précision qui annonçait 19,96 là où le format
140:    réel donne 19,30.
141: 3. **Une hypothèse se teste, elle ne se défend pas.** Trois ont été réfutées cette
142:    session : cache KV pour l'attention (c'était la vectorisation), rotary partiel
143:    pour gpt-oss (185 → 1 095), YaRN (184,9 contre 39,8 sans).
144: 4. **Vérifier quel chemin est actif** avant de déboguer un chiffre : la trace
145:    `[config]` au chargement dit quelles particularités ont été reconnues.
146: 5. **Ne pas conclure sur 255 jetons** : l'écart peut être du bruit ; 510 minimum.
147: 6. **Ne pas laisser un dépôt cassé** pour finir une refactorisation : revenir au
148:    dernier état valide est une op
… [9670 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je compte les commits du jour et vérifie les affirmations de la session.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --since='2026-09-30 00:00' --until='2026-09-30 23:59' --format='%h %ad %s' --date=format:'%H:%M' | wc -l; echo \"--- first/last ---\"; git log --since='2026-09-30 00:00' --format='%h %ad %s' --date=format:'%H:%M' | tail -3; g … [128 caractères tronqués]`

  ```
73
--- first/last ---
b97d129 08:48 Drave : renommage complet (crate, binaire, variables, documents)
15c4c8c 08:36 Drave : document de vision, et le nom dans le README
d349063 07:18 vision : la permutation colonne-majeur des couches fenêtrées est implémentée
a383cd7 15:11 Plan du noyau GPU de top-k (phase 1.1), chiffré, et la perplexité attendue du notebook
90a74a6 15:09 Colab clé en main : le nœud local, les trois tunnels, et un texte réel dans le notebook
6c1aecf 14:09 REPRISE : la frontière du cache KV et les deux gains du mode lot
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '25,50p' drave-core/src/main.rs", "description": "Read rename warning code"}`

  ```
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() < 2 {
        eprintln!("usage: drave-core <modele.gguf> [--matrix NOM] [--threads N]");
        eprintln!("       drave-core <modele.gguf> --infer (--ids 1,2,3 | --prompt TEXTE)");
        eprintln!("                    [--n 32] [--temp 0] [--ctx 512] [--threads N]");
        std::process::exit(1);
    }
    // Une seule analyse, puis un aiguillage : `--plan`, `--tokenize`,
    // `--ppl`/`--ppl-texte` et `--infer` partagent désormais la même structure
    // d'options, donc les mêmes drapeaux.
    // Les variables d'environnement ont été renommées QT_* -> DRAVE_* : un
    // ancien nom encore présent dans un script ne ferait RIEN, en silence. On le
    // dit, plutôt que de laisser croire que l'option est active.
    if let Some((vieux, _)) = std::env::vars().find(|(k, _)| k.starts_with("QT_")) {
        eprintln!("[attention] {vieux} est l'ancien nom d'une variable d'environnement : \
elles s'appellent maintenant DRAVE_* (voir docs/histoire.md). Rien n'a été appliqué.");
    }
    let opt = analyser(&args);
    let _ = MODELE.set(args[1].clone());
    // Plusieurs modes demandés : l'aiguilla
… [162 caractères tronqués]
  ```

- **bash** `{"command": "env | grep -c '^QT_'; env | grep '^QT_' | head -3; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"commits jusqu'à 13:37:\"; git log --until='2026-09-30 13:37' --since='2026-09-30 00:00' --oneline | wc -l; echo \"commits jusqu'à 14:09:\"; git log --until='2026-09-30 14:09'  … [113 caractères tronqués]`

  ```
2
QT_IM_SWITCHER=imsw-multi
QT_IM_MODULE=xim
commits jusqu'à 13:37:
64
commits jusqu'à 14:09:
70
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"10:06→13:37:\"; git log --since='2026-09-30 10:06' --until='2026-09-30 13:37' --oneline | wc -l; echo \"10:06→14:09:\"; git log --since='2026-09-30 10:06' --until='2026-09-30 14:09' --oneline | wc -l; echo \"11:46→13:37:\"; gi … [130 caractères tronqués]`

  ```
10:06→13:37:
57
10:06→14:09:
63
11:46→13:37:
34
  ```

### 🤖 Assistant

⏵ Je vérifie le kit Colab et ses renvois.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la colab/ tools/ | head -40; echo \"=== renvois colab dans docs ===\"; grep -rn \"colab/\" docs/*.md REPRISE.md README.md | head -20", "description": "List colab and tools files, check refs"}`

  ```
colab/:
total 16
drwxr-xr-x. 1 stephane stephane   56 30 sep 12:20 .
drwxr-xr-x. 1 stephane stephane  598 30 sep 12:19 ..
-rw-r--r--. 1 stephane stephane 8858 30 sep 15:11 Drave-reparti.ipynb
-rw-r--r--. 1 stephane stephane 3625 30 sep 13:01 README.md

tools/:
total 184
drwxr-xr-x. 1 stephane stephane   658 30 sep 15:09 .
drwxr-xr-x. 1 stephane stephane   598 30 sep 12:19 ..
-rwx--x--x. 1 stephane stephane  6744 30 sep 08:44 aiguille.py
-rwxr-xr-x. 1 stephane stephane  3757 30 sep 10:35 analyse_flux.py
-rwx--x--x. 1 stephane stephane  8444 27 sep 11:40 archive_sessions.py
-rwxr-xr-x. 1 stephane stephane  3107 30 sep 15:09 colab_cote_local.sh
-rw-------. 1 stephane stephane  3401 28 sep 15:22 compare_logits.py
-rwxr-xr-x. 1 stephane stephane  3345 30 sep 08:58 diff_flux.py
-rwxr-xr-x. 1 stephane stephane  6144 30 sep 12:28 flux_codec.py
-rw-------. 1 stephane stephane  3264 30 sep 08:44 harmony_canonique.py
-rw-r--r--. 1 stephane stephane  2645 30 sep 08:44 make_patch.py
-rw-------. 1 stephane stephane 10607 29 sep 20:07 mla_synthetique.py
-rwxr-xr-x. 1 stephane stephane  5216 30 sep 12:43 pair_factice.py
-rwxr-xr-x. 1 stephane stephane  2269 30 sep 12:20 preparer_colab.sh
-rwxr-xr-
… [1237 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je vérifie l'analyse de --flux-serveur (port seul vs hôte:port).

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src && grep -n \"flux_serveur\\|rsplit_once\" main.rs | head -20; echo \"===\"; sed -n '/fn run_flux_serveur/,/^}/p' main.rs | head -40", "description": "Check flux-serveur address parsing"}`

  ```
51:        (opt.flux_serveur.is_some(), "--flux-serveur"),
63:    if let Some(adresse) = opt.flux_serveur.clone() { run_serveur_flux(opt, &adresse); return; }
419:    flux_serveur: Option<String>,
506:            "--flux-serveur" => { o.flux_serveur = Some(suivant(i).clone()); 2 }
1811:    let (hote, port) = match adresse.rsplit_once(':') {
===
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src && sed -n '1805,1830p' main.rs", "description": "Read flux-serveur address resolution"}`

  ```
/// flux reçu et renvoie le flux résultant. Un seul client à la fois — c'est un
/// banc d'essai, pas un service.
fn run_serveur_flux(opt: Options, adresse: &str) {
    // `port` reste localhost ; `hôte:port` écoute sur l'interface nommée
    // (« 0.0.0.0:5599 » pour un pair distant). Le pair distant est le cas de la
    // phase 3.4 : un nœud Colab, ou une autre machine du réseau.
    let (hote, port) = match adresse.rsplit_once(':') {
        Some((h, p)) => (h.to_string(), p.parse().expect("port invalide")),
        None => ("127.0.0.1".to_string(), adresse.parse().expect("port invalide")),
    };
    let chemin = modele_chemin();
    // Le contexte du nœud moteur suit `--ctx` : figé à 4096, il faisait payer au
    // pair des tampons d'attention seize fois plus grands que le banc (mesuré :
    // 4,8 s contre 1,7 s pour le même calcul, à contexte 256).
    let ctx = if opt.ctx_impose { opt.ctx } else { 4096 };
    let mut mdl = model::Model::load(&chemin, ctx, fils(&opt), true, opt.keep, false, 0, 0);
    appliquer_quantification(&mut mdl, &opt);
    if opt.options_actives { options_actives(&mdl, "nœud moteur du flux", opt.ctx_impose, true, opt.keep); }
    let hidden = mdl.cf
… [529 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je vérifie les derniers points du plan préremplissage et du format.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '336,362p' docs/plan-prefill-reparti.md; echo \"=== fin du plan ===\"; sed -n '410,424p' docs/plan-prefill-reparti.md", "description": "Check plan-prefill references and tail"}`

  ```
```bash
# test unitaire du codec, sans modèle : l'aller-retour est identique à l'octet
cargo test -p drave-core tests_flux_lot
```

Les deux premiers critères sont **exacts** ; en mode listes (hors de ce plan),
l'écart serait au contraire du même ordre que le chemin par jeton (2,7e-2 pour
`--flux-blocs --act-thresh 0.01`) : ne pas confondre les deux régimes.

## 5. Plan d'implémentation ordonné

| # | fichier | quoi | critère de succès vérifiable |
|---|---|---|---|
| 1 | `main.rs:1231-1251` | `VERSION_FLUX = 3`, `MODE_LOT = 3` | un binaire v3 et un binaire v2 se refusent au 1er message en nommant les deux versions ; deux v3 en mode 0 dense : écart 0,00e0 inchangé |
| 2 | `main.rs:1277-1345, 1400-1486` | `Flux.n`, `ChargeFlux::Lot`, `plat()`, bras `MODE_LOT` de `recevoir_flux`, `envoyer_lot` | `tests_flux_lot` : encode→décode rend les mêmes f32 à l'octet près, taille `39 + 4·t·hidden` ; un corps tronqué rend une erreur, pas une panique |
| 3 | `model.rs:728, 1546, 2091-2111` | `emb_imposee_lot` + `forward_lot_impose` | test unitaire : `forward_lot_impose(pos, embeddings_du_lot)` == `forward_lot(jetons, pos)` **exactement** |
| 4 | `main.rs:1491-1552` | branche lot de la boucle serv
… [1872 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je vérifie le binaire et le modèle disponibles pour deux courtes exécutions autorisées.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la drave-core/target/release/drave 2>/dev/null; ls -la models/ 2>/dev/null; ls -la /tmp/ids_qwen.txt /tmp/ids_qwen_long.txt /tmp/wt2_txt.txt 2>/dev/null; pgrep -x drave | wc -l; ps -o pid,etime,pcpu,args -p $(pgrep -x drave | hea … [84 caractères tronqués]`

  ```
-rwxr-xr-x. 2 stephane stephane 1593672 30 sep 13:36 drave-core/target/release/drave
total 863324
drwxr-xr-x. 1 stephane stephane        88 25 sep 17:13 .
drwxr-xr-x. 1 stephane stephane       598 30 sep 12:19 ..
-rw-r--r--. 1 stephane stephane 352972352 25 sep 17:13 Qwen2.5-0.5B-Q4_0.gguf
-rw-r--r--. 1 stephane stephane 531068480 25 sep 16:52 Qwen2.5-0.5B-Q8_0.gguf
-rw-r--r--. 1 stephane stephane 79500 29 sep 15:15 /tmp/ids_qwen_long.txt
-rw-r--r--. 1 stephane stephane 21380 28 sep 11:30 /tmp/ids_qwen.txt
-rw-r--r--. 1 stephane stephane 20000 28 sep 11:30 /tmp/wt2_txt.txt
1
    PID     ELAPSED %CPU COMMAND
 656529       01:28 1747 ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --ppl /tmp/ids_qwen_long.txt --ctx 4096 --limit 4096 --dense --threads 16 --lot 512
  ```

### 🤖 Assistant

⏵ Deux courtes exécutions autorisées pour vérifier trace v2/v3 et le tableau de bord.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 120 ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --ppl /tmp/ids_qwen.txt --ctx 256 --limit 4 --dense --threads 2 --options-actives --trace-flux /tmp/verif_v2.bin 2>&1 | tail -25; echo \"EXIT=$?\"", "descrip … [74 caractères tronqués]`

  ```
[attention] QT_IM_SWITCHER est l'ancien nom d'une variable d'environnement : elles s'appellent maintenant DRAVE_* (voir docs/histoire.md). Rien n'a été appliqué.
/tmp/ids_qwen.txt : 4 tokens, fenêtres de 256
[config] cache KV : 32 bits, 0.01 Go pour 256 jetons
[modele] 24 couches chargées en 827.119745ms — listes 0.00 Go , 2 threads
[config] 24 couches, hidden 896 · 
[config] puits appris sur 0/24 couches · n_rot 64 · ffn 4864 · experts 0
[config] rotation : RoPE simple (le modèle ne déclare pas YaRN)
[trace] flux enregistré dans /tmp/verif_v2.bin
[options] mode perplexité · contexte 256 (imposé) · dense true · keep 1.000
[options] activation : niveaux 32767 · seuil 0 · k-WTA 0 · renorm false
[options] top-k : attn 0 · q·k 0 · MoE 0 · par projection [0, 0, 0, 0, 0, 0, 0]
[options] couches 0..24 · flux brut false · trace true · rejeu false
[options] fenêtre 0 · motif 0 · seuil push 0.22 · lot 1 · ffn_gain None · hebb false
[options] cache KV : 32 bits · f16 avant false
       3 tokens notés — perplexité cumulée 1929.323  (4.3 tok/s)
[trace] 192 listes · 171554 neurones actifs · 1 Mo

=== perplexité 1929.3230 sur 3 tokens (0 événements, 0.7 s) ===
    4.3 tok/s effectifs (avant + têt
… [501 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je lance la seconde exécution (trace v3) et lis la fonction du tableau de bord.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && DRAVE_TRACE_BLOCS=1 timeout 120 ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --ppl /tmp/ids_qwen.txt --ctx 256 --limit 4 --dense --threads 2 --trace-flux /tmp/verif_v3.bin 2>&1 | grep -E \"trace|attention\" ; echo  … [352 caractères tronqués]`

  ```
[attention] QT_IM_SWITCHER est l'ancien nom d'une variable d'environnement : elles s'appellent maintenant DRAVE_* (voir docs/histoire.md). Rien n'a été appliqué.
[trace] flux enregistré dans /tmp/verif_v3.bin
[trace] 192 listes · 166206 neurones actifs · 0 Mo
    attention : 0.00 M paires (requête, clé) par token
    part de l'attention dans le flux d'événements : 100.0 %
    postes (ms/token) : projets-attn 12.76 | rope 0.82 | attention 0.14 | proj+mlp 142.53 | somme 156.25 | reste (tête + échantillonnage) 22.60
    dont attention : scores 0.04 | softmax 0.03 | somme pondérée + écriture KV 0.08
EXIT=0
/tmp/verif_v2.bin b'DRVF' version 2 n_layer 24 hidden 896 taille 517366
/tmp/verif_v3.bin b'DRVF' version 3 n_layer 24 hidden 896 taille 346636
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src && sed -n '336,400p' main.rs", "description": "Read options_actives function"}`

  ```
/// `argv` ni à supposer que le modèle est en position 1.
static MODELE: std::sync::OnceLock<String> = std::sync::OnceLock::new();
fn modele_chemin() -> String { MODELE.get().cloned().unwrap_or_default() }

/// **Tableau de bord des réglages en vigueur** (`--options-actives`), lus sur le
/// MODÈLE après toutes les affectations.
///
/// Pourquoi il existe : le défaut le plus coûteux de ce dépôt n'est pas un calcul
/// faux, c'est un drapeau qui ne fait rien. Huit ont été corrigés en une session
/// (`--keep` en perplexité, `--ffn-gain` en inférence, les top-k dans les modes
/// flux, `--trace-flux` en inférence, `--threads` figé…), et chacun était
/// INVISIBLE : la sortie ne disait nulle part quelle valeur agissait. Ici, elle
/// le dit — et une valeur qu'on ne voit pas bouger est une valeur qui ne sert à
/// rien.
fn options_actives(mdl: &model::Model, mode: &str, ctx_impose: bool, dense: bool, keep: f32) {
    let oui = |b: bool| if b { "imposé" } else { "défaut" };
    println!("[options] mode {mode} · contexte {} ({}) · dense {} · keep {:.3}",
             mdl.ctx, oui(ctx_impose), dense, keep);
    println!("[options] activation : niveaux {:.0} · seuil {} · k-WTA {} · renorm 
… [2320 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je vérifie la valeur exacte de `n` par mode dans l'émetteur.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src && sed -n '1620,1670p' main.rs", "description": "Read emitter n computation per mode"}`

  ```
let paires = encoder_paires_blocs(&idx, &val);
        // La longueur est écrite : avec les échappements, elle n'est pas
        // déductible du nombre de paires, et un décodeur qui la suppose lit
        // hors du tampon.
        c.extend_from_slice(&(paires.len() as u32).to_le_bytes());
        c.extend_from_slice(&paires);
        (idx.len(), 0f32, c)
    } else if mode == MODE_LISTE {
        let (idx, val, ech) = mdl.expect("modèle requis pour quantifier un flux")
                                 .flux_en_liste(actifs);
        let mut c = Vec::with_capacity(idx.len() * 4);
        for (&i, &v) in idx.iter().zip(val.iter()) {
            c.extend_from_slice(&i.to_le_bytes());
            c.extend_from_slice(&v.to_le_bytes());
        }
        (idx.len(), ech, c)
    } else {
        let mut c = Vec::with_capacity(actifs.len() * 4);
        for v in actifs { c.extend_from_slice(&v.to_le_bytes()); }
        (actifs.len(), 0f32, c)
    };
    let mut tete = Vec::with_capacity(TAILLE_TETE);
    tete.extend_from_slice(&MAGIE_FLUX.to_le_bytes());
    tete.push(VERSION_FLUX);
    tete.push(mode);
    tete.extend_from_slice(&debut.to_le_bytes());
    tete.extend_from_slice(&fin.to_
… [1147 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je vérifie le message d'erreur de version réellement imprimé.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src && grep -n \"arrêt\\|flux en version\" main.rs | head -10", "description": "Check version error message prefix"}`

  ```
430:    /// s'arrête. Sert à préparer un chemin qu'on ne sait pas encore lire — le
1721:            format!("flux en version {version}, cette build parle la {VERSION_FLUX} \
1890:                println!("[flux] arrêt : {e}");
2764:                  (leur KV s'arrête à {fenetre} entrées) · pleines : {n_pleines}");
  ```

### 🤖 Assistant

⏵ Je collecte les numéros de ligne exacts des constats.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for spec in \"README.md:11 440\" \"README.md:blocs lus\" \"REPRISE.md:11 440\" \"REPRISE.md:11/11\" \"REPRISE.md:75 %\" \"REPRISE.md:campagne à 8 192\" \"REPRISE.md:917 543\" \"REPRISE.md:3 623\" \"REPRISE.md:~2 300\" \"docs/roadmap. … [921 caractères tronqués]`

  ```
--- README.md  << 11 440
281:le moteur tenait en 386 lignes à ses débuts ; il en fait 11 440 aujourd'hui). Détail complet :
355:BLAS, sans aucune dépendance : **11 440 lignes de Rust, `std` seul** (2 319 au premier prototype). Détail :
--- README.md  << blocs lus
345:| **gpt-oss-120b** (MoE, MXFP4) | MXFP4 | blocs lus | 15,1757 (ctx 256) | 60 Go |
--- REPRISE.md  << 11 440
16:`drave-core` est un moteur d'inférence Rust (~11 440 lignes, `std` seul) qui
--- REPRISE.md  << 11/11
35:> **19,3885** et gpt-oss ctx 256 = **15,1757**, `cargo test` **11/11**. La porte
--- REPRISE.md  << 75 %
245:| `DRAVE_KV_K_F32=1` | garde les CLÉS en f32 (valeurs quantifiées) | **le bon compromis mesuré** : à 8 192, 75 % de la taille f32 pour +0,02 % de perplexité, contre +3,0 % pour l'int8 complet — l'écart int8 vient des clés à 99 % (`reports/rapport-attribution-kv.md`) |
314:suite : `DRAVE_KV_BITS=8 DRAVE_KV_K_F32=1` (75 % de la taille f32 pour +0,02 %).
--- REPRISE.md  << campagne à 8 192
425:   là où l'int8/int8 coûte +2,15 % — la campagne à 8 192 jetons est en cours ;
--- REPRISE.md  << 917 543
324:**écart 0,00e0** (18,0851 = 18,0851) ; en UN lot de 917 543 octets → **0,00e0**
--- REPRISE.md  << 3 62
… [2979 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je vérifie si la version 4 et l'en-tête de 79 octets datent du même commit.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show d59d061 --stat | head -15; echo \"=== diff constantes ===\"; git show d59d061 -- drave-core/src/main.rs | grep -E \"^[-+].*(VERSION_FLUX|TAILLE_TETE)\" | head -10; echo \"=== log de TAILLE_TETE ===\"; git log --oneline -S 'T … [160 caractères tronqués]`

  ```
commit d59d061835bc8614204cfab927c789765664e327
Author: Stéphane <stephane@localhost>
Date:   Wed Sep 30 12:11:40 2026 -0400

    Protocole v4 : les top-k voyagent aussi (défaut n°1 de l'audit)
    
    L'audit délégué avait trouvé le trou : `appliquer_quantification` ne posait que
    niveaux/seuil/top-k/renorm, et l'en-tête ne transportait que ces quatre champs.
    Deux nœuds lancés avec des `--topk-q/-k/-v/-o/-gate/-up/-down`, `--attn-topk`,
    `--qk-topk` ou `--moe-topk` différents calculaient donc deux choses différentes,
    en silence — alors que le commentaire du code affirmait le contraire.
    
    Le contrat d'activation transporte maintenant les dix champs de plus (version 4 du
    protocole) et le client les IMPOSE au serveur. Vérifié :
    
=== diff constantes ===
-const TAILLE_TETE: usize = 4 + 1 + 1 + 4 + 4 + 4 + 4 + 4 + 4 + 4 + 4 + 1;
+const TAILLE_TETE: usize = 4 + 1 + 1 + 4 + 4 + 4 + 4 + 4 + 4 + 4 + 4 + 1
=== log de TAILLE_TETE ===
7b88131 Phase 3.2 : le flux voyage en LISTE — courbe taille/fidélité
  ```

### 🤖 Assistant

⏵ Je vérifie si la règle R4 refuse bien n == 0 comme l'affirme le plan.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src && grep -n \"verifier_taille\" main.rs; echo \"=== n == 0 ? ===\"; grep -n \"n == 0\\|n == 0u\\|== 0 {\" main.rs | head -20; echo \"=== extrait verifier_taille ===\"; sed -n '1455,1485p' main.rs", "description": "Check n= … [38 caractères tronqués]`

  ```
1468:fn verifier_taille(octets: usize, quoi: &str) -> std::io::Result<()> {
1745:            verifier_taille(taille, &format!("lot de {n} états × {hidden} canaux"))?;
1762:            verifier_taille(n_blocs.saturating_mul(4), &format!("{n_blocs} blocs d'échelles"))?;
1770:            verifier_taille(longueur, &format!("corps de {n} paires"))?;
1783:    verifier_taille(n.saturating_mul(4), &format!("flux de {n} valeurs"))?;
=== n == 0 ? ===
801:            if std::io::stdin().read_line(&mut ligne).unwrap_or(0) == 0 { break; }
1205:            if l == 0 { poids_bloc = vec![ln1, ln2, wq, bq, wk, bk, wv, bv, wo, bo,
2210:                       else if pente { if i == 0 { pos as f32 * 100.0 } else { 0.0 } }
2222:            for i in 0..hd { qs[hh * hd + i] = if i == 0 { 1.0 } else { 0.0 }; }
2923:            _ => if tour % 2 == 0 { "user" } else { "assistant" },
3064:                 if mdl.attn_window == 0 { "aucune".to_string() } else { mdl.attn_window.to_string() },
3103:            if depuis == 0 {
3228:        if n == 0 {
3251:            if *c == 0 { continue; }
3274:                 if r.manquantes > 0 && r.servies == 0 {
3280:    if n == 0 {
=== extrait verifier_taille ===
    
… [1489 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je vérifie les tests du protocole (lot géant, n=0).

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src && grep -n -A2 '#\\[test\\]' main.rs | grep \"fn \" | head -20", "description": "List protocol test names"}`

  ```
3343-    fn entete_et_version_sont_ce_que_les_numeros_disent() {
3349-    fn paires_blocs_aller_retour_avec_echappement() {
3362-    fn paires_blocs_tronquees_sont_refusees() {
3373-    fn flux_dense_aller_retour_par_la_vraie_mise_en_trame() {
3448-    fn une_trame_liste_hors_dimension_ne_tue_pas_le_noeud() {
3461-    fn un_nombre_de_blocs_dement_grand_est_refuse() {
3474-    fn un_lot_dement_grand_est_refuse_avant_allocation() {
  ```

### 🤖 Assistant

⏵ Je compare le diagnostic prévu par le plan (DRAVE_FLUX_POS) à celui du code.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src && sed -n '1852,1872p' main.rs", "description": "Read DRAVE_DEBUG_FLUX output"}`

  ```
// états entrent directement dans SA première couche.
                    let t = f.n;
                    // Refus EXPLICITE plutôt qu'une boucle sans fin : au-delà de
                    // son contexte, `KvCache::assurer` ne peut pas agrandir et
                    // tournerait indéfiniment (relevé dans `docs/plan-prefill-reparti.md`).
                    if f.pos as usize + t > mdl.ctx {
                        println!("[flux] lot refusé : {t} états à partir de la position {} \
                                  dépassent le contexte {} de ce nœud",
                                 f.pos, mdl.ctx);
                        break;
                    }
                    mdl.emb_imposee_lot = Some(f.charge.plat().to_vec());
                    let hs = mdl.forward_lot(&vec![0u32; t], f.pos as usize);
                    let plat: Vec<f32> = hs.concat();
                    if std::env::var("DRAVE_DEBUG_FLUX").is_ok() {
                        eprintln!("[debug] lot reçu : n={t} pos={} états={} plat={} corps={}",
                                  f.pos, hs.len(), plat.len(), f.octets_corps);
                    }
                    if envoyer_lot(&mut sock, f.debut, f.fin, f.po
… [82 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Dernier balayage : modes annoncés et mentions résiduelles du mode 4.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"quatre modes\\|trois modes\\|4 modes\\|mode 4\\|mode 3\\|MODE_LOT\" README.md REPRISE.md docs/*.md | grep -v journal | head -30", "description": "Sweep mode descriptions"}`

  ```
REPRISE.md:322:**Le préremplissage par lots sur le fil est FAIT** (mode 3 du protocole) : N états
REPRISE.md:389:- **Règle R4 dans le code** : les trois modes qui allouent sur une taille lue dans
REPRISE.md:419:1. ~~Préremplissage par LOTS sur le fil~~ **FAIT** (mode 3 : 256 jetons en 4 lots,
REPRISE.md:421:   veine : le **lot en listes** (mode 4), chaque état en liste creuse au lieu de
docs/colab-reparti.md:28:| **préremplissage par lots sur le fil** | ✅ mode 3, `--lot T` : 256 jetons en 4 lots, écart **0,00e0** (`reports/rapport-prefill-reparti.md`) |
docs/format-flux.md:108:          mode 3 : n × dimension × f32   (n = nombre d'ÉTATS, pas de canaux)
docs/format-flux.md:111:Le **mode 3 est le préremplissage réparti** : `n` états d'un coup, la position
docs/format-flux.md:117:f32 dense (3,5 ko par jeton) ; le lot en listes est le mode 4, pas encore écrit.
docs/plan-mode4-lot-listes.md:1:# Spécification — mode 4 : le **lot en listes** (protocole v5)
docs/plan-mode4-lot-listes.md:6:> (le mode 3, mis en œuvre, et ses leçons). Les numéros de ligne sont ceux de
docs/plan-mode4-lot-listes.md:8:> `MODE_LOT = 3`).
docs/plan-mode4-lot-listes.md:10:**En une ligne** : le mode 3 transporte `t
… [2453 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je fige la révision auditée (HEAD, hashes, comptes de lignes).

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log -1 --format='%H %ad %s' --date=iso; echo \"---\"; sha256sum drave-core/src/main.rs drave-core/src/model.rs docs/format-flux.md REPRISE.md README.md docs/roadmap.md reports/rapport-placement-bits-kv.md | cut -c1-16,66-; echo \ … [174 caractères tronqués]`

  ```
a383cd75fc60457a79f11ab9da897fdf8202eb4c 2026-09-30 15:11:59 -0400 Plan du noyau GPU de top-k (phase 1.1), chiffré, et la perplexité attendue du notebook
---
bc53a66ad757faa6 drave-core/src/main.rs
61582adb8ded0f25 drave-core/src/model.rs
a49f5a2ae0effdcb docs/format-flux.md
563e8a1d2e74044d REPRISE.md
8c402cc69dab5511 README.md
4679c37d81b8a6cf docs/roadmap.md
0077279a10554956 reports/rapport-placement-bits-kv.md
---
 11901 total
73
 M journal/README.md
?? docs/plan-mode4-lot-listes.md
  ```

### 🤖 Assistant

⏵ Je vérifie les derniers numéros de ligne cités dans le rapport.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src && grep -n \"pub fn nouveau\\|let version: u16\\|version != 1 && version != 2\\|version != 1 && version != 2 && version != 3\" model.rs; grep -n \"fn envoyer_flux\\|fn envoyer_lot\\|fn recevoir_flux\\|while pos + 1 < ids. … [174 caractères tronqués]`

  ```
411:    pub fn nouveau(budget: usize) -> Self {
540:    pub fn nouveau(chemin: &str, couches: Vec<usize>, hidden: usize, n_layer: usize)
549:        let version: u16 = if std::env::var("DRAVE_TRACE_BLOCS").is_ok() { 3 } else { 2 };
691:        if version != 1 && version != 2 && version != 3 {
1602:fn envoyer_flux(s: &mut std::net::TcpStream, debut: u32, fin: u32, pos: u32,
1671:fn envoyer_lot(s: &mut std::net::TcpStream, debut: u32, fin: u32, pos0: u32,
1707:fn recevoir_flux(s: &mut std::net::TcpStream, hidden: usize) -> std::io::Result<Flux> {
1991:        while pos + 1 < ids.len() {
1465:const PLAFOND_FLUX: usize = 256 << 20;
1468:fn verifier_taille(octets: usize, quoi: &str) -> std::io::Result<()> {
1548:fn encoder_paires_blocs(idx: &[u16], val: &[i8]) -> Vec<u8> {
1566:fn decoder_paires_blocs(corps: &[u8], n: usize) -> Result<(Vec<u16>, Vec<i8>), String> {
  ```

### 🤖 Assistant

⏵ Je rédige le rapport de cohérence (second passage).

- **write** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs-2.md", "content": "# Cohérence des documents avec le code — second passage\n\n**En une ligne** : **66 affirmations** revérifiées contre le code et les rapports\n**après** les changements du 30/09 ; **27 tie … [28766 caractères tronqués]`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs-2.md</path>
<type>file</type>
<content>
Created file
</content>
  ```

### 🤖 Assistant

⏵ Je corrige trois imprécisions de mon rapport et vérifie les faits cités.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -c \"K_F16\\|placement\" docs/contexte-long.md; grep -n \"include_str\" drave-core/src/gpu.rs | head -3; git log --until='2026-09-30 14:09' --since='2026-09-30 00:00' --oneline | wc -l; git status --porcelain", "description": "V … [56 caractères tronqués]`

  ```
0
39:const PTX: &str = include_str!("../gpu/drave_gpu.ptx");
70
 M journal/README.md
?? docs/plan-mode4-lot-listes.md
?? reports/rapport-coherence-docs-2.md
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs-2.md", "old_string": "| 45 | `REPRISE.md:383-387` | `--options-actives` imprime « APRÈS toutes les affectations », branché dans les quatre modes principaux, cache KV avec sa variante | conforme : `main.rs:5 … [718 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs-2.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs-2.md", "old_string": "| 59 | `reports/rapport-session-2026-09-30.md:4` vs `:66` | « **Trente-cinq** commits » ; plus bas « **quarante** commits » | la journée compte **73 commits** (dont 63 avant 14:09) : l … [356 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs-2.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs-2.md", "new_string": "| 63 | `REPRISE.md:389-390` | « les **trois modes** qui allouent sur une taille lue dans l'en-tête refusent au-delà de 256 Mo » | le plafond couvre **4 appels** de `verifier_taille` (1 … [528 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs-2.md has been updated successfully.
  ```

### 🤖 Assistant

⏵ Je relis le rapport pour vérifier le rendu des tableaux.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"blocs lus\" reports/rapport-coherence-docs-2.md; echo \"---\"; wc -l reports/rapport-coherence-docs-2.md", "description": "Check row 49 pipe escaping"}`

  ```
113:| 49 | `README.md:345` | ligne gpt-oss : `| … | MXFP4 | **blocs lus** | **15,1757 (ctx 256)** | 60 Go |` | la ligne est **décalée d'une colonne** : « blocs lus » occupe la colonne perplexité et 15,1757 la colonne débit ; la référence est 15,1757 (`REPRISE.md:70`) | CONTRADICTOIRE |
187:    (« blocs lus » en perplexité, 15,1757 en débit) ; remettre perplexité =
188:    15,1757 (ctx 256), débit = « blocs lus » ou la valeur réelle, mémoire = 60 Go.
---
241 reports/rapport-coherence-docs-2.md
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs-2.md", "new_string": "| 49 | `README.md:345` | ligne gpt-oss : `\\| … \\| MXFP4 \\| **blocs lus** \\| **15,1757 (ctx 256)** \\| 60 Go \\|` | la ligne est **décalée d'une colonne** : « blocs lus » occupe la  … [412 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs-2.md has been updated successfully.
  ```

### 🤖 Assistant

⏵ Je vérifie l'intégrité des tableaux et relis le début du rapport.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'EOF'\nimport re\nlines=open('reports/rapport-coherence-docs-2.md',encoding='utf-8').read().split('\\n')\nbad=[]\nfor i,l in enumerate(lines,1):\n    if l.startswith('| ') and not l.startswith('|---') and '---' not in l[: … [450 caractères tronqués]`

  ```
lignes de tableau avec mauvais nombre de colonnes: [(12, 3, '| | |'), (14, 3, '| Commit de référence | `a383cd7` (2026-09-30 15:11) |'), (15, 3, '| `drave-core/src/main.rs` | sha256 `bc53a66ad757faa6…` · 3 508 lignes |'), (16, 3, '| `drave-core/src/model.rs` | sha256 `61582adb8ded0f25…` · 3 928 lignes |'), (17, 3, '| Total `.rs` du moteur | **11 901 lignes** (7 fichiers) |'), (18, 3, "| Arbre au moment d'écrire | `journal/` modifié, `docs/plan-mode4-lot-listes.md` non suivi")]
verdicts: {'PÉRIMÉ': 18, 'CONTRADICTOIRE': 15, 'MANQUANT': 9, 'OK': 28}
  ```

### 🤖 Assistant

⏵ Je relis le rapport final avant de le transmettre.

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs-2.md", "limit": 60}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs-2.md</path>
<type>file</type>
<content>
1: # Cohérence des documents avec le code — second passage
2: 
3: **En une ligne** : **66 affirmations** revérifiées contre le code et les rapports
4: **après** les changements du 30/09 ; **27 tiennent**, **17 sont périmées**, **14 se
5: contredisent** et **8 manquent** — les deux plus graves sont le **chiffre vedette du
6: cache KV** (« 75 % / 50 % » contre « 64 % / 28 % » dans le rapport qui l'a mesuré) et
7: la règle **R4** dont la moitié (`n == 0` refusé) n'est **pas** dans le code alors que
8: le plan affirme le contraire.
9: 
10: ## Révision auditée, méthode, réserves
11: 
12: | | |
13: |---|---|
14: | Commit de référence | `a383cd7` (2026-09-30 15:11) |
15: | `drave-core/src/main.rs` | sha256 `bc53a66ad757faa6…` · 3 508 lignes |
16: | `drave-core/src/model.rs` | sha256 `61582adb8ded0f25…` · 3 928 lignes |
17: | Total `.rs` du moteur | **11 901 lignes** (7 fichiers) |
18: | Arbre au moment d'écrire | `journal/` modifié, `docs/plan-mode4-lot-listes.md` non suivi ; **73 commits** dans la journée |
19: 
20: Trois réserves, parce qu'elles changent la portée
… [4375 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs-2.md", "new_string": "   `DRAVE_TRACE_BLOCS=1` écrit bien **v3** (`/tmp/verif_v3.bin`, 346 636 o,\n   192 listes, 166 206 actifs — avec perte, donc) ; et le tableau de bord\n   `--options-actives` imprime b … [393 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs-2.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs-2.md", "offset": 60, "limit": 75}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs-2.md</path>
<type>file</type>
<content>
60: | 11 | `docs/format-flux.md:95` | `n` = « dimension (mode 0) ou actifs (mode 1) » | en mode 2 `n` = **actifs** (`main.rs:1627-1631`), en mode 3 = **états** (`envoyer_lot`, 1690) ; le commentaire `main.rs:1447` (« canaux (dense, listes) ») est faux pour les listes, `n` y valant `idx.len()` | MANQUANT |
61: | 12 | `docs/plan-prefill-reparti.md:76-78` + bandeau `:9-10` | règle R4 : « `n == 0` **et** `n × hidden × 4 > 256 Mo` sont refusés » ; « la règle R4 est maintenant DANS le code, avec son test » | seul le plafond existe : `verifier_taille` (`main.rs:1468`) ne teste que `> 256 Mo` et est appelé 5 fois (1570, 1745, 1762, 1770, 1783) ; **aucun refus de `n == 0`**, aucun test (les 7 tests de `main.rs:3343-3474` couvrent l'en-tête, l'échappement, la troncature, l'aller-retour dense, l'indice hors dimension, les blocs démesurés et le lot géant) | CONTRADICTOIRE |
62: | 13 | `docs/plan-prefill-reparti.md:266` | « `DRAVE_FLUX_POS=1` fait imprimer `[flux] lot pos .. pos+t-1` des deux côtés » | cette variable **n'existe pas** ; le diagnostic livré est `DRAVE_DEBUG
… [16193 caractères tronqués]
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs-2.md", "new_string": "| 12 | `docs/plan-prefill-reparti.md:76-78` + bandeau `:9-10` | règle R4 : « `n == 0` **et** `n × hidden × 4 > 256 Mo` sont refusés » ; « la règle R4 est maintenant DANS le code, avec  … [1009 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs-2.md has been updated successfully.
  ```

- **edit** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs-2.md", "new_string": "| 20 | `REPRISE.md:298` | « listes i16, seuil 0,01 : **~2 300** octets » | aucune mesure de ce type : 2 159 est l'i16 au seuil **0,02** (vrai texte, `rapport-transport-liste.md:135`) e … [379 caractères tronqués]`

  ```
The file /home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs-2.md has been updated successfully.
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs-2.md", "offset": 135}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-coherence-docs-2.md</path>
<type>file</type>
<content>
135: | 66 | `docs/plan-gpu-topk.md` (apparu pendant l'audit) | ×73 pour le KV en VRAM, 968 ms CPU, 1,99e-7, 12,4 → 12,5 ms en top-k CPU | ces chiffres sont ceux de `REPRISE.md:163-164,184,224` et de la mesure GPU du jour ; rien de contradictoire relevé | OK |
136: 
137: ---
138: 
139: ## Les corrections à faire, dans l'ordre
140: 
141: 1. **Trancher le chiffre du cache KV, et l'écrire une fois pour toutes.** Les
142:    documents publient « 75 % de la taille f32 » (REPRISE:245,314 ;
143:    roadmap:173-174 ; rapport-attribution-kv:33) et « int8 complet 50 % »
144:    (attribution:34 ; roadmap:174) alors que le rapport de la campagne complète
145:    donne **64 %** et **28 %** — et le tableau de REPRISE:365,368 dit déjà 64/28.
146:    Corriger les quatre documents, ou re-mesurer si la campagne en cours dit autre
147:    chose, mais ne pas laisser deux valeurs pour le même réglage.
148: 2. **Corriger `reports/rapport-placement-bits-kv.md`** : ligne 5, « +0,06 % » →
149:    « +0,018 % à 8 191 jetons (+0,057 % à contexte 256) » ; remplacer la section
150:    « La
… [6705 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Je transmets le résultat à l'agent parent.

- **todo_write** `{"todos": [{"content": "Extraire les faits du code (VERSION_FLUX, TAILLE_TETE, modes, DRAVE_*, drapeaux)", "status": "completed"}, {"content": "Vérifier versions & en-tête dans README/REPRISE/docs", "status": "completed"}, {"content": "Croiser les chiffres publiés avec les rapports (octets, traces,  … [349 caractères tronqués]`

  ```
Updated todo list: 0 pending, 0 in progress, 6 completed.
  ```

- **send_message** `{"agent_id": "bbd6969f-0f70-42b2-8951-64d1f2f36d2e", "message": "Second passage de cohérence documentaire TERMINÉ. Livrable : reports/rapport-coherence-docs-2.md (241 lignes, 66 affirmations, tableaux à 4 colonnes + verdicts, 15 corrections ordonnées, résumé 10 lignes). Aucun autre fichier modifié ( … [3358 caractères tronqués]`

  ```
message delivered to agent bbd6969f-0f70-42b2-8951-64d1f2f36d2e
  ```

### 🤖 Assistant

⏵ Rapport livré et transmis au parent.

## Mission terminée

**Livrable** : `reports/rapport-coherence-docs-2.md` (241 lignes) — second passage de vérification de la documentation **après** les changements du 30/09. Aucun autre fichier touché (`git status` ne montre que mon rapport en plus des modifications préexistantes).

### Ce qui a été vérifié
- **66 affirmations** contre le code (`VERSION_FLUX = 4`, `TAILLE_TETE = 79`, modes 0–3, sémantique de `n`, `PLAFOND_FLUX` 256 Mo, 28 variables `DRAVE_*`, drapeaux), contre les rapports et entre documents (octets par flux, tailles de trace, perplexités, pourcentages KV, accélérations, comptes de tests/lignes/commits).
- Tous les liens `[texte](chemin)` par script : **aucun lien mort**.
- Deux exécutions courtes autorisées (`--limit 4`) : trace par défaut = **DRVF v2**, `DRAVE_TRACE_BLOCS=1` = **v3** (avec perte), `--options-actives` opérationnel.
- Réserve de méthode : l'arbre a bougé pendant l'audit (deux plans apparus, un commit en cours), une campagne de mesure tournait — rien de lourd n'a été lancé.

### Verdicts
**27 OK · 17 PÉRIMÉ · 14 CONTRADICTOIRE · 8 MANQUANT**

### Les trois défauts majeurs
1. **Cache KV** : « 75 % / 50 % » (REPRISE, roadmap, rapport d'attribution) contre « **64 % / 28 %** » dans le rapport de la campagne complète et dans le tableau de REPRISE lui-même ; le bandeau du rapport de placement dit même `+0,06 %` contre `+0,018 %` dans son propre tableau.
2. **Règle R4** : le refus de `n == 0` est annoncé comme « dans le code, avec son test » — il n'y est pas ; seul le plafond de 256 Mo existe.
3. **Époques de l'en-tête mélangées** : « 39 octets + version 4 » est impossible depuis `d59d061`, et contamine six passages (REPRISE §6bis, roadmap:56, rapport transport, phase 3).

Le rapport se termine par les **15 corrections ordonnées** (sans les appliquer) et un **résumé de 10 lignes**.

