# Session 31f26a6e — Tu es un relecteur ADVERSARIAL

| | |
|---|---|
| Identifiant | `31f26a6e-65f5-480d-be32-36b9f425b3dd` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-02 19:26 |
| Durée | 0.4 h |
| Tours | 1 |
| Messages | 85 |
| Appels d'outils | 111 |
| Fichiers touchés | 1 |
| Commandes | 82 |
| Sous-agents | 2 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu es un relecteur ADVERSARIAL autonome, en LECTURE SEULE. Tu ne modifies AUCUN fichier du dépôt (pas d'édition, pas de `git commit`, pas d'écriture dans le dépôt ; tes scripts temporaires vont dans /tmp). Ta sortie est un rapport en français dans ta réponse finale.  Dépôt : /home/stephane/Data13TB/stephane/GitHub/Qtrinet (moteur d'inférence LLM en Rust, `std` seul). Modèle de travail : DeepSeek-V … [4531 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu es un relecteur ADVERSARIAL autonome, en LECTURE SEULE. Tu ne modifies AUCUN fichier du dépôt (pas d'édition, pas de  … [4811 caractères tronqués]

*111 appels d'outils.* Actions notables :

- bash — Show recent git log and status
- bash — List repo root, reports and tools
- bash — Show uncommitted diff in model.rs
- bash — Show stats of three most recent commits
- bash — Grep YaRN-related symbols in model.rs
- bash — Read rope_yarn in llama.cpp ggml
- read
- bash — Outline engram.rs
- bash — Read deepseek4.cpp rope block
- bash — Find dsv4_rope_attn_factor definition
- bash — Read other rope call sites in deepseek4.cpp
- bash — Read attn_factor helper and q_pe rope
- bash — Grep rope init details
- bash — Find corr_dims call sites in llama.cpp
- … et 76 autres

**Synthèse produite :**

⏵ Rapport final (relecture adversariale, lecture seule)

\# Rapport adversarial — commits `8444a39` → `93cb1b7` (Qtrinet)

**Mode** : lecture seule ; aucun fichier du dépôt modifié (scripts dans `/tmp`). Références de lignes = **arbre de travail** (`model.rs` porte +37 lignes non commitées ; pour HEAD, retrancher ~10-15 selon l'endroit).

\## FAUX

\### F1 — `--sans-yarn` ne coupe PAS le YaRN des couches compressées
- `main.rs:881` et `4558` : `if sans_yarn { mdl.cfg_yarn_off(); }`, appelé **après** la construction. `model.rs:3895` : `pub fn cfg_yarn_off(&mut self) { self.cfg.yarn = None; }` — c'est tout.
- Or `Mla4.yarn_compresse` est **figé à la construction** (`model.rs:3121-3122`) sur `cfg.yarn_declare` et la seule variable `DRAVE_YARN_NON`. `cfg.yarn` n'est lu que par les chemins **denses** (`4614`, `6131`) : sur V4 le drapeau CLI est inerte.
- Contredit `model.rs:2693` (« `DRAVE_YARN_NON=1` jamais de YaRN (ce que fait `--sans-yarn`) ») et `3117-3120` (« `DRAVE_YARN_NON` (et `--sans-yarn`) veut dire “JAMAIS de YaRN” »).
- **Mesuré** (2 passes bornées, `--couches 2:3`, 8 jetons) : `--sans-yarn` → perplexité **64 730 738,578** ; `DRAVE_YARN_NON=1` → **65 819 810,336** (+1,7 %). Seule la couche 2 tourne (ratio 4) et les deux passes ne diffèrent que par cette rotation ⇒ le drapeau n'a rien coupé. Logs `/tmp/yarn_sans.log`, `/tmp/yarn_non.log`.

\### F2 — « fenêtre de `max_ngram − 1` jetons » : faux tel qu'écrit (le code, lui, est juste)
`model.rs:5962` garde **`max_ngram` = 4** jetons (`pos.saturating_sub(max_ngram-1)`). Une fenêtre de 3 jetons donne **11 412 / 45 640 adresses fausses (25 %)**, colonnes 16-23 et 40-47 (groupe `shift=3`), identiques dans l'oracle Python.

\## FAIBLE

- **Fa1 — l'annonce de rotation ment sur V4 (mesuré).** Le log de la passe ci-dessus imprime « `[config] rotation : RoPE simple (contexte 8 ≤ 65536 initial ; YaRN ×16 prendrait le relais au-delà)` » (`model.rs:3423-3445`) alors que la couche exécutée tourne en YaRN ×16 à toutes les positions. Idem `3373`/`3393`. Le commentaire `3420-3422` dit que cette trace sert à distinguer RoPE simple et YaRN : pour V4 (41/44 couches en YaRN) elle ne le fait pas.
- **Fa2 — citation du mscale inexacte, conclusion juste.** `model.rs:4326-4329` cite `llama-context.cpp:492-494` ; pour deepseek4 le mécanisme est `dsv4_rope_attn_factor` (`deepseek4.cpp:11-17`, l'inverse de `1+0,1·ln(1/freq_scale)`) remultiplié par le noyau ⇒ produit **1,0 exact** (mesuré). `cparams.yarn_attn_factor` n'est pas utilisé 
… [5893 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/tmp/verif_yarn_adv.py` | 1 | 0 |

### Sous-agents lancés

- tour 1 — Test équivalence hachage engram
- tour 1 — Vérif sélection indexeur 512 blocs

### Commandes exécutées (échantillon)

- **T1** Show recent git log and status
- **T1** List repo root, reports and tools
- **T1** Show uncommitted diff in model.rs
- **T1** Show stats of three most recent commits
- **T1** Grep YaRN-related symbols in model.rs
- **T1** Read rope_yarn in llama.cpp ggml
- **T1** Outline engram.rs
- **T1** Read deepseek4.cpp rope block
- **T1** Find dsv4_rope_attn_factor definition
- **T1** Read other rope call sites in deepseek4.cpp
- **T1** Read attn_factor helper and q_pe rope
- **T1** Grep rope init details
- **T1** Find corr_dims call sites in llama.cpp
- **T1** Grep yarn params in llama.cpp src
- **T1** Read llama-context rope params
- **T1** Read graph rope params and dsv4 kv rope
- **T1** Grep rope scaling loading in llama-model.cpp
- **T1** Read yarn_attn_factor block start
- **T1** Grep rope/indexer call sites
- **T1** List all rope calls in deepseek4.cpp
- **T1** List /tmp dumps and scripts
- **T1** Read engram reference tool header
- **T1** Find candidate_topk_blocks references
- **T1** Grep candidate filter in Qtrinet repo
- **T1** Grep vLLM candidate code in journal
- **T1** Locate vLLM deepseek_v41 reference
- **T1** Read vLLM indexer code in journal
- **T1** Look for spill files and mscale mentions
- **T1** Grep rope.py hints in digest
- **T1** Locate YaRN report
- **T1** Show model.rs diff of YaRN commit
- **T1** Grep sans_yarn flag handling
- **T1** Read ggml-cpu rope kernel init
- **T1** Read cfg_yarn_off implementation
- **T1** Inspect y128/p128 dumps and compare tool
- **T1** Read engram verifier tool
- **T1** Read source_de and consumer refusal
- **T1** Grep kv_source_layer_ids handling
- **T1** Find adresses call sites
- **T1** Search indexer verifier scripts
- … et 42 autres

## 4. Mesures et résultats marquants

- **T1** `+    /// `candidate_topk_blocks × candidate_block_size` (2 048 × 8 = 16 384 pour ce`
- **T1** ``compress_ratio > 0`, la rotation est YaRN ×16 (base 160000, beta 32/1, contexte`
- **T1** `(chiffrée dans le rapport : vLLM applique YaRN ×16 à toutes les positions des`
- **T1** `[timed out after 60000ms]`
- **T1** `./drave-core/src/model.rs:1252:    /// `candidate_topk_blocks × candidate_block_size` (2 048 × 8 = 16 384 pour ce`
- **T1** `3916-    /// (mesuré : densité de 51 104 %, tous les neurones « chauds »). PowerInfer`
- **T1** `1252-    /// `candidate_topk_blocks × candidate_block_size` (2 048 × 8 = 16 384 pour ce`
- **T1** `/dev/mapper/system-root   11T  7,4T  3,5T  69% /home/stephane/Data13TB`
- **T1** `/dev/nvme0n1p2           828G  559G  268G  68% /home/stephane/FastNVMe`
- **T1** `3451-        // rapide que le chemin scalaire Q6_K, qui coûtait 42 % du temps par`
- **T1** `journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/rapport.md:3923:**P5 — le compresseur CSA et l'indexeur** : validés aussi (0,999990 pour le CSA aux positions 3-9 ; scores d'indexeur à **0,1-0,3 `
- **T1** `Écart **0,1 à 0,3 %**, du même ordre que partout ailleurs. Le top-k lui-même`
- **T1** `[config] rotation : RoPE simple (contexte 8 ≤ 65536 initial ; YaRN ×16 prendrait le relais au-delà)`
- **T1** `[tête 4 bits] 129280 × 4096 → 4.50 b/poids, 0 Mo, 0.0 s`
- **T1** `2:[config] attention V4 : 43 couches · 1 tête latente de 512 (448 nope + 64 rope) · 64 têtes de requête · sortie groupée 8×1024 · puits par tête`
- **T1** `13:[config] rotation : RoPE simple (contexte 8 ≤ 65536 initial ; YaRN ×16 prendrait le relais au-delà)`
- **T1** `part de l'attention dans le flux total : 5.7 %`
- **T1** `7 tokens notés — perplexité cumulée 64730738.578  (1.5 tok/s)`
- **T1** `=== perplexité 64730738.5776 sur 7 tokens (0 événements, 4.7 s) ===`
- **T1** `7 tokens notés — perplexité cumulée 65819810.336  (1.4 tok/s)`
- **T1** `=== perplexité 65819810.3365 sur 7 tokens (0 événements, 5.1 s) ===`

## 5. Erreurs rencontrées

4 sorties en erreur ou divergentes. Les premières :

- **T1** : case GGML_TYPE_IQ4_NL:         case GGML_TYPE_IQ4_XS:         case GGML_TYPE_IQ3_S:         case GGML_TYPE_IQ2_S:         case GGML_TYPE_Q8_K:         case GGML_TYPE_I8:         case GGML_TYPE_I16:   
- **T1** : /tmp/dump_sel: total 422240 drwxr-xr-x.  2 stephane stephane 239240  2 oct 19:23 . drwxrwxrwt. 82 root     root     413300  2 oct 19:29 .. -rw-r--r--.  1 stephane stephane 131072  2 oct 19:21 d-attn_b
- **T1** : /tmp/ids_v4flash.txt : 8 tokens, fenêtres de 8  thread 'main' (3089139) panicked at src/model.rs:2630:39: ouverture du GGUF: Custom { kind: NotFound, error: "/home/stephane/Data13TB/stephane/modeles/g
- **T1** : 98:route "V4-Flash : racine de softplus" "$M/DeepSeek-V4-Flash-UD-IQ1_M/DeepSeek-V4-Flash-UD-IQ1_M-00001-of-00003.gguf" "racine de softplus" 101:# 6bis. V4-Flash : le modèle de la famille V4 tourne EN

