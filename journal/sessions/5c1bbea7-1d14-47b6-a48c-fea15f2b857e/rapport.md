# Session 5c1bbea7 — Tu es relecteur ADVERSE. Tu

| | |
|---|---|
| Identifiant | `5c1bbea7-1d14-47b6-a48c-fea15f2b857e` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-02 09:52 |
| Durée | 0.1 h |
| Tours | 1 |
| Messages | 43 |
| Appels d'outils | 52 |
| Fichiers touchés | 0 |
| Commandes | 43 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu es relecteur ADVERSE. Tu ne modifies AUCUN fichier : tu produis un rapport de constats, avec citations exactes et numéros de ligne.  Contexte : le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet contient un moteur d'inférence nommé **Drave**. Sa vision est définie dans `docs/vision.md` et `docs/programme-recherche.md` — lis-les ENTIER d'abord (textes de référence), puis audite les documen … [3808 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu es relecteur ADVERSE. Tu ne modifies AUCUN fichier : tu produis un rapport de constats, avec citations exactes et num … [4088 caractères tronqués]

*52 appels d'outils.* Actions notables :

- bash — List docs and count lines
- read
- bash — Show git log, status, reports list
- bash — Grep gpt-oss gate values
- bash — Grep numbers/protocol claims in target docs
- bash — Check protocol consts, mode 4 message, format gate
- bash — Inspect format gate script and README
- bash — Inspect routing gate in portes.sh
- bash — Find current format count claims
- bash — Locate readable formats enumeration
- bash — Check format-flux version and density report
- bash — Read sparsity and crossover reports
- bash — Read multi-file reader report
- bash — Read V4.1 execution report and energy figures
- … et 30 autres

**Synthèse produite :**

⏵ Writing the adversarial report with exact citations and minimal corrections.

\# Rapport de relecture adverse — 4 documents

Faits de référence vérifiés dans l'arbre (02/10) : `VERSION_FLUX = 5`, `MODE_LOT_LISTES = 4` (main.rs:1862, 1886) ; refus des modes inconnus après l'en-tête (main.rs:2256-2275) ; lecteur multi-fichiers `Gguf::open_multi` (gguf.rs:447) et métadonnées résolues depuis le shard 1 (`drave …-00001-of-00003.gguf --config` → « deepseek4, 43 couches, 256 experts, 6 par jeton ») ; MLA à rang faible faite, validation arrêtée à la position 2 (rapport-mla-experts.md §7) ; 48 `#[test]` ; 18 formats lisibles (README.md:352), 17 à la porte (README.md:364) ; 4 routages (tools/portes.sh:88-91) ; gpt-oss = 128 experts **top-4** (`--config`) ; porte gpt-oss **15,6017** (rapport-routage-experts.md:66) ; 1 046 tenseurs / 365,70 Go (run `--tensors` : 62,7 ms), types réels F32 493, Q8_0 321, F16 110, IQ2_XXS 80, Q2_K 40, **I8 2** — aucun I32.

| fichier:ligne | citation exacte (≤ 25 mots) | problème | correction minimale proposée (texte de remplacement exact) | gravité |
|---|---|---|---|---|
| docs/plan-deepseek-v4-flash.md:13 | `**non** — aucun GGUF publié` | Faux : `DeepSeek-V4.1-Flash-Q2.gguf` (365 713 686 528 o) existe et est mesuré (rapport-execution-v41.md ; plan41 §3.1) | `**oui** — GGUF Q2 communautaire (365,71 Go), incomplet (`output_hc_*` absents) : voir `plan-deepseek41-complet.md` §3.2` | élevée |
| docs/plan-deepseek-v4-flash.md:32 | `est le lien entre les deux — les métadonnées d'un fichier, les tenseurs de trois —` | Décrit comme manquant ce qui est fait : `--config` sur le shard 1 lit l'architecture, le tokenizer et les 1 328 tenseurs (rapport-lecteur-multifichiers.md ; vérifié) | `est fait : `Gguf::open_multi` résout les métadonnées et les tenseurs des trois shards (`reports/rapport-lecteur-multifichiers.md`) —` | élevée |
| docs/plan-deepseek-v4-flash.md:40 | `**lecteur multi-fichiers** : ouvrir les N shards, résoudre un nom de tenseur dans` | La suite « C'est le premier chantier » (l.42) est périmée : fait le 01/10 (gguf.rs:447, rapport-lecteur-multifichiers.md) | `**lecteur multi-fichiers** : **fait** (`Gguf::open_multi`, `reports/rapport-lecteur-multifichiers.md`) — ouvrir les N shards, résoudre un nom de tenseur dans` | moyenne |
| docs/plan-deepseek-v4-flash.md:63 | `| 1 | lecteur GGUF **multi-shards** | les 3 shards ouverts, un tenseur résolu depuis le shard 2, le placement total affiché |` | Étape 1 du plan déjà satisfaite (3 shar
… [10522 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** List docs and count lines
- **T1** Show git log, status, reports list
- **T1** Grep gpt-oss gate values
- **T1** Grep numbers/protocol claims in target docs
- **T1** Check protocol consts, mode 4 message, format gate
- **T1** Inspect format gate script and README
- **T1** Inspect routing gate in portes.sh
- **T1** Find current format count claims
- **T1** Locate readable formats enumeration
- **T1** Check format-flux version and density report
- **T1** Read sparsity and crossover reports
- **T1** Read multi-file reader report
- **T1** Read V4.1 execution report and energy figures
- **T1** Check deepseek4 support and banc-mla flag
- **T1** Check multi-file open and V4-Flash mentions
- **T1** Read mode-4 measured report
- **T1** Verify spiking-doc numbers and tools
- **T1** Check TAILLE_TETE asserts and test counts
- **T1** Inspect format gate script and README claims
- **T1** Grep IQ, MLA, shard mentions in target docs
- **T1** Verify V4-Flash reference numbers and trace size
- **T1** Check V4.1 Q2 provenance facts
- **T1** Search repo for V4-Flash reference numbers
- **T1** List root docs and read REPRISE head
- **T1** Grep MLA validation wording
- **T1** Check gpt-oss top-k expert configuration
- **T1** Check expert configurations in README
- **T1** Check binary and gpt-oss model presence
- **T1** Run drave --config on gpt-oss
- **T1** Check spiking doc framing and energy report
- **T1** Check I32 support and trace size figures
- **T1** Search journal and read trace report section
- **T1** Find v2 trace size documentation
- **T1** Run config on V4-Flash shard 1
- **T1** Check config on Qwen and V4.1 file presence
- **T1** Print exact cited lines
- **T1** List V4.1 tensors and count types
- **T1** Count tensor types in V4.1 GGUF
- **T1** Compare V4.1 copies tensor types
- **T1** Locate architecture check message
- … et 3 autres

## 4. Mesures et résultats marquants

- **T1** `acc3498 L'écart naît APRÈS la couche 0 : 1,9 % / 1,3 % / 3,8 % / 4,0 % aux positions 0-3`
- **T1** `./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:3663:=== perplexité 15.1757 sur 510 tokens (0 événements, 98.0 s) ===`
- **T1** `./journal/sessions/bbd6969f-0f70-42b2-8951-64d1f2f36d2e/digest.md:5619:=== perplexité 15.1757 sur 510 tokens (0 événements, 97.3 s) ===`
- **T1** `25:| la version change ? | **oui, 4 → 5** | dans `recevoir_flux`, un mode inconnu n'est refusé qu'APRÈS la lecture de `n × 4` octets (repli `_ => {}` puis `autre => Err`) : un pair v4 lirait `4·t` oct`
- **T1** `17:| **listes d'activation** | `(indice, valeur)` par vecteur, encodage DRVF v1/v2/v3 ; v2 = **3 octets par neurone actif** | trace dense 512 jetons : 66,4 Mo, rejeu **identique** (19,3885) |`
- **T1** `README.md:364:tools/portes_formats.sh                   # 17 formats × 2 blocs, contre libggml`
- **T1** `364:tools/portes_formats.sh                   # 17 formats × 2 blocs, contre libggml`
- **T1** `route "GLM-5.3 : sigmoïde ×2,5" "$M/GLM-5.3-UD-IQ1_S/GLM-5.3-UD-IQ1_S-00001-of-00006.gguf" "sigmoïde"`
- **T1** `route "Kimi-K2.7 : sigmoïde ×2,827" "$M/Kimi-K2.7-Code-UD-IQ1_M/Kimi-K2.7-Code-UD-IQ1_M-00001-of-00008.gguf" "sigmoïde"`
- **T1** `drave-core/src/gguf.rs:256:/// IQ3_XXS : 98 octets par super-bloc de 256 poids (30 % des poids de Kimi,`
- **T1** `drave-core/src/gguf.rs:259:/// IQ1_S : 50 octets par super-bloc de 256 poids (42 à 45 % des poids de GLM).`
- **T1** `128:f32 dense (3,5 ko par jeton) ; le lot en LISTES est le mode 4 (1,5 ko par jeton,`
- **T1** `152:Le mode dense coûte **3 663 octets par flux** (79 d'en-tête + 896 × 4) pour`
- **T1** `TurboSparse (≈ 90 % de creux) est *entraîné* ainsi, précisément parce`
- **T1** `| opérateurs creux par neurone | chemin par **listes d'événements** (`SparseVec`, push) | bascule push/pull mesurée à **22 % de densité** (`seuil_push = 0.22`) |`
- **T1** `| déport GPU | matrices entières, seuil de rentabilité mesuré (8 Mo) | granularité **grossière** : pas de placement par neurone |`
- **T1** `5 % du maximum du vecteur : chez eux, zéro est exact (ReLU), chez nous le SiLU`
- **T1** `quantifiée non nulle » laissait passer 100 % des neurones à 16 bits`
- **T1** `(mesuré : densité de 51 104 %).`
- **T1** `| densité d'activation (seuil 5 % du max) | **17,9 %** des neurones par jeton (82 % ne font rien) |`
- **T1** `| magnitude portée par les 1 / 10 / 50 % de neurones les plus lourds | 12,3 % / **33,1 %** / 74,2 % |`
- **T1** `| neurones tirés **> 90 %** du temps | **0,08 %** |`
- **T1** `| neurones tirés > 50 % du temps | 2,82 % |`
- **T1** `| dispersion entre couches | 173 à 1 579 tirs par jeton (×9) ; part des 10 % les plus lourds : 16,7 à 51,1 % |`
- **T1** `**Lecture** : la localité existe (82 % des neurones sont inactifs par jeton) mais`
- **T1** `minuscule (0,08 %). Un préchargement figé à la PowerInfer ne couvrirait donc`
- **T1** `Modèle minimal (MLP 32→64→10), accuracy float **76.07 %**, ternaire (non élagué) **49.71 %**.`
- **T1** `- poids non nuls : **26.3 %** (densité d = 0.263)`
- **T1** `- activations non nulles après ReLU : **52.8 %**`
- **T1** `- événements réels (poids ∧ activation) : **13.9 %**`
- **T1** `| Encodage | Coût | À d = 50 % | À d = 25 % |`
- **T1** `| 100.0 % | 26.3 % | 49.71 % | 2.00 | 1.26 | 4.48 | 8.69 | ×1.58 |`
- **T1** `| 75.0 % | 19.8 % | 49.41 % | 2.00 | 1.20 | 3.36 | 6.52 | ×1.67 |`
- **T1** `| 50.0 % | 13.2 % | 45.31 % | 2.00 | 1.13 | 2.24 | 4.35 | ×1.77 |`
- **T1** `| 25.0 % | 6.6 % | 52.93 % | 2.00 | 1.07 | 1.12 | 2.17 | ×1.88 |`
- **T1** `| 12.5 % | 3.3 % | 50.00 % | 2.00 | 1.03 | 0.56 | 1.08 | ×1.94 |`
- **T1** `| 6.2 % | 1.6 % | 50.49 % | 2.00 | 1.02 | 0.28 | 0.54 | ×1.97 |`
- **T1** `| 3.1 % | 0.9 % | 47.66 % | 2.00 | 1.01 | 0.15 | 0.28 | ×1.98 |`
- **T1** `| 2:4 struct. | 24.0 % | 48.73 % | 2,00 | 1.24 | — | — | ×1.61 |`
- **T1** `| bitmap vs dense2 | 100.0 % | bitmap |`
- **T1** `| csr32 vs dense2 | 6.1 % | csr32 |`
- **T1** `| csr16 vs dense2 | 11.8 % | csr16 |`
- **T1** `| csr32 vs bitmap | 3.1 % | csr32 |`
- **T1** `| csr16 vs bitmap | 6.2 % | csr16 |`
- **T1** `| 100.0 % | 5.5 | 5.5 | 0.6 | 0.3 | 7.4 |`
- **T1** `| 26.3 % | 5.5 | 8.7 | 2.5 | 1.3 | 7.4 |`
- **T1** `| 50.0 % | 5.5 | 7.4 | 1.3 | 0.7 | 7.4 |`
- **T1** `| 25.0 % | 5.5 | 8.8 | 2.6 | 1.3 | 7.4 |`
- **T1** `| 12.5 % | 5.5 | 9.8 | 5.2 | 2.7 | 7.4 |`
- **T1** `| 6.2 % | 5.5 | 10.4 | 10.4 | 5.4 | 7.4 |`
- **T1** `1. **Oui, un modèle ternaire est déjà creux** — ici 26.3 % de non-nuls, sans aucun élagage. C'est le point de départ, pas une contrainte ajoutée.`
- **T1** `3. **Le CSR, lui, est disqualifié** : rentable seulement sous 6 % (indice 32 b) ou 12 % (indice 16 b) de densité — un régime que les LLM n'atteignent pas sans s'effondrer.`
- **T1** `4. **Le vrai obstacle n'est pas le poids, c'est l'activation** : un événement n'existe que si le poids *et* l'activation sont non nuls (ici 13.9 % d'événements réels). Récupérer l'activation à un inde`
- **T1** `5. **Recommandation** : garder le dense 2 bits comme chemin nominal (simple, déterministe, déjà validé) et ajouter un **encodage bitmap + signe** là où la densité est faible. Le saut de blocs entièrem`
- **T1** `- La courbe précision ↔ élagage est **bruitée** : le modèle ne pèse que 2688 poids et son accuracy ternaire (49.7 %) laisse peu de marge de mesure. Les variations observées (±4 pt) sont dans le bruit `
- **T1** `- La densité naturelle (26.3 %) est propre à ce modèle. Un modèle **entraîné** en ternaire (BitNet b1.58) tourne plutôt autour de 50-70 % de non-nuls : le gain du bitmap y serait de ×1,2 à ×1,4, pas ×`
- **T1** `- La littérature (SparseGPT, Wanda) situe l'élagage non structuré *one-shot* des LLM à 50-60 % sans réentraînement, et le 2:4 structuré (50 %) est la forme matériellement supportée. **Au-delà de ~90 %`
- **T1** `43:➡️ **Les deux architectures se croisent à ~22 % de densité d'activation**, pas à`
- **T1** `44:10 %. Le chiffre se lit dans le rapport à pleine densité : le pull traite 4,7 fois`
- **T1** `54:| LLM dense entraîné (notre Qwen2.5-0.5B) | **100 %** (0,00 % de zéros) | ❌ pull gagne ×4,7 |`
- **T1** `96:| 200 | 22 % | 0 év — 9,6 s | 18,1 G év — 8,7 s (bascule) |`
- **T1** `100:➡️ La bascule tombe exactement au seuil mesuré (22 %), et le gain croît à mesure`
- **T1** `101:que la densité baisse — ×1,47 à 5 % de densité. Le choix n'est plus une`
- **T1** `106:1. **Sur CPU, le mode pull est le bon choix** au-dessus de 22 % de densité. Le`
- **T1** `| temps de lecture des en-têtes | 54 ms (disque au repos) |`
- **T1** `| en-têtes seuls (`--tensors`) | mmap, aucune copie | 1 046 tenseurs, **365,70 Go** lus en **63,8 ms** |`
- **T1** `| configuration (`--config`) | en-tête seul | **74 ms** au total, aucune donnée lue |`
- **T1** `| sonde engram (`--sonder-engram 10000`) | mmap, 16 lecteurs | table 1 : 10 000 entrées en **524 ms** (2,6 Mo touchés sur 101,4 Go) · table 2 : **219 ms** · RSS max **120 Mo** pour 365,7 Go adressés |`
- **T1** `| passe avant (`--ppl`) | `DRAVE_PRELIRE_TOUT=1 DRAVE_GPU=1` | **refusée en 0,33 s**, RSS 47 Mo |`
- **T1** `mmap sans copie (365,7 Go adressés, 120 Mo résidents), parallélisme des lecteurs`
- **T1** `moteur refuse donc, et le refuse en 74 ms.`
- **T1** `drave $V --config                       # 74 ms : routage, dimensions, ce qui manque`
- **T1** `drave $V --sonder-engram 10000          # 203 Go de tables adressées, 5 Mo touchés`
- **T1** `46:| CPU (16 threads) | **5,3 G évts/s** mesuré | ~57 nJ |`
- **T1** `47:| FPGA (1 carte, 51 voies) | 4,83 G évts/s *projeté* (limite DDR3) | **~8,3 nJ** |`
- **T1** `48:| GPU (dispersion) | **18,1 G évts/s** mesuré | ~12,7 nJ |`
- **T1** `reports/rapport-architecture-memoire.md:373:| DeepSeek-V4-Flash (3 shards) | 86,90 Go | 0,07 s | 35 Mo |`
- **T1** `au lieu de f32 dense — 1,5 ko par jeton contre 3,5 — au prix d'une quantification`
- **T1** `| **mode 4, lots de 16** | **1,5 ko** (contre 3,5 en lot dense) | **3,03e-2** |`
- **T1** `total ne pas l'être — un pair annonçait 268 Mo par état sur 74 898 états`
- **T1** `franchit les 256 Mo, en le disant :`
- **T1** `plafond de 256 Mo` — 258 Mo envoyés en 1,4 s, aucun octet de trop décodé ;`
- **T1** `lots de 16, elle annonçait 0,9 ko par jeton pour 1,45 réels ;`
- **T1** `reports/rapport-cpu-aer.md:49:3. **Une carte FPGA ≈ ce CPU** (23 contre 22 tok/s) : le CPU a`
- **T1** `reports/rapport-inference.md:18:généré  : 38 tokens en 3.86 s  (9.85 tok/s)`
- **T1** `reports/rapport-inference.md:81:| **Débit de génération** | **10,5 tok/s** (int16) · 10,6 (int8) · **11,4 en dense** |`
- **T1** `reports/rapport-inference.md:97:soit 7,6 tok/s. **Le moteur d'événements est 38 % plus rapide que numpy+BLAS** — sans`
- **T1** `reports/rapport-inference.md:116:(8,5 tok/s) parce que sa boucle de produit scalaire était limitée par une chaîne`
- **T1** `reports/rapport-inference.md:118:11,4 tok/s. La comparaison ci-dessus est celle de deux implémentations soignées.*`
- **T1** `reports/rapport-inference.md:219:identiques. Le débit par événement passe de 3,6 à **5,3 G év/s**.`
- **T1** `reports/rapport-inference.md:234:14,8 tok/s le moteur d'événements est maintenant **plus rapide que le noyau dense`
- **T1** `reports/rapport-inference.md:235:int8** (11,4 tok/s) sur la même machine.`
- **T1** `reports/rapport-inference.md:248:| Événements par token | 352,7 M | 312,5 M | −12 % |`
- **T1** `reports/rapport-inference.md:250:| Débit | 10,33 tok/s | 11,78 tok/s | +14 % |`
- **T1** `reports/rapport-inference.md:271:| 100 % | 352,7 M | 10,33 | 3,56 G év/s |`
- **T1** `reports/rapport-inference.md:285:| élagage à 25 % | événements | matvec | tok/s |`
- **T1** `reports/rapport-attention-creuse.md:5:l'exécution, et son coût croît **linéairement avec le contexte** (2,0 ms à 64`
- **T1** `reports/rapport-attention-creuse.md:6:tokens, 12,7 ms à 512, ~200 ms extrapolé à 8 192).`
- **T1** `**Sans multiplieur** : décalages + additions donnent le résultat exact en 112,3 ms`
- **T1** `contre 2,5 ms pour i8×i8 (×44,9 sur CPU) — mais **sur FPGA le multiplieur n'existe`
- **T1** `> un débit surestimé à 7,53 G év/s), un `&mut` dans la boucle chaude (barrière`
- **T1** `> d'aliasing : 3,09 → 0,97 G év/s), et la **sursouscription** de l'attente active`
- **T1** `> (39+1 threads sur 40 CPU : effondrement ×2,4 — et le `yield_now()` censé le`
- **T1** `tools/portes_formats.sh                   # 17 formats × 2 blocs, contre libggml`
- **T1** `| Qwen2.5-0.5B | Q4_0 | 21,01 | 39 tok/s | 0,41 Go |`
- **T1** `27:| shard 1 (5,3 Mo) | ✅ l'**architecture** (`--plan` : « deepseek4, 43 couches, 256 experts (top-6) ») et le **tokenizer** : 129 280 jetons, aller-retour texte→jetons→texte **identique** sur `data/w`
- **T1** `docs/plan-deepseek41-complet.md:17:| **listes d'activation** | `(indice, valeur)` par vecteur, encodage DRVF v1/v2/v3 ; v2 = **3 octets par neurone actif** | trace dense 512 jetons : 66,4 Mo, rejeu **`
- **T1** `> du pilote, et `--gpu-banc` retrouve l'exactitude des noyaux — 1,6 ms par ligne`
- **T1** `> en warp-par-ligne contre 7,2 ms sur 30 fils CPU, **écart max 1,99e-7**.`
- **T1** `README.md:373:| **Qwen3-30B-A3B** (MoE 128 experts, top-8) | Q4_K_M | **7,61** | 5,4 tok/s | **17,7 Go** |`
- **T1** `373:| **Qwen3-30B-A3B** (MoE 128 experts, top-8) | Q4_K_M | **7,61** | 5,4 tok/s | **17,7 Go** |`
- **T1** `| CPU (16 threads) | **5,3 G évts/s** mesuré | ~57 nJ |`
- **T1** `| FPGA (1 carte, 51 voies) | 4,83 G évts/s *projeté* (limite DDR3) | **~8,3 nJ** |`
- **T1** `| GPU (dispersion) | **18,1 G évts/s** mesuré | ~12,7 nJ |`
- **T1** `| FPGA | 1 événement/cycle/voie, **0,86 mesuré** avec le lecteur ; optimum à 32 PE pour le banc seul (177 MHz) |`
- **T1** `| GPU | 18,1 G évts/s de dispersion, 380 Go/s de lecture |`
- **T1** `même machine. Il reste 2,8× de marge avant la limite mémoire (10,4 Go/s utilisés`
- **T1** `Une carte = 4,83 G évts/s = **un CPU 20 cœurs**, pour 41 % de la logique et 41 %`
- **T1** `elle est **38× plus lente** sur les mêmes données, parce que sa DDR3 fait 9,66 Go/s`
- **T1** `contre 380 Go/s.`
- … (tronqué)

## 5. Erreurs rencontrées

3 sorties en erreur ou divergentes. Les premières :

- **T1** : === VERSION_FLUX / MODE === 1862:const VERSION_FLUX: u8 = 5; 1879:const MODE_LOT: u8 = 3; 1886:const MODE_LOT_LISTES: u8 = 4; 2216:    let tete = tete_flux(MODE_LOT_LISTES, debut, fin, pos0, t, 0.0, S
- **T1** : 74:# 6. Convention de routage annoncée : elle doit correspondre à ce que le GGUF 79:    v=$($D "$2" --config 2>/dev/null | grep -oE "routage +: .*" | head -1)     case "$v" in         *"$3"*) printf "
- **T1** : === docs/plan-mode4-lot-listes.md === === docs/plan-deepseek-v4-flash.md === 4:disque mécanique (`/home/stephane/Data13TB/stephane/modeles/gguf/DeepSeek-V4-Flash-UD-IQ1_M/`, 5:3 shards, 86,9 Go). Le N

