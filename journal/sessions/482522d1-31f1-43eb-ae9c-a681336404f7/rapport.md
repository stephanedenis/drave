# Session 482522d1 — Tu travailles dans le dépôt

| | |
|---|---|
| Identifiant | `482522d1-31f1-43eb-ae9c-a681336404f7` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-08 09:18 |
| Durée | 0.1 h |
| Tours | 1 |
| Messages | 54 |
| Appels d'outils | 58 |
| Fichiers touchés | 0 |
| Commandes | 50 |
| Sous-agents | 4 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave » : un moteur d'inférence en Rust, drave-core/, qui charge des GGUF en place et fait tourner de gros modèles sur une machine à RAM limitée ; outils dans tools/, rapports dans reports/, reprise dans REPRISE.md).  MISSION : inventorier les capacités de DISTRIBUTION et d'EXPLOITATION HÉTÉROGÈNE du moteur — rép … [2326 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet « Drave » : un moteur d'inférence en … [2606 caractères tronqués]

*58 appels d'outils.* Actions notables :

- bash — List repo structure
- bash — Show git log and reports
- bash — Grep key env vars
- bash — List rest of tools and portes
- bash — Count lines of key files
- bash — Grep network transport in Rust sources
- bash — Read main.rs flux serveur region 1
- bash — Grep relais in sources
- bash — Read Relais definition in kimi_k3.rs
- bash — Read K3 plage/relais invocation
- bash — Read run_serveur_flux
- bash — Read Rust tests for flux
- bash — Read portes.sh
- bash — Read porte-flux and portes_formats
- … et 42 autres

**Synthèse produite :**

⏵ Inventaire terminé : rapport et addendum transmis au parent

Mission terminée. Livrables envoyés à `d31b3d9b-58e4-4d34-85fa-381b6f6a6a76` : le rapport complet (≤150 lignes, tableau par capacité, portes, manques, limites mesurées) puis un addendum issu du dernier sous-agent.

**Complément (addendum) — 4 points qui s'ajoutent au rapport, sans le corriger :**
1. **Plages de couches mesurées au-delà de V4.1** : `reports/rapport-phase3-reparti.md:42-53` (0..12 / 12..24 sur Qwen2.5-0.5B : 144,8289 = 144,8289, 0,00e0, 1 023 flux, 9,5146 à 1 024 jetons) et `reports/rapport-passe-k3-disque.md:409-467` (Kimi-K3 coupé couche 13 : B et C **identiques au bit**, 4 jetons, relais de **28 672 octets**).
2. `tools/test-plage-k3.sh:1-36` **est** la porte du découpage K3, mais elle **n'est pas câblée** dans `tools/portes.sh` (0 occurrence de « plage ») — les seules portes liées restent n°1 (`cargo test` ≥48) et n°3 (clusters, 799.8557).
3. **Second artefact clusters** : V4-Flash 86,9 Go → commun + 8 clusters, 11 008 entrées de mapping (43 × 256), 450 s ; 8 430,2968 en 39,9 s contre 111,8 s, soit **2,8×** (`rapport-v4-reparti.md:55-70`) ; `--ppl-reparti` sur le même : 0,00e0.
4. **Sensibilité de la porte clusters** : passage transitoire à 799,8152 (−0,005 %, `x/s` au lieu de `x*(1/s)`) puis retour à **799.8557 au bit près** (`rapport-routage-experts.md:65-77`) — la valeur attendue par `portes.sh:60` est cohérente.

Nuance de vocabulaire : aucun `reports/*cluster*` n'existe ; les documents « grappes » traitent un autre objet que le format `commun.gguf` + `cluster-XX.gguf`.

**Conclusion inchangée** : un seul découpage est à la fois juste et prouvé — 2 nœuds TCP, N plages de couches, mêmes logits au bit près — mais uniquement sur la même machine, chaque nœud chargeant le modèle entier. Les manques structurants restent le partage RAM/disque entre nœuds, la sommation inter-nœuds des experts, le branchement réseau du relais K3, toute mesure sur un vrai lien réseau, et toute porte GPU/mmap/disque. Aucun fichier n'a été modifié, aucune compilation ni test lancé.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Sous-agents lancés

- tour 1 — Extract network split facts
- tour 1 — Extract GPU dispatch facts
- tour 1 — Extract cluster split facts
- tour 1 — Extract memory/disk/threads facts

### Commandes exécutées (échantillon)

- **T1** List repo structure
- **T1** Show git log and reports
- **T1** Grep key env vars
- **T1** List rest of tools and portes
- **T1** Count lines of key files
- **T1** Grep network transport in Rust sources
- **T1** Read main.rs flux serveur region 1
- **T1** Grep relais in sources
- **T1** Read Relais definition in kimi_k3.rs
- **T1** Read K3 plage/relais invocation
- **T1** Read run_serveur_flux
- **T1** Read Rust tests for flux
- **T1** Read portes.sh
- **T1** Read porte-flux and portes_formats
- **T1** Read test-plage-k3 and pair_factice
- **T1** Read run_ppl_reparti pilote
- **T1** Read transport stats printout
- **T1** Grep throughput reporting in code
- **T1** Grep REPRISE for distribution sections
- **T1** Read REPRISE head
- **T1** Read REPRISE phase 3 distribution section
- **T1** Check gate callers and colab assets
- **T1** Grep couches options and K3 network mentions
- **T1** Find K3 plage reports and recent commits
- **T1** Grep roadmap phases
- **T1** Read roadmap phases 2-3 and status
- **T1** Read colab-reparti doc
- **T1** Read placement planner
- **T1** Read plan output and materiel cost model
- **T1** Count and list Rust tests
- **T1** Read tests_noeud_partiel
- **T1** Read clusters tests and k3 tests
- **T1** Check CLI wiring of cluster subsets
- **T1** Read usage text and MMAP handling
- **T1** Check where materiel plan is used
- **T1** Read thread affinity and fils()
- **T1** Read runtime hw decisions
- **T1** List GPU tools and kernels
- **T1** Grep LAN test evidence
- **T1** Find 0.0.0.0 usage evidence
- … et 10 autres

## 4. Mesures et résultats marquants

- **T1** `6df6de4 §10 : le palier NVMe donne −8,8 %, la prédiction était de −16,3 %`
- **T1** `3169941 Attribution des 206,58 Gio : 72 % sont les experts, relus à chaque jeton`
- **T1** `d186466 §94 : rang 1, 2 ou 3 — le meilleur rang n'est pas celui du meilleur chiffre`
- **T1** `./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:22747:- Regression gates (must stay): Qwen ctx 256 = **19,3885**; gpt-oss ctx 256 = **15,1757** — measured **without** `DRAVE_GPU` (th`
- **T1** `./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:25989:Chiffres : 84 drapeaux + 26 variables DRAVE_* = 110 options auditées ; 46 drapeaux (55 %) ignorés dans au moins un mode où ils d`
- **T1** `./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:26014:2. **46 drapeaux (55 %) sont ignorés dans au moins un mode où ils devraient s'appliquer**, dont 20 classés critiques ; 5 de plus`
- **T1** `./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:27290:Autres points saillants : docs/format-flux.md se contredit (titre v3, version u8=4, message « parle la 4 », en-tête 26 octets) e`
- **T1** `./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:29006:- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > /tmp/porte_gpu.sh <<'EOF'\n#!/bin/bash\ncd `
- **T1** `./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:29015:=== 1. gpt-oss avec DRAVE_GPU (documenté : 15,1667, le pilote déporte les Q8_0 > 8 Mo) ===`
- **T1** `./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:29596:`DRAVE_GPU=1` sur gpt-oss redonne **15,1667**, et le noyau de tête **1,6 ms** (88 Go/s) pour un écart de **1,99e-7**. Le noyau d`
- **T1** `./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:31489:AUTRES : (3) plafond R4 = par message, pas par session : 8 flux de 35,4 Mo (282,9 Mo cumulés > 256) tous acceptés — mais la RAM `
- **T1** `./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:32509:| la même, **KV en VRAM** (`DRAVE_GPU_KV=1`, noyaux `attn_kv_*`) | **13,2 ms** (×73) |`
- **T1** `./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:34777:- **Reproduction exécutée** : `DRAVE_GPU=1 … --banc-topk 4096` (1,2 s) et `… --banc-topk 262144` (10,7 s) → mêmes verdicts (14/1`
- **T1** `./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:35249:./reports/rapport-placement-bits-kv.md:137:| contexte long **avec** `DRAVE_GPU_KV=1` | **int8/int8** (28 %, +3,04 %) ou f32/f32 `
- **T1** `./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:35250:./docs/contexte-long.md:104:| E4 | **KV déporté sur les 2 GPU** (pagination, préchargement) | **fait** : noyau `attn_kv_*` (tuil`
- **T1** `/// en version 2 lirait `n × 4` octets d'un corps qui en fait `n × hidden × 4`,`
- **T1** `/// payait 256 allers-retours. Le corps fait `n × hidden × 4` octets ; la`
- **T1** `/// Pour quatre jetons et 7168 canaux, cela fait **142 ko**. Ce n'est pas un`
- **T1** `// distantes : **97,6 ms** d'attente contre 15,6 ms de calcul local — six fois`
- **T1** `// adverse du bloc 13). Ici : 4 copies × 1 pré-mix, trame montée à la`
- **T1** `assert!((x[40] - 1.5).abs() < 1e-6, "canal 40 = 3 × 0,5 = 1,5, vu {}", x[40]);`
- **T1** `// `n_blocs × 4` octets + un Vec<f32> (mesuré : 16 Gio sur une trame de`
- **T1** `route "GLM-5.3 : sigmoïde ×2,5" "$M/GLM-5.3-UD-IQ1_S/GLM-5.3-UD-IQ1_S-00001-of-00006.gguf" "sigmoïde"`
- **T1** `route "Kimi-K2.7 : sigmoïde ×2,827" "$M/Kimi-K2.7-Code-UD-IQ1_M/Kimi-K2.7-Code-UD-IQ1_M-00001-of-00008.gguf" "sigmoïde"`
- **T1** `# passée du RoPE simple (régime retardé du moteur) à YaRN ×16 sans mscale,`
- **T1** `#          rejeu = 688 servies, 0 manquante ; perplexité 4 221,0901 contre`
- **T1** `#   top-1 (>= 85 %), perplexité (<= 10 %) — ce dernier SEULEMENT au-delà de`
- **T1** `#   64 prédictions : sur 4 jetons, deux quantifications divergent de 25 %,`
- **T1** `#   sur 63 prédictions de 6,4 % (mesuré). Une fenêtre courte mesure le chaos.`
- **T1** `printf "  %-34s %s  ❌ (mode 4 %s > mode 2 %s)\n" "$nom" "$ecart" "$ecart" "$ecart2"; echec=1`
- **T1** `# LOT : `n` est le nombre d'ÉTATS, le corps fait n × dimension × 4.`
- **T1** `# Lire n × 4 (comme avant) laissait le client BLOQUÉ dans read_exact`
- **T1** `// coût (0,9 ko annoncés contre 1,45 réels à 20 jetons en lots de 16).`
- **T1** `drave-core/src/materiel.rs:296:        // leurs hyperthreads (+27 %, la latence mémoire est masquée et le L2`
- **T1** `drave-core/src/materiel.rs:311:rendent +27 % (14,7 -> 18,7 Go/s) en masquant la latence mémoire",`
- **T1** `drave-core/src/gguf.rs:80:/// Cette demande vise le débit parallèle, 31 Go/s.`
- **T1** `drave-core/src/engine.rs:99:    // barrière d'aliasing avec `acc` et coûtait ×3 sur le débit.`
- **T1** `drave-core/src/engine.rs:342:    // Mesuré : lier les seize fils au seul nœud 0 coûte 16 % de débit`
- **T1** `drave-core/src/engine.rs:443:                    // et le débit s'effondre (mesuré : ×3,3 de perte à 40+1`
- **T1** `drave-core/src/engine.rs:613:                    // 92 ms -> 51 ms sur le MLP, +48 % de débit.`
- **T1** `drave-core/src/main.rs:1817:        // Lectures **en parallèle** : sur un NVMe, le débit passe de 5,4 Go/s à un`
- **T1** `> Budget par jeton **mesuré** : **86,787 Go** — experts routés 25,830 (29,8 %),`
- **T1** `> dense 60,958 (70,2 %). Le dense pèse 2,3× les experts : aucune technique sur`
- **T1** `> les experts n'adresse plus de 30 % du trafic d'un jeton.`
- **T1** `> sans avoir jamais été mesuré, vaut **×1,58** (Qwen3-30B-A3B, invite de`
- **T1** `> refermés (« paires experts » tombait à 1 % dès le lot 2), et `forward_lot``
- **T1** `> **11 % de CPU** (borné par le disque : 1,80 To lus, 451 Go/jeton, 5,2 balayages`
- **T1** `>   trace** — 25 à 60 % des positions sur la donnée à une unité, 3 % à dix unités.`
- **T1** `| `DRAVE_KV_BITS=8` ou `4` | quantifie le cache KV (défaut f32) | le 4 bits coûte +364 % de perplexité à 8 192 |`
- **T1** `| `DRAVE_KV_K_F32=1` | garde les CLÉS en f32 (valeurs quantifiées) | mesuré : à 8 192, **64 %** de la taille f32 (5,125 octets par élément, échelles comprises) pour +0,023 %, contre +3,04 % pour l'int`
- **T1** `| `DRAVE_KV_V_F32=1` | garde les VALEURS en f32 | +3,01 % : ne sert à rien, l'erreur ne passe pas par là |`
- **T1** `| `DRAVE_KV_K_F16=1` | clés en **f16** (2 octets/valeur, précision relative) | **le meilleur réglage mesuré** : à 8 192 jetons, clés f16 + valeurs int8 = **+0,018 %** pour **39 % de la taille f32** — `
- **T1** `| `DRAVE_TRACE_BLOCS=1` | trace DRVF **v3** : valeurs i8, échelle f16 par bloc de 32 | 45 079 930 o contre 66 370 408 en v2 (−32 %), rejeu 19,4029 contre 19,3885 (+0,074 %) |`
- **T1** `elle seule les projections Q8_0 de plus de 8 Mo, ce qui change le chiffre de`
- **T1** `0,06 % (15,1757 → 15,1667 sur gpt-oss).`
- **T1** `réparti prenant le temps du calcul local (19,7 contre 19,4 ms par jeton). Il a`
- **T1** ``TCP_NODELAY` a divisé l'attente du pair par six (**97,6 → 16,1 ms** par jeton,`
- **T1** `0 ms, 1,99× à 5 ms, 4,89× à 20 ms, fidélité intacte (0,00e0) dans les trois cas.`
- **T1** `0,25 Mbit/s suffisent. Un aller-retour Colab de 60 ms donnerait ~8 jetons/s`
- **T1** `KV int8 (+3,0 % à 8 192) vient **entièrement des clés** — clés f32 + valeurs int8`
- **T1** `donne +0,023 %, clés int8 + valeurs f32 donne +3,01 %. Réglage utilisable tout de`
- **T1** `suite : `DRAVE_KV_BITS=8 DRAVE_KV_K_F32=1` (75 % de la taille f32 pour +0,02 %).`
- **T1** `(`git bundle`, 4,5 Mo — il n'y a pas de dépôt distant) et vérifie l'empreinte du`
- **T1** `| rejeu `--flux-forcer` | 19,3885 | 19,3885 | 19,4029 (+0,074 %) |`
- **T1** `seuil 0,01 : **1,5 ko par jeton au lieu de 3,5** (÷2,3) pour un écart de 3,03e-2 —`
- **T1** `Le remède tient en 142 ko : flux (4 × 7168 f32) + pile (2 banques × 4 × 7168 f32).`
- **T1** `A : 0..12  -> relais « reprend à la couche 13 · 4 jetons × 7168 canaux · 2 banques »`
- **T1** `| `8e04c99a` | 2026-09-30 18:17 | 0.7 Mo | 118 Ko | 1 | 59 | 85 | 0 | 0 |`
- **T1** `| `aa5f9fc5` | 2026-09-30 15:17 | 0.8 Mo | 129 Ko | 1 | 78 | 100 | 0 | 0 |`
- **T1** `| `b13a6032` | 2026-10-02 15:09 | 0.3 Mo | 88 Ko | 1 | 17 | 43 | 0 | 0 |`
- **T1** `-| `bbd6969f` | 2026-10-07 20:29 | 56.7 Mo | 8962 Ko | 205 | 9590 | 9012 | 63 | 26 |`
- **T1** `+| `bbd6969f` | 2026-10-07 20:45 | 56.7 Mo | 8968 Ko | 205 | 9596 | 9018 | 63 | 26 |`
- **T1** `| `bcfe0b97` | 2026-09-30 12:39 | 1.0 Mo | 145 Ko | 1 | 102 | 110 | 0 | 0 |`
- **T1** `| `c25f97d1` | 2026-09-30 11:59 | 0.8 Mo | 126 Ko | 1 | 73 | 104 | 0 | 0 |`
- **T1** `| `c776b71f` | 2026-09-30 18:43 | 0.7 Mo | 82 Ko | 1 | 35 | 54 | 0 | 0 |`
- **T1** `17:| 0.3 | **Le format EST le contrat d'échange** (phase 3) : versionné, en-tête + paires | ✅ | codec de référence (`tools/flux_codec.py`) : aller-retour **identique** sur 132 Mo ; **et le rejeu dans `
- **T1** `58:| 3.4 | **Démonstration Colab** : préremplissage réparti (le décodage reste séquentiel — c'est écrit dans la vision) | 🔬 | **le préremplissage par lots sur le fil est FAIT et fidèle** (mode 3 : 256`
- **T1** `| 2.2 | **Streaming des poids depuis le NVMe** (3,5 Go/s) pour ce qui ne tient pas en RAM — c'est la même idée : ne lire que ce qui parle | ⏳ | un modèle > RAM exécuté, débit mesuré |`
- **T1** `| 2.3 | **Cache d'experts rentable** : +6 % aujourd'hui ; grouper les trois projections par expert et supprimer les copies | ⏳ | ≥ +30 %, sinon abandonné (et écrit) |`
- **T1** `| 3.2 | **Granularité** : par couche, par bloc de canaux, par expert | ✅ | listes i16, **échelles par bloc (i8)** et **indices par écarts** (1 608 octets par flux à 256 jetons) ; **mode 4 « lot en lis`
- **T1** `| 3.3 | **Seuil de rentabilité** : à partir de quel débit réseau le découpage gagne | 🔬 | mesuré jusqu'à 20 ms de latence par message (`tools/proxy_latence.py`) : **attente ≈ calcul distant + 3,2 × la`
- **T1** `| 3.4 | **Démonstration Colab** : préremplissage réparti (le décodage reste séquentiel — c'est écrit dans la vision) | 🔬 | **le préremplissage par lots sur le fil est FAIT et fidèle** (mode 3 : 256 je`
- **T1** `redonne **exactement** le calcul local — écart **0,00e0**, perplexité 144,8289 des`
- **T1** `s'améliore : à sparsité égale (seuil 0,02, 59 % d'activité) les blocs font`
- **T1** `**1 745 octets contre 2 159** pour la liste i16, et 14 % d'écart contre 16 % —`
- **T1** `est donc le seuil **0,01** : **÷2,3 sur le fil pour 2,7 %** d'écart — et l'écart DÉCROÎT avec la`
- **T1** `longueur (13,7 % à 64 jetons, 6,4 % à 128, 2,7 % à 256, **1,3 % à 1 024**) : la perturbation est`
- **T1** `courbe et les deux formulations que la mesure a corrigées (« ÷2 pour 0,2 % »,`
- **T1** `de 12 couches prend 15,9 ms par jeton, l'attente du pair 16,1 ms — soit **1,01×**.`
- **T1** `identiques. Avant `TCP_NODELAY`, cette attente était de 97,6 ms (6,26×) : le`
- **T1** `**jeter des canaux coûte cher** — l'écart est déjà de 2,6 % à 16 bits pleins,`
- **T1** `| avant correction | 144,8289 | 1 621,7239 | ×11,2 |`
- **T1** `| après la norme seule | 144,8289 | 693,4492 | ×4,8 |`
- **T1** ``tools/preparer_colab.sh` produit le dépôt en **un fichier** (`drave.bundle`, 4,5 Mo`
- **T1** `| latence | ✅ `TCP_NODELAY` : 16,1 ms d'attente contre 15,9 ms de calcul local (97,6 ms avant) |`
- **T1** `| **préremplissage par lots sur le fil** | ✅ mode 3, `--lot T` : 256 jetons en 4 lots, écart **0,00e0** (`reports/rapport-prefill-reparti.md`) ; mode 4 (lot en listes) : 1,5 ko par jeton au lieu de 3,`
- **T1** `listes à échelle par bloc à 68 % d'activité. En **lots** (`--lot 64`), c'est`
- **T1** `229 455 octets par lot de 64 jetons, soit **3,5 ko par jeton** — et surtout UN`
- **T1** `| 0 ms (localhost) | 16,8 ms | 1,01× |`
- **T1** `| 5 ms | 33,0 ms | 1,99× |`
- **T1** `| 20 ms | 81,8 ms | 4,89× |`
- **T1** `Un aller-retour Colab de 60 ms donne donc ≈ 112 ms par jeton, soit ~8 jetons/s`
- **T1** `relais qui ajoute 20 ms par message (64 jetons, 12 couches par nœud), un seul`
- **T1** `/// cette machine : CPU 14–25 Go/s, PCIe x8 6,5 Go/s, NVLink 25,78 Go/s,`
- **T1** `/// GPU 380 Go/s en lecture locale.`
- **T1** `else { "GPU (PCIe 6,5 Go/s)" };`
- **T1** `// Mesuré sur le 30B-A3B : les tranches d'experts sont lues à 8 Go/s,`
- **T1** `// pas 20 — dix-huit mille tranches de 900 Ko dispersées sur 18 Go`
- **T1** `println!("  à       8.0 Go/s (MoE épars, mesuré) : {:>7.2} tok/s",`
- **T1** `println!("  KV par jeton et par couche : {} têtes KV × {} dim × 2 (K et V)",`
- **T1** `l'empreinte) ; le reste se lit à la demande — mesuré, 90 % des appels tiennent dans \`
- **T1** `46 % de l'empreinte", experts_go, pour_ram, 100.0 * part));`
- **T1** `// Taux de succès du cache d'experts : mesuré, 25 % de l'empreinte sert`
- **T1** `// 80 % des appels. On l'applique au trafic, pas à la place occupée.`
- **T1** `assert_eq!(moe.numeros, vec![1], "la vue porte le NUMÉRO 1, pas le rang 0");`
- **T1** `/// `local[couche][expert_global]` = `cluster × 65536 + ligne`, ou -1 si cet`
- **T1** `// Mesuré : lier les seize fils au seul nœud 0 coûte 16 % de débit`
- **T1** `// reste. Mesuré : la VRAM lit à 84,9 Go/s contre 22,5 pour la RAM,`
- **T1** `// et un cache de 25 % de l'empreinte sert 80 % des appels.`
- **T1** `// KV de MLA pèse 90 Ko par jeton en F16, soit 96,6 Go à 1 M de jetons —`
- … (tronqué)

## 5. Erreurs rencontrées

2 sorties en erreur ou divergentes. Les premières :

- **T1** : #!/bin/bash # Les portes du dépôt, en une commande. # # Un chiffre de référence qui dérive sans qu'on s'en aperçoive ne vaut rien : # chaque porte est comparée à la valeur ATTENDUE, et le script sort 
- **T1** : #!/bin/bash # CHANTIER 3 — LA PORTE DE CORRECTION DU DÉCOUPAGE. # # Deux nœuds doivent donner EXACTEMENT ce que donne la passe monolithe. On # coupe à la couche 13, donc on TRAVERSE la banque de la co

