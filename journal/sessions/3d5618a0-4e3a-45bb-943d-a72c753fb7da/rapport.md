# Session 3d5618a0 — Tu écris un **document de

| | |
|---|---|
| Identifiant | `3d5618a0-4e3a-45bb-943d-a72c753fb7da` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-02 15:02 |
| Durée | 0.3 h |
| Tours | 1 |
| Messages | 73 |
| Appels d'outils | 85 |
| Fichiers touchés | 1 |
| Commandes | 35 |
| Sous-agents | 4 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu écris un **document de référence** pour le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet : un **glossaire raisonné** de tout le vocabulaire, sigles, abréviations et notions employés dans `docs/` et `reports/`, destiné à un **néophyte** qui veut pouvoir lire et comprendre tous les documents du dépôt.  CONTEXTE DU PROJET (vérifie chaque point dans les fichiers, ne me crois pas sur parole) … [3796 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu écris un **document de référence** pour le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet : un **glossaire rai … [4076 caractères tronqués]

*85 appels d'outils.* Actions notables :

- bash — List repo root
- bash — List docs and reports
- bash — Full reports tree
- bash — List sprints, tools, src
- bash — Measure doc sizes
- bash — Preview vision doc
- todo_write
- sous-agent — Dépouiller rapports 1-20
- sous-agent — Dépouiller rapports 21-40
- sous-agent — Dépouiller rapports 41-60
- sous-agent — Dépouiller sprints et outils
- read
- list_agents
- bash — Grep technical acronyms across docs/reports
- … et 49 autres

**Synthèse produite :**

⏵ Livraison terminée

`docs/glossaire.md` est écrit (1630 lignes, ~14 000 mots) — seul fichier créé, rien d'autre modifié de mon fait.

- **187 entrées**, 7 thèmes classés alphabétiquement : le projet et sa méthode ; modèles et architectures ; formats et quantification ; le moteur Drave ; flux, protocole et transport ; répartition, matériel et énergie ; mesure et méthode. Chaque entrée donne forme développée FR/EN, définition sans prérequis, référence `chemin:ligne`, et source externe (60 liens, tous testés ; les non vérifiables cités par titre).
- Plus : mode d'emploi, parcours de lecture néophyte en 9 étapes, index des outils `tools/`, table des drapeaux CLI et des variables `DRAVE_*`, **21 points relevés non corrigés**, liste des sources.
- **Point 1** — `docs/contexte-long.md:399-401` attribue l'écart int8 aux valeurs, alors que `:176-197` du même fichier et `docs/roadmap.md:30` disent « tout l'écart est dans les CLÉS ».
- **Point 2** — `docs/vision.md:74` liste `--ppl-profil` comme existant ; `reports/rapport-drapeaux-ignores.md:97` le dit « jamais lu » et le code n'a qu'un champ mort (`main.rs:541`) : le drapeau n'existe pas.
- **Point 3** — `reports/bilan-multi-materiel.md:96` reprend « 8 % plus rapide que le dense (15,8 contre 14,7 tok/s) », le chiffre même que `reports/rapport-croisement-push-pull.md:66-71` déclare faux (pull corrigé : 36,4 tok/s).
- Autres : phases P1-P5 dupliquées dans `plan-deepseek41-complet.md` (FAIT puis à faire) ; `plan-prefill-reparti.md:421` dit le mode 4 « à écrire » alors qu'il est mesuré ; accuracy de 4 971 % en `rapport-encodage.md:42` ; `reports/` compte 60 fichiers, pas « une centaine ».
- Signalé au parent : `drave-core/src/model.rs` est modifié dans l'arbre de travail (mtime 15:03) sans que ce soit moi — probable travail parallèle, à vérifier avant commit.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/glossaire.md` | 1 | 18 |

### Sous-agents lancés

- tour 1 — Dépouiller rapports 1-20
- tour 1 — Dépouiller rapports 21-40
- tour 1 — Dépouiller rapports 41-60
- tour 1 — Dépouiller sprints et outils

### Commandes exécutées (échantillon)

- **T1** List repo root
- **T1** List docs and reports
- **T1** Full reports tree
- **T1** List sprints, tools, src
- **T1** Measure doc sizes
- **T1** Preview vision doc
- **T1** Grep technical acronyms across docs/reports
- **T1** Grep more terms across repo docs
- **T1** Check Hadamard/MTP and other terms repo-wide
- **T1** Grep porte/push/événement
- **T1** Inspect Rust identifiers and CLI flags
- **T1** List all CLI flags and DRAVE_ env vars
- **T1** Cross-check logging cost figures
- **T1** Check date and file counts
- **T1** List external URLs cited in docs/reports
- **T1** Extract URLs from docs and reports
- **T1** Check HTTP status of candidate external URLs
- **T1** Verify contradiction quotes
- **T1** Verify remaining URLs
- **T1** Check glossary size and typos
- **T1** Inspect lines to fix
- **T1** Verify struct and flag names
- **T1** Count flags and check ppl-profil
- **T1** Check ppl-profil references and var count
- **T1** Count declared DRAVE_ variables
- **T1** Count entries per theme
- **T1** Count true entries and list headings
- **T1** Check bold balance and links
- **T1** Verify quoted lines
- **T1** Check alphabetical order per theme
- **T1** Sort entries alphabetically per theme
- **T1** Verify pure reordering
- **T1** Check git status and sample content
- **T1** Inspect modified model.rs
- **T1** Final file verification

## 4. Mesures et résultats marquants

- **T1** `**mesuré** : en dessous d'environ **22 % de densité**, le push (listes) bat le`
- **T1** `+0,074 % près** (19,4029 contre 19,3885) et l'écart d'activation entre le calcul`
- **T1** `La densité observée, elle, dépend du modèle et de la couche : **17,9 %** sur`
- **T1** `reports/rapport-compacite-trace.md:20:> Reste : l'emballage zstd en étape EXTERNE (−79 % au total, mesuré ici) — le`
- **T1** `reports/rapport-compacite-trace.md:27:indice** — le reste (valeurs i8, échelles f16, zstd) porte le total à **−79 %**.`
- **T1** `reports/rapport-passage-a-l-echelle.md:160:   TLB. Des pages de 2 Mo diviseraient ce coût par 512.`
- **T1** `reports/rapport-localite-activation.md:24:| opérateurs creux par neurone | chemin par **listes d'événements** (`SparseVec`, push) | bascule push/pull mesurée à **22 % de densité** (`seuil_push = 0.22``
- **T1** `docs/histoire.md:12:| **le virage événementiel** | l'idée qui a tout changé : ne plus multiplier des matrices, mais **pousser des listes d'activation** vers leurs destinations (AER, *Address Event Rep`
- **T1** `docs/programme-recherche.md:58:| Carte FPGA | PE vérifié sur 309 020 événements réels, synthétisé (176 ALMs, 0 DSP), lecteur DDR3 vérifié de bout en bout |`
- **T1** `reports/rapport-cpu-aer.md:11:  (accumulateur, 4096 × 24 bits = **12 Kio**, tient dans les M20K) ;`
- **T1** `reports/bilan-multi-materiel.md:95:| « 27 PE suffisent, 3 % de la logique » | **Corrigée** — en comptant le lecteur : 51 voies, 41 % de la logique et 41 % de la M20K |`
- **T1** `docs/comparaison-spiking.md:59:| Arithmétique | ET logique + **AC** (accumulation) | MAC (mais décalages+additions validés, 0 DSP sur FPGA) |`
- **T1** `docs/histoire.md:11:| **Qtrinet** (origine) | inférence de LLM en ternaire / multi-bits sur un cluster de cartes **Stratix V** (Microsoft Storey Peak), 100 % logique, sans DSP. Le cahier des charges d`
- **T1** `docs/plan-deepseek41-complet.md:70:| tables d'engram | 10 000 entrées en **219–524 ms**, 2,6 Mo touchés par table, **120 Mo de RSS** pour 365,7 Go |`
- **T1** `reports/rapport-inference.md:249:| RSS | 1,27 Go | 1,02 Go | −20 % |`
- **T1** `docs/convertisseur.md:101:- **NUMA d'abord** : 20,7 → **24,7 Go/s** en liant un socket (mesuré au banc).`
- **T1** `docs/convertisseur.md:102:  Un plan de placement qui ignore les nœuds NUMA laisse 20 % sur la table, et`
- **T1** `docs/convertisseur.md:93:| PCIe x8 (gen 3) | 6,5 Go/s | transfert CPU↔GPU |`
- **T1** `docs/contexte-long.md:6:> NVMe à ~3,5 Go/s, 20 cœurs Haswell AVX2).`
- **T1** `docs/contexte-long.md:362:est **déjà vectorisé AVX2** et le coût par expert (4,4 Mo) est faible : le`
- **T1** `docs/comparaison-spiking.md:63:| Énergie par opération | E_AC = 0,9 pJ contre E_MAC = 4,5 pJ (Horowitz) | 8,3 nJ/événement (FPGA, **projeté** : 4,83 G évts/s, limite DDR3) contre 57 nJ (CPU, **mesuré*`
- **T1** `docs/convertisseur.md:146:5. **L'alignement 2 Mo** est ce qui permettra les grosses pages le jour où mmap`
- **T1** `docs/plan-deepseek41-complet.md:174:  mélanges → `pre` sigmoïde, `post` sigmoïde ×2, `comb` **Sinkhorn 20`
- **T1** `docs/programme-recherche.md:10:(encodage ×2,17 retiré pour violation de Kraft, divergence fantôme, tokenizer`
- **T1** `reports/bilan-multi-materiel.md:92:| « Encodage hybride ×2,17 » | **Retirée** — le code proposé viole l'inégalité de Kraft (Σ2^−l = 1,992 > 1) |`
- **T1** `docs/plan-mla-vision.md:187:| projecteur (fusion 2 × 2 → `mm.0` → GELU → `mm.2`) | **1,73e-06** |`
- **T1** `docs/plan-deepseek-v4-flash.md:38:| shard 1 (5,3 Mo) | ✅ l'**architecture** (`--plan` : « deepseek4, 43 couches, 256 experts (top-6) ») et le **tokenizer** : 129 280 jetons, aller-retour texte→jetons→`
- **T1** `docs/contexte-long.md:102:| E2 | **KV int8** | **fait** (échelle **par bloc de 32**, dequantification à la lecture) | ÷4 sur le KV ; 128 k confortable | mesuré : **+1,5 %** à 512 jetons, **+3,0 %** à `
- **T1** `docs/comparaison-spiking.md:71:**17,9 %** — sous le croisement push/pull de **22 %**`
- **T1** `docs/roadmap.md:28:| 1.2 | **Quantification choisie par la mesure** : par couche, par tenseur, plutôt qu'un réglage global | 🔬 | la densité par couche varie de **20 % à 56 %** (`reports/rapport-analys`
- **T1** `docs/vision.md:155:   croisement push/pull à ~22 % donne déjà l'ordre de grandeur de ce qu'on`
- **T1** `reports/rapport-cpu-aer.md:17:- dispersion (`np.bincount`) : **183999808.87 G événements/s**`
- **T1** `reports/rapport-cpu-aer.md:18:- dispersion (`np.add.at`) : 364797216.41 G événements/s`
- **T1** `=== 1,2 Mo ===`
- **T1** `docs/programme-recherche.md:29:   nommées. Journaliser les listes d'activations (1,2 Mo/token, **+3,0 %**)`
- **T1** `reports/rapport-inference.md:301:1,2 Mo d'accumulateurs, qui débordent le cache L2 de chaque cœur : chaque écriture`
- **T1** `reports/rapport-capteur-hebbien.md:34:sa copie coûte 7 Ko par matrice, 1,2 Mo par token, soit 19 Mo/s à 15,8 tok/s.`
- **T1** `reports/rapport-programme-evolutif.md:19:| Journal des activations de toutes les couches (24) | ~1,2 Mo/token, soit 19 Mo/s à 15,8 tok/s |`
- **T1** `reports/rapport-programme-evolutif.md:23:les *listes d'activations* suffit à rejouer intégralement le calcul. 1,2 Mo/token`
- **T1** `docs/programme-recherche.md:60:| Journalisation | +3,0 %, digest versionnable, archive automatique |`
- **T1** `docs/roadmap.md:15:| 0.1 | **Format de trace du flux** : par (couche, position), la liste des neurones actifs (indice + valeur), l'échelle, le nombre | ✅ | écrit et relu sans perte ; **132 Mo pour 512`
- **T1** `docs/roadmap.md:30:| 1.4 | **Écart int8 résiduel** (+3,0 % contre +0,8 % chez llama.cpp à 8 192) | ✅ | **attribué** : tout l'écart est dans les CLÉS (clés f32 + valeurs int8 = +0,023 % ; l'inverse = +`
- **T1** `docs/roadmap.md:108:| 2026-09-30 | trace du flux, Qwen2.5-0.5B, 512 jetons, 24 couches, 2 points par couche | 24 576 listes · **132 Mo** en v1 · 6 octets par neurone actif · **+8 % de temps** (aujourd`
- **T1** `docs/roadmap.md:111:| 2026-09-30 | attribution du cache KV int8, 8 191 jetons, ctx 8 192 | f32 **14,2339** · int8 **14,6667** (+3,0 %) · **clés f32** + valeurs int8 **14,2372** (+0,023 %) · clés int8 `
- **T1** `docs/roadmap.md:157:L'écart avec llama.cpp à 8 192 (+3,0 % contre +0,8 %) est attribué. Les deux`
- **T1** `docs/contexte-long.md:159:| **int8** | **14,6667** | **+3,0 %** | 16,73 | +0,8 % | 1 144 s |`
- **T1** `docs/contexte-long.md:399:à 2 048 jetons). L'écart de +3,0 % contre +0,8 % à 8 192 vient donc d'ailleurs :`
- **T1** `docs/vision.md:219:  **+3,0 %** à 8 192, là où l'int4 coûte +364 % — le débat n'est pas « combien de`
- **T1** `reports/rapport-capteur-hebbien.md:27:| **surcoût** | **+3,0 %** |`
- **T1** `reports/rapport-capteur-hebbien.md:107:   gradient (c'est fait ici : +3,0 %).`
- **T1** `reports/rapport-programme-evolutif.md:17:| Capteur de co-activation branché sur une projection | **+3,0 %** (96,75 s → 99,64 s sur 1 025 tokens) |`
- **T1** `reports/rapport-programme-evolutif.md:118:1. **Journaliser** pendant l'inférence (+3,0 %).`
- **T1** `reports/rapport-attribution-kv.md:35:l'int8 complet (28 %, soit 2,25 octets) coûte +3,0 %. C'est le`
- **T1** `reports/rapport-coherence-docs-2.md:100:| 41 | `docs/contexte-long.md:101-102` (E2) | KV int8 « **fait** (échelle par vecteur) », « mesuré : **+7,1 %** (llama.cpp : +3,1 %) » | le même document §4.bis`
- **T1** `reports/rapport-architecture-memoire.md:111:experts. Le moteur sait déjà le faire (`DRAVE_KV_BITS`, mesuré sur Qwen : +3,0 %`
- **T1** `reports/rapport-architecture-memoire.md:112:de perplexité en int8, +3,0 % en clés seules) — il reste à le faire sur V4.1.`
- **T1** `=== 132 Mo ===`
- **T1** `docs/roadmap.md:17:| 0.3 | **Le format EST le contrat d'échange** (phase 3) : versionné, en-tête + paires | ✅ | codec de référence (`tools/flux_codec.py`) : aller-retour **identique** sur 132 Mo ; **e`
- **T1** `docs/roadmap.md:139:| `--abits 16` (défaut) | 99-100 % (rien n'est seuillé) | 132 Mo | 25 à 42 % |`
- **T1** `docs/roadmap.md:204:Mesuré, Qwen2.5-0.5B, 512 jetons, deux fenêtres de contexte, trace de 132 Mo :`
- **T1** `docs/format-flux.md:51:| trace dense, 512 jetons | 132 396 736 o | **66 370 408 o (−49,87 %)** |`
- **T1** `docs/format-flux.md:183:| la taille suit l'activité | densité ÷2,3 → trace ÷2,5 (132 Mo → 53 Mo) |`
- **T1** `reports/rapport-compacite-trace.md:5:> 512 jetons **132 396 736 → 66 370 408 octets (−49,87 %)**, rejeu `--flux-forcer``
- **T1** `reports/rapport-compacite-trace.md:59:| `/tmp/flux_f32.bin` | même modèle, 512 jetons, `--abits 16` (rien n'est seuillé) | **132 396 736 o** | 22 008 776 | 99,9 % |`
- **T1** `à 2 048 jetons). L'écart de +3,0 % contre +0,8 % à 8 192 vient donc d'ailleurs :`
- **T1** `| 3 | `attn_topk_somme` : softmax sur les k retenus + puits, puis Σ pondérée des V | ✅ 1,0–4,8e-7 · temps GPU constant (0,07 ms) |`
- **T1** `| 4 | branchement dans `model.rs` (`attn_topk > 0` + miroir VRAM) | ✅ **fait** (opt-in `DRAVE_GPU_TOPK=1`) : PPL identique (9,4162 contre 9,4167 à 2 k ; 12,2265 contre 12,2267 à 4 095 jetons) et **le `
- **T1** `| 5 | mesure 1 M de clés : ms/couche avec et sans top-k | ✅ **fait au niveau des noyaux** : chaîne complète **3,90 ms** pour 14 lignes × 1 M clés contre 539,9 ms d'attention complète CPU (×138) et 13,`
- **T1** `| **mode 4, lots de 16** | **1,5 ko** (contre 3,5 en lot dense) | **3,03e-2** |`
- **T1** `principe (« 0 DSP ») : ses multiplications ternaires deviennent des additions et`
- **T1** `docs/contexte-long.md:520:   **722,56** chez nous (1,1 %). Le profil par profondeur (`--ppl-profil`) montre`
- **T1** `1221: d'extension. Mesuré à 6,5 Go/s en x8 Gen3 ici ; c'est **le goulot d'un montage`
- **T1** `| 2.00 | 4971.00 % | 5.5 | dense ternaire (référence CDC) |`
- **T1** `| Capteur de co-activation branché sur une projection | **+3,0 %** (96,75 s → 99,64 s sur 1 025 tokens) |`
- **T1** `## 6. Répartition, matériel et énergie      28 entrées  DÉSORDRE: [('Cœur physique · SMT · hyperthreading · paire HT', 'CUDA · noyau (kernel) · sm_75 · PTX · FFI'), ('Grappe · `commun.gguf` · `cluster`

