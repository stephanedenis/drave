# Vérifier Kimi-K3, étage par étage — le protocole

> Écrit le 03/10 (bloc 30) **avant** d'écrire l'architecture, pour que chaque
> morceau de code ait son point de comparaison le jour où il naît. La règle du
> dépôt est constante : on compare les **tenseurs intermédiaires avant** de
> regarder la perplexité, parce qu'une implémentation qui « a l'air de tourner »
> peut avoir une porte de travers sans que ça se voie dans les logits à court
> terme (l'épisode de la porte bornée de V4.1 et celui du clamp SwiGLU sont là
> pour le rappeler).

## 1. Les deux côtés de la comparaison

| côté | commande | ce qu'elle écrit |
|---|---|---|
| **référence** (llama.cpp `kimi-k3`) | `REF_DUMP=/tmp/refk3 ./tools/ref_logits_k3 <K3.gguf> <ids> <sortie> <n>` | `<préfixe>-<nom>-<couche>.bin`, en-tête `REFD` + `ndim` + `ne[4]`, f32 dans l'ordre ggml (une colonne par position) |
| **moteur** | `DRAVE_DUMP_COUCHES=/tmp/notrek3 ./drave-core/target/release/drave <K3.gguf> --ppl <ids> …` | `<préfixe>-<nom>-<couche>-<position>.bin`, f32 brut |
| **comparaison** | `python3 tools/compare_etats.py /tmp/notrek3 /tmp/refk3 <nom> <couche> <positions>` | écart max et relatif sur le **vecteur entier** |

Les deux outils existent déjà : `ref_logits_k3` a été lié contre `llama.cpp-k3`
(03/10), et `compare_etats.py` a servi pour V4 (`hc_attn_pre` concorde à **1e-7**).

## 2. Les points de comparaison, dans l'ordre où il faut les atteindre

Les noms sont ceux des `cb(...)` de la référence — **notre moteur doit écrire les
mêmes**, sinon la comparaison n'a pas lieu d'être.

| # | nom (référence) | ce que ça vérifie | si ça diverge, la faute est dans… |
|---|---|---|---|
| 1 | `inp_embd` | embarquement du jeton | déquantification de `token_embd` (Q8_0 emprunté) ou rangée mal indexée |
| 2 | `attn_norm` | RMSNorm d'entrée | epsilon, ordre des opérations |
| 3 | `kda_q_conv`, `kda_k_conv`, `kda_v_conv` | projections + **convolution courte** (noyau 4) + SiLU | disposition de l'état de convolution (**canal-majeur**), ordre du noyau, SiLU |
| 4 | `kda_g1` | **porte de décroissance** bornée | signe de `exp(A_log)` (le fichier stocke `−exp(A_log)`), `dt_bias`, borne −5 |
| 5 | `kda_beta` | pas appris, sigmoïde, **par tête** | projection `ssm_beta`, forme |
| 6 | `kda_normed`, `kda_out` | normalisation L2 de q/k puis **récurrence delta** | conventions `i` = clé / `j` = valeur, état par tête |
| 7 | `mla_out`, `mla_gated` | MLA (absorption) + **porte de sortie** | `q_lora_rank`, absence de RoPE (`nope`), porte lue sur l'entrée **normalisée** |
| 8 | `res_probs` | **attention résiduelle** : softmax sur les points de contrôle + le courant | scores sur les valeurs **normalisées**, somme sur les **brutes**, pile append-only |
| 9 | `prefix_sum_attn` | **redémarrage du flux** aux couches « banque » (toutes les 12) | la couche banque remplace le flux au lieu de s'y ajouter |
| 10 | `ffn_norm`, `ffn_out` (dense, couche 0) | **SiTU** | la formule, `linear_beta ≤ 0` désactivant la branche `up` |
| 11 | `ffn_moe_logits`, `ffn_shexp`, `ffn_moe_out` | routage (sigmoïde, 896 experts, 16 par jeton) + **MoE latent** | routeur noté sur la **pleine largeur**, experts sur le latent, normalisation des poids |
| 12 | `l_out` | la couche entière | — |
| 13 | `result_norm`, `result_output` | le `res_mix` final + la tête | oubli du dernier `res_mix` (`output_res_score`) |

## 3. Le premier jalon qui compte : la couche 0

La couche 0 est **dense** (`leading_dense_block_count = 1`) : elle exerce
l'embarquement, la RMSNorm, le **KDA complet**, l'attention résiduelle (avec une
pile vide au premier raccord), **SiTU** et le FFN dense — mais **pas** le MoE, ni
la cadence MLA. C'est donc le jalon le plus riche par unité de travail, et il se
vérifie sur **4 positions** en quelques minutes.

Ensuite : la couche 1 (MoE latent), la couche 3 (MLA), la couche 12 (premier
**redémarrage** du flux résiduel), puis les 93 couches.

## 4. Les tolérances, et ce qu'elles veulent dire

- **1e-7 à 1e-6** : même calcul, ordre d'accumulation différent. C'est ce que
  donnait `hc_attn_pre` pour V4 contre llama.cpp.
- **1e-4 à 1e-3** : quantifications différentes (nos activations 16 bits contre
  bf16/f32 côté ggml). Acceptable **si** l'écart ne croît pas avec la position.
- **> 1e-2, ou une croissance avec la position** : une erreur de structure, pas
  d'arrondi. On ne passe pas à l'étage suivant.

## 5. Ce qui est déjà vérifié sans poids (et le restera)

| pièce | état |
|---|---|
| tokenizer | **identifiants identiques** au tokenizer officiel (11 textes, `tools/porte-tokenizer-kimi.sh`) |
| métadonnées et cadence | 93 couches, MLA aux couches 3/7/11/15, 2 `res_score` partout, couche 0 dense — **lus dans le fichier** |
| `res_mix` (attention résiduelle) | implémenté, testé (scores normalisés / somme brute) |
| SiTU | implémenté, testé (dont `linear_beta ≤ 0`) |
| KDA : récurrence | implémenté, testé contre NumPy f64 (état **et** sortie) |
| KDA : porte bornée | implémenté, testé (toujours dans (−5, 0) → l'état décroît) |
| KDA : convolution courte | implémenté, testé (état canal-majeur, noyau contigu) |
| **le reste** | à écrire, chaque étage avec son point de comparaison ci-dessus |
