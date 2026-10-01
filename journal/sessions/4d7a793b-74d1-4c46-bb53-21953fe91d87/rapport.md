# Session 4d7a793b — Tu es relecteur ADVERSARIAL, en

| | |
|---|---|
| Identifiant | `4d7a793b-74d1-4c46-bb53-21953fe91d87` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-09-30 22:59 |
| Durée | 0.3 h |
| Tours | 1 |
| Messages | 43 |
| Appels d'outils | 63 |
| Fichiers touchés | 0 |
| Commandes | 52 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu es relecteur ADVERSARIAL, en mode autonome, dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (moteur d'inférence Rust « Drave »). Ta mission : vérifier que les artefacts produits pendant le sprint 3 (21h49 → 23h49) ne contiennent AUCUN chiffre sans source, aucune affirmation non mesurée, et aucun défaut dans les outils modifiés. Le dépôt a une règle : « chaque chiffre publié doit a … [3148 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu es relecteur ADVERSARIAL, en mode autonome, dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (moteur d'i … [3428 caractères tronqués]

*63 appels d'outils.* Actions notables :

- bash — List reports, tools and tmp sources
- read
- bash — Dump aiguille and compare logs
- bash — Grep main.rs for lot/topk/dense usage
- bash — Inspect models, ids, and old logs
- bash — Rerun dense Qwen logits CPU vs GPU
- bash — Count ids, list tmp txt, grep report figures
- bash — Read main.rs run_infer region
- bash — Find forward_lot callers and ids candidates
- bash — Check which ids file matches gpt-oss log
- bash — Read run_infer prompt/generation loop
- bash — Read generation path of run_infer
- bash — Read GPU topk gating and forward_lot
- bash — Locate generate and its prefill path
- … et 41 autres

**Synthèse produite :**

⏵ Audit terminé : rédaction du verdict final

Aucun fichier du dépôt n'a été modifié. **Attention** : `reports/rapport-aiguille-topk.md` a changé pendant l'audit (77 lignes à 22:55 → 83 lignes à 23:00:49, md5 `8c04d547…`). J'audite la version courante ; l'ancienne version (celle du commit `6ad2bc6`) affirmait « `--infer` ignore `--lot` » — c'était **faux**, et la version courante le corrige exactement (§ lignes 22-32). Les écarts ci-dessous portent sur la version courante.

---

\# Écarts, un par un

\## 1. « même top-1 partout » — FAUX
- **(a)** `reports/rapport-logits-gpu-vs-cpu.md:5-6` (résumé) et `:77` (usage).
- **(b)** « il les décale de 0,038 nat en moyenne — **même top-1 partout** » ; « … **sans changer les jetons choisis en top-1** ».
- **(c)** La mesure du rapport lui-même (`:42`) : **497/511**, 14 positions divergentes. Recalcul indépendant sur `/tmp/logits_cpu.bin` + `/tmp/logits_gpu.bin` + `/tmp/ids_oss_512.txt` : 497/511, positions 126, 186, 207, 261, 284, 287, 343, 358, 368, 414, 443, 452, 492, 497.
- **(d)** **FAUX** (et contradiction interne avec `:45` « 97 % des positions »).
- **(e)** Remplacer par « même top-1 sur 97 % des positions (497/511) ». C'est exactement l'erreur « 511/511 » rejouée dans le résumé, à la fin du sprint qui prétendait l'avoir corrigée.

\## 2. `--attn-topk` n'agit qu'au décodage sous `--lot 256` — portée surestimée
- **(a)** `reports/rapport-aiguille-topk.md:3-12` (méthode + titre) et toute la grille `:36-59`.
- **(b)** « à 4 096 clés, une attention qui ne garde que **256 clés (6 %)** retrouve l'information… » avec `--lot 256`.
- **(c)** Le moteur imprime, dans cette configuration exacte : « `[attention] --attn-topk 256 est IGNORÉ en mode lot (--lot 256) : l'attention par lots est DENSE.` » (repris à l'identique sur la commande `aiguille.py` du rapport). Seuls les **24 jetons générés** (24/4138 = **0,58 %** des passes avant) ont une attention à 256 clés ; le préremplissage de 4114 jetons est dense. `tools/aiguille.py:93-97` ne lit la sortie moteur que si `n_prompt == 0`, donc le message est jeté. Test A/B : `--lot 256` vs `--lot 256 --attn-topk 8` → ids générés différents (le top-k agit bien au décodage) ; `--lot 256 --attn-topk 256` vs `--lot 256` → identiques ici, mais la tâche aiguille est plus fragile.
- **(d)** **IMPRÉCIS** (conclusion valable pour le décodage, mais l'affichage laisse croire que tout le passage était creux — « une valeur affichée qui n'agit qu'à 0,58 % »).
- **(e)** Ajouter à la méthode : « avec 
… [8910 caractères tronqués]

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** List reports, tools and tmp sources
- **T1** Dump aiguille and compare logs
- **T1** Grep main.rs for lot/topk/dense usage
- **T1** Inspect models, ids, and old logs
- **T1** Rerun dense Qwen logits CPU vs GPU
- **T1** Count ids, list tmp txt, grep report figures
- **T1** Read main.rs run_infer region
- **T1** Find forward_lot callers and ids candidates
- **T1** Check which ids file matches gpt-oss log
- **T1** Read run_infer prompt/generation loop
- **T1** Read generation path of run_infer
- **T1** Read GPU topk gating and forward_lot
- **T1** Locate generate and its prefill path
- **T1** Read main.rs forward_lot call sites
- **T1** Read Options defaults and argument parsing
- **T1** Check attn_topk uses, git state, mtimes
- **T1** Empirically test lot and attn-topk in infer
- **T1** Diff the report and find the grid runner
- **T1** Dump the aiguille runner scripts
- **T1** Read digest around forward_lot grep
- **T1** Rerun compare_logits on gpt-oss with real ids
- **T1** Find the 30B 670s source
- **T1** Show gpt-oss compare result
- **T1** Check 8192 launches and topk runner
- **T1** Compute exact stats and bitwise identity
- **T1** Check model metadata and prior sources
- **T1** Inspect topk_gpu_possible conditions
- **T1** Demonstrate compare_logits count divergence
- **T1** Test silent gpu-topk without attn-topk
- **T1** Find sources for kernel exactness and 0.06 percent
- **T1** Trace the 8192 probe stop in the digest
- **T1** Grep reports for e-7 precision figures
- **T1** Read digest around 8192 and the lot claim
- **T1** Gather line numbers and compute rates
- **T1** Check MXFP4 source and sprint doc claim
- **T1** Check report mtime and hash
- **T1** Confirm gpu top-k activation with lot 256
- **T1** A/B/C decode output with and without topk
- **T1** Confirm topk selection is inside forward
- **T1** Check attn window and ids provenance
- … et 12 autres

## 4. Mesures et résultats marquants

- **T1** `reports/rapport-campagne-parcimonie.md:21:| entrée des projections d'attention (90 %) | +0,06 % | ✅ quasi gratuit |`
- **T1** `reports/rapport-coherence-docs-2.md:95:| 36 | `reports/rapport-placement-bits-kv.md:5` | en-tête : « clés f16 … 39 % de la taille f32 pour **+0,06 %** » | le tableau du même rapport (`:21`) donne **+0`
- **T1** `reports/rapport-coherence-docs-2.md:148:2. **Corriger `reports/rapport-placement-bits-kv.md`** : ligne 5, « +0,06 % » →`
- **T1** `reports/rapport-gpu-topk-selection.md:316:   sommation diffère — un effet de 0,06 % à ctx 256 sur le même modèle, donc`
- **T1** `reports/rapport-logits-gpu-vs-cpu.md:62:C'est cohérent avec l'écart de 0,06 % mesuré à `--ctx 256` (deux fenêtres de 255`
- **T1** `reports/rapport-parcimonie-imposee.md:68:| attention seule à 90 % | 350,0 M (−1,2 %) | +0,06 % | — |`
- **T1** `reports/rapport-precision.md:22:| creux 1 bits d=0.125 | 1 | 8.4 % | 1.08 | 60.06 % | 10.2 **◀** |`
- **T1** `reports/rapport-precision.md:47:| 1.08 | creux 1 bits d=0.125 | 60.06 % | 10.2 |`
- **T1** `/// mesure (23 → 159 ms) : sans un banc isolé, on ne sait pas si un changement`
- **T1** `/// fois au lieu de `t` fois (mesuré au noyau : ×2,4 à 16 jetons sur une`
- **T1** `/// matrice 4864 × 896).`
- **T1** `# Mesuré : une sonde coûte ~175 ms par jeton de prompt (le chemin `--infer``
- **T1** `# (clés f16 + valeurs int8 : +0,018 % de perplexité à 8 192 ; int8/int8 : +3,04 %)`
- **T1** `16426:La perplexité ne dit pas si le modèle **retrouve** une information. `tools/aiguille.py` plante un code et vérifie qu'il ressort : 6/6 échecs sur Qwen 0.5B (modèle trop faible) et **9,6 min pour `
- **T1** `15887:KV 32  ctx 8192 : perplexité 14.2339 sur 8191 tokens (0 événements, 863.9 s)`
- **T1** `15894:KV 32  ctx 8192 : perplexité 14.2339 sur 8191 tokens (0 événements, 863.9 s)`
- **T1** `reports/rapport-coherence-docs-2.md:86:| 32 | `docs/format-flux.md:169` | lot : 4×64 → 18,0851 ; 1 lot de 256 → 918 ko, 0,00e0 | conforme à `reports/rapport-prefill-reparti.md:41-42` (917 583 o ≈ 918 `
- **T1** `reports/rapport-coherence-docs.md:93:| 37 | `docs/format-flux.md:142` | « 1 lot de 256 : 0,00e0 (**918 ko** sur le fil) » | 917 583 o ≈ 918 ko (arrondi décimal) | OK |`
- **T1** `reports/rapport-gpu-topk-selection.md:306:| GPU, dense (`DRAVE_GPU_KV`) | 18,3074 | −1,47 % vs CPU |`
- **T1** `reports/rapport-logits-gpu-vs-cpu.md:16:| GPU, miroir KV seul (`DRAVE_GPU_KV`) | 18,3074 | −1,47 % |`
- **T1** `// notation restait donc sur CPU, où elle coûte 968 ms par couche à`
- **T1** `// complet en VRAM — mesuré 3,90 ms pour 14 lignes × 1 M de clés,`
- **T1** `// contre 539,9 ms pour l'attention complète sur CPU.`
- **T1** `// 0,13 contre 0,22 ms à 4 k clés, 0,85 contre 0,89 à 131 k —`
- **T1** `=== ctx256 0,06% context ===`
- **T1** `| CPU, top-k 256 | 19,0740 | **+2,66 %** : le coût du pruning |`
- **T1** `| GPU, dense (`DRAVE_GPU_KV`) | 18,3074 | −1,47 % vs CPU |`
- **T1** `| GPU, top-k 256 (`DRAVE_GPU_TOPK`) | 18,8391 | **+2,90 %** : même coût |`
- **T1** `| GPU sans miroir KV (`DRAVE_GPU` seul) | 18,3538 | −1,22 % vs CPU |`
- **T1** `1. **le coût du pruning est le même des deux côtés** (+2,7 % CPU, +2,9 % GPU) :`
- **T1** `2. **l'écart CPU/GPU de 1,2 à 1,5 % n'est PAS le miroir KV** (−1,22 % avec les`
- **T1** `seules projections déportées, −1,47 % avec le miroir en plus, soit −0,25 % pour`
- **T1** `sommation diffère — un effet de 0,06 % à ctx 256 sur le même modèle, donc`
- **T1** `36132:- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY'\np='/tmp/ceremonie.md'\ns=open(p).read()\n\ns = s.replace(\"\"\"| 7 | **le gain dans le moteur, à `
- **T1** `37110:- **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > /tmp/ceremonie2.md <<'EOF'\n\n**Objectif du sprint** : « Fusionner la chaîne du top-k déporté : descente radi`
- **T1** `reports/rapport-gpu-topk-selection.md:342:| 3 | `attn_topk_somme` : softmax sur les k retenus + puits, puis Σ pondérée des V | ✅ 1,0–4,8e-7 · temps GPU constant (0,07 ms) |`
- **T1** `docs/plan-mla-vision.md:568:| embedding de patchs, projecteur | **validés** contre numpy (5,4e-7 et 1,7e-6, à 28 × 28) |`
- **T1** `REPRISE.md:162:| 7 | noyaux GPU | **fait, quatre formats** | warp par ligne : tête **Q8_0** (1,6 ms contre 7,3 CPU, écart 2e-7), **MXFP4** (0,1 ms, écart **0,00e0** — bit à bit), **Q4_K** (0,5 contre `
- **T1** `REPRISE.md:172:| noyau GPU Q6_K warp (tête liée Qwen 1.5B, 191,4 Mo) | **3,6 ms** contre 8,3 ms CPU 16 fils (23,2 → 53,6 Go/s), écart 3,3e-7 |`
- **T1** `REPRISE.md:173:| noyau GPU Q6_K warp (ffn_down Qwen 1.5B, 11,3 Mo) | **0,3 ms** contre 1,5 ms CPU (×5), écart 7,1e-7 |`
- **T1** `REPRISE.md:407:| 3 · somme | `attn_topk_somme` (softmax sur les k + puits, Σ w·V, indices lus en VRAM) | écart **1,0–4,8e-7** (critère 1e-6) · temps GPU **constant : 0,07 ms** de 4 k à 262 k clés |`
- **T1** `Qwen : perplexité 19.3885 sur 510 tokens`
- **T1** `gpt-oss : perplexité 15.1757 sur 510 tokens`
- **T1** `256/4096 = 6.25 %`
- **T1** `0.5B @4096 : 256.5/4114 = 62.3 ms/jeton ; 238.5/4114=58.0`
- **T1** `1.5B @4096 : 725.1/4114 = 176.3 ms/jeton`
- **T1** `30B @2048 : 667.6/2147 = 310.9 ; 690.5/2147 = 321.6 ms/jeton`
- **T1** `8704 x 175ms = 25.4 min`
- **T1** `8704 x 61ms = 8.8 min`
- **T1** `decode part of forwards: 24/4138 = 0.58 %`
- **T1** `| 7 | noyaux GPU | **fait, quatre formats** | warp par ligne : tête **Q8_0** (1,6 ms contre 7,3 CPU, écart 2e-7), **MXFP4** (0,1 ms, écart **0,00e0** — bit à bit), **Q4_K** (0,5 contre 1,2 ms, 4e-7), `
- **T1** `prompt  : 656 tokens en 20.372 s  (32.2 tok/s, TTFT 31.1 ms)`
- **T1** `// réécrire les boucles ne gagnait rien (mesuré : 12,4 → 12,5 ms).`
- **T1** `perplexité 18.5803 sur 511 tokens`
- **T1** `perplexité 18.3538 sur 511 tokens`
- **T1** `// contexte (0,88 / 1,91 / 3,20 ms à 64 / 128 / 256) — c'est la`

