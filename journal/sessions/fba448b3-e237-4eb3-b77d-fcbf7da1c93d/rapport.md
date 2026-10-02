# Session fba448b3 — Tu travailles dans le dépôt

| | |
|---|---|
| Identifiant | `fba448b3-e237-4eb3-b77d-fcbf7da1c93d` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-02 15:03 |
| Durée | 0.1 h |
| Tours | 1 |
| Messages | 19 |
| Appels d'outils | 26 |
| Fichiers touchés | 0 |
| Commandes | 3 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave », moteur d'inférence LLM en Rust qui exécute les projections sous forme de listes d'activation creuses plutôt que de produits scalaires denses).  TÂCHE : dépouille EXHAUSTIVEMENT ces 20 fichiers Markdown : reports/aiguille-30b.md reports/aiguille-gpt-oss.md reports/bilan-multi-materiel.md reports/rapport-8 … [3037 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave », moteur d'inférence LLM en … [3317 caractères tronqués]

*26 appels d'outils.* Actions notables :

- bash — Count lines in the 20 target reports
- read
- bash — Grep rare technical terms across the 20 reports
- bash — Grep project vocabulary terms across reports
- send_message

**Synthèse produite :**

⏵ Livrable livré en 3 messages au parent ; récapitulatif final

Inventaire terminé : les 20 fichiers ont été lus intégralement (3 058 lignes), aucun fichier du dépôt n'a été modifié. Le livrable complet (sections A, B, C, D) a été transmis au parent en 3 messages :

1. **A. Termes et sigles** — ~150 entrées (AER, PE, ALM, M20K, CDC, NVLink, UPI, HMB, MLA, CSA/HCA, DRVF, mode 0-4, k-WTA, PTQ, engram, hyper-connexion, seuil_push, KvCache::assurer, toutes les `DRAVE_*` et les familles de drapeaux, outils…) avec définition, usage et première occurrence `reports/fichier.md:ligne`. Absents vérifiés par grep : Sinkhorn, Hadamard, SwiGLU, LoRA, MTP, TLB, AVX2, HBM, MTok/s, p50/p95, « greffon ».
2. **B. Chiffres et affirmations mesurées** — ~230 mesures citées entre guillemets avec `fichier:ligne`, fichier par fichier.
3. **C. Contradictions / périmés / douteux** — ~85 entrées ; **D. Fichiers du dépôt cités** — ~80 chemins avec leur rôle.

Points saillants pour la détection de contradictions :
- **×2,17** revendiqué comme gain mesuré en `rapport-8bits.md:56` alors que `bilan-multi-materiel.md:92` le déclare **retiré** (inégalité de Kraft violée).
- **Croisement push/pull** : « ~10 % » (`rapport-analyse-flux.md:14`) contre « ~22 %, pas à 10 % » (`rapport-croisement-push-pull.md:43`) — contradiction interne au corpus.
- **« Le mode liste bat le dense »** : `bilan-multi-materiel.md:96,103` reproduit exactement l'affirmation que `rapport-croisement-push-pull.md:66-77` démontre fausse (15,8/14,7 contre 15,59/36,43 tok/s).
- **FPGA** : PCIe Gen3 ×8 6,5 Go/s (`bilan:8`) contre « USB seulement, 625 Mo/s » (`rapport-architecture-memoire.md:385`), qui se contredit aussi avec « Pas de FPGA dans cette machine » (`:246`).
- **KV à 1 M** : 82 Ko/82 Go (`rapport-architecture-memoire.md:418`) contre 90 Ko/96,6 Go (`:96`) dans le même document.
- **Cache KV** : 64 %/28 % (`rapport-attribution-kv.md:33-35`) contre 75 %/50 % dans REPRISE/roadmap (relevé par `rapport-coherence-docs-2.md:97`).
- **k = 32** : 23,3302 dans le tableau de `rapport-attention-creuse.md:27` contre 23,3279 aux lignes 95/126 et dans `rapport-campagne-parcimonie.md:36`.
- Chiffres manifestement faux et signalés comme tels : dispersion `1.8e17 évts/s` (`rapport-cpu-aer.md:17-18`), 5,3 G évts/s attribué à 16 puis 32 fils (`bilan:46` vs `:54`), « 8 % plus rapide » (`bilan:96`), 11 440 vs 11 901 lignes, en-tête 39/26/79 octets, 3 623/3 663, 1 589/1 629, 1 989/≈1 419.
- Les trois rapports de cohérence sont **datés** 
… [141 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** Count lines in the 20 target reports
- **T1** Grep rare technical terms across the 20 reports
- **T1** Grep project vocabulary terms across reports

## 4. Mesures et résultats marquants

- **T1** `bilan-multi-materiel.md:94:| Perplexité 20,29 (harnais Python) | **Invalidée** — `bpe_np.py` s'écarte du vrai pré-tokenizer Qwen2 sur 5 points (5,2 % d'identifiants). Le tokenizer Rust est conforme 73`
- **T1** `rapport-coherence-docs.md:100:| 44 | `reports/rapport-compacite-trace.md:13-14` | « restent à faire : valeurs i8 (−60,9 %), échelles f16 (−63,5 %), zstd (−79 %) » | i8 + échelles f16 par bloc sont **f`
- **T1** `rapport-compacite-trace.md:20:> Reste : l'emballage zstd en étape EXTERNE (−79 % au total, mesuré ici) — le`
- **T1** `rapport-compacite-trace.md:27:indice** — le reste (valeurs i8, échelles f16, zstd) porte le total à **−79 %**.`
- **T1** `rapport-coherence-docs-2.md:76:| 22 | `docs/roadmap.md:56` | critère 3.2 : « **3 623 → 1 589** octets par flux (÷2,3) pour 1,3 % d'écart à 1 024 jetons » | avec l'en-tête v4 : **3 663 → 1 629** ; le ÷`
- **T1** `rapport-coherence-docs-2.md:81:| 27 | `docs/format-flux.md:47`, `reports/rapport-compacite-trace.md:4-5`, `docs/roadmap.md:108` | trace dense 512 jetons : 132 396 736 → **66 370 408** (−49,87 %) | coh`
- **T1** `rapport-coherence-docs-2.md:82:| 28 | `docs/format-flux.md:58-61`, `REPRISE.md:248,340-341`, `docs/roadmap.md:94` | v3 : **45 079 930 o** (−32,1 % vs v2), rejeu 19,4029 (+0,074 %), 21 630 645 actifs |`
- **T1** `rapport-architecture-memoire.md:242:Écart de **4 %** sur le chemin qui traverse réellement l'UPI (le NVMe), et du`
- **T1** `bilan-multi-materiel.md:8:RTX 5000 (16 Go, NVLink 25,78 Go/s), 1 carte Stratix V GS (Storey Peak,`
- **T1** `bilan-multi-materiel.md:97:| « Le FPGA n'a pas NVLink / les RTX 5000 non plus » | **Corrigée** — l'utilisateur avait raison, 25,78 Go/s mesurés par lien |`
- **T1** `rapport-architecture-memoire.md:224:| **GPU 0 ↔ GPU 1** | | | **NVLink, 25,78 Go/s** |`
- **T1** `rapport-architecture-memoire.md:226:**Le NVLink est là, et il vaut 2× le PCIe** (25,78 contre ~12 Go/s réels). CUDA`
- **T1** `bilan-multi-materiel.md:9:DDR3 9,66 Go/s, PCIe Gen3 ×8 6,5 Go/s, QSFP+ 4,8 Go/s).`
- **T1** `bilan-multi-materiel.md:66:3. **Pas de multiplieur requis.** Le PE atteint 112,5 MHz avec 176 ALMs **et zéro`
- **T1** `bilan-multi-materiel.md:67:   DSP**, contre 115 ALMs et 1 DSP avec multiplieur — et **pas un hertz d'écart**.`
- **T1** `bilan-multi-materiel.md:95:| « 27 PE suffisent, 3 % de la logique » | **Corrigée** — en comptant le lecteur : 51 voies, 41 % de la logique et 41 % de la M20K |`
- **T1** `rapport-cpu-aer.md:11:  (accumulateur, 4096 × 24 bits = **12 Kio**, tient dans les M20K) ;`
- **T1** `bilan-multi-materiel.md:46:| CPU (16 threads) | **5,3 G évts/s** mesuré | ~57 nJ |`
- **T1** `bilan-multi-materiel.md:47:| FPGA (1 carte, 51 voies) | 4,83 G évts/s *projeté* (limite DDR3) | **~8,3 nJ** |`
- **T1** `bilan-multi-materiel.md:48:| GPU (dispersion) | **18,1 G évts/s** mesuré | ~12,7 nJ |`
- **T1** `rapport-coherence-vision.md:70:| `comparaison-spiking.md` | **corrigé, 4 sites** | encadré : le spike est un **moyen** d'obtenir la parcimonie, le cœur de Drave (grappes + lecture des flux) n'est pas `
- **T1** `rapport-architecture-memoire.md:373:| DeepSeek-V4-Flash (3 shards) | 86,90 Go | 0,07 s | 35 Mo |`
- **T1** `rapport-architecture-memoire.md:46:| **NVMe** | 828 Go | le reste des experts (~51 Go) + **l'engram mmappé** (203 Go, 0,4 Go de cache) | 5,5 Go/s |`
- **T1** `rapport-architecture-memoire.md:52:| engram mmappé + 90 % des experts en RAM | 8 + 71 + 0,4 = **79 Go** | confortable |`
- **T1** `bilan-multi-materiel.md:72:   mesurée : passer de 8 à 4 bits ne rapporte que 11 % de mémoire et 12 %`
- **T1** `bilan-multi-materiel.md:134:demande aucun matériel, et il porterait le moteur à ~40 tok/s — au niveau du GPU en`
- **T1** `rapport-campagne-parcimonie.md:19:| activations du FFN (k-WTA 90 %) | +0,15 à +0,28 % | ✅ acceptable |`
- **T1** `rapport-campagne-parcimonie.md:20:| activations du FFN (k-WTA 85 %) | +0,5 à +1,2 % | ⚠️ selon le budget |`
- **T1** `bilan-multi-materiel.md:92:| « Encodage hybride ×2,17 » | **Retirée** — le code proposé viole l'inégalité de Kraft (Σ2^−l = 1,992 > 1) |`
- **T1** `rapport-8bits.md:18:| **entropie de la source** | **7.648** | **×1.046** |`
- **T1** `rapport-8bits.md:19:| **code de Huffman réel** | **7.671** | **×1.043** |`
- **T1** `rapport-8bits.md:35:| Huffman | 473.6 Mo | ×1.043 |`
- **T1** `rapport-8bits.md:44:   vaut 7.65 b/poids et un vrai code de Huffman atteint 7.67 b/poids, soit **×1.04**.`

