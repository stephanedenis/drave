# Session c776b71f — Tu es relecteur ADVERSARIAL de

| | |
|---|---|
| Identifiant | `c776b71f-525a-4bad-b83c-eff1c2d204ff` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-09-30 18:36 |
| Durée | 0.1 h |
| Tours | 1 |
| Messages | 35 |
| Appels d'outils | 54 |
| Fichiers touchés | 0 |
| Commandes | 37 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu es relecteur ADVERSARIAL de code dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (moteur d'inférence Rust « Drave », std seul). Ton but est de TROUVER DES DÉFAUTS RÉELS en LISANT le code — les bancs de ce dépôt ne les voient presque jamais, les relectures si.  Périmètre EXACT (dernier ajout de la journée, commit `d221ead`) :  1. `drave-core/src/model.rs` — la branche « top-k dépor … [4505 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu es relecteur ADVERSARIAL de code dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (moteur d'inférence Ru … [4785 caractères tronqués]

*54 appels d'outils.* Actions notables :

- bash — Check repo state and commit stats
- bash — Count lines in target files
- read
- bash — Show model.rs diff for the commit
- bash — Locate relevant gpu.rs symbols
- bash — Locate CUDA kernels
- bash — Grep key symbols in model.rs
- bash — Show gpu.rs and main.rs diff
- bash — Read vram_assurer helper
- bash — Find all attn_events uses
- bash — Find env flag docs and uses
- bash — Read perf print and doc diff
- bash — Read REPRISE env table
- bash — Read attn_kv kernels for sink indexing
- … et 25 autres

**Synthèse produite :**

⏵ Report sent to the parent agent; summarizing the findings

Rapport livré au parent (`send_message` → `bbd6969f-...`). Aucun fichier modifié.

\## Vérifié conforme (ne pas re-vérifier)
- **Aucun résultat partiel dans `att`** : le noyau 3 est le seul à écrire `att` ; le repli CPU reprend les `nh` têtes (`model.rs:3272`) et **zéroïse** `att[hh*hd..]` (`3356-3357`, `3319`). Même une DtoH interrompue (`gpu.rs:1035`) est réécrite.
- **4 passes exactes** (24,16,8,0), `ok` propagé, descente/préfixes corrects, `besoin ≥ 1` par construction, garde `gpu.rs:892` en filet.
- **Layout** `ligne = kvh*rep + r = hh` ; `att[hh*hd..]` ↔ `out[ligne*hd..]`.
- **Puits au dénominateur seulement**, et le noyau 3 les indexe bien par `hh` (`sinks[ligne]`).
- **`sc2`/`ctx` vs `sc`/`n` : pas un bug** (deux tampons, chacun son pas ; `ctx` du noyau = pas du cache KV).
- **Déterminisme : oui** (`atom.shared/global.add.u32` réels, réductions fixes, accumulation séquentielle).
- **Pas d'usage-après-libre** des tampons partagés (chaque usage finit par une DtoH bloquante / `cuCtxSynchronize`), et pas d'alternance possible sur une même couche.

\## Défauts, classés
1. **D1 (faux résultat silencieux, pré-existant)** `drave_gpu.cu:578,588` : `sinks[warp]` alors que la sortie est `out[(kvh*rep + warp)*hd …]` (`:592`). gpt-oss : `attn_sinks.weight` = 64 = `n_head` (GGUF vérifié), `n_kv_head` = 8, écarts intra-groupe jusqu'à 4,65 logit ⇒ tête 48+w drainée par le puits de la tête w. Le CPU et le nouveau noyau 3 sont corrects. Correctif : `sinks[kvh*rep + warp]`.
2. **D2 (faux résultat silencieux)** `forward_lot` ignore `--attn-topk` (`model.rs:2526,2591`) : `--lot > 1` calcule une attention dense, sans message.
3. **D5** `sel` (`model.rs:3256`) n'est jamais contrôlé alors que la collecte le recopie (`gpu.rs:924`) et que `t.sortie` n'est jamais remis à zéro : une sous-écriture publierait des indices périmés (`fait_en_gpu = true`). Le banc, lui, teste `cases_vides`.
4. **D3 (perf)** `k ≤ 1024` / `bits ∈ {8,32}` ne sont testés qu'à `gpu.rs:946,951`, après 7 noyaux : `--attn-topk 2048` ou `DRAVE_KV_BITS=4` refait 7 passes GPU par couche et par jeton avant de rendre la main au CPU.
5. **D4 (perf/robustesse)** `gpu.rs:639-647` matérialise `nh×n×4` par couche — exactement le tampon que `docs/plan-gpu-topk.md:44-46` déclare « ✗ trop » (56 Mo/couche à 1 M × 14 têtes ; 9,2 Go pour gpt-oss), non budgété, échec muet ⇒ repli CPU silencieux.
6. **D11 (latent)** `sinks_cap`/`out_cap` en éléments dans `attn_kv` (
… [1244 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** Check repo state and commit stats
- **T1** Count lines in target files
- **T1** Show model.rs diff for the commit
- **T1** Locate relevant gpu.rs symbols
- **T1** Locate CUDA kernels
- **T1** Grep key symbols in model.rs
- **T1** Show gpu.rs and main.rs diff
- **T1** Read vram_assurer helper
- **T1** Find all attn_events uses
- **T1** Find env flag docs and uses
- **T1** Read perf print and doc diff
- **T1** Read REPRISE env table
- **T1** Read attn_kv kernels for sink indexing
- **T1** Grep sinks in CUDA file
- **T1** Read attn_kv_partiels kernel
- **T1** Read recombine kernel and sink index
- **T1** Read partiels kernel tail
- **T1** Read bench context before new step 5
- **T1** Read second-pass bench after step 5
- **T1** List models and check GPU availability
- **T1** Find attn_sinks handling in Rust
- **T1** Parse GGUF metadata for sinks shape
- **T1** Read gpt-oss sink values and spread
- **T1** Inspect CUDA stub atomics
- **T1** Check plan for VRAM budget
- **T1** Read the plan doc header
- **T1** Get doc line numbers and batch path callers
- **T1** Collect exact quotes and lines
- **T1** Find ppl entry and forward calls
- **T1** Map kernel line numbers
- **T1** Read the ppl batching loop
- **T1** Find lot option default
- **T1** Extract exact gpu.rs lines
- **T1** Extract remaining exact lines
- **T1** Final quotes: out indexing, CPU scoring loop
- **T1** Final line numbers for doc claims
- **T1** Read bench coverage check

## 4. Mesures et résultats marquants

- **T1** `1f53667 Compteur de lignes Rust unifié : 13 168 (un seul chiffre, mesuré, dans README ×2 et REPRISE)`
- **T1** `| 2 048 | 4,21 ms/jeton | 7,68 | 13,1358 / 13,1355 |`
- **T1** `| 8 192 | 6,35 ms/jeton | 7,36 | 13,1358 / 13,1355 |`
- **T1** `Le GPU est plat (7,4 ms/jeton), le CPU croît de 3,5e-4 ms par clé : le croisement`
- **T1** `complète sans relecture des scores coûte 3,90 ms contre 539,9 ms pour l'attention`
- **T1** `complète sur CPU (×138) et 13,2 ms pour l'attention complète en VRAM — soit 0,3×`
- **T1** `moteur utilisera vraiment (le banc, lui, relit 15,59 ms de scores à 1 M pour`
- **T1** `+            // notation restait donc sur CPU, où elle coûte 968 ms par couche à`
- **T1** `+            // complet en VRAM — mesuré 3,90 ms pour 14 lignes × 1 M de clés,`
- **T1** `+            // contre 539,9 ms pour l'attention complète sur CPU.`
- **T1** `+    /// pèse 14,7 Mo sur le bus PCIe, et 56 Mo à 1 M : la mesurer séparément est`
- **T1** `+    // pondérée) — la référence que le plan cite : 968 ms par couche à 1 M de clés.`
- **T1** `./reports/rapport-placement-bits-kv.md:137:| contexte long **avec** `DRAVE_GPU_KV=1` | **int8/int8** (28 %, +3,04 %) ou f32/f32 | le miroir exige une disposition homogène ; il divise le temps de l'att`
- **T1** `./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:22747:- Regression gates (must stay): Qwen ctx 256 = **19,3885**; gpt-oss ctx 256 = **15,1757** — measured **without** `DRAVE_GPU` (th`
- **T1** `./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:29006:- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > /tmp/porte_gpu.sh <<'EOF'\n#!/bin/bash\ncd `
- **T1** `./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:29015:=== 1. gpt-oss avec DRAVE_GPU (documenté : 15,1667, le pilote déporte les Q8_0 > 8 Mo) ===`
- **T1** `./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:29596:`DRAVE_GPU=1` sur gpt-oss redonne **15,1667**, et le noyau de tête **1,6 ms** (88 Go/s) pour un écart de **1,99e-7**. Le noyau d`
- **T1** `./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:31489:AUTRES : (3) plafond R4 = par message, pas par session : 8 flux de 35,4 Mo (282,9 Mo cumulés > 256) tous acceptés — mais la RAM `
- **T1** `./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:32509:| la même, **KV en VRAM** (`DRAVE_GPU_KV=1`, noyaux `attn_kv_*`) | **13,2 ms** (×73) |`
- **T1** `// Aucun événement : le mode dense ne compte rien. Annoncer « 100 % »`
- **T1** `// l'aveugle. Le poste non compté contient la tête de sortie (151 936 × 896`
- **T1** `| `DRAVE_KV_BITS=8` ou `4` | quantifie le cache KV (défaut f32) | le 4 bits coûte +364 % de perplexité à 8 192 |`
- **T1** `| `DRAVE_KV_K_F32=1` | garde les CLÉS en f32 (valeurs quantifiées) | mesuré : à 8 192, **64 %** de la taille f32 (5,125 octets par élément, échelles comprises) pour +0,023 %, contre +3,04 % pour l'int`
- **T1** `@@ -89,8 +89,8 @@ doit montrer l'effet cherché : **968 ms → quelques dizaines de ms par couche*`
- **T1** `-| 4 | branchement dans `model.rs` (autoriser le GPU quand `attn_topk > 0` **et** que le noyau rend `true`, garder le repli CPU sinon) | perplexité 2 048 = 234,88 ± tolérance |`
- **T1** `+| 5 | mesure 1 M : ms/layer avec et sans top-k, sur GPU | ✅ **fait au niveau des noyaux** : la chaîne complète (scores sans relecture + 4 passes + collecte + somme) coûte **3,90 ms** pour 14 lignes ×`
- **T1** `TEL QUEL** : le cache LRU donne +6 % en décodage (5,12 → 5,43 jetons/s,`
- **T1** `53,5 % de succès, 10,64 Go montés) — le chemin CPU des experts est déjà AVX2`
- **T1** `// pondérée) — la référence que le plan cite : 968 ms par couche à 1 M de clés.`
- **T1** `// pilote (≥ 64 ko), donc 14 ko d'écriture hors bornes peuvent passer`
- **T1** `18:| la même, **KV en VRAM** (`DRAVE_GPU_KV=1`, noyaux `attn_kv_*`) | **13,2 ms** (×73) |`
- **T1** `44:   *Budget mémoire* : 14 têtes × N × 4 octets — 56 Mo à 1 M ✗ trop. **Le tampon ne`
- **T1** `93:| 5 | mesure 1 M : ms/layer avec et sans top-k, sur GPU | ✅ **fait au niveau des noyaux** : la chaîne complète (scores sans relecture + 4 passes + collecte + somme) coûte **3,90 ms** pour 14 lignes`
- **T1** `| attention 1 M de clés, **CPU** (int4, host) | **968 ms** par couche |`
- **T1** `| la même, **KV en VRAM** (`DRAVE_GPU_KV=1`, noyaux `attn_kv_*`) | **13,2 ms** (×73) |`
- **T1** `| « masquer sans réécrire les boucles » en top-k CPU | 12,4 → 12,5 ms : **aucun gain** |`
- **T1** `* sm_75 (Quadro RTX 5000) : 1024 fils par bloc, 48 ko de partagé, pas de`
- **T1** `*Budget mémoire* : 14 têtes × N × 4 octets — 56 Mo à 1 M ✗ trop. **Le tampon ne`
- **T1** `1484:/// contrôle : jusqu'à ~15 To demandés au noyau. 256 Mo couvrent largement un lot`
- **T1** `1485:/// de 8 192 jetons × 8 192 canaux (268 Mo... soit un lot par fenêtre maximale).`

