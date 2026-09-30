# Session 8e04c99a — Tu es VÉRIFICATEUR de documentation

| | |
|---|---|
| Identifiant | `8e04c99a-8ba1-4675-9f80-fa3338449b17` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-09-30 18:07 |
| Durée | 0.1 h |
| Tours | 1 |
| Messages | 36 |
| Appels d'outils | 57 |
| Fichiers touchés | 0 |
| Commandes | 48 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu es VÉRIFICATEUR de documentation dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (moteur d'inférence « Drave »). Règle du dépôt : « chaque chiffre publié doit avoir une source, et une valeur affichée est une valeur qui agit ». Ta tâche : confronter les chiffres écrits aujourd'hui dans la documentation aux traces de mesure réelles, et signaler tout écart.  Fichiers écrits ou modifi … [3475 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu es VÉRIFICATEUR de documentation dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (moteur d'inférence «  … [3755 caractères tronqués]

*57 appels d'outils.* Actions notables :

- bash — List repo root and measurement traces
- bash — Show today's git log
- bash — List reports, sprints, docs directories
- read
- bash — Recompute ratios and sums
- bash — Read gate logs and sprint pointer
- bash — Grep README for key numbers
- bash — Show REPRISE lines 480-560
- bash — Print README next-steps section
- bash — Count CUDA kernels and Rust lines
- bash — Check README line-count claim and duplicates
- bash — Show recent commits touching sources
- bash — Diff docs in last commit
- bash — Find line-count methodology references
- … et 35 autres

**Synthèse produite :**

⏵ Recherche de la commande Q4_0 avec --ppl

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** List repo root and measurement traces
- **T1** Show today's git log
- **T1** List reports, sprints, docs directories
- **T1** Recompute ratios and sums
- **T1** Read gate logs and sprint pointer
- **T1** Grep README for key numbers
- **T1** Show REPRISE lines 480-560
- **T1** Print README next-steps section
- **T1** Count CUDA kernels and Rust lines
- **T1** Check README line-count claim and duplicates
- **T1** Show recent commits touching sources
- **T1** Diff docs in last commit
- **T1** Find line-count methodology references
- **T1** Count Rust lines at each commit
- **T1** Show README 368-378 and REPRISE header
- **T1** Check git status, binary, models
- **T1** Locate bench function in main.rs
- **T1** List /tmp logs and grep provenance numbers
- **T1** History of the scores report
- **T1** Show scores report at creation commit
- **T1** Grep digest for scores table numbers
- **T1** Read digest region with scores bench output
- **T1** Grep digest for 27-40 range
- **T1** Grep digest for 27.1x source
- **T1** Read digest around plan edit
- **T1** Find references to the pre-fix logs
- **T1** Inspect uncommitted source changes
- **T1** Check GPU availability
- **T1** Run bench at 4096 keys
- **T1** Run report repro command at 262144
- **T1** Read portes.log, timestamps, 19.3885 origin
- **T1** Read end of bench output code
- **T1** Inspect topk host launch config
- **T1** Check CUDA traps and model gating
- **T1** Find origin of 12840 count
- **T1** Read collecte host code
- **T1** Read digest around 12840 total
- **T1** Find Q4_0 expected gate value
- **T1** Find Q4_0 gate value history
- **T1** Read digest around the 18:00 Q4_0 gate
- … et 8 autres

## 4. Mesures et résultats marquants

- **T1** `dc8a193 Feuille de route : les clés f16 mesurées (+0,018 % pour 39 % de la taille du f32)`
- **T1** `528639c Cache KV : les clés en f16 sont le meilleur réglage mesuré (+0,018 % pour 39 % de la taille)`
- **T1** `255 tokens notés — perplexité cumulée 17.431  (2.5 tok/s)  [fenêtre 1 : 255 notés, PPL 17.431]`
- **T1** `510 tokens notés — perplexité cumulée 19.388  (4.5 tok/s)  [fenêtre 2 : 255 notés, PPL 21.565]`
- **T1** `765 tokens notés — perplexité cumulée 21.374  (6.0 tok/s)  [fenêtre 3 : 255 notés, PPL 25.977]`
- **T1** `255 tokens notés — perplexité cumulée 19.859  (17.9 tok/s)  [fenêtre 1 : 255 notés, PPL 19.859]`
- **T1** `510 tokens notés — perplexité cumulée 21.198  (21.9 tok/s)  [fenêtre 2 : 255 notés, PPL 22.628]`
- **T1** `765 tokens notés — perplexité cumulée 23.671  (24.0 tok/s)  [fenêtre 3 : 255 notés, PPL 29.515]`
- **T1** `255 tokens notés — perplexité cumulée 13.715  (5.1 tok/s)  [fenêtre 1 : 255 notés, PPL 13.715]`
- **T1** `510 tokens notés — perplexité cumulée 15.176  (5.1 tok/s)  [fenêtre 2 : 255 notés, PPL 16.792]`
- **T1** `=== perplexité 15.1757 sur 510 tokens (0 événements, 100.3 s) ===`
- **T1** `162:de blocs entièrement nuls (1 bit par bloc de 64 = 1,6 % de surcoût) est le premier pas.`
- **T1** `397:| **4 bits** (`--q4`, `--q4-tout`) | modèle 4 bits existant (Q4_0) ou débit prioritaire | **41,6 – 44 tok/s** |`
- **T1** `413:requantification), fait tourner un vrai Qwen2.5-0.5B **Q4_0** à **41,6 tok/s**`
- **T1** `514: #    moteur déporte alors tout seul les projections Q8_0 de plus de 8 Mo — le`
- **T1** `503:    sur le CPU où il coûte 968 ms par couche à 1 M de clés, contre 13,2 ms avec le`
- **T1** `516:    streaming des poids depuis le NVMe (3,5 Go/s) pour ce qui ne tient pas en RAM,`
- **T1** `517:    cache d'experts rentable (+6 % aujourd'hui, l'objectif est ≥ +30 %).`
- **T1** `520:    énergie/jeton. Le prototype C mesure 7,79 G événements/s et le croisement`
- **T1** `521:    push/pull (~22 % de densité) — de quoi décider si le mode événementiel vaut le`
- **T1** `./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:32289:- Docs errors corrected: "75 %/50 %" → **64 %/28 %**; crossover "10 %" → **~22 %**; 6-bit reference 19.3045 → **19.5633**; line `
- **T1** `sur le CPU où il coûte 968 ms par couche à 1 M de clés, contre 13,2 ms avec le`
- **T1** `#    moteur déporte alors tout seul les projections Q8_0 de plus de 8 Mo — le`
- **T1** `@@ -77,8 +83,8 @@ doit montrer l'effet cherché : **968 ms → quelques dizaines de ms par couche*`
- **T1** `| 4 | branchement dans `model.rs` (autoriser le GPU quand `attn_topk > 0` **et** que le noyau rend `true`, garder le repli CPU sinon) | perplexité 2 048 = 234,88 ± tolérance |`
- **T1** `| 256 | 0,25 ms | 0,07 ms | 3,8× | 1,03e-7 |`
- **T1** `| 4 096 | 3,98 ms | **0,14 ms** | **29×** | 1,03e-7 |`
- **T1** `| 65 536 | 65,3 ms | 7,4 ms | 8,9× | 1,03e-7 |`
- **T1** `./docs/programme-recherche.md:48:| Moteur d'événements | 5,3 G événements/s, 2 547 lignes de Rust sans dépendance |`
- **T1** `[timed out after 60000ms]`
- **T1** `Qwen2.5-0.5B (2 têtes KV × 64, 7 têtes de requête par tête KV), KV int8, un`
- **T1** `| **262 144** | 257,9 ms | **6,36 ms** | **40,6×** | 1,03e-7 |`
- **T1** `avec une grille de `n_kv` blocs, le GPU tournait à 1,2 Go/s, presque au repos. Une`
- **T1** `4256:     452 tokens notés — perplexité cumulée 3476.367  (4.6 tok/s)  [fenêtre 2 : 226 notés, PPL 3067.009]`
- **T1** `4372:     452 tokens notés — perplexité cumulée 3476.367  (4.6 tok/s)  [fenêtre 2 : 226 notés, PPL 3067.009]`
- **T1** `9130:  GPU  ligne par fil  :     3.6 ms  (  40.6 Go/s)  écart max +2.49e2 (relatif au plus grand logit)`
- **T1** `32095:[262144]   GPU  scores  :     6.36 ms  (40.6× plus rapide)`
- **T1** `32306:- Measured results to reuse: mode 4 lot-en-listes 1 500 B/token vs 3 663 dense (écart 3.03e-2 at 256 tokens, criterion ≤1.5× mode 2's 2.74e-2); lot mode 18× faster over a 20 ms link, 7× per-toke`
- **T1** `banc top-k : 256 clés · 2 têtes KV × 64 dim · 7 têtes de requête par tête KV · KV 8 bits`
- **T1** `CPU  20 fils :     0.25 ms`
- **T1** `GPU  scores  :     0.07 ms  (3.8× plus rapide)`
- **T1** `[4096]   CPU  20 fils :     3.98 ms`
- **T1** `[4096]   GPU  scores  :     0.46 ms  (8.6× plus rapide)`
- **T1** `[65536]   CPU  20 fils :    65.29 ms`
- **T1** `[65536]   GPU  scores  :     7.36 ms  (8.9× plus rapide)`
- **T1** `[262144]   CPU  20 fils :   259.05 ms`
- **T1** `[262144]   GPU  scores  :    27.58 ms  (9.4× plus rapide)`
- **T1** `[4096]   GPU  scores  :     0.14 ms  (29.3× plus rapide)`
- **T1** `[262144]   CPU  20 fils :   257.88 ms`
- **T1** `[262144]   GPU  scores  :     6.36 ms  (40.6× plus rapide)`
- **T1** `CPU  20 fils :     3.88 ms`
- **T1** `GPU  scores  :     0.12 ms  (31.6× plus rapide)`
- **T1** `CPU  20 fils :    63.06 ms`
- **T1** `GPU  scores  :     2.36 ms  (26.7× plus rapide)`
- **T1** `CPU  20 fils :   243.82 ms`
- **T1** `GPU  scores  :     6.09 ms  (40.0× plus rapide)`
- **T1** `6:tailles testées) et coûte **0,89 ms** là où le tri CPU en coûte **497 ms** à`
- **T1** `reports/rapport-gpu-scores.md:27:| 256 | 0,25 ms | 0,07 ms | 3,8× | 1,03e-7 |`
- **T1** `reports/rapport-gpu-scores.md:28:| 4 096 | 3,98 ms | **0,14 ms** | **29×** | 1,03e-7 |`
- **T1** `reports/rapport-gpu-scores.md:29:| 65 536 | 65,3 ms | 7,4 ms | 8,9× | 1,03e-7 |`
- **T1** `reports/rapport-gpu-scores.md:30:| **262 144** | 257,9 ms | **6,36 ms** | **40,6×** | 1,03e-7 |`
- **T1** `./reports/rapport-gpu-scores.md:35:| 256 | 0,25 ms | 0,07 ms | 3,8× | 1,03e-7 |`
- **T1** `./reports/rapport-gpu-scores.md:36:| 4 096 | 3,98 ms | **0,14 ms** | **29×** | 1,03e-7 |`
- **T1** `./reports/rapport-gpu-scores.md:37:| 65 536 | 65,3 ms | 7,4 ms | 8,9× | 1,03e-7 |`
- **T1** `./reports/rapport-gpu-scores.md:38:| **262 144** | 257,9 ms | **6,36 ms** | **40,6×** | 1,03e-7 |`
- **T1** `Quadro RTX 5000, 1383 MiB, 24 %`
- **T1** `Quadro RTX 5000, 381 MiB, 27 %`
- **T1** `CPU  tri + comptage :     1.22 ms`
- **T1** `GPU  4 passes d'histogramme :     0.14 ms  (9.0× plus rapide)`
- **T1** `collecte GPU     0.21 ms · CPU tri complet     3.94 ms (19.2× plus rapide)`
- **T1** `[sondes] 1 passe = 0.0374 ms, ok = true`
- **T1** `second passage k = 512, mêmes tampons : 14/14 lignes · 0.0001 ms (0.0001 ms de seuil) · cases non écrites 0`
- **T1** `CPU  20 fils :   239.31 ms`
- **T1** `GPU  scores  :     6.43 ms  (37.2× plus rapide)`
- **T1** `CPU  tri + comptage :    96.42 ms`
- **T1** `GPU  4 passes d'histogramme :     0.44 ms  (217.0× plus rapide)`
- **T1** `collecte GPU     0.44 ms · CPU tri complet   389.41 ms (878.1× plus rapide)`
- **T1** `[sondes] 1 passe = 0.0809 ms, ok = true`
- **T1** `second passage k = 512, mêmes tampons : 14/14 lignes · 0.0004 ms (0.0003 ms de seuil) · cases non écrites 0`
- **T1** `part de l'attention dans le flux d'événements : 100.0 %`
- **T1** `410:=== perplexité 19.3885 sur 510 tokens (0 événements, 17.2 s) ===`
- **T1** `2027:=== perplexité 19.3885 sur 510 tokens (0 événements, 16.1 s) ===`
- **T1** `5478:=== perplexité 19.3885 sur 510 tokens (0 événements, 16.0 s) ===`
- **T1** `drave-core/gpu/cuda_stub.h:55:    asm volatile("atom.global.add.u32 %0, [%1], %2;" : "=r"(ancien) : "l"(p), "r"(v) : "memory");`
- **T1** `drave-core/gpu/cuda_stub.h:62:    asm volatile("cvta.to.shared.u64 %0, %1;" : "=l"(adresse) : "l"(p));`
- **T1** `drave-core/gpu/cuda_stub.h:64:    asm volatile("atom.shared.add.u32 %0, [%1], %2;"`
- **T1** `359:| Qwen2.5-0.5B | Q4_0 | 21,01 | 39 tok/s | 0,41 Go |`
- **T1** `31313:       7 tokens notés — perplexité cumulée 821.198  (21.8 tok/s)`
- **T1** `33635:     510 tokens notés — perplexité cumulée 21.198  (21.9 tok/s)  [fenêtre 2 : 255 notés, PPL 22.628]`
- **T1** `33764:     510 tokens notés — perplexité cumulée 21.198  (21.9 tok/s)  [fenêtre 2 : 255 notés, PPL 22.628]`
- **T1** `CPU  tri + comptage :     1.29 ms`
- **T1** `GPU  4 passes d'histogramme :     0.15 ms  (8.7× plus rapide)`
- **T1** `collecte GPU     0.14 ms · CPU tri complet     4.31 ms (30.0× plus rapide)`
- **T1** `collecte GPU     0.15 ms · CPU tri complet     4.30 ms (29.0× plus rapide)`
- **T1** `3663:=== perplexité 15.1757 sur 510 tokens (0 événements, 98.0 s) ===`
- **T1** `5619:=== perplexité 15.1757 sur 510 tokens (0 événements, 97.3 s) ===`
- **T1** `GPU  scores  :    61.36 ms  (12.9× plus rapide)`
- **T1** `CPU  tri + comptage :    27.12 ms`
- **T1** `GPU  4 passes d'histogramme :     0.74 ms  (36.5× plus rapide)`
- **T1** `collecte GPU     0.36 ms · CPU tri complet    16.55 ms (46.1× plus rapide)`
- **T1** `31489:AUTRES : (3) plafond R4 = par message, pas par session : 8 flux de 35,4 Mo (282,9 Mo cumulés > 256) tous acceptés — mais la RAM ne s'accumule PAS (RSS 593 Mo stable, HWM 698 Mo) ; la vérif du cu`

