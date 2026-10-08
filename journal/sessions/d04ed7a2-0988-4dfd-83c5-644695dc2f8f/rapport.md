# Session d04ed7a2 — Tu travailles dans le dépôt

| | |
|---|---|
| Identifiant | `d04ed7a2-0988-4dfd-83c5-644695dc2f8f` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-08 09:18 |
| Durée | 0.1 h |
| Tours | 1 |
| Messages | 43 |
| Appels d'outils | 60 |
| Fichiers touchés | 0 |
| Commandes | 38 |
| Sous-agents | 1 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (moteur d'inférence Rust « Drave », drave-core/). LECTURE SEULE STRICTE : ne modifie aucun fichier, ne compile pas, ne lance aucun test ni binaire.  Objectif : inventorier le DÉCOUPAGE EN CLUSTERS et le DÉCOUPAGE PAR PLAGES DE COUCHES (répartition d'un même modèle sur plusieurs unités/processus).  À examiner : - drave-core … [1767 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (moteur d'inférence Rust « Drave », drave-co … [2047 caractères tronqués]

*60 appels d'outils.* Actions notables :

- bash — List repository root
- glob
- bash — Count lines of key files
- bash — List relevant reports
- read
- bash — Grep couches options in main and model
- bash — Grep couche_debut/couche_fin definitions
- bash — Grep range validation checks
- bash — Read plage/pilote sections
- bash — Grep clusters in portes.sh
- bash — Read portes.sh head
- bash — Check report sizes
- bash — Find cluster-related tests in Rust sources
- sous-agent — Digest cluster reports
- … et 28 autres

**Synthèse produite :**

⏵ Condensé consolidé — clusters et plages de couches (lecture seule, rien modifié)

**1) Tableau** — état : P = vérifié par une porte, M = mesuré localement (rapport/REPRISE), D = déduit du code.

| capacité | ce qu'elle fait | fichier source | état | chiffre mesuré |
|---|---|---|---|---|
| Lecteur clusters + mmap | commun.gguf + cluster-XX.gguf réunis en un `Gguf` ; experts sous `cl{c}/` ; `mapping.tsv` lu d'un bloc ; fichiers mappés | `clusters.rs:150-297` · `gguf.rs:153-170, 478-520` | P (porte 1 : 6 tests `clusters.rs:309-505` ; porte 3) | 9 fichiers · 1 587 tenseurs · 18,55 Go ; mmap 9,32 s / 6,35 Go contre 30,68 s / 19,20 Go |
| Nœud partiel | `DRAVE_CLUSTERS=0,3` ; demandé-absent = erreur ; incomplet refusé sans `DRAVE_CLUSTERS` | `clusters.rs:167-176, 239-273, 291-295` | M | 1 cl. 2,35 Go / 268 786,62 · 4 cl. 4,60 Go / 3 378,91 · 8 cl. 6,28 Go / 799,8557 |
| Porte clusters | dossier complet Qwen3-30B 8 clusters, mêmes jetons | `tools/portes.sh:55-61` | P (799,8557 revérifié au bit près après le correctif de routage : `rapport-routage-experts.md:65-77`) | attendu 799.8557 |
| Convertisseur experts | GGUF → commun + 8 clusters + `mapping.tsv` + `manifeste.json`, copie d'octets sans requantification | `convertir_clusters.py:402-582` | M | Qwen3-30B : 435+8×144 = 1 587 tenseurs · 18,60 Go · 351,7 s · SHA-256 « TOUT CONCORDE » ; V4-Flash : 86,9 Go, 11 008 entrées, 450 s, 8 430,2968 = 8 430,2968 (39,9 s contre 111,8 s, 2,8×) |
| Conversion par plages de couches | `--mode couches` : blocs `blk.N` en groupes contigus (dense), sans `mapping.tsv` | `convertir_clusters.py:446-463, 520-529` | M | Qwen2.5-0.5B : commun + 4 fichiers × 6 couches · 290 tenseurs |
| Plage de couches moteur | `couche_debut..couche_fin` = [a,b) exécutée ; hors plage → flux brut | `model.rs:2551-2569, 4368-4369, 6641-6646, 6904-6905` | M (V4.1 + phase 3), aucune porte dans `portes.sh` | V4.1 : 0,00e0, 1 743 713,6243 (51,3 s / 68,0 s) ; phase 3 : 144,8289 = 144,8289, 0,00e0, 1 023 flux, 9,5146 |
| Porte de plage K3 | `--k3-essai --couches 0:13 / 13:26 / 0:26` ; coupe après la banque de la couche 12 | `tools/test-plage-k3.sh:1-36` · `main.rs:147, 2131-2134, 2144` | porte TENUE mais NON câblée dans `portes.sh` | B et C identiques au bit · 4 jetons · 28 672 octets |
| Réparti pilote/pair | `--couches-locales N` : local [0,N), pair [N,n_layer), plage dans l'en-tête | `main.rs:3345, 3430, 3457-3460, 3549, 3204-3213` | M | écart 0,00e0 dense (`REPRISE.md:1307-1316`) |
| Outils d'analyse | c
… [4605 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Sous-agents lancés

- tour 1 — Digest cluster reports

### Commandes exécutées (échantillon)

- **T1** List repository root
- **T1** Count lines of key files
- **T1** List relevant reports
- **T1** Grep couches options in main and model
- **T1** Grep couche_debut/couche_fin definitions
- **T1** Grep range validation checks
- **T1** Read plage/pilote sections
- **T1** Grep clusters in portes.sh
- **T1** Read portes.sh head
- **T1** Check report sizes
- **T1** Find cluster-related tests in Rust sources
- **T1** Check --plage flag and invalide messages
- **T1** Read couches call sites in main.rs
- **T1** Locate load functions in model.rs
- **T1** Read flux server validation
- **T1** Read couche_fin usage and charger_moe
- **T1** Trace couches_locales and couches param
- **T1** Read forward layer loops
- **T1** Check range guards
- **T1** Look for plage docs in reports/README
- **T1** Grep gates for reparti/clusters
- **T1** Read REPRISE distributed section
- **T1** Grep measured cluster figures
- **T1** Find Moe::ou and expert bias handling
- **T1** Check mmap handling in gguf.rs
- **T1** Read expert bias refusal and mmap choice
- **T1** Find multi-file open and alignment
- **T1** Read multi-file documentation
- **T1** Read usage text and tete-partielle
- **T1** Check transport header carrying the range
- **T1** Check shared expert handling
- **T1** Grep shared expert fields
- **T1** List test fn names in gguf.rs
- **T1** List cluster test names
- **T1** Verify v4-reparti and phase3 figures
- **T1** Verify k3 range figures
- **T1** Check k3 plage test script wiring
- **T1** Read routing report gate impact

## 4. Mesures et résultats marquants

- **T1** `model.rs:116:    // (une couche MoE = 1 366 ms/jeton, et 93 couches en f32 demanderaient`
- **T1** `model.rs:494:    // différence traverse 48 couches et déplace la porte publiée de 0,03 % —`
- **T1** `route "GLM-5.3 : sigmoïde ×2,5" "$M/GLM-5.3-UD-IQ1_S/GLM-5.3-UD-IQ1_S-00001-of-00006.gguf" "sigmoïde"`
- **T1** `route "Kimi-K2.7 : sigmoïde ×2,827" "$M/Kimi-K2.7-Code-UD-IQ1_M/Kimi-K2.7-Code-UD-IQ1_M-00001-of-00008.gguf" "sigmoïde"`
- **T1** `// sur 20 cœurs / 40 threads : 18 threads = 22,6 Go/s, 20 = 18,7 (bruité),`
- **T1** `// 15 = 19,9, 10 = 14,3. Le `× 3/4` d'avant visait à laisser un quart des CPU`
- **T1** `// sursouscription (mesuré : ×1,3 de perte à 40+1 threads sur 40 CPU).`
- **T1** `// tous les cœurs physiques : mesuré, 10 threads rendent 14,3 Go/s contre`
- **T1** `// 22,5 à 20 — le `cpu / 2` laissait 36 % sur la table.`
- **T1** `// distantes : **97,6 ms** d'attente contre 15,6 ms de calcul local — six fois`
- **T1** `// que coûte déjà un état en `hc` copies — 0,02 %.`
- **T1** `// (24 × 264 octets) sont lues dans la table de 101 Go : c'est le`
- **T1** `#    moteur déporte alors tout seul les projections Q8_0 de plus de 8 Mo — le`
- **T1** `#    du même ordre que les 0,06 % mesurés alors — non re-mesuré depuis.)`
- **T1** `reports/rapport-decoupage-moe.md:41:| 4 | **0,799** | **1,94** | 0,440 | 3,59 | ×1,8 |`
- **T1** `reports/rapport-portes-p0-p9.md:28:| **P6** — V4-Flash complet, listes, grappes | **TENUE**, trois fenêtres : 63 positions (min 0,9550 · moyenne 0,9852 · top-1 88,9 % · PPL +6,4 %), **255 positions** `
- **T1** `reports/rapport-routage-experts.md:75:déplacé la porte Qwen3-30B de 799,8557 à 799,8152 (−0,005 %). Cause : la`
- **T1** `reports/rapport-tete-restreinte.md:94:| 0,01 | 61,5 % | 22,3563 | +15 % |`
- **T1** `reports/rapport-transport-liste.md:107:| 0,05 | 24,0 % | 799 | 1,1e0 | 897 octets · 8,1e-1 |`
- **T1** `78:/// Mesuré : charger 18,6 Go prend 6,8 s en mmap paresseux (2,7 Go/s) — proche du`
- **T1** `drave-core/src/model.rs:2634:    /// **une valeur partagée** (5 × 5120 = 25 600).`
- **T1** `les experts pèsent 80 % du fichier.`
- **T1** `| avant correction | 144,8289 | 1 621,7239 | ×11,2 |`
- **T1** `| après la norme seule | 144,8289 | 693,4492 | ×4,8 |`
- **T1** `réparti prend le temps du calcul local : 19,4 ms par jeton en local, 19,7 ms à`
- **T1** `| **A** | 0..12 | écrit le relais : *« reprend à la couche 13 · 4 jetons × 7 168 canaux · 2 banque(s) »* |`
- **T1** `déplacé la porte Qwen3-30B de 799,8557 à 799,8152 (−0,005 %). Cause : la`

## 5. Erreurs rencontrées

1 sorties en erreur ou divergentes. Les premières :

- **T1** : #!/bin/bash # Les portes du dépôt, en une commande. # # Un chiffre de référence qui dérive sans qu'on s'en aperçoive ne vaut rien : # chaque porte est comparée à la valeur ATTENDUE, et le script sort 

