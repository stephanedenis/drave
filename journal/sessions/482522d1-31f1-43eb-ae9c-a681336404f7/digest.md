# Session DSH — relecture

- identifiant : `482522d1-31f1-43eb-ae9c-a681336404f7`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-10-08 09:18:07
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave » : un moteur d'inférence en Rust, drave-core/, qui charge des GGUF en place et fait tourner de gros modèles sur une machine à RAM limitée ; outils dans tools/, rapports dans reports/, reprise dans REPRISE.md).

MISSION : inventorier les capacités de DISTRIBUTION et d'EXPLOITATION HÉTÉROGÈNE du moteur — répartir le calcul sur les différentes unités de traitement et ressources d'UNE machine (cœurs CPU, GPU, disques, RAM), et sur PLUSIEURS machines en réseau.

CE QU'IL FAUT EXAMINER :
- le calcul réparti entre deux nœuds : cherche « flux-serveur », « nœud », « pilote », les modes de transport (chercher dans drave-core/src/ et tools/pair_factice.py, tools/portes.sh) ;
- le découpage en clusters et le découpage par plages de couches : cherche DRAVE_K3_RELAIS_ENTREE / DRAVE_K3_RELAIS_SORTIE, « relais », « plage », « cluster », tools/convertir_clusters.py, tools/clusters_moe.py, docs/format-clusters.md ;
- l'usage du GPU : DRAVE_GPU, le dispatch automatique des projections, le top-k GPU, docs/plan-gpu-topk.md, tools/gpu_*.py, tools/trace_gpu.py, et les scripts de banc (bench/) ;
- la gestion mémoire et disque : mmap, page cache, DRAVE_MMAP, l'affinité des fils (threads), la détection matérielle ;
- l'état des PORTES : tools/portes.sh, `cargo test`, et quels modes de transport/découpage sont réellement couverts par une porte.

RENDS un rapport en français :
1. TABLEAU par capacité : nom, ce qu'elle fait, état (implémentée et vérifiée par une porte / implémentée mais mesurée seulement en local / non testée), fichier source, et le chiffre mesuré s'il existe.
2. Ce qui est PROUVÉ par une porte (et laquelle), et ce qui ne l'est pas.
3. Ce qui manque concrètement pour (a) répartir sur les unités d'UNE machine, (b) répartir sur PLUSIEURS machines en réseau — en citant le code qui manque ou qui bloque (par exemple un transport par fichier au lieu d'un transport réseau).
4. Les limites mesurées : débits réseau/PCIe/disque, goulots identifiés.

CONTRAINTES : ne modifie AUCUN fichier, ne lance aucune compilation ni aucun test. Distingue « mesuré », « déduit », « supposé ». Rapport final : 150 lignes maximum, dense et factuel, avec chemins de fichiers.
Your parent agent id is "d31b3d9b-58e4-4d34-85fa-381b6f6a6a76". Before you finish, send your result to that agent with send_message({ agent_id: "d31b3d9b-58e4-4d34-85fa-381b6f6a6a76", message: "<self-contained result>" }). The parent shares your workspace but does not automatically receive your transcript, tool output, or reasoning. Send earlier messages as well when a finding changes what the parent should do next; sending a message does not end your turn.

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

⏵ Inventaire des capacités de distribution du moteur Drave — lecture seule
Je commence par cartographier le dépôt, puis je lirai les fichiers ciblés par la mission.

- **bash** `{"command": "ls -la; echo \"---\"; ls drave-core/src/ 2>/dev/null | head -60; echo \"---TOOLS\"; ls tools/ 2>/dev/null | head -80; echo \"---BENCH\"; ls bench/ 2>/dev/null | head -40; echo \"---DOCS\"; ls docs/ 2>/dev/null | head -60", "description": "List repo structure"}`

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
… [3107 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -15 2>/dev/null; echo \"---\"; wc -l REPRISE.md 2>/dev/null; ls reports/ 2>/dev/null | head -60", "description": "Show git log and reports"}`

  ```
7d32b4f Déclare DRAVE_K3_RELAIS_ENTREE et DRAVE_K3_RELAIS_SORTIE dans VARS_LUES
3c2b542 Chantier 3 : un nœud = une plage de couches, et la porte est TENUE au bit près
6f62aec §11 : la loi des octets (79,0 + 31,9·T Gio) validée sur trois points — et le critère du chantier 2 est impossible
9eb9732 Le corpus complet confirme : la bande sémantique 10–15 ne bouge pas quand le corpus double
8b232d0 Premier résultat du cycle rapide : la première couche sémantique est dans la bande 10–15
372385d premiere_couche_semantique : chemin numpy rapide (vérifié identique au lent) et cache
f655a8b Le cycle rapide : l'article 1 de l'UDHR dans 399 langues, et pourquoi le modèle n'est pas le bon levier
6df6de4 §10 : le palier NVMe donne −8,8 %, la prédiction était de −16,3 %
d1cb6b5 Feuille de route : le regroupement par expert EXISTE, l'axe 1 devient un axe de LOT
abebe58 §9 : le plafond du disque est 205 Mio/s, la passe en obtient 133
3169941 Attribution des 206,58 Gio : 72 % sont les experts, relus à chaque jeton
648aad6 Où passe le temps d'une passe Kimi-K3 : le disque dur, et rien d'autre
84160d1 §95 : la portée du contexte — le voisin immédiat porte presque tout
0b0161f localite_couches : le témo
… [1698 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Cartographie faite ; je grep maintenant les points clés (relais, flux-serveur, GPU, mmap)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"DRAVE_K3_RELAIS\\|DRAVE_GPU\\|DRAVE_MMAP\\|DRAVE_FLUX\\|DRAVE_NOEU\" --include=*.rs --include=*.sh --include=*.py --include=*.md . 2>/dev/null | grep -v \"^./reports/\" | head -80", "description": "Grep key env vars"}`

  ```
./tools/aiguille.py:75:        env["DRAVE_GPU"] = "1"
./tools/aiguille.py:77:        env["DRAVE_GPU"] = "1"
./tools/aiguille.py:78:        env["DRAVE_GPU_KV"] = "1"
./tools/aiguille.py:80:        env["DRAVE_GPU"] = "1"
./tools/aiguille.py:81:        env["DRAVE_GPU_KV"] = "1"
./tools/aiguille.py:82:        env["DRAVE_GPU_TOPK"] = "1"
./tools/aiguille.py:134:    ap.add_argument("--gpu", action="store_true", help="DRAVE_GPU=1 (déport des projections)")
./tools/aiguille.py:135:    ap.add_argument("--gpu-kv", action="store_true", help="DRAVE_GPU=1 DRAVE_GPU_KV=1 (KV en VRAM)")
./tools/aiguille.py:143:                    help="DRAVE_GPU=1 DRAVE_GPU_KV=1 DRAVE_GPU_TOPK=1")
./tools/test-plage-k3.sh:25:DRAVE_K3_PASSE=93 DRAVE_DUMP_COUCHES=/tmp/pl_A DRAVE_K3_RELAIS_SORTIE="$R" \
./tools/test-plage-k3.sh:30:DRAVE_K3_PASSE=93 DRAVE_DUMP_COUCHES=/tmp/pl_B DRAVE_K3_RELAIS_ENTREE="$R" \
./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:21490:"DRAVE_BANC_KV_DEBUG" "DRAVE_BANC_KV_GPU_SEUL" "DRAVE_BANC_KV_GRAD" "DRAVE_BANC_KV_K0" "DRAVE_BANC_KV_KUNIT" "DRAVE_BANC_KV_UNIT" "DRAVE_BANC_KV_V1" "DRAVE_GPU" "DRAVE_GPU_EXPERTS" "DRAVE_GPU_EXPERTS_GO" "DRAVE_GPU_KV" "DRAVE_GPU_TETE" "DRAVE_
… [22135 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls tools/ | tail -60; echo \"---PORTES\"; ls tools/porte*; echo \"---\"; grep -rn \"VARS_LUES\" -l drave-core/src/ tools/ 2>/dev/null", "description": "List rest of tools and portes"}`

  ```
ou_est_le_contenu.py
pair_factice.py
plateau_multilingue.py
pont_fidele.py
pont_generatif.py
pont_parallele.py
pont_recurrent.py
pont_reglages.py
pont_reservoir.py
pont_unites.py
porte-flux.sh
portes_formats.sh
portes.sh
porte-tokenizer-kimi.sh
position_seule.py
premiere_couche_semantique.py
preparer_colab.sh
profil_couches.py
profil_flux.py
profil_langues.py
proxy_latence.py
__pycache__
rapport_du_pont.py
ref_ggml_bloc.c
ref_logits
ref_logits.cpp
ref_logits_k3
ref_logits.md
renforcement_directions.py
renforcement.py
rope_yarn_temoin.py
saturation.py
session_report.py
sonde-passe-k3.sh
sonde_pont.py
sous_ensemble_actif.py
sous_espace_du_contenu.py
sprint.sh
stabilite_directions.py
stabilite_evenements.py
telecharger_modeles.py
test-plage-k3.sh
tokenize_llama
tokenize_llama.cpp
tokenizer_kimi
trace_compacite.py
trace_gpu.py
transfert_ridge.py
v41_attention_blocs.py
v41_attention_coeur.py
v41_attention_reference.py
v41_compresseur_reference.py
v41_experts_reference.py
verifier_formats.py
verifier_table_types.sh
verifier_v41_engram.py
verifier_v41_mhc.py
vision_mtmd.py
vision_ref.py
wiki_apparie.py
---PORTES
tools/porte-flux.sh
tools/portes_formats.sh
tools/portes.sh
tools/porte-token
… [39 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des sources clés : clusters.rs, flux/relais dans main.rs, portes

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && wc -l drave-core/src/*.rs tools/portes.sh tools/porte-flux.sh tools/portes_formats.sh tools/pair_factice.py tools/convertir_clusters.py tools/clusters_moe.py tools/test-plage-k3.sh tools/trace_gpu.py docs/format-clusters.md docs/plan … [91 caractères tronqués]`

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
    336 tools/portes.sh
    125 tools/porte-flux.sh
     74 tools/portes_formats.sh
    151 tools/pair_factice.py
    586 tools/convertir_clusters.py
    224 tools/clusters_moe.py
     55 tools/test-plage-k3.sh
    197 tools/trace_gpu.py
    189 docs/format-clusters.md
    139 docs/plan-gpu-topk.md
    132 docs/colab-reparti.md
  30695 total
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"flux-serveur\\|flux_serveur\\|FluxServeur\\|--flux\\b\\|--serveur\\|TcpListener\\|TcpStream\\|UnixStream\\|127.0.0.1\\|localhost\" --include=*.rs drave-core/src/ | head -40", "description": "Grep network transport in Rust  … [9 caractères tronqués]`

  ```
drave-core/src/main.rs:121:        (opt.flux_serveur.is_some(), "--flux-serveur"),
drave-core/src/main.rs:140:    if let Some(adresse) = opt.flux_serveur.clone() { run_serveur_flux(opt, &adresse); return; }
drave-core/src/main.rs:567:    /// au-delà de localhost (un pair distant, un tunnel, une autre machine).
drave-core/src/main.rs:568:    flux_serveur: Option<String>,
drave-core/src/main.rs:699:            "--flux-forcer" => { o.flux_forcer = Some(suivant(i).clone()); 2 }
drave-core/src/main.rs:700:            "--flux-serveur" => { o.flux_serveur = Some(suivant(i).clone()); 2 }
drave-core/src/main.rs:770:            "--flux" => { o.flux = true; 1 }
drave-core/src/main.rs:771:            "--flux-liste" => { o.flux_liste = true; 1 }
drave-core/src/main.rs:772:            "--flux-blocs" => { o.flux_blocs = true; 1 }
drave-core/src/main.rs:923:    // Le REJEU aussi : `--flux-forcer` était ignoré en inférence, sans un mot.
drave-core/src/main.rs:2465:/// des chemins FLUX. Ils étaient ignorés dans `--flux-serveur` et
drave-core/src/main.rs:2802:fn envoyer_flux(s: &mut std::net::TcpStream, debut: u32, fin: u32, pos: u32,
drave-core/src/main.rs:2883:fn envoyer_lot(s: &mut std::net::TcpSt
… [2240 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Transport réseau TCP confirmé ; lecture du serveur flux et des relais dans main.rs

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '2440,2560p' drave-core/src/main.rs", "description": "Read main.rs flux serveur region 1"}`

  ```
for (i, (n, o)) in par_fichier.iter().zip(&octets).enumerate() {
            println!("  fichier {i} : {n:5} tenseurs · {:.2} Go", *o as f64 / 1e9);
        }
    }
    // Les métadonnées d'architecture, celles qu'on relit à chaque fois.
    for k in ["block_count", "embedding_length", "feed_forward_length", "attention.head_count",
              "attention.head_count_kv", "expert_count", "expert_used_count",
              "context_length", "vocab_size"] {
        if let Some(v) = g.cfg(k) {
            let s = v.as_u64().map(|x| x.to_string())
                .or_else(|| v.as_f64().map(|x| format!("{x}")))
                .or_else(|| v.as_str().map(str::to_string))
                .unwrap_or_else(|| format!("{v:?}"));
            print!(" · {k} {s}");
        }
    }
    println!();
    for t in &g.tensors {
        let poids: u64 = t.dims.iter().product();
        println!("  {:8} {:38} {:?} · {:.1} M poids · fichier {}",
                 Gguf::nom_type(t.ttype), t.name, t.dims, poids as f64 / 1e6, t.fichier);
    }
}

/// Applique les réglages de quantification de la ligne de commande à un modèle
/// des chemins FLUX. Ils étaient ignorés dans `--flux-serveur` et
/// `--ppl-repart
… [5373 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"RELAIS\\|relais\" drave-core/src/*.rs | head -60", "description": "Grep relais in sources"}`

  ```
drave-core/src/kimi_k3.rs:1633:                                           "relais : en-tête absente ou magie fausse"));
drave-core/src/kimi_k3.rs:1663:/// **Une PLAGE de couches** — `debut..fin` — avec reprise possible sur un relais.
drave-core/src/kimi_k3.rs:1665:/// Rend le résultat ET le relais à transmettre. `passe_complete` est cette même
drave-core/src/kimi_k3.rs:1678:    // il reçoit le flux et la pile. Sans relais, il part de la plongée, comme
drave-core/src/kimi_k3.rs:1683:                return Err(format!("relais incompatible : {} jetons × {:?} canaux, attendu {ntok} × {h}", r.flux.len(), r.flux.first().map(|v| v.len())));
drave-core/src/kimi_k3.rs:1686:                return Err(format!("relais pris à la couche {} mais la plage commence à {debut} — le trou serait silencieux", r.debut));
drave-core/src/kimi_k3.rs:1852:        let relais = Relais { debut: fin, flux: flux.clone(), pile: pile.clone() };
drave-core/src/kimi_k3.rs:1853:        return Ok((lgs, relais));
drave-core/src/kimi_k3.rs:1855:    let relais = Relais { debut: fin, flux: flux.clone(), pile };
drave-core/src/kimi_k3.rs:1856:    Ok((flux, relais))
drave-core/src/kimi_k3.rs:1860:/// `passe_plage`, sans rela
… [1880 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture du relais K3 (transport par fichier) et du serveur flux TCP

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1595,1700p' drave-core/src/kimi_k3.rs", "description": "Read Relais definition in kimi_k3.rs"}`

  ```
///   faux **sans erreur** — le même écueil que la `pre` reçue de V4.1.
///
/// Pour quatre jetons et 7168 canaux, cela fait **142 ko**. Ce n'est pas un
/// protocole de réseau, c'est un fichier.
#[derive(Clone)]
pub struct Relais {
    /// Première couche NON calculée : le suivant commence ici.
    pub debut: usize,
    pub flux: Vec<Vec<f32>>,
    pub pile: Vec<Vec<Vec<f32>>>,
}

impl Relais {
    pub fn ecrire(&self, chemin: &str) -> std::io::Result<()> {
        use std::io::Write;
        let mut o = std::io::BufWriter::new(std::fs::File::create(chemin)?);
        let (ntok, h) = (self.flux.len(), self.flux.first().map(|v| v.len()).unwrap_or(0));
        o.write_all(b"K3RL")?;
        o.write_all(&1u32.to_le_bytes())?;
        o.write_all(&(self.debut as u64).to_le_bytes())?;
        o.write_all(&(ntok as u32).to_le_bytes())?;
        o.write_all(&(h as u32).to_le_bytes())?;
        for v in &self.flux {
            for &x in v { o.write_all(&x.to_le_bytes())?; }
        }
        o.write_all(&(self.pile.len() as u32).to_le_bytes())?;
        for ck in &self.pile {
            for v in ck {
                for &x in v { o.write_all(&x.to_le_bytes())?; }
            }
        }
… [3297 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '2100,2175p' drave-core/src/main.rs", "description": "Read K3 plage/relais invocation"}`

  ```
// qui était juste — le tableau d'attente était faux, pas
                        // le moteur.
                        let attendu = [1103u32, 3140, 0][pas.min(2)];
                        println!("  pas {pas} : {} jeton(s) en entrée ({} s) → argmax {imax}{}",
                                 suite.len(), t0.elapsed().as_secs(),
                                 if attendu != 0 {
                                     if imax as u32 == attendu { " ✅ (référence)".to_string() }
                                     else { format!(" ❌ (référence : {attendu})") }
                                 } else { String::new() });
                        if pas == gen { break; }
                        // `DRAVE_K3_IMPOSE=1309,3140` force la suite du texte
                        // au lieu de laisser le moteur choisir : c'est ce qui
                        // permet de vérifier un pas d'APRÈS que la référence ait
                        // publié ses logits, et de tester la PERSISTANCE de
                        // l'état entre deux appels (le 2e appel ne voit qu'un
                        // jeton nouveau, l'état vient du 1er).
                        let impose: Vec<u32> = std::env::var("DRAVE
… [3761 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture du serveur flux TCP, du mode lot et des tests Rust

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '3160,3340p' drave-core/src/main.rs", "description": "Read run_serveur_flux"}`

  ```
format!("mode de flux inconnu : {autre}"))),
    };
    Ok(Flux { n, debut, fin, pos, mode, act, premix, octets_corps: octets_prefixe + octets.len(), charge })
}

/// Le NŒUD MOTEUR : charge le modèle, écoute, applique SA plage de couches au
/// flux reçu et renvoie le flux résultant. Un seul client à la fois — c'est un
/// banc d'essai, pas un service.
fn run_serveur_flux(opt: Options, adresse: &str) {
    if opt.tete_partielle {
        eprintln!("[plage] `--tete-partielle` est sans effet sur un SERVEUR de flux : ce \
nœud rend un flux résiduel BRUT par contrat (la tête appartient au nœud qui la possède)");
    }
    // `port` reste localhost ; `hôte:port` écoute sur l'interface nommée
    // (« 0.0.0.0:5599 » pour un pair distant). Le pair distant est le cas de la
    // phase 3.4 : un nœud Colab, ou une autre machine du réseau.
    let (hote, port) = match adresse.rsplit_once(':') {
        Some((h, p)) => (h.to_string(), p.parse().expect("port invalide")),
        None => ("127.0.0.1".to_string(), adresse.parse().expect("port invalide")),
    };
    let chemin = modele_chemin();
    // Le contexte du nœud moteur suit `--ctx` : figé à 4096, il faisait payer au
    // pair des t
… [9522 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '5500,5903p' drave-core/src/main.rs", "description": "Read Rust tests for flux"}`

  ```
assert_eq!(niveaux_activation(16), 32767.0);
        // au-delà de 16 bits, on borne (et `poser_niveaux` le DIT)
        assert_eq!(niveaux_activation(24), 32767.0);
        assert_eq!(niveaux_activation(32), 32767.0);
        // et jamais zéro ni négatif : `1 << (abits-1)` avec abits = 0 paniquait
        assert_eq!(niveaux_activation(0), 0.0);
        assert_eq!(niveaux_activation(1), 0.0);
    }
}

#[cfg(test)]
mod tests_flux {
    //! Les tests du PROTOCOLE et du CODEC. Ils manquaient : les deux bugs les
    //! plus coûteux de la session (un en-tête d'un octet trop long, un
    //! échappement d'indice écrit sur quatre octets et lu sur deux) étaient
    //! invisibles pour les six tests existants, qui ne couvraient que le cache KV.
    use super::*;
    use std::net::{TcpListener, TcpStream};

    #[test]
    fn entete_et_version_sont_ce_que_les_numeros_disent() {
        assert_eq!(TAILLE_TETE, 79, "l'en-tête de flux doit faire 79 octets");
        // La version suit l'en-tête : 4 quand les top-k sont entrés dans le
        // contrat, 5 quand le mode 4 (lot en listes) est apparu, 6 quand le
        // pré-mix porté de V4.1 a été ajouté en tête de corps. Ce test a
        // 
… [18479 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des portes (portes.sh, porte-flux.sh, portes_formats.sh) et du pair factice

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat tools/portes.sh", "description": "Read portes.sh"}`

  ```
#!/bin/bash
# Les portes du dépôt, en une commande.
#
# Un chiffre de référence qui dérive sans qu'on s'en aperçoive ne vaut rien :
# chaque porte est comparée à la valeur ATTENDUE, et le script sort en erreur si
# l'une diverge. Les valeurs sont celles publiées dans les rapports.
#
#   tools/portes.sh            toutes les portes
#   tools/portes.sh rapide     sans gpt-oss (le seul qui prenne ~20 min)

set -u
cd "$(dirname "$0")/.."
D=./drave-core/target/release/drave
RAPIDE=${1:-}
ECHEC=0

[ -x "$D" ] || { echo "compiler d'abord : (cd drave-core && cargo build --release)"; exit 2; }

compare() {  # nom, attendu, obtenu
    if [ "$2" = "$3" ]; then
        printf "  %-42s %s  ✅\n" "$1" "$3"
    else
        printf "  %-42s %s  ❌ (attendu %s)\n" "$1" "${3:-—}" "$2"
        ECHEC=1
    fi
}

# Attention : le moteur affiche AUSSI une perplexité cumulée par fenêtre, avant
# le total. Prendre la première occurrence du motif donnait 17,431 (fenêtre 1) au
# lieu de 19,3885 (total) — un instrument faux qui accuse le code.
valeur() { grep -oE "=== perplexité [0-9]+\.[0-9]+" | grep -oE "[0-9]+\.[0-9]+" | head -1; }

echo "=== Portes ==="

# 1. Tests unitaires. Le seuil (48) protège le NOMBR
… [17244 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat tools/porte-flux.sh; echo \"=====FORMATS=====\"; cat tools/portes_formats.sh", "description": "Read porte-flux and portes_formats"}`

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
#   tools/porte-flux.sh            la porte
#   MODELE=... tools/porte-flux.sh autre modèle (dense, sans hyper-connexions)

set -u
cd "$(dirname "$0"
… [9634 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lancement de 4 sous-agents d'extraction (réseau, GPU, clusters, mémoire/disque) pendant que je lis le relais K3

- **subagent** `{"description": "Extract network split facts", "prompt": "Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (moteur d'inférence Rust « Drave », drave-core/). LECTURE SEULE STRICTE : ne modifie aucun fichier, ne compile pas, ne lance aucun test ni binaire.\n\nObjectif : extr … [1322 caractères tronqués]`
- **subagent** `{"description": "Extract GPU dispatch facts", "prompt": "Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (moteur d'inférence Rust « Drave », drave-core/). LECTURE SEULE STRICTE : ne modifie aucun fichier, ne compile pas, ne lance aucun test ni binaire.\n\nObjectif : inven … [1761 caractères tronqués]`
- **subagent** `{"description": "Extract cluster split facts", "prompt": "Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (moteur d'inférence Rust « Drave », drave-core/). LECTURE SEULE STRICTE : ne modifie aucun fichier, ne compile pas, ne lance aucun test ni binaire.\n\nObjectif : inve … [1481 caractères tronqués]`
- **subagent** `{"description": "Extract memory/disk/threads facts", "prompt": "Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (moteur d'inférence Rust « Drave », drave-core/). LECTURE SEULE STRICTE : ne modifie aucun fichier, ne compile pas, ne lance aucun test ni binaire.\n\nObjectif  … [1887 caractères tronqués]`

  ```
started subagent 04ed1834-b0f8-42a1-aa21-75a75c19647e
  ```


  ```
started subagent 1966e052-ebc6-4f4b-b7f9-6d1c6cb4b445
  ```


  ```
started subagent d04ed7a2-0988-4dfd-83c5-644695dc2f8f
  ```


  ```
started subagent a4eaa4c8-11e2-4ca3-bcb1-b28919cb601a
  ```

### 🤖 Assistant

⏵ Pendant ce temps : lecture du test de plage K3, du pair factice et du pilote

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat tools/test-plage-k3.sh; echo \"=====PAIR FACTICE=====\"; cat tools/pair_factice.py", "description": "Read test-plage-k3 and pair_factice"}`

  ```
#!/bin/bash
# CHANTIER 3 — LA PORTE DE CORRECTION DU DÉCOUPAGE.
#
# Deux nœuds doivent donner EXACTEMENT ce que donne la passe monolithe. On
# coupe à la couche 13, donc on TRAVERSE la banque de la couche 12 : c'est le
# point où un découpage naïf se trompe, parce que le nœud 2 a besoin de l'entrée
# BRUTE empilée à la couche 12, pas seulement du flux.
#
#   A : couches 0..12   -> relais (flux + pile)
#   B : couches 13..25  <- relais A
#   C : couches 0..25   (monolithe)
#
# B et C doivent être IDENTIQUES AU BIT. Toute différence est un défaut du
# découpage, et le bit-à-bit ne laisse rien passer.
set -u
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet
D=./drave-core/target/release/drave
K=/home/stephane/Data13TB/stephane/modeles/gguf/Kimi-K3-UD-Q4_K_XL/Kimi-K3-UD-Q4_K_XL-00001-of-00032.gguf
J=/tmp/test_plage.log
R=/tmp/plage_relais.bin
rm -f /tmp/pl_A-* /tmp/pl_B-* /tmp/pl_C-* "$R"
: > "$J"

echo "##### A : couches 0..12" | tee -a "$J"
DRAVE_K3_PASSE=93 DRAVE_DUMP_COUCHES=/tmp/pl_A DRAVE_K3_RELAIS_SORTIE="$R" \
    $D "$K" --k3-essai --couches 0:13 2>&1 | grep -E "plage|relais|passe " | tee -a "$J"

echo "" | tee -a "$J"
echo "##### B : couches 13..25, à partir du relais A" | t
… [8652 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '3340,3520p' drave-core/src/main.rs", "description": "Read run_ppl_reparti pilote"}`

  ```
fn run_ppl_reparti(opt: Options, pair: &str) {
    use std::time::Instant;
    let chemin = modele_chemin();
    let ctx = if opt.ctx_impose { opt.ctx } else { 256 };
    let limite = opt.limit.max(1).min(ctx);
    let couches_locales = if opt.couches_locales > 0 { opt.couches_locales } else { 12 };
    // `--lot T` : préremplissage par LOTS sur le fil. La référence locale est
    // alors calculée avec le MÊME découpage — sinon l'écart mesurerait la
    // différence entre deux ordres de sommation, pas celle du découpage.
    let lot = opt.lot.max(1);
    let mut mdl = model::Model::load(&chemin,
                                     ctx, fils(&opt), true, opt.keep, false, 0, 0);
    appliquer_quantification(&mut mdl, &opt);
    // Le `hc` du PILOTE : c'est SON modèle qui décide de la largeur du pré-mix
    // qu'il envoie et de celle de celui qu'il reçoit (le pair valide le sien).
    let hc_pilote = mdl.hc.as_ref().map(|v| v[0].0.hc).unwrap_or(1);
    // `--tete-partielle` n'a pas d'objet ici : la « plage » de ce mode est le
    // découpage entre les DEUX nœuds, et le modèle local est le modèle entier.
    // Le taire serait exactement le défaut que `--options-actives` combat.
 
… [8532 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des statistiques de transport du pilote (débits mesurés)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '3520,3660p' drave-core/src/main.rs", "description": "Read transport stats printout"}`

  ```
// La norme finale reste au nœud qui a la tête, et la tête se fait par
            // lots : le lot reçu ne redescend pas jeton par jeton.
            let mut hn: Vec<Vec<f32>> = Vec::with_capacity(t);
            for i in 0..t {
                hn.push(mdl.norme_finale(&etats[i * mdl.cfg.hidden..(i + 1) * mdl.cfg.hidden],
                                         pos + i));
            }
            let lgs = mdl.logits_lot(&hn);
            for i in 0..t {
                if pos + i + 1 < ids.len() {
                    nll += nll_logits(&lgs[i], ids[pos + i + 1]);
                }
            }
            pos += t;
        }
    } else {
    for (pos, &t) in ids.iter().enumerate() {
        let dernier = pos + 1 == ids.len();
        // Le DERNIER jeton n'a rien à prédire : lui demander un aller-retour
        // distant, c'est payer un calcul complet — des deux côtés — pour un état
        // que personne ne lit. On sort donc ici, AVANT le calcul local aussi.
        // La référence locale, elle, calcule encore ce dernier jeton pour rien
        // (1 sur N : négligeable, mais écrit ici pour que personne ne s'étonne
        // d'un écart de temps entre les deux chemins).
     
… [7000 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"débit\\|Mio/s\\|Mo/s\\|octets/flux\\|octets par flux\\|latence\" --include=*.rs drave-core/src/ | head -30", "description": "Grep throughput reporting in code"}`

  ```
drave-core/src/materiel.rs:296:        // leurs hyperthreads (+27 %, la latence mémoire est masquée et le L2
drave-core/src/materiel.rs:311:rendent +27 % (14,7 -> 18,7 Go/s) en masquant la latence mémoire",
drave-core/src/materiel.rs:318:        // --- lecteurs disque : le parallélisme multiplie le débit.
drave-core/src/materiel.rs:375:    /// Ce que coûtera un jeton, d'après les débits **mesurés** sur cette machine.
drave-core/src/materiel.rs:378:    /// divisée par les débits, pour voir où passe le temps et ce qu'un
drave-core/src/materiel.rs:379:    /// déplacement changerait. Les débits viennent du banc (`--gpu-banc`) et des
drave-core/src/gguf.rs:79:/// débit séquentiel du NVMe, et 4,5× mieux qu'une lecture complète (30,5 s).
drave-core/src/gguf.rs:80:/// Cette demande vise le débit parallèle, 31 Go/s.
drave-core/src/list.rs:659:    /// le jour où le débit comptera plus que l'exactitude.
drave-core/src/engine.rs:99:    // barrière d'aliasing avec `acc` et coûtait ×3 sur le débit.
drave-core/src/engine.rs:342:    // Mesuré : lier les seize fils au seul nœud 0 coûte 16 % de débit
drave-core/src/engine.rs:389:    /// sursouscrite effondre le débit (cf. commentaire dans la boucle 
… [1877 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de REPRISE.md sur les chantiers distribution et réseau

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"chantier 3\\|Chantier 3\\|CHANTIER 3\\|phase 3\\|Phase 3\\|réseau\\|reseau\\|relais\\|plage\" REPRISE.md | head -60", "description": "Grep REPRISE for distribution sections"}`

  ```
687:| Exécution bornée | `--couches a:b` : exécute une plage de couches pour comparer à la référence avant que le reste du modèle existe. Le manque retiré est **annoncé**, jamais silencieux |
908:   toutes par-dessus (`forward_lot` et `forward_mla`, eux, respectaient la plage) ;
910:   plage allait jusqu'à la dernière couche, puis le pilote normait). La règle est
920:`colab/` (notebook + `tools/preparer_colab.sh`) porte la recette de la phase 3.4.
932:local, à logits identiques. Et avec un relais retardateur
936:Le seuil de rentabilité (phase 3.3) est donc une affaire de latence, pas de débit :
954:aussi. C'était le bloqueur de la phase 3.4 ; `colab/` contient maintenant le
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,120p' REPRISE.md", "description": "Read REPRISE head"}`

  ```
# Reprise — état du projet et mode d'emploi pour une nouvelle session

> Rédigé à la fin d'une session longue. Tout ce qui suit est **mesuré**, pas
> déduit. Les valeurs de perplexité sont des **références de non-régression** :
> si une modification les change, c'est qu'elle a changé le calcul.
>
> **Nom** : le projet s'appelle **Drave** (binaire `drave`, paquet `drave-core`,
> variables `DRAVE_*`, histoire du renommage dans `docs/histoire.md`). Le dossier
> de travail, lui, s'appelle encore `Qtrinet` — les chemins ci-dessous sont ceux
> qui existent.

---

## 1. En une phrase

`drave-core` est un moteur d'inférence Rust (~13 758 lignes, `std` seul) qui
charge les GGUF **en place** (aucune copie, aucune requantification), exécute les
projections soit en listes d'événements, soit en produit scalaire dense, gère les
MoE, tient une conversation, et déporte au GPU ce qui y gagne. Il fait tourner du
0,5 B au 120 B sur le CPU de cette machine.

```bash
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core && cargo build --release
./target/release/drave ../models/Qwen2.5-0.5B-Q8_0.gguf \
    --infer --chat --flux --prompt "Explique le ciel bleu en une phrase." \
    --n 64 --ctx 5
… [5338 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de la section « phase 3 / réseau » de REPRISE

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '860,1000p' REPRISE.md", "description": "Read REPRISE phase 3 distribution section"}`

  ```
étendre la grille à 8 192 et 16 384, plusieurs codes par sonde, et croiser avec
   `--attn-topk`.

### Les variables d'environnement, et leurs pièges

| variable | ce qu'elle fait | le piège |
|---|---|---|
| `DRAVE_GPU=1` | ouvre le pilote CUDA (`gpu::instance`) | **c'est elle qui commande tout** ; sans elle, les autres ne font RIEN et rien ne le dit |
| `DRAVE_GPU_TETE=1` | déporte la tête (Q8_0 ou Q6_K) | inutile sans `DRAVE_GPU` |
| `DRAVE_GPU_KV=1` | tient le cache KV en VRAM et y calcule l'attention | inutile sans `DRAVE_GPU` ; au-dessous de ~4 000 clés le CPU gagne (lancements + recopies) |
| `DRAVE_GPU_TOPK=1` | calcule le top-k de l'attention (`--attn-topk`) en VRAM : scores, seuil radix, collecte des k indices, softmax + Σ w·V | inutile sans `DRAVE_GPU` **et** `DRAVE_GPU_KV` ; exige `nkv × rep = nh` et `k ≤ 1 024` ; tout refus d'un noyau retombe sur le CPU. Perplexité identique à 5e-4 près (9,4162 contre 9,4167 à ctx 2 048), mais **pas encore de gain de temps à 2 048 clés** : six lancements et cinq recopies par couche et par jeton (la fusion des quatre passes est à faire) |
| `DRAVE_GPU_EXPERTS=1` | cache LRU des experts MXFP4 en VRAM | inutile sans `DRAVE_GPU` ; budget p
… [9280 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification de la couverture des portes et du mode réseau côté Kimi-K3

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && echo \"--- appelants test-plage-k3 ---\"; grep -rn \"test-plage-k3\" --include=* . 2>/dev/null | grep -v \"^./journal/\" | grep -v Binary | head; echo \"--- proxy_latence ---\"; sed -n '1,45p' tools/proxy_latence.py; echo \"--- colab … [87 caractères tronqués]`

  ```
--- appelants test-plage-k3 ---
./reports/rapport-passe-k3-disque.md:440:`tools/test-plage-k3.sh` coupe à la **couche 13** — donc **après** la banque de la
--- proxy_latence ---
#!/usr/bin/env python3
"""Relais TCP qui ajoute une latence par message, pour mesurer ce qu'un lien
distant coûte à un découpage de modèle.

Pourquoi : sur localhost, l'attente du pair vaut 1,01× le calcul local — c'est un
plancher optimiste. Une VM Colab est à quelques dizaines de millisecondes, et la
phase 3.3 demande « à partir de quel débit le découpage gagne ». Le débit n'est
jamais le problème (0,25 Mbit/s) ; la latence, si. Ce relais la rend réglable.

    python3 tools/proxy_latence.py <port_écoute> <hôte_cible:port> [délai_ms]
"""
import socket, sys, threading, time


def relais(src, dst, delai):
    try:
        while True:
            donnees = src.recv(65536)
            if not donnees:
                break
            if delai:
                time.sleep(delai)
            dst.sendall(donnees)
    except OSError:
        pass
    finally:
        for s in (src, dst):
            try:
                s.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass


def main():
   
… [519 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"couches-locales\\|--couches\\b\\|\\\"--couches\\\"\\|couches:\" --include=*.rs drave-core/src/main.rs | head -20; echo \"--- K3 mention réseau ---\"; grep -rn \"réseau\\|reseau\\|TCP\\|distribu\\|nœud\\|noeud\" drave-core/ … [90 caractères tronqués]`

  ```
424:/// fin d'une plage `--couches a:b`. Par défaut une plage partielle rend le flux
576:    couches: Option<(usize, usize)>,
578:    trace_couches: Vec<usize>,
616:    /// **Sonde de plage** : avec `--couches a:b`, appliquer AUSSI la tête de
705:            "--couches-locales" => { o.couches_locales = suivant(i).parse().unwrap(); 2 }
706:            "--couches" => {
709:                    panic!("--couches attend `a:b` (reçu « {v} »)"));
2125:                // `--couches a:b` borne la plage. Le relais transporte ce que le
3361:y est le découpage entre nœuds (voir `--couches-locales`), pas un `--couches a:b`");
--- K3 mention réseau ---
1585:/// **Ce qu'un nœud doit transmettre au suivant** pour que la passe reprenne
1593:///   Un nœud qui démarre à la couche 47 a besoin des banques 0 à 36 : sans
1598:/// protocole de réseau, c'est un fichier.
1677:    // REPRISE. Un nœud qui démarre à la couche `debut` ne relit pas la plongée :
  ```

### 🤖 Assistant

⏵ Recherche des rapports plage K3 et transport pour les chiffres publiés

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls reports/ | grep -iE \"plage|transport|phase3|reparti|k3|noeud|nœud|gpu|cluster|disque|materiel\"; echo \"--- git show 3c2b542 stat ---\"; git show --stat 3c2b542 | head -25; echo \"--- git show 7d32b4f ---\"; git show 7d32b4f | he … [67 caractères tronqués]`

  ```
bilan-multi-materiel.md
rapport-budget-kimi-k3.md
rapport-gpu-scores.md
rapport-gpu-tandem-nvlink.md
rapport-gpu-topk-selection.md
rapport-logits-gpu-vs-cpu.md
rapport-materiel-disque-ou-cpu.md
rapport-passe-k3-disque.md
rapport-phase3-reparti.md
rapport-prefill-reparti.md
rapport-transport-liste.md
rapport-v4-reparti.md
--- git show 3c2b542 stat ---
commit 3c2b542b620d7f3b4c2467589c8c7bf702c80489
Author: Stéphane <stephane@localhost>
Date:   Wed Oct 7 20:29:10 2026 -0400

    Chantier 3 : un nœud = une plage de couches, et la porte est TENUE au bit près
    
    passe_complete calculait toujours 0..n. Il fallait deux choses pour qu'un
    processus devienne un NŒUD :
    
    1. une plage debut..fin — faite, par --couches a:b, qui veut déjà dire « plage de
       couches » partout ailleurs dans ce moteur ;
    2. un relais entre nœuds — et ce n'est PAS seulement le flux résiduel.
    
    Le point dur : le modèle empile une BANQUE toutes les 12 couches, et res_mix
    mélange ce plateau à chaque couche suivante. Un nœud qui démarre à la couche 13 a
    donc besoin des entrées BRUTES des couches 0 ET 12. Sans elles, res_mix
    mélangerait un plateau incomplet et le résultat serait
… [3411 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de docs/roadmap.md (phases 0–3) et du plan de préremplissage réparti

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"Phase\\|phase\\|Reste\\|reste à\\|MANQUE\\|manque\" docs/roadmap.md | head -50; echo \"=== TAILLE ===\"; wc -l docs/roadmap.md docs/plan-prefill-reparti.md docs/colab-reparti.md docs/format-flux.md", "description": "Grep ro … [14 caractères tronqués]`

  ```
3:> Suite de [`docs/vision.md`](vision.md). Six phases, de ce qui se fait **tout de
5:> phase a un critère de succès **mesurable**, et l'état de chaque chantier est
8:## Phase 0 — La drave observable (aucune infra)
17:| 0.3 | **Le format EST le contrat d'échange** (phase 3) : versionné, en-tête + paires | ✅ | codec de référence (`tools/flux_codec.py`) : aller-retour **identique** sur 132 Mo ; **et le rejeu dans le moteur redonne les mêmes logits** (`--flux-forcer`) |
20:## Phase 1 — La drave mesurée (aucune infra)
32:## Phase 2 — La drave répartie localement (aucune infra)
44:## Phase 3 — La drave distribuée (Colab, hors infra locale)
50:entre les deux **le format de la phase 0** — c'est précisément pour cela qu'il est
55:| 3.1 | **Contrat d'échange** (protocole v5) : tranche de liste = en-tête (couche, source, échelle, bits) + paires (destination, valeur) | ✅ | format écrit, relu, rejoué sans perte (phase 0.3/0.3bis) ; **transport TCP en place et FIDÈLE** (`--flux-serveur`, `--ppl-reparti`) — écart local/réparti **0,00e0** sur 40 et 200 jetons (39 et 199 flux : le dernier n'a rien à prédire), après correction de deux défauts (plage de couches ignorée par `forward`, norme finale ap
… [1187 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '32,60p' docs/roadmap.md; echo \"=== 223+ ===\"; sed -n '223,311p' docs/roadmap.md", "description": "Read roadmap phases 2-3 and status"}`

  ```
## Phase 2 — La drave répartie localement (aucune infra)

**Objectif** : la machine entière comme un seul flux — deux GPU, 40 cœurs, et le
disque quand la mémoire ne suffit plus.

| # | chantier | état | critère de succès |
|---|---|---|---|
| 2.1 | **Ordonnanceur de flux** : placer chaque opérateur là où son flux coûte le moins cher (2 GPU, CPU, VRAM, RAM, NVMe) | ⏳ | prefill à 8 k mesuré, placement décidé par la règle |
| 2.2 | **Streaming des poids depuis le NVMe** (3,5 Go/s) pour ce qui ne tient pas en RAM — c'est la même idée : ne lire que ce qui parle | ⏳ | un modèle > RAM exécuté, débit mesuré |
| 2.3 | **Cache d'experts rentable** : +6 % aujourd'hui ; grouper les trois projections par expert et supprimer les copies | ⏳ | ≥ +30 %, sinon abandonné (et écrit) |
| 2.4 | **KV sur deux cartes, politique de page** (le KV est paginé, la politique ne l'est pas) | ⏳ | 1 M de jetons tenus avec une politique d'éviction mesurée |

## Phase 3 — La drave distribuée (Colab, hors infra locale)

**Objectif** : deux machines qui se passent des listes, pas des matrices.

Le prototype se fera **avec Colab** : un *nœud moteur* (un bloc de couches) sur le
runtime Colab, un *nœud pilote* (embeddin
… [7259 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1,80p' docs/colab-reparti.md", "description": "Read colab-reparti doc"}`

  ```
# Répétition Colab — la phase 3.4, pas à pas

Objectif : deux machines qui se passent des **listes d'activation**, l'une sur le
runtime Colab, l'autre en local, et **les mêmes logits** qu'en local.

Ce flux est aussi le **journal** qu'on relit (`--trace-flux`, puis
`tools/analyse_flux.py`, `profil_flux.py`, `diff_flux.py`) pour comprendre où
travaille le modèle et adapter l'architecture à la tâche — la fidélité du
transport n'est pas le seul enjeu (`docs/vision.md` §2).

Ce document est la recette ; l'état du protocole et les chiffres qui la
dimensionnent sont dans `docs/format-flux.md` et
`reports/rapport-transport-liste.md`.

## Mise en place, concrètement

`tools/preparer_colab.sh` produit le dépôt en **un fichier** (`drave.bundle`, 4,5 Mo
avec tout l'historique) et affiche l'empreinte SHA-256 du modèle — les deux nœuds
doivent charger le même GGUF, la dimension ne voyage pas. `colab/README.md` donne
la marche à suivre (tunnel, téléversements) et `colab/Drave-reparti.ipynb` est le
notebook prêt à ouvrir, avec la vérification d'empreinte et la lecture du résultat.

## Ce qui est déjà vérifié, et ce qui ne l'est pas

| point | état |
|---|---|
| fidélité du découpage | ✅ écart **0
… [3253 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture du planificateur de placement (--plan) : répartition sur les unités d'une machine

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '4740,4870p' drave-core/src/main.rs", "description": "Read placement planner"}`

  ```
// calculée sur ce flux ne mesurerait plus le texte.
        let retour = tk.decode(&ids);
        if retour == texte {
            println!("réversibilité : texte reconstruit identique ✅ ({} octets)", texte.len());
        } else {
            let pos = retour.bytes().zip(texte.bytes()).position(|(a, b)| a != b)
                .unwrap_or(retour.len().min(texte.len()));
            println!("réversibilité : DIVERGE à l'octet {pos} — {} vs {} octets",
                     retour.len(), texte.len());
            println!("  source  : {:?}", &texte[pos.saturating_sub(40)..(pos + 40).min(texte.len())]);
            println!("  retour  : {:?}", &retour[pos.saturating_sub(40)..(pos + 40).min(retour.len())]);
        }
        return;
    }
    let ids = tk.encode(&texte);
    println!("{} tokens", ids.len());
    for id in &ids {
        print!("{id} ");
    }
    println!();
    println!("recolle : {:?}", tk.decode(&ids));
}

/// Plan de placement : ce que pèse chaque couche, et où la mettre.
///
/// C'est l'« index » du conteneur : on le lit **avant** les poids, donc on
/// décide sans avoir rien chargé. Les seuils viennent des débits mesurés sur
/// cette machine : CPU 14–25 Go/s, PC
… [5666 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '2380,2440p' drave-core/src/main.rs; echo \"=== materiel 360-440 ===\"; sed -n '360,440p' drave-core/src/materiel.rs", "description": "Read plan output and materiel cost model"}`

  ```
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
    println!("  lecteurs disque  : {}", plan.lecteurs);
    println!("  cache experts    : {:.1} Go en VRAM", plan.cache_experts_go);
    println!("  cache KV         : {} bits", plan.kv_bits);
    println!();
    for r in &plan.raisons { println!("  · {r}"); }
    println!();

… [5466 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Comptage des tests Rust liés au transport/découpage

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"#\\[test\\]\" drave-core/src/*.rs | wc -l; echo \"--- modules de test ---\"; grep -rn \"^mod tests\\|^mod tests_\" drave-core/src/*.rs; echo \"--- noms de tests ---\"; grep -rn \"fn [a-z_]*(\" drave-core/src/main.rs | sed  … [143 caractères tronqués]`

  ```
77
--- modules de test ---
drave-core/src/clusters.rs:300:mod tests {
drave-core/src/engine.rs:943:mod tests_gemm {
drave-core/src/engine.rs:990:mod tests_gemm_q4 {
drave-core/src/engram.rs:292:mod tests {
drave-core/src/formats.rs:2883:mod tests {
drave-core/src/list.rs:1397:mod tests_q4 {
drave-core/src/list.rs:1426:mod tests_mxfp4 {
drave-core/src/list.rs:1497:mod tests_q6k {
drave-core/src/list.rs:1537:mod tests_grille {
drave-core/src/main.rs:5490:mod tests_niveaux {
drave-core/src/main.rs:5511:mod tests_flux {
drave-core/src/main.rs:5583:mod tests_plafond {
drave-core/src/main.rs:5846:mod tests_vars {
drave-core/src/materiel.rs:439:mod tests {
drave-core/src/model.rs:8458:mod tests_kv {
drave-core/src/model.rs:8510:mod tests_noeud_partiel {
drave-core/src/model.rs:8615:mod tests_hc {
drave-core/src/model.rs:8915:mod tests_router {
drave-core/src/model.rs:9037:mod tests_kimi_k3 {
drave-core/src/tokenizer.rs:585:mod tests_kimi {
--- noms de tests ---
53:fn fmt_bits(b: u64, n: usize) -> String {
66:fn rapport_hebb_diff(mdl: &model::Model) {
76:fn main() {
421:fn modele_chemin() -> String { MODELE.get().cloned().unwrap_or_default() }
429:fn poser_tete_partielle(mdl: &mut model::M
… [1241 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des tests « nœud partiel » et clusters

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '8510,8615p' drave-core/src/model.rs", "description": "Read tests_noeud_partiel"}`

  ```
mod tests_noeud_partiel {
    use super::*;
    use crate::gguf::tests::{ecrire, gguf_synth, gguf_synth_q4_0};

    #[test]
    fn traduction_par_numero_de_cluster() {
        let d = std::env::temp_dir().join("drave_noeud_partiel");
        let _ = std::fs::remove_dir_all(&d);
        std::fs::create_dir_all(&d).unwrap();
        // Quatre experts globaux, deux clusters de deux. n_in = 32 (un bloc),
        // n_ff = 32 : les formes minimales acceptées par `charger_moe`.
        let (n_in, n_ff, par_cluster, n_clusters) = (32u64, 32u64, 2u64, 2usize);
        // Le commun : le routeur, en F32, dimensionné sur les experts GLOBAUX.
        let routeur: Vec<(&str, Vec<u64>)> =
            vec![("blk.0.ffn_gate_inp.weight", vec![4, n_in])];
        std::fs::write(d.join("commun.gguf"), gguf_synth(&routeur, 0, 1.0)).unwrap();
        // Chaque cluster : ses experts LOCAUX, en Q4_0 (le type que `source_de`
        // accepte, donc le seul qui permette de construire un `Moe`).
        for c in 0..n_clusters {
            let t: Vec<(&str, Vec<u64>)> = vec![
                ("blk.0.ffn_gate_exps.weight", vec![par_cluster, n_ff, n_in]),
                ("blk.0.ffn_up_exps.weight",   vec![p
… [4092 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '300,380p' drave-core/src/clusters.rs; echo \"=== K3 tests in model.rs ===\"; sed -n '9037,9100p' drave-core/src/model.rs", "description": "Read clusters tests and k3 tests"}`

  ```
mod tests {
    use super::*;

    fn ecrire(nom: &str, contenu: &str) -> PathBuf {
        let p = std::env::temp_dir().join(nom);
        std::fs::write(&p, contenu).unwrap();
        p
    }

    #[test]
    fn mapping_lu_et_traduit() {
        let p = ecrire("drave_mapping_ok.tsv", "\
# drave-clusters-mapping v1
# n_couches 2 · n_experts 4 · clusters 2 · experts_par_cluster 2
# couche\tlocal\tglobal\tcluster
0\t0\t3\t0
0\t1\t1\t0
0\t0\t0\t1
0\t1\t2\t1
1\t0\t2\t0
1\t1\t0\t0
1\t0\t1\t1
1\t1\t3\t1
");
        let m = Mapping::lire(&p).unwrap();
        assert_eq!((m.n_couches, m.n_experts, m.n_clusters, m.par_cluster), (2, 4, 2, 2));
        assert_eq!(m.ou(0, 3), Some((0, 0)));
        assert_eq!(m.ou(0, 1), Some((0, 1)));
        assert_eq!(m.ou(0, 0), Some((1, 0)));
        assert_eq!(m.ou(0, 2), Some((1, 1)));
        assert_eq!(m.ou(1, 3), Some((1, 1)));
        assert_eq!(m.presents(0), 4);
        assert_eq!(m.ou(1, 9), None, "un expert hors bornes n'est pas une panique");
        let _ = std::fs::remove_file(&p);
    }

    /// Un expert placé deux fois est une faute du convertisseur : la refuser est
    /// le seul moyen de ne pas exécuter un modèle silencieusement amputé
… [5439 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification du branchement CLI du sous-ensemble de clusters

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"ouvrir_sous_ensemble\\|sous_ensemble\\|clusters::\\|--cluster\\|cluster\" --include=*.rs drave-core/src/main.rs | head -30; echo \"=== clusters.rs entête ===\"; sed -n '1,60p' drave-core/src/clusters.rs", "description": "C … [36 caractères tronqués]`

  ```
36:mod clusters;
79:        eprintln!("usage: drave <modele.gguf|dossier-de-clusters> [--matrix NOM] [--threads N]");
92:        eprintln!("        ne charge que certains clusters ; DRAVE_MMAP=0 lit au lieu de mapper)");
2359:            // Un modèle en clusters préfixe ses tenseurs (`cl0/blk.0.…`) : on
2368:                // fichier de cluster il n'y en a qu'une fraction (16 sur 128),
=== clusters.rs entête ===
//! Format **clusters** : un fichier commun, N fichiers d'experts, un mapping.
//!
//! Le problème que ce format résout : un MoE range ses 128 experts dans trois
//! tenseurs 3D par couche, et un nœud qui n'en sert que 16 en lit quand même
//! 128 — soit 8 fois trop. Découpé, le nœud ne lit que son huitième.
//!
//! Trois pièces, et rien d'autre :
//!
//! * `commun.gguf` — tout ce qui n'est pas un expert : embeddings, attention,
//!   normes, ET le routeur (`ffn_gate_inp`), qui doit rester global puisque
//!   c'est lui qui désigne l'expert ;
//! * `cluster-XX.gguf` — les seuls `ffn_{gate,up,down}_exps` d'un sous-ensemble
//!   d'experts, aux mêmes décalages internes que dans le fichier d'origine ;
//! * `mapping.tsv` — pour chaque couche, où est chaque expert global.
//!

… [2112 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '76,100p' drave-core/src/main.rs; echo \"=== grep DRAVE_CLUSTERS / MMAP ===\"; grep -rn \"MMAP\\|CLUSTERS\" --include=*.rs drave-core/src/ | head -20", "description": "Read usage text and MMAP handling"}`

  ```
fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() < 2 {
        eprintln!("usage: drave <modele.gguf|dossier-de-clusters> [--matrix NOM] [--threads N]");
        eprintln!("       drave <modele> --infer (--ids 1,2,3 | --prompt TEXTE | --ids-file F)");
        eprintln!("             [--n 32] [--temp 0] [--ctx 512] [--threads N]");
        eprintln!("       drave <modele> --ppl FICHIER-IDS [--ctx N] [--limit N] [--dense]");
        eprintln!("       drave <modele> --tensors      inventaire par les en-têtes seuls");
        eprintln!("       drave <modele> --materiel     détection matérielle et plan de");
        eprintln!("                                     configuration, AVEC la raison de chaque");
        eprintln!("                                     choix — ne charge pas le modèle");
        eprintln!("       drave <modele> --sonder-engram N   accès mmappé à une table d'engram");
        eprintln!("       drave <modele> --tete-restreinte F  génération CONTRAINTE : la tête ne");
        eprintln!("                                     calcule que les tokens de F. Change la");
        eprintln!("                                     sortie — re
… [2366 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification de l'avancement des sous-agents

- **list_agents** `{}`

  ```
04ed1834-b0f8-42a1-aa21-75a75c19647e [running] — Extract network split facts
1966e052-ebc6-4f4b-b7f9-6d1c6cb4b445 [running] — Extract GPU dispatch facts
d04ed7a2-0988-4dfd-83c5-644695dc2f8f [running] — Extract cluster split facts
a4eaa4c8-11e2-4ca3-bcb1-b28919cb601a [running] — Extract memory/disk/threads facts
  ```

### 🤖 Assistant

⏵ Vérification si le plan matériel est appliqué ou seulement affiché

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"materiel::\\|Materiel\\|plan(\" --include=*.rs drave-core/src/main.rs drave-core/src/model.rs | grep -v \"^drave-core/src/materiel.rs\" | head -25", "description": "Check where materiel plan is used"}`

  ```
drave-core/src/main.rs:148:    if opt.plan { run_plan(opt); return; }
drave-core/src/main.rs:2334:    let m = materiel::Materiel::detecter();
drave-core/src/main.rs:2391:    let plan = m.plan(ctx, taille_go, n_experts, mo_expert);
drave-core/src/main.rs:4769:fn run_plan(opt: Options) {
drave-core/src/model.rs:4073:                let libre = crate::materiel::ram_libre_go() * 1e9;
drave-core/src/model.rs:4300:                let m = crate::materiel::Materiel::detecter();
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '330,360p' drave-core/src/engine.rs; echo \"=== fils() ===\"; grep -n \"fn fils\" -A 20 drave-core/src/main.rs | head -35", "description": "Read thread affinity and fils()"}`

  ```
);
    }
    ret == 0
}

/// Processeurs du premier nœud NUMA, cœurs physiques puis frères SMT.
/// Repli : la numérotation linéaire si la topologie n'est pas reconnue.
fn cibles_locales(n: usize) -> Vec<usize> {
    // Chaque nœud liste d'abord ses cœurs physiques, puis leurs frères SMT
    // (`0-9,20-29` pour un Xeon 10 cœurs). On garde la première moitié de
    // chaque nœud : les cœurs physiques des DEUX sockets.
    //
    // Mesuré : lier les seize fils au seul nœud 0 coûte 16 % de débit
    // (23,8 -> 27,6 s sur le 30B MoE). Le gain de localité mémoire ne compense
    // pas la contention SMT — deux fils d'un même cœur se disputent les ports
    // d'émission, et nos ouvriers en attente active en souffrent doublement.
    let mut v = Vec::new();
    for noeud in 0..8 {
        let chemin = format!("/sys/devices/system/node/node{noeud}/cpulist");
        let Ok(txt) = std::fs::read_to_string(&chemin) else { break };
        let mut cpus = Vec::new();
        for morceau in txt.trim().split(',') {
            if let Some((a, b)) = morceau.split_once('-') {
                if let (Ok(a), Ok(b)) = (a.parse::<usize>(), b.parse::<usize>()) {
                    cpus.extend(a..=
… [1212 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des décisions d'exécution fondées sur la détection matérielle

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '4290,4320p' drave-core/src/model.rs; echo \"=== 4060-4085 ===\"; sed -n '4060,4085p' drave-core/src/model.rs; echo \"=== cibles_locales appelants ===\"; grep -rn \"cibles_locales\\|--pin\\|opt.pin\" --include=*.rs drave-core/ … [61 caractères tronqués]`

  ```
// Cache VRAM des experts : opt-in, et seulement sur un modèle à experts
        // au format MXFP4 (les autres formats ont leurs propres noyaux).
        let cache_experts = if std::env::var("DRAVE_GPU_EXPERTS").is_ok()
                               && crate::gpu::instance().is_some()
                               && cfg.n_expert > 0 {
            // Budget par défaut : ce que la VRAM peut donner sans étrangler le
            // reste. Mesuré : la VRAM lit à 84,9 Go/s contre 22,5 pour la RAM,
            // et un cache de 25 % de l'empreinte sert 80 % des appels.
            let defaut = {
                let m = crate::materiel::Materiel::detecter();
                let libre: f64 = m.gpus.iter().map(|g| g.vram_libre_go).sum();
                (libre - 2.0).max(1.0)      // 2 Go de réserve pour le contexte CUDA
            };
            let go: f64 = std::env::var("DRAVE_GPU_EXPERTS_GO").ok()
                .and_then(|v| v.parse().ok()).unwrap_or(defaut);
            let budget = (go * 1e9) as usize;
            println!("[gpu] cache d'experts : budget {:.1} Go de VRAM (LRU), éviction par (couche, expert)",
                     go);
            Some(CacheExperts::nouveau(budg
… [2555 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Inventaire des outils GPU et du dossier bench/

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls tools/ | grep -i gpu; echo \"--- dirs ---\"; ls -d gpu 2>/dev/null; ls -la bench/; echo \"--- gpu.rs kernels ---\"; grep -n \"pub fn \\|const .*PTX\\|include_str\\|EXPERTS_GO\\|pub struct\\|pub enum\" drave-core/src/gpu.rs | head  … [50 caractères tronqués]`

  ```
trace_gpu.py
--- dirs ---
total 16
drwxr-xr-x. 1 stephane stephane   40 25 sep 15:38 .
drwxr-xr-x. 1 stephane stephane  612  7 oct 18:16 ..
-rw-r--r--. 1 stephane stephane 4193 25 sep 15:34 cpu_aer.c
-rw-r--r--. 1 stephane stephane 4522 25 sep 15:38 cpu_merge.c
--- gpu.rs kernels ---
40:const PTX: &str = include_str!("../gpu/drave_gpu.ptx");
74:pub struct MatriceGpu {
86:pub struct KvGpu {
133:pub struct TamponsTopk {
152:pub struct Gpu {
187:    pub fn ouvrir_auto() -> Option<Gpu> {
195:    pub fn ouvrir(ordinal: c_int) -> Option<Gpu> {
356:    pub fn charger_tete(&self, blocs: &[u8], n_out: usize, _n_in: usize, nb: usize) -> Option<MatriceGpu> {
379:    pub fn charger_proj(&self, blocs: &[u8], n_out: usize, nb: usize) -> Option<MatriceGpu> {
385:    pub fn charger_mxfp4(&self, blocs: &[u8], n_out: usize, nb: usize) -> Option<MatriceGpu> {
404:    pub fn charger_q4k(&self, blocs: &[u8], n_out: usize, nb: usize) -> Option<MatriceGpu> {
424:    pub fn kv_allouer(&self, n_kv: usize, ctx: usize, hd: usize, bits: u32) -> Option<KvGpu> {
440:    pub fn kv_assurer(&self, m: &mut KvGpu, besoin: usize) -> bool {
519:    pub fn kv_ecrire_tranche(&self, m: &mut KvGpu, kvh: usize, pos0: usize
… [1436 caractères tronqués]
  ```

### 👤 Utilisateur

Agent 1966e052-ebc6-4f4b-b7f9-6d1c6cb4b445 sent a message:
INVENTAIRE GPU DRAVE (lecture seule, aucun fichier modifié ; M=mesuré, D=déduit du code, S=supposé)

1) CAPACITÉS
| capacité | effet | variable | fichier:ligne | chiffres |
|---|---|---|---|---|
| Pilote + 15 noyaux PTX | API pilote CUDA, PTX sm_75 chargé à la volée (clang, sans toolkit) | DRAVE_GPU (portail) | gpu.rs:1530-1568, 187-347 ; drave-core/gpu/drave_gpu.cu:37-987 ; gpu/compiler.sh | M: 2× Quadro RTX 5000 16 Go ; NVLink 25,781 Go/s/sens ; PCIe cité 6,5 Go/s (gpu.rs:7) |
| Projections Q8_0 (auto) | poids ≥8 Mio copiés UNE fois en VRAM, noyau warp/ligne | DRAVE_GPU seul | model.rs:1550-1569 ; appel 4505-4518 | M: 0,5B FFN 4,6 Mo CPU 123 µs / GPU 151 µs ; gpt-oss attn 12,5 Mo 216/187 µs ; PPL gpt-oss 15,1757→15,1667 ; MoE ctx1024 18,5803→18,3538 (−1,22 %) |
| Tête Q8_0/Q6_K | logits de sortie en VRAM | DRAVE_GPU_TETE | model.rs:4202-4227, 7911-7923 (appels 7834/8077) | M: Q8_0 1,6 ms / 88 Go/s, écart 1,99e-7 (CPU 7,3 ms) ; MXFP4 0,1 ms bit à bit ; Q4_K 0,5 vs 1,2 ms, 4e-7 ; Q6_K 3,6 vs 8,3 ms (tête 191 Mo), 3,3e-7 ; moteur 7,58→3,60 ms/jeton, PPL 13,6877 idem |
| Miroir KV | KV recopié en VRAM par tranches, attention complète déportée | DRAVE_GPU_KV | model.rs:4230-4282 (alloc), 3150-3190 (copie), 5447-5470 (noyau) ; gpu.rs:1178 | M: ctx4096 attn 22,16→3,29 ms/jeton (÷6,7), balayage 219,4→136,2 s (−38 %), PPL 12,2177→12,2175 ; préremplissage 3961 jetons 286,6→63,8 s (×4,5), attn 52,6→2,2 ms (contexte-long.md:305-310) ; 1 M clés int4 968→13,2 ms/couche (×73) |
| Top-k déporté | scores + radix select + collecte + softmax/Σw·V ; noyau 4 fusionné si n≤131 072 | DRAVE_GPU_TOPK (+KV) | model.rs:7220-7312 (garde 7242-7246, seuil 7258) ; gpu.rs:561-1176 | M: banc 4 k clés 1,6e-7 / 31,6× ; 262 k 2,25e-7 / 40× ; ensemble = CPU 14/14 ; noyau 3 1,0-4,8e-7, 0,07 ms constant ; chaîne 1 M 3,90 ms vs 539,9 CPU (×138) ; moteur PPL 9,4162/9,4167 (2 k), 12,2265/12,2267 ; à 2 047 clés attn 19,58→7,59 (−61 %), balayage −24 % ; à 255 clés GPU perd (7,68 vs 4,21) |
| Cache experts MXFP4 | LRU (couche, expert) en VRAM | DRAVE_GPU_EXPERTS / _GO (déf. = VRAM libre −2 Go) | model.rs:4291-4310, 1573-1639, 7578-7596 | M: gpt-oss 32 jetons 5,12→5,43 tok/s (+6 %), succès 53,5 %, verdict « ne pas activer par défaut » ; 1 expert bit à bit ; K3 plafond ×1,41 à 100 % (rapport-cache-experts-vram.md) |
| Bancs CLI | --gpu-banc, --banc-topk, --banc-kv | DRAVE_GPU | main.rs:4441, 3642, 4262 | M, hors porte |

2) CRITÈRE EXACT DU DISPATCH AUTO (copie, model.rs:1558-1568) :
const SEUIL_GPU: usize = 8 << 20;
let gpu = match (&d, crate::gpu::instance()) {
    (Some(d8), Some(machine))
        if d8.src == crate::list::Source8::Q8_0 && keep >= 1.0
           && n_out * d8.nb_ligne * 34 >= SEUIL_GPU => {
        ... machine.charger_proj(blocs, n_out, d8.nb_ligne)
    }
    _ => None,
};
→ Q8_0 seulement, poids empruntés au mmap (keep≥1, DRAVE_SANS_EMPRUNT absent), seuil 8 Mio = n_out×nb_ligne×34 octets ; sinon None → CPU. Seuil M: croisement entre FFN 4,6 Mo (CPU gagne) et attn 12,5 Mo (GPU gagne), aller-retour ~60 µs (commentaire 1552-1557). Refus : sans DRAVE_GPU rien ne part (gpu.rs:1540,1565) ; tête : Q6_K/Q8_0 seulement ; KV : refus si toutes les couches ne tiennent pas OU disposition mixte f32/f16 (model.rs:4245-4279), kv_assurer faux si besoin>ctx ou total>VRAM libre (gpu.rs:446-453) ; top-k : k≤1024, bits 8/32, rep≤32, hd%32=0, hd/32≤4, lot=1, fenêtre=0, nkv×rep=nh, `=0`/vide = inactif, tout refus → CPU sans résultat partiel (model.rs:7242-7312, main.rs:494-514) ; experts : MXFP4 + n_expert>0 seulement.

3) GPU SIMULTANÉS : 2 au plus, UNIQUEMENT pour le KV. instance() = 1 carte — ouvrir_auto essaie les ordinals [1,0] (D: éviter la carte qui pilote l'affichage) et crée un contexte plutôt que le primaire (gpu.rs:187-211) ; second() = un autre ordinal 0-3 (gpu.rs:1538-1548) ; machines() = [premier, second] (gpu.rs:1554-1561). Le miroir KV répartit les couches EN TOURNANT : idx = l % machines.len() (model.rs:4239), et le top-k suit la carte de sa couche (model.rs:7249). Projections, tête et cache d'experts : instance() seul, jamais « second ». NVLink : aucun appel peer/P2P/nvlink dans gpu.rs ni drave_gpu.cu → D: le code n'échange jamais entre cartes, NVLink n'est pas exploité explicitement ; S: CUDA l'emprunterait si un transfert inter-GPU existait (rapport-gpu-tandem-nvlink.md, M 25,78 Go/s ; sur V4-Flash/V4.1 les 2 GPU sont au repos).

4) COUVERTURE — portes automatisées : AUCUNE ne touche le GPU. grep -i "gpu|DRAVE_GPU" dans tools/*.sh = vide ; tools/portes.sh (:53 Qwen 19.3885, :183 gpt-oss 15.6017) et tools/porte-flux.sh ne posent aucune DRAVE_GPU — les valeurs de porte se mesurent SANS GPU (REPRISE.md:890, plan-gpu-topk.md:101). gpu.rs (1573 l.) n'a aucun #[cfg(test)] ; les modules de test de model.rs (:8457 tests_kv, :8509, :8614, :8914, :9036) ne citent jamais gpu → D: zéro test Rust sur le GPU.
- Mesuré à la main seulement : tous les chiffres du §1 (bancs CLI, A/B PPL, tools/compare_logits.py) ; tools/aiguille.py arme DRAVE_GPU/_KV/_TOPK (l.74-82) = harnais de mesure, pas porte.
- Non testé / absent : --gpu-banc/--banc-topk/--banc-kv absents des portes ; bench/ = cpu_aer.c + cpu_merge.c (aucun banc GPU) ; pas de gpu/ à la racine, seulement drave-core/gpu/ ; tools/trace_gpu.py = traceur PyTorch/transformers fp32 (safetensors), étranger à gpu.rs (D d'après son en-tête) — pas un test du chemin CUDA ; chemins de refus (rep>32, hd%32≠0, KV mixte, seconde carte absente, budget experts) jamais exercés par une porte (D).
- Écarts numériques : noyaux exacts sur dense (logits bit à bit, Δ=0,0000) ; sur MoE le déport déplace la PPL de ~1,2-1,5 % (top-1 change sur 14/511) — cause S: bascule du routage top-8, hypothèse étayée non démontrée (rapport-logits-gpu-vs-cpu.md).

### 🤖 Assistant

⏵ Vérification de la preuve « au-delà de localhost » pour le transport TCP

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"0\\.0\\.0\\.0\\|192\\.168\\|10\\.0\\.\\|réseau local\\|autre machine\\|deux machines\" reports/rapport-phase3-reparti.md reports/rapport-prefill-reparti.md reports/rapport-transport-liste.md docs/format-flux.md REPRISE.md  … [65 caractères tronqués]`

  ```
docs/format-flux.md:162:garder cohérents entre deux machines.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"0\\.0\\.0\\.0\" --include=*.md --include=*.sh --include=*.rs . 2>/dev/null | grep -v \"^./journal/\" | head -20; echo \"=== journal (preuves) ===\"; grep -rn \"0\\.0\\.0\\.0\" journal/sessions/bbd6969f-0f70-42b2-8951-64d1f … [76 caractères tronqués]`

  ```
./reports/rapport-coherence-docs-2.md:126:| 57 | `docs/colab-reparti.md:22-28` | fidélité ✅, version ✅, latence ✅, au-delà de localhost ✅, « deux machines avec le même GGUF » ❌, préremplissage par lots ✅ | conforme : `Model::load` lit le fichier entier, `--flux-serveur` accepte `0.0.0.0:PORT` (`main.rs:1807-1814`), `MODE_LOT` existe | OK |
./tools/preparer_colab.sh:35:    ./target/release/drave ../$MODELE --flux-serveur 0.0.0.0:$PORT --ctx 256
./tools/colab_cote_local.sh:29:echo "  sur 0.0.0.0:$PORT — donc au-delà de localhost, ce qu'il faut pour un pair distant"
./tools/colab_cote_local.sh:30:$BIN "$MODELE" --flux-serveur "0.0.0.0:$PORT" --ctx 256 > /tmp/noeud_colab.log 2>&1 &
./docs/colab-reparti.md:31:| au-delà de localhost | ✅ testé sur l'IP du réseau local (`--flux-serveur 0.0.0.0:PORT`) |
./docs/colab-reparti.md:79:   --ppl-reparti <hôte-public>:PORT  ─────────▶ --flux-serveur 0.0.0.0:PORT
./docs/colab-reparti.md:91:    --flux-serveur 0.0.0.0:5599 --ctx 256
./drave-core/src/main.rs:3174:    // (« 0.0.0.0:5599 » pour un pair distant). Le pair distant est le cas de la
./colab/README.md:41:./target/release/drave ../models/Qwen2.5-0.5B-Q8_0.gguf --flux-serveur 0.0.0.0:5599 --ctx 
… [1538 caractères tronqués]
  ```

### 👤 Utilisateur

Background subagent 1966e052-ebc6-4f4b-b7f9-6d1c6cb4b445 finished and will do no further work unless you send it more.
Its closing message:
⏵ Condensé GPU remis au parent, réponse finale

**Inventaire GPU DRAVE** (lecture seule ; M=mesuré, D=déduit du code, S=supposé)

**1) Capacités**

| capacité | effet | variable | fichier:ligne | chiffres |
|---|---|---|---|---|
| Pilote + 15 noyaux PTX | API pilote CUDA, PTX sm_75 chargé à la volée (clang, sans toolkit) | `DRAVE_GPU` (portail) | gpu.rs:1530-1568, 187-347 ; gpu/drave_gpu.cu:37-987 ; gpu/compiler.sh | M: 2× Quadro RTX 5000 16 Go ; NVLink 25,781 Go/s/sens ; PCIe cité 6,5 Go/s (gpu.rs:7) |
| Projections Q8_0 (auto) | poids ≥ 8 Mio copiés UNE fois en VRAM, noyau warp/ligne | `DRAVE_GPU` seul | model.rs:1550-1569 ; appel 4505-4518 | M: 0,5B FFN 4,6 Mo CPU 123 µs / GPU 151 µs ; gpt-oss attn 12,5 Mo 216/187 µs ; PPL gpt-oss 15,1757→15,1667 ; MoE ctx 1024 18,5803→18,3538 (−1,22 %) |
| Tête Q8_0/Q6_K | logits de sortie en VRAM | `DRAVE_GPU_TETE` | model.rs:4202-4227, 7911-7923 (appels 7834/8077) | M: Q8_0 1,6 ms / 88 Go/s, écart 1,99e-7 (CPU 7,3 ms) ; MXFP4 0,1 ms bit à bit ; Q4_K 0,5 vs 1,2 ms, 4e-7 ; Q6_K 3,6 vs 8,3 ms (tête 191 Mo), 3,3e-7 ; moteur 7,58→3,60 ms/jeton, PPL 13,6877 idem |
| Miroir KV | KV recopié en VRAM par tranches, attention complète déportée | `DRAVE_GPU_KV` | model.rs:4230-4282 (alloc), 3150-3190 (copie), 5447-5470 ; gpu.rs:1178 | M: ctx 4096 attn 22,16→3,29 ms/jeton (÷6,7), balayage 219,4→136,2 s (−38 %), PPL 12,2177→12,2175 ; préremplissage 3961 jetons 286,6→63,8 s (×4,5), attn 52,6→2,2 ms (contexte-long.md:305-310) ; 1 M clés int4 968→13,2 ms/couche (×73) |
| Top-k déporté | scores + radix select + collecte + softmax/Σw·V ; noyau 4 fusionné si n ≤ 131 072 | `DRAVE_GPU_TOPK` (+KV) | model.rs:7220-7312 (garde 7242-7246, seuil 7258) ; gpu.rs:561-1176 | M: banc 4 k clés 1,6e-7/31,6× ; 262 k 2,25e-7/40× ; ensemble = CPU 14/14 ; noyau 3 1,0-4,8e-7, 0,07 ms constant ; chaîne 1 M 3,90 vs 539,9 ms CPU (×138) ; moteur PPL 9,4162/9,4167 (2 k), 12,2265/12,2267 ; à 2 047 clés attn 19,58→7,59 (−61 %), balayage −24 % ; à 255 clés GPU perd (7,68 vs 4,21) |
| Cache experts MXFP4 | LRU (couche, expert) en VRAM | `DRAVE_GPU_EXPERTS` / `_GO` (déf. VRAM libre −2 Go) | model.rs:4291-4310, 1573-1639, 7578-7596 | M: gpt-oss 32 jetons 5,12→5,43 tok/s (+6 %), succès 53,5 %, « ne pas activer par défaut » ; 1 expert bit à bit ; K3 plafond ×1,41 (rapport-cache-experts-vram.md) |
| Bancs CLI | `--gpu-banc`, `--banc-topk`, `--banc-kv` | `DRAVE_GPU` | main.rs:4441, 3642, 4262 | M, hors porte |

**2) Critère exact du dispatch auto** (copie, model.rs:1558-1568)
```rust
const SEUIL_GPU: usize = 8 << 20;
let gpu = match (&d, crate::gpu::instance()) {
    (Some(d8), Some(machine))
        if d8.src == crate::list::Source8::Q8_0 && keep >= 1.0
           && n_out * d8.nb_ligne * 34 >= SEUIL_GPU => { ... machine.charger_proj(...) }
    _ => None,
};
```
→ Q8_0 seulement, poids empruntés au mmap (keep≥1, `DRAVE_SANS_EMPRUNT` absent), seuil 8 Mio = `n_out × nb_ligne × 34` octets ; sinon `None` → CPU. Seuil M : croisement entre FFN 4,6 Mo (CPU gagne) et attn 12,5 Mo (GPU gagne), aller-retour ~60 µs (commentaire 1552-1557). Refus : sans `DRAVE_GPU` rien ne part (gpu.rs:1540,1565) ; tête : Q6_K/Q8_0 seulement ; KV : refus si toutes les couches ne tiennent pas OU disposition mixte f32/f16 (model.rs:4245-4279), `kv_assurer` faux si besoin>ctx ou total>VRAM libre (gpu.rs:446-453) ; top-k : k≤1024, bits 8/32, rep≤32, hd%32=0, hd/32≤4, lot=1, fenêtre=0, nkv×rep=nh, `=0`/vide = inactif, tout refus → CPU sans résultat partiel (model.rs:7242-7312, main.rs:494-514) ; experts : MXFP4 + n_expert>0.

**3) GPU simultanés** : **2 au plus, uniquement pour le KV.** `instance()` = 1 carte — `ouvrir_auto` essaie les ordinals **[1,0]** (D : éviter la carte d'affichage) et crée un contexte plutôt que le primaire (gpu.rs:187-211) ; `second()` = un autre ordinal 0-3 (gpu.rs:1538-1548) ; `machines()` = [premier, second] (gpu.rs:1554-1561). Le miroir KV répartit les couches **en tournant** (`idx = l % machines.len()`, model.rs:4239) et le top-k suit la carte de sa couche (model.rs:7249). Projections, tête, experts : `instance()` seul, jamais « second ». NVLink : aucun appel peer/P2P/nvlink dans gpu.rs ni drave_gpu.cu → **D** : le code n'échange jamais entre cartes, NVLink n'est pas exploité explicitement ; **S** : CUDA l'emprunterait si un transfert inter-GPU existait (rapport-gpu-tandem-nvlink.md ; sur V4-Flash/V4.1 les deux GPU sont au repos).

**4) Couverture** — **portes automatisées : aucune ne touche le GPU.** `grep -i "gpu|DRAVE_GPU"` dans tools/*.sh = vide ; `tools/portes.sh` (:53 Qwen 19.3885, :183 gpt-oss 15.6017) et `tools/porte-flux.sh` ne posent aucune `DRAVE_GPU` — les valeurs de porte se mesurent **sans** GPU (REPRISE.md:890, plan-gpu-topk.md:101). gpu.rs (1573 l.) n'a aucun `#[cfg(test)]` ; les tests de model.rs (:8457 `tests_kv`, :8509, :8614, :8914, :9036) ne citent jamais gpu → **D** : zéro test Rust sur le GPU.
- **Mesuré à la main seulement** : tous les chiffres du §1 (bancs CLI, A/B PPL, `tools/compare_logits.py`) ; `tools/aiguille.py` arme `DRAVE_GPU/_KV/_TOPK` (l.74-82) = harnais, pas porte.
- **Non testé / absent** : `--gpu-banc/--banc-topk/--banc-kv` hors portes ; bench/ = seulement cpu_aer.c et cpu_merge.c ; pas de dossier gpu/ à la racine (seulement drave-core/gpu/) ; `tools/trace_gpu.py` = traceur PyTorch/transformers fp32 (safetensors), étranger à gpu.rs (**D** d'après son en-tête) ; chemins de refus (rep>32, hd%32≠0, KV mixte, seconde carte absente, budget experts) jamais exercés par une porte (**D**).
- **Écarts numériques** : noyaux exacts sur dense (logits bit à bit, Δ=0,0000) ; sur MoE le déport déplace la PPL de ~1,2-1,5 % (top-1 change sur 14/511) — cause **S** : bascule du routage top-8, hypothèse étayée non démontrée (rapport-logits-gpu-vs-cpu.md).

Le condensé a été transmis au parent (`send_message` → agent 482522d1…). Aucun fichier n'a été modifié, aucun binaire ni test lancé.

### 🤖 Assistant

⏵ Confirmation du contexte du test « IP du réseau local » (même machine ou deux machines ?)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '24215,24230p' journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md | cut -c1-400; echo \"=== 29779 ctx ===\"; sed -n '29774,29782p' journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md | cut -c1-300", "d … [45 caractères tronqués]`

  ```
```
--flux-serveur accepte hôte:port
    Finished `release` profile [optimized] target(s) in 0.01s
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && IP=$(hostname -I | awk '{print $1}'); echo \"IP locale : $IP\"; (./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf --flux-serveur 0.0.0.0:45797 --ctx 256 > /tmp/serveur_lan.log 2>&1 &) ; for i in $(seq 1 60); do ss -ltn … [408 caractères tronqués]`

  ```
IP locale : 192.168.1.101
[flux] nœud moteur sur 0.0.0.0:45797 · 896 cachés · 24 couches · contexte 256
  référence locale  : perplexité 144.8289  (1.6 s)
  deux nœuds        : perplexité 144.8289  (1.6 s)
  écart             : 0.00e0
  transport         : dense f32 · 3623 octets par flux (aller) · 3623 au retour · 100.0 % d'activité (896 neurones par flux) · 40 flux
  temps             : 15.1 ms par jeton en local · 15.7 ms à attendre le pair (son calcul + l'aller-retour) · soit 1.04× le calcul local seul
[killed by signal: SIGTERM]
=== 29779 ctx ===
  sha256 (24 premiers, à coller dans la cellule 4 du notebook) :
            25130a98aa782284a7dabea0
  ⚠ un autre « drave » tourne déjà (campagne de mesure ?) : le nœud s'y ajoutera

===
… [215 caractères tronqués]
  ```

### 👤 Utilisateur

Agent a4eaa4c8-11e2-4ca3-bcb1-b28919cb601a sent a message:
INVENTAIRE MÉMOIRE / DISQUE / FILS — drave-core (lecture seule, aucun fichier modifié)

**1) Capacités**

| Capacité | Fait | fichier:ligne | État | Chiffre |
|---|---|---|---|---|
| Détection matérielle | /sys (cœurs physiques vs logiques, paires SMT, NUMA, caches L1/L2/L3), /proc/meminfo, nvidia-smi (VRAM/NVLink), df/findmnt (disques+nœud) ; --materiel = resume()+plan() | materiel.rs:91-157,178-273,276-282,408-435 ; main.rs:2333-2335 | mesuré (réf. 20 cœurs/40 fils, 125 Go, 2×RTX5000, NVMe MAP1602, sda ROTA=1) | RAM 22,5 Go/s · VRAM 84,9 · NVMe 31,1 (16 lecteurs) |
| Threads par défaut | cœurs PHYSIQUES ; --threads l'emporte ; pool borné CPU logiques−1 | engine.rs:289-313 ; main.rs:162,666-667,872,521-527 ; engine.rs:390-393 | mesuré | 20 cœurs 22,5 Go/s ; 40 fils 22,8 (rien de plus) ; 10 cœurs 14,7→18,7 +HT (+27 %) |
| Affinité | --pin→EPINGLER ; sched_setaffinity syscall 203 ; cibles = 1re moitié de chaque node*/cpulist | engine.rs:268-334,337-364 ; main.rs:778,835 | mesuré, AUCUNE porte | 20,7→24,7 Go/s épinglé ; 16 fils sur node 0 seul : −16 % |
| mmap poids | Mappe PROT_READ/MAP_PRIVATE par fichier ; DRAVE_MMAP=0 → read_to_end ; tranches/experts empruntés (DenseQ4::emprunter, Vue4) ; DRAVE_SANS_EMPRUNT=1 recopie | gguf.rs:30-177,155-160 ; list.rs:897/910/1070 ; model.rs:824,1096,1213-1241,1528-1540 | mesuré, mmap = défaut | 9,32 s/6,35 Go vs 30,68 s/19,20 Go (lu) ; 47 Mo RSS pour 365,7 Go adressés |
| Prélecture | madvise(MADV_WILLNEED) par expert après routage (DRAVE_PRELIRE=0 off) ; DRAVE_PRELIRE_TOUT=1 off ; union K3 DRAVE_K3_PRELIRE_UNION=1 off | gguf.rs:52-99 ; model.rs:7562-7564,1215-1219 ; kimi_k3.rs:838-855 | mesuré, sans gain ici | +0,3 % (25,73 vs 25,80 s) ; union K3 ×0,37 (6:57 vs 2:34) |
| Éviction | VRAM LRU (couche,expert), budget DRAVE_GPU_EXPERTS_GO (défaut VRAM libre−2) ; RAM DRAVE_EXPERTS_RAM Mo LRU horloge ; arène dense K3 DRAVE_K3_DENSE_FIGE=1 | model.rs:1573-1646,1323-1390,4298-4310,4368-4380 ; kimi_k3.rs:1138-1185 | mesuré, désactivé/déconseillé, pas de porte | RAM +4 % (4 Go) / +21 % (32 Go) ; K3 VRAM plafond ×1,41, verdict ×1,09 (LRU-32 34,5 %) |
| Lecteurs disque | plan.lecteurs = 16.min(physiques.max(4)) — calculé/affiché, JAMAIS utilisé ailleurs (seul appel main.rs:2400) | materiel.rs:318-325 ; main.rs:2400 | SUPPOSÉ, non câblé ; seuls parallélismes réels : page faults noyau, engram ≤16 fils main.rs:1821, K3 ≤16 fils kimi_k3.rs:874 | NVMe ×6 (5,37→31,08) ; engram 10 000 entrées 219–524 ms, 2,6 Mo touchés |

DRAVE_KEEP, DRAVE_FILS, DRAVE_LECTEURS, prefetch, pread, O_DIRECT : inexistants dans drave-core/src (grep vide).

**2) Débits disque mesurés / goulot**
- NVMe MAP1602 node 0 (rapport-architecture-memoire.md:179-184) : 1→5,37 · 4→18,08 · 8→28,29 · 16→31,08 Go/s ; parcours 50,5 Go/395 fichiers 3,42/21,02/33,19 (l.183) ; dd iflag=direct 8,39 Go en 4,247 s = 2,0 Go/s (rapport-materiel-disque-ou-cpu.md:26-28). Réserve l.192-195 : tout tient dans ~112 Go de page cache, O_DIRECT échoue (errno 29) → pas de régime froid isolé.
- Disque dur sda (ROTA=1) : passe K3 1 587 s / 206,58 Gio = 133,5 Mio/s ; plafond séquentiel cp 205 Mio/s → 65 % (rapport-passe-k3-disque.md:60-61,229-234) ; disque occupé 87,6 %, file ≈14, CPU 21 %.
- Goulot : K3 sur HDD → LE DISQUE (206,58 Go/130 Mo/s = 1 589 s vs 1 587 mesuré, 0,1 % ; loi octets(T)=79,0+31,9·T Gio, §11) ; V4.1 Q2 sur NVMe → LE CALCUL (375 s CPU en 16 s de mur, ~0,6 Go/s = 30 % du disque) ; V4-Flash 82 Go sur HDD read_bytes=0 (page cache). Critère 10 min inatteignable (coût fixe 79,0 > 77,9 Gio) ; 3 nœuds ≈8,8 min.

**3) Auto vs manuel**
- Auto : tools/portes.sh:63-68 = SEULE porte matérielle (« threads par défaut », --materiel, 0<threads≤nproc/2). Tests materiel.rs:442-477 (détection cohérente, plan borné). RIEN sur mmap, disque, éviction, prélecture, affinité.
- Manuel : tools/sonde-passe-k3.sh + CSV, --sonder-engram, --gpu-banc, banc mémoire main.rs:268-296, tools/test-plage-k3.sh (bit à bit).
- Statuts : mesuré = rapports avec protocole ; déduit = cout_par_jeton (materiel.rs:381-406, constantes 84,9/22,5/31 Go/s, succès 0,80) + extrapolation N nœuds ; supposé = plan.lecteurs non câblé, et « pas de swap » kimi_k3.rs:1144-1148 CONTREDIT par docs/verification-kimi-k3.md:300-303 (62,8 Go de swap, VmSwap 28,5 Go) — source correcte = /proc/swaps.

Point d'action possible : câbler plan.lecteurs (ou le retirer de l'affichage) ; ajouter une porte mmap/disque (aucune n'existe).

### 🤖 Assistant

⏵ Vérification de la cohérence doc/code du protocole de flux (v5 vs v6)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"version\\|Version\\|79\\|en-tête\" docs/format-flux.md | head -25; echo \"=== fin doc ===\"; sed -n '150,209p' docs/format-flux.md", "description": "Check format-flux doc version"}`

  ```
23:en-tête   "DRVF"                    4 octets
24:          version      u16          = 2 (défaut) ou 3 (`DRAVE_TRACE_BLOCS=1`)
32:          puis n_actifs × ( indice u32 · valeur i16 )           [version 1]
33:          puis n_actifs × ( écart u8 · valeur i16 )             [version 2]
41:l'en-tête de liste de 14 octets pèse alors sur trois fois moins de neurones.
43:### Version 2 : les indices par écarts
46:99,9997 % des cas (22 échappements sur 8 790 000 mesurés). Trois octets par
49:| | version 1 | version 2 |
55:### Version 3 : valeurs i8 et échelle f16 par bloc (`DRAVE_TRACE_BLOCS=1`)
60:| | version 2 | version 3 |
62:| trace dense, 512 jetons | 66 370 408 o | **45 079 930 o (−32,1 %)** |
70:Le lecteur lit **les trois versions** (1, 2 et 3) ; une version inconnue est refusée en la
91:en-tête (79 octets, identique à l'aller et au retour)
93:          version      u8           6   (refusée si différente, en le disant)
164:La version est dans **chaque** en-tête, et un pair d'une autre version est refusé
165:avec un message qui nomme les deux versions en présence :
168:[flux] arrêt : flux en version 99, cette build parle la 5 (pair incompatible : rien n'a été interprété)
171:Le pa
… [4974 caractères tronqués]
  ```

### 👤 Utilisateur

Background subagent a4eaa4c8-11e2-4ca3-bcb1-b28919cb601a finished and will do no further work unless you send it more.
Its closing message:
Résultat envoyé au parent (`482522d1-…`) : l'inventaire ci-dessus tient en ~28 lignes, avec les trois distinctions demandées (mesuré / déduit / supposé), les chemins et numéros de ligne, et deux constats à retenir — `plan.lecteurs = 16` n'est **pas câblé** (materiel.rs:322, seul usage main.rs:2400) et **aucune porte** ne couvre mmap, disque, éviction ou affinité (tools/portes.sh:63-68 ne teste que les threads par défaut).

### 🤖 Assistant

⏵ Vérification du comportement quand un expert manque sur un nœud partiel

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"\\.ou(\" --include=*.rs drave-core/src/ | head -20; echo \"=== contexte ===\"; grep -rn \"\\.ou(\" --include=*.rs drave-core/src/model.rs | head -5", "description": "Find expert lookup usage"}`

  ```
drave-core/src/clusters.rs:326:        assert_eq!(m.ou(0, 3), Some((0, 0)));
drave-core/src/clusters.rs:327:        assert_eq!(m.ou(0, 1), Some((0, 1)));
drave-core/src/clusters.rs:328:        assert_eq!(m.ou(0, 0), Some((1, 0)));
drave-core/src/clusters.rs:329:        assert_eq!(m.ou(0, 2), Some((1, 1)));
drave-core/src/clusters.rs:330:        assert_eq!(m.ou(1, 3), Some((1, 1)));
drave-core/src/clusters.rs:332:        assert_eq!(m.ou(1, 9), None, "un expert hors bornes n'est pas une panique");
drave-core/src/clusters.rs:393:        assert_eq!(m.mapping.ou(0, 3), Some((0, 0)));
drave-core/src/clusters.rs:394:        assert_eq!(m.mapping.ou(0, 1), Some((0, 1)));
drave-core/src/clusters.rs:395:        assert_eq!(m.mapping.ou(0, 0), Some((1, 0)));
drave-core/src/clusters.rs:396:        assert_eq!(m.mapping.ou(0, 2), Some((1, 1)));
drave-core/src/clusters.rs:458:        assert_eq!(un.mapping.ou(0, 0), Some((0, 0)));
drave-core/src/clusters.rs:459:        assert_eq!(un.mapping.ou(0, 4), Some((2, 0)));
drave-core/src/clusters.rs:502:        assert_eq!(m.ou(0, 2), Some((1, 0)));
drave-core/src/clusters.rs:503:        assert_eq!(m.ou(0, 0), None);
drave-core/src/model.rs:1303:            
… [955 caractères tronqués]
  ```

### 👤 Utilisateur

Agent 04ed1834-b0f8-42a1-aa21-75a75c19647e sent a message:
Condensé FACTUEL — répartition multi-machines en réseau (Drave/Qtrinet). Tout est « mesuré » sauf mention « déduit »/« supposé ».

**1) Chiffres mesurés** (valeur · contexte · source:ligne)
- Qwen2.5-0.5B Q8_0, 2 processus 127.0.0.1, 12 couches/nœud, ctx 256 : 144,8289 = 144,8289, écart 0,00e0 à 40 jetons ; avant correctifs 1 621,7239 (×11,2), après la norme seule 693,4492 (×4,8) — reports/rapport-phase3-reparti.md:42-46
- Même banc 1 024 jetons : 9,5146 des deux côtés (0,00e0) ; 19,4 ms/jeton local vs 19,7 ms en attente du pair — :50-54. Flux dense = 3 663 o (79 d'en-tête + 896×4) — :62-64, docs/format-flux.md:178
- Préremplissage mode 3 : 256 jetons en 4 lots de 64 → 0,00e0 (18,0851) ; 1 lot de 917 583 o → 0,00e0 ; contrôle --lot 1 (255 flux) → 0,00e0 (18,0206) ; 1 024 jetons/16 lots → 0,00e0 (9,5939) — reports/rapport-prefill-reparti.md:39-44
- Lots vs jeton, localhost machine au repos (256 jetons) : 116,7 → 22,4 (lots 16) → 18,5 (lots 64) → 16,6 ms/jeton (1 lot) = 7× — :71-77
- Lien latent simulé (+20 ms/message, 64 jetons) : 1 lot = 1 145 ms calcul + 1 488 ms attente = 2,6 s ; 1 flux/jeton = 350+394 ms/jeton = 47,6 s → 18× ; écart 0,00e0 — :56-61
- TCP_NODELAY (200 jetons, localhost) : attente 97,6 → 16,1 ms/jeton (calcul local 15,9 ms, 1,01×) ; banc 24,5 → 8,3 s (réf. locale 8,2 s) — reports/rapport-transport-liste.md:187-200, docs/roadmap.md:113
- Latence simulée (relais local) : 0 ms → 16,8 ms/jeton (1,01×) ; 5 ms → 33,0 (1,99×) ; 20 ms → 81,8 (4,89×) ; attente ≈ calcul distant + 3,2 × latence ; 0,00e0 partout — rapport-transport-liste.md:207-222
- Débits : 0,25 Mbit/s à 20 jetons/s (blocs) ; « < 1 Mbit/s » ; lot de 64 = 229 455 o = 3,5 ko/jeton — rapport-transport-liste.md:183, docs/colab-reparti.md:42-45
- Listes : mode blocs 1 608 o/flux à 256 jetons (vs 3 663 dense), écart 2,74e-2 (÷2,3) ; mode 4 (lots de 16) 1,5 ko/jeton vs 3,5, écart 3,03e-2 — REPRISE.md:926-928, reports/rapport-mode4-lot-listes.md:25-31
- V4-Flash (hc), 2 processus même machine : dense 65 615 o/flux, 0,00e0, 4 873 ms/jeton (1,11×) ; listes 65 544 o, 9,13e-2 (399,6 % d'activité = état dense) — reports/rapport-v4-reparti.md:14-17,88
- V4.1 365,71 Go coupé couche 20 : 82 016 o/flux aller (79+1+16+20 480×4), 81 999 retour, 3 flux, 0,00e0, 1 743 713,6243 des deux côtés (68,0 vs 51,3 s) — reports/rapport-decoupage-v41.md:4,82-90
- K3 : relais 142 ko/saut (4 jetons × 7 168 canaux), transporté par fichier — reports/rapport-passe-k3-disque.md:430-434,478

**2) Deux machines distinctes : NON — tout est localhost**
- Tous les bancs = 2 processus sur la MÊME machine : rapport-phase3-reparti.md:9,16 ; rapport-prefill-reparti.md:37 ; « MÊME machine » rapport-v4-reparti.md:88 ; rapport-decoupage-v41.md:4,153 ; tools/porte-flux.sh:78 (127.0.0.1).
- Seul « au-delà de localhost » : serveur 0.0.0.0:45797 joint par l'IP LAN 192.168.1.101 de la même machine → 0,00e0, 3 623 o/flux, 15,1 vs 15,7 ms (1,04×) — commit 27f46c1 + journal/sessions/bbd6969f-…/digest.md:24220-24233 ; c'est la preuve revendiquée par docs/colab-reparti.md:31.
- Colab jamais exécuté : docs/roadmap.md:58 (3.4 🔬 « reste à le faire tourner sur le runtime Colab ») ; reports/rapport-session-2026-09-30.md:87-88 (« demande le compte de l'utilisateur »). Le « vérifié de bout en bout » (colab/README.md:51) = simulation locale : clone du bundle dans /tmp/colab_test, build 22,8 s, 2 nœuds 127.0.0.1:46550 (digest.md:28282-28302) ; notebook = 15 cellules, 0 sortie.
- tools/pair_factice.py = pair factice sur 127.0.0.1 (:36) qui ne charge aucun modèle et répond des zéros (:124-145) → contrôle du cadriciel, pas un test réseau.

**3) Goulots et limites**
- Latence = seul poste qui compte (1 aller-retour/jeton en séquentiel ; ≈3,2 messages/jeton ; 4,89× à 20 ms) ; Nagle/ACK différé coûtait ×6 (97,6→16,1 ms).
- Débit jamais limitant (0,25–1 Mbit/s à 20 jetons/s) mais AUCUNE mesure de bande passante réelle : pas d'iperf, pas de 1 GbE, pas de RTT WAN dans reports/ ni docs/.
- Taille d'état : 3,5 ko/jeton en lots denses ; 65 615 o/flux (V4-Flash hc×cachés) et 82 016 o (V4.1) → découpage hc = ×4 de transport, listes inutiles (399,6 % d'activité).
- Protocole : en-tête 79 o, v6 (préfixe np/pré-mix), modes 0-4, version refusée ; même GGUF + même build exigés des deux côtés.
- Model::load lit le modèle ENTIER : le découpage porte sur le CALCUL, pas sur la mémoire/disque (docs/colab-reparti.md:32) ; Colab n'accepte aucune connexion entrante → tunnel (ngrok/Tailscale/ssh -R) ; --ctx identique exigé (:130-132).

**4) Explicitement NON testé / supposé**
- Deux machines physiques distinctes (RAM/disques séparés) : jamais exécuté — supposé.
- « Colab 60 ms → ≈112 ms/jeton, ~8 jetons/s contre ~60 local » : DÉDUIT de la droite mesurée jusqu'à 20 ms (rapport-transport-liste.md:224-226), pas mesuré.
- Le « lien latent » 18× est un sleep dans un relais loopback (tools/proxy_latence.py, bind 127.0.0.1:40) : aucune gigue, perte, MTU ni congestion testés.
- K3 : réseau non branché (relais fichier), découpage >2 plages non tenu, extrapolation à N nœuds non validée — rapport-passe-k3-disque.md:478-486.
- Mode 4 avec perte assumée (3,03e-2) ; seul le dense f32 est exact ; plafond R4 (256 Mo) vérifié localement seulement.
- Incohérence doc : docs/format-flux.md:88 dit protocole v6, alors que docs/colab-reparti.md:42 et docs/roadmap.md:123 disent encore v5 (périmé, déduit du format).

### 🤖 Assistant

⏵ Examen du sort d'un expert absent sur un nœud partiel (silence ou refus ?)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '5630,5650p' drave-core/src/model.rs; echo \"=== 7550-7580 ===\"; sed -n '7550,7580p' drave-core/src/model.rs; echo \"=== 1295-1310 ===\"; sed -n '1295,1312p' drave-core/src/model.rs", "description": "Read missing-expert handl … [5 caractères tronqués]`

  ```
// Les paires du chemin par LOTS : `gemm_dense_q4` ne tient pas
                // de compteur (le pool ne connaît pas le modèle), et le chemin
                // jeton, lui, passe par `matvec4_ou_iq` qui en tient un. Sans
                // cette ligne, « paires experts » tombait à ~1 % de sa valeur
                // dès `--lot 2` : le compteur ne voyait plus que les jetons de
                // génération, et un chiffre qui chute de 97 % sans raison
                // visible fait croire à une optimisation qui n'existe pas.
                let mut paires_lot = 0u64;
                for e in 0..ne {
                    let g = groupes[e].len();
                    if g == 0 { continue; }
                    // L'expert global `e` peut ne pas être dans ce nœud.
                    let Some((k, loc)) = moe.ou(e) else { continue; };
                    for (j, &(i, _)) in groupes[e].iter().enumerate() {
                        xg[j * h..(j + 1) * h].copy_from_slice(&x16[i * h..(i + 1) * h]);
                    }
                    s32g.clear();
                    sxg.clear();
                    for &(i, _) in groupes[e].iter() { s32g.push(s32[i].clone()); sxg.push(sx[i]); }
    
… [2910 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification : les experts absents sont-ils comptés ou avertis ?

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '228,280p' drave-core/src/clusters.rs; echo \"=== compteurs experts absents ===\"; grep -rn \"absent\\|manquant\\|hors de ce nœud\\|pas dans ce nœud\" --include=*.rs drave-core/src/model.rs | head -15", "description": "Check p … [22 caractères tronqués]`

  ```
for (num, p) in &clusters {
        if *num >= mapping.n_clusters {
            return Err(std::io::Error::new(std::io::ErrorKind::InvalidData, format!(
                "{} : cluster {num} au-delà des {} annoncés par mapping.tsv",
                p.display(), mapping.n_clusters)));
        }
    }
    // Un nœud peut ne porter qu'une PARTIE des clusters (`DRAVE_CLUSTERS=0,3`) :
    // c'est le mode « nœud partiel », où chaque nœud ne sert que ses experts et
    // où les contributions se somment entre nœuds. Le mapping, lui, reste
    // global : il dit où est chaque expert, pas ce que ce nœud-ci possède.
    let clusters: Vec<(usize, PathBuf)> = match gardes {
        None => clusters,
        Some(g) => {
            for c in g {
                if *c >= mapping.n_clusters {
                    return Err(std::io::Error::new(std::io::ErrorKind::InvalidInput,
                        format!("DRAVE_CLUSTERS : cluster {c} hors bornes ({} au total)",
                                mapping.n_clusters)));
                }
                // Un cluster DEMANDÉ mais absent du disque était ignoré en
                // silence : le nœud tournait avec moins d'experts que voulu, et
       
… [3066 caractères tronqués]
  ```

### 👤 Utilisateur

Background subagent 04ed1834-b0f8-42a1-aa21-75a75c19647e finished and will do no further work unless you send it more.
Its closing message:
⏵ Synthèse livrée ; voici le condensé final

**1) Chiffres mesurés** (valeur · contexte · source:ligne) — « mesuré » sauf mention contraire
- Qwen2.5-0.5B Q8_0, 2 processus 127.0.0.1, 12 couches/nœud, ctx 256 : 144,8289 = 144,8289, écart 0,00e0 à 40 jetons ; avant correctifs 1 621,7239 (×11,2), après la norme seule 693,4492 (×4,8) — `reports/rapport-phase3-reparti.md:42-46`
- Même banc 1 024 jetons : 9,5146 des deux côtés (0,00e0) ; 19,4 ms/jeton local vs 19,7 ms en attente du pair — `:50-54` ; flux dense = 3 663 o (79 d'en-tête + 896×4) — `:62-64`, `docs/format-flux.md:178`
- Préremplissage mode 3 : 256 jetons en 4 lots de 64 → 0,00e0 (18,0851) ; 1 lot de 917 583 o → 0,00e0 ; contrôle `--lot 1` (255 flux) → 0,00e0 (18,0206) ; 1 024 jetons/16 lots → 0,00e0 (9,5939) — `reports/rapport-prefill-reparti.md:39-44`
- Lots vs jeton, localhost machine au repos (256 jetons) : 116,7 → 22,4 (lots 16) → 18,5 (lots 64) → 16,6 ms/jeton (1 lot) = **7×** — `:71-77`
- Lien latent simulé (+20 ms/message, 64 jetons) : 1 lot = 1 145 ms calcul + 1 488 ms attente = **2,6 s** ; 1 flux/jeton = 350+394 ms/jeton = **47,6 s** → **18×**, écart 0,00e0 — `:56-61`
- TCP_NODELAY (200 jetons, localhost) : attente **97,6 → 16,1 ms/jeton** (calcul local 15,9 ms, 1,01×) ; banc 24,5 → 8,3 s (réf. locale 8,2 s) — `reports/rapport-transport-liste.md:187-200`, `docs/roadmap.md:113`
- Latence simulée (relais local) : 0 ms → 16,8 ms/jeton (1,01×) ; 5 ms → 33,0 (1,99×) ; 20 ms → 81,8 (4,89×) ; **attente ≈ calcul distant + 3,2 × latence**, 0,00e0 partout — `rapport-transport-liste.md:207-222`
- Débits : 0,25 Mbit/s à 20 jetons/s (blocs) ; « < 1 Mbit/s » ; lot de 64 = 229 455 o = 3,5 ko/jeton — `rapport-transport-liste.md:183`, `docs/colab-reparti.md:42-45`
- Listes : mode blocs 1 608 o/flux à 256 jetons (vs 3 663 dense), écart 2,74e-2 (÷2,3) ; mode 4 (lots de 16) 1,5 ko/jeton vs 3,5, écart 3,03e-2 — `REPRISE.md:926-928`, `reports/rapport-mode4-lot-listes.md:25-31`
- V4-Flash (hc), 2 processus même machine : dense 65 615 o/flux, 0,00e0, 4 873 ms/jeton (1,11×) ; listes 65 544 o, 9,13e-2 (399,6 % d'activité = état dense) — `reports/rapport-v4-reparti.md:14-17,88`
- V4.1 365,71 Go coupé couche 20 : 82 016 o/flux aller (79+1+16+20 480×4), 81 999 retour, 3 flux, 0,00e0, 1 743 713,6243 des deux côtés (68,0 vs 51,3 s) — `reports/rapport-decoupage-v41.md:4,82-90`
- K3 : relais 142 ko/saut (4 jetons × 7 168 canaux), transporté par **fichier** — `reports/rapport-passe-k3-disque.md:430-434,478`

**2) Deux machines distinctes : NON — tout est localhost**
- Tous les bancs = 2 processus sur la MÊME machine : `rapport-phase3-reparti.md:9,16` ; `rapport-prefill-reparti.md:37` ; « MÊME machine » `rapport-v4-reparti.md:88` ; `rapport-decoupage-v41.md:4,153` ; `tools/porte-flux.sh:78` (127.0.0.1).
- Seul « au-delà de localhost » : serveur 0.0.0.0:45797 joint par l'IP LAN **192.168.1.101** de la même machine → 0,00e0, 3 623 o/flux, 15,1 vs 15,7 ms (1,04×) — commit `27f46c1` + `journal/sessions/bbd6969f-…/digest.md:24220-24233` ; c'est la preuve revendiquée par `docs/colab-reparti.md:31`.
- Colab **jamais exécuté** : `docs/roadmap.md:58` (3.4 🔬 « reste à le faire tourner sur le runtime Colab ») ; `reports/rapport-session-2026-09-30.md:87-88` (« demande le compte de l'utilisateur »). Le « vérifié de bout en bout » (`colab/README.md:51`) = simulation locale : clone du bundle dans `/tmp/colab_test`, build 22,8 s, 2 nœuds 127.0.0.1:46550 (`digest.md:28282-28302`) ; notebook = 15 cellules, **0 sortie**.
- `tools/pair_factice.py` = pair **factice** sur 127.0.0.1 (`:36`), ne charge aucun modèle et répond des zéros (`:124-145`) → contrôle du cadriciel, pas un test réseau.

**3) Goulots et limites**
- Latence = seul poste qui compte (1 aller-retour/jeton en séquentiel ; ≈3,2 messages/jeton ; 4,89× à 20 ms) ; Nagle/ACK différé coûtait ×6 (97,6→16,1 ms).
- Débit jamais limitant (0,25–1 Mbit/s à 20 jetons/s) mais **aucune mesure de bande passante réelle** : ni iperf, ni 1 GbE, ni RTT WAN dans `reports/` ni `docs/`.
- Taille d'état : 3,5 ko/jeton en lots denses ; 65 615 o/flux (V4-Flash hc×cachés) et 82 016 o (V4.1) → découpage hc = ×4 de transport, listes inutiles (399,6 % d'activité).
- Protocole : en-tête 79 o, v6 (préfixe np/pré-mix), modes 0-4, version refusée ; même GGUF + même build exigés des deux côtés.
- `Model::load` lit le modèle ENTIER : le découpage porte sur le **calcul**, pas la mémoire/disque (`docs/colab-reparti.md:32`) ; Colab n'accepte aucune connexion entrante → tunnel (ngrok/Tailscale/ssh -R) ; `--ctx` identique exigé (`:130-132`).

**4) Explicitement NON testé / supposé**
- Deux machines physiques distinctes (RAM/disques séparés) : jamais exécuté — **supposé**.
- « Colab 60 ms → ≈112 ms/jeton, ~8 jetons/s contre ~60 local » : **déduit** de la droite mesurée jusqu'à 20 ms (`rapport-transport-liste.md:224-226`), pas mesuré.
- Le « lien latent » 18× est un `sleep` dans un relais **loopback** (`tools/proxy_latence.py`, bind 127.0.0.1:40) : aucune gigue, perte, MTU ni congestion testés.
- K3 : réseau non branché (relais fichier), découpage >2 plages non tenu, extrapolation à N nœuds non validée — `rapport-passe-k3-disque.md:478-486`.
- Mode 4 avec perte assumée (3,03e-2) ; seul le dense f32 est exact ; plafond R4 (256 Mo) vérifié localement seulement.
- Incohérence doc : `docs/format-flux.md:88` dit protocole **v6**, alors que `docs/colab-reparti.md:42` et `docs/roadmap.md:123` disent encore v5 (périmé).

### 🤖 Assistant

⏵ Vérification : le mode « nœud partiel » par clusters est-il mesuré quelque part ?

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"DRAVE_CLUSTERS\\|nœud partiel\\|noeud partiel\" --include=*.md --include=*.sh --include=*.py . 2>/dev/null | grep -v \"^./journal/\" | head -20", "description": "Grep DRAVE_CLUSTERS usage in docs/tools"}`

  ```
./reports/rapport-lecteur-multifichiers.md:68:| nœud partiel (cluster 0 seul) | 268 786,6218 | **268 786,6218** |
./reports/rapport-lecteur-multifichiers.md:123:### 6. Le nœud partiel pouvait perdre des experts sans le dire (revue adverse)
./reports/rapport-lecteur-multifichiers.md:125:Défaut **bloquant et silencieux**, trouvé par la revue déléguée : `DRAVE_CLUSTERS`
./reports/rapport-lecteur-multifichiers.md:138:### 7. Le correctif du nœud partiel n'avait aucun test
./reports/rapport-lecteur-multifichiers.md:143:coïncident. Il fallait un nœud partiel dont le cluster chargé n'est pas le rang 0.
./reports/rapport-lecteur-multifichiers.md:191:### Le nœud partiel : un huitième des experts pour un huitième de la mémoire
./reports/rapport-lecteur-multifichiers.md:193:`DRAVE_CLUSTERS=0` ne fait charger que `commun.gguf` + `cluster-00.gguf`. Le
./reports/rapport-lecteur-multifichiers.md:261:- Le **nœud partiel** : charger un seul cluster et sommer les experts entre
./reports/rapport-architecture-memoire.md:264:d'un nœud partiel : dix cœurs physiques avec leurs jumeaux valent mieux que dix
./docs/format-clusters.md:162:* **Le nœud partiel** : `DRAVE_CLUSTERS=0,3` ne charge que ces clusters
… [1485 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture des mesures du nœud partiel et du « reste à faire » (sommation inter-nœuds)

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '55,80p' reports/rapport-lecteur-multifichiers.md; echo \"=== 185-200 ===\"; sed -n '185,205p' reports/rapport-lecteur-multifichiers.md; echo \"=== 250-270 ===\"; sed -n '250,270p' reports/rapport-lecteur-multifichiers.md", "d … [44 caractères tronqués]`

  ```
| tenseurs | **1 587** = le compte de la conversion |
| poids | **18,55 Go** = le modèle d'origine |
| chargement complet du modèle | 48 couches en 27,8 s |
| mélanges d'experts chargés | **48/48 couches** |

### Portes de régression

| porte | attendu | obtenu |
|---|---|---|
| Qwen2.5-0.5B ctx 256 `--dense` | 19,3885 | **19,3885** |
| gpt-oss-120b ctx 256 (binaire final, mmap) | 15,1757 | **15,1757** |
| `cargo test --release` | vert | **32 verts** (20 au début du sprint) |
| modèle en clusters | 15,2789 | **15,2789** |
| nœud partiel (cluster 0 seul) | 268 786,6218 | **268 786,6218** |

## Les défauts trouvés

### 1. `q8_dot_at` lisait 34 octets trop tôt — perplexité NaN

Le refactor a changé la signification de `Q8View.base` : offset **global**
(`data_start + offset`) devenu offset **local au fichier**. Deux sites
(`q8_dot_at`, `q8_dot_avx2`) faisaient `&self.bufs[v.fichier]` au lieu de
`&self.bufs[v.fichier][self.starts[v.fichier]..]` : le tenseur était lu dans
l'en-tête du fichier.

La perplexité Qwen est passée à **NaN**, et **aucun test ne l'a vu**. Le test
=== 185-200 ===
n'en touche que 6,35 Go — les pages réellement lues. Un modèle dont on
n'utiliserait qu'un huitième de
… [1986 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Attente du dernier sous-agent (clusters) ; préparation du rapport

- **list_agents** `{}`

  ```
04ed1834-b0f8-42a1-aa21-75a75c19647e [ready] — Extract network split facts
1966e052-ebc6-4f4b-b7f9-6d1c6cb4b445 [ready] — Extract GPU dispatch facts
d04ed7a2-0988-4dfd-83c5-644695dc2f8f [running] — Extract cluster split facts
a4eaa4c8-11e2-4ca3-bcb1-b28919cb601a [ready] — Extract memory/disk/threads facts
  ```

### 🤖 Assistant

⏵ Dernières vérifications : sémantique exacte de --couches et --couches-locales

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '418,442p' drave-core/src/main.rs; echo \"=== 700-715 ===\"; sed -n '700,716p' drave-core/src/main.rs; echo \"=== porte-flux tester ===\"; sed -n '70,80p' tools/porte-flux.sh", "description": "Read couches semantics"}`

  ```
/// Chemin du modèle, posé une fois par `main` : les modes n'ont plus à fouiller
/// `argv` ni à supposer que le modèle est en position 1.
static MODELE: std::sync::OnceLock<String> = std::sync::OnceLock::new();
fn modele_chemin() -> String { MODELE.get().cloned().unwrap_or_default() }

/// **Sonde de plage** (`--tete-partielle`) : appliquer la tête de sortie à la
/// fin d'une plage `--couches a:b`. Par défaut une plage partielle rend le flux
/// résiduel brut — ce qu'un nœud de grappe doit expédier — donc la tête ne voit
/// jamais le jour : impossible de comparer des LOGITS par plage, et impossible
/// de vérifier une réduction finale dont les couches suivantes ne tournent pas
/// encore (V4.1, dont la compression est refusée).
fn poser_tete_partielle(mdl: &mut model::Model) {
    mdl.tete_partielle = true;
    eprintln!("[plage] `--tete-partielle` : la tête de sortie est appliquée à la fin de la \
plage — le résultat est celui d'un modèle TRONQUÉ, pas du modèle entier");
}

/// **Tableau de bord des réglages en vigueur** (`--options-actives`), lus sur le
/// MODÈLE après toutes les affectations.
///
/// Pourquoi il existe : le défaut le plus coûteux de ce dépôt n'est pas un cal
… [2123 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Lecture de la section « nœud partiel » de docs/format-clusters.md

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '150,189p' docs/format-clusters.md", "description": "Read format-clusters partial node section"}`

  ```
`ggml_type_size` pour chaque type, et compare au source Rust. Dernier passage :

```
types confondus : 41 · divergents : 0 · absents du moteur : 0
```

Il liste aussi les types que ggml connaît et que le moteur ignore — c'est ainsi
que les huit types ajoutés après NVFP4 (`Q1_0`, `Q2_0`, `Q6_0`, `Q6_1`, `Q3_0`,
`Q3_1`, `Q2_0S`, `Q2_1`) ont été relevés et ajoutés.

## Ce qui reste

* **Le nœud partiel** : `DRAVE_CLUSTERS=0,3` ne charge que ces clusters — et un
  cluster **demandé mais absent du disque est une erreur**, pas un silence : sans
  cela, un artefact amputé passait pour complet et les contributions manquantes
  disparaissaient sans un mot. Mesuré
  sur Qwen3-30B, mêmes 7 jetons :

  | clusters | perplexité | mémoire |
  |---|---|---|
  | 1 | 268 786,62 | **2,35 Go** |
  | 2 | 63 780,09 | 2,83 Go |
  | 4 | 3 378,91 | 4,60 Go |
  | 8 | **799,8557** | 6,28 Go |

  **Ce qui manque** : la somme des contributions entre nœuds. Le moteur saute
  déjà un expert absent, mais rien n'additionne encore ce que deux nœuds calculent
  chacun de leur côté. Avec elle, deux nœuds à quatre clusters rendraient
  799,8557 pour 4,60 Go chacun — moins que les 6,28 Go d'un nœud complet.
* **Les bia
… [757 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Vérification de la présence des artefacts nécessaires aux portes (clusters, modèles)

- **bash** `{"command": "ls -d /home/stephane/FastNVMe/artefacts/modeles-optimises/qwen3-30b-8clusters-v2 2>&1 | head -3; ls /home/stephane/FastNVMe/artefacts/modeles-optimises/qwen3-30b-8clusters-v2 2>/dev/null | head -5; echo \"--- modeles repo ---\"; ls -la /home/stephane/Data13TB/stephane/GitHub/Qtrinet/mod … [179 caractères tronqués]`

  ```
/home/stephane/FastNVMe/artefacts/modeles-optimises/qwen3-30b-8clusters-v2
cluster-00.gguf
cluster-01.gguf
cluster-02.gguf
cluster-03.gguf
cluster-04.gguf
--- modeles repo ---
total 863324
drwxr-xr-x. 1 stephane stephane        88 25 sep 17:13 .
drwxr-xr-x. 1 stephane stephane       612  7 oct 18:16 ..
-rw-r--r--. 1 stephane stephane 352972352 25 sep 17:13 Qwen2.5-0.5B-Q4_0.gguf
-rw-r--r--. 1 stephane stephane 531068480 25 sep 16:52 Qwen2.5-0.5B-Q8_0.gguf
--- ids ---
-rw-r--r--. 1 stephane stephane  2437 28 sep 15:41 /tmp/ids_oss_512.txt
-rw-r--r--. 1 stephane stephane 21380 30 sep 17:11 /tmp/ids_qwen.txt
-rw-r--r--. 1 stephane stephane    40  3 oct 07:51 /tmp/ids_v41_8.txt
  ```

### 👤 Utilisateur

Agent d04ed7a2-0988-4dfd-83c5-644695dc2f8f sent a message:
CONDENSÉ — Découpage en clusters et par plages de couches (Qtrinet/Drave, lecture seule stricte, rien modifié/compilé/testé). État : P = vérifié par une porte, M = mesuré localement (rapport/REPRISE), D = déduit du code.

1) TABLEAU
| capacité | ce qu'elle fait | source | état | chiffre |
| Lecteur clusters | commun.gguf + cluster-XX.gguf réunis en un Gguf ; experts sous cl{c}/ ; mapping.tsv lu d'un bloc | drave-core/src/clusters.rs:150-297 · gguf.rs:478-520 | P (porte 1 : 6 tests clusters.rs:309-505 ; porte 3) | 9 fichiers · 1 587 tenseurs · 18,55 Go |
| Nœud partiel | DRAVE_CLUSTERS=0,3 ne charge que ces clusters ; demandé-absent = erreur ; incomplet refusé sans DRAVE_CLUSTERS | clusters.rs:167-176, 239-273, 291-295 | M | 1 cl. 2,35 Go/268 786,62 · 4 cl. 4,60 Go/3 378,91 · 8 cl. 6,28 Go/799,8557 |
| Porte clusters | dossier complet Qwen3-30B 8 clusters, mêmes jetons | tools/portes.sh:55-61 | P | attendu 799.8557 (--ctx 64 --limit 8 --dense --lot 1) |
| Convertisseur experts | GGUF → commun.gguf + 8 cluster-XX.gguf + mapping.tsv + manifeste.json, copie d'octets sans requantification | tools/convertir_clusters.py:402-582 | M | 435+8×144 = 1 587 tenseurs · 18,60 Go · 351,7 s · SHA-256 « TOUT CONCORDE » |
| Conversion par plages de couches | --mode couches : blocs blk.N en groupes contigus (dense), pas de mapping.tsv | convertir_clusters.py:446-463, 520-529 | M | Qwen2.5-0.5B : commun + 4 fichiers × 6 couches · 290 tenseurs |
| mmap du dossier | N fichiers mappés, pages lues à la demande | gguf.rs:153-170 · clusters.rs:282-286 | M | 9,32 s/6,35 Go contre 30,68 s/19,20 Go (DRAVE_MMAP=0), ppl identique |
| Plage de couches moteur | couche_debut..couche_fin = [a,b) exécutée ; hors plage → flux résiduel brut | model.rs:2551-2569, 4368-4369, 6641-6646, 6904-6905 | M (V4.1), aucune porte | V4.1 2 nœuds : écart 0,00e0 · 1 743 713,6243 (51,3 s contre 68,0 s) |
| Réparti pilote/pair | --couches-locales N : local [0,N), pair [N,n_layer), plage portée par l'en-tête | main.rs:3345, 3430, 3457-3460, 3549, 3204-3213 | M | écart 0,00e0 dense (REPRISE.md:1307-1316) |
| Outils d'analyse | co-activation/ventilation MoE, union d'experts lus, jumeaux statiques, localité de couche (R²) | tools/clusters_moe.py · analyse_union_experts.py · analyse_experts_statique.py · localite_couches.py | M hors moteur | couverture 0,799/0,607/0,442 à 4/8/16 clusters ; hasard 0,440/0,319/0,250 |

2) CE QUE LE FORMAT CHANGE / RESTE À FAIRE
- Fichiers : commun.gguf + N cluster-XX.gguf + mapping.tsv + manifeste.json (9 GGUF pour Qwen3-30B) ; source 18,56 Go → commun 1,00 Go + cluster 2,20 Go ; surcoût = métadonnées dupliquées 8×~4 Mo = 0,2 % (docs/format-clusters.md:80-89).
- Partagé/commun : routeur ffn_gate_inp (clusters.rs:9-11) ; expert partagé ffn_*_shexp (2D, ne matche pas « _exps. ») → convertir_clusters.py:428 ; model.rs:695-713. Biais par expert + clusters = REFUSÉ par panic plutôt que mal indexé (model.rs:791-796).
- Jointure : mapping.tsv texte 4 colonnes (couche, local, global, cluster), 6 144 lignes pour 48×128 (rapport-lecteur-multifichiers.md:240) ; rangé en local[couche][global]=cluster×65536+ligne (clusters.rs:103) ; publié en OnceLock après ouverture réussie (clusters.rs:291-295) ; Moe::ou traduit puis cherche le n° parmi les vues chargées (model.rs:1299-1311) ; les 3 projections doivent porter les mêmes clusters (model.rs:717-731).
- À faire : sommer les contributions entre nœuds (docs/format-clusters.md:175-178 ; rapport-lecteur-multifichiers.md:208-215) ; découper les biais d'experts ; équilibrer par charge (format-clusters.md:187-189) ; manifeste binaire si un fichier par expert (185-186).

3) SÉMANTIQUE EXACTE
- --couches a:b : main.rs:706-712 — exige « a:b » (sinon panic « --couches attend `a:b` ») ; a,b en usize par parse().unwrap() ; AUCUN contrôle de bornes à l'analyse. Report model.rs:4368-4369 : couche_debut=a, couche_fin=b ; doc model.rs:2551-2554 « dernière couche PORTÉE (exclue) » → plage [a,b) ; boucles `for l in couche_debut..couche_fin` (model.rs:6904 forward, aussi 4751, 5345, 6562). Donc a inclus, b exclu.
- b == n_layer → norme finale + tête (model.rs:6641-6646) ; b < n_layer → flux résiduel brut (model.rs:5740, 7745-7752), sauf --tete-partielle qui applique la tête en fin de plage et l'annonce (main.rs:423-435).
- Refus : a>=b et b>n_layer ne sont PAS refusés par le moteur principal. a>=b → boucle vide, rend l'entrée sans erreur ; b>n_layer → layers[l] indexé directement (model.rs:6905) → panique « index out of bounds ». Seuls gardes : --k3-essai (main.rs:2131-2134, « plage {debut}:{fin} invalide pour {n} couche(s) ») et le serveur de flux (main.rs:3210-3213, flux refusé, le nœud continue).
- Reprise à a>0 sans flux : V4.1 avertit « convention de sonde, copie 0 » (model.rs:6791-6800) ou assert si flux brut sans `pre` (model.rs:6787-6790). Un manque d'architecture n'est retiré que s'il tombe dans [a,b) (model.rs:3485-3500).
- `--plage` n'existe PAS comme option CLI : grep `"--plage"` = 0 occurrence ; c'est le concept, et --k3-essai réutilise opt.couches (main.rs:147, 1899).
- --couches-locales N : main.rs:705, défaut 12 si 0 (main.rs:3345) ; pilote couche_fin=N, couche_debut reste 0 (main.rs:3430) → [0,N) ; l'en-tête porte debut=N, fin=n_layer (main.rs:3457-3460, 3549) → pair exécute [N,n_layer), revalidé (main.rs:3210). Aucun contrôle N ≤ n_layer : déduit du code, N>n_layer non refusé et sortirait du tableau layers au pilote (model.rs:6905).

4) MESURÉ / DÉDUIT / SUPPOSÉ
- Mesuré et gardé : 799,8557 (porte 3 : dossier complet, ctx 64, 8 ids → 7 jetons) ; 6 tests unitaires clusters.rs via la porte 1 (cargo test ≥48 verts, portes.sh:32-44). Aucune porte ne couvre DRAVE_CLUSTERS, --couches a:b ni --couches-locales (grep portes.sh : néant).
- Mesuré une fois, non gardé : table nœud partiel 1/2/4/8 clusters (rapport-lecteur-multifichiers.md:199-204) ; 15,2789 = 15,2789 sur 63 jetons (docs/format-clusters.md:116) ; conversion, mmap, mesures Python.
- Déduit du code, non mesuré : absence de refus pour a>=b, b>n_layer, N>n_layer ; « boucle vide » silencieuse.
- Supposé/à faire : « la somme inter-nœuds rendrait 799,8557 pour 4,60 Go par nœud » est un calcul, pas une mesure (rapport-lecteur-multifichiers.md:209-210) ; biais d'experts refusés ; rééquilibrage par charge non fait.
- Aucun fichier reports/*cluster* n'existe ; les rapports clusters réels sont rapport-lecteur-multifichiers.md, rapport-decoupage-moe.md (clusters d'experts, pas de plage a:b), rapport-decoupage-v41.md et decoupage-v41-digest.txt (plages 0-19/20-39, pas de clusters).

### 🤖 Assistant

⏵ Rédaction du rapport final et transmission au parent

- **send_message** `{"agent_id": "d31b3d9b-58e4-4d34-85fa-381b6f6a6a76", "message": "# Drave — capacités de DISTRIBUTION et d'EXPLOITATION HÉTÉROGÈNE (inventaire, LECTURE SEULE)\n\nAucun fichier modifié, aucune compilation ni test lancé. Légende : **P** = mesuré ET vérifié par une porte du dépôt · **M** = mesuré (rappo … [12919 caractères tronqués]`

  ```
message delivered to agent d31b3d9b-58e4-4d34-85fa-381b6f6a6a76
  ```

### 🤖 Assistant

⏵ Rapport final livré au parent

# Drave — capacités de DISTRIBUTION et d'EXPLOITATION HÉTÉROGÈNE (inventaire, LECTURE SEULE)

Aucun fichier modifié, aucune compilation ni test lancé. Légende : **P** = mesuré ET vérifié par une porte du dépôt · **M** = mesuré (rapport/REPRISE) · **D** = déduit du code · **S** = supposé.

## 1. TABLEAU PAR CAPACITÉ

### 1.a Plusieurs machines en réseau — `--flux-serveur` / `--ppl-reparti`
| capacité | fait | état | source | chiffre |
|---|---|---|---|---|
| Nœud moteur TCP | charge le modèle, écoute, applique SA plage reçue dans l'en-tête, renvoie le flux brut | P | `main.rs:3170-3340` | 1 client à la fois |
| Pilote TCP | garde N couches locales, envoie, reçoit, note la perplexité | P | `main.rs:3340-3650` | écart local/réparti **0,00e0** (144,8289 ; 9,5146 à 1 024) — `reports/rapport-phase3-reparti.md:42-54` |
| Protocole v6 | en-tête 79 o, 14 champs de réglages, 5 modes | P | `main.rs:2495-2620` (`VERSION_FLUX=6`, `TAILLE_TETE=79`) | `tests_flux`, `tests_plafond` (`main.rs:5511-5845`) |
| Modes 0-4 | dense f32 · listes i16 · blocs i8+échelle/32 · lot dense · lot en listes | P | `tools/porte-flux.sh` | écarts 0 / 0 / ≤6e-2 / 0 / ≤1e-2 |
| Préremplissage réparti | 1 aller-retour par lot au lieu d'un par jeton | P (mode 3) | `main.rs:3360-3520` | 256 jetons en 4 lots → **0,00e0** ; 1 lot de 917 583 o → 0,00e0 |
| TCP_NODELAY | supprime Nagle + ACK différé | M | `main.rs:3196-3201, 3428-3430` | **97,6 → 16,1 ms**/jeton (local 15,9) = 1,01× |
| Relais de latence | mesure le coût d'un lien distant | M | `tools/proxy_latence.py` | attente ≈ calcul distant + **3,2 × latence** ; ×1,01/×1,99/×4,89 à 0/5/20 ms |
| Pair factice | contrôle indépendant du cadriciel (ne calcule rien) | M | `tools/pair_factice.py` | 127.0.0.1 seulement |
| Recette Colab | bundle git + notebook + tunnel | **non exécutée** | `tools/preparer_colab.sh`, `colab/`, `docs/colab-reparti.md` | roadmap 3.4 = 🔬 |

### 1.b Découpage en plages de couches — Kimi-K3
| capacité | fait | état | source | chiffre |
|---|---|---|---|---|
| `--couches a:b` | exécute [a,b) ; hors plage → flux résiduel brut | M (V4.1), D | `main.rs:705-712, 2123-2160`, `model.rs:2551-2569, 6904` | V4.1, 2 nœuds : 0,00e0 — `reports/rapport-decoupage-v41.md` |
| Relais entre nœuds | flux résiduel + pile des banques (sinon `res_mix` faux ET muet) | **M, porte manuelle tenue** | `kimi_k3.rs:1595-1690` | **142 ko** (4 jetons × 7 168 canaux + 2 banques) |
| Transport du relais | **fichier** (`File::create` / `std::fs::read`) | M | `kimi_k3.rs:1610-1655` | le commentaire dit : « ce n'est pas un protocole de réseau, c'est un fichier » |
| Garde-fou | refuse un relais pris à une autre couche que le début de plage | M | `kimi_k3.rs:1683-1688` | — |
| Porte bit à bit | A 0:13 → relais → B 13:26 vs C 0:26 monolithe | **M hors porte** | `tools/test-plage-k3.sh` (jamais appelé par `portes.sh`) | `cmp` identique, commit `3c2b542` |

### 1.c Découpage en clusters (experts)
| capacité | fait | état | source | chiffre |
|---|---|---|---|---|
| Lecteur clusters | `commun.gguf` + `cluster-XX.gguf` + `mapping.tsv` réunis en un Gguf | P | `clusters.rs:150-297` | Qwen3-30B : 9 fichiers, 1 587 tenseurs, 18,55 Go |
| Convertisseur | copie d'octets, sans requantification | M | `tools/convertir_clusters.py:402-582` | 351,7 s, SHA-256 concorde |
| Mode « couches » | groupes `blk.N` contigus, sans mapping | M | `convertir_clusters.py:446-463` | Qwen2.5-0.5B : commun + 4×6 couches |
| Nœud partiel | `DRAVE_CLUSTERS=0,3` ne charge que ces clusters | M | `clusters.rs:166-275` | 1 cl. **2,35 Go**/PPL 268 786,62 · 4 cl. 4,60 Go/3 378,91 · 8 cl. 6,28 Go/799,8557 |
| mmap du dossier | N fichiers mappés, pages à la demande | M | `gguf.rs:153-170`, `clusters.rs:282-286` | **9,32 s/6,35 Go** contre 30,68 s/19,20 Go |
| Porte clusters | dossier complet Qwen3-30B, mêmes jetons | P | `tools/portes.sh:55-61` (artefact présent sur disque) | attendu **799.8557** |
| Outils d'analyse | co-activation, union d'experts, localité | M | `tools/clusters_moe.py`, `analyse_union_experts.py`, `localite_couches.py` | couverture 0,799/0,607/0,442 à 4/8/16 clusters (hasard 0,440/0,319/0,250) |

### 1.d GPU (une machine)
| capacité | fait | état | source | chiffre |
|---|---|---|---|---|
| Pilote + 15 noyaux PTX sm_75 | API CUDA brute, PTX compilé par clang | M | `gpu.rs:40, 187-347`, `drave-core/gpu/` | 2× Quadro RTX 5000 16 Go ; NVLink 25,781 Go/s/sens |
| Projections Q8_0 auto | poids ≥ 8 Mio copiés en VRAM | M | `model.rs:1558-1568` | seuil `n_out × nb_ligne × 34 ≥ 8 Mio` ; gpt-oss 15,1757→15,1667 |
| Tête Q8_0/Q6_K | logits en VRAM | M | `model.rs:4202-4227` | 1,6 ms / 88 Go/s, écart 1,99e-7 (CPU 7,3 ms) |
| Miroir KV | KV en VRAM, attention déportée | M | `model.rs:4230-4282, 5447` | attn 22,16→3,29 ms/jeton (÷6,7) ; 1 M clés int4 : ×73 |
| Top-k GPU | scores + radix + collecte + softmax | M | `model.rs:7220-7312`, `docs/plan-gpu-topk.md` | 262 k clés : 2,25e-7, ×40 ; à 2 047 clés −61 % |
| Cache experts MXFP4 | LRU (couche, expert) en VRAM | M | `model.rs:4291-4310` | +6 % (gpt-oss) ; « ne pas activer par défaut » |
| 2 GPU simultanés | **KV seulement**, tourniquet `l % machines.len()` | M | `model.rs:4239`, `gpu.rs:1538-1561` | projections/tête/experts : 1 carte ; aucun P2P/NVLink explicite (D) |

### 1.e Mémoire, disque, fils (une machine)
| capacité | fait | état | source | chiffre |
|---|---|---|---|---|
| Détection matérielle | /sys (physiques/SMT/NUMA/caches), /proc/meminfo, nvidia-smi, df | P (partielle) | `materiel.rs:91-282` | 20 cœurs/40 fils, 125 Go, 2 GPU, NVMe + sda |
| mmap des poids | PROT_READ/MAP_PRIVATE, tranches empruntées | M | `gguf.rs:30-177` | **47 Mo RSS pour 365,7 Go** adressés |
| `DRAVE_MMAP=0` | lecture complète (repli) | M | `gguf.rs:153-160` | 30,68 s/19,20 Go contre 9,32 s/6,35 Go |
| Prélecture | `madvise(WILLNEED)` des experts routés | M | `model.rs:7562-7564` | **+0,3 %** (sans gain) |
| Éviction | VRAM LRU + RAM `DRAVE_EXPERTS_RAM` | M | `model.rs:1573-1646` | RAM +4 % (4 Go), +21 % (32 Go) → déconseillé |
| Threads | cœurs PHYSIQUES par défaut, `--threads` prioritaire | P | `main.rs:521-527`, `engine.rs:289-313` | porte `portes.sh:63-68` |
| Affinité | `--pin` → `sched_setaffinity`, 1re moitié de chaque nœud NUMA | M (aucune porte) | `engine.rs:268-364` | 20,7→**24,7 Go/s** ; node 0 seul : −16 % |
| Plan de placement | `--plan` chiffre couche par couche où mettre les poids | **affichage seul** | `main.rs:4769-4830` | CPU 20 · PCIe 6,5 · NVLink 25,78 · GPU 380 Go/s |

## 2. CE QUI EST PROUVÉ PAR UNE PORTE (et ce qui ne l'est pas)

**Prouvé :** (1) `tools/portes.sh:32-44` — `cargo test --release`, ≥48 verts ET 0 échec (**77 tests** dans le source) ; couvre le codec de flux et les refus de trames (`tests_flux`, `tests_plafond` : plafond R4, 100 M d'états refusés AVANT allocation) et 6 tests clusters. (2) `portes.sh:55-61` — Qwen3-30B en clusters = **799.8557**. (3) `portes.sh:63-68` — threads par défaut = cœurs physiques. (4) `portes.sh:243-263` — `tools/porte-flux.sh`, **seule porte du découpage** : deux processus sur **127.0.0.1**, Qwen2.5-0.5B, 12 couches locales, les 5 modes. (5) rejeu de trace + formats contre libggml.

**Non prouvé par une porte :** aucun mode **au-delà de loopback** — le seul essai « réseau » est un serveur `0.0.0.0:45797` joint par l'IP LAN **192.168.1.101 de la MÊME machine** (journal `bbd6969f…/digest.md:24220-24233` : 0,00e0, 15,1 vs 15,7 ms) ; **aucune porte GPU** (grep `DRAVE_GPU` dans `tools/*.sh` = vide ; `gpu.rs` sans `#[cfg(test)]`) ; **aucune porte** mmap/disque/éviction/affinité ; **aucune porte** pour `DRAVE_CLUSTERS`, `--couches a:b`, `--couches-locales` hors `porte-flux.sh` ; `tools/test-plage-k3.sh` n'est appelé par personne ; **Colab jamais exécuté**.

## 3. CE QUI MANQUE CONCRÈTEMENT

**(a) Répartir sur les unités d'UNE machine**
1. **Ordonnanceur absent** (roadmap 2.1 = ⏳) : `--plan` conseille, rien ne décide à l'exécution ; seul dispatch automatique = seuil codé en dur (Q8_0 ≥ 8 Mio, `model.rs:1558-1568`), sans modèle de coût PCIe/NVLink/latence.
2. **2 GPU sous-exploités** : seul le KV est réparti (`model.rs:4239`) ; projections, tête, cache d'experts sur `instance()` ; aucun appel P2P/NVLink dans `gpu.rs`/`drave_gpu.cu` (D).
3. **Disque non parallélisé** : `plan.lecteurs = 16.min(physiques.max(4))` est calculé et affiché mais **jamais utilisé** (`materiel.rs:318-325` ; seul appel `main.rs:2400`) ; parallélisme réel = page faults ; ni `O_DIRECT` ni `pread` (grep vide).
4. **Nœud partiel par clusters inexploitable** : `Moe::ou()` rend `None` et le code fait `continue` (`model.rs:5642, 7571`) — expert absent **sauté sans un mot**. Il manque « la somme des contributions entre nœuds » (`docs/format-clusters.md:173-179`, `reports/rapport-lecteur-multifichiers.md:261-263`) ; 1 cluster = PPL 268 786,62. Rien n'additionne.
5. Éviction RAM perdante (+4 %/+21 %), prélecture sans gain (+0,3 %) : seul levier disque restant = page cache.

**(b) Répartir sur PLUSIEURS machines en réseau**
1. **Bloqueur n°1 : chaque nœud charge le modèle ENTIER** — `Model::load` mappe tout le GGUF ; le découpage porte sur le CALCUL, pas la RAM ni le disque (`docs/colab-reparti.md:32`). Un modèle > RAM ne peut donc PAS être réparti.
2. **Le découpage par plages K3 ne passe pas par le réseau** : `kimi_k3::Relais::ecrire/lire` = `std::fs` (`kimi_k3.rs:1610-1655`) ; aucun TCP dans ce chemin — exactement « un transport par fichier au lieu d'un transport réseau ».
3. **Pas de sommation inter-nœuds** pour les clusters (a.4) : la seule voie MoE répartie est inutilisable.
4. **Banc d'essai, pas service** : `run_serveur_flux` sert **un seul client puis s'arrête** (`main.rs:3169`) ; pas de reconnexion, reprise, TLS, compression ni découverte ; pas de découpage > 2 nœuds (`reports/rapport-passe-k3-disque.md:478-486`).
5. **Aucune mesure de bande passante réelle** : pas d'iperf, pas de 1 GbE, pas de RTT WAN ; latence simulée par un `sleep` loopback (`tools/proxy_latence.py:40`) — ni gigue, ni perte, ni MTU, ni congestion.
6. **Colab non démontré** ; contraintes non automatisées : même build + même GGUF + même `--ctx`, tunnel obligatoire.

## 4. LIMITES MESURÉES

**Réseau** : 3 663 o/flux dense ; 1 608 o en blocs à 256 jetons (2,74e-2, ÷2,3) ; 1,5 ko/jeton en mode 4 (3,03e-2) ; lot de 64 = 229 455 o. Débit jamais limitant : **0,25 Mbit/s** à 20 jetons/s. Latence = seul poste : 1 aller-retour/jeton, ≈3,2 messages/jeton, **×4,89 à 20 ms**. Nagle/ACK différé coûtait ×6. Colab 60 ms → ≈112 ms/jeton, ~8 jetons/s contre ~60 local : **DÉDUIT**, pas mesuré.
**PCIe/GPU** : PCIe x8 6,5 Go/s (cité `gpu.rs:7`), NVLink **25,781 Go/s**/sens, VRAM 84,9 Go/s, RAM 22,5 Go/s, CPU 14-25 Go/s ; seuil de bascule ≈ 8 Mio, aller-retour ≈ 60 µs ; sous ~255 clés le GPU **perd** (7,68 vs 4,21 ms).
**Disque** : NVMe 1→5,37 · 4→18,08 · 8→28,29 · **16 lecteurs→31,08 Go/s** ; `dd iflag=direct` 2,0 Go/s ; HDD sda plafond **205 Mio/s**, passe K3 **133,5 Mio/s** (65 %, disque occupé 87,6 %, CPU 21 %). Goulot : K3 sur HDD = **le disque** (206,58 Go/130 Mo/s ≈ 1 589 s, mesuré 1 587 s) ; V4.1 Q2 sur NVMe = **le calcul** (≈0,6 Go/s, 30 % du disque).
**Mémoire** : 47 Mo RSS pour 365,7 Go adressés ; cache VRAM experts +6 % ; LRU RAM perdante. Contradiction : `kimi_k3.rs:1144-1148` dit « pas de swap », `docs/verification-kimi-k3.md:300-303` relève **62,8 Go de swap** (VmSwap 28,5 Go) — non tranché.
**Doc** : `docs/colab-reparti.md:42` et `docs/roadmap.md:123` disent encore protocole **v5** alors que `VERSION_FLUX=6` ; la ligne « deux machines avec le même GGUF ❌ » est la limite la plus lourde, assumée.

**Verdict** : le dépôt sait faire *un* découpage juste et prouvé — **2 nœuds TCP, N plages de couches, mêmes logits au bit près** — mais sur la même machine, avec le modèle entier de chaque côté. Ce qui manque n'est pas le transport (fidèle et prouvé) : c'est (i) le partage de la MÉMOIRE et du DISQUE entre nœuds, (ii) la sommation inter-nœuds des experts, (iii) le branchement réseau du relais K3, (iv) toute mesure sur un vrai lien, (v) toute porte GPU/mmap/disque.

### 👤 Utilisateur

Agent d04ed7a2-0988-4dfd-83c5-644695dc2f8f sent a message:
ADDENDUM au condensé (vérifié moi-même après le rapport étendu du sous-agent) — 4 points qui complètent, rien à corriger :
1. Plages de couches réellement mesurées, en plus de V4.1 : reports/rapport-phase3-reparti.md:42-53 — pilote 0..12 / nœud 12..24, Qwen2.5-0.5B ctx 256 : locale 144,8289 = répartie 144,8289, écart 0,00e0 ; avant correctif ×11,2 ; après la norme seule ×4,8 ; 1 023 flux servis, 9,5146 des deux côtés, 19,4 vs 19,7 ms/jeton. Et reports/rapport-passe-k3-disque.md:409-467 — `--couches a:b` coupé à la couche 13 (0..12 → relais → 13..26 → monolithe 0..26) : B et C identiques AU BIT, 4 jetons, 28 672 octets.
2. tools/test-plage-k3.sh:1-36 EST cette porte (lance `--k3-essai --couches 0:13 / 13:26 / 0:26`) mais elle N'EST PAS câblée dans tools/portes.sh (grep « plage » dans portes.sh = 0 occurrence). Seules portes liées dans portes.sh : n°3 (clusters, 799.8557) et n°1 (cargo test ≥48, qui couvre les 6 tests de clusters.rs).
3. Second artefact clusters complet : V4-Flash 86,9 Go → commun + 8 clusters, 11 008 entrées de mapping (43 couches × 256 experts), 450 s, original 8 430,2968 (111,8 s) vs éclaté 8 430,2968 (39,9 s), soit 2,8× (reports/rapport-v4-reparti.md:55-70) ; --ppl-reparti sur le même : 0,00e0 (reports/rapport-materiel-disque-ou-cpu.md:72-75).
4. Point sensible levé : le correctif de routage a déplacé la porte Qwen3-30B clusters transitoirement à 799,8152 (−0,005 %, cause : x/s au lieu de x*(1/s)) puis elle est revenue à 799,8557 AU BIT PRÈS (reports/rapport-routage-experts.md:65-77) — la valeur attendue de portes.sh:60 est donc cohérente. Confirmation satellite : 799,8557 inchangée dans rapport-optimisations-auto.md:135, rapport-mla-experts.md:98-100, rapport-coherence-vision.md:159 (48 tests).
Rappel : aucun fichier reports/*cluster* ; les homonymes « grappes » (neurones/co-activation, ex. docs/grappes.md) sont un autre objet que le format fichiers commun.gguf + cluster-XX.gguf.

### 🤖 Assistant

⏵ Addendum reçu du sous-agent clusters ; je le transmets au parent

- **send_message** `{"message": "ADDENDUM au rapport « distribution / exploitation hétérogène » (4 précisions, aucune correction du corps du rapport) :\n\n1. **Plages de couches mesurées, au-delà de V4.1** : `reports/rapport-phase3-reparti.md:42-53` — pilote 0..12 / nœud 12..24 sur Qwen2.5-0.5B ctx 256 : locale = répar … [1759 caractères tronqués]`

  ```
message delivered to agent d31b3d9b-58e4-4d34-85fa-381b6f6a6a76
  ```

### 👤 Utilisateur

Background subagent d04ed7a2-0988-4dfd-83c5-644695dc2f8f finished and will do no further work unless you send it more.
Its closing message:
⏵ Condensé consolidé — clusters et plages de couches (lecture seule, rien modifié)

**1) Tableau** — état : P = vérifié par une porte, M = mesuré localement (rapport/REPRISE), D = déduit du code.

| capacité | ce qu'elle fait | fichier source | état | chiffre mesuré |
|---|---|---|---|---|
| Lecteur clusters + mmap | commun.gguf + cluster-XX.gguf réunis en un `Gguf` ; experts sous `cl{c}/` ; `mapping.tsv` lu d'un bloc ; fichiers mappés | `clusters.rs:150-297` · `gguf.rs:153-170, 478-520` | P (porte 1 : 6 tests `clusters.rs:309-505` ; porte 3) | 9 fichiers · 1 587 tenseurs · 18,55 Go ; mmap 9,32 s / 6,35 Go contre 30,68 s / 19,20 Go |
| Nœud partiel | `DRAVE_CLUSTERS=0,3` ; demandé-absent = erreur ; incomplet refusé sans `DRAVE_CLUSTERS` | `clusters.rs:167-176, 239-273, 291-295` | M | 1 cl. 2,35 Go / 268 786,62 · 4 cl. 4,60 Go / 3 378,91 · 8 cl. 6,28 Go / 799,8557 |
| Porte clusters | dossier complet Qwen3-30B 8 clusters, mêmes jetons | `tools/portes.sh:55-61` | P (799,8557 revérifié au bit près après le correctif de routage : `rapport-routage-experts.md:65-77`) | attendu 799.8557 |
| Convertisseur experts | GGUF → commun + 8 clusters + `mapping.tsv` + `manifeste.json`, copie d'octets sans requantification | `convertir_clusters.py:402-582` | M | Qwen3-30B : 435+8×144 = 1 587 tenseurs · 18,60 Go · 351,7 s · SHA-256 « TOUT CONCORDE » ; V4-Flash : 86,9 Go, 11 008 entrées, 450 s, 8 430,2968 = 8 430,2968 (39,9 s contre 111,8 s, 2,8×) |
| Conversion par plages de couches | `--mode couches` : blocs `blk.N` en groupes contigus (dense), sans `mapping.tsv` | `convertir_clusters.py:446-463, 520-529` | M | Qwen2.5-0.5B : commun + 4 fichiers × 6 couches · 290 tenseurs |
| Plage de couches moteur | `couche_debut..couche_fin` = [a,b) exécutée ; hors plage → flux brut | `model.rs:2551-2569, 4368-4369, 6641-6646, 6904-6905` | M (V4.1 + phase 3), aucune porte dans `portes.sh` | V4.1 : 0,00e0, 1 743 713,6243 (51,3 s / 68,0 s) ; phase 3 : 144,8289 = 144,8289, 0,00e0, 1 023 flux, 9,5146 |
| Porte de plage K3 | `--k3-essai --couches 0:13 / 13:26 / 0:26` ; coupe après la banque de la couche 12 | `tools/test-plage-k3.sh:1-36` · `main.rs:147, 2131-2134, 2144` | porte TENUE mais NON câblée dans `portes.sh` | B et C identiques au bit · 4 jetons · 28 672 octets |
| Réparti pilote/pair | `--couches-locales N` : local [0,N), pair [N,n_layer), plage dans l'en-tête | `main.rs:3345, 3430, 3457-3460, 3549, 3204-3213` | M | écart 0,00e0 dense (`REPRISE.md:1307-1316`) |
| Outils d'analyse | co-activation/ventilation MoE, union d'experts lus, jumeaux statiques, localité (R²) | `clusters_moe.py` · `analyse_union_experts.py` · `analyse_experts_statique.py` · `localite_couches.py` | M hors moteur | couverture 0,799/0,607/0,442 ; hasard 0,440/0,319/0,250 |

**2) Ce que le format change / reste à faire**
- Fichiers : commun + N clusters + `mapping.tsv` + `manifeste.json` ; source 18,56 Go → commun 1,00 Go + cluster 2,20 Go ; surcoût = métadonnées dupliquées 8×~4 Mo = 0,2 % (`docs/format-clusters.md:80-89`).
- Partagé : routeur `ffn_gate_inp` (`clusters.rs:9-11`) ; expert partagé `ffn_*_shexp` (2D, ne matche pas « _exps. ») → `convertir_clusters.py:428`, `model.rs:695-713`. Biais d'experts + clusters = **refusé par panic** (`model.rs:791-796`).
- Jointure : TSV 4 colonnes, 6 144 lignes pour 48×128 (`rapport-lecteur-multifichiers.md:240`) ; `local[couche][global]=cluster×65536+ligne` (`clusters.rs:103`), publié en `OnceLock` après ouverture réussie (`clusters.rs:291-295`) ; `Moe::ou` traduit puis cherche le n° parmi les vues chargées (`model.rs:1299-1311`) ; les 3 projections doivent porter les mêmes clusters (`model.rs:717-731`).
- À faire : sommer les contributions entre nœuds (`docs/format-clusters.md:175-178`) ; découper les biais ; équilibrer par charge (`:187-189`) ; manifeste binaire si un fichier par expert (`:185-186`).

**3) Sémantique exacte**
- `--couches a:b` : `main.rs:706-712` — exige « a:b » (sinon panic), `a`/`b` en `usize` par `parse().unwrap()` ; **aucun contrôle de bornes**. Report `model.rs:4368-4369` : `couche_debut=a`, `couche_fin=b` ; doc « dernière couche PORTÉE (exclue) » (`:2551-2554`) → **[a,b)** ; boucles `for l in couche_debut..couche_fin` (`model.rs:6904`, aussi 4751, 5345, 6562). a inclus, b exclu.
- `b == n_layer` → norme finale + tête (`model.rs:6641-6646`) ; `b < n_layer` → flux brut (`:5740, 7745-7752`), sauf `--tete-partielle` (modèle TRONQUÉ, annoncé, `main.rs:423-435`).
- Refus : `a>=b` et `b>n_layer` **ne sont pas refusés** par le moteur principal — `a>=b` = boucle vide silencieuse ; `b>n_layer` = `layers[l]` indexé directement (`model.rs:6905`) → panique d'index. Gardes existants : `--k3-essai` (`main.rs:2131-2134`, « plage {debut}:{fin} invalide pour {n} couche(s) ») et le serveur de flux (`main.rs:3210-3213`, flux refusé, nœud vivant).
- Reprise à `a>0` sans flux : V4.1 avertit « convention de sonde, copie 0 » (`model.rs:6791-6800`) ou assert si flux brut sans `pre` (`:6787-6790`) ; un manque d'architecture n'est retiré que dans [a,b) (`:3485-3500`).
- `--plage` **n'existe pas** comme option CLI (grep `"--plage"` = 0) ; c'est le concept, `--k3-essai` réutilise `opt.couches` (`main.rs:147, 1899`).
- `--couches-locales N` : `main.rs:705`, défaut 12 si 0 (`:3345`) ; pilote `couche_fin=N`, `couche_debut` reste 0 (`:3430`) → [0,N) ; l'en-tête porte `debut=N, fin=n_layer` (`:3457-3460, 3549`) → pair exécute [N,n_layer), revalidé (`:3210`). Aucun contrôle `N ≤ n_layer` (D).

**4) Mesuré / déduit / supposé**
- Mesuré et gardé : 799,8557 (porte 3, dossier complet, ctx 64, 8 ids → 7 jetons ; inchangée après le correctif de routage, épisode transitoire 799,8152 dû à `x/s` au lieu de `x*(1/s)`, `rapport-routage-experts.md:65-77`) ; 6 tests unitaires `clusters.rs` via la porte 1 (`portes.sh:32-44`). **Aucune porte dans `portes.sh`** ne couvre `DRAVE_CLUSTERS`, `--couches a:b` ni `--couches-locales` ; la porte de plage K3 (`tools/test-plage-k3.sh`) est un script séparé.
- Mesuré une fois, non gardé : nœud partiel 1/2/4/8 clusters (`rapport-lecteur-multifichiers.md:199-204`) ; 15,2789 = 15,2789 sur 63 jetons (`docs/format-clusters.md:116`) ; V4-Flash éclaté = 8 430,2968 (`rapport-v4-reparti.md:55-70`) ; phase 3 répartie 0,00e0 (`rapport-phase3-reparti.md:42-53`) ; conversion, mmap, mesures Python.
- Déduit du code, non mesuré : absence de refus pour `a>=b`, `b>n_layer`, `N>n_layer` ; boucle vide silencieuse.
- Supposé / à faire : « la somme inter-nœuds rendrait 799,8557 pour 4,60 Go par nœud » est un calcul, pas une mesure (`rapport-lecteur-multifichiers.md:209-210`) ; biais refusés ; équilibrage par charge non fait ; loi `octets(T)=79,0+31,9·T` Gio et projections 3/11 nœuds (`rapport-passe-k3-disque.md:457-467`) = extrapolation sur bande disque.
- Aucun `reports/*cluster*` : les rapports réels sont `rapport-lecteur-multifichiers.md`, `rapport-decoupage-moe.md` (clusters d'experts), `rapport-decoupage-v41.md`, `decoupage-v41-digest.txt`, `rapport-phase3-reparti.md` et `rapport-passe-k3-disque.md` (plages de couches). Les homonymes « grappes » (neurones/co-activation) sont un autre objet.

### 🤖 Assistant

⏵ Inventaire terminé : rapport et addendum transmis au parent

Mission terminée. Livrables envoyés à `d31b3d9b-58e4-4d34-85fa-381b6f6a6a76` : le rapport complet (≤150 lignes, tableau par capacité, portes, manques, limites mesurées) puis un addendum issu du dernier sous-agent.

**Complément (addendum) — 4 points qui s'ajoutent au rapport, sans le corriger :**
1. **Plages de couches mesurées au-delà de V4.1** : `reports/rapport-phase3-reparti.md:42-53` (0..12 / 12..24 sur Qwen2.5-0.5B : 144,8289 = 144,8289, 0,00e0, 1 023 flux, 9,5146 à 1 024 jetons) et `reports/rapport-passe-k3-disque.md:409-467` (Kimi-K3 coupé couche 13 : B et C **identiques au bit**, 4 jetons, relais de **28 672 octets**).
2. `tools/test-plage-k3.sh:1-36` **est** la porte du découpage K3, mais elle **n'est pas câblée** dans `tools/portes.sh` (0 occurrence de « plage ») — les seules portes liées restent n°1 (`cargo test` ≥48) et n°3 (clusters, 799.8557).
3. **Second artefact clusters** : V4-Flash 86,9 Go → commun + 8 clusters, 11 008 entrées de mapping (43 × 256), 450 s ; 8 430,2968 en 39,9 s contre 111,8 s, soit **2,8×** (`rapport-v4-reparti.md:55-70`) ; `--ppl-reparti` sur le même : 0,00e0.
4. **Sensibilité de la porte clusters** : passage transitoire à 799,8152 (−0,005 %, `x/s` au lieu de `x*(1/s)`) puis retour à **799.8557 au bit près** (`rapport-routage-experts.md:65-77`) — la valeur attendue par `portes.sh:60` est cohérente.

Nuance de vocabulaire : aucun `reports/*cluster*` n'existe ; les documents « grappes » traitent un autre objet que le format `commun.gguf` + `cluster-XX.gguf`.

**Conclusion inchangée** : un seul découpage est à la fois juste et prouvé — 2 nœuds TCP, N plages de couches, mêmes logits au bit près — mais uniquement sur la même machine, chaque nœud chargeant le modèle entier. Les manques structurants restent le partage RAM/disque entre nœuds, la sommation inter-nœuds des experts, le branchement réseau du relais K3, toute mesure sur un vrai lien réseau, et toute porte GPU/mmap/disque. Aucun fichier n'a été modifié, aucune compilation ni test lancé.

