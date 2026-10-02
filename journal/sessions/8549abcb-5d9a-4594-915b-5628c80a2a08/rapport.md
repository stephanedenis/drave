# Session 8549abcb — Tu travailles dans le dépôt

| | |
|---|---|
| Identifiant | `8549abcb-5d9a-4594-915b-5628c80a2a08` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-02 15:03 |
| Durée | 0.1 h |
| Tours | 1 |
| Messages | 20 |
| Appels d'outils | 28 |
| Fichiers touchés | 0 |
| Commandes | 6 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave », moteur d'inférence LLM en Rust qui exécute les projections sous forme de listes d'activation creuses plutôt que de produits scalaires denses).  TÂCHE : dépouille EXHAUSTIVEMENT ces 20 fichiers Markdown : reports/rapport-optimisations-auto.md reports/rapport-optimisations.md reports/rapport-p0-flux.md rep … [3059 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave », moteur d'inférence LLM en … [3339 caractères tronqués]

*28 appels d'outils.* Actions notables :

- read
- bash — Compute first occurrence of key terms
- bash — Extract repo file paths cited in reports
- bash — Verify key numeric citations across reports
- bash — Check IQ, porte, indexeur terminology lines
- bash — Locate project jargon and CLI flags
- bash — Verify last batch of terms
- send_message

**Synthèse produite :**

⏵ Inventory complete and delivered to the parent agent

The exhaustive inventory of the 20 reports is complete (no repo file modified — reads and greps only), and both halves were sent to `3d5618a0-4e3a-45bb-943d-a72c753fb7da`:

- **Partie 1/2** — `## A. Termes et sigles` (~130 entrées, chacune avec définition, usage/outil, première occurrence `reports/fichier.md:ligne`) et `## B. Chiffres et affirmations mesurées` (une ligne par mesure, citation exacte, ~280 entrées).
- **Partie 2/2** — `## C. Contradictions, chiffres périmés, affirmations douteuses` (35 entrées) et `## D. Fichiers du dépôt cités` (~35 chemins + tenseurs GGUF + fichiers temporaires + référence externe llama.cpp).

Points saillants remontés au parent :

1. **Faux départs auto-signalés** : `19,3045 → 19,5633`, « rejeu v3 = 19,3885 » faux positif, chiffres périmés `11,737136 / 125 133` (remplacés par 11,077944 / 64 727,68), `×2,17` de l'unaires déclaré FAUX mais réaffirmé.
2. **Contradictions inter-rapports** : porte gpt-oss 15,1757 vs 15,6017 ; V4.1 = 341 Go vs 365 Go ; débit atteint 10,4 vs 20–25 Go/s ; Qwen 0.5B 32 vs 41,6 tok/s ; prédictions tok/s ~2× les mesures ; GLM-5.3 « exécuté » (p0-flux) vs « jamais exécuté, MLA à rang faible manquante » (routage-experts) ; mode 4 livré vs « spécifié, pas écrit » ; « cinq fois » vs « huit fois » vs « 46 sur 110 » ; 13/13 vs 35 tests.
3. **Incohérences internes** : totaux GLM-5.3 58,2 G vs 83,1 G dans le même rapport ; défaut de threads `3/4 × CPU` vs cœurs physiques ; 0,97 G év/s attribué à deux causes ; E2M1 `{0,1,2,3,4,6,8,12}` vs `{0,½,1,1½,2,3,4,6}` ; 90 Ko/jeton ≠ 96,6 Go à 1 M ; 1 629 vs 1 589 vs 1 568 octets/flux ; vocabulaire 16 384 ne pouvant contenir 19 793 identifiants distincts.
4. **Termes attendus mais absents** des 20 fichiers : DRVF/DRVF v5, PTX, RSS, IQ2_XXS, HBM, M20K, greffon, liste valuée, shard, p50/p95, MTok/s, Gbit/s, bf16, Hadamard, LoRA, MTP.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** Compute first occurrence of key terms
- **T1** Extract repo file paths cited in reports
- **T1** Verify key numeric citations across reports
- **T1** Check IQ, porte, indexeur terminology lines
- **T1** Locate project jargon and CLI flags
- **T1** Verify last batch of terms

## 4. Mesures et résultats marquants

- **T1** `'MLA'                        reports/rapport-optimisations-auto.md:56  | Mesuré : le KV de MLA de V4.1 pèse **90 Ko par jeton en F16**, soit 96,6 Go à 1 M`
- **T1** `'TLB'                        reports/rapport-passage-a-l-echelle.md:160  | TLB. Des pages de 2 Mo diviseraient ce coût par 512.`
- **T1** `'DDR3'                       reports/rapport-precision.md:63  | passante. Le débit est fixé par la DDR3 (9,66 Go/s) ; 312 voies suffisent à la`
- **T1** `'DDR4'                       reports/rapport-passage-a-l-echelle.md:152  | Nous atteignons 20–25 Go/s là où deux sockets DDR4-2133 en offrent ~136. Les`
- **T1** `'PCIe'                       reports/rapport-optimisations-auto.md:17  | | **NVLink** | `nvidia-smi nvlink -s` | 25,8 Go/s, 2× le PCIe |`
- **T1** `'NVLink'                     reports/rapport-optimisations-auto.md:17  | | **NVLink** | `nvidia-smi nvlink -s` | 25,8 Go/s, 2× le PCIe |`
- **T1** `'QSFP'                       reports/rapport-passage-a-l-echelle.md:179  | | QSFP+ 4,8 Go/s, NVLink 25,78 Go/s, PCIe x8 6,5 Go/s | le flux d'événements adressé par destination est un pr`
- **T1** `'madvise'                    reports/rapport-optimisations-auto.md:79  | | `madvise(WILLNEED)` après le routage (experts) | 25,73 s contre 25,80 | 0,3 % |`
- **T1** `'WILLNEED'                   reports/rapport-optimisations-auto.md:79  | | `madvise(WILLNEED)` après le routage (experts) | 25,73 s contre 25,80 | 0,3 % |`
- **T1** `'sched_yield'                reports/rapport-optimisations.md:122  | 8 threads) : `sched_yield` est un appel système, et un worker qui attend 1 ms en`
- **T1** `'perplexité'                 reports/rapport-optimisations-auto.md:117  | modèle (densité 5,1 % ⇒ perplexité ×107). Détail dans`
- **T1** `'tok/s'                      reports/rapport-passage-a-l-echelle.md:47  | par jeton ÷ 20 Go/s = **13 ms/jeton = 41 tok/s**, contre **41,6 tok/s mesurés**.`
- **T1** `'Go/s'                       reports/rapport-optimisations-auto.md:17  | | **NVLink** | `nvidia-smi nvlink -s` | 25,8 Go/s, 2× le PCIe |`
- **T1** `'débit'                      reports/rapport-optimisations-auto.md:89  | 20 fils. Le mmap paresseux atteint déjà 2,7 Go/s, proche du débit séquentiel du`
- **T1** `"densité d'activation"       reports/rapport-passage-a-l-echelle.md:39  | | listes d'événements (`PushMat`) | **1,98** | densité d'activation < 22 % |`
- **T1** `'Q8_0'                       reports/rapport-optimisations.md:4  | Matrice réelle `blk.0.ffn_gate.weight` de Qwen2.5-0.5B-Q8_0 : 4864 entrées × 896`
- **T1** `'tuilage'                    reports/rapport-passage-a-l-echelle.md:178  | | l'accumulateur décide du débit en régime creux (mesuré : ×1,7 entre 4 et 32 threads sur des événements épars`
- **T1** `'bitmap'                     reports/rapport-optimisations.md:38  | séparées. Le bitmap+signe reste à 1,09 Mo (1,99 b/poids), mais impose un parcours`
- **T1** `'protocole'                  reports/rapport-passage-a-l-echelle.md:179  | | QSFP+ 4,8 Go/s, NVLink 25,78 Go/s, PCIe x8 6,5 Go/s | le flux d'événements adressé par destination est un pr`
- **T1** `'proxy'                      reports/rapport-prefill-reparti.md:53  | `tools/proxy_latence.py` ajoute 20 ms par message, comme le ferait un lien`
- **T1** `reports/rapport-session-2026-09-30.md:14:| **Transport en listes** | dense 3 663 octets → **1 629** par flux (÷2,3) pour 1,3 % d'écart à 1 024 jetons | `rapport-transport-liste.md` |`
- **T1** `reports/rapport-transport-liste.md:152:| **1 024** | **1,32e-2** | **1 589** | 79,8 % |`
- **T1** `reports/rapport-transport-liste.md:4:3 623** à seuil 5 %, et **1 568** avec des indices par écarts — mais jeter des`
- **T1** `reports/rapport-transport-liste.md:182:3 623 à 1 568 octets, soit **÷2,3**, pour 2,7 % d'écart sur 256 jetons de vrai`
- **T1** `reports/rapport-transport-liste.md:25:| dense f32 | 100 % | 3 623 | 3 623 | 144,8289 | **144,8289** | **0,00e0** |`
- **T1** `reports/rapport-transport-liste.md:26:| listes 0,00 | 100,0 % (896) | 3 623 | 3 623 | 144,8289 | 141,0539 | 2,6e-2 |`
- **T1** `reports/rapport-transport-liste.md:132:| dense f32 | — | 100 % | 3 623 | **0,00e0** |`
- **T1** `reports/rapport-optimisations-auto.md:56:Mesuré : le KV de MLA de V4.1 pèse **90 Ko par jeton en F16**, soit 96,6 Go à 1 M`
- **T1** `=== 90 Ko`
- **T1** `=== 9,66 Go/s`
- **T1** `reports/rapport-precision.md:63:   passante. Le débit est fixé par la DDR3 (9,66 Go/s) ; 312 voies suffisent à la`
- **T1** `=== 10,4 Go/s`
- **T1** `reports/rapport-programme-evolutif.md:102:10,4 Go/s alors que la machine en offre 28,7 : il est **borné par le calcul de`
- **T1** `reports/rapport-tete-restreinte.md:95:| 0,02 | 30,3 % | 28,7635 | +48 % |`
- **T1** `reports/rapport-passage-a-l-echelle.md:47:par jeton ÷ 20 Go/s = **13 ms/jeton = 41 tok/s**, contre **41,6 tok/s mesurés**.`
- **T1** `reports/rapport-passage-a-l-echelle.md:56:| Qwen2.5-0.5B (dense) | 0,49 G | 0,26 Go | 13 ms | **41,6** (mesuré) |`
- **T1** `=== 32 tok/s`
- **T1** `reports/rapport-travail-reel.md:48:| Débits mesurés | 0,5 B : 32 tok/s · 1,5 B : 17 · 30 B MoE : **5,6** · 7 B : 2,8 |`
- **T1** `=== 5,62 tok/s`
- **T1** `reports/rapport-travail-reel.md:22:(**5,62 tok/s**), premier jeton en 166 ms.`
- **T1** `reports/rapport-p0-flux.md:62:| partagé | **5,6 G** | 9,7 % |`
- **T1** `reports/rapport-prefill-par-lots.md:137:   le déport GPU (`DRAVE_GPU_TETE=1`, déjà mesuré à 6,2 ms/jeton contre 15,6 pour`
- **T1** `reports/rapport-prefill-reparti.md:76:| **un seul lot de 256** | 4 255,6 ms | **16,6 ms** |`
- **T1** `reports/rapport-transport-liste.md:191:| calcul local (12 couches) | 15,6 ms/jeton | 15,9 ms/jeton |`
- **T1** `reports/rapport-parcimonie-imposee.md:34:| 0,5 % | 312,3 M (−11,5 %) | 20,1511 | 1,05× |`
- **T1** `reports/rapport-passage-a-l-echelle.md:60:| **Qwen3-30B-A3B** (MoE) | 3,3 G | 1,7 Go | 87 ms | **11,5** |`
- **T1** `reports/rapport-session-2026-09-30.md:20:| **Colab prêt** | dépôt en un fichier (4,5 Mo), notebook (texte réel : perplexité ~20 au lieu de 17 869), trois voies de tunnel — vérifié de bout en bout | `c`
- **T1** `reports/rapport-passage-a-l-echelle.md:58:| DeepSeek-R1-Distill-14B | 14 G | 7,4 Go | 370 ms | 2,7 |`
- **T1** `reports/rapport-v4-couches-0-1.md:91:**NLL moyenne 11,077944 · perplexité 64 727,68**. C'est le chiffre auquel la`
- **T1** `reports/rapport-routage-experts.md:75:déplacé la porte Qwen3-30B de 799,8557 à 799,8152 (−0,005 %). Cause : la`
- **T1** `nope  ==>  reports/rapport-v4-hca.md:52:tournée) alors que les **448 premières** (nope) étaient justes à 0,4 %. Signature`
- **T1** `ape  ==>  reports/rapport-optimisations.md:156:   FPGA à 124 MHz × 32 PEs taperait 4 G év/s — la carte gagne par le watt, pas par`
- **T1** `R4  ==>  reports/rapport-passage-a-l-echelle.md:152:Nous atteignons 20–25 Go/s là où deux sockets DDR4-2133 en offrent ~136. Les`
- **T1** `mode 2  ==>  reports/rapport-prefill-reparti.md:107:soit ÷2,3 sur le fil à 2,7 % d'écart — la même recette que le mode 2, répétée par`
- **T1** `PushMat  ==>  reports/rapport-passage-a-l-echelle.md:39:| listes d'événements (`PushMat`) | **1,98** | densité d'activation < 22 % |`
- **T1** `DenseQ8  ==>  reports/rapport-passage-a-l-echelle.md:40:| int8 dense (`DenseQ8`) | 1,00 | densité > 22 % |`
- **T1** `DRAVE_KV_K_F16  ==>  reports/rapport-placement-bits-kv.md:64:   Autrement dit : `DRAVE_KV_BITS=8 DRAVE_KV_K_F16=1` donne un cache à **39 % de la`
- **T1** `DRAVE_KV_K_F32  ==>  reports/rapport-placement-bits-kv.md:56:   rogner les valeurs. `DRAVE_KV_K_F32=1` (clés f32, valeurs int8) donne 64 % de`
- **T1** `DRAVE_GPU_KV  ==>  reports/rapport-placement-bits-kv.md:137:| contexte long **avec** `DRAVE_GPU_KV=1` | **int8/int8** (28 %, +3,04 %) ou f32/f32 | le miroir exige une disposition homogène ; il divise `
- **T1** `DRAVE_GPU_TETE  ==>  reports/rapport-prefill-par-lots.md:137:   le déport GPU (`DRAVE_GPU_TETE=1`, déjà mesuré à 6,2 ms/jeton contre 15,6 pour`
- **T1** `--tete-restreinte  ==>  reports/rapport-optimisations-auto.md:122:**`--tete-restreinte`** : +10,5 % (liste française) à +15 % (anglaise), mais la`
- **T1** `numactl  ==>  reports/rapport-passage-a-l-echelle.md:165:Test NUMA préliminaire (8 threads, `numactl`) : repère 20,7 → **24,7 Go/s** en`
- **T1** `banc  ==>  reports/rapport-optimisations.md:155:2. **3–5 G év/s sur un CPU de bureau**, soit ~1 événement par cycle. Un banc`
- **T1** `DRAVE_GPU  ==>  reports/rapport-placement-bits-kv.md:137:| contexte long **avec** `DRAVE_GPU_KV=1` | **int8/int8** (28 %, +3,04 %) ou f32/f32 | le miroir exige une disposition homogène ; il divise le `
- **T1** `MLP  ==>  reports/rapport-precision.md:3:Modèle minimal (MLP 32→64→10, 2688 poids), référence float **76.07 %**.`
- **T1** `312 voies  ==>  reports/rapport-precision.md:63:   passante. Le débit est fixé par la DDR3 (9,66 Go/s) ; 312 voies suffisent à la`
- **T1** `Heaps  ==>  reports/rapport-tete-restreinte.md:21:Exposant de Heaps ≈ **0,21** : atteindre 50 % du vocabulaire demanderait des`
- **T1** `notebook  ==>  reports/rapport-session-2026-09-30.md:20:| **Colab prêt** | dépôt en un fichier (4,5 Mo), notebook (texte réel : perplexité ~20 au lieu de 17 869), trois voies de tunnel — vérifié de bo`
- **T1** `tunnel  ==>  reports/rapport-session-2026-09-30.md:20:| **Colab prêt** | dépôt en un fichier (4,5 Mo), notebook (texte réel : perplexité ~20 au lieu de 17 869), trois voies de tunnel — vérifié de bout`
- **T1** `Mo   ==>  reports/rapport-optimisations.md:37:Coût : 4,89 Mo (8,97 b/poids) contre 4,34 Mo (7,98 b/poids) pour les deux listes`
- **T1** `Ko   ==>  reports/rapport-optimisations-auto.md:56:Mesuré : le KV de MLA de V4.1 pèse **90 Ko par jeton en F16**, soit 96,6 Go à 1 M`
- **T1** `esc  ==>  reports/rapport-placement-bits-kv.md:40:centièmes de pour cent. Descendre plus bas coûte cher d'un coup — 33 % pour`

