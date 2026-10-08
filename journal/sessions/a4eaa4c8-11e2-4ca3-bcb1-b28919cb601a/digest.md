# Session DSH — relecture

- identifiant : `a4eaa4c8-11e2-4ca3-bcb1-b28919cb601a`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-10-08 09:18:41
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (moteur d'inférence Rust « Drave », drave-core/). LECTURE SEULE STRICTE : ne modifie aucun fichier, ne compile pas, ne lance aucun test ni binaire.

Objectif : inventorier la GESTION MÉMOIRE, DISQUE et FILS (exploitation des ressources d'UNE machine), avec chiffres mesurés.

À examiner :
- drave-core/src/materiel.rs : détection matérielle (cœurs physiques vs logiques, cache, disque, GPU, RAM), ce qui est affiché par --materiel, ce qui est utilisé pour décider (threads par défaut, placement).
- mmap / page cache : grep « mmap », « Mmap », « DRAVE_MMAP », « madvise », « MADV_ », « munmap », « page cache », « pread », « O_DIRECT » dans drave-core/src/ (gguf.rs, model.rs, formats.rs, engine.rs) ; explique comment les poids sont lus (mmap ? lecture explicite ? par tranches ?), et ce qui est proposé à l'utilisateur.
- affinité des fils / threads : grep « affinity », « sched_setaffinity », « core_affinity », « DRAVE_FILS », « threads », fonction fils() dans main.rs ; nombre de fils par défaut, comment il est choisi.
- RAM limitée / éviction : grep « eviction », « DRAVE_KEEP », « keep », « prefetch », « DRAVE_PRELIRE », LRU, cache d'experts ; reports/rapport-materiel-disque-ou-cpu.md, reports/rapport-architecture-memoire.md, reports/rapport-empreinte-memoire.md, reports/rapport-passe-k3-disque.md, reports/rapport-budget-kimi-k3.md, reports/rapport-cache-experts-vram.md.
- Portes : ce que tools/portes.sh vérifie sur le matériel (section « threads par défaut ») ; y a-t-il une porte pour le mmap, le disque, l'éviction ?

Rends un condensé FACTUEL en français, maximum 45 lignes :
1) Tableau : capacité (mmap, page cache, éviction, affinité fils, détection matérielle, prélecture), ce qu'elle fait, fichier:ligne, état (porte / mesuré / supposé), chiffre mesuré (Mio/s, Go/s, ms, nb de fils).
2) Débits disque mesurés (NVMe vs disque dur) avec source, et le goulot identifié.
3) Ce qui est vérifié automatiquement vs mesuré à la main.
Distingue « mesuré », « déduit », « supposé ». Donne chemins et numéros de ligne.
Your parent agent id is "482522d1-31f1-43eb-ae9c-a681336404f7". Before you finish, send your result to that agent with send_message({ agent_id: "482522d1-31f1-43eb-ae9c-a681336404f7", message: "<self-contained result>" }). The parent shares your workspace but does not automatically receive your transcript, tool output, or reasoning. Send earlier messages as well when a finding changes what the parent should do next; sending a message does not end your turn.

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

⏵ Inventaire lecture seule mémoire/disque/fils du moteur Drave

Je commence par repérer les fichiers et les motifs demandés.

- **bash** `{"command": "ls -la; ls drave-core/src/ 2>/dev/null; ls reports/ 2>/dev/null | head -50; ls tools/ 2>/dev/null | head -50", "description": "List repo structure"}`

  ```
total 308
drwxr-xr-x. 1 stephane stephane    612  7 oct 18:16 .
drwxr-xr-x. 1 stephane stephane   2374  3 oct 10:09 ..
drwxr-xr-x. 1 stephane stephane     40 25 sep 15:38 bench
drwxr-xr-x. 1 stephane stephane     56 30 sep 12:20 colab
drwxr-xr-x. 1 stephane stephane     96  1 oct 06:58 data
drwxr-xr-x. 1 stephane stephane   1130  5 oct 13:47 docs
drwxr-xr-x. 1 stephane stephane     82 28 sep 11:58 drave-core
drwxr-xr-x. 1 stephane stephane    164  8 oct 09:11 .git
-rw-r--r--. 1 stephane stephane    399 30 sep 10:01 .gitignore
drwxr-xr-x. 1 stephane stephane     34 27 sep 11:39 journal
drwxr-xr-x. 1 stephane stephane     88 25 sep 17:13 models
drwxr-xr-x. 1 stephane stephane    114 25 sep 15:24 __pycache__
-rw-r--r--. 1 stephane stephane   4992 25 sep 10:54 Qtrinet-bootstrap.md
-rw-------. 1 stephane stephane  36518  2 oct 10:21 README.md
drwxr-xr-x. 1 stephane stephane   4256  7 oct 18:22 reports
-rw-------. 1 stephane stephane 120322  5 oct 16:21 REPRISE.md
-rw-------. 1 stephane stephane   8566 30 sep 08:44 run_8bit_perfection.py
-rw-------. 1 stephane stephane  10507 30 sep 08:44 run_clusters.py
-rw-------. 1 stephane stephane  12507 30 sep 08:44 run_cpu.py
-rw-------. 1 stephan
… [3120 caractères tronqués]
  ```

- **grep** `{"pattern": "mmap|Mmap|MMAP|DRAVE_MMAP|madvise|MADV_|munmap|O_DIRECT|pread", "path": "drave-core/src"}`

  ```
Found 44 matches

drave-core/src/model.rs
Line 143:     // L'engram est une table mmappée que le moteur sait ADRESSER (`--sonder-engram`)
Line 256: sonde mmap), ou passe bornée `--couches a:b` — annoncée comme telle.\n  \
Line 1157:         // Le pointeur vient d'un mmap qui vit plus longtemps que l'appel ; il
Line 1331: /// sommation ne change — un expert lu en RAM rend exactement ce que le mmap
Line 7599:                     // redirigée, loc = 0) au lieu du mmap ; sinon on lit le
Line 7600:                     // mmap comme avant, puis on le recopie.

drave-core/src/main.rs
Line 24:     "KV_BITS", "KV_F16", "KV_K_F16", "KV_K_F32", "KV_V_F32", "MMAP",
Line 87:         eprintln!("       drave <modele> --sonder-engram N   accès mmappé à une table d'engram");
Line 92:         eprintln!("        ne charge que certains clusters ; DRAVE_MMAP=0 lit au lieu de mapper)");
Line 612:     /// Sonde d'accès mmappé à la table d'engram : combien d'entrées lire, à des
Line 1684: /// Sonde d'accès mmappé à la table d'engram.
Line 1691: /// Cette sonde le démontre : elle ouvre le fichier entier en mmap, lit `n`
Line 1757:     // `open` (mmap) et non `open_meta_auto` : lire une rangée demande les
L
… [2492 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de materiel.rs, gguf.rs (mmap) et main.rs (fils)

- **bash** `{"command": "wc -l drave-core/src/*.rs; echo ---; wc -l tools/portes.sh 2>/dev/null; ls tools | grep -i porte", "description": "Count lines of source files"}`

  ```
506 drave-core/src/clusters.rs
   1029 drave-core/src/engine.rs
    408 drave-core/src/engram.rs
   2901 drave-core/src/formats.rs
   2343 drave-core/src/gguf.rs
   1573 drave-core/src/gpu.rs
   1866 drave-core/src/kimi_k3.rs
   1597 drave-core/src/list.rs
   5903 drave-core/src/main.rs
    478 drave-core/src/materiel.rs
   9237 drave-core/src/model.rs
    646 drave-core/src/tokenizer.rs
  28487 total
---
336 tools/portes.sh
porte-flux.sh
portes_formats.sh
portes.sh
porte-tokenizer-kimi.sh
  ```

- **read** `{"file_path": "drave-core/src/gguf.rs", "limit": 220}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/gguf.rs</path>
<type>file</type>
<content>
1: //! Lecteur GGUF minimal (std seul).
2: //!
3: #![allow(dead_code)] // lecteur générique : tous les formats ne servent pas au moteur
4: 
5: //! Ne lit que ce dont le moteur a besoin : métadonnées, descripteurs de tenseurs,
6: //! et les niveaux quantifiés (Q8_0 / Q4_0) ou les flottants (F32 / F16).
7: 
8: use std::collections::HashMap;
9: use std::fs::File;
10: use std::io::{Read, Seek, SeekFrom};
11: use std::ops::Deref;
12: use std::path::Path;
13: 
14: /// Résultat empruntant à `self`. Écrit à la main parce qu'un tenseur peut vivre
15: /// dans n'importe lequel des fichiers de l'assemblage.
16: type io_result<'a> = std::io::Result<&'a [u8]>;
17: 
18: /// Fichier **mappé** en mémoire plutôt que lu.
19: ///
20: /// `read_to_end` fait deux choses coûteuses : il lit tout le fichier (18,55 Go
21: /// pour Qwen3-30B, 366 Go pour DeepSeek-V4.1-Flash) et il en garde une copie
22: /// dans le tas, en plus du cache de pages du noyau — soit deux fois la taille du
23: /// modèle en mémoire physique au premier accès.
24: ///
25: /// Le mmap ne lit rien : il rend une plage d'adre
… [8029 caractères tronqués]
  ```

- **read** `{"file_path": "drave-core/src/materiel.rs"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/materiel.rs</path>
<type>file</type>
<content>
1: //! Détection du matériel et choix automatique de la configuration.
2: //!
3: //! Tout ce que ce module décide vient d'une **mesure**, pas d'une intuition.
4: //! Chaque heuristique porte le chiffre qui la justifie, et la commande
5: //! `--materiel` les affiche toutes avec leur raison — pour qu'un réglage
6: //! surprenant puisse être contesté.
7: //!
8: //! Les mesures de référence (session du 01/10, Xeon E5-2687W v3, 2 Quadro
9: //! RTX 5000, NVMe MAP1602) :
10: //!
11: //! | | |
12: //! |---|---|
13: //! | VRAM (noyau warp) | 84,9 Go/s |
14: //! | RAM, 20 cœurs physiques | 22,5 Go/s |
15: //! | RAM, 10 cœurs + leurs hyperthreads | 18,7 Go/s (+27 % sur 10 cœurs secs) |
16: //! | RAM, 20 cœurs + hyperthreads | 18,9 Go/s — **rien de plus** |
17: //! | NVMe, 1 lecteur | 5,4 Go/s |
18: //! | **NVMe, 16 lecteurs** | **31,1 Go/s** |
19: 
20: use std::path::Path;
21: use std::process::Command;
22: 
23: #[derive(Debug, Clone)]
24: pub struct Noeud {
25:     pub id: usize,
26:     pub cpus: Vec<usize>,
27:     pub memoire_go: f64,
28: }
29: 
30: #[derive(Debug, Clone)]
3
… [22523 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Recherche des fils, affinité et éviction dans le code

- **grep** `{"path": "drave-core/src", "pattern": "affinity|sched_setaffinity|core_affinity|DRAVE_FILS|fn fils|threads|epinglage|DRAVE_KEEP|eviction|Eviction|LRU|lru|prefetch|PRELIRE|DRAVE_LECTEURS|lecteurs"}`

  ```
Found 139 matches

drave-core/src/model.rs
Line 1573: /// Cache VRAM des experts MoE (MXFP4), à éviction LRU.
Line 1590:     pub evictions: u64,
Line 1598:                        demandes: 0, manques: 0, evictions: 0, octets_envoyes: 0, ticks: 0 }
Line 1624:                     self.evictions += 1;
Line 3296:     pub fn load(path: &str, ctx: usize, n_threads: usize, dense: bool, keep: f32,
Line 3298:         Self::load_partiel(path, ctx, n_threads, dense, keep, auto, q4, b6, None)
Line 3302:     pub fn load_partiel(path: &str, ctx: usize, n_threads: usize, dense: bool, keep: f32,
Line 4088:         let pool = Pool::new(n_threads, cfg.hidden);
Line 4089:         eprintln!("[modele] {} couches chargées en {:?} — listes {:.2} Go{} , {} threads",
Line 4094:                   pool.threads());
Line 4307:             println!("[gpu] cache d'experts : budget {:.1} Go de VRAM (LRU), éviction par (couche, expert)",
Line 6554:         let n_fils = self.pool.threads();
Line 6683:         let threads_iq = self.pool.threads().clamp(1, 32);
Line 6954:                     matvec_f32_fils(wkv, &rangee, nhc * VALEURS_PAR_RANGEE, kv_dim, &mut kv, pool.threads());
Line 7078:                           
… [10218 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '145,200p' drave-core/src/main.rs; echo '=== 500-540 ==='; sed -n '505,535p' drave-core/src/main.rs; echo '=== 655,690 ==='; sed -n '655,690p' drave-core/src/main.rs; echo '=== 860,880 ==='; sed -n '860,880p' drave-core/src/main.rs", "description": "Read main.rs thread selection  … [9 caractères tronqués]`

  ```
if opt.banc_topk > 0 { run_banc_topk(opt); return; }
    if opt.gpu_banc { run_gpu_banc(opt); return; }
    if opt.k3_essai { run_k3_essai(opt.couches); return; }
    if opt.plan { run_plan(opt); return; }
    if opt.tokenize { run_tokenize(opt); return; }
    if opt.ppl { run_ppl(opt); return; }
    if opt.infer { run_infer(opt); return; }
    let path = &args[1];
    let mut matrix = "blk.0.ffn_gate.weight".to_string();
    // Par défaut : les cœurs PHYSIQUES, pas les threads logiques. Mesuré au banc
    // sur 20 cœurs / 40 threads : 18 threads = 22,6 Go/s, 20 = 18,7 (bruité),
    // 15 = 19,9, 10 = 14,3. Le `× 3/4` d'avant visait à laisser un quart des CPU
    // au système, mais il comptait les threads logiques : il donnait 30 fils sur
    // 20 cœurs. Prendre les 20 cœurs laisse de toute façon leurs 20 hyperthreads
    // au système, et l'attente active de la barrière ne tolère aucune
    // sursouscription (mesuré : ×1,3 de perte à 40+1 threads sur 40 CPU).
    let cpu = engine::coeurs_physiques();
    let mut n_threads = cpu.max(1);
    // Pas de 2 SEULEMENT devant un drapeau qui prend une valeur : un pas de 2
    // aveugle sautait `--threads 4` dès qu'un drapeau booléen l
… [6248 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '260,340p' drave-core/src/engine.rs; echo '=== 420,470 ==='; sed -n '415,470p' drave-core/src/engine.rs", "description": "Read engine.rs affinity code"}`

  ```
n_active: AtomicUsize,
    accs: AtomicPtr<Vec<Vec<i32>>>,
    accs64: AtomicPtr<Vec<Vec<i64>>>,
    spans: AtomicPtr<Vec<(usize, usize)>>,
    dirty: AtomicPtr<Vec<usize>>,
}

/// Épingle-t-on les workers ? Réglé une fois par le programme principal.
pub static EPINGLER: std::sync::atomic::AtomicBool = std::sync::atomic::AtomicBool::new(false);

/// Épingle le fil courant sur un processeur logique.
///
/// `std` n'expose pas `sched_setaffinity` : on passe par l'appel système
/// direct (numéro 203 sur x86-64). Le masque fait 128 octets, soit 1 024
/// processeurs — la taille maximale que le noyau accepte.
///
/// Intérêt mesuré : les poids sont alloués par le fil principal, donc sur le
/// nœud NUMA 0. Un worker qui tourne sur l'autre socket paie chaque accès au
/// QPI. Au banc : 20,7 Go/s en laissant l'ordonnanceur placer les fils,
/// **24,7 Go/s** en les liant à un socket.
#[cfg(all(target_arch = "x86_64", target_os = "linux"))]
/// Nombre de **cœurs physiques**.
///
/// `available_parallelism` rend les threads logiques — 40 sur cette machine,
/// pour 20 cœurs. Or la charge du moteur est limitée par la **bande passante
/// mémoire**, pas par le calcul : mesuré au banc, 40 thre
… [5675 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"EPINGLER\\|epingler\\|--pin\\|cibles_locales\\|fn new(n\" drave-core/src/*.rs | head -40; echo '=== pool new ==='; sed -n '355,420p' drave-core/src/engine.rs; echo '=== cibles 330,360 ==='; sed -n '336,360p' drave-core/src/engine.rs", "description": "Inspect pinning and Pool:: … [12 caractères tronqués]`

  ```
drave-core/src/engine.rs:268:pub static EPINGLER: std::sync::atomic::AtomicBool = std::sync::atomic::AtomicBool::new(false);
drave-core/src/engine.rs:315:pub fn epingler(cpu: usize) -> bool {
drave-core/src/engine.rs:337:fn cibles_locales(n: usize) -> Vec<usize> {
drave-core/src/engine.rs:390:    pub fn new(n: usize, n_out: usize) -> Self {
drave-core/src/engine.rs:428:        let epingle = EPINGLER.load(Ordering::Relaxed);
drave-core/src/engine.rs:429:        let cibles = if epingle { cibles_locales(n) } else { Vec::new() };
drave-core/src/engine.rs:436:                if let Some(c) = cpu { epingler(c); }
drave-core/src/main.rs:533:/// et pas dans l'autre. Le bug est arrivé quatre fois — `--pin`, `--moe-topk`,
drave-core/src/main.rs:778:            "--pin" => { o.pin = true; 1 }
drave-core/src/main.rs:835:    if o.pin { engine::EPINGLER.store(true, std::sync::atomic::Ordering::Relaxed); }
=== pool new ===
                }
            } else if let Ok(a) = morceau.parse::<usize>() { cpus.push(a); }
        }
        let physiques = cpus.len() / 2;
        v.extend_from_slice(&cpus[..physiques.max(1)]);
    }
    if v.is_empty() { v = (0..n).collect(); }
    v
}

pub struct Pool {
… [4063 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '7900,8000p' drave-core/src/model.rs 2>/dev/null | head -5; echo '=== eviction LRU 1560,1660 ==='; sed -n '1560,1660p' drave-core/src/model.rs", "description": "Read expert LRU cache code"}`

  ```
unsafe { *(base_out as *mut f32).add(o * t + i) = v; }
                                }
                            }
                        }
                    });
=== eviction LRU 1560,1660 ===
            (Some(d8), Some(machine))
                if d8.src == crate::list::Source8::Q8_0 && keep >= 1.0
                   && n_out * d8.nb_ligne * 34 >= SEUIL_GPU => {
                let octets = n_out * d8.nb_ligne * 34;
                let blocs = unsafe { std::slice::from_raw_parts(d8.base, octets) };
                machine.charger_proj(blocs, n_out, d8.nb_ligne)
            }
            _ => None,
        };
        Proj { gpu, m, d, q4: q4v, bias }
    }
}

/// Cache VRAM des experts MoE (MXFP4), à éviction LRU.
///
/// Pourquoi un cache et pas un simple déport : un expert pèse 4,4 Mo et
/// gpt-oss en a 4 608 (36 couches × 128) — 60 Go, la VRAM n'en tient pas le
/// quart. Mais un expert SÉLECTIONNÉ est réutilisé d'un jeton à l'autre : c'est
/// exactement ce qu'un cache attrape. La mesure d'activation
/// (`reports/rapport-localite-activation.md`) dit qu'un préchargement STATIQUE
/// ne paie pas ; une résidence dynamique, si.
pub struct CacheExperts {
    /// Une entrée
… [3812 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des rapports matériels et de portes.sh

- **bash** `{"command": "wc -l reports/rapport-materiel-disque-ou-cpu.md reports/rapport-architecture-memoire.md reports/rapport-empreinte-memoire.md reports/rapport-passe-k3-disque.md reports/rapport-budget-kimi-k3.md reports/rapport-cache-experts-vram.md reports/rapport-localite-activation.md tools/portes.sh  … [43 caractères tronqués]`

  ```
94 reports/rapport-materiel-disque-ou-cpu.md
   428 reports/rapport-architecture-memoire.md
   545 reports/rapport-empreinte-memoire.md
   490 reports/rapport-passe-k3-disque.md
    84 reports/rapport-budget-kimi-k3.md
    95 reports/rapport-cache-experts-vram.md
    81 reports/rapport-localite-activation.md
   336 tools/portes.sh
  2153 total
  ```

- **read** `{"file_path": "tools/portes.sh"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/portes.sh</path>
<type>file</type>
<content>
1: #!/bin/bash
2: # Les portes du dépôt, en une commande.
3: #
4: # Un chiffre de référence qui dérive sans qu'on s'en aperçoive ne vaut rien :
5: # chaque porte est comparée à la valeur ATTENDUE, et le script sort en erreur si
6: # l'une diverge. Les valeurs sont celles publiées dans les rapports.
7: #
8: #   tools/portes.sh            toutes les portes
9: #   tools/portes.sh rapide     sans gpt-oss (le seul qui prenne ~20 min)
10: 
11: set -u
12: cd "$(dirname "$0")/.."
13: D=./drave-core/target/release/drave
14: RAPIDE=${1:-}
15: ECHEC=0
16: 
17: [ -x "$D" ] || { echo "compiler d'abord : (cd drave-core && cargo build --release)"; exit 2; }
18: 
19: compare() {  # nom, attendu, obtenu
20:     if [ "$2" = "$3" ]; then
21:         printf "  %-42s %s  ✅\n" "$1" "$3"
22:     else
23:         printf "  %-42s %s  ❌ (attendu %s)\n" "$1" "${3:-—}" "$2"
24:         ECHEC=1
25:     fi
26: }
27: 
28: # Attention : le moteur affiche AUSSI une perplexité cumulée par fenêtre, avant
29: # le total. Prendre la première occurrence du motif donnait 17,431 (fenêtre 1) au
30: # lieu de 19,3885 (t
… [18965 caractères tronqués]
  ```

- **read** `{"file_path": "reports/rapport-materiel-disque-ou-cpu.md"}`
- **read** `{"file_path": "reports/rapport-cache-experts-vram.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-materiel-disque-ou-cpu.md</path>
<type>file</type>
<content>
1: # Disque ou CPU ? — ce que la mesure dit d'un deuxième NVMe
2: 
3: > Question posée le 03/10 : « est-ce que ça vaudrait la peine d'acheter un 2ᵉ NVMe
4: > pour le mettre sur le 2ᵉ CPU (chacun son NVMe pour le mmap) ? »
5: >
6: > Réponse mesurée : **non, pas pour la vitesse**, parce que le mur est le CPU, pas
7: > le stockage — y compris sur le seul modèle qui ne tient pas en RAM. Ce rapport
8: > existe pour que la décision ne repose pas sur une impression.
9: 
10: ## 1. La machine, telle qu'elle est
11: 
12: | | |
13: |---|---|
14: | CPU | 2 × Intel Xeon E5-2687W v3 @ 3,10 GHz — 2 sockets, 10 cœurs chacun, 40 fils |
15: | NUMA | node 0 = CPU 0-9,20-29 · node 1 = CPU 10-19,30-39 |
16: | RAM | 125 Go (≈ 110 Go disponibles, ≈ 95 Go en `buff/cache`) |
17: | NVMe | **un seul** : Fanxiang S660 1 To, `numa_node = 0`, monté sur `/home/stephane/FastNVMe` (828 Go) |
18: | « 11 To » | `/home/stephane/Data13TB` — LVM sur **`WDC WD120EFGX` : un disque ROTATIONNEL (ROTA=1)**, 12 To |
19: 
20: Les deux emplacements de modèles ne sont donc pas équivalents : **V4.1 Q
… [4124 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-cache-experts-vram.md</path>
<type>file</type>
<content>
1: # Rapport — un cache d'experts en VRAM pour Kimi-K3 : mesuré, et pourquoi c'est non
2: 
3: **Question** (venue de Strata, `github.com/architectds/Strata`, via la vidéo
4: « Local AI Is Now 6x Faster on Your PC ») : garder les experts les plus appelés
5: dans la VRAM rend-il Kimi-K3 plus rapide ici ?
6: 
7: **Réponse courte : non.** ×1,09 prédit, pour un plafond absolu de ×1,41 — contre
8: un plafond de ×3,1 pour le chantier du dense, qui est déjà nommé.
9: 
10: ## 1. Le plafond, avant toute mesure
11: 
12: Trafic disque d'un jeton de Kimi-K3, sur les postes **déjà mesurés**
13: (`tools/budget_execution_locale.py`, fichier complet) :
14: 
15: | poste | Go/jeton | part |
16: |---|---:|---:|
17: | **experts routés** (16 sur 896) | 25,83 | 29,3 % |
18: | experts partagés (2 par couche) | 12,40 | 14,1 % |
19: | **dense Q8_0** (attention, KDA, MLA, routage) | 48,56 | **55,1 %** |
20: | tête de sortie | 1,30 | 1,5 % |
21: | **total** | **88,09** | |
22: 
23: Un cache d'experts ne peut retirer **que** les 25,83 Go routés. Donc :
24: 
25: | taux de succès | gain 
… [3430 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Analyse des rapports disque K3 et empreinte mémoire

- **read** `{"file_path": "reports/rapport-passe-k3-disque.md", "limit": 240}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-passe-k3-disque.md</path>
<type>file</type>
<content>
1: # Où passe le temps d'une passe Kimi-K3 : le disque, et rien d'autre
2: 
3: > Mesuré le 07/10. Répond à la question laissée ouverte par `REPRISE.md`, qui
4: > demandait explicitement de la trancher **en premier** :
5: >
6: > *« la passe complète coûte 2,95 s par couple (couche, jeton) contre 0,75 s à
7: > chaud — quatre fois plus — et réduire de 25 % les experts lus ne change rien.
8: > Hypothèse non mesurée : la dispersion (~144 lectures par couple × ~10 ms de
9: > déplacement). Le pas pour trancher : `majflt` et le temps d'attente disque sur
10: > une passe complète. »*
11: 
12: La réponse est **le disque**, et elle est exacte à 0,1 % près. La sonde est
13: `tools/sonde-passe-k3.sh`, le relevé brut `/tmp/sonde_k3.csv` (793 échantillons,
14: 2 s), la sortie moteur `/tmp/sonde_k3_moteur.log`.
15: 
16: ---
17: 
18: ## 1. Le montage
19: 
20: `DRAVE_K3_PASSE=93` sur `Kimi-K3-UD-Q4_K_XL` — **1,4 To, 32 shards**, quatre
21: jetons (les identifiants de la référence `[3638, 275, 1309, 3140]`), soit
22: **372 couples (couche, jeton)**. Une seule couche en mémoire à
… [11470 caractères tronqués]
  ```

- **bash** `{"command": "grep -nE \"Go/s|Mo/s|mio/s|Mio/s|ms|page cache|mmap|DRAVE_|munmap|madvise|LRU|éviction|eviction|threads|fils\" reports/rapport-architecture-memoire.md | head -70", "description": "Grep architecture report for figures"}`

  ```
13:| **VRAM** (noyau `warp par ligne`) | **84,9 Go/s** | banc GPU, tête de 144,6 Mo en 1,7 ms |
14:| VRAM (noyau `ligne par fil`) | 41,9 Go/s | même banc, 3,4 ms |
15:| **RAM** (CPU, 30 fils) | **20,9 Go/s** | même banc, 6,9 ms |
16:| **NVMe**, aléatoire, blocs 4 Mo | 5,5 Go/s | mesuré, cache chaud |
17:| **PCIe** 3.0 ×16 | ~12 Go/s | théorique 15,75 ; le lien monte à gen 3 sous charge |
30:| tête de sortie | 1,32 | Q4_K | **oui** | 63,2 ms | **15,5 ms** |
31:| **attention MLA** | **5,40** | Q8_0 | **NON** | **258,4 ms** | 63,6 ms |
32:| embeddings | 1,32 | F16 | **oui** | 63,2 ms | **15,5 ms** |
33:| experts (top-6 × 40) | 2,39 | IQ2_XXS / Q2_K | **NON** | 114,4 ms | 28,2 ms |
34:| **total** | **10,43** | | | **499 ms** | **404 ms** |
36:**L'attention MLA est le premier poste de dépense** (5,40 Go par jeton, 258 ms à
38:déport actuel ne fait donc gagner que 95 ms sur 499.
44:| **VRAM** | 30,2 Go | tête 1,32 + attention 5,40 + embeddings 1,32 = **8,0 Go**, puis **22,2 Go d'experts chauds** (2 227) | 84,9 Go/s |
45:| **RAM** | 102 Go | jusqu'à **10 247 experts** — or 90 % des appels tiennent dans 71 Go | 20,9 Go/s |
46:| **NVMe** | 828 Go | le reste des experts (~51 Go) + **l'engram
… [3960 caractères tronqués]
  ```

- **read** `{"file_path": "reports/rapport-architecture-memoire.md", "offset": 130, "limit": 180}`
- **read** `{"file_path": "reports/rapport-passe-k3-disque.md", "offset": 241, "limit": 250}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-architecture-memoire.md</path>
<type>file</type>
<content>
130: **La conséquence est nette** : à très long contexte, la VRAM appartient au KV, et
131: les experts redescendent en RAM et sur NVMe. Les deux ressources se disputent les
132: mêmes 30 Go, et le point de bascule est autour de **100 K jetons**.
133: 
134: ## 8. CPU, hyperthreading, NUMA et NVMe : ce qui n'avait pas été évalué
135: 
136: ### Le CPU sature à 22 Go/s — et l'hyperthreading n'apporte rien
137: 
138: Banc mémoire, nombre de fils croissant :
139: 
140: | fils | 1 | 4 | 8 | **16** | 20 | 30 | 40 |
141: |---|---|---|---|---|---|---|---|
142: | Go/s | 1,9 | 6,3 | 8,7 | **20,8** | 16,8 | 23,8 | 23,0 |
143: 
144: **Le plateau est atteint dès 16 fils.** La charge est limitée par la bande
145: passante mémoire, pas par le calcul.
146: 
147: Et la mesure décisive, chaque configuration répétée trois fois (un seul essai ne
148: distingue pas le bruit du signal — le premier passage donnait un résultat
149: incohérent) :
150: 
151: | épinglage | médiane | essais |
152: |---|---|---|
153: | 10 cœurs purs (socket 0) | 11,8 | 11,7 · 11,8 · 14,8 |
154: | 10 h
… [8183 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-passe-k3-disque.md</path>
<type>file</type>
<content>
241:    défauts de page sur un `mmap` : elles arrivent par morceaux de page, à des
242:    endroits dispersés dans le fichier, au rythme où le calcul les touche. Une
243:    copie séquentielle lit de gros blocs contigus.
244: 2. **Le chiffre à citer n'est pas « 130 Mo/s, c'est le disque »** mais **« 133
245:    Mio/s sur un plafond séquentiel de 205 »**. La différence est une question de
246:    motif, pas de matériel — et c'est une question sur laquelle on peut agir.
247: 
248: **Prédiction, avant mesure** : si la prélecture pouvait rapprocher le motif de la
249: passe du motif séquentiel, la même passe tomberait de 1 587 s à **≈ 1 030 s**.
250: L'essai de prélecture déjà consigné dans le code (×0,37, et 8,5× plus d'octets
251: lus) l'a tenté **en demandant l'union entière d'un coup**, ce qui a fait travailler
252: le noyau pour rien : ce n'est pas la même chose que de lire plus gros **au bon
253: moment**.
254: 
255: ---
256: 
257: ## 10. Le palier NVMe : la prédiction était de −16,3 %, la mesure donne −8,8 %
258: 
259: **Prédiction, écrite au §5 avant toute
… [12122 caractères tronqués]
  ```

- **read** `{"file_path": "reports/rapport-budget-kimi-k3.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-budget-kimi-k3.md</path>
<type>file</type>
<content>
1: # Kimi-K3 Q4 : ce qu'un jeton lit vraiment, et ce que ça impose
2: 
3: > Écrit le 03/10 (bloc 29) parce qu'un chiffre publié la veille était **faux par
4: > omission** : « un jeton lit ~35 Go de poids » ne comptait que les **experts**
5: > (`tools/analyse_octets_par_jeton.py`, écrit pour la question du MoE). Le total
6: > comprend aussi l'attention, les experts partagés et la tête — et c'est
7: > **87 Go par jeton**. Ce rapport donne la ventilation mesurée et ce qu'elle
8: > impose au placement.
9: 
10: ## 1. La ventilation, mesurée sur 25 couches (de 93), par type
11: 
12: | | par couche (Mo) | × 93 couches (Go/jeton) |
13: |---|---|---|
14: | **attention** (q/k/v/o, `ssm_*`, compresseur) | 554 (KDA) · 327 (MLA) | **48,7** |
15: | **experts routés** (16 sur 896) | 0,25 Go | **24,7** |
16: | **experts partagés** (2, ×93) | 140 | **12,4** |
17: | scores résiduels + tête de sortie | 0,06 + 1,25 (hors couche) | 1,3 |
18: | **TOTAL** | 15,5 Go | **87,0** |
19: 
20: Deux surprises, et les deux comptent :
21: 
22: 1. **L'attention pèse plus que les experts** (48,7
… [4261 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"EXPERTS_RAM\\|DRAVE_KEEP\\|keep\\b\\|--keep\\|GARDES\\|resident\\|resident-budget\\|DRAVE_K3_PRELIRE\\|prelire\" drave-core/src/model.rs drave-core/src/kimi_k3.rs drave-core/src/main.rs drave-core/src/engine.rs | head -60", "description": "Grep keep/resident/prefetch options"}`

  ```
drave-core/src/model.rs:402:/// `DRAVE_EXPERTS_GARDES=<fichier>` : une ligne par couche, `couche e1 e2 …`,
drave-core/src/model.rs:416:        let chemin = std::env::var("DRAVE_EXPERTS_GARDES").ok()?;
drave-core/src/model.rs:1215:    fn prelire_expert(&self, e: usize) {
drave-core/src/model.rs:1218:        crate::gguf::prelire(p, octets);
drave-core/src/model.rs:1287:    /// `-inf` élagué). Rempli depuis `DRAVE_EXPERTS_GARDES=<fichier>`, une ligne
drave-core/src/model.rs:1323:/// **Cache RAM des experts** (`DRAVE_EXPERTS_RAM` en Mo).
drave-core/src/model.rs:1424:/// Élague chaque ligne de sortie en ne gardant que la fraction `keep` des poids
drave-core/src/model.rs:1427:/// valeurs. `keep = 1.0` ne touche à rien.
drave-core/src/model.rs:1428:fn prune_rows(w: &mut [f32], n_out: usize, n_in: usize, keep: f32) {
drave-core/src/model.rs:1429:    if keep >= 1.0 { return; }
drave-core/src/model.rs:1430:    let k = ((n_in as f32 * keep) as usize).max(1);
drave-core/src/model.rs:1445:fn prune_structured(w: &mut [f32], n_out: usize, n_in: usize, keep: f32) {
drave-core/src/model.rs:1446:    if keep >= 1.0 { return; }
drave-core/src/model.rs:1447:    let win = ((n_out as f32 * keep) as usize
… [5620 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '1195,1240p' drave-core/src/model.rs; echo '=== CACHE RAM 1320,1420 ==='; sed -n '1320,1425p' drave-core/src/model.rs", "description": "Read expert prefetch and RAM cache code"}`

  ```
let mut reste = out;
            let mut o0 = 0usize;
            let mut poignees = Vec::new();
            while o0 < n_out {
                let o1 = (o0 + par).min(n_out);
                let (tranche, reste2) = reste.split_at_mut(o1 - o0);
                reste = reste2;
                poignees.push(sc.spawn(move || travail(o0, o1, tranche)));
                o0 = o1;
            }
            for p in poignees { let _ = p.join(); }
        });
    }

    /// Demande au noyau de lancer la lecture de l'expert `e` **en avance**.
    ///
    /// Le routeur choisit ses `k` experts avant tout calcul : on connaît donc
    /// les plages à lire une couche entière à l'avance. Les demander d'un coup
    /// laisse le noyau paralléliser ses lectures de pages, au lieu de les subir
    /// une par une au fil du calcul.
    fn prelire_expert(&self, e: usize) {
        let octets = self.octets_expert();
        let p = unsafe { self.base.add(e * octets) };
        crate::gguf::prelire(p, octets);
    }

    /// Octets bruts de l'expert `e` (tels qu'ils sont dans le fichier) : c'est
    /// ce qu'il faut copier en VRAM pour que le noyau y travaille.
    fn blocs_expert(&self, e: usize) -> &
… [5570 caractères tronqués]
  ```

- **read** `{"file_path": "reports/rapport-empreinte-memoire.md", "limit": 120}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-empreinte-memoire.md</path>
<type>file</type>
<content>
1: # Rapport — l'empreinte mémoire : ce qui réduit vraiment ce qu'il faut charger
2: 
3: Session du 01/10, de 10 h 47 à 17 h 35. Modèle d'étude : Qwen3-30B-A3B
4: (48 couches, 128 experts, top-8), dont on sait produire les traces de routage.
5: Cible : DeepSeek-V4.1-Flash (40 couches, **384 experts**, top-6, 365,7 Go).
6: 
7: **Résultat principal** : l'empreinte de V4.1 tombe de 365,7 Go à **50–80 Go**,
8: non pas en découpant les experts mais parce que **56 % du modèle (203 Go) est une
9: table d'engram creuse par nature**, qu'il suffit de mmapper. Une session de
10: 10 000 jetons n'en touche que **4,6 Mo**.
11: 
12: ## La question
13: 
14: Un modèle de 365 Go ne tient pas dans 125 Go de RAM. Que peut-on **ne pas
15: charger** ? Et parmi les pistes — découpage plus fin, grappes par langue, cache,
16: restriction du vocabulaire — lesquelles paient réellement ?
17: 
18: Toutes les mesures qui suivent viennent de traces de routage réelles
19: (`DRAVE_TRACE_EXPERTS`), pas d'estimations.
20: 
21: ## 1. La granularité : la courbe s'arrête à l'expert
22: 
23: Volu
… [3758 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '2360,2440p' drave-core/src/main.rs; echo '=== main 80,100 ==='; sed -n '78,100p' drave-core/src/main.rs", "description": "Read --materiel plan output"}`

  ```
// cherche les deux formes, sinon la taille tombe à zéro en silence.
            let trouve = |base: &str| {
                g.tensor(base).or_else(|| g.tensor(&format!("cl0/{base}")))
            };
            let mo = ["ffn_gate_exps.weight", "ffn_up_exps.weight", "ffn_down_exps.weight"]
                .iter()
                .filter_map(|s| trouve(&format!("blk.0.{s}")))
                // On divise par le nombre d'experts RÉELS du tenseur : dans un
                // fichier de cluster il n'y en a qu'une fraction (16 sur 128),
                // et diviser par le total donnait 0,38 Mo au lieu de 3,05.
                .map(|t| Gguf::octets_tensor(t) as f64 / (t.dims[0].max(1)) as f64)
                .sum::<f64>() / 1e6;
            if mo <= 0.0 {
                eprintln!("[materiel] taille d'expert introuvable (couche 0) : le plan \
utilisera 9,95 Mo par expert, valeur de DeepSeek-V4.1");
            }
            let mo = if mo > 0.0 { mo } else { 9.95 };
            let _ = (ffn, embd);
            let total = g.octets_poids() as f64 / 1e9;
            let _ = couches;
            if n_exp > 0 {
                println!("Modèle : {} · {:.1} Go · {} experts de {:.2} Mo\n",

… [4604 caractères tronqués]
  ```

- **read** `{"file_path": "reports/rapport-architecture-memoire.md", "offset": 310, "limit": 120}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-architecture-memoire.md</path>
<type>file</type>
<content>
310: Le code est conservé — il ne coûte rien et servira sur un modèle **plus gros que
311: le cache**, ce qui est précisément le cas de V4.1 (365 Go) — mais **il ne faut pas
312: le compter comme un gain** : sur cette machine et ces modèles, il n'en produit
313: aucun. Trois autres optimisations de la même famille se sont heurtées au même
314: mur : le calcul est 18× plus rapide que la lecture, et le noyau fait déjà son
315: travail.
316: 
317: ## 12. La tête restreinte à une liste de tokens : +15 %, mais pas transparent
318: 
319: Implémentée (`--tete-restreinte <fichier>`), sur les deux chemins de calcul —
320: `logits` par jeton et `logits_lot` par lots. **J'avais d'abord patché le mauvais**
321: et mesuré « aucun gain » : c'est en cherchant pourquoi que j'ai trouvé que
322: `--infer` passe par `logits`.
323: 
324: ### Équivalence du refactor : parfaite
325: 
326: Avec la liste **complète** (151 936 tokens), la sortie est **identique au token
327: près** à la tête non restreinte :
328: 
329: ```
330: sans     : [6224, 1076, 330, 438, 264, 1352, 315, 31
… [5054 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"tranche\\|Vue4\\|emprunter\\|fn octets_expert\\|DRAVE_SANS_EMPRUNT\" drave-core/src/list.rs drave-core/src/model.rs drave-core/src/formats.rs | head -50", "description": "Grep borrowed slice views"}`

  ```
drave-core/src/list.rs:440:    pub unsafe fn emprunter_q8(base: *const u8, n_out: usize, n_in: usize,
drave-core/src/list.rs:480:    /// Produit scalaire avec accumulation i32 par tranches de 256, reportée en
drave-core/src/list.rs:481:    /// i64 entre tranches. L'accumulation i64 sur toute la ligne empêchait
drave-core/src/list.rs:483:    /// 256 garantit qu'aucune tranche ne débordé (127 × 32767 × 256 = 1,07e9).
drave-core/src/list.rs:496:            // Débordement : 32 termes par tranche de 256 et par chaîne, soit
drave-core/src/list.rs:897:    pub unsafe fn emprunter_q4k(base: *const u8, n_out: usize, n_in: usize,
drave-core/src/list.rs:910:    pub unsafe fn emprunter_q6k(base: *const u8, n_out: usize, n_in: usize,
drave-core/src/list.rs:1070:    pub unsafe fn emprunter(base: *const u8, n_out: usize, n_in: usize,
drave-core/src/list.rs:1290:        // Un format IQ n'a pas de noyau ici : il passe par `Vue4::matvec_iq`.
drave-core/src/list.rs:1519:        let d = unsafe { DenseQ4::emprunter_q6k(bloc.as_ptr(), 1, n_in, 1) };
drave-core/src/model.rs:594:/// Type ggml → origine des blocs pour `Vue4`.
drave-core/src/model.rs:625:    let vues = |s: &str| -> Option<(Vec<usize>, Vec<Vu
… [3723 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '820,880p' drave-core/src/kimi_k3.rs; echo '=== 1130,1200 ==='; sed -n '1130,1200p' drave-core/src/kimi_k3.rs", "description": "Read K3 prefetch and dense arena"}`

  ```
mv(&self.rout_down, latent, h, cur, &mut ri);
            rin.push(ri);
            for (j, &e) in choisis.iter().enumerate() { groupes[e].push((i, poids[j])); }
            poids_par_jeton.push(poids);
        }
        self.appels.set(self.appels.get() + t);
        let _ = &poids_par_jeton;
        // ---- 3. un expert lu UNE fois, appliqué à tous ses jetons
        // Chaque fil a SES tampons : rien n'est partagé en écriture, seule la
        // lecture de `rin` l'est.
        let mut acc: Vec<Vec<f32>> = vec![vec![0f32; latent]; t];
        // **PRÉLECTURE DE TOUTE L'UNION, AVANT LE PREMIER CALCUL.** Le routeur a
        // parlé : on connaît les experts du lot avant d'en calculer un seul. Les
        // demander d'un coup laisse le noyau lancer ses lectures de pages EN
        // PARALLÈLE au lieu de les subir une par une — mesuré ailleurs dans ce
        // dépôt, le NVMe passe de 5,4 à 31 Go/s quand les lectures se
        // recouvrent. C'est aussi le test direct de l'hypothèse de DISPERSION :
        // si le temps vient des déplacements du disque, recouvrir les demandes
        // doit se voir tout de suite. `DRAVE_PRELIRE=0` l'éteint.
        // **ELLE EST ÉTEINTE PAR D
… [6003 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"fn open\\|fn open_auto\\|fn open_meta\\|read_to_end\\|read_exact\\|seek\\|read_at\\|nb_fichiers\\|octets_poids\\|data_ptr\" drave-core/src/gguf.rs | head -40; echo '=== run_plan start ==='; grep -n \"fn run_plan\" drave-core/src/main.rs", "description": "Inspect GGUF open path … [3 caractères tronqués]`

  ```
20:/// `read_to_end` fait deux choses coûteuses : il lit tout le fichier (18,55 Go
175:    f.read_to_end(&mut buf)?;
405:    pub fn open<P: AsRef<Path>>(path: P) -> std::io::Result<Self> {
428:    pub fn open_meta<P: AsRef<Path>>(path: P) -> std::io::Result<Self> {
432:            f.seek(SeekFrom::Start(0))?;
470:    pub fn open_multi<P: AsRef<Path>>(chemins: &[P]) -> std::io::Result<Self> {
478:    pub fn open_avec_prefixes<P: AsRef<Path>>(chemins: &[P], prefixes: &[&str])
630:    pub fn open_auto<P: AsRef<Path>>(path: P) -> std::io::Result<Self> {
644:    pub fn open_meta_auto<P: AsRef<Path>>(path: P) -> std::io::Result<Self> {
659:    pub fn open_multi_meta<P: AsRef<Path>>(chemins: &[P]) -> std::io::Result<Self> {
665:    pub fn open_meta_avec_prefixes<P: AsRef<Path>>(chemins: &[P], prefixes: &[&str])
680:                f.seek(SeekFrom::Start(0))?;
826:    pub fn octets_poids(&self) -> u64 {
833:    pub fn nb_fichiers(&self) -> usize { self.starts.len() }
960:    /// normalisées (`deepseek4.hyper_connection.*`), V4.1 seulement dans le
961:    /// `config.json` recopié sous `deepseek41.config` (`hc_mult`,
1557:    pub fn data_ptr(&self, name: &str) -> Option<*const u8> {
1901:  
… [351 caractères tronqués]
  ```

- **read** `{"file_path": "reports/rapport-localite-activation.md"}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-localite-activation.md</path>
<type>file</type>
<content>
1: # Localité d'activation : ce que PowerInfer apporte, et ce qu'on en garde
2: 
3: > Étude demandée du dépôt [SJTU-IPADS/PowerInfer](https://github.com/SJTU-IPADS/PowerInfer)
4: > (miroir `Tiiny-AI/PowerInfer`), confrontée à nos propres mesures. Tout ce qui
5: > suit est mesuré sur cette machine ; les chiffres de PowerInfer viennent de leur
6: > README et de l'article SOSP 2024.
7: 
8: ## 1. Leur idée
9: 
10: La distribution des activations d'un LLM suit une **loi de puissance** : une
11: petite partie des neurones est active presque toujours (« chauds »), le reste
12: dépend de l'entrée (« froids »). PowerInfer en tire un moteur hybride CPU/GPU
13: **à la granularité du neurone** : les chauds résident sur le GPU, les froids sont
14: calculés sur le CPU, ce qui réduit à la fois la VRAM nécessaire et le trafic
15: PCIe. S'y ajoutent un **prédicteur** (un petit MLP qui devine l'ensemble actif
16: pour précharger) et des **opérateurs creux conscients des neurones**. Leur modèle
17: TurboSparse (≈ 90 % de creux) est *entraîné* ainsi, précisément parce
18: qu'
… [4077 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"n_lecteurs\\|plan.lecteurs\\|\\.lecteurs\" drave-core/src | head; echo '=== main 15,40 ==='; sed -n '15,40p' drave-core/src/main.rs; echo '=== run_plan 4769,4820 ==='; sed -n '4769,4810p' drave-core/src/main.rs; echo '=== model 7550,7620 ==='; sed -n '7548,7620p' drave-core/s … [71 caractères tronqués]`

  ```
drave-core/src/materiel.rs:470:        assert!(p.lecteurs >= 1);
drave-core/src/main.rs:2400:    println!("  lecteurs disque  : {}", plan.lecteurs);
=== main 15,40 ===
/// une variable lue mais absente d'ici rendrait le message muet, et une variable
/// listée mais jamais lue annoncerait une option qui n'existe pas.
const VARS_LUES: &[&str] = &[
    "BANC_KV_DEBUG", "BANC_KV_GPU_SEUL", "BANC_KV_GRAD", "BANC_KV_K0",
    "BANC_KV_KUNIT", "BANC_KV_UNIT", "BANC_KV_V1", "BANC_SANS_PUITS",
    "CLUSTERS", "DEBUG_ETAT", "DEBUG_FLUX", "DEBUG_MLA", "DEBUG_YARN", "DUMP_COUCHES",
    "ETAT_ENTREE",
    "FLUX_VERIF", "GPU", "GPU_EXPERTS",
    "GPU_EXPERTS_GO", "GPU_KV", "GPU_TETE", "GPU_TOPK", "HARMONY_TRACE",
    "KV_BITS", "KV_F16", "KV_K_F16", "KV_K_F32", "KV_V_F32", "MMAP",
    "BIAIS_VL", "EXPERTS_RAM", "PRELIRE", "PRELIRE_TOUT", "Q8_BLOCS", "SANS_ENGRAM",
    "SANS_EMPRUNT",
    "TRACE_BLOCS", "TUILE_LOT", "K3_COUCHES", "K3_SANS_ETAT", "K3_PASSE", "K3_TETE", "K3_LOGITS", "K3_GEN", "K3_MXFP4", "K3_TRACE_EXPERTS", "K3_IDS", "K3_DENSE_FIGE", "K3_STATS_EXPERTS", "K3_RELAIS_ENTREE", "K3_RELAIS_SORTIE", "HEBB_SEUIL", "HEBB_SIGNE", "HEBB_DECROI", "HEBB_SAUVER", "HEBB_CHARGER", "K3_PRELIRE_UNION
… [7287 caractères tronqués]
  ```

- **read** `{"file_path": "drave-core/src/main.rs", "offset": 1684, "limit": 180}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
1684: /// Sonde d'accès mmappé à la table d'engram.
1685: ///
1686: /// `blk.N.engram_embd.weight` pèse 101,4 Go par couche sur DeepSeek-V4.1 — plus
1687: /// que tous les experts réunis. Ce n'est pourtant **pas un tenseur de poids** :
1688: /// c'est une table de hachage de n-grammes, et un jeton n'en lit que quelques
1689: /// entrées de 264 octets. La charger serait une faute ; il faut l'**adresser**.
1690: ///
1691: /// Cette sonde le démontre : elle ouvre le fichier entier en mmap, lit `n`
1692: /// entrées dispersées, et affiche le temps comme la mémoire. Le noyau ne lit que
1693: /// les pages touchées.
1694: /// **La liste d'adresses de l'engram** (P8) : quelles rangées le modèle irait
1695: /// lire pour une séquence de jetons.
1696: ///
1697: /// Elle se calcule **sans charger le modèle** — les métadonnées suffisent (48
1698: /// premiers, 8 multiplicateurs, la table de correspondance des jetons) — et
1699: /// c'est tout l'intérêt : on peut la comparer à la référence
1700: /// (`tools/engram_reference.py`) sur un fichier de 365 Go sans lire un poids.
1701: fn r
… [9526 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"Mo/s utiles\\|sonder-engram\\|entrées/s\\|ms par entrée\" reports/ docs/ 2>/dev/null | head -20", "description": "Grep engram probe measurements"}`

  ```
reports/rapport-optimisations-auto.md:104:16 ms par entrée de 264 octets — là, la prélecture aurait de quoi faire, et c'est
reports/rapport-provenance-v41.md:68:1. **l'engram** (P8) : `--sonder-engram` lit déjà ses tables (10 000 entrées en
reports/rapport-engram-etat.md:27:| sonde | `--sonder-engram 10000` : **219 à 524 ms**, **2,6 Mo touchés** par table, **120 Mo de RSS** pour 365,7 Go | `reports/rapport-execution-v41.md` |
reports/rapport-engram-etat.md:146:l'engram est ce qu'il fait : **l'adresser** (`--sonder-engram`), le **compter**
reports/rapport-execution-v41.md:29:| sonde engram (`--sonder-engram 10000`) | mmap, 16 lecteurs | table 1 : 10 000 entrées en **524 ms** (2,6 Mo touchés sur 101,4 Go) · table 2 : **219 ms** · RSS max **120 Mo** pour 365,7 Go adressés |
reports/rapport-execution-v41.md:90:drave $V --sonder-engram 10000          # 203 Go de tables adressées, 5 Mo touchés
docs/glossaire.md:994:| modèles | `--config`, `--tensors`, `--plan`, `--couches`, `--tete-partielle`, `--patch`, `--tete-restreinte`, `--tete-garantie`, `--sonder-engram` |
docs/plan-deepseek41-complet.md:800:> e8m0 = **264 octets**. La sonde (`--sonder-engram 10000`) touche 2,6 Mo par
  ```

- **bash** `{"command": "grep -rn \"DRAVE_MMAP\\|MADV_WILLNEED\\|madvise\\|page cache\\|buff/cache\" reports/*.md docs/*.md 2>/dev/null | head -30", "description": "Grep mmap/page cache in reports"}`

  ```
reports/rapport-architecture-memoire.md:295:`madvise(MADV_WILLNEED)` — c'est la seule forme de parallélisme de lecture
reports/rapport-architecture-memoire.md:308:`MADV_WILLNEED` n'a rien à lancer.
reports/rapport-lecteur-multifichiers.md:182:| lu en entier (`DRAVE_MMAP=0`) | 30,68 s | 19,20 Go |
reports/rapport-materiel-disque-ou-cpu.md:16:| RAM | 125 Go (≈ 110 Go disponibles, ≈ 95 Go en `buff/cache`) |
reports/rapport-optimisations-auto.md:79:| `madvise(WILLNEED)` après le routage (experts) | 25,73 s contre 25,80 | 0,3 % |
reports/rapport-optimisations-auto.md:80:| `madvise` sur tout le fichier au chargement | 7,29 s contre 7,47 | −2 % |
reports/rapport-optimisations-auto.md:109:**La prélecture parallèle** (`madvise(MADV_WILLNEED)` après le routage) :
reports/rapport-p0-flux.md:109:(41,8 s contre 215,7 s pour la première, page cache), donc comparer
reports/rapport-reutilisation-experts.md:116:   hiérarchie de stockage* : le noyau servait déjà tout depuis le `buff/cache`.
reports/rapport-vitesse-v41.md:51:| **cache RAM des experts** (justifié par une trace : 50 % des lectures dans 394 experts, 31,9 % de réutilisation entre jetons consécutifs) | **plus lent** : passe ctx 32 = 145,1
… [1965 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '160,200p' reports/rapport-lecteur-multifichiers.md; echo '=== optimisations-auto 70,115 ==='; sed -n '70,115p' reports/rapport-optimisations-auto.md; echo '=== glossaire 1245,1260 ==='; sed -n '1245,1260p' docs/glossaire.md", "description": "Read mmap vs read measurements"}`

  ```
93,08 = 93,1 · Qwen3-235B 85,68 = 85,7. **La file de 1 138 Go est terminée**, et
chacun de ses modèles est complet : le lecteur refuse un découpage dont un shard
manque. Une seule entrée
fausse dans la table des types ggml donnerait un écart visible sur des centaines
de gigaoctets — c'est ainsi que `iq1_m` manquant avait fait annoncer 8,56 Go pour
86,9 Go.

Les architectures sont lues (`deepseek41`, `deepseek2`, `deepseek4`, `glm-dsa`) ;
aucune n'a encore de `forward`. Kimi est en huit fichiers, GLM en six : le lecteur
les rassemble à partir d'un seul chemin.

### Le mmap : 3,3× plus rapide, 3× moins de mémoire

`read_to_end` lisait tout le fichier et en gardait une copie dans le tas, **en
plus** du cache de pages du noyau — deux fois la taille du modèle en mémoire
physique. Les fichiers sont maintenant **mappés** (le noyau lit les pages à la
demande). Sur Qwen3-30B-A3B en clusters, mêmes 7 jetons, perplexité identique
(799,8557 dans les deux cas) :

| | chargement + passe | mémoire maximale (RSS) |
|---|---|---|
| mappé (défaut) | **9,32 s** | **6,35 Go** |
| lu en entier (`DRAVE_MMAP=0`) | 30,68 s | 19,20 Go |

Les 19,20 Go sont exactement la taille du modèle : la copie complète.
… [4201 caractères tronqués]
  ```

- **bash** `{"command": "grep -n \"resume()\\|--materiel\\|materiel\" drave-core/src/main.rs | head -20; echo '=== resident 4595,4640 ==='; sed -n '4590,4640p' drave-core/src/model.rs", "description": "Read resident cache helper and materiel dispatch"}`

  ```
43:mod materiel;
84:        eprintln!("       drave <modele> --materiel     détection matérielle et plan de");
125:        (opt.gpu_banc, "--gpu-banc"), (opt.materiel, "--materiel"), (opt.config, "--config"),
134:    if opt.materiel { run_materiel(&opt); return; }
611:    materiel: bool,
782:            "--materiel" => { o.materiel = true; 1 }
2333:fn run_materiel(opt: &Options) {
2334:    let m = materiel::Materiel::detecter();
2335:    print!("{}", m.resume());
2373:                eprintln!("[materiel] taille d'expert introuvable (couche 0) : le plan \
=== resident 4595,4640 ===
    /// Produit scalaire d'un expert, **quel que soit son format** : noyau 4 bits
    /// emprunté quand il existe, déquantification sinon.
    ///
    /// Les formats IQ (IQ1_S, IQ1_M, IQ2_XXS, IQ3_XXS) portent 30 % des poids de
    /// Kimi-K2.7, GLM-5.3 et DeepSeek-V4. Ils n'ont pas de noyau ici, et les
    /// refuser rendait ces modèles inchargeables — « mélanges d'experts
    /// chargés : 0/79 » était la seule trace, sans dire pourquoi.
    /// Redirige une vue d'expert vers le cache RAM s'il la connaît, et l'y met
    /// sinon. Retourne la vue à employer et le `loc` qui va avec (0 quand la
    /
… [2338 caractères tronqués]
  ```

- **bash** `{"command": "sed -n '300,345p' docs/verification-kimi-k3.md; echo '=== roadmap 100,115 ==='; sed -n '100,115p' docs/roadmap-drave.md", "description": "Check dense arena swap claim"}`

  ```
```

**62,8 Go de swap, dont 53 Go utilisés.** La mémoire anonyme est donc
récupérable, et l'arène s'est mise à swaper : `VmSwap` du processus = **28,5 Go**,
mémoire disponible tombée à 7 Go. La passe aurait été plus lente, pas plus
rapide. Arrêtée avant la fin.

**Ce que ça laisse** : sur cette machine, le dense ne peut pas être rendu
résident à bon compte. La page cache ne le garde pas (mesuré), la copie anonyme
swape (mesuré), et `mlock` de 32 Go demande `CAP_IPC_LOCK` — les limites
habituelles sont de quelques mégaoctets. Le mécanisme reste **opt-in**
(`DRAVE_K3_DENSE_FIGE=1`), documenté, et **déconseillé** ici.

**Leçon de méthode, et elle est la même que celle du bloc 31** : un instrument
qui n'existe pas ne renvoie pas « non ». `swapon --show` vide, `grep` sans
résultat, un fichier absent — le silence n'est une mesure que si l'on a vérifié
que l'outil était là. La bonne source est `/proc/swaps`, qui est un fichier.

### Et l'hypothèse du cache de pages est RÉFUTÉE

La thèse était : « ne plus déquantifier, et le cache de pages gardera les 59,6 Go
du dense entre deux passes ». **Deux passes complètes enchaînées, même
processus :**

| | passe 1 | passe 2 |
|---|---:|---:|
| cha
… [2240 caractères tronqués]
  ```

- **bash** `{"command": "grep -rn \"DRAVE_KEEP\\|prefetch\\|DRAVE_FILS\\|DRAVE_LECTEURS\\|O_DIRECT\\|pread\" drave-core/src/ | head; echo \"[fin greps]\"; grep -c \"\" drave-core/src/materiel.rs", "description": "Confirm absent env vars and syscalls"}`

  ```
[fin greps]
478
  ```

- **bash** `{"command": "sed -n '4300,4312p' drave-core/src/model.rs; echo '=== 4368,4380 ==='; sed -n '4368,4380p' drave-core/src/model.rs; echo '=== main 840,850 ==='; sed -n '840,850p' drave-core/src/main.rs", "description": "Read GPU expert cache budget and stats"}`

  ```
let m = crate::materiel::Materiel::detecter();
                let libre: f64 = m.gpus.iter().map(|g| g.vram_libre_go).sum();
                (libre - 2.0).max(1.0)      // 2 Go de réserve pour le contexte CUDA
            };
            let go: f64 = std::env::var("DRAVE_GPU_EXPERTS_GO").ok()
                .and_then(|v| v.parse().ok()).unwrap_or(defaut);
            let budget = (go * 1e9) as usize;
            println!("[gpu] cache d'experts : budget {:.1} Go de VRAM (LRU), éviction par (couche, expert)",
                     go);
            Some(CacheExperts::nouveau(budget))
        } else { None };
        let head4 = if q4 & 4 != 0 || tete_quantifiee {
            let t0 = Instant::now();
=== 4368,4380 ===
            couche_debut: couches.map(|(a, _)| a).unwrap_or(0),
            couche_fin: couches.map(|(_, b)| b).unwrap_or(n_layer_total),
            flux_brut: false, tete_partielle: false,
            cache_experts,
            cache_ram: match std::env::var("DRAVE_EXPERTS_RAM").ok()
                            .and_then(|v| v.parse::<usize>().ok()) {
                Some(mo) if mo > 0 => {
                    println!("[experts] cache RAM des experts : {mo} Mo — ATTEN
… [821 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Rédaction du condensé factuel et envoi au parent

Inventaire terminé : code, portes et rapports croisés. Voici le condensé.

**1) Tableau — capacités mémoire / disque / fils**

| Capacité | Ce qu'elle fait | fichier:ligne | État | Chiffre mesuré |
|---|---|---|---|---|
| Détection matérielle | lit /sys (cœurs physiques vs logiques, paires SMT, NUMA + cpulist, caches L1/L2/L3), /proc/meminfo, `nvidia-smi` (VRAM, NVLink), `df`/`findmnt` (disques + nœud NUMA) ; `--materiel` affiche `resume()` + `plan()` | materiel.rs:91-157, 178-273, 276-282, 408-435 ; main.rs:2333-2335 | mesuré (machine réf. : 20 cœurs/40 fils, 125 Go, 2×RTX 5000, NVMe MAP1602, `sda` ROTA=1) | RAM 22,5 Go/s · VRAM 84,9 · NVMe 31,1 (16 lecteurs) |
| Threads par défaut | prend les cœurs **physiques** (jamais `available_parallelism`) ; `--threads` l'emporte ; pool borné à CPU logiques−1 | engine.rs:289-313 ; main.rs:162, 666-667, 872, 521-527 ; engine.rs:390-393 | mesuré (défaut = 20 fils ; l'ancien `cpu×3/4` donnait 30) | 20 cœurs 22,5 Go/s ; 40 fils 22,8 (« rien de plus ») ; 10 cœurs 14,7 → +HT 18,7 (+27 %) |
| Affinité des fils | `--pin` → `EPINGLER` ; `sched_setaffinity` par syscall 203 ; cibles = 1ʳᵉ moitié de chaque `node*/cpulist` (cœurs physiques des 2 sockets) | engine.rs:268-334, 337-364 ; main.rs:778, 835 | mesuré, **aucune porte** | 20,7 → **24,7 Go/s** avec épinglage ; 16 fils sur node 0 seul : **−16 %** |
| mmap des poids | `Mappe` (PROT_READ, MAP_PRIVATE) par fichier ; `Tampon::Lu` si `DRAVE_MMAP=0` (`read_to_end`) ; accès par expert/tranche **empruntée** (`DenseQ4::emprunter`, `Vue4`) ; `DRAVE_SANS_EMPRUNT=1` force la recopie | gguf.rs:30-177, 155-160 ; list.rs:897/910/1070 ; model.rs:824, 1096, 1213-1241, 1528-1540 | mesuré (mmap = défaut) | 9,32 s/6,35 Go (mmap) vs 30,68 s/19,20 Go (lu) ; **47 Mo RSS pour 365,7 Go adressés** |
| Prélecture | `madvise(MADV_WILLNEED)` par expert après le routage (`gguf::prelire` ; `DRAVE_PRELIRE=0` l'éteint) ; tout le fichier `DRAVE_PRELIRE_TOUT=1` (off) ; union K3 `DRAVE_K3_PRELIRE_UNION=1` (off) | gguf.rs:52-99 ; model.rs:7562-7564, 1215-1219 ; kimi_k3.rs:838-855 | mesuré, **sans gain ici** | +0,3 % (25,73 vs 25,80 s) ; union K3 **×0,37** (6:57 vs 2:34) |
| Éviction / cache d'experts | VRAM : LRU par (couche, expert), budget `DRAVE_GPU_EXPERTS_GO` (défaut VRAM libre−2 Go) ; RAM : `DRAVE_EXPERTS_RAM` Mo, LRU par horloge ; arène dense K3 `DRAVE_K3_DENSE_FIGE=1` | model.rs:1573-1646, 1323-1390, 4298-4310, 4368-4380 ; kimi_k3.rs:1138-1185 | mesuré, **désactivé/déconseillé**, pas de porte | RAM +4 % (4 Go), +21 % (32 Go) ; K3 VRAM plafond ×1,41, verdict **×1,09** (LRU-32 = 34,5 %) |
| Lecteurs disque | `plan.lecteurs = 16.min(physiques.max(4))` — **calculé et affiché, mais jamais utilisé ailleurs** (seul appel main.rs:2400) | materiel.rs:318-325 ; main.rs:2400 | **supposé** (recommandation non câblée) ; parallélismes réels : page faults noyau, sonde engram ≤16 fils (main.rs:1821), K3 ≤16 fils (kimi_k3.rs:874) | NVMe ×6 (5,37→31,08) ; engram 10 000 entrées en 219–524 ms, 2,6 Mo touchés |

`DRAVE_KEEP`, `DRAVE_FILS`, `DRAVE_LECTEURS`, `prefetch`, `pread`, `O_DIRECT` : **inexistants dans drave-core/src** (grep vide).

**2) Débits disque mesurés et goulot**
- NVMe MAP1602 (node 0) : 1 lecteur **5,37** → 4 **18,08** → 8 **28,29** → 16 **31,08 Go/s** (rapport-architecture-memoire.md:179-184) ; parcours 50,5 Go/395 fichiers : 3,42 / 21,02 / 33,19 (l.183) ; `dd iflag=direct` = 8,39 Go en 4,247 s = **2,0 Go/s** (rapport-materiel-disque-ou-cpu.md:26-28). Réserve : tout tient dans les ~112 Go de page cache et `O_DIRECT` échoue (errno 29) → l'absolu n'est pas « froid » (architecture:192-195).
- Disque dur `sda` (WD120EFGX, ROTA=1) : passe K3 = 1 587 s pour **206,58 Gio** lus = **133,5 Mio/s** ; plafond séquentiel `cp` **205 Mio/s** → la passe n'en obtient que **65 %** (rapport-passe-k3-disque.md:60-61, 229-234) ; `dm-1` occupé 87,6 %, file ≈14, CPU 21 %.
- Goulot : **K3 sur HDD → le disque** (206,58 Go / 130 Mo/s = 1 589 s vs 1 587 s mesuré, écart 0,1 % ; loi `octets(T)=79,0+31,9·T` Gio, §11) ; **V4.1 Q2 sur NVMe → le calcul** (375 s CPU en 16 s de mur, ~0,6 Go/s lus = 30 % du disque) ; V4-Flash 82 Go sur HDD : `read_bytes=0`, entièrement en page cache. Critère « 10 min » inatteignable : coût fixe 79,0 Gio > 77,9 Gio ; à 3 nœuds ≈ 8,8 min.

**3) Vérifié automatiquement vs mesuré à la main**
- **Auto** : `tools/portes.sh:63-68` est la **seule** porte matérielle — « threads par défaut » (`--materiel`, 0 < threads ≤ `nproc/2`). Tests unitaires materiel.rs:442-477 (détection cohérente, plan dans les bornes). **Rien sur mmap, disque, éviction, prélecture ou affinité.**
- **À la main** : `tools/sonde-passe-k3.sh` + CSV (passe K3), `--sonder-engram`, `--gpu-banc`, banc mémoire (main.rs:268-296), porte de découpage `tools/test-plage-k3.sh` (bit à bit).
- **Statuts** : *mesuré* = rapports avec protocole/appariement ; *déduit* = `cout_par_jeton` (materiel.rs:381-406 : constantes 84,9/22,5/31 Go/s, succès 0,80) et extrapolation à N nœuds ; *supposé* = `plan.lecteurs` non câblé, et l'hypothèse « cette machine n'a pas de swap » (kimi_k3.rs:1144-1148) **contredite** par docs/verification-kimi-k3.md:300-303 (62,8 Go de swap, VmSwap 28,5 Go) — `swapon --show` muet ne prouve rien, la source est `/proc/swaps`.

- **send_message** `{"agent_id": "482522d1-31f1-43eb-ae9c-a681336404f7", "message": "INVENTAIRE MÉMOIRE / DISQUE / FILS — drave-core (lecture seule, aucun fichier modifié)\n\n**1) Capacités**\n\n| Capacité | Fait | fichier:ligne | État | Chiffre |\n|---|---|---|---|---|\n| Détection matérielle | /sys (cœurs physiques v … [4215 caractères tronqués]`

  ```
message delivered to agent 482522d1-31f1-43eb-ae9c-a681336404f7
  ```

### 🤖 Assistant

Résultat envoyé au parent (`482522d1-…`) : l'inventaire ci-dessus tient en ~28 lignes, avec les trois distinctions demandées (mesuré / déduit / supposé), les chemins et numéros de ligne, et deux constats à retenir — `plan.lecteurs = 16` n'est **pas câblé** (materiel.rs:322, seul usage main.rs:2400) et **aucune porte** ne couvre mmap, disque, éviction ou affinité (tools/portes.sh:63-68 ne teste que les threads par défaut).

