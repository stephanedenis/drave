# Session 4e786d3f — Tu es un relecteur ADVERSARIAL.

| | |
|---|---|
| Identifiant | `4e786d3f-0b66-4b23-8dc4-b452bc383bea` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-02 10:08 |
| Durée | 0.2 h |
| Tours | 1 |
| Messages | 80 |
| Appels d'outils | 129 |
| Fichiers touchés | 0 |
| Commandes | 125 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu es un relecteur ADVERSARIAL. Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (moteur d'inférence Rust nommé Drave). Tu ne dois MODIFIER AUCUN fichier : ta sortie est un rapport en markdown, rien d'autre. N'utilise que la lecture (read, grep, glob, bash en lecture seule). N'exécute aucun modèle (pas de forward, pas de --ppl) : les runs lourds sont déjà en cours.  CONT … [4133 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu es un relecteur ADVERSARIAL. Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (moteur d'in … [4413 caractères tronqués]

*129 appels d'outils.* Actions notables :

- bash — Show git status and diff stat
- bash — Show recent git log and branch
- bash — Diff of model.rs, portes.sh, REPRISE.md
- bash — Diff of docs, first half
- bash — Read docs diff lines 250-600
- bash — Read docs diff lines 600-969
- bash — Check flux protocol constants
- bash — Check YaRN 4x threshold in model.rs
- bash — Check activation density and push/pull crossover
- bash — List reports directory
- bash — Read TAILLE_TETE definition
- bash — Extract and test file refs in added lines
- bash — Test markdown link targets and tools scripts
- bash — Explicit existence check of cited docs and reports
- … et 113 autres

**Synthèse produite :**

Le rapport complet est ci-dessus et a été transmis au parent (`bbd6969f…`) sous forme autonome. Résumé en trois lignes, sans flatterie :

- **14 corrections problématiques** documentées avec citation exacte, correctif textuel et gravité, dont **une haute** : `REPRISE.md:114` affirme encore la politique YaRN périmée (bascule à 1× la longueur déclarée) que le moteur n'applique plus (4×, `model.rs:2203`) et que le reste du même fichier a été mis à jour.
- **Le correctif `model.rs` est fonctionnellement sain** : `sinks` est bien consommé dans tous les chemins d'attention, aucun modèle du parc ne combine chemin MLA et `attn_sinks`, et `--config` donne gpt-oss = oui / V4-Flash et V4.1 = NON pour d'autres raisons. Deux résidus : une closure morte (l. 92) et un commentaire (l. 137-139) qui dit le contraire du message réécrit juste en dessous ; plus une affirmation fausse sur `--config` (l. 126).
- **`tools/portes.sh` section 7 : rien à redire** sur le fond (`bash -n` OK, `valeur`/`compare` cohérents, commande identique à la recette) — seule la ligne 118 est cosmétique.

Les six points à trancher (dont « 19 ou 18 formats lisibles » et l'affirmation « identique à l'original » non mesurée) sont en fin de rapport.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** Show git status and diff stat
- **T1** Show recent git log and branch
- **T1** Diff of model.rs, portes.sh, REPRISE.md
- **T1** Diff of docs, first half
- **T1** Read docs diff lines 250-600
- **T1** Read docs diff lines 600-969
- **T1** Check flux protocol constants
- **T1** Check YaRN 4x threshold in model.rs
- **T1** Check activation density and push/pull crossover
- **T1** List reports directory
- **T1** Read TAILLE_TETE definition
- **T1** Extract and test file refs in added lines
- **T1** Test markdown link targets and tools scripts
- **T1** Explicit existence check of cited docs and reports
- **T1** Verify MLA report figures and sections
- **T1** Verify prefill report figures
- **T1** Verify routing and gpt-oss reports
- **T1** Verify KV int4 219% figure
- **T1** Search for 219 percent claim
- **T1** Check llama.cpp q8_0 reference and contexte-long E2/E3
- **T1** Read contexte-long KV table
- **T1** Read REPRISE KV rows
- **T1** Grep sinks usage across drave-core
- **T1** Read manques_architecture context
- **T1** Grep attn_sinks and puits in sources
- **T1** Read attention softmax with sinks
- **T1** List available GGUF model files
- **T1** Grep calculable and perplexite output
- **T1** Check tokenize flags, data and models dirs
- **T1** Find === perplexite print statements
- **T1** Find ppl total print
- **T1** List sharded GGUF files
- **T1** Grep attn_derope references
- **T1** Scan GGUF headers for attn_sinks and attn_derope
- **T1** Run --config on gpt-oss
- **T1** Read context of puits appris print
- **T1** Find --config handler in main.rs
- **T1** Find enclosing function of the puits print
- **T1** Read --config implementation
- **T1** Run --config on V4-Flash and V4.1
- … et 85 autres

## 4. Mesures et résultats marquants

- **T1** `acc3498 L'écart naît APRÈS la couche 0 : 1,9 % / 1,3 % / 3,8 % / 4,0 % aux positions 0-3`
- **T1** `> du pilote, et `--gpu-banc` retrouve l'exactitude des noyaux — 1,6 ms par ligne`
- **T1** `| 3 | KV int8 puis int4 | **fait, jusqu'à 8 192** | **échelles par bloc de 32** : int8 +**1,5 %** à 512 (était +7,1 %), **+3,0 % à 8 192** (llama.cpp +0,8 %) ; int4 **+364 % à 8 192** contre +494 % po`
- **T1** `| 4 | préremplissage par lots | **fait, −20 % et attribué** | tuilage, **attention groupée dans le lot** et **tête en lot** (`logits_lot`) : Qwen ctx 512, **17,1 s → 13,6 s (−20 %)** à perplexité égal`
- **T1** `| 5 | échelles par bloc pour `DenseQ8` | **fait, hypothèse réfutée** | 23,696 contre 23,612 : les échelles par bloc n'apportent rien ; l'avantage du 6 bits est son coût (25 % d'octets en moins à quali`
- **T1** `#    moteur déporte alors tout seul les projections Q8_0 de plus de 8 Mo — le`
- **T1** `+#    du même ordre que les 0,06 % mesurés alors — non re-mesuré depuis.)`
- **T1** `@@ -88,9 +88,34 @@ route "Kimi-K2.7 : sigmoïde ×2,827" "$M/Kimi-K2.7-Code-UD-IQ1_M/Kimi-K2.7-Code`
- **T1** `listes à échelle par bloc à 68 % d'activité. En **lots** (`--lot 64`), c'est`
- **T1** `229 455 octets par lot de 64 jetons, soit **3,5 ko par jeton** — et surtout UN`
- **T1** `+| Énergie par opération | E_AC = 0,9 pJ contre E_MAC = 4,5 pJ (Horowitz) | 8,3 nJ/événement (FPGA, **projeté** : 4,83 G évts/s, limite DDR3) contre 57 nJ (CPU, **mesuré**) — rapport 6,9× |`
- **T1** `+qui s'active » reste théorique. À seuil 5 % du max, la densité mesurée tombe à`
- **T1** `+**17,9 %** — sous le croisement push/pull de **22 %**`
- **T1** `- Les gains annoncés (32×, 57 %) sont **théoriques**, calculés avec`
- **T1** `-| E2 | **KV int8** | **fait** (échelle par vecteur, dequantification à la lecture) | ÷4 sur le KV ; 128 k confortable | mesuré : +7,1 % de perplexité (llama.cpp q8_0 : +3,1 %) |`
- **T1** `-| E3 | **KV int4** | **fait** (nibbles empaquetés) | 1 M tient en RAM (9,7 Go) et en VRAM | mesuré : **+384 %** à 512 jetons, **+364 % à 8 192** — llama.cpp q4_0 : +411 % puis +494 % ; à réserver aux`
- **T1** `+| E1 | **Préremplissage par lots** | **fait** : `gemm_dense_i8` et `gemm_dense_q4` (produits matrice-matrice par tranches), `forward_lot` juste sur dense **et** sur MoE avec regroupement des jetons p`
- **T1** `+| E2 | **KV int8** | **fait** (échelle **par bloc de 32**, dequantification à la lecture) | ÷4 sur le KV ; 128 k confortable | mesuré : **+1,5 %** à 512 jetons, **+3,0 %** à 8 192 (llama.cpp q8_0 : +`
- **T1** `+| E3 | **KV int4** | **fait** (nibbles empaquetés) | 1 M tient en RAM (9,7 Go) et en VRAM | mesuré : **+219 %** à 512 jetons, **+364 % à 8 192** — llama.cpp q4_0 : +411 % puis +494 % ; à réserver aux`
- **T1** `| E4 | **KV déporté sur les 2 GPU** (pagination, préchargement) | **fait** : noyau `attn_kv_*` (tuiles de 32 clés en mémoire partagée, une passe par (tête KV, tranche), recombinaison + puits), miroir `
- **T1** `- **restreindre aux 256 meilleures clés AMÉLIORE la perplexité** (−21 %) : sur du`
- **T1** `-en-tête      magie, version, nb_calques, nb_tenseurs, alignement (2 Mo), graine`
- **T1** `+en-tête      magie, version, nb_couches, nb_tenseurs, alignement (2 Mo), graine`
- **T1** `5. **L'alignement 2 Mo** est ce qui permettra les grosses pages le jour où mmap`
- **T1** `@@ -161,12 +167,12 @@ coûté : **12 % de perplexité** sur Q4_0 avant qu'on s'en aperçoive.`
- **T1** `| 1 | emprunt des blocs en place (Q4_0, MXFP4) | ✅ **fait** | chargement ×3,2, mémoire ÷2, fidélité exacte |`
- **T1** `-| 5 | placement : épinglage NUMA, threads par calque | à faire | 20,7 → 24,7 Go/s mesuré au banc |`
- **T1** `+| 5 | placement : épinglage NUMA, threads par couche | ✅ mesuré, **perdant** (`--pin` : 23,2 → 27,6 s) | 20,7 → 24,7 Go/s mesuré au banc |`
- **T1** `+| 6 | **Q8_0 en place** (projections) | ✅ **fait** | chargement 2,73 → 0,81 s, mémoire 921 → 566 Mo |`
- **T1** `@@ -244,12 +250,14 @@ chiffre maintenant aussi ce régime — 4,81 tok/s prévus contre 5,4 mesurés.`
- **T1** `-2. **Épinglage NUMA** : 20 % mesurés, mais `sched_setaffinity` n'est pas dans`
- **T1** `+> 921 → 566 Mo).`
- **T1** `18,56** et **625 ms au lieu de 3,9 s** sur Qwen3-30B-A3B.`
- **T1** `jetons, 16 par lot, seuil 0,01 : **1,5 ko par jeton au lieu de 3,5** (÷2,3) pour`
- **T1** `| en-têtes + inventaire | 1 046 tenseurs, 365,70 Go en **63,8 ms** (mmap) |`
- **T1** `| description | **74 ms** : 40 couches, 384 experts top-6, racine de softplus ×1,5, routage par table des 3 premières couches |`
- **T1** `| tables d'engram | 10 000 entrées en **219–524 ms**, 2,6 Mo touchés par table, **120 Mo de RSS** pour 365,7 Go |`
- **T1** `doit montrer l'effet cherché : **968 ms → quelques dizaines de ms par couche**.`
- **T1** `@@ -91,9 +96,9 @@ doit montrer l'effet cherché : **968 ms → quelques dizaines de ms par couche*`
- **T1** `| 5 | mesure 1 M : ms/layer avec et sans top-k, sur GPU | ✅ **fait au niveau des noyaux** : la chaîne complète (scores sans relecture + 4 passes + collecte + somme) coûte **3,90 ms** pour 14 lignes × `
- **T1** `(matrice `[512, n_head × 192]`, soit ~1 Mo en Q8 : le coût est réel mais petit`
- **T1** `-| **DeepSeek-V4.1-Flash** | le plus lourd des ouverts, MoE, agentique | **365,7 Go** (Q2) | — | **en cours** (26 % à 09h36) |`
- **T1** `+| **MiniMax-H3** | famille différente (vision+langage) | 22,8 Go au total (2 × 11,42 Go, Q4_K) | — | ✅ arrivé |`
- **T1** `| 5 | **format** : manifeste + index + disposition contiguë | ✅ **écrit et mesuré sur Qwen3-30B-A3B** : `commun.gguf` + 8 `cluster-XX.gguf`, un nœud charge **3,20 Go au lieu de 18,56** et 625 ms au li`
- **T1** `nommées. Journaliser les listes d'activations (1,2 Mo/token, **+3,0 %**)`
- **T1** `borné par la dispersion (10,4 Go/s utilisés sur 28,7) : **2,8× de marge`
- **T1** `-| Inférence 0,5 B quantifié, CPU seul, sans GPU ni BLAS | **15,8 tok/s**, perplexité 24,90 (référence float32 : 25,00) |`
- **T1** `+| Inférence 0,5 B quantifié, CPU seul, sans GPU ni BLAS | **15,8 tok/s**, perplexité 24,90 (référence float32 : 25,00) — et **5,3 G événements/s** : le coût suit l'activité (`reports/rapport-inferenc`
- **T1** `| Moteur d'événements | 5,3 G événements/s, 2 547 lignes de Rust sans dépendance |`
- **T1** `| Carte FPGA | PE vérifié sur 309 020 événements réels, synthétisé (176 ALMs, 0 DSP), lecteur DDR3 vérifié de bout en bout |`
- **T1** `| 1.2 | **Quantification choisie par la mesure** : par couche, par tenseur, plutôt qu'un réglage global | 🔬 | la densité par couche varie de **20 % à 56 %** (`reports/rapport-analyse-flux.md`) : la dé`
- **T1** `| 1.4 | **Écart int8 résiduel** (+3,0 % contre +0,8 % chez llama.cpp à 8 192) | ✅ | **attribué** : tout l'écart est dans les CLÉS (clés f32 + valeurs int8 = +0,023 % ; l'inverse = +3,01 %) ; **courbe `
- **T1** `| 3.2 | **Granularité** : par couche, par bloc de canaux, par expert | ✅ | listes i16, **échelles par bloc (i8)** et **indices par écarts** (1 608 octets par flux à 256 jetons) ; **mode 4 « lot en lis`
- **T1** `| 3.3 | **Seuil de rentabilité** : à partir de quel débit réseau le découpage gagne | 🔬 | mesuré jusqu'à 20 ms de latence par message (`tools/proxy_latence.py`) : **attente ≈ calcul distant + 3,2 × la`
- **T1** `| 3.4 | **Démonstration Colab** : préremplissage réparti (le décodage reste séquentiel — c'est écrit dans la vision) | 🔬 | **le préremplissage par lots sur le fil est FAIT et fidèle** (mode 3 : 256 je`
- **T1** `@@ -183,7 +183,8 @@ coûte +0,023 % là où clés int8 + valeurs f32 coûte +3,01 % (facteur 130), e`
- **T1** `Les **clés en f16** sont mesurées : clés f16 + valeurs int8 = **+0,018 %** à`
- **T1** `8 192 jetons pour **39 % de la taille f32** — le meilleur réglage de la courbe`
- **T1** `(les clés f32, à 64 % de la taille, font +0,023 % ; l'int8 complet, à 28 %, +3,04 %).`
- **T1** `+Clés f16 + valeurs int4 : **+0,61 %** à 33 % de la taille f32`
- **T1** `(62,5 % de la taille f32 — si les valeurs tolèrent 4 bits, ce réglage bat l'int8`
- **T1** `* **top 10 % des neurones portent 33,1 % de la magnitude** ; seuls **0,08 %** sont`
- **T1** `« chauds » plus de 90 % du temps — donc un préchargement statique ne paie pas,`
- **T1** `| experts MXFP4 | cache VRAM LRU | **+6 %** — mesuré, verdict : ne pas activer tel quel |`
- **T1** `+   latence aller-retour jusqu'à 20 ms, attente ≈ calcul distant + 3,2 × latence`
- **T1** `* l'int8 sur le cache KV coûte **+1,5 %** de perplexité à 512 jetons et`
- **T1** `**+3,0 %** à 8 192, là où l'int4 coûte +364 % — le débat n'est pas « combien de`
- **T1** `**7,0 ms** par couche à 1 M (308 Go/s, 69 % de la bande VRAM) : quand le`
- **T1** `+| **3. Répartir sur machines** | **transport en place et fidèle** (`0,00e0`, protocole v5, cinq modes) ; mesuré : 1 608 octets/flux, 0,25 Mbit/s, latence ≤ 20 ms | ordonnanceur de placement ; granula`
- **T1** `reports/rapport-localite-activation.md:24:| opérateurs creux par neurone | chemin par **listes d'événements** (`SparseVec`, push) | bascule push/pull mesurée à **22 % de densité** (`seuil_push = 0.22``
- **T1** `reports/rapport-localite-activation.md:43:| densité d'activation (seuil 5 % du max) | **17,9 %** des neurones par jeton (82 % ne font rien) |`
- **T1** `125:soit −20 %**, à perplexité identique (13,1368 → 13,1359). Sur gpt-oss (MoE`
- **T1** `127:**33,7 / 33,9 / 34,4 s**, perplexité 13,7205 dans tous les cas.`
- **T1** `193:| Qwen2.5-0.5B Q8_0, `--dense`, 16 fils | 512 | 17,1 s | **13,6 s** | **−20 %** |`
- **T1** `194:| gpt-oss-120b MXFP4, MoE groupé, 16 fils | 256 | ≈ 50 s | 34,4 s (lot 256) | **−31 %** |`
- **T1** `reports/rapport-placement-bits-kv.md:22:| int4 | int4 | 1,25 | 16 % | 66,0369 | **+364 %** |`
- **T1** `reports/rapport-placement-bits-kv.md:30:16 %  int4/int4 ................ +364 %`
- **T1** `reports/rapport-placement-bits-kv.md:52:   Et le 4 bits des DEUX côtés (1,25 octet, 16 % du f32) coûte **+364 %** : c'est`
- **T1** `reports/rapport-attribution-kv.md:35:l'int8 complet (28 %, soit 2,25 octets) coûte +3,0 %. C'est le`
- **T1** `reports/rapport-execution-v41.md:18:| sonde engram (`--sonder-engram 10000`) | mmap, 16 lecteurs | table 1 : 10 000 entrées en **524 ms** (2,6 Mo touchés sur 101,4 Go) · table 2 : **219 ms** · RSS max`
- **T1** `docs/contexte-long.md:103:| E3 | **KV int4** | **fait** (nibbles empaquetés) | 1 M tient en RAM (9,7 Go) et en VRAM | mesuré : **+219 %** à 512 jetons, **+364 % à 8 192** — llama.cpp q4_0 : +411 % pui`
- **T1** `docs/contexte-long.md:144:| int4 | 63,6107 (+384 %) | **41,9442 (+219 %)** | **49,9438 (+287 %)** |`
- **T1** `docs/plan-deepseek41-complet.md:70:| tables d'engram | 10 000 entrées en **219–524 ms**, 2,6 Mo touchés par table, **120 Mo de RSS** pour 365,7 Go |`
- **T1** `REPRISE.md:189:| KV int4, échelles par bloc | +219 % (512) et +287 % (4 591) — était +384 % et +450 % |`
- **T1** `REPRISE.md:194:| KV déporté dans le moteur (`DRAVE_GPU_KV=1`, ctx 4 096) | attention **22,16 → 3,29 ms/jeton** (÷6,7) · balayage 219,4 → **136,2 s** · perplexité 12,2177 → 12,2175 |`
- **T1** `REPRISE.md:1172:74 ms, plan matériel complet, sonde engram 10 000 entrées en 219-524 ms avec`
- **T1** `reports/rapport-placement-bits-kv.md:5:donnent 39 % de la taille f32 pour **+0,018 %**.`
- **T1** `reports/rapport-placement-bits-kv.md:21:| **f16** | **int8** | **3,125** | **39 %** | **14,2365** | **+0,018 %** |`
- **T1** `reports/rapport-placement-bits-kv.md:33:39 %  clés f16 · valeurs int8 .. +0,018 %   ← le meilleur point`
- **T1** `reports/rapport-placement-bits-kv.md:59:   (39 % du f32) pour **+0,018 %** — contre 5,125 octets (64 %) pour les clés f32`
- **T1** `reports/rapport-placement-bits-kv.md:65:   taille f32** pour +0,018 %, là où l'int8 complet (28 %) coûte +3,04 %.`
- **T1** `reports/rapport-placement-bits-kv.md:67:5. **La perspective llama.cpp** : son cache q8_0 coûte +0,8 % à la même longueur.`
- **T1** `reports/rapport-placement-bits-kv.md:77:8 192 jetons : **+0,018 %** pour 3,125 octets par élément (**39 %** du f32), et à`
- **T1** `reports/rapport-placement-bits-kv.md:88:| clés f16 · valeurs int8 | **12,2188** | **+0,011 %** | 14,2365 | +0,018 % |`
- **T1** `reports/rapport-placement-bits-kv.md:100:+0,018 % contre +0,023 % à 8 192) — pour **moitié moins d'octets**. On ne prétend`
- **T1** `reports/rapport-placement-bits-kv.md:136:| contexte court ou moyen, CPU | **clés f16 + valeurs int8** (39 % du f32, +0,018 %) | le meilleur compromis taille/qualité, et le temps CPU n'y est pas le fac`
- **T1** `reports/rapport-attribution-kv.md:38:Perspective : llama.cpp paie +0,8 % pour son cache int8 à la même longueur. Notre`
- **T1** `reports/rapport-attribution-kv.md:51:   clés int8 sous celui de llama.cpp (+0,8 %).`
- **T1** `REPRISE.md:167:| 3 | KV int8 puis int4 | **fait, jusqu'à 8 192** | **échelles par bloc de 32** : int8 +**1,5 %** à 512 (était +7,1 %), **+3,0 % à 8 192** (llama.cpp +0,8 %) ; int4 **+364 % à 8 192** c`
- **T1** `REPRISE.md:190:| KV à 8 192 jetons (longueur de la référence llama.cpp) | f32 **14,2339** · int8 **14,6667 (+3,0 %)** contre +0,8 % chez llama.cpp · int4 **66,0369 (+364 %)** contre +494 % chez llama.`
- **T1** `REPRISE.md:264:| `DRAVE_KV_K_F16=1` | clés en **f16** (2 octets/valeur, précision relative) | **le meilleur réglage mesuré** : à 8 192 jetons, clés f16 + valeurs int8 = **+0,018 %** pour **39 % de la `
- **T1** `REPRISE.md:394:= +0,011 % et +0,018 %, int8/int8 = +2,25 % et +3,04 %. Les clés f16 font aussi`
- **T1** `REPRISE.md:557:| clés f16 · valeurs int8 | 3,125 | **39 %** | **+0,018 %** ← le meilleur point |`
- **T1** `| E1 | **Préremplissage par lots** | **fait** : `gemm_dense_i8` et `gemm_dense_q4` (produits matrice-matrice par tranches), `forward_lot` juste sur dense **et** sur MoE avec regroupement des jetons pa`
- **T1** `| E2 | **KV int8** | **fait** (échelle **par bloc de 32**, dequantification à la lecture) | ÷4 sur le KV ; 128 k confortable | mesuré : **+1,5 %** à 512 jetons, **+3,0 %** à 8 192 (llama.cpp q8_0 : +0`
- **T1** `| E3 | **KV int4** | **fait** (nibbles empaquetés) | 1 M tient en RAM (9,7 Go) et en VRAM | mesuré : **+219 %** à 512 jetons, **+364 % à 8 192** — llama.cpp q4_0 : +411 % puis +494 % ; à réserver aux `
- **T1** `| **int8** | **14,07** (+7,1 %) | 14,68 (+3,1 %) | **13,58** (+5,2 %) | 16,73 (+0,8 %) |`
- **T1** `| **int4** | **63,61** (+384 %) | 72,80 (+411 %) | **71,05** (+450 %) | 98,53 (+494 %) |`
- **T1** `3. **Notre int8 était plus cher que celui de llama.cpp** (+5,2 % contre +0,8 %)`
- **T1** `| int8 | 14,0707 (+7,1 %) | **13,3360 (+1,5 %)** | **13,3459 (+3,4 %)** |`
- **T1** `| int4 | 63,6107 (+384 %) | **41,9442 (+219 %)** | **49,9438 (+287 %)** |`
- **T1** `L'écart avec llama.cpp (+0,8 %) est donc comblé à contexte court, et le 4 bits`
- **T1** `| **int8** | **14,6667** | **+3,0 %** | 16,73 | +0,8 % | 1 144 s |`
- **T1** `| **int4** | **66,0369** | **+364 %** | 98,53 | +494 % | 1 461 s |`
- **T1** `| noyau GPU Q4_K warp (Qwen 1.5B, 7,7 Mo) | 0,5 ms contre 1,2 ms CPU (×2,2), écart 4e-7 |`
- **T1** `| noyau GPU Q6_K warp (tête liée Qwen 1.5B, 191,4 Mo) | **3,6 ms** contre 8,3 ms CPU 16 fils (23,2 → 53,6 Go/s), écart 3,3e-7 |`
- **T1** `| noyau GPU Q6_K warp (ffn_down Qwen 1.5B, 11,3 Mo) | **0,3 ms** contre 1,5 ms CPU (×5), écart 7,1e-7 |`
- **T1** `| tête Q6_K déportée (Qwen 1.5B Q4_K_M, ctx 256, 510 jetons) | 7,58 → **3,60 ms/jeton** ; bout en bout 44,4 → 41,4 s (−7 %) ; lot 512 : 36,0 → 34,0 s ; **perplexité identique** (13,6877 / 13,6864) |`
- **T1** `| préremplissage par lots (Qwen, ctx 512) | lot 1 = **17,1 s** · lot 512 = **13,6 s** → **−20 %** (perplexité 13,1368 → 13,1359) |`
- **T1** `| tête de sortie en lot | **aucun gain** (5,47 contre 5,63 ms/jeton) : noyau lié au calcul — il faut AVX2 ou le GPU |`
- … (tronqué)

## 5. Erreurs rencontrées

3 sorties en erreur ou divergentes. Les premières :

- **T1** : diff --git a/REPRISE.md b/REPRISE.md index e256ad6..3c5deda 100644 --- a/REPRISE.md +++ b/REPRISE.md @@ -36,6 +36,15 @@ cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core && cargo build --r
- **T1** : ### /home/stephane/Data13TB/stephane/modeles/gguf/DeepSeek-V4-Flash-UD-IQ1_M/DeepSeek-V4-Flash-UD-IQ1_M-00001-of-00003.gguf routage       : racine de softplus (source : expert_gating_func) · renormali
- **T1** : === session dir === journal/sessions/8b6d46ab-6ad0-4648-92a8-0bec40a02526 digest.md rapport.md session.jsonl.zstd === tests === unit #[test]: 48 integration:  [exit code: 2]

