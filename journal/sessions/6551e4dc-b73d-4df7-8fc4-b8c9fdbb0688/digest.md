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

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"Box::leak\\|leak(\\|static ref\\|OnceLock<.*Gguf\\|OnceLock<.*Model\\|OnceLock<.*Moe\" drave-core/src/*.rs | head -40; echo ---; grep -rn \"gguf\" drave-core/src/model.rs | head -40", "description": "Find Gguf ownership ho … [7 caractères tronqués]`

  ```
---
17:use crate::gguf::Gguf;
74:    use crate::gguf::{GGML_MXFP4, GGML_Q4_0, GGML_Q4_K, GGML_Q6_K};
159:            let bloc = if t.ttype == crate::gguf::GGML_Q4_K || t.ttype == crate::gguf::GGML_Q6_K { 256 } else { 32 };
176:        let bloc = if t.ttype == crate::gguf::GGML_Q4_K || t.ttype == crate::gguf::GGML_Q6_K { 256 } else { 32 };
252:            Q4_K => crate::gguf::TAILLE_Q4K,
253:            Q6_K => crate::gguf::TAILLE_Q6K,
302:    /// un modèle en clusters en a une par `cluster-XX.gguf`, chacune ne
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"\\.ou(\\|numeros\" drave-core/src/model.rs drave-core/src/main.rs | head -60", "description": "Find Moe::ou callers"}`

  ```
drave-core/src/model.rs:107:        let (numeros, noms): (Vec<usize>, Vec<String>) = match map {
drave-core/src/model.rs:167:        Some((numeros, out))
drave-core/src/model.rs:180:    let (numeros, gate) = vues("ffn_gate_exps.weight")?;
drave-core/src/model.rs:183:    if num_up != numeros || num_down != numeros {
drave-core/src/model.rs:185:clusters ({numeros:?}, {num_up:?}, {num_down:?})");
drave-core/src/model.rs:232:        couche: l, numeros, n_expert_global: n_expert, local: map,
drave-core/src/model.rs:313:    pub numeros: Vec<usize>,
drave-core/src/model.rs:331:                let (cluster, ligne) = m.ou(self.couche, e)?;
drave-core/src/model.rs:335:                let k = self.numeros.iter().position(|c| *c == cluster)?;
drave-core/src/model.rs:2937:                    let Some((k, loc)) = moe.ou(e) else { continue; };
drave-core/src/model.rs:3745:                    let Some((kexp, loc)) = moe.ou(e as usize) else { continue; };
drave-core/src/main.rs:4213:    fn entete_et_version_sont_ce_que_les_numeros_disent() {
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"pub struct \\|pub fn \\|^fn \" drave-core/src/model.rs | sed -n '1,80p'", "description": "List model.rs top-level items"}`

  ```
25:pub struct Cfg {
62:pub struct Proj {
73:fn source_de(t: u32) -> Option<crate::list::Source> {
88:fn clusters_actifs() -> Option<&'static crate::clusters::Mapping> {
97:fn charger_moe(g: &Gguf, l: usize, n_expert: usize) -> Option<Moe> {
240:pub struct Vue4 {
289:pub struct Moe {
327:    pub fn ou(&self, e: usize) -> Option<(usize, usize)> {
342:pub struct Layer {
366:pub struct Stats {
382:fn prune_rows(w: &mut [f32], n_out: usize, n_in: usize, keep: f32) {
399:fn prune_structured(w: &mut [f32], n_out: usize, n_in: usize, keep: f32) {
422:fn construire_q8(w: &[f32], n_out: usize, n_in: usize) -> DenseQ8 {
433:    pub fn vide() -> Self {
534:pub struct CacheExperts {
549:    pub fn nouveau(budget: usize) -> Self {
554:    pub fn taux(&self) -> f64 {
599:pub struct Mla {
618:fn matvec_f32(w: &[f32], x: &[f32], n_in: usize, n_out: usize, y: &mut [f32]) {
630:pub fn f16_depuis_f32(x: f32) -> u16 {
643:pub fn f32_depuis_f16(h: u16) -> f32 {
662:pub struct TraceFlux {
678:    pub fn nouveau(chemin: &str, couches: Vec<usize>, hidden: usize, n_layer: usize)
704:    pub fn ecrire(&mut self, couche: usize, pos: usize, actifs: &[i32], echelle: f32) {
789:    pub fn terminer(&mut self) {
8
… [2547 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs", "limit": 80, "offset": 2900}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs</path>
<type>file</type>
<content>
2900:                         for v in sc_e.iter_mut() { *v = (*v - mx).exp(); somme += *v; }
2901:                         if somme > 0.0 { for v in sc_e.iter_mut() { *v /= somme; } }
2902:                         if k < ne {
2903:                             idx.select_nth_unstable_by(k, |&a, &b| {
2904:                                 sc_e[b as usize].partial_cmp(&sc_e[a as usize]).unwrap()
2905:                             });
2906:                             idx.truncate(k);
2907:                         }
2908:                         let somme_k: f32 = idx.iter().map(|&e| sc_e[e as usize]).sum();
2909:                         inv_k = if somme_k > 0.0 { 1.0 / somme_k } else { 0.0 };
2910:                     }
2911:                     if trace_active {
2912:                         use std::io::Write;
2913:                         let mut ids: Vec<u32> = idx.clone();
2914:                         ids.sort_unstable();
2915:                         let liste: Vec<String> = ids.iter().map(|e| e.to_string()).collect();
2916:                         let f = self.trace
… [3994 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs", "limit": 80, "offset": 1531}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs</path>
<type>file</type>
<content>
1531:     pub fn load(path: &str, ctx: usize, n_threads: usize, dense: bool, keep: f32,
1532:                 auto: bool, q4: u8, b6: u8) -> Model {
1533:         let t0 = Instant::now();
1534:         let g = Gguf::open_auto(path).expect("ouverture du GGUF");
1535:         let cfg = Cfg {
1536:             n_layer: g.cfg("block_count").and_then(|m| m.as_u64()).unwrap_or(0) as usize,
1537:             hidden: g.cfg("embedding_length").and_then(|m| m.as_u64()).unwrap_or(0) as usize,
1538:             n_head: g.cfg("attention.head_count").and_then(|m| m.as_u64()).unwrap_or(0) as usize,
1539:             n_kv_head: g.cfg("attention.head_count_kv").and_then(|m| m.as_u64()).unwrap_or(0) as usize,
1540:             ffn: g.cfg("feed_forward_length").and_then(|m| m.as_u64()).unwrap_or(0) as usize,
1541:             eps: g.cfg("attention.layer_norm_rms_epsilon").and_then(|m| m.as_f64()).unwrap_or(1e-6) as f32,
1542:             rope_base: g.cfg("rope.freq_base").and_then(|m| m.as_f64()).unwrap_or(10000.0) as f32,
1543:             // `attention.key_length` donne la dimension de t
… [5157 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"Gguf\\|gguf\" drave-core/src/main.rs | head -50", "description": "Find Gguf usage in main.rs"}`

  ```
4://!   drave-core <modele.gguf> [--matrix blk.0.ffn_gate.weight] [--threads 8]
13:mod gguf;
20:use gguf::Gguf;
31:        eprintln!("usage: drave-core <modele.gguf> [--matrix NOM] [--threads N]");
32:        eprintln!("       drave-core <modele.gguf> --infer (--ids 1,2,3 | --prompt TEXTE)");
99:    let g = Gguf::open_auto(path).expect("ouverture du GGUF");
976:fn meta_strings(g: &Gguf, key: &str) -> Vec<String> {
978:        Some(gguf::Meta::Array(a)) => a.iter().map(|m| m.as_str().unwrap_or("").to_string()).collect(),
983:fn meta_ints(g: &Gguf, key: &str) -> Vec<i32> {
985:        Some(gguf::Meta::Array(a)) => a.iter().map(|m| m.as_u64().unwrap_or(0) as i32).collect(),
990:fn build_tokenizer(g: &Gguf) -> tokenizer::Tokenizer {
1007:    let g = Gguf::open_meta_auto(path).ok()?;
1041:    let g = Gguf::open_auto(path).expect("ouverture du GGUF");
1342:    // `DRAVE_VISION_TEXTE=<modele.gguf>` charge le modèle de texte et lui impose le
1380:    let g = Gguf::open_meta_auto(path).expect("ouverture de l'en-tête GGUF");
1391:            octets[t.fichier] += Gguf::octets_tensor(t);
1413:                 Gguf::nom_type(t.ttype), t.name, t.dims, poids as f64 / 1e6, t.fichier);
2417:    let
… [604 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/Google 2>/dev/null; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"g\\b\" drave-core/src/model.rs | sed -n '1,10p'; echo \"=== around 1660-1720 ===\"; sed -n '1655,1720p' drave-core/src/model.rs", "description": "Inspect Model::load c … [13 caractères tronqués]`

  ```
25:pub struct Cfg {
41:    /// `g·σ(1,702·g)·(u+1)`, avec `g` et `u` écrêtés à ±7 — une sigmoïde
85:/// Le mapping global → local, quand le modèle est en clusters. Un modèle
88:fn clusters_actifs() -> Option<&'static crate::clusters::Mapping> {
97:fn charger_moe(g: &Gguf, l: usize, n_expert: usize) -> Option<Moe> {
107:        let (numeros, noms): (Vec<usize>, Vec<String>) = match map {
108:            // Un mapping actif prime sur le nom en clair : si les deux existent,
111:            None if g.tensor(&base).is_some() => (vec![0], vec![base.clone()]),
120:                // `mapping.tsv` continue de désigner le bon fichier.
121:                let v: Vec<(usize, String)> = (0..m.n_clusters)
=== around 1660-1720 ===
                // FFN ; c'est le même tenseur sous un autre nom.
                ffn_norm: if g.tensor(&p("ffn_norm.weight")).is_some() {
                    g.dequant(&p("ffn_norm.weight"))
                } else {
                    g.dequant(&p("post_attention_norm.weight"))
                },
                q_norm: if g.tensor(&p("attn_q_norm.weight")).is_some() {
                    Some(g.dequant(&p("attn_q_norm.weight"))) } else { None },
                k_no
… [3855 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs", "limit": 60, "offset": 935}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs</path>
<type>file</type>
<content>
935: pub struct Model {
936:     pub g: Gguf,
937:     pub cfg: Cfg,
938:     pub layers: Vec<Layer>,
939:     pub out_norm: Vec<f32>,
940:     pub pool: Pool,
941:     /// cache KV, par couche : `[n_kv_head × ctx × head_dim]`, en f32 ou quantifié
942:     /// Caches KV, un par couche (pub : le tableau de bord `--options-actives`
943:     /// montre ce que le moteur utilise vraiment — et c'est là qu'on voit si
944:     /// `DRAVE_KV_K_F32` ou `DRAVE_KV_K_F16` a réellement pris).
945:     pub kv: Vec<KvCache>,
946:     pub ctx: usize,
947:     pub events: u64,
948:     /// Nombre de niveaux de quantification des **activations** (127 pour int8,
949:     /// 32767 pour int16). Les poids restent int8 : c'est la précision de
950:     /// l'activation qui décide de la fidélité au modèle flottant.
951:     pub act_levels: f32,
952:     /// Parcimonie **imposée** à l'inférence, sans aucun entraînement.
953:     /// `act_thresh` écarte les activations sous cette fraction du maximum du
954:     /// vecteur ; `act_topk` ne garde que les k plus grandes. Les deux imitent
955:     ///
… [2811 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show b24a2e6 --stat && git show b24a2e6 -- drave-core/src/gguf.rs | head -200", "description": "Diff of mmap commit in gguf.rs"}`

  ```
commit b24a2e6e6871a89059f3c12c0b44e59217f893bb
Author: Stéphane <stephane@localhost>
Date:   Thu Oct 1 11:56:47 2026 -0400

    mmap (3,3x plus rapide, 3x moins de mémoire) et nœud partiel (2,36 Go pour un huitième des experts)
    
    mmap : read_to_end lisait tout le fichier et en gardait une copie dans le tas, en
    plus du cache de pages — deux fois la taille du modèle. Les fichiers sont
    maintenant mappés, le noyau lit à la demande. Sur Qwen3-30B en clusters, mêmes
    7 jetons : 9,32 s et 6,35 Go contre 30,68 s et 19,20 Go, perplexité identique.
    DRAVE_MMAP=0 revient à la lecture complète.
    
    Nœud partiel : DRAVE_CLUSTERS=0,3 ne charge que ces clusters. Un nœud à un
    cluster tient en 2,36 Go (contre 6,33 Go pour le modèle entier) et la perplexité
    décroît à mesure qu'on ajoute des clusters : 268 786 -> 17 929 -> 800. La somme
    des contributions entre nœuds reste à écrire.
    
    Ce chantier a confirmé en vrai un défaut prédit par la revue adverse :
    l'identifiant de cluster du mapping servait d'index direct dans le Vec des vues.
    Tant que les huit clusters étaient chargés, les deux coïncidaient et rien ne se
    voyait ; avec un seul, index out
… [9509 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show b24a2e6 -- drave-core/src/model.rs drave-core/src/clusters.rs | sed -n '1,260p'", "description": "Diff of model.rs and clusters.rs"}`

  ```
commit b24a2e6e6871a89059f3c12c0b44e59217f893bb
Author: Stéphane <stephane@localhost>
Date:   Thu Oct 1 11:56:47 2026 -0400

    mmap (3,3x plus rapide, 3x moins de mémoire) et nœud partiel (2,36 Go pour un huitième des experts)
    
    mmap : read_to_end lisait tout le fichier et en gardait une copie dans le tas, en
    plus du cache de pages — deux fois la taille du modèle. Les fichiers sont
    maintenant mappés, le noyau lit à la demande. Sur Qwen3-30B en clusters, mêmes
    7 jetons : 9,32 s et 6,35 Go contre 30,68 s et 19,20 Go, perplexité identique.
    DRAVE_MMAP=0 revient à la lecture complète.
    
    Nœud partiel : DRAVE_CLUSTERS=0,3 ne charge que ces clusters. Un nœud à un
    cluster tient en 2,36 Go (contre 6,33 Go pour le modèle entier) et la perplexité
    décroît à mesure qu'on ajoute des clusters : 268 786 -> 17 929 -> 800. La somme
    des contributions entre nœuds reste à écrire.
    
    Ce chantier a confirmé en vrai un défaut prédit par la revue adverse :
    l'identifiant de cluster du mapping servait d'index direct dans le Vec des vues.
    Tant que les huit clusters étaient chargés, les deux coïncidaient et rien ne se
    voyait ; avec un seul, index out
… [10157 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"DRAVE_VISION_TEXTE\\|Model::load(\" drave-core/src/*.rs | head -30", "description": "Find multiple model loads"}`

  ```
drave-core/src/main.rs:687:    let mut mdl = model::Model::load(path, ctx, n_threads, dense, keep, auto, q4, b6);
drave-core/src/main.rs:1342:    // `DRAVE_VISION_TEXTE=<modele.gguf>` charge le modèle de texte et lui impose le
drave-core/src/main.rs:1351:        let chemin = std::env::var("DRAVE_VISION_TEXTE").unwrap_or_default();
drave-core/src/main.rs:1353:            let mut mdl = model::Model::load(&chemin, 512, 16, true, 1.0, false, 0, 0);
drave-core/src/main.rs:2030:    let mut mdl = model::Model::load(&chemin, ctx, fils(&opt), true, opt.keep, false, 0, 0);
drave-core/src/main.rs:2162:    let mut mdl = model::Model::load(&chemin, ctx, fils(&opt), true, opt.keep, false, 0, 0);
drave-core/src/main.rs:2998:    let mut mdl = model::Model::load(path, 4096, fils(&opt), opt.dense, opt.keep, false, 0, 0);
drave-core/src/main.rs:3874:    let mut mdl = model::Model::load(path, ctx, n_threads, dense, keep, auto, q4, b6);
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"mem::replace\\|mem::take\\|\\.g =\\|drop(g\\|drop(self.g\\|take()\" drave-core/src/model.rs drave-core/src/main.rs | head -30", "description": "Find Gguf replacement or drop"}`

  ```
drave-core/src/model.rs:2532:        let impose = self.emb_imposee_lot.take();
drave-core/src/model.rs:3233:        let mut x = match emb_imposee.take() {
drave-core/src/model.rs:3819:                    let mut seuil = std::mem::take(&mut scratch);
drave-core/src/model.rs:3902:        if let Some(d) = self.head4.take() {
drave-core/src/model.rs:4065:            let d = self.head4.take().unwrap();
drave-core/src/main.rs:3799:            fenetres.push((std::mem::take(&mut cur), std::mem::take(&mut masque)));
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs", "limit": 80, "offset": 1330}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
1330:             }
1331:             for v in w0.iter().chain(b0.iter()).chain(w2.iter()).chain(b2.iter()) {
1332:                 f2.write_all(&v.to_le_bytes()).unwrap();
1333:             }
1334:         }
1335:         println!("projecteur : {n_groupe} groupes × {n2} valeurs, |sortie| = {:.4}, 4 premières {:?}",
1336:                  y.iter().map(|v| v * v).sum::<f32>().sqrt(),
1337:                  &y[..4].iter().map(|v| (v * 1e4).round() / 1e4).collect::<Vec<_>>());
1338:         proj = Some((Vec::new(), y));
1339:     }
1340: 
1341:     // ---- Injection : le moteur consomme-t-il un embedding d'image ?
1342:     // `DRAVE_VISION_TEXTE=<modele.gguf>` charge le modèle de texte et lui impose le
1343:     // PREMIER jeton d'image via `Model::emb_imposee` — le chemin qui manquait
1344:     // (« forward partait toujours de token_embd »). C'est un contrôle de
1345:     // PLOMBERIE : le moteur ne panique pas, il rend des logits d'échelle
1346:     // normale. La qualité, elle, demanderait la comparaison complète.
1347:     if let Some((_, y)) = proj.as_ref() {
1348:   
… [3620 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '660,700p' drave-core/src/main.rs", "description": "Inspect run path around Model::load"}`

  ```
{:.2} Go montés sur le bus, {:.2} Go résidents",
                 c.demandes, c.manques, c.taux(), c.evictions,
                 c.octets_envoyes as f64 / 1e9, c.octets as f64 / 1e9);
    }
}

fn run_infer(opt: Options) {
    // Lu AVANT la déstructuration, qui consomme `opt`.
    let montre_options = opt.options_actives;
    // Une seule analyse de la ligne de commande (voir `analyser`) : chaque mode
    // ne fait plus que déstructurer ce dont il a besoin.
    let Options {
        ids: mut ids, ids_file, prompt, n: n_new, temp, top_p, topk, rep_pen, hist,
        flux, session, chat, ctx: ctx_opt, threads: threads_opt, abits: abits_opt,
        ctx_impose, threads_impose, abits_impose, dense, auto, q4, b6,
        keep, attn_window, swa_pattern, sans_fenetre, attn_sinks, attn_topk, qk_topk,
        act_thresh, act_topk, act_renorm, topk_proj, moe_topk, patch: patch_file,
        hebb_layer, hebb_q, hebb_out, sans_yarn, lot, ffn_gain,
        trace_flux, trace_couches, flux_forcer, ..
    } = opt;
    let path = &modele_chemin();
    // Défauts du mode INFÉRENCE : 512 jetons, la moitié des cœurs (l'attente
    // active de la barrière ne tolère pas la sursouscription), 8 bits.
  
… [969 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"^fn \\|^pub fn \" drave-core/src/main.rs | awk -F: '$1>1100 && $1<1400' | head; echo ===; sed -n '1150,1230p' drave-core/src/main.rs", "description": "Inspect vision mode model opens"}`

  ```
1374:fn run_tensors() {
===
            let bu = g.dequant(&p("ffn_up.bias"));
            let wd = g.dequant(&p("ffn_down.weight"));
            let bd = g.dequant(&p("ffn_down.bias"));
            let nff = wg.len() / e;
            let (mut qq, mut kk, mut vv) = (Vec::new(), Vec::new(), Vec::new());
            for pi in 0..n_patch {
                norme_ln(&x[pi * e..(pi + 1) * e], &ln1, &mut xn);
                qq.extend(proj_l(&xn, &wq, &bq, e, e));
                kk.extend(proj_l(&xn, &wk, &bk, e, e));
                vv.extend(proj_l(&xn, &wv, &bv, e, e));
            }
            // Rotation 2-D (mRoPE) : quatre blocs de la dimension de tête, lus
            // dans clip.cpp — le tenseur `positions` y est rempli (ligne,
            // colonne, ligne, colonne), donc les blocs 0 et 2 tournent selon la
            // LIGNE et les blocs 1 et 3 selon la COLONNE. Chaque couple d'un
            // bloc est (i, i + quart/2), la convention « moitié tournée ».
            // Convention exacte, lue dans ggml_mrope_cache_init :
            //   * les paires sont CONSÉCUTIVES : (i0, i0+1) ;
            //   * le secteur vaut (i0/2) % sect_dims, avec quatre sections de
            /
… [3296 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"impl Drop for\" drave-core/src/*.rs; echo ===; sed -n '3230,3260p' drave-core/src/main.rs; echo === ; sed -n '3310,3340p' drave-core/src/main.rs", "description": "Check Drop impls and raw-pointer bench paths"}`

  ```
drave-core/src/engine.rs:786:impl Drop for Pool {
drave-core/src/gguf.rs:67:impl Drop for Mappe {
===
    let t = g.tensor(nom).unwrap();
    if mx {
        return banc_mxfp4(opt, &g, nom, threads);
    }
    let (blocs, nb) = g.q8_blocks(nom).expect("tête Q8_0 requise pour ce banc");
    let (n_out, n_in) = (t.dims[0] as usize, t.dims[1] as usize);
    // Taille RÉELLE des poids de la tête (`blocs` couvre la fin du fichier).
    let octets = n_out * nb * 34;
    println!("tête {nom} : {n_out} × {n_in} · {:.1} Mo · {} blocs de 32",
             octets as f64 / 1e6, nb);

    // Activations de test, quantifiées comme dans le moteur. Les noyaux de TÊTE
    // ne multiplient PAS par l'échelle d'activation (c'est `proj_q8` qui le
    // fait) : la comparaison doit donc se faire sans `sx`, sinon l'écart
    // mesuré n'est que le facteur oublié (constaté : 2,5e2).
    let xi: Vec<i32> = (0..n_in).map(|i| ((i * 2654435761usize) % 255) as i32 - 127).collect();

    // 1. CPU : le chemin de référence.
    let d = unsafe { DenseQ8::emprunter_q8(blocs.as_ptr(), n_out, n_in, nb) };
    let t0 = Instant::now();
    let mut cpu = vec![0f32; n_out];
    let chunk = n_out.div_ceil(threads);
    
… [2013 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1940,1995p' drave-core/src/model.rs", "description": "Read tail of Model::load"}`

  ```
unsafe { DenseQ4::emprunter(buf.as_ptr(), v, h, nb, true) }
            } else if let Some((buf, nb)) = g.q4_blocks(&tete) {
                unsafe { DenseQ4::emprunter(buf.as_ptr(), v, h, nb, false) }
            } else {
                DenseQ4::build(&g.dequant(&tete), v, h)
            };
            println!("[tête 4 bits] {} × {} → {:.2} b/poids, {:.0} Mo, {:.1} s",
                     v, h, d.bits_per_weight(),
                     (d.q.len() + d.sc.len()) as f64 / 1e6, t0.elapsed().as_secs_f64());
            Some(d)
        } else { None };
        Model {
            g, cfg, layers, out_norm, pool,
            kv: caches_kv,
            ctx, events: 0, act_levels: 127.0, act_thresh: 0.0, act_topk: 0, act_renorm: false,
            act_topk_proj: [0; 7], attn_topk: 0, attn_events: 0, qk_topk: 0,
            moe_topk: 0,
            profil_neurones: None,
            profil_experts: None,
            // Trace de routage des experts : c'est la matière première du
            // découpage en clusters (quels experts sont allumés ENSEMBLE). Le
            // fichier est créé (tronqué) au chargement, tamponné, et fermé avec
            // le modèle — une exécution = une trace.

… [1493 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '90,115p' drave-core/src/main.rs; echo \"=== 1030-1060\"; sed -n '1030,1060p' drave-core/src/main.rs; echo \"=== 2405-2430\"; sed -n '2405,2430p' drave-core/src/main.rs; echo \"=== 3020-3045\"; sed -n '3020,3045p' drave-core/s … [205 caractères tronqués]`

  ```
"--matrix" if i + 1 < args.len() => { matrix = args[i + 1].clone(); i += 2; }
            "--threads" if i + 1 < args.len() => {
                n_threads = args[i + 1].parse().unwrap_or(n_threads); i += 2;
            }
            _ => i += 1,
        }
    }

    let t0 = Instant::now();
    let g = Gguf::open_auto(path).expect("ouverture du GGUF");
    println!("GGUF ouvert en {:?} — {} tenseurs", t0.elapsed(), g.tensors.len());
    let arch = g.meta.get("general.architecture").and_then(|m| m.as_str()).unwrap_or("?");
    let n_layer = g.cfg("block_count").and_then(|m| m.as_u64()).unwrap_or(0);
    let hidden = g.cfg("embedding_length").and_then(|m| m.as_u64()).unwrap_or(0);
    let inter = g.cfg("feed_forward_length").and_then(|m| m.as_u64()).unwrap_or(0);
    println!("architecture : {arch} · {n_layer} couches · hidden {hidden} · intermédiaire {inter}");
    println!("threads : {n_threads}\n");

    // ---------------------------------------------------------------- tailles
    println!("=== 1. Taille exacte des encodages (mesurée sur les niveaux réels) ===");
    let mats = [
        "blk.0.ffn_gate.weight",
        "blk.0.ffn_down.weight",
        "blk.0.attn_q.weight",
   
… [6688 caractères tronqués]
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs", "limit": 70, "offset": 530}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/model.rs</path>
<type>file</type>
<content>
530: /// quart. Mais un expert SÉLECTIONNÉ est réutilisé d'un jeton à l'autre : c'est
531: /// exactement ce qu'un cache attrape. La mesure d'activation
532: /// (`reports/rapport-localite-activation.md`) dit qu'un préchargement STATIQUE
533: /// ne paie pas ; une résidence dynamique, si.
534: pub struct CacheExperts {
535:     /// Une entrée par (couche, expert) : ses trois matrices (gate, up, down).
536:     cartes: std::collections::HashMap<(usize, usize), (crate::gpu::MatriceGpu,
537:                                                        crate::gpu::MatriceGpu,
538:                                                        crate::gpu::MatriceGpu, u64)>,
539:     pub octets: usize,
540:     pub budget: usize,
541:     pub demandes: u64,
542:     pub manques: u64,
543:     pub evictions: u64,
544:     pub octets_envoyes: u64,
545:     ticks: u64,
546: }
547: 
548: impl CacheExperts {
549:     pub fn nouveau(budget: usize) -> Self {
550:         CacheExperts { cartes: std::collections::HashMap::new(), octets: 0, budget,
551:                        demandes: 0, manques: 0,
… [2707 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && ls -la models/ 2>/dev/null | head -30; echo ===; ls drave-core/target/release/ 2>/dev/null | head -20; echo ===; find models -maxdepth 2 -name \"mapping.tsv\" 2>/dev/null | head", "description": "List available models and binary"}`

  ```
total 863324
drwxr-xr-x. 1 stephane stephane        88 25 sep 17:13 .
drwxr-xr-x. 1 stephane stephane       612 30 sep 17:59 ..
-rw-r--r--. 1 stephane stephane 352972352 25 sep 17:13 Qwen2.5-0.5B-Q4_0.gguf
-rw-r--r--. 1 stephane stephane 531068480 25 sep 16:52 Qwen2.5-0.5B-Q8_0.gguf
===
build
deps
drave
drave.d
examples
incremental
qtrinet-core
qtrinet-core.d
===
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && find . -maxdepth 4 -name \"mapping.tsv\" 2>/dev/null | head; ls data 2>/dev/null | head; echo ===; grep -n '\"--tensors\"' drave-core/src/main.rs | head", "description": "Search for cluster artifacts and --tensors flag"}`

  ```
wikitext2_test.txt
wikitext2_test.txt.ids
wt2.json
===
54:        (opt.tensors, "--tensors"), (opt.banc_mla.is_some(), "--banc-mla"),
539:            "--tensors" => { o.tensors = true; 1 }
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs", "limit": 70, "offset": 25}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs</path>
<type>file</type>
<content>
25:     format!("{:8.3} b/poids  ({:7.2} Mo)", b as f64 / n as f64, b as f64 / 8.0 / 1e6)
26: }
27: 
28: fn main() {
29:     let args: Vec<String> = std::env::args().collect();
30:     if args.len() < 2 {
31:         eprintln!("usage: drave-core <modele.gguf> [--matrix NOM] [--threads N]");
32:         eprintln!("       drave-core <modele.gguf> --infer (--ids 1,2,3 | --prompt TEXTE)");
33:         eprintln!("                    [--n 32] [--temp 0] [--ctx 512] [--threads N]");
34:         std::process::exit(1);
35:     }
36:     // Une seule analyse, puis un aiguillage : `--plan`, `--tokenize`,
37:     // `--ppl`/`--ppl-texte` et `--infer` partagent désormais la même structure
38:     // d'options, donc les mêmes drapeaux.
39:     // Les variables d'environnement ont été renommées QT_* -> DRAVE_* : un
40:     // ancien nom encore présent dans un script ne ferait RIEN, en silence. On le
41:     // dit, plutôt que de laisser croire que l'option est active.
42:     if let Some((vieux, _)) = std::env::vars().find(|(k, _)| k.starts_with("QT_")) {
43:         eprintln!("[attenti
… [3117 caractères tronqués]
  ```

### 🤖 Assistant

⏵ Building synthetic GGUF cluster dirs in /tmp to exercise DRAVE_CLUSTERS with the real binary.

- **write** `{"file_path": "/tmp/revue/gen.py", "content": "import struct, os, shutil\n\ndef s(x):\n    b = x.encode()\n    return struct.pack(\"<Q\", len(b)) + b\n\ndef entete(n_tensors=0, kvs=None):\n    kvs = kvs or []\n    out = b\"GGUF\" + struct.pack(\"<I\", 3) + struct.pack(\"<Q\", n_tensors) + struct.pac … [1385 caractères tronqués]`

  ```
<path>/tmp/revue/gen.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /tmp/revue && python3 gen.py && ls ok manque && xxd ok/commun.gguf | head -3", "description": "Generate synthetic cluster directories"}`

  ```
ok
manque:
cluster-00.gguf
cluster-01.gguf
cluster-02.gguf
cluster-03.gguf
cluster-04.gguf
cluster-05.gguf
cluster-06.gguf
commun.gguf
mapping.tsv

ok:
cluster-00.gguf
cluster-01.gguf
cluster-02.gguf
cluster-03.gguf
cluster-04.gguf
cluster-05.gguf
cluster-06.gguf
cluster-07.gguf
commun.gguf
mapping.tsv
00000000: 4747 5546 0300 0000 0000 0000 0000 0000  GGUF............
00000010: 0100 0000 0000 0000 1400 0000 0000 0000  ................
00000020: 6765 6e65 7261 6c2e 6172 6368 6974 6563  general.architec
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && B=drave-core/target/release/drave; $B /tmp/revue/ok --tensors 2>&1 | head -8; echo \"exit=$?\"", "description": "Baseline run on complete synthetic cluster dir"}`

  ```
[attention] QT_IM_SWITCHER est l'ancien nom d'une variable d'environnement : elles s'appellent maintenant DRAVE_* (voir docs/histoire.md). Rien n'a été appliqué.
qwen3moe · 9 fichiers · 8 tenseurs · 0.00 Go de poids · en-têtes lus en 3.280144ms
  fichier 0 :     0 tenseurs · 0.00 Go
  fichier 1 :     1 tenseurs · 0.00 Go
  fichier 2 :     1 tenseurs · 0.00 Go
  fichier 3 :     1 tenseurs · 0.00 Go
  fichier 4 :     1 tenseurs · 0.00 Go
  fichier 5 :     1 tenseurs · 0.00 Go
exit=0
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && B=drave-core/target/release/drave\nrun() { desc=\"$1\"; val=\"$2\"; dir=\"$3\";\n  out=$(env DRAVE_CLUSTERS=\"$val\" $B \"$dir\" --tensors 2>&1); rc=$?\n  line=$(echo \"$out\" | grep -v QT_IM_SWITCHER | grep -E \"fichiers|Erreur|pani … [1052 caractères tronqués]`

  ```
--- dossier complet (8 fichiers, 8 annonces) ---
aucune             val=''                     dir=ok               rc=0  qwen3moe · 9 fichiers · 8 tenseurs · 0.00 Go de poids · en-têtes lus en 3.396173ms 
sous-ensemble      val='0,3'                  dir=ok               rc=0  qwen3moe · 3 fichiers · 2 tenseurs · 0.00 Go de poids · en-têtes lus en 1.827714ms 
doublon            val='0,0'                  dir=ok               rc=0  qwen3moe · 2 fichiers · 1 tenseurs · 0.00 Go de poids · en-têtes lus en 156.683µs 
virgule fin.       val='0,'                   dir=ok               rc=134  
espaces            val=' 0 '                  dir=ok               rc=0  qwen3moe · 2 fichiers · 1 tenseurs · 0.00 Go de poids · en-têtes lus en 261.074µs 
negatif            val='-1'                   dir=ok               rc=134  
exposant           val='1e3'                  dir=ok               rc=134  
hors bornes        val='8'                    dir=ok               rc=134  
desordre           val='3,0'                  dir=ok               rc=0  qwen3moe · 3 fichiers · 2 tenseurs · 0.00 Go de poids · en-têtes lus en 1.882543ms 
tous               val='0,1,2,3,4,5,6,7'      dir=ok            
… [811 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && B=drave-core/target/release/drave\nfor v in \"0,\" \"-1\" \"1e3\" \"8\" \"99999999999999999999\" \"1 2\" \"0x1\"; do\n  echo \"=== DRAVE_CLUSTERS='$v'\";\n  env DRAVE_CLUSTERS=\"$v\" $B /tmp/revue/ok --tensors 2>&1 | grep -v QT_IM_SW … [85 caractères tronqués]`

  ```
=== DRAVE_CLUSTERS='0,'
ouverture de l'en-tête GGUF: Custom { kind: InvalidInput, error: "DRAVE_CLUSTERS : «  » n'est pas un numéro de cluster" }
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
=== DRAVE_CLUSTERS='-1'
ouverture de l'en-tête GGUF: Custom { kind: InvalidInput, error: "DRAVE_CLUSTERS : « -1 » n'est pas un numéro de cluster" }
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
=== DRAVE_CLUSTERS='1e3'
ouverture de l'en-tête GGUF: Custom { kind: InvalidInput, error: "DRAVE_CLUSTERS : « 1e3 » n'est pas un numéro de cluster" }
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
=== DRAVE_CLUSTERS='8'
ouverture de l'en-tête GGUF: Custom { kind: InvalidInput, error: "DRAVE_CLUSTERS : cluster 8 hors bornes (8 au total)" }
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
=== DRAVE_CLUSTERS='99999999999999999999'
ouverture de l'en-tête GGUF: Custom { kind: InvalidInput, error: "DRAVE_CLUSTERS : « 99999999999999999999 » n'est pas un numéro de cluster" }
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
=== DRAVE_CLUSTERS='1 2'
ouverture de 
… [417 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core && timeout 3000 cargo test --release 2>&1 | tail -40", "description": "Run the release test suite once", "run_in_background": true, "timeoutMs": 3000000}`

  ```
started background job bash-95
  ```

- **bash** `{"command": "cd /tmp/revue && python3 - <<'EOF'\nimport gen, os, shutil\ngen.faire(\"/tmp/revue/sparse\", 0, 8, True)   # commun + mapping seulement\nfor c in [3]:\n    shutil.copy(\"/tmp/revue/ok/cluster-%02d.gguf\" % c, \"/tmp/revue/sparse/cluster-%02d.gguf\" % c)\ngen.faire(\"/tmp/revue/sparse2\" … [227 caractères tronqués]`

  ```
ok
/tmp/revue/sparse:
cluster-03.gguf
commun.gguf
mapping.tsv

/tmp/revue/sparse2:
cluster-00.gguf
cluster-03.gguf
commun.gguf
mapping.tsv
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn -i \"partiel\\|DRAVE_CLUSTERS\" README.md docs/*.md REPRISE.md 2>/dev/null | head -30", "description": "Check documented partial-node semantics"}`

  ```
README.md:286:   partielles venant de plusieurs cartes (ring), ou déterminisme du résultat. Dans ce cas,
docs/contexte-long.md:217:`(max, somme, accumulateur)` partiel par softmax **en ligne** ; le second
docs/contexte-long.md:267:2. les partiels n'étaient **pas indexés par tête KV** : les blocs d'une même
docs/convertisseur.md:298:| 4 | (1 095) | rotary partiel supposé — **hypothèse réfutée**, annulée |
docs/format-clusters.md:140:* **Le nœud partiel** : `DRAVE_CLUSTERS=0,3` ne charge que ces clusters. Mesuré
docs/plan-gpu-topk.md:28:* `drave-core/gpu/drave_gpu.cu` (956 lignes, 14 noyaux) : `attn_kv_partiels` (scores
docs/plan-gpu-topk.md:29:  et partiels par tranche, softmax en ligne), `attn_kv_recombine` (fusion des
docs/plan-gpu-topk.md:31:* `drave-core/src/gpu.rs` : `Machine::attn_kv(...)` (FFI, allocations, partiels) ;
docs/plan-gpu-topk.md:33:  partiels), le repli propre (`fait_en_gpu`) ;
docs/plan-gpu-topk.md:43:   `attn_kv_partiels` sait déjà le faire). Sortie : `sc[nh][N]` en f32.
docs/plan-gpu-topk.md:100:* **la disposition du KV** : un partiel par (tranche, tête KV, tête de requête),
docs/plan-gpu-topk.md:110:  que le CPU (partiels par tranche) — c'est déjà le cas pour 
… [984 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '720,745p' REPRISE.md; echo \"=== docs/format-clusters.md 125-160\"; sed -n '125,165p' docs/format-clusters.md", "description": "Read partial-node documentation"}`

  ```
```

# Les fichiers sont MAPPÉS : 3,3x plus rapide et 3x moins de mémoire qu'une
# lecture complète (9,32 s / 6,35 Go contre 30,68 s / 19,20 Go sur Qwen3-30B,
# perplexité identique). `DRAVE_MMAP=0` revient à la lecture complète.

# Un NŒUD PARTIEL ne charge que ses clusters : 2,36 Go pour un huitième des
# experts, contre 6,33 Go pour le modèle entier.
DRAVE_CLUSTERS=0 ./drave-core/target/release/drave \
    /home/stephane/FastNVMe/artefacts/modeles-optimises/qwen3-30b-8clusters \
    --ppl /tmp/ids_qwen.txt --ctx 64 --limit 8 --dense --threads 8 --lot 1
```

**Ouvert** : la SOMME des contributions entre nœuds (le nœud partiel saute les
experts absents, mais rien n'additionne encore ce que deux nœuds calculent) ; les
biais d'experts en clusters (gpt-oss en a, refusés explicitement) ; le
rééquilibrage des clusters par charge et non par nombre d'experts.
=== docs/format-clusters.md 125-160
 2 q4_0 32/18   10 q2_K 256/84   18 iq3_xxs 256/98   30 bf16  1/2
 3 q4_1 32/20   11 q3_K 256/110  19 iq1_s  256/50   34 tq1_0 256/54
 6 q5_0 32/22   12 q4_K 256/144  20 iq4_nl 32/18    35 tq2_0 256/66
 7 q5_1 32/24   13 q5_K 256/176  21 iq3_s  256/110
                14 q6_K 256/210  22 iq2_s  25
… [1557 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && B=drave-core/target/release/drave\nfor d in sparse sparse2; do for v in \"\" \"3\" \"0,3\"; do\n out=$(env DRAVE_CLUSTERS=\"$v\" $B /tmp/revue/$d --tensors 2>&1 | grep -v QT_IM_SWITCHER | grep -E \"fichiers|error\" | head -1)\n print … [112 caractères tronqués]`

  ```
sparse   val=''     ouverture de l'en-tête GGUF: Custom { kind: InvalidData, error: "/tmp/revue/sparse/cluster-03.gguf : cluster 0 attendu, 3 trouvé — la numérotation doit être continue à partir de 0" }
sparse   val='3'    ouverture de l'en-tête GGUF: Custom { kind: InvalidData, error: "/tmp/revue/sparse/cluster-03.gguf : cluster 0 attendu, 3 trouvé — la numérotation doit être continue à partir de 0" }
sparse   val='0,3'  ouverture de l'en-tête GGUF: Custom { kind: InvalidData, error: "/tmp/revue/sparse/cluster-03.gguf : cluster 0 attendu, 3 trouvé — la numérotation doit être continue à partir de 0" }
sparse2  val=''     ouverture de l'en-tête GGUF: Custom { kind: InvalidData, error: "/tmp/revue/sparse2/cluster-03.gguf : cluster 1 attendu, 3 trouvé — la numérotation doit être continue à partir de 0" }
sparse2  val='3'    ouverture de l'en-tête GGUF: Custom { kind: InvalidData, error: "/tmp/revue/sparse2/cluster-03.gguf : cluster 1 attendu, 3 trouvé — la numérotation doit être continue à partir de 0" }
sparse2  val='0,3'  ouverture de l'en-tête GGUF: Custom { kind: InvalidData, error: "/tmp/revue/sparse2/cluster-03.gguf : cluster 1 attendu, 3 trouvé — la numérotation doit être conti
… [20 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"moe\\.\\(gate\\|up\\|down\\|shexp\\|ou\\)\\|\\.gate\\[\\|\\.up\\[\\|\\.down\\[\" drave-core/src/model.rs | head -40", "description": "Find all expert-vector index sites"}`

  ```
2937:                    let Some((k, loc)) = moe.ou(e) else { continue; };
2944:                    let mg = moe.gate[k].expert(loc);
2953:                    let mu = moe.up[k].expert(loc);
2983:                    let md = moe.down[k].expert(loc);
3745:                    let Some((kexp, loc)) = moe.ou(e as usize) else { continue; };
3753:                    if moe.gate[0].src == crate::list::Source::Mxfp4 && moe.local.is_none() {
3757:                                                                      &moe.gate[0], &moe.up[0], &moe.down[0]) {
3771:                    let mg = moe.gate[kexp].expert(loc);
3775:                    let mu = moe.up[kexp].expert(loc);
3782:                    let md = moe.down[kexp].expert(loc);
3792:                if let Some((sg, su, sd)) = moe.shexp.as_ref() {
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '3735,3775p' drave-core/src/model.rs", "description": "Read second Moe::ou call site"}`

  ```
let mut ids: Vec<u32> = idx.clone();
                    ids.sort_unstable();       // l'ordre de `select_nth` est arbitraire
                    let liste: Vec<String> = ids.iter().map(|e| e.to_string()).collect();
                    let _ = writeln!(f, "{} {} {}", l, pos, liste.join(" "));
                }
                for v in down.iter_mut() { *v = 0.0; }
                for &e in &idx {
                    let w_exp = sc_e[e as usize] * inv_k;
                    // Traduction pour les modèles en clusters : l'expert global
                    // `e` n'est pas forcément dans ce nœud.
                    let Some((kexp, loc)) = moe.ou(e as usize) else { continue; };
                    // ---- experts MXFP4 sur le GPU ----
                    // Le noyau MXFP4 est BIT À BIT identique au chemin CPU
                    // (écart mesuré 0,00e0 sur un expert) : seule la vitesse
                    // change, la perplexité ne peut pas bouger. Les poids
                    // montent une fois et restent (cache LRU), sinon on
                    // repasserait 4,4 Mo sur le bus à chaque jeton.
                    let mut fait = false;
                    if moe.gate[0].src == crat
… [1534 caractères tronqués]
  ```

### 👤 Utilisateur

background job bash-95 (bash: cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core && timeout 3000 cargo test --release 2>&1 | tail -40) finished [status: completed, exit code: 0]. Read its output with job_output.

- **job_output** `{"job_id": "bash-95"}`

  ```
= note: `#[warn(non_shorthand_field_patterns)]` on by default

warning: `drave-core` (bin "drave" test) generated 23 warnings (run `cargo fix --bin "drave" -p drave-core --tests` to apply 13 suggestions)
    Finished `release` profile [optimized] target(s) in 8.09s
     Running unittests src/main.rs (target/release/deps/drave-9a06049b91b56c63)

running 30 tests
test clusters::tests::mapping_lu_et_traduit ... ok
test clusters::tests::mapping_partiel_est_permis ... ok
test clusters::tests::mapping_refuse_les_doublons ... ok
test clusters::tests::numerotation_des_clusters_exigee_continue ... ok
test clusters::tests::dossier_de_clusters_ouvre_et_apparie ... ok
test gguf::tests::multi_fichiers_refuse_les_doublons_divergents ... ok
test gguf::tests::multi_fichiers_egale_mono_fichier ... ok
test gguf::tests::type_inconnu_ne_compte_pas_zero_en_silence ... ok
test gguf::tests::q8_dot_at_voit_les_bons_octets ... ok
test list::tests_mxfp4::import_exact ... ok
test gguf::tests::shards_reconnus_et_rassembles ... ok
test list::tests_q4::avx2_egale_scalaire ... ok
test clusters::tests::sous_ensemble_garde_les_numeros ... ok
test list::tests_q6k::quarts_successifs ... ok
test model::tests_kv::alle
… [1154 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"sous_ensemble_garde_les_numeros\" --include=*.rs . ; echo \"=== git status\"; git status --porcelain | head -20; echo \"=== log -1\"; git log --oneline -1; echo \"=== mtime\"; ls -l --time-style=full-iso drave-core/src/clu … [166 caractères tronqués]`

  ```
./drave-core/src/clusters.rs:395:    fn sous_ensemble_garde_les_numeros() {
=== git status
 M drave-core/src/clusters.rs
 M journal/README.md
=== log -1
6a2dfcb Journal du bloc : mmap, nœud partiel, et le défaut prédit par la revue confirmé en vrai
=== mtime
-rw-------. 1 stephane stephane 22744 2026-10-01 12:01:24.613297587 -0400 drave-core/src/clusters.rs
-rw-------. 1 stephane stephane 71038 2026-10-01 11:43:22.212400075 -0400 drave-core/src/gguf.rs
-rwxr-xr-x. 1 stephane stephane 1344976 2026-10-01 12:01:40.886741018 -0400 drave-core/target/release/deps/drave-9a06049b91b56c63
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && date && git status --porcelain && git diff --stat && git diff drave-core/src/clusters.rs | head -120", "description": "Diff the dirty working tree"}`

  ```
jeu 01 oct 2026 12:02:02 EDT
 M drave-core/src/clusters.rs
 M journal/README.md
 drave-core/src/clusters.rs | 100 +++++++++++++++++++++++++++++++++++++++------
 journal/README.md          |   3 +-
 2 files changed, 90 insertions(+), 13 deletions(-)
diff --git a/drave-core/src/clusters.rs b/drave-core/src/clusters.rs
index 86b8829..df1d203 100644
--- a/drave-core/src/clusters.rs
+++ b/drave-core/src/clusters.rs
@@ -150,16 +150,42 @@ pub struct Modele {
 /// ce qui permet de réunir les N fichiers dans un seul `Gguf` sans que les noms
 /// se recouvrent.
 pub fn ouvrir(dossier: &Path) -> std::io::Result<Modele> {
-    ouvrir_interne(dossier, false)
+    let gardes = gardes_du_milieu()?;
+    ouvrir_interne(dossier, false, gardes.as_deref())
+}
+
+/// Ouvre un modèle en ne retenant QUE les clusters demandés.
+///
+/// C'est le mode « nœud partiel » : chaque nœud ne sert que ses experts. Le
+/// paramètre est explicite pour que ce chemin soit **testable** — la variable
+/// d'environnement, elle, est globale au processus et ne se prête pas à un test
+/// qui s'exécute en parallèle d'autres.
+pub fn ouvrir_sous_ensemble(dossier: &Path, clusters: Option<&[usize]>)
+    -> std::io::Result<
… [4795 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git diff drave-core/src/clusters.rs | sed -n '120,260p'", "description": "Read rest of clusters.rs working diff"}`

  ```
+        let e = match ouvrir_sous_ensemble(&d, Some(&[0, 7])) {
+            Ok(_) => panic!("un cluster hors bornes doit être refusé"),
+            Err(e) => e,
+        };
+        assert!(e.to_string().contains("cluster 7"), "{e}");
+        // Un sous-ensemble vide est refusé aussi.
+        assert!(ouvrir_sous_ensemble(&d, Some(&[])).is_err());
+        let _ = std::fs::remove_dir_all(&d);
+    }
+
     /// Un numéro de cluster manquant doit être refusé, pas renuméroté : les
     /// préfixes `cl{c}/` sont attribués par position, donc un trou décalerait
     /// tous les experts suivants sans le moindre bruit.
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -n \"mod tests\" drave-core/src/gguf.rs && sed -n '/pub mod tests/,/^}/p' drave-core/src/gguf.rs | head -80", "description": "Read gguf test helpers"}`

  ```
1226:pub(crate) mod tests {
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/gguf.rs", "limit": 100, "offset": 1226}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/gguf.rs</path>
<type>file</type>
<content>
1226: pub(crate) mod tests {
1227:     use super::*;
1228:     use std::io::Write;
1229: 
1230:     /// Fabrique un GGUF minimal : `general.architecture` plus des tenseurs F32
1231:     /// dont la valeur de chaque poids est son indice global. Un GGUF de labo,
1232:     /// écrit à la main, uniquement pour éprouver le lecteur.
1233:     pub(crate) fn gguf_synth(tensors: &[(&str, Vec<u64>)], depart: usize, valeur0: f32) -> Vec<u8> {
1234:         let mut b = Vec::new();
1235:         let mut s = |b: &mut Vec<u8>, v: &str| {
1236:             b.extend_from_slice(&(v.len() as u64).to_le_bytes());
1237:             b.extend_from_slice(v.as_bytes());
1238:         };
1239:         b.extend_from_slice(b"GGUF");
1240:         b.extend_from_slice(&3u32.to_le_bytes());
1241:         b.extend_from_slice(&(tensors.len() as u64).to_le_bytes());
1242:         b.extend_from_slice(&2u64.to_le_bytes());        // deux métadonnées
1243:         // Ordre GGUF : clef, type (u32), valeur.
1244:         s(&mut b, "general.architecture");
1245:         b.extend_from_slice(&8u32.to_le_bytes());
… [4181 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '1890,1945p' drave-core/src/model.rs; echo \"=== Proj::load\"; grep -n \"impl Proj\" drave-core/src/model.rs", "description": "Inspect head tensor borrow path"}`

  ```
let vd = per / nh - qkn;
                v.push(Mla {
                    q_a: g.dequant(&p("attn_q_a.weight")),
                    q_a_norm: g.dequant(&p("attn_q_a_norm.weight")),
                    q_b,
                    kv_a: g.dequant(&p("attn_kv_a_mqa.weight")),
                    kv_a_norm: g.dequant(&p("attn_kv_a_norm.weight")),
                    kv_b,
                    wo: g.dequant(&p("attn_output.weight")),
                    ffn_norm: g.dequant(&p("ffn_norm.weight")),
                    gate: g.dequant(&p("ffn_gate.weight")),
                    up: g.dequant(&p("ffn_up.weight")),
                    down: g.dequant(&p("ffn_down.weight")),
                    attn_norm: g.dequant(&p("attn_norm.weight")),
                    q_lora, kv_lora, qkr, qkn, vd, nh, ffn: cfg.ffn,
                });
            }
            let m0 = &v[0];
            println!("[config] MLA : {} couches · q_lora {} · kv_lora {} · qk_nope {} + qk_rope {} · v {} · \
                      cache latente {} valeurs par jeton (au lieu de {})",
                     v.len(), m0.q_lora, m0.kv_lora, m0.qkn, m0.qkr, m0.vd,
                     m0.kv_lora + m0.qkr, cfg.n_kv_head * (m0.qkn + m0.v
… [1825 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '780,800p' drave-core/src/engine.rs; echo \"=== DenseQ4 struct\"; grep -n \"pub struct DenseQ4\" -A 20 drave-core/src/list.rs | head -30", "description": "Check Pool Drop and DenseQ4 layout"}`

  ```
(out, sv.idx.len())
    }

    pub fn shutdown(self) { drop(self) }
}

impl Drop for Pool {
    fn drop(&mut self) {
        self.shared.stop.store(true, Ordering::Relaxed);
        self.shared.gen.fetch_add(1, Ordering::Release);
        for h in self.handles.drain(..) { let _ = h.join(); }
    }
}

// --------------------------------------------------------------------------- //
// Références non optimisées (comparaison)
// --------------------------------------------------------------------------- //

#[inline]
pub fn row_delta_into(lists: &SignedDelta, r: usize, xv: i64, acc: &mut [i64],
                      span: &mut (usize, usize)) -> usize {
=== DenseQ4 struct
574:pub struct DenseQ4 {
575-    pub n_in: usize,
576-    pub n_out: usize,
577-    /// Table des 16 nibbles → valeur entière signée. Par défaut `n − 8`
578-    /// (grille symétrique int4) ; l'import MXFP4 y met les magnitudes E2M1
579-    /// doublées, `±{0,1,2,3,4,6,8,12}`, qui sont exactement les valeurs du
580-    /// format une fois l'échelle ramenée à une puissance de deux.
581-    pub lut: [i8; 16],
582-    /// Vrai si `sc` porte l'octet d'exposant E8M0 du format MXFP4 au lieu
583-    /// d'une échelle relati
… [631 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && B=drave-core/target/release/drave\n: > /tmp/revue/zero.gguf\necho \"--- fichier de 0 octet (mmap)\"; $B /tmp/revue/zero.gguf --tensors 2>&1 | grep -v QT_IM | tail -1\necho \"--- fichier de 0 octet (DRAVE_MMAP=0)\"; env DRAVE_MMAP=0 $ … [499 caractères tronqués]`

  ```
--- fichier de 0 octet (mmap)
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
--- fichier de 0 octet (DRAVE_MMAP=0)
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
--- ok avec DRAVE_MMAP=0
qwen3moe · 9 fichiers · 8 tenseurs · 0.00 Go de poids · en-têtes lus en 3.257184ms
--- ok avec mmap
qwen3moe · 9 fichiers · 8 tenseurs · 0.00 Go de poids · en-têtes lus en 3.365872ms
--- manque + DRAVE_CLUSTERS=0,1,2,3,4,5,6,7 + DRAVE_MMAP=0
qwen3moe · 8 fichiers · 7 tenseurs · 0.00 Go de poids · en-têtes lus en 3.006009ms
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && B=drave-core/target/release/drave; $B /tmp/revue/zero.gguf --tensors 2>&1 | grep -v QT_IM | grep -i \"error\\|panique\" | head -2; echo \"rc=${PIPESTATUS[0]}\"", "description": "Capture zero-length file error message"}`

  ```
ouverture de l'en-tête GGUF: Custom { kind: UnexpectedEof, error: "en-tête GGUF incomplet" }
rc=134
  ```

### 🤖 Assistant

⏵ Probing the duplicate-tensor check for out-of-range offsets in sharded files.

- **write** `{"content": "import struct, os, shutil\n\ndef s(x):\n    b = x.encode(); return struct.pack(\"<Q\", len(b)) + b\n\ndef gguf(tensors, kvs):\n    out = b\"GGUF\" + struct.pack(\"<I\", 3) + struct.pack(\"<Q\", len(tensors)) + struct.pack(\"<Q\", len(kvs))\n    for k, v in kvs:\n        out += s(k) + st … [957 caractères tronqués]`

  ```
<path>/tmp/revue/shards.py</path>
<type>file</type>
<content>
Created file
</content>
  ```

- **bash** `{"command": "cd /tmp/revue && python3 shards.py && cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && B=drave-core/target/release/drave\necho \"--- shard tronque, mmap\"; $B /tmp/revue/shards/modele-00001-of-00002.gguf --plan 2>&1 | grep -v QT_IM | grep -iE \"error|panique|index|range\" | head -3 … [256 caractères tronqués]`

  ```
shard1 132 shard2 128
--- shard tronque, mmap
range start index 1073741952 out of range for slice of length 128
--- shard tronque, DRAVE_MMAP=0
range start index 1073741952 out of range for slice of length 128
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && for l in 687 1353 2030 2162 2998 3874; do f=$(awk -v L=$l 'NR<=L && /^fn |^pub fn /{n=NR; s=$0} END{print n\": \"s}' drave-core/src/main.rs); echo \"line $l -> $f\"; done; echo ===; grep -n \"fn run_serveur_flux\" -A 25 drave-core/sr … [118 caractères tronqués]`

  ```
line 687 -> 666: fn run_infer(opt: Options) {
line 1353 -> 1038: fn run_banc_vision(sortie: &str) {
line 2030 -> 2017: fn run_serveur_flux(opt: Options, adresse: &str) {
line 2162 -> 2152: fn run_ppl_reparti(opt: Options, pair: &str) {
line 2998 -> 2987: fn run_banc_mla(opt: Options, sortie: &str) {
line 3874 -> 3826: fn run_ppl(opt: Options) {
===
14:2030-    let mut mdl = model::Model::load(&chemin, ctx, fils(&opt), true, opt.keep, false, 0, 0);
21:2037-    let (mut sock, pair) = ecoute.accept().expect("connexion");
  ```

- **read** `{"file_path": "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/clusters.rs", "limit": 75, "offset": 196}`

  ```
<path>/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/clusters.rs</path>
<type>file</type>
<content>
196:     // attribués par POSITION. Un décalage ferait lire les experts d'un autre
197:     // fichier — mêmes formes, donc aucune erreur, juste un résultat faux.
198:     let mut clusters: Vec<(usize, PathBuf)> = Vec::new();
199:     for e in std::fs::read_dir(dossier)? {
200:         let p = e?.path();
201:         let n = p.file_name().and_then(|x| x.to_str()).unwrap_or("").to_string();
202:         let Some(num) = n.strip_prefix("cluster-")
203:                           .and_then(|r| r.strip_suffix(".gguf")) else { continue };
204:         let Ok(c) = num.parse::<usize>() else {
205:             return Err(std::io::Error::new(std::io::ErrorKind::InvalidData, format!(
206:                 "{} : « {n} » ne porte pas un numéro de cluster lisible", dossier.display())));
207:         };
208:         clusters.push((c, p));
209:     }
210:     clusters.sort();
211:     if clusters.is_empty() {
212:         return Err(std::io::Error::new(std::io::ErrorKind::NotFound,
213:             format!("{} : aucun cluster-*.gguf", dossier.display())));
214:     }
215:     for (atte
… [3261 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && sed -n '3895,3915p' drave-core/src/model.rs; echo ===; sed -n '4058,4080p' drave-core/src/model.rs", "description": "Check head4 take/restore path"}`

  ```
}
            if complet { return tous; }
        }
        let vocab = self.cfg.vocab;
        let nt = self.pool.threads().max(1);
        let chunk = vocab.div_ceil(nt);
        let mut out = vec![0f32; vocab * t];
        if let Some(d) = self.head4.take() {
            let dref = &d;
            let s32: Vec<Vec<i32>> = (0..t)
                .map(|i| crate::list::sommes32(&qx[i * h..(i + 1) * h])).collect();
            let (qxr, s32r, sxsr) = (&qx, &s32, &sxs);
            std::thread::scope(|sc| {
                for (ci, part) in out.chunks_mut(chunk * t).enumerate() {
                    let base = ci * chunk;
                    sc.spawn(move || {
                        for i0 in (0..t).step_by(TUILE_TETE) {
                            let i1 = (i0 + TUILE_TETE).min(t);
                            for j in 0..(part.len() / t) {
                                let o = base + j;
                                for i in i0..i1 {
===
        // écrits, remis à zéro puis réduits, soit plus de trafic que les poids
        // économisés.
        if self.head4.is_some() {
            let xi: Vec<i16> = sv.idx.iter().zip(sv.val.iter())
                .fold(vec![0i16; h.len()], 
… [813 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git show --stat 6a2dfcb | tail -8; echo \"=== fichiers de code modifies vs HEAD\"; git diff --name-only; echo \"=== clusters.rs @b24a2e6 : lignes cles\"; git show b24a2e6:drave-core/src/clusters.rs > /tmp/revue/clusters_b24.rs; grep  … [232 caractères tronqués]`

  ```
journal/README.md                                  |   2 +-
 .../6551e4dc-b73d-4df7-8fc4-b8c9fdbb0688/digest.md | 341 +++++++++++++++++++++
 .../rapport.md                                     |  57 ++++
 journal/sessions/MANIFEST.md                       |   5 +-
 .../bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md | 110 +++++++
 .../rapport.md                                     |  22 +-
 .../08-un-modele-eclate-se-lit-comme-un-seul.md    |  31 ++
 8 files changed, 569 insertions(+), 17 deletions(-)
=== fichiers de code modifies vs HEAD
README.md
drave-core/src/clusters.rs
journal/README.md
=== clusters.rs @b24a2e6 : lignes cles
130:/// Ce nœud ne porte-t-il qu'une PARTIE des clusters (`DRAVE_CLUSTERS`) ?
184:    clusters.sort();
190:        if *num != attendu {
197:    // Un nœud peut ne porter qu'une PARTIE des clusters (`DRAVE_CLUSTERS=0,3`) :
201:    let gardes: Option<Vec<usize>> = match std::env::var("DRAVE_CLUSTERS") {
205:                format!("DRAVE_CLUSTERS : « {x} » n'est pas un numéro de cluster"))))
215:                        format!("DRAVE_CLUSTERS : cluster {c} hors bornes ({} au total)",
219:            clusters.into_iter().filter(|(c, _)| g.contains(c)).collect(
… [179 caractères tronqués]
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && B=drave-core/target/release/drave\nfor v in \"7\" \"7,3\" \"5\"; do echo \"=== manque + DRAVE_CLUSTERS=$v\"; env DRAVE_CLUSTERS=\"$v\" $B /tmp/revue/manque --tensors 2>&1 | grep -v QT_IM | grep -E \"fichiers|error\" | head -1; done", … [61 caractères tronqués]`

  ```
=== manque + DRAVE_CLUSTERS=7
ouverture de l'en-tête GGUF: Custom { kind: InvalidInput, error: "DRAVE_CLUSTERS ne retient aucun cluster" }
=== manque + DRAVE_CLUSTERS=7,3
qwen3moe · 2 fichiers · 1 tenseurs · 0.00 Go de poids · en-têtes lus en 323.472µs
=== manque + DRAVE_CLUSTERS=5
qwen3moe · 2 fichiers · 1 tenseurs · 0.00 Go de poids · en-têtes lus en 150.293µs
  ```

- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && grep -rn \"impl Clone for\\|derive(Clone\" drave-core/src/gguf.rs drave-core/src/model.rs | head; echo \"=== data_ptr appelants\"; grep -rn \"data_ptr\" drave-core/src/ | head; echo \"=== mem::forget / Box::leak\"; grep -rn \"mem::fo … [116 caractères tronqués]`

  ```
drave-core/src/model.rs:239:#[derive(Clone, Copy)]
=== data_ptr appelants
drave-core/src/model.rs:161:            let Some(ptr) = g.data_ptr(nom) else {
drave-core/src/model.rs:178:        Some(Vue4 { base: g.data_ptr(nom)?, n_out, n_in, nb: n_in / bloc, src })
drave-core/src/gguf.rs:915:    pub fn data_ptr(&self, name: &str) -> Option<*const u8> {
=== mem::forget / Box::leak
  ```

### 🤖 Assistant

⏵ Rédaction du rapport adverse et envoi au parent.

- **send_message** `{"agent_id": "bbd6969f-0f70-42b2-8951-64d1f2f36d2e", "message": "RAPPORT ADVERSE — lecteur multi-fichiers / mmap / nœud partiel / numeros.\n\nATTENTION RÉVISION : HEAD a bougé pendant l'audit (6a2dfcb) et clusters.rs + README.md sont MODIFIÉS non commités (refactor `gardes_du_milieu`/`ouvrir_sous_en … [10741 caractères tronqués]`

  ```
message delivered to agent bbd6969f-0f70-42b2-8951-64d1f2f36d2e
  ```

### 🤖 Assistant

⏵ Rapport final : réponses aux 8 questions, preuves et correctifs.

**Révision auditée** : b24a2e6 (gguf.rs et model.rs inchangés sur disque). Pendant l'audit, HEAD est passé à 6a2dfcb et `clusters.rs` + `README.md` sont modifiés non commités (refactor `gardes_du_milieu`/`ouvrir_sous_ensemble`) : pour `clusters.rs`, ajouter **+26** après la ligne ~150. Aucun fichier du dépôt touché ; tout est dans `/tmp/revue`.

---

**1. mmap utilisé après munmap ? NON, aucun cas atteignable.**
Seule sortie de pointeur nu : `data_ptr` — `gguf.rs:915-918` `Some(self.tbuf(t).as_ptr())` — appelé uniquement par `charger_moe` (`model.rs:161` et `178`). Les `Vue4` (`model.rs:241` `pub base: *const u8`) vivent dans `Moe` → `Layer` → `Model.layers` (`model.rs:938`), et le `Gguf` propriétaire est le même `Model.g` (`model.rs:936`), construit par `Model::load` : `charger_moe(&g, l, cfg.n_expert)` (`model.rs:1673`) puis `Model { g, … }` (`model.rs:1949`). `Gguf`/`Tampon`/`Mappe` ne sont pas `Clone` ; ni `Vue4`, ni `Moe`, ni `Layer`, ni `DenseQ4` n'ont de `Drop` ; aucun `mem::forget`/`Box::leak` dans `src/`. Déplacer `Gguf` ne change pas la valeur du pointeur → sûr.
*Latent seulement* : (a) `Model` déclare `g` en premier, donc `munmap` a lieu avant le drop de `layers`/`head4` qui pointent dedans — sûr aujourd'hui parce qu'aucun `Drop` ne lit les poids ; (b) `Pool` est droppé après `g` et `impl Drop for Pool` (`engine.rs:786-791`) joint les fils ; (c) l'invariant « `g` survit aux pointeurs » n'est pas vérifié par le compilateur. Gravité : cosmétique/latent.

**2. Fuite si `Mappe::ouvrir` échoue, ou si `entete_de` rend `None` après mmap ? NON.**
`bufs` est un local (`gguf.rs:355`) droppé sur tout `?`/`Err` ; `Drop for Mappe` (`gguf.rs:67-71`) fait le `munmap` ; pas de `Clone` donc pas de double `munmap`. `entete_de` → `None` : `buf` n'est pas encore poussé et est droppé avec les précédents. Prémisse en partie fausse : un échec de `Mappe::ouvrir` **n'interrompt pas** l'ouverture — `ouvrir_tampon` (`gguf.rs:109-115`) imprime « mmap refusé … lecture complète » et retombe sur `read_to_end`. Seules les erreurs de lecture remontent.

**3. `Tampon::len` : OUI, correct.** `gguf.rs:91` `(**self).len()` déréférence vers `[u8]` ; `is_empty` (92) cohérent (et mort, `allow(dead_code)` ligne 3). Fichier vide : `Mappe::ouvrir` rend `ptr: null_mut(), len: 0` (`gguf.rs:48`) sans mmap, `Deref` rend `&[]` (`gguf.rs:62`), `Drop` saute `munmap` (`gguf.rs:69`). Vérifié sur un fichier 0 octet → erreur propre « en-tête GGUF incomplet » (`gguf.rs:675`), aucune UB. Aucun défaut.

**4. `DRAVE_CLUSTERS` (mesuré avec le binaire, dossiers synthétiques `/tmp/revue`, `--tensors`)**
| valeur | résultat |
|---|---|
| `0,0` | rc=0, cluster 0 chargé une fois (union via `g.contains`, `clusters.rs:219`) — doublon silencieux, **cosmétique** |
| `0,` | erreur claire « «  » n'est pas un numéro de cluster » |
| `" 0 "` | rc=0, marche (`clusters.rs:202-204`) |
| `-1`, `1e3`, `1 2`, `0x1`, `999…9` | erreur claire nommant la valeur |
| `""` | = pas de mode partiel, charge tout (`clusters.rs:202`) |
| `8` (8 clusters) | erreur « cluster 8 hors bornes (8 au total) » (`clusters.rs:213-217`) |
| `3,0` | rc=0, correct : filtre ensembliste + préfixes par numéro (`clusters.rs:219`, `234-238`) |
| **`7,3` avec cluster 7 absent du disque** | **rc=0, charge le seul cluster 3 en silence** — demandé mais absent = ignoré. **Gênant.** Correctif : exiger que chaque numéro demandé ait son `cluster-XX.gguf`, sinon erreur nommant le numéro. |

**5. `Moe::numeros`/`Moe::ou` : cohérent, aucun hors-bornes atteignable.**
`local = None` → `(vec![0], vec![base])` (`model.rs:111`) et `Some((0, e))` si `e < n_expert_global` (`model.rs:329`) ; `dims[0] == n_expert` exigé (`model.rs:147-148`). `local = Some(m)` → `numeros` construit par `v.iter().map(|(c,_)| *c)` (`model.rs:128`) donc `numeros.len() == gate.len()` par construction ; `num_up == numeros` et `num_down == numeros` sinon panique (`model.rs:183-186`) ; longueurs croisées vérifiées (`model.rs:195-198`) ; `k = numeros.position(cluster)` (`model.rs:335`) donc `k < gate.len() == up.len() == down.len()`. `ligne < par_cluster` garanti (`clusters.rs:92-96`) et `dims[0] == par_cluster` (`model.rs:147-148`) → `expert(loc)` dans le tenseur. Appelants : seulement `model.rs:2937` et `3745`, tous deux `let Some((k, loc)) = moe.ou(e) else { continue; }`. Aucun défaut.

**6. `DRAVE_CLUSTERS` + contrôle d'exhaustivité désactivé : OUI, résultat faux possible — confirmé.**
Contrôle fait seulement si `gardes.is_none()` (`clusters.rs:223-227`) et `gate.len() == n_clusters` seulement si `!partiel()` (`model.rs:191`). Reproduction : dossier de 7 fichiers `cluster-00..06` + mapping annonçant 8 clusters → sans variable : `Err "7 fichiers de cluster pour 8 annoncés"` ; avec `DRAVE_CLUSTERS=0,1,2,3,4,5,6,7` : **rc=0, « 8 fichiers · 7 tenseurs »**, sans un mot (idem `DRAVE_MMAP=0`, donc pas lié au mmap). Les experts du cluster manquant rendent `None` dans `Moe::ou` et leur contribution pondérée est perdue sans renormalisation (`model.rs:2920` puis `2937 else { continue; }`), la somme inter-nœuds n'existant pas (`REPRISE.md:733`). Le « désordre » est sain ; le danger est la var qui couvre tous les clusters annoncés alors qu'un fichier manque. **Gravité : bloquant (silencieux).** Correctif minimal : vérifier l'existence de chaque cluster demandé, et `let complet = clusters.len() == mapping.n_clusters; let _ = PARTIEL.set(!complet);` en gardant l'erreur d'exhaustivité dès que la demande couvre tous les clusters annoncés.

**7. `PARTIEL` (OnceLock global, `clusters.rs:135-138`, posé ligne `222`) : 1ᵉʳ appel avec la var, 2ᵉ sans → `partiel()` reste `true`**, et `ACTIF` (`clusters.rs:124-128`) garde le mapping du **premier** modèle : `charger_moe` traduirait les experts avec le mapping de l'autre modèle (mêmes formes → muet), ou chercherait `cl*/` pour un GGUF ordinaire et retomberait en silence sur le chemin dense. Atteignable en CLI ? **NON aujourd'hui** : un seul `Model::load` par exécution (`main.rs:687, 1353, 2030, 2162, 2998, 3874`). Atteignable dans les tests (plusieurs `ouvrir` par processus). Détail : `PARTIEL.set` précède l'ouverture réelle (`240-244`) → un échec d'ouverture laisse le drapeau armé. Gravité : latent/gênant.

**8. Le test `dossier_de_clusters_ouvre_et_apparie` peut passer avec du code faux : OUI.**
Il n'appelle jamais `charger_moe`/`Moe::ou`, et il ne *peut* pas : `gguf_synth` n'écrit que des F32 (`gguf.rs:1264`), refusés par `source_de` (`model.rs:81`). Défaut concret non détecté : remplacer `model.rs:335` par `Some((cluster, ligne))` (le bug d'origine) laisse les 30 tests verts, et c'est invisible à l'exécution sur un nœud complet (position == numéro) — seul un nœud partiel dont le cluster chargé n'est pas le rang 0 le révèle : **le correctif mis en avant par le commit n'a aucun test**. Le test ne couvre que `tbuf`/`dequant` (2 clusters `cluster-00/01`), ni pas de `Vue4`, ni `est_mappe()`, ni `DRAVE_MMAP=0`, ni `partiel()`.

**Autres défauts**
- **A.** `octets_de` (`gguf.rs:579-584`) ne borne pas le début : `&b[debut..(debut+besoin).min(b.len())]` panique si `debut > b.len()`. Reproduit avec 2 shards dont le doublon a un offset à 1 Go : « range start index 1073741952 out of range for slice of length 128 ». Gênant ; correctif : borner et rendre une `io::Error`.
- **B.** Commentaire périmé `clusters.rs:168-171` (« préfixes attribués par POSITION ») contredisant `clusters.rs:234-238`. Le contrôle de continuité `189-195` n'est plus nécessaire à la justesse et **empêche un nœud de ne posséder que ses fichiers** : dossier avec seulement `commun.gguf` + `cluster-03.gguf` → refusé quel que soit `DRAVE_CLUSTERS`. Le mode partiel ne réduit que la RAM, pas le disque. Gênant ; correctif : continuité après filtrage (ou supprimée) + existence de chaque cluster demandé.
- **C.** Aucune vérification `mapping.n_experts == cfg.n_expert` : un mapping étranger aux mêmes formes ferait sauter en silence les experts routés au-delà (`model.rs:329`, `clusters.rs:110-112`).

**Rien trouvé** sur : fuite mémoire, double `munmap`, dépassement d'index via `Moe::ou`, longueur de `Tampon`, cas `len == 0`. `cargo test --release` : 30 tests, 0 échec.

