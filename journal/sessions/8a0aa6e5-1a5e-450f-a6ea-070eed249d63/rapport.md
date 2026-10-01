# Session 8a0aa6e5 — Tu es un relecteur adverse.

| | |
|---|---|
| Identifiant | `8a0aa6e5-1a5e-450f-a6ea-070eed249d63` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-01 11:15 |
| Durée | 0.2 h |
| Tours | 1 |
| Messages | 47 |
| Appels d'outils | 66 |
| Fichiers touchés | 0 |
| Commandes | 61 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu es un relecteur adverse. Tu ne modifies AUCUN fichier : tu lis, tu vérifies, tu rapportes. Ton travail est de trouver ce qui est FAUX, pas de confirmer ce qui va bien.  Contexte : dépôt Rust à /home/stephane/Data13TB/stephane/GitHub/Qtrinet (moteur d'inférence GGUF « std seul », binaire `drave-core/target/release/drave`). Le commit le plus récent (3eb0af7) vient d'introduire un lecteur GGUF mul … [3695 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu es un relecteur adverse. Tu ne modifies AUCUN fichier : tu lis, tu vérifies, tu rapportes. Ton travail est de trouver … [3975 caractères tronqués]

*66 appels d'outils.* Actions notables :

- bash — Inspect repo state and file sizes
- bash — List source files
- read
- bash — Find users of q8_view/base/data_ptr
- bash — Locate Moe struct and call sites
- bash — Read model.rs head
- bash — Read Moe impl
- bash — Read charger_moe call site
- bash — Read first moe.ou call site
- bash — Read second moe.ou call site
- bash — Read MoE routing prologue (batch path)
- bash — Read MoE routing prologue (single path)
- bash — Find converter and docs referencing clusters
- bash — List repo root and sprints
- … et 49 autres

**Synthèse produite :**

⏵ Rédaction du rapport adverse et envoi au parent

Review complete. Here is the report.

---

\# Rapport adverse — commit 3eb0af7 (lecteur multi-fichiers + clusters)

**État vérifié** : `gguf.rs` md5 `10b97dcd…`, `clusters.rs` `35cbad5f…` (identiques au commit) ; `model.rs` `d6b11c43…` **modifié après le commit** (+9 lignes non commitées vers 1640, un diagnostic `mélanges d'experts chargés`). Les numéros de ligne `model.rs` ci-dessous sont ceux de l'arbre de travail actuel ; `gguf.rs`/`clusters.rs` sont ceux du commit.
**Vérifié empiriquement** : `cargo test --release` → **24 passed** ; inventaire DeepSeek → **3 fichiers · 1328 tenseurs · 86.90 Go · 54 ms**, répartition **0 / 784 / 544**, total disque **86.90 Go** — les mesures du sprint sont exactes.

\## 1. Décalage des données — **OUI, tous les chemins sont corrects**
Aucun chemin ne lit plus au début du fichier : `tbuf` (`gguf.rs:560-567`), `octets_de` (`450-452`), `data_ptr` (`763-766`, passe par `tbuf`), `q8_dot_at` (`820` : `&self.bufs[v.fichier][self.starts[v.fichier]..]`), `q8_dot_avx2` (`934`, idem), `q8_blocks`/`q4k_blocks`/`q6k_blocks`/`mxfp4_blocks`/`q4_blocks` (`774-814`, tous `self.tbuf(t)`), `dequant` (`959`), `raw_levels` (`620`), `row_f32` (`653`).
Deux nuances, pas des défauts : `Q8View.base` est un offset **local au fichier** (`758`) — correct uniquement parce que les deux `q8_dot_*` tranchent `starts[...]` eux-mêmes ; tout nouveau lecteur de `Q8View` doit le refaire. Et `starts` des fichiers 2..N est calculé avec l'`alignment` du **premier fichier porteur de métadonnées** (`272`, `435`), pas du fichier concerné (`cosmétique` : tous les découpages réels partagent la même valeur).

\## 2. `octets_tensor` — **OUI, juste pour tous les types listés**
Confronté à l'amont ggml (`ggml-common.h` `static_assert(sizeof(block…))` + table `type_size` de `ggml.c`) : Q4_K 144/256 ✓, Q6_K 210/256 ✓, Q8_0 34/32 ✓, MXFP4 17/32 ✓, **IQ1_M 56/256** ✓ (`sizeof(block_iq1_m) == QK_K/8+QK_K/16+QK_K/32`), BF16 2/1 ✓, F32 4/1 ✓, plus Q4_0/Q4_1/Q5_0/Q5_1/Q8_1/Q2_K/Q3_K/Q5_K/Q8_K/IQ2_XXS/IQ2_XS/IQ2_S/IQ3_XXS/IQ3_S/IQ1_S/IQ4_NL/IQ4_XS/TQ1_0/TQ2_0/NVFP4 (36/64) ✓. Aucun type mal apparié.
**Défaut (gênant)** : `_ => return 0,` (`gguf.rs:477`) — un type inconnu est compté **0 octet en silence**, exactement le mécanisme de l'incident iq1_m. Les types 41 (`Q1_0`) et 42 (`Q2_0`), ajoutés à ggml (`ggml.h:431-432`), tombent dedans. Correctif minimal : rendre `Option<u64>`/paniquer avec le numéro de type. À noter aussi : le c
… [7510 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** Inspect repo state and file sizes
- **T1** List source files
- **T1** Find users of q8_view/base/data_ptr
- **T1** Locate Moe struct and call sites
- **T1** Read model.rs head
- **T1** Read Moe impl
- **T1** Read charger_moe call site
- **T1** Read first moe.ou call site
- **T1** Read second moe.ou call site
- **T1** Read MoE routing prologue (batch path)
- **T1** Read MoE routing prologue (single path)
- **T1** Find converter and docs referencing clusters
- **T1** List repo root and sprints
- **T1** Inspect converter naming
- **T1** Find callers of new constructors
- **T1** Find swallowed errors in gguf/clusters
- **T1** Check docs for ggml type table
- **T1** Look for local ggml sources
- **T1** Read format-clusters doc highlights
- **T1** Read converter header
- **T1** Fetch ggml-common.h and inspect block_iq1_m
- **T1** Extract all block size asserts
- **T1** Fetch ggml.c type table
- **T1** Read Q8View usage in head
- **T1** Read Proj::load / data_ptr usage
- **T1** Find cfg.n_expert derivation
- **T1** Read main.rs .ok()? context
- **T1** Test Path::parent empty-path behavior
- **T1** Check converter expert_count and common file
- **T1** Read converter split logic
- **T1** Find mapping.tsv producers
- **T1** Show commit stat
- **T1** Find mapping.tsv producers (scoped)
- **T1** Show commit files and model.rs diff
- **T1** Run cargo test --release once
- **T1** Show main.rs diff of commit
- **T1** List model directories
- **T1** Check artifacts and cluster dirs
- **T1** Check binary freshness and other dirs
- **T1** Check CLI for modele/tensors
- … et 21 autres

## 4. Mesures et résultats marquants

- **T1** `//! accumulateur de 151 936 × 8 octets **par worker** (36 Mo) et chaque sortie`
- **T1** `//! précision. Le reste du modèle — 99,7 % des poids — passe par les événements.`
- **T1** `// repasserait 4,4 Mo sur le bus à chaque jeton.`
- **T1** `// sur 128, soit 6 % du FFN — et c'est le régime où l'architecture`
- **T1** `[timed out after 60000ms]`
- **T1** `6:18,56** et **625 ms au lieu de 3,9 s** sur Qwen3-30B-A3B.`
- **T1** `70:| le modèle entier | 0,9 ms | **3 906,4 ms** | **18,56 Go** |`
- **T1** `tenseurs en 54 ms · Qwen3-30B-A3B en clusters 1587 tenseurs / 18,55 Go ·`
- **T1** `/// GPU 380 Go/s en lecture locale.`
- **T1** `deepseek4 · 3 fichiers · 1328 tenseurs · 86.90 Go de poids · en-têtes lus en 54.153788ms`

## 5. Erreurs rencontrées

4 sorties en erreur ou divergentes. Les premières :

- **T1** : == bare filename (cwd=/tmp) == [attention] QT_IM_SWITCHER est l'ancien nom d'une variable d'environnement : elles s'appellent maintenant DRAVE_* (voir docs/histoire.md). Rien n'a été appliqué.  thread
- **T1** : == bare == thread 'main' (2892031) panicked at src/main.rs:1380:40: ouverture de l'en-tête GGUF: Os { code: 2, kind: NotFound, message: "No such file or directory" } note: run with `RUST_BACKTRACE=1` 
- **T1** : 24 69 thread 'main' (2892142) panicked at src/gguf.rs:435:59: called `Option::unwrap()` on a `None` value note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
- **T1** : == prefixe contenant -of- == thread 'main' (2892804) panicked at src/gguf.rs:526:9: version GGUF 0 non gérée note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace == total=1 ==

