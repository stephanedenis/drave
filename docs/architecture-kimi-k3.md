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

### La cadence hybride, vérifiée SUR LE FICHIER

Les 16 premières couches (7 shards déjà téléchargés) le confirment :

| couches | type | tenseurs |
|---|---|---|
| **3, 7, 11, 15** (`il % 4 == 3`) | **MLA** | 9 tenseurs `attn_*`, **aucun** `ssm_*` |
| toutes les autres | **KDA** | 10 tenseurs `ssm_*` + 4 `attn_*` |
| **toutes** | — | **2** `res_score` (`attn_res_score`, `ffn_res_score`) |
| couche 0 | **dense** | **0** tenseur `*_exps` (`leading_dense_block_count = 1`) |

Le fichier encode la règle dans `attention.head_count_kv`, qui vaut **1 sur les
couches 3, 7, 11…** et **0 ailleurs** : une couche « récurrente » n'a pas de tête
KV. (Le `config.json` publie la même liste en **base 1** : `full_attn_layers =
[4, 8, 12, …]` — le décalage d'un cran est une source d'erreur classique.)
La règle d'implémentation est donc : `est_mla(il) = head_count_kv[il] > 0`.

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

**MLA (détail des projections, pour l'implémentation)** — lu dans la référence,
c'est du MLA à absorption, très proche du nôtre (V4/V4.1) :

```
Q  = wq_b( rms_norm( wq_a(x), attn_q_a_norm ) )        # 7168 → 1536 → 96×192
kv = wkv_a_mqa(x)                                      # 7168 → 512 + 64
kv_cmpr = rms_norm( kv[:512], attn_kv_a_norm )         # le latent
k_pe    = kv[512:576]                                  # 64 canaux… SANS RoPE
q_nope  = wk_b( q[:128] )  (absorbé dans le latent)    # 128 → 512 par tête
Q = concat(q_nope_absorbé, q_pe)   # 576 par tête  ✓ key_length 576
K = concat(kv_cmpr, k_pe)          # 576
V = kv_cmpr                        # 512 latent
sortie = attn_gate(x_normé) ⊗ wv_b(attn) puis wo       # value_length_mla 128
```

`mla_use_nope` est **vérifié à la conversion** : la partie `pe` est portée et
concaténée, mais **aucune rotation n'est appliquée**. La porte de sortie lit
l'entrée de couche **normalisée** (`inp_gate = cur` avant la première projection).

**MoE latent — l'ORDRE exact** (lu dans `build_latent_moe`, et l'ordre est ce qui
se rate) :

```
routed_in = ffn_routed_down · cur          # 7168 → 3584
logits    = ffn_gate_inp · cur             # 896, sur la PLEINE largeur (identity)
moe_out   = Σ_{16 experts} w_e · ffn_down_exps[e] · situ(gate_exps[e]·routed_in,
                                                          up_exps[e]·routed_in)
moe_out   = rms_norm(moe_out, ffn_routed_norm)   # ← dans le LATENT, avant la remontée
moe_out   = ffn_routed_up · moe_out              # 3584 → 7168
partagé   = ffn_down_shexp · situ(gate_shexp·cur, up_shexp·cur)   # 6144 de large
sortie    = moe_out + partagé
```

Trois pièges : le routeur note la **pleine largeur** pendant que les experts
consomment le latent ; la **norme est dans le latent**, *avant* la remontée
(l'inverse donnerait des valeurs plausibles) ; la porte `exp_probs_b` sert à la
**sélection**, pas aux poids (la question a déjà coûté un défaut sur gpt-oss).

**MoE latent** — les experts travaillent dans un **latent de 3 584** (et non
7 168) : `ffn_routed_down` (7168→3584), les 896 experts (`gate/up/down`, 3 072 de
largeur, **MXFP4**), `ffn_routed_up` (3584→7168), normalisation `ffn_routed_norm`,
plus 2 experts partagés en 7 168. Routage : 896 experts, **16 par jeton**, un seul
groupe, gating fonction 2, poids normalisés. **Le routeur note l'entrée PLEINE
largeur** (`cur`) pendant que les experts consomment le latent — un détail qui
change le résultat si on le rate.

**Et un dernier `res_mix` après la couche 92** (`output_res_score`) : la pile de
points de contrôle est mélangée **une fois de plus** avant la normalisation
finale et la tête. La pile ne sert donc pas qu'aux couches : elle alimente la
sortie.

**SiTU (activation)** : `situ(g,u) = 4·tanh(g/4)·sigmoid(g) · 25·tanh(u/25)`.

## 4bis. Le KDA : la pièce la plus lourde, et comment on la vérifiera

`build_kda_layer` s'appuie sur `llm_build_delta_net_base`, qui porte **trois
chemins** de la même récurrence : `build_delta_net_chunking` (préremplissage
parallèle), `build_delta_net_autoregressive` (un jeton) et `build_delta_net_fused`.
Les trois doivent donner le **même** résultat — c'est en soi un point de
vérification, et pas le plus facile.

Ce que la référence nomme, et qui sera nos points de comparaison (les `cb(...)`) :
`q_in`, `k_in`, `v_in`, `b_in`, `g_in`, `dnet_add_ar_state`, puis la sortie
`kda_*` de la couche (`kda_q_conv`, `kda_k_conv`, `kda_v_conv`, `kda_g1`,
`kda_beta`). Une implémentation qui « a l'air de tourner » mais dont le `g1` ou le
`beta` diffère ne se voit **pas** dans les logits à court terme : on compare donc
ces tenseurs **avant** de regarder la perplexité, comme on l'a fait pour V4.

**Ce qui est déjà implémenté et testé (sans poids)** : la **porte de décroissance**
(`kda_porte` : `g = −5·σ(exp(A_log)·z)` ; le fichier stocke **`−exp(A_log)`** dans
`ssm_a` — se tromper de signe donne une porte positive, donc un état qui *croît*),
la **convolution courte** (`kda_conv_silu` : noyau 4 causal, état canal-majeur
`etat[k + 3·canal]` — les poids, eux, ont le noyau contigu — puis SiLU), et la
**récurrence** (`kda_pas`, vérifiée contre NumPy). Le chemin par blocs reste à
faire.

Le contrat de la couche, tel que la référence le montre :
`q,k,v` = convolutions courtes (noyau 4) sur les projections, `q,k` normalisés en
L2, `beta = sigmoïde(W_beta·x)` par tête, porte de décroissance `g` bornée à
**−5** (variante K3 — la variante Kimi-Linear utilise `−exp(A_log)·softplus(…)`,
et confondre les deux donne des scores plausibles et faux), puis la récurrence
delta avec un état **par tête** (`head_dim × head_dim`), et enfin la porte `ssm_g`
et la norme `ssm_o_norm` en sortie.

## 4ter. Comment l'implémenter dans le moteur (notes d'exécution)

- **Poids empruntés, jamais recopiés** : les projections Q8_0 passent par
  `DenseQ8::emprunter_q8(ptr, n_out, n_in, nb)` (`g.data_ptr(nom)`), les F32 par
  une tranche. Recopier les 1,5 To en f32 est hors de question (et inutile : le
  moteur emprunte déjà les blocs de V4/V4.1).
- **Activations** : `dot_q8_source(o, x: &[i32])` attend une activation
  **quantifiée** — c'est le motif du moteur (quantifier une fois, puis sommer).
- **État du KDA** par couche : convolution `3 × 12288` f32 (147 Ko) et delta
  `96 × 128 × 128` f32 (**6,3 Mo**) — pour 93 couches, ~590 Mo : acceptable.
- **Ordre de la couche 0**, tel que la référence le déroule :
  1. `x = embd[token]` ; `cur = rms_norm(x, attn_norm)` ;
  2. KDA : `q/k/v = W·cur` → convolution 4 + SiLU → L2-norm par tête →
     `g = kda_porte(f_b(f_a(cur)) + dt_bias, ssm_a, −5)` ; `beta = σ(W_beta·cur)` ;
     récurrence (`kda_pas`) ; `normed = rms_norm(o, ssm_norm)` ;
     `gated = normed · σ(W_g·cur)` ; `out = attn_output · gated` ;
  3. **le flux REDÉMARRE** (`il % 12 == 0`) : `prefix = out` (et non `x + out`) ;
  4. `cur = res_mix(prefix, ffn_res_score)` (la pile contient déjà `x`, empilé
     AVANT l'attention) ;
  5. `cur = rms_norm(cur, ffn_norm)` ; FFN dense : `situ(W_gate·cur, W_up·cur)`
     puis `W_down · h` ;
  6. `prefix += cur` → `l_out`.
- **La pile de points de contrôle** se transporte : c'est le nouveau flux de
  coupure (≤ 8 × 7 168 f32 = 229 Ko par jeton), à mesurer comme les copies `hc`
  de V4 l'ont été.

## 4quater. Croisement avec le code PUBLIÉ (et ce qu'il confirme)

Les maths ci-dessus venaient de `llama.cpp-k3`. Elles ont été **recroisées avec le
code de Moonshot** (`modeling_kimi_linear.py`, `configuration_kimi_k3.py`, dans le
dépôt officiel) — un contrôle indépendant de notre transcription :

| pièce | code publié | notre implémentation |
|---|---|---|
| SiTU | `SituAndMul` : `beta·tanh(gate/beta)·sigmoid(gate) · up`, et `up = linear_beta·tanh(up/linear_beta)` si `linear_beta` est fixé | **identique** (`situ`) |
| attention résiduelle | `_apply_attn_res` : `v = cat(block_residual, prefix_sum)`, `k = v·rsqrt(mean(v²)+eps)`, `scores = (k·score_weight).sum(-1)`, `probs = softmax`, `sortie = probs @ v` (les **brutes**) | **identique** (`res_mix`), y compris le détail « scores sur les normalisées, somme sur les brutes » |
| projections du KDA | `q/k_proj → head_dim×num_k_heads` (128×96), `v_proj → head_dim×num_heads`, `f_a → head_dim`, `f_b → projection`, `dt_bias`, `b_proj → num_heads`, `g_proj` **plein rang** (`use_full_rank_gate`), `o_norm = RMSNormGated(…, activation='sigmoid')` | **correspondance nom par nom** avec `attn_q/k/v`, `ssm_f_a/f_b`, `ssm_dt`, `ssm_beta`, `ssm_g`, `ssm_norm` |
| convolution courte | `ShortConvolution(kernel_size=4, activation='silu')` sur q, k et v | **identique** (`kda_conv_silu`) |
| porte bornée | `safe_gate=True`, `lower_bound=-5`, `use_beta_sigmoid_in_kernel=True` | **identique** (`kda_porte`) |

**Ce que le code publié ne donne PAS** : la récurrence elle-même. Elle est dans des
noyaux externes (`chunk_kda`, `fused_recurrent_kda`) qui ne sont pas livrés avec le
modèle. La seule implémentation lisible est donc celle de `llama.cpp` — et c'est
celle qui a été transcrite puis **vérifiée contre une référence NumPy en f64**
(`kda_pas`, état *et* sortie). Le croisement avec le code publié porte donc sur les
**formes et les sémantiques**, pas sur l'algèbre de la récurrence : c'est écrit.

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

Mesuré : **≈ 87 Go de poids par jeton** — attention **48,7** (dense, lue en
entier), experts routés **24,7** (16 sur 896), partagés **12,4**, tête 1,3 — soit
**5,8 % du modèle** (`reports/rapport-budget-kimi-k3.md`). Planchers : disque dur
**435 s/jeton**, NVMe **43 s**, PCIe x8 **13 s**, RAM **4,4 s**. La partie
**dense (62 Go)** doit être résidente ; le reste est du routage et de la
réutilisation. Aucune de ces valeurs n'est « locale » au sens
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
