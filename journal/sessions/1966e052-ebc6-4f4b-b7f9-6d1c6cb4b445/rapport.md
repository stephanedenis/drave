# Session 1966e052 — Tu travailles dans le dépôt

| | |
|---|---|
| Identifiant | `1966e052-ebc6-4f4b-b7f9-6d1c6cb4b445` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-08 09:18 |
| Durée | 0.0 h |
| Tours | 1 |
| Messages | 22 |
| Appels d'outils | 33 |
| Fichiers touchés | 0 |
| Commandes | 20 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (moteur d'inférence Rust « Drave », drave-core/). LECTURE SEULE STRICTE : ne modifie aucun fichier, ne compile pas, ne lance aucun test ni binaire.  Objectif : inventorier les capacités d'EXPLOITATION DU GPU (et du tandem de GPU) du moteur.  À examiner : - drave-core/src/gpu.rs : quelles fonctions, quels noyaux (kernels),  … [2049 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (moteur d'inférence Rust « Drave », drave-co … [2329 caractères tronqués]

*33 appels d'outils.* Actions notables :

- bash — List repo root and drave-core src
- bash — Inventory tools, reports, bench, gpu dir
- grep
- read
- bash — List functions in gpu.rs
- bash — Find dispatch threshold and multi-GPU refs
- bash — Find GPU call sites in model.rs
- bash — Check tests, gpu dir, tools scripts
- bash — Inspect tests and gates for GPU
- bash — Read tandem NVLink report
- bash — Check gates and GPU benches in main.rs
- bash — Read GPU scores and logits reports
- bash — Read trace_gpu.py
- bash — Read experts cache report and topk plan
- … et 9 autres

**Synthèse produite :**

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

**2) Critère exact du dispatch auto** (copie, model.rs:1558-
… [3395 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** List repo root and drave-core src
- **T1** Inventory tools, reports, bench, gpu dir
- **T1** List functions in gpu.rs
- **T1** Find dispatch threshold and multi-GPU refs
- **T1** Find GPU call sites in model.rs
- **T1** Check tests, gpu dir, tools scripts
- **T1** Inspect tests and gates for GPU
- **T1** Read tandem NVLink report
- **T1** Check gates and GPU benches in main.rs
- **T1** Read GPU scores and logits reports
- **T1** Read trace_gpu.py
- **T1** Read experts cache report and topk plan
- **T1** Check logits_gpu callers and gpu bench
- **T1** Read topk selection report key sections
- **T1** List CUDA kernels, compiler script, gates
- **T1** Check KV group condition and expert cache measurement
- **T1** Read KV engine measurements and gpu tools
- **T1** Check banc-kv and aiguille GPU usage
- **T1** Check NVLink usage, gates, options display
- **T1** Extract expected gate values

## 4. Mesures et résultats marquants

- **T1** `nvidia-smi nvlink -s : 25,781 Go/s par lien et par sens`
- **T1** `Turing, 16 Go de VRAM chacun : **32 Go au total**, et 25,78 Go/s entre les deux`
- **T1** `> « **les poids restent sur le GPU**. Mesuré : PCIe x8 6,5 Go/s contre 380 Go/s en`
- **T1** `> lecture locale et 20 Go/s sur CPU. Déplacer les poids à chaque jeton coûterait`
- **T1** `**+6 % seulement** sur gpt-oss-120b MXFP4, avec la mention « à ne pas activer par`
- **T1** `du moteur l'annonce lui-même (« `[tête 4 bits] … 0 Mo` »). Les GPU sont au repos`
- **T1** `| VRAM locale (poids résidents) | 380 Go/s | 7 ms/jeton | 10 ms/jeton |`
- **T1** `| lecture CPU (RAM) | 20 Go/s | 133 ms/jeton | 195 ms/jeton |`
- **T1** `| **bus PCIe (x8 mesuré)** | 6,5 Go/s | **411 ms/jeton** | **599 ms/jeton** |`
- **T1** `| disque dur 12 To (ROTA, non caché) | ~200 Mo/s | **13,3 s/jeton** | 19,5 s/jeton |`
- **T1** `au-dessus du plancher PCIe** — il n'est pas limité par la mémoire (133 ms/jeton à`
- **T1** `20 Go/s), mais par le **calcul de déquantification + produit scalaire**.`
- **T1** `25,78 Go/s au lieu de 6,5).`
- **T1** `**411 à 599 ms/jeton de bus** — donc un potentiel de **×5 à ×7** sur l'état actuel.`
- **T1** `3. un **regroupement par expert** par couche (6 experts × 43 couches, avec`
- **T1** `pinned. Le dépôt cite 6,5 Go/s en x8 ; les cartes annoncent x16 Gen3. Si le banc`
- **T1** `donne ≥ 5 Go/s, la piste B vaut ses semaines de travail ; s'il donne 1-2 Go/s, elle`
- **T1** `+6 %, cache RAM d'experts plus lent, épinglage NUMA perdant).`
- **T1** `Qwen2.5-0.5B (2 têtes KV × 64, 7 têtes de requête par tête KV), KV int8, un`
- **T1** `> le découpage en tranches (7,4 ms, 8,9×) ; re-mesurée après, elle vaut **2,36 ms et`
- **T1** `| 256 | 0,25 ms | 0,07 ms | 3,8× | 1,03e-7 |`
- **T1** `| 4 096 | 3,98 ms | **0,14 ms** | **29×** | 1,03e-7 |`
- **T1** `| 65 536 | 65,3 ms | 7,4 ms | 8,9× | 1,03e-7 |`
- **T1** `| **262 144** | 257,9 ms | **6,36 ms** | **40,6×** | 1,03e-7 |`
- **T1** `| 4 096 | 3,88 ms | **0,12 ms** | **31,6×** | 1,60e-7 |`
- **T1** `| 65 536 | 63,06 ms | **2,36 ms** | **26,7×** | 2,13e-7 |`
- **T1** `| **262 144** | 243,82 ms | **6,09 ms** | **40,0×** | 2,25e-7 |`
- **T1** `avec une grille de `n_kv` blocs, le GPU tournait à 1,2 Go/s, presque au repos. Une`
- **T1** `même top-1** (14 divergent), et cela suffit à déplacer la perplexité de 1,2 %. L'hypothèse la plus simple, fortement étayée par ce contraste, est que de`
- **T1** `| GPU, miroir KV seul (`DRAVE_GPU_KV`) | 18,3074 | −1,47 % |`
- **T1** `| GPU, projections seules (`DRAVE_GPU`) | 18,3538 | −1,22 % |`
- **T1** `Ajouter le miroir KV aux projections ne pèse que **0,25 % de plus** : l'essentiel`
- **T1** `(1,22 %) vient du déport des **projections** lui-même. Or les noyaux GPU sont exacts`
- **T1** `1,2 % de perplexité — d'où le doute consigné.`
- **T1** `Le jeton choisi est le même sur 97 % des positions. Les 14 divergences portent un`
- **T1** `C'est cohérent avec l'écart de 0,06 % mesuré à `--ctx 256` (deux fenêtres de 255`
- **T1** `basculements suffisent à déplacer une perplexité de 1 %. La perplexité GPU est`
- **T1** `~500 jetons évalués, en changeant le top-1 sur **3 % des positions** (14 sur 511) —`
- **T1** `# 151 936 jetons, soit 4,6 Gio pour un lot de 32 × 256 positions — pour des`
- **T1** `17:| **experts routés** (16 sur 896) | 25,83 | 29,3 % |`
- **T1** `18:| experts partagés (2 par couche) | 12,40 | 14,1 % |`
- **T1** `19:| **dense Q8_0** (attention, KDA, MLA, routage) | 48,56 | **55,1 %** |`
- **T1** `20:| tête de sortie | 1,30 | 1,5 % |`
- **T1** `27:| 100 % (impossible) | **×1,41** |`
- **T1** `28:| 70 % | ×1,26 |`
- **T1** `29:| 47 % | ×1,16 |`
- **T1** `30:| 25 % | ×1,08 |`
- **T1** `49:| réutilisation immédiate (t−1 → t) | **30,2 %** | 46,9 % |`
- **T1** `50:| LRU 20 experts/couche | **28,7 %** | — |`
- **T1** `51:| LRU 32 | 34,5 % | 86,8 % |`
- **T1** `52:| LRU 128 | 49,8 % | — |`
- **T1** `| attention 1 M de clés, **CPU** (int4, host) | **968 ms** par couche |`
- **T1** `| la même, **KV en VRAM** (`DRAVE_GPU_KV=1`, noyaux `attn_kv_*`) | **13,2 ms** (×73) |`
- **T1** `| « masquer sans réécrire les boucles » en top-k CPU | 12,4 → 12,5 ms : **aucun gain** |`
- **T1** `* sm_75 (Quadro RTX 5000) : 1024 fils par bloc, 48 ko de partagé, pas de`
- **T1** `*Budget mémoire* : 14 têtes × N × 4 octets — 56 Mo à 1 M ✗ trop. **Le tampon ne`
- **T1** `(0,07 ms de 4 k à 262 k clés) — `reports/rapport-gpu-topk-selection.md`.`
- **T1** `doit montrer l'effet cherché : **968 ms → quelques dizaines de ms par couche**.`
- **T1** `| 5 | mesure 1 M : ms/layer avec et sans top-k, sur GPU | ✅ **fait au niveau des noyaux** : la chaîne complète (scores sans relecture + 4 passes + collecte + somme) coûte **3,90 ms** pour 14 lignes × `
- **T1** `Mesuré à 16 384 clés : la chaîne déportée gagne (attention 19,58 → 7,59 ms/jeton,`
- **T1** `balayage −24 %), mais elle coûte **8 lancements et 17 transferts par couche et par`
- **T1** `3. **budgéter le tampon de scores** `nh × n × 4` par couche (56 Mo à 1 M pour`
- **T1** `dénominateur ×45,7 et sortie 55× trop petite à k = 1 ; écart relatif 2,05e-1. Une`
- **T1** `| **16 384** | 4 095 | **2 047** | 19,58 | **7,59** | 12,2267 / **12,2265** | **203,7 / 155,5 s (−24 %)** |`
- **T1** `(4,21 contre 7,68 ms/jeton), à ~2 047 clés le déport gagne nettement (7,59 contre`
- **T1** `chaque appel : 24,5 ms/jeton au lieu de 2,9 », `docs/contexte-long.md` §4.ter) :`
- **T1** `~74 000 lancements pour ces 511 jetons, à comparer aux ~0,1 ms de calcul utile par`
- **T1** `GPU en prend 36 %, à 4 095 clés il est **7,8× plus rapide** (4,97 contre`
- **T1** `38,84 ms/jeton).`
- **T1** `linéairement (+0,0043 ms par clé et par jeton). La perplexité est identique à 2e-5`
- **T1** `| CPU, top-k 256 | 19,0740 | **+2,66 %** : le coût du pruning |`
- **T1** `| GPU, dense (`DRAVE_GPU_KV`) | 18,3074 | −1,47 % vs CPU |`
- **T1** `| GPU, top-k 256 (`DRAVE_GPU_TOPK`) | 18,8391 | **+2,90 %** : même coût |`
- **T1** `| GPU sans miroir KV (`DRAVE_GPU` seul) | 18,3538 | −1,22 % vs CPU |`
- **T1** `1. **le coût du pruning est le même des deux côtés** (+2,7 % CPU, +2,9 % GPU) :`
- **T1** `2. **l'écart CPU/GPU de 1,2 à 1,5 % n'est PAS le miroir KV** (−1,22 % avec les`
- **T1** `seules projections déportées, −1,47 % avec le miroir en plus, soit −0,25 % pour`
- **T1** `sommation diffère — un effet de 0,06 % à ctx 256 sur le même modèle, donc`
- **T1** `| 3 | `attn_topk_somme` : softmax sur les k retenus + puits, puis Σ pondérée des V | ✅ 1,0–4,8e-7 · temps GPU constant (0,07 ms) |`
- **T1** `| 4 | branchement dans `model.rs` (`attn_topk > 0` + miroir VRAM) | ✅ **fait** (opt-in `DRAVE_GPU_TOPK=1`) : PPL identique (9,4162 contre 9,4167 à 2 k ; 12,2265 contre 12,2267 à 4 095 jetons) et **le `
- **T1** `| 5 | mesure 1 M de clés : ms/couche avec et sans top-k | ✅ **fait au niveau des noyaux** : chaîne complète **3,90 ms** pour 14 lignes × 1 M clés contre 539,9 ms d'attention complète CPU (×138) et 13,`
- **T1** `=== mesure experts +6% ===`
- **T1** `REPRISE.md:808:| cache d'experts MXFP4 en VRAM (gpt-oss, 32 jetons) | 5,12 → **5,43 jetons/s (+6 %)**, 53,5 % de succès — verdict : ne pas activer par défaut |`
- **T1** `REPRISE.md:1393:Décomposition des 365,7 Go de V4.1 : **engram 203,4 Go (55,6 %)** · experts`
- **T1** `| 4 096 | **KV déporté** | **12,2175** | **3,29** | **136,2 s** (−38 %) |`
- **T1** `Le poste « attention » devient **plat** (3,3 ms/jeton quelle que soit la`
- **T1** `longueur) là où le CPU croît linéairement : à 32 k il serait à ≈ 180 ms/jeton,`
- **T1** `appel — 24 couches × 6 appels CUDA par jeton, mesuré **24,5 ms/jeton** à 512`
- **T1** `jetons au lieu de 2,9. Les réutiliser a ramené l'attention déportée à 3,2 ms.`
- **T1** `soit ×3,9 au lieu de ×4,5 :`
- **T1** `| CPU | **286,6 s** (13,8 tok/s) | attention **52,6** · matvec+mlp 18,4 |`
- **T1** `| `DRAVE_GPU=1 DRAVE_GPU_KV=1` | **63,8 s** (62,1 tok/s) | attention **2,2** · matvec+mlp 12,8 |`
- **T1** `L'attention du préremplissage est **le** poste dominant sur CPU (73 % du temps :`

## 5. Erreurs rencontrées

2 sorties en erreur ou divergentes. Les premières :

- **T1** : === cfg(test)/mod tests dans gpu.rs === === tests touchant gpu dans les autres .rs === drave-core/src/clusters.rs:299:#[cfg(test)] drave-core/src/engine.rs:942:#[cfg(test)] drave-core/src/engine.rs:98
- **T1** : === portes.sh GPU === === main.rs bancs GPU === 124:        (opt.banc_kv > 0, "--banc-kv"), (opt.banc_topk > 0, "--banc-topk"), 125:        (opt.gpu_banc, "--gpu-banc"), (opt.materiel, "--materiel"), 

