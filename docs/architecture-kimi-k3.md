# Architecture Kimi-K3 — spécification tirée de la référence

> Écrite le 03/10 (bloc 28) pour préparer l'exécution locale du premier modèle de
> la classe « trop gros pour le local » (1 508,7 Go en Q4). **Tout ce qui suit
> vient de deux sources vérifiables** : les métadonnées du GGUF (lues avec
> `tools/lire_meta_gguf.py`) et le code de la référence exécutable
> (`llama.cpp-k3/src/models/kimi-k3.cpp`, amont `ggml-org/llama.cpp`, plus le code
> publié par Moonshot : `modeling_kimi_k3.py`, `configuration_kimi_k3.py`).
> Rien n'est déduit de mémoire.

## 1. Ce que déclare le fichier (mesuré)

| clé GGUF | valeur | sens |
|---|---|---|
| `general.architecture` | **`kimi-k3`** | notre moteur ne la connaît pas |
| `block_count` | **93** | 93 couches |
| `embedding_length` | 7 168 | largeur du flux |
| `feed_forward_length` | 33 792 | FFN dense (couche 0) |
| `leading_dense_block_count` | **1** | seule la couche 0 est dense |
| `attention.head_count` | 96 | |
| `attention.key_length` / `value_length` | 576 / 74 | forme « linéaire » |
| `attention.key_length_mla` / `value_length_mla` | 192 / 128 | forme MLA |
| `attention.q_lora_rank` / `kv_lora_rank` | 1 536 / 512 | MLA à rang faible |
| `rope.dimension_count` / `rope.freq_base` | 64 / 10 000 | RoPE partiel |
| `expert_count` / `expert_used_count` | **896 / 16** | MoE |
| `expert_group_used_count` / `expert_gating_func` | 1 / 2 | un seul groupe utilisé |
| `expert_feed_forward_length` | 3 072 | largeur d'un expert |
| `expert_latent_length` | **3 584** | **le MoE travaille en latent** |
| `expert_shared_count` | 2 | deux experts partagés |
| `expert_weights_norm` / `expert_weights_scale` | true / 1,0 | normalisation des poids de routage |
| `ssm.conv_kernel` | **4** | convolution courte (Q, K, V) |
| `kda.head_dim` / `kda.gate_lower_bound` | 128 / **−5,0** | attention delta avec porte bornée |
| `activation.situ_beta` / `situ_linear_beta` | 4,0 / 25,0 | activation **SiTU** |
| `attn_res.block_size` | **12** | **attention résiduelle inter-couches** |
| `context_length` | 1 048 576 | 1 M |

### Ce que contiennent les tenseurs (relevé sur le shard 2)

| tenseur | dims | type | rôle |
|---|---|---|---|
| `token_embd.weight`, `output.weight` | [7168, 163840] | Q8_0 | vocabulaire 163 840 |
| `blk.N.attn_q.weight` / `attn_k` / `attn_v` | [7168, 12288] | Q8_0 | couches **KDA** (96 × 128) |
| `blk.N.ssm_g.weight` | [7168, 12288] | Q8_0 | porte de sortie du KDA |
| `blk.N.ssm_*` (conv1d q/k/v, f_a, f_b, beta, a, dt, o_norm) | — | — | mécanique du delta-net |
| `blk.N.ffn_gate/up/down.weight` | [7168, 33792] | Q8_0 | FFN dense (couche 0) |
| `blk.N.ffn_{gate,up,down}_exps.weight` | […, 896] | **MXFP4** | 41,93 Go pour 3 couches |
| `blk.N.ffn_*_shexp.weight` | — | — | 2 experts partagés |
| `blk.N.attn_gate.weight` | — | — | porte de sortie de l'attention (MLA) |
| `blk.N.attn_norm` / `ffn_norm` | [7168] | F32 | RMSNorm |
| `blk.N.attn_res_score` / `ffn_res_score` | [7168] | F32 | **score de l'attention résiduelle** |
| `output_res_score.weight` | [7168] | F32 | idem, au niveau de la tête |

## 2. La boucle d'une couche (d'après la référence)

```
prefix_sum = inpL                       # le flux résiduel
cur = res_mix(prefix_sum, attn_res_score)     # ATTENTION RÉSIDUELLE (voir §3)
banked = (il % 12 == 0)
si banked: res_push(prefix_sum)               # on empile l'état BRUT de la couche
cur = rms_norm(cur, attn_norm)
cur = KDA(cur)   si la couche est récurrente   # 3 couches sur 4
    = MLA(cur)   sinon                         # 1 couche sur 4 (indices 4, 8, 12, …)
prefix_sum = cur si banked sinon prefix_sum + cur   # ← le flux REDÉMARRE sur la couche « banque »
cur = res_mix(prefix_sum, ffn_res_score)
cur = rms_norm(ffn_norm)
cur = FFN dense (couche 0, SiTU)  ou  MoE latent (toutes les autres)
prefix_sum = prefix_sum + cur
```

Deux mécanismes sont **nouveaux pour nous** :

- **le redémarrage du flux résiduel** toutes les 12 couches (`banked`) : à ces
  couches, `prefix_sum` ne s'additionne pas, il **repart de la sortie
  d'attention** — les 12 couches précédentes vivent alors dans la pile de
  points de contrôle ;
- **l'attention résiduelle** (§3) qui, à chaque sous-couche, mélange par softmax
  la pile des points de contrôle et le flux courant.

## 3. L'attention résiduelle (`res_mix`) — le mécanisme à ne pas rater

Pour un état `x` et un vecteur de score `w` (par couche, `attn_res_score` ou
`ffn_res_score`), avec la pile `src` de `n_ckpt` points de contrôle :

```
score(ckpt) = somme_canaux( rms_norm(ckpt) * w )        # un score par point de contrôle
score(cur)  = somme_canaux( rms_norm(cur)  * w )
p           = softmax( [score(ckpt_1..k), score(cur)] )  # sur les k+1 candidats
sortie      = Σ_i p_i · ckpt_i  +  p_cur · cur           # la SOMME utilise les valeurs BRUTES
```

Deux détails qui décident de la fidélité : les scores sont calculés sur les
valeurs **normalisées**, mais la somme pondérée utilise les valeurs **brutes** ;
et la couche 0 n'a rien à mélanger (la pile est vide). La pile est
**append-only** (on empile, on ne replie pas) : elle contient au plus
`⌈93/12⌉ = 8` états de 7 168 valeurs — soit **8 × 7 168 × 4 = 229 Ko** par jeton
si on la transporte en f32 d'un nœud à l'autre. *C'est le nouveau « flux de
coupure » à mesurer, comme les copies `hc` l'étaient pour V4.*

## 4. Les couches

**KDA (Kimi Delta Attention, 3 couches sur 4)** — attention linéaire à porte :
`q,k,v = conv1d_4(W_q·x, W_k·x, W_v·x)` ; `q,k = L2_norm(q,k)` ; `beta = sigmoid(W_beta·x)`
(par tête) ; la porte de décroissance suit la variante K3 (le fichier stocke
`-exp(A_log)`) :

```
g = gate_lower_bound · sigmoid( -(-ssm_a) · (f_b(f_a(x)) + dt_bias) )      # borne −5,0
```

puis la récurrence delta-net avec l'état par tête (`head_dim × head_dim`), la
porte `ssm_g` et la normalisation `ssm_o_norm` en sortie.

**MLA (1 couche sur 4)** — attention latente **sans RoPE appris** (`mla_use_nope`) :
`q_lora_rank 1536`, `kv_lora_rank 512`, tête 192 (nope) + 64 (rope), valeur 128,
porte de sortie `attn_gate`. C'est la même famille que les MLA de V4/V4.1, dont
nous avons déjà les briques.

**MoE latent** — les experts travaillent dans un **latent de 3 584** (et non
7 168) : `ffn_routed_down` (7168→3584), les 896 experts (`gate/up/down`, 3 072 de
largeur, **MXFP4**), `ffn_routed_up` (3584→7168), normalisation `ffn_routed_norm`,
plus 2 experts partagés en 7 168. Routage : 896 experts, **16 par jeton**, un seul
groupe, gating fonction 2, poids normalisés.

**SiTU (activation)** : `situ(g,u) = 4·tanh(g/4)·sigmoid(g) · 25·tanh(u/25)`.

## 5. Ce que notre moteur a déjà, et ce qui manque

| brique | chez nous | état |
|---|---|---|
| MLA à rang faible + tête latente + porte de sortie | V4/V4.1 (`Mla4`) | **acquis**, à adapter aux dims (1 536/512/192/128/64) |
| RoPE partiel, RMSNorm, SwiGLU, softmax | partout | acquis |
| MoE à table de routage, experts empruntés au fichier | V4-Flash (256 experts), V4.1 (384) | acquis, à porter à 896 + latent |
| Formats | Q8_0, MXFP4, Q2_K, IQ* | acquis (MXFP4 déjà emprunté tel quel) |
| **Attention delta-net (KDA)** : conv1d courte, porte bornée, récurrence par tête | — | **neuf** |
| **Attention résiduelle** (pile de points de contrôle + softmax) | — | **neuf** |
| **MoE latent** (down/up autour des experts) | — | **neuf** |
| **SiTU** | — | neuf (une fonction) |
| **Redémarrage du flux résiduel** toutes les 12 couches | — | neuf (une ligne, mais structurante) |

## 6. Comment on vérifiera (les portes, dès le premier jour)

La différence avec V4.1 est décisive : **la référence exécutable existe**
(`llama.cpp-k3`, construit le 03/10, `src/models/kimi-k3.cpp`). La porte de
correction est donc possible, étage par étage, et elle se mène comme pour V4 :

1. `tools/ref_logits` **reconstruit contre `llama.cpp-k3`** → logits et
   perplexité de référence ;
2. comparaison **tenseur par tenseur** (les `cb(...)` de la référence nomment
   exactement les points de contrôle : `inp_embd`, `attn_norm`, `kda_q_conv`,
   `kda_g1`, `kda_beta`, `res_probs`, `ffn_norm`, `ffn_out`, `l_out`…) ;
3. la porte Drave ensuite : trace de routage des 896 experts (réutilisation entre
   jetons), découpage en grappes, flux du point de coupure — dont la **pile de
   points de contrôle**, qui est le nouveau flux à transporter.

## 7. Le coût, et pourquoi c'est LE sujet

Mesuré : **≈ 35 Go de poids par jeton** (16 experts sur 896 × 93 couches, MXFP4),
soit **2,3 % du modèle**. Planchers : disque dur **173 s/jeton**, NVMe **17 s**,
PCIe x8 **5,4 s**, RAM **1,7 s**. Aucune de ces valeurs n'est « locale » au sens
ordinaire : le modèle ne tient pas, il ne se cache pas, et **il faut donc ne lire
que ce qui sert**. Les trois leviers mesurables, dans l'ordre :

1. **la réutilisation des experts entre jetons** (16 sur 896 par jeton) : c'est
   elle qui décide si un cache paie — le cache RAM d'experts a été mesuré **plus
   lent** sur V4.1, donc la réponse n'est pas acquise ;
2. **le découpage** : chaque nœud ne lit que ses experts (grappes), et transporte
   le flux de coupure — mesuré exact à 0,00e0 sur les modes 0, 1 et 3 ;
3. **le débit de calcul par octet lu** : le CPU est 5 à 7× au-dessus du plancher
   PCIe (noyaux), avec les acquis SIMD/déquantification **bit-exacte** ou
   annoncés.
