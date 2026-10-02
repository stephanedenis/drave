# Session 56879594 — Tu travailles dans le dépôt

| | |
|---|---|
| Identifiant | `56879594-1434-4e34-83cc-de42cdf192a1` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-02 15:03 |
| Durée | 0.1 h |
| Tours | 1 |
| Messages | 17 |
| Appels d'outils | 29 |
| Fichiers touchés | 0 |
| Commandes | 8 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave », moteur d'inférence LLM en Rust qui exécute les projections sous forme de listes d'activation creuses plutôt que de produits scalaires denses).  TÂCHE : dépouille EXHAUSTIVEMENT ces 20 fichiers Markdown : reports/rapport-empreinte-memoire.md reports/rapport-encodage.md reports/rapport-eparsite.md reports/ … [3026 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave », moteur d'inférence LLM en … [3306 caractères tronqués]

*29 appels d'outils.* Actions notables :

- bash — Count lines in the 20 reports
- read
- bash — List backticked file paths in reports
- bash — List repo-relative paths cited in reports
- bash — Find first occurrence of each term
- bash — Locate env vars and remaining terms
- bash — Check terms restricted to the 20 files
- bash — Print exact lines for key claims
- bash — Spot-check remaining key lines
- send_message

**Synthèse produite :**

⏵ Inventory delivered; reporting completion.

L'inventaire complet (sections A à D, format demandé) vient d'être envoyé à l'agent parent `3d5618a0-4e3a-45bb-943d-a72c753fb7da` via `send_message`. Il est self-contained : aucune lecture de mon transcript n'est nécessaire.

Contenu transmis, en résumé de structure :
- **A. Termes et sigles** — ~110 entrées (sigles MLA/MoE/MXFP4/IQ*/Q4_K/GQA/RSS/PTX/AVX2/NUMA…, algorithmes Sinkhorn/RoPE/YaRN/SwiGLU/radix select/Jaccard/Gini/Heaps, matériel FPGA/ALM/M20K/DDR3/PCIe/Stratix/Xeon/Quadro, vocabulaire projet engram/grappe/push-pull/porte/mode 2-3-4/greffon/seuil_push/aiguillage, métriques perplexité/NLL/p50-p99/TTFT, formats GGUF/QPAT/mapping.tsv, variables `DRAVE_*`), chacune avec définition, outil/fichier d'usage et première occurrence `reports/fichier.md:ligne` — plus la liste explicite des termes demandés mais **absents** (AER, DRVF v5, TLB, HBM, LoRA, MTP, Hadamard, GFLOPS, MTok/s, aiguille…).
- **B. Chiffres et affirmations mesurées** — ~180 lignes de citations exactes horodatées par `fichier:ligne`, fichier par fichier.
- **C. Contradictions et chiffres périmés** — ~55 entrées, dont les plus exploitables : « top-k pas encore branché » vs « ✅ fait » (`rapport-gpu-topk-selection.md:347` vs `:343`), 0,89 ms/497 ms introuvables dans les tableaux du même rapport, 8/6/9 lancements contradictoires, réductibilité « uniforme » vs « non uniforme » (`rapport-empreinte-memoire.md:200` vs `:369`), cache 8 entrées « à rien » vs « 27–52 % », mmap « pas fait » vs « implémenté » (`rapport-lecteur-multifichiers.md:267` vs `:171`), 38 % vs 30 % vs numpy, 10,5/10,6 tok/s vs 10,3/10,0, tableau GLM 53+22+4+1 = 80 couches pour 79, 53 s vs 190 s/jeton, ÷2,3 vs ÷2,2 (mode 4), « 4971.00 % » d'accuracy (`rapport-encodage.md:42`), gpt-oss « 4 experts » vs « top-8 », sommes 984/1 138 Go invérifiables.
- **D. Fichiers du dépôt cités** — ~40 chemins (`drave-core/gpu/drave_gpu.cu`, `cuda_stub.h`, `src/*.rs`, `src/bpe_np.py`, `docs/plan-gpu-topk.md`, `docs/contexte-long.md`, `REPRISE.md`, `tools/*`, `run_*.py`, artefacts `commun.gguf`/`cluster-*.gguf`/`mapping.tsv`, `journal/`, `qwen3-30b-8clusters-v2`) avec leur rôle d'après le texte.

Aucun fichier du dépôt n'a été modifié : seules des lectures et des commandes de recherche (`grep`, `sed`, `wc`) ont été exécutées.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** Count lines in the 20 reports
- **T1** List backticked file paths in reports
- **T1** List repo-relative paths cited in reports
- **T1** Find first occurrence of each term
- **T1** Locate env vars and remaining terms
- **T1** Check terms restricted to the 20 files
- **T1** Print exact lines for key claims
- **T1** Spot-check remaining key lines

## 4. Mesures et résultats marquants

- **T1** `DRAVE_PRELIRE_TOUT     rapport-execution-v41.md:19:| passe avant (`--ppl`) | `DRAVE_PRELIRE_TOUT=1 DRAVE_GPU=1` | **refusée en 0,33 s**, RSS 47 Mo |`
- **T1** `Gini                   rapport-empreinte-memoire.md:194:| | 90 % | 99 % | Gini |`
- **T1** `Heaps                  rapport-empreinte-memoire.md:64:Exposant de Heaps ≈ **0,21** : la couverture croît très lentement. Atteindre 50 %`
- **T1** `TurboSparse            rapport-localite-activation.md:17:TurboSparse (≈ 90 % de creux) est *entraîné* ainsi, précisément parce`
- **T1** `BitNet b1.58           rapport-eparsite.md:70:- La densité naturelle (26.3 %) est propre à ce modèle. Un modèle **entraîné** en ternaire (BitNet b1.58) tourne plutôt autour de 50-70 % de non-nuls : le`
- **T1** `TTFT                   rapport-inference.md:83:| TTFT | 74–95 ms |`
- **T1** `M20K                   bilan-multi-materiel.md:95:| « 27 PE suffisent, 3 % de la logique » | **Corrigée** — en comptant le lecteur : 51 voies, 41 % de la logique et 41 % de la M20K |`
- **T1** `ALM                    bilan-multi-materiel.md:66:3. **Pas de multiplieur requis.** Le PE atteint 112,5 MHz avec 176 ALMs **et zéro`
- **T1** `DSP                    bilan-multi-materiel.md:67:   DSP**, contre 115 ALMs et 1 DSP avec multiplieur — et **pas un hertz d'écart**.`
- **T1** `Stratix                bilan-multi-materiel.md:8:RTX 5000 (16 Go, NVLink 25,78 Go/s), 1 carte Stratix V GS (Storey Peak,`
- **T1** `DRAVE_GPU              rapport-execution-v41.md:19:| passe avant (`--ppl`) | `DRAVE_PRELIRE_TOUT=1 DRAVE_GPU=1` | **refusée en 0,33 s**, RSS 47 Mo |`
- **T1** `ALM                    rapport-eparsite.md:64:4. **Le vrai obstacle n'est pas le poids, c'est l'activation** : un événement n'existe que si le poids *et* l'activation sont non nuls (ici 13.9 % d'événe`
- **T1** `BitNet                 rapport-eparsite.md:70:- La densité naturelle (26.3 %) est propre à ce modèle. Un modèle **entraîné** en ternaire (BitNet b1.58) tourne plutôt autour de 50-70 % de non-nuls : le`
- **T1** `Wanda                  rapport-eparsite.md:71:- La littérature (SparseGPT, Wanda) situe l'élagage non structuré *one-shot* des LLM à 50-60 % sans réentraînement, et le 2:4 structuré (50 %) est la form`
- **T1** `SparseGPT              rapport-eparsite.md:71:- La littérature (SparseGPT, Wanda) situe l'élagage non structuré *one-shot* des LLM à 50-60 % sans réentraînement, et le 2:4 structuré (50 %) est la form`
- **T1** `non pas en découpant les experts mais parce que **56 % du modèle (203 Go) est une`
- **T1** `10 000 jetons n'en touche que **4,6 Mo**.`
- **T1** `| couche | 90 % | 99 % |`
- **T1** `experts, un cache ne sert **à rien** (0 % de succès — un jeton consomme ses 8`
- **T1** `entrées, prédiction gratuite — sert 27 à 52 % des appels. Mais un LRU de 32 fait`
- **T1** `**78 %** : la localité temporelle est réelle et insuffisante.`
- **T1** `| | experts pour 90 % |`
- **T1** `+1,2 % au mieux.`
- **T1** `| cache d'experts 25 % (32 par couche) | 1,82 Go | mesuré, à écrire |`
- **T1** `| tête restreinte à la langue | **0,70 Go** | mesuré (top-1 à 99,2 %) |`
- **T1** `| VRAM (2 Quadro, 32 Go) | 3 200 experts = 21 % du total | `CacheExperts` existe |`
- **T1** `| experts (40 couches) | 152,9 Go | 38 à 71 Go (cache de 25 à 90 %) | 1 / 4 à 1 / 2 |`
- **T1** `chaque appel : 24,5 ms/jeton au lieu de 2,9 », `docs/contexte-long.md` §4.ter) :`
- **T1** `~74 000 lancements pour ces 511 jetons, à comparer aux ~0,1 ms de calcul utile par`
- **T1** ``nh × n × 4` du plan disparaît.`
- **T1** `| 3 | `attn_topk_somme` : softmax sur les k retenus + puits, puis Σ pondérée des V | ✅ 1,0–4,8e-7 · temps GPU constant (0,07 ms) |`
- **T1** `| 4 | branchement dans `model.rs` (`attn_topk > 0` + miroir VRAM) | ✅ **fait** (opt-in `DRAVE_GPU_TOPK=1`) : PPL identique (9,4162 contre 9,4167 à 2 k ; 12,2265 contre 12,2267 à 4 095 jetons) et **le `
- **T1** `| 5 | mesure 1 M de clés : ms/couche avec et sans top-k | ✅ **fait au niveau des noyaux** : chaîne complète **3,90 ms** pour 14 lignes × 1 M clés contre 539,9 ms d'attention complète CPU (×138) et 13,`
- **T1** `coïncident. Il fallait un nœud partiel dont le cluster chargé n'est pas le rang 0.`
- **T1** `| **Débit de génération** | **10,5 tok/s** (int16) · 10,6 (int8) · **11,4 en dense** |`
- **T1** `| Temps par token | 100 ms = 90 ms de forward + 10 ms de tête |`
- **T1** `4. Elle est **30 % plus rapide que numpy + OpenBLAS** sur le même modèle, sur le même`
- **T1** `| **mode 4, lots de 16** | **1,5 ko** (contre 3,5 en lot dense) | **3,03e-2** |`
- **T1** `> le découpage en tranches (7,4 ms, 8,9×) ; re-mesurée après, elle vaut **2,36 ms et`
- **T1** `| 2.00 | 4971.00 % | 5.5 | dense ternaire (référence CDC) |`
- **T1** `| 2 bits | 50.9 % | 27.5 % |`
- **T1** `| 3 bits | 51.3 % | 44.1 % | 27.5 % |`
- **T1** `| 4 bits | 51.5 % | 48.1 % | 42.8 % | 27.5 % |`
- **T1** `même top-1** (14 divergent), et cela suffit à déplacer la perplexité de 1,2 %. L'hypothèse la plus simple, fortement étayée par ce contraste, est que de`
- **T1** `61 couches MLA, routage sigmoïde ×2,827, 384 experts dont 8 par jeton.`
- **T1** `| 4 096 | 14/14 | 14/14 | 14/14 | **0** | 0,14 ms (9×) | 1,31 ms | 0,13 ms (35×) | 4,33 ms |`
- **T1** `| 65 536 | 14/14 | 14/14 | 14/14 | **0** | 0,32 ms (69×) | 22,17 ms | 0,34 ms (258×) | 86,53 ms |`
- **T1** `| 262 144 | 14/14 | 14/14 | 14/14 | **0** | 0,44 ms (224×) | 97,88 ms | 0,45 ms (896×) | 399,21 ms |`
- **T1** `2. **La tête restreinte par langue** : −30 % de trafic, le top-1 y est toujours.`
- **T1** `Écart : **−0,4 %** — la qualité est préservée. (La valeur absolue plus élevée que les`

