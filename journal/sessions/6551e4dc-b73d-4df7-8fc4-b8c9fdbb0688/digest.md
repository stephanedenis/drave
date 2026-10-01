# Session DSH — relecture

- identifiant : `6551e4dc-b73d-4df7-8fc4-b8c9fdbb0688`
- dossier : `/home/stephane/Data13TB/stephane/GitHub/Qtrinet`
- créée : 2026-10-01 11:57:27
- agent : standard


## Tour 1

### 👤 Utilisateur

Tu es un relecteur adverse. Tu ne modifies AUCUN fichier du dépôt : tu lis, tu vérifies, tu rapportes. Ton travail est de trouver ce qui est FAUX, pas de confirmer ce qui va bien. Tu peux écrire uniquement dans /tmp.

Dépôt : /home/stephane/Data13TB/stephane/GitHub/Qtrinet (moteur d'inférence GGUF en Rust, « std seul »). Les deux derniers commits (8f55e4f, b24a2e6) ont introduit :
1. un lecteur GGUF multi-fichiers (shards et clusters) ;
2. le **mmap** des fichiers au lieu de `read_to_end` ;
3. le **nœud partiel** (`DRAVE_CLUSTERS=0,3` ne charge que certains clusters) ;
4. une table de numéros de cluster `Moe::numeros` pour traduire l'identifiant du mapping en index de `Vec`.

Fichiers à examiner : `drave-core/src/gguf.rs` (surtout `Mappe`, `Tampon`, `ouvrir_tampon`, `mmap_voulu`, `tbuf`, `open_auto`, `open_meta_auto`, `open_avec_prefixes`, `open_meta_avec_prefixes`, `octets_tensor`), `drave-core/src/clusters.rs` (surtout `ouvrir_interne`, `partiel`, la variable `DRAVE_CLUSTERS`, le tri des clusters, `Mapping::lire`), `drave-core/src/model.rs` (`charger_moe`, `impl Moe`, `Moe::ou`).

Questions précises — réponds OUI/NON avec la preuve (fichier:ligne + extrait) :

1. **Sûreté du mmap.** `Mappe` utilise `mmap`/`munmap` liés en `extern "C"`. Y a-t-il un cas où la mémoire mappée est utilisée APRÈS le `munmap` (le `Drop` de `Mappe`) ? Notamment : `Gguf` est-il déplacé/cloné quelque part, et les `*const u8` rendus par `data_ptr` peuvent-ils survivre au `Gguf` ? Cherche `data_ptr`, `Vue4`, `DenseQ4::emprunter`, et tout endroit qui garde un pointeur nu.
2. **Fuite ou fuite inverse.** Si `Mappe::ouvrir` échoue en cours de route dans `open_avec_prefixes` (par ex. le 3ᵉ fichier sur 9), les `Mappe` déjà créés sont-ils bien libérés ? Que se passe-t-il si `entete_de` renvoie `None` APRÈS qu'un tampon a été mappé ?
3. **`Tampon::len`** : `Mappe` a un `len`, `Vec<u8>` aussi. La méthode `Tampon::len()` fait `(**self).len()` puis `is_empty` fait `self.len() == 0`. Est-ce correct dans tous les cas ? Le fichier de longueur 0 est-il géré (que fait `Mappe::ouvrir` avec `len == 0`, et `Deref` ensuite) ?
4. **`DRAVE_CLUSTERS`** : que se passe-t-il si la variable vaut `0,0` (doublon), `0,` (virgule finale), ` 0 ` (espaces), `-1`, `1e3`, une chaîne vide, ou un nombre plus grand que le nombre de clusters ? Chaque cas doit soit marcher, soit produire une erreur claire — jamais un résultat faux en silence.
5. **`Moe::numeros` et `Moe::ou`** : quand `local` est `None` (modèle ordinaire), `ou` rend `Some((0, e))` et `numeros` vaut `vec![0]`. Est-ce cohérent pour TOUS les appelants ? Vérifie que `moe.gate[k]`, `moe.up[k]`, `moe.down[k]` ne peuvent jamais indexer hors bornes maintenant que `k` vient d'une recherche dans `numeros`, et que `gate`/`up`/`down` ont bien la même longueur que `numeros`.
6. **Le contrôle d'exhaustivité** est désactivé quand `clusters::partiel()` est vrai. Peut-on obtenir un résultat FAUX avec `DRAVE_CLUSTERS` alors qu'on croit charger tout le modèle (par exemple `DRAVE_CLUSTERS=0,1,2,3,4,5,6,7` sur un modèle à 8 clusters, ou une valeur qui liste tous les clusters dans le désordre) ?
7. **`partiel()` est un `OnceLock<bool>`** posé dans `ouvrir_interne`. Un premier appel avec `DRAVE_CLUSTERS` puis un second sans (dans le même processus) donnerait quoi ? Est-ce atteignable depuis la ligne de commande ?
8. **Le test `dossier_de_clusters_ouvre_et_apparie`** peut-il passer alors que le code est faux ? Décris un défaut qu'il ne détecterait pas, en particulier sur le mmap ou sur `numeros`.

Tu peux exécuter en lecture seule : `grep`, `sed`, `cargo test --release` (une fois), et exécuter le binaire `drave-core/target/release/drave` sur les modèles déjà présents SI c'est utile (mais PAS sur gpt-oss-120b : une mesure est en cours dessus, ne la perturbe pas). Tu peux fabriquer des fichiers de test dans /tmp. Ne modifie rien dans le dépôt, ne lance pas `cargo build`.

Rends un rapport court et dense : pour chaque question, la réponse, la preuve (fichier:ligne), et s'il y a un défaut, sa gravité (bloquant / gênant / cosmétique) et le correctif minimal. Si tu ne trouves rien sur une question, dis-le explicitement. Ne félicite pas, ne résume pas le code.
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

⏵ Reading the repository files to audit the mmap, shard, and partial-cluster logic.

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log --oneline -5 && ls && wc -l drave-core/src/gguf.rs drave-core/src/clusters.rs drave-core/src/model.rs", "description": "Inspect repo layout and file sizes"}`

  ```
b24a2e6 mmap (3,3x plus rapide, 3x moins de mémoire) et nœud partiel (2,36 Go pour un huitième des experts)
8f55e4f Clusters exécutables : origine 15,2789 = clusters 15,2789, et les défauts trouvés en chemin
3eb0af7 Un modèle éclaté se lit comme un seul : lecteur multi-fichiers, shards et clusters
7c1b9ff Convertisseur GGUF → modèle éclaté en clusters : un fichier par cluster, vérifié par empreintes
aea1b10 Politique de stockage : la bibliothèque brute sur le mécanique, le NVMe pour nos artefacts (mesures à l'appui)
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
  1504 drave-core/src/gguf.rs
   406 drave-core/src/clusters.rs
  4321 drave-core/src/model.rs
  6231 total
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show --stat 8f55e4f b24a2e6 | head -60", "description": "Show last two commits stats"}`

  ```
commit 8f55e4fd83f0b5631bfa61afdaf3db3d36edddbb
Author: Stéphane <stephane@localhost>
Date:   Thu Oct 1 11:39:42 2026 -0400

    Clusters exécutables : origine 15,2789 = clusters 15,2789, et les défauts trouvés en chemin
    
    L'épreuve appariée (mêmes jetons, même contexte, chemin par jeton) rend le même
    chiffre des deux côtés : la traduction expert global -> (fichier, ligne locale)
    est juste.
    
    Défauts corrigés :
    - Le nom des tenseurs d'experts était préfixé DEUX fois (blk.0.blk.0.…) :
      charger_moe rendait None pour les 48 couches sans un mot, et le moteur tombait
      dans le chemin FFN dense. Trouvé en rendant le silence visible (un message par
      refus, un compteur au chargement).
    - Tri des clusters lexicographique : cluster-100 se rangeait avant cluster-20,
      alors que les préfixes cl{c}/ sont attribués par position. Numéro lu et
      numérotation exigée continue.
    - Le mapping était publié avant l'ouverture : un dossier refusé laissait le
      mapping d'un autre modèle. Publié après succès.
    - Vos préfixes ignorés en mode en-tête seul (3,19 Go au lieu de 18,55).
    - meta.as_ref().unwrap() paniquait quand le premier fichier n'a
… [2057 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/gguf.rs", "limit": 400}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/clusters.rs"}`

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
14: /// Fichier **mappé** en mémoire plutôt que lu.
15: ///
16: /// `read_to_end` fait deux choses coûteuses : il lit tout le fichier (18,55 Go
17: /// pour Qwen3-30B, 366 Go pour DeepSeek-V4.1-Flash) et il en garde une copie
18: /// dans le tas, en plus du cache de pages du noyau — soit deux fois la taille du
19: /// modèle en mémoire physique au premier accès.
20: ///
21: /// Le mmap ne lit rien : il rend une plage d'adresses, et le noyau lit les pages
22: /// à la demande. Un modèle qu'on inspecte coûte quelques mégaoctets ; un modèle
23: /// dont on n'utilise qu'un huitième des experts ne lit qu'un huitième des
24: //
… [17195 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/clusters.rs</path>
<type>file</type>
<content>
1: //! Format **clusters** : un fichier commun, N fichiers d'experts, un mapping.
2: //!
3: //! Le problème que ce format résout : un MoE range ses 128 experts dans trois
4: //! tenseurs 3D par couche, et un nœud qui n'en sert que 16 en lit quand même
5: //! 128 — soit 8 fois trop. Découpé, le nœud ne lit que son huitième.
6: //!
7: //! Trois pièces, et rien d'autre :
8: //!
9: //! * `commun.gguf` — tout ce qui n'est pas un expert : embeddings, attention,
10: //!   normes, ET le routeur (`ffn_gate_inp`), qui doit rester global puisque
11: //!   c'est lui qui désigne l'expert ;
12: //! * `cluster-XX.gguf` — les seuls `ffn_{gate,up,down}_exps` d'un sous-ensemble
13: //!   d'experts, aux mêmes décalages internes que dans le fichier d'origine ;
14: //! * `mapping.tsv` — pour chaque couche, où est chaque expert global.
15: //!
16: //! Le mapping est un **texte**, délibérément : le moteur est en Rust sans
17: //! dépendance, et un format binaire maison demanderait un lecteur de plus à
18: //! éprouver. Trois colonnes se lisent à l'œil, ce qui n'est pas un luxe quand
19: //!
… [19877 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/gguf.rs", "offset": 400, "limit": 400}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/gguf.rs</path>
<type>file</type>
<content>
400:                     continue;
401:                 }
402:                 tous.push(t);
403:             }
404:         }
405:         let meta = meta.ok_or_else(|| std::io::Error::new(std::io::ErrorKind::InvalidData,
406:             "aucun fichier ne porte de métadonnées (general.architecture absent partout)"))?;
407:         Ok(Gguf { meta, tensors: tous, bufs, starts })
408:     }
409: 
410:     /// Reconnaît un nom de shard `…-00002-of-00007.gguf`.
411:     ///
412:     /// Rend `(préfixe, numéro, total)`. Le numéro doit être un groupe de
413:     /// chiffres : un modèle dont le nom contiendrait « -of- » par hasard ne doit
414:     /// pas être pris pour un découpage.
415:     pub fn shard_de(nom: &str) -> Option<(String, usize, usize)> {
416:         let base = nom.strip_suffix(".gguf")?;
417:         let (avant, apres) = base.rsplit_once("-of-")?;
418:         let total: usize = apres.parse().ok()?;
419:         let (prefixe, num) = avant.rsplit_once('-')?;
420:         if num.is_empty() || !num.bytes().all(|c| c.is_ascii_digit()) { return None; }
421:       
… [19740 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"data_ptr\\|Vue4\\|emprunter\\|Q8View\\|as_ptr\\|from_raw_parts\" drave-core/src/ | head -80", "description": "Find raw pointer usages"}`

  ```
drave-core/src/list.rs:440:    pub unsafe fn emprunter_q8(base: *const u8, n_out: usize, n_in: usize,
drave-core/src/list.rs:452:            let octets = unsafe { std::slice::from_raw_parts(p, 34) };
drave-core/src/list.rs:766:        let xp = x.as_ptr();
drave-core/src/list.rs:774:            let octets = _mm_loadu_si128(q4.as_ptr().add(b * 16) as *const __m128i);
drave-core/src/list.rs:780:            let p2 = q2.as_ptr().add(o * n_bloc * 8 + b * 8);
drave-core/src/list.rs:788:            let d0 = _mm_loadu_si128(deux.as_ptr() as *const __m128i);
drave-core/src/list.rs:789:            let d1 = _mm_loadu_si128(deux.as_ptr().add(16) as *const __m128i);
drave-core/src/list.rs:808:    pub unsafe fn emprunter_q4k(base: *const u8, n_out: usize, n_in: usize,
drave-core/src/list.rs:821:    pub unsafe fn emprunter_q6k(base: *const u8, n_out: usize, n_in: usize,
drave-core/src/list.rs:838:        let xp = x.as_ptr();
drave-core/src/list.rs:850:                let sc = std::slice::from_raw_parts(p.add(192 + moitie * 8), 8);
drave-core/src/list.rs:907:        let xp = x.as_ptr();
drave-core/src/list.rs:913:            let sc = std::slice::from_raw_parts(p.add(4), 12);
drave-core/src/list.rs:
… [7137 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"data_ptr\\|Vue4\\|numeros\\|struct Moe\\|impl Moe\\|charger_moe\" drave-core/src/*.rs | head -60", "description": "Locate Moe and numeros usages"}`

  ```
drave-core/src/clusters.rs:348:        // gagnerait. `charger_moe` lit le publié, mais il ne s'exécute que dans
drave-core/src/gguf.rs:915:    pub fn data_ptr(&self, name: &str) -> Option<*const u8> {
drave-core/src/main.rs:4213:    fn entete_et_version_sont_ce_que_les_numeros_disent() {
drave-core/src/model.rs:72:/// Type ggml → origine des blocs pour `Vue4`.
drave-core/src/model.rs:97:fn charger_moe(g: &Gguf, l: usize, n_expert: usize) -> Option<Moe> {
drave-core/src/model.rs:105:    let vues = |s: &str| -> Option<(Vec<usize>, Vec<Vue4>)> {
drave-core/src/model.rs:107:        let (numeros, noms): (Vec<usize>, Vec<String>) = match map {
drave-core/src/model.rs:161:            let Some(ptr) = g.data_ptr(nom) else {
drave-core/src/model.rs:165:            out.push(Vue4 { base: ptr, n_out, n_in, nb: n_in / bloc, src });
drave-core/src/model.rs:167:        Some((numeros, out))
drave-core/src/model.rs:171:    let vue_unique = |nom: &str| -> Option<Vue4> {
drave-core/src/model.rs:178:        Some(Vue4 { base: g.data_ptr(nom)?, n_out, n_in, nb: n_in / bloc, src })
drave-core/src/model.rs:180:    let (numeros, gate) = vues("ffn_gate_exps.weight")?;
drave-core/src/model.rs:183:    if num_u
… [1051 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"partiel()\\|DRAVE_CLUSTERS\\|clusters::actif\\|clusters::ouvrir\" drave-core/src/*.rs | head -60", "description": "Find partial-node usages"}`

  ```
drave-core/src/clusters.rs:130:/// Ce nœud ne porte-t-il qu'une PARTIE des clusters (`DRAVE_CLUSTERS`) ?
drave-core/src/clusters.rs:138:pub fn partiel() -> bool { PARTIEL.get().copied().unwrap_or(false) }
drave-core/src/clusters.rs:197:    // Un nœud peut ne porter qu'une PARTIE des clusters (`DRAVE_CLUSTERS=0,3`) :
drave-core/src/clusters.rs:201:    let gardes: Option<Vec<usize>> = match std::env::var("DRAVE_CLUSTERS") {
drave-core/src/clusters.rs:205:                format!("DRAVE_CLUSTERS : « {x} » n'est pas un numéro de cluster"))))
drave-core/src/clusters.rs:215:                        format!("DRAVE_CLUSTERS : cluster {c} hors bornes ({} au total)",
drave-core/src/clusters.rs:230:            "DRAVE_CLUSTERS ne retient aucun cluster"));
drave-core/src/gguf.rs:479:            return Ok(crate::clusters::ouvrir(p)?.gguf);
drave-core/src/gguf.rs:489:            return Ok(crate::clusters::ouvrir_meta(p)?.gguf);
drave-core/src/model.rs:89:    crate::clusters::actif()
drave-core/src/model.rs:191:        if !crate::clusters::partiel() && gate.len() != m.n_clusters {
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs", "limit": 300, "offset": 60}`
- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/gguf.rs", "limit": 120, "offset": 860}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs</path>
<type>file</type>
<content>
60: /// `m` = listes d'événements (architecture du projet) ;
61: /// `d` = matrice dense int8 (référence de comparaison, sans événements).
62: pub struct Proj {
63:     /// Copie GPU des poids (sources Q8_0), si le déport est actif.
64:     pub gpu: Option<crate::gpu::MatriceGpu>,
65:     pub m: Option<PushMat>,
66:     pub d: Option<DenseQ8>,
67:     /// Variante 4 bits de la forme dense (0,5 octet/poids). Exclusif de `d`.
68:     pub q4: Option<DenseQ4>,
69:     pub bias: Option<Vec<f32>>,
70: }
71: 
72: /// Type ggml → origine des blocs pour `Vue4`.
73: fn source_de(t: u32) -> Option<crate::list::Source> {
74:     use crate::gguf::{GGML_MXFP4, GGML_Q4_0, GGML_Q4_K, GGML_Q6_K};
75:     use crate::list::Source;
76:     match t {
77:         GGML_Q4_K => Some(Source::Q4_K),
78:         GGML_Q6_K => Some(Source::Q6_K),
79:         GGML_MXFP4 => Some(Source::Mxfp4),
80:         GGML_Q4_0 => Some(Source::Q4_0),
81:         _ => None,
82:     }
83: }
84: 
85: /// Le mapping global → local, quand le modèle est en clusters. Un modèle
86: /// ordinaire n'en a pas : `None`, et l
… [14491 caractères tronqués]
  ```


  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/gguf.rs</path>
<type>file</type>
<content>
860:                     let qh = &buf[p + 128..p + 192];
861:                     let sc = &buf[p + 192..p + 208];
862:                     let d = Self::f16_to_f32(u16::from_le_bytes(buf[p+208..p+210].try_into().unwrap()));
863:                     for moitie in 0..2 {
864:                         let (ql, qh, sc) = (&ql[moitie*64..], &qh[moitie*32..], &sc[moitie*8..]);
865:                         let mut tmp = [0f32; 128];
866:                         for l in 0..32 {
867:                             let is = l / 16;
868:                             let q1 = ((ql[l] & 0x0F) | ((qh[l] & 3) << 4)) as i16 - 32;
869:                             let q2 = ((ql[l + 32] & 0x0F) | (((qh[l] >> 2) & 3) << 4)) as i16 - 32;
870:                             let q3 = ((ql[l] >> 4) | (((qh[l] >> 4) & 3) << 4)) as i16 - 32;
871:                             let q4 = ((ql[l + 32] >> 4) | (((qh[l] >> 6) & 3) << 4)) as i16 - 32;
872:                             let s = |k: usize| d * (sc[is + k] as i8) as f32;
873:                             tmp[l] = s(0) * q1 as f32;
874:               
… [5240 caractères tronqués]
  ```

