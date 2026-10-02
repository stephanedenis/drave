# Session 8734fc13 — Tu es un relecteur ADVERSARIAL

| | |
|---|---|
| Identifiant | `8734fc13-aeb8-4cdf-b005-c182f77be0dc` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-02 18:10 |
| Durée | 0.2 h |
| Tours | 1 |
| Messages | 96 |
| Appels d'outils | 108 |
| Fichiers touchés | 0 |
| Commandes | 74 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu es un relecteur ADVERSARIAL autonome, en lecture seule. Tu ne dois MODIFIER AUCUN fichier (ni édition, ni `git commit`, ni écriture) — ta sortie est un rapport en français, dans ta réponse finale.  Dépôt : /home/stephane/Data13TB/stephane/GitHub/Qtrinet (moteur d'inférence LLM en Rust, `std` seul). Les deux derniers commits (`93cb1b7`, `e4331d4`) portent le travail à attaquer.  ## Ce qui est af … [3838 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu es un relecteur ADVERSARIAL autonome, en lecture seule. Tu ne dois MODIFIER AUCUN fichier (ni édition, ni `git commit … [4118 caractères tronqués]

*108 appels d'outils.* Actions notables :

- bash — Show recent commits and stats
- bash — List repo layout and tools
- read
- bash — Dump model.rs diffs to /tmp
- bash — Find dump sites of hc tensors
- bash — Locate helper functions
- bash — Grep hc_retarde and related fields usage
- bash — Find forward_lot callers and flag assignments
- bash — Show main.rs diff of first commit
- bash — Find ppl mode and tete_partielle calls
- bash — Inspect /tmp dumps
- bash — Read --couches parsing
- bash — Find couches usage in model loading
- bash — Read gguf cfg helpers
- … et 64 autres

**Synthèse produite :**

⏵ Rapport final

\## Cadre et méthode

J'ai attaqué l'état **commité** (HEAD = `e4331d4`), en lisant les deux diffs, `model.rs` (extrait de `git show e4331d4`), les quatre scripts Python, puis en **re-mesurant** sur les vides et le GGUF. J'ai aussi relu la **référence vLLM réelle** (elle existe, accessible) pour tester les affirmations de provenance.

⚠️ **L'arbre de travail a bougé pendant la revue** : implémentation du partage de cache consommateur dans `model.rs` vers 18:17, puis **retour à HEAD** (18:22:13) et reconstruction du binaire (18:22:45). Toutes mes mesures sur binaire utilisent ce binaire 18:22:45, qui correspond à HEAD — prouvé par le fait que `--couches 3:4` y est refusé comme le code HEAD le prescrit, alors que la version 18:18 de l'arbre le laissait tourner. Je cite les lignes de la version **committée** du rapport.

**Verdict : rien de grave dans le moteur.** Aucun calcul faux en silence trouvé sur les chemins vérifiés. Les quatre affirmations tiennent, avec 4 déformations factuelles, 4 trous de couverture et 5 formulations trop fortes.

---

\## FAUX

**F1 — « les couches 0 et 1 tournent »** (rapport §4 l.80 et 85 ; message de commit `93cb1b7`).
La commande est `--couches 0:1` = **[0,1)**, donc une seule couche. Les vides le prouvent : 56 fichiers, tous `-0-` ; le rapport écrit lui-même « (1 couche sur 40) » l.115.
`ls /tmp/dump_v41-* | sed 's/.*-\([0-9]*\)-[0-9]*\.bin/\1/' | sort -u` → `0`. J'ai refait la passe avec le binaire HEAD (`DRAVE_DUMP_COUCHES=/tmp/dump_v41_bis … --couches 0:1 --tete-partielle --ppl /tmp/v41_texte.txt.ids --ctx 8 --limit 4`) : mêmes vides, mêmes chiffres. De toute façon ① ne peut porter que sur la couche 0.

**F2 — « Les 4 couches sources tournent (§5) »** (rapport §6, l.163).
La couche 14 est source (ratio 2) **et** couche engram (`deepseek41.engram.layer_ids = [1,14]`) ; le manque engram n'est retiré que si aucune couche d'engram n'est dans la plage (`model.rs` 2784-2793). Mesuré avec le binaire HEAD :
`… --couches 14:15 --tete-partielle --ppl … --limit 1` → panic « engram (V4.1) : l'injection dans la passe avant n'est pas branchée », EXIT=134. Donc au plus **3** sources chargent, 2 sont vérifiées.

**F3 — « YaRN … la rotation était fausse dès la position 1 »** (message de commit `93cb1b7` ; le tableau §3 du rapport, lui, est juste).
À ctx 8, `cfg.yarn = None` **avant et après** le correctif : le seuil est `ctx > y.3 * 4.0` (`model.rs` 2710-2714) = 262144. Pour les couches ratio 0 (les seules exécutées), vLLM 
… [6663 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** Show recent commits and stats
- **T1** List repo layout and tools
- **T1** Dump model.rs diffs to /tmp
- **T1** Find dump sites of hc tensors
- **T1** Locate helper functions
- **T1** Grep hc_retarde and related fields usage
- **T1** Find forward_lot callers and flag assignments
- **T1** Show main.rs diff of first commit
- **T1** Find ppl mode and tete_partielle calls
- **T1** Inspect /tmp dumps
- **T1** Read --couches parsing
- **T1** Find couches usage in model loading
- **T1** Read gguf cfg helpers
- **T1** Dump GGUF metadata keys of V4.1
- **T1** Print full JSON config of V4.1
- **T1** List heavy models and manifest
- **T1** Find published gates
- **T1** Read portes.sh
- **T1** Check availability of V4-Flash and Qwen models
- **T1** Inspect dense flag semantics
- **T1** Check dense semantics in model.rs
- **T1** Dump V4-Flash metadata
- **T1** Find usages of new fields
- **T1** Check working tree status
- **T1** Show uncommitted model.rs diff
- **T1** Scan metadata of other models
- **T1** List layer 2 and 20 dumps
- **T1** Rerun compressor reference for layer 2
- **T1** Rerun compressor reference for layer 20
- **T1** Rerun mHC verifier on dumps
- **T1** Extract committed model.rs and locate dumps
- **T1** List key V4.1 tensors
- **T1** Find mla4 usages in committed file
- **T1** Check V4-Flash mla marker tensors
- **T1** Inspect forward_lot guards
- **T1** Check lot handling in main
- **T1** Inspect Proj::vide behavior
- **T1** Per-layer tensor family inventory of V4.1
- **T1** Inspect V4-Flash shard 2 tensor names
- **T1** Read Proj::vide and matvec fallback
- … et 34 autres

## 4. Mesures et résultats marquants

- **T1** `Témoins synthétiques : la chaîne écrite à l'envers change la tête de 67 %.`
- **T1** `450:    // différence traverse 48 couches et déplace la porte publiée de 0,03 % —`
- **T1** `1125:/// gpt-oss en a 4 608 (36 couches × 128) — 60 Go, la VRAM n'en tient pas le`
- **T1** `reports/rapport-transport-liste.md:48:(19,3885), mais ici 16 bits coûtent 2,6 % : la différence n'est pas la précision,`
- **T1** `reports/rapport-compacite-trace.md:6:> **identique** (perplexité 19,3885 dans les deux cas), et la relecture par`
- **T1** `reports/rapport-compacite-trace.md:16:> **+0,074 % de perplexité au rejeu** (19,4029 contre 19,3885) et d'une erreur par`
- **T1** `reports/rapport-tete-restreinte.md:93:| 0 | 85,4 % | **19,3885** | référence |`
- **T1** `reports/rapport-routage-experts.md:75:déplacé la porte Qwen3-30B de 799,8557 à 799,8152 (−0,005 %). Cause : la`
- **T1** `reports/rapport-routage-experts.md:136:Qwen2.5-0.5B, **sans YaRN** : 19,3885 contre 18,9750 chez llama.cpp (2,2 %).`
- **T1** `route "GLM-5.3 : sigmoïde ×2,5" "$M/GLM-5.3-UD-IQ1_S/GLM-5.3-UD-IQ1_S-00001-of-00006.gguf" "sigmoïde"`
- **T1** `route "Kimi-K2.7 : sigmoïde ×2,827" "$M/Kimi-K2.7-Code-UD-IQ1_M/Kimi-K2.7-Code-UD-IQ1_M-00001-of-00008.gguf" "sigmoïde"`
- **T1** `1042:        // scalaire dense (pull). Le croisement mesuré est à 22 %`
- **T1** `2128:/// contrôle : jusqu'à ~15 To demandés au noyau. 256 Mo couvrent largement un lot`
- **T1** `2129:/// de 8 192 jetons × 8 192 canaux (268 Mo... soit un lot par fenêtre maximale).`
- **T1** `[config] attention V4 : 40 couches · 1 tête latente de 512 (448 nope + 64 rope) · 64 têtes de requête · sortie groupée 8×1024 · puits par tête`
- **T1** `3 tokens notés — perplexité cumulée 16810711.868  (3.2 tok/s)`
- **T1** `=== perplexité 16810711.8682 sur 3 tokens (0 événements, 0.9 s) ===`
- **T1** `3.2 tok/s effectifs (avant + tête)`
- **T1** `part de l'attention dans le flux total : 15.2 %`
- **T1** `3 tokens notés — perplexité cumulée 4172058.408  (2.9 tok/s)`
- **T1** `=== perplexité 4172058.4080 sur 3 tokens (0 événements, 1.0 s) ===`
- **T1** `2.9 tok/s effectifs (avant + tête)`
- **T1** `part de l'attention dans le flux total : 15.7 %`
- **T1** `21	       3 tokens notés — perplexité cumulée 4172058.408  (2.9 tok/s)`
- **T1** `23	=== perplexité 4172058.4080 sur 3 tokens (0 événements, 1.0 s) ===`
- **T1** `24	    2.9 tok/s effectifs (avant + tête)`
- **T1** `29	    part de l'attention dans le flux total : 15.7 %`
- **T1** `20	       3 tokens notés — perplexité cumulée 31033792.347  (2.7 tok/s)`
- **T1** `22	=== perplexité 31033792.3467 sur 3 tokens (0 événements, 1.1 s) ===`
- **T1** `23	    2.7 tok/s effectifs (avant + tête)`
- **T1** `28	    part de l'attention dans le flux total : 15.4 %`
- **T1** `/// cette machine : CPU 14–25 Go/s, PCIe x8 6,5 Go/s, NVLink 25,78 Go/s,`
- **T1** `/// GPU 380 Go/s en lecture locale.`
- **T1** `GLM-5.3 : sigmoïde ×2,5                  sigmoïde  ✅`
- **T1** `Kimi-K2.7 : sigmoïde ×2,827              sigmoïde  ✅`
- **T1** `3 tokens notés — perplexité cumulée 31033792.347  (2.7 tok/s)`
- **T1** `=== perplexité 31033792.3467 sur 3 tokens (0 événements, 1.1 s) ===`
- **T1** `2.7 tok/s effectifs (avant + tête)`
- **T1** `part de l'attention dans le flux total : 15.4 %`
- **T1** `-| **cache compressé partagé** | `kv_source_layer_ids = [2,8,14,20]`, `compress_ratios = [0,0,2×18,1×20]` | « Compressors and compressed-KV caches live only on `kv_source_layer_ids`; consumers reuse t`
- **T1** `+| **cache compressé partagé** | `kv_source_layer_ids = [2,8,14,20]`, `compress_ratios = [0,0,2×18,1×20]` | **fait** : les sources projettent, les consommatrices lisent leurs tampons (`comp_source`), `
- **T1** `44	| **cache compressé partagé** | `kv_source_layer_ids = [2,8,14,20]`, `compress_ratios = [0,0,2×18,1×20]` | « Compressors and compressed-KV caches live only on `kv_source_layer_ids`; consumers reuse`
- **T1** `163:| **cache compressé partagé** | `kv_source_layer_ids = [2,8,14,20]`, `compress_ratios = [0,0,2×18,1×20]` | « Compressors and compressed-KV caches live only on `kv_source_layer_ids`; consumers reus`

## 5. Erreurs rencontrées

4 sorties en erreur ou divergentes. Les premières :

- **T1** : #!/bin/bash # Les portes du dépôt, en une commande. # # Un chiffre de référence qui dérive sans qu'on s'en aperçoive ne vaut rien : # chaque porte est comparée à la valeur ATTENDUE, et le script sort 
- **T1** : pos 0: mean(replie^2)=1.5488e-03 | eps=1e-20 -> 6.753e-07 | eps=1e-06 -> 1.005e-03 pos 1: mean(replie^2)=2.0449e-03 | eps=1e-20 -> 4.031e-07 | eps=1e-06 -> 7.186e-04 pos 2: mean(replie^2)=1.0041e-02 |
- **T1** : /tmp/v41_texte.txt.ids : 1 tokens, fenêtres de 8 [rope] YaRN déclaré par le JSON `<arch>.config` (`rope_scaling`), pas par une clef GGUF — lu là, et ANNONCÉ [partiel] couches 3..4 : aucune couche d'EN
- **T1** : --- rapport (HEAD) 80:Commande (couches 0 et 1 : les seules en ratio 0, donc sans compression) : 85:    --couches 0:1 --tete-partielle --ppl /tmp/v41_texte.txt.ids --ctx 8 --limit 4 110:Ce que cette v

