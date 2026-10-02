# V4.1 : la chaîne mHC **retardée**, et les trois égalités vérifiées sur le vrai modèle

**En une ligne** : les deux manques que le moteur annonçait pour DeepSeek-V4.1
(« réduction finale non spécifiée », « compression de ratio 2 sans référence »)
étaient **faux tous les deux** — la référence d'exécution existe (vLLM), elle dit
que V4.1 n'a **pas de tête apprise** et que ses coefficients se **retardent d'un
raccord** — et cette chaîne est maintenant implémentée, exécutée sur le fichier
de 365,7 Go, et vérifiée par trois égalités recalculées hors du moteur.

## 1. Ce que le moteur disait, et pourquoi c'était faux

Message de refus, tel qu'il sortait du binaire (mesuré le 02/10 à 17:33) :

```
architecture « deepseek41 » non implémentée par ce moteur :
  compression de ratio 2 (V4.1) : sans référence d'exécution — le support amont
  de V4.1 n'existe pas encore (llama.cpp n'accepte que 0, 4 et 128) ·
  réduction des copies avant la norme finale : V4.1 ne déclare pas `output_hc_*`
  (c'est son jeu de tenseurs) et aucun moteur ne spécifie ce cas.
```

Les deux affirmations sont réfutées par les sources, pas par un raisonnement :

| ce qui était dit | ce que dit la source |
|---|---|
| « sans référence d'exécution » | vLLM porte `vllm/models/deepseek_v41/compressor.py` (`DeepseekCompressor`, ratios **1 et 2**) et le noyau `fused_save_compress_norm` : softmax **par canal** sur le groupe (`tl.softmax(score, 0)`), norme RMS du latent, RoPE à la position du premier jeton du groupe ; ratio 1 = aucune porte, aucun groupe, aucun `ape` |
| « aucun moteur ne spécifie ce cas » | `vllm/models/deepseek_v41/nvidia/model.py:1009-1014` : `hc_collapse_triton(hidden_states, pre_mix)` puis `self.norm`, avec le commentaire « Collapse the hc copies with the pre-mix from the last layer's FFN mixes — the mix the reference applies via `last_layer.hc_pre(h, pre_mix)` (**v4.1 has no learned hc_head**) » |

Leçon, la même qu'au tour précédent : **« je n'ai pas trouvé » n'est pas « ça
n'existe pas »**. Le refus était honnête dans sa forme (il nommait le manque) et
faux dans son contenu — et un refus faux coûte plus cher qu'un refus muet, parce
qu'il décourage la recherche.

## 2. La chaîne de V4.1, en trois phrases

1. **Le post d'abord** : `mhc_shifted_post_pre` applique le `post` du raccord
   précédent, *puis* appelle la pré-retardée sur le flux **post-mappé**
   (`vllm/models/deepseek_v41/nvidia/ops/mhc.py:256-280` : `residual =
   mhc_post_tilelang(...)` puis `mhc_pre_delayed_overlap(residual, ...)` avec
   `x=None`, donc les mélanges sont calculés sur le flux post-mappé).
2. **Les coefficients se retardent d'un raccord** : « The reference collapses
   each sublayer's input with the *previous* sublayer's pre-mix: attention uses
   the pre-mix carried in (identity for the first layer), the FFN uses this
   layer's attention pre-mix ». Au tout premier raccord, `pre_mix is None` →
   la référence prend **`residual[:, 0]`**, la copie 0, sans mélange
   (`kernels/mhc/torch.py`, `mhc_pre_delayed_torch`).
3. **Pas de tête apprise** : le flux final est replié avec la `pre` de la
   **dernière FFN** (celle qui a été calculée sur le flux d'avant son `post`),
   puis `output_norm`. C'est le seul repliement que le fichier permet : le jeu de
   tenseurs `deepseek41` ne contient aucun `output_hc_*`.

V4 (`deepseek4`, V4-Flash) ne fait **pas** ça : chaque raccord s'y replie avec
ses propres coefficients — c'est la chaîne validée à 1e-7 contre llama.cpp
(`reports/rapport-v4-couches-0-1.md`). Deux architectures, deux chaînes, un seul
drapeau pour les distinguer (`general.architecture`), et le moteur **annonce**
laquelle il applique.

## 3. Ce qui a été implémenté

| pièce | où | ce que ça change |
|---|---|---|
| `hc_retarde` (détecté sur `general.architecture == "deepseek41"`) | `model.rs` (champ + chargement) | choisit la chaîne ; annoncé au chargement |
| coefficients portés d'un raccord au suivant | `forward` (attn puis FFN) | `melanger(&x, &hc_porte)` au lieu de `&s.pre` ; `hc_porte = sf.pre` après la FFN |
| tête non apprise | `forward` (fin) | repliement par `hc_porte` + `output_norm` |
| refus si le flux ne peut pas porter la `pre` | `forward` (nœud qui reprend à `couche_debut > 0`), `norme_finale` | un nœud de grappe replierait avec la copie 0 : faux et muet |
| `--tete-partielle` | `main.rs` | applique la tête à la fin d'une plage `--couches`, sinon une plage partielle rend le flux brut et la tête ne voit jamais le jour |
| dumps `hc_ffn_in`, `hc_ffn_pre`, `hidden_final` | `vider_couche` | de quoi recalculer la chaîne hors du moteur |

Trois bugs de configuration ont été trouvés **par** cette exécution — chacun
rendait le modèle faux en silence, et aucun n'était visible dans un inventaire :

| symptôme | cause | correctif |
|---|---|---|
| `tenseur blk.0.ffn_gate.weight absent` | `n_expert` relu en GGUF-seul (`expert_count`) alors que V4.1 ne déclare que `n_routed_experts` ; `routage_du_gguf` lisait déjà correctement les trois sources, mais **le résultat était jeté** (variables mortes) | `Cfg` prend les valeurs de `routage_du_gguf` |
| toutes les normes décalées d'environ 1e-6 | `rms_norm_eps` (JSON, **1e-20**) au lieu de `attention.layer_norm_rms_epsilon` (absent) → repli sur 1e-6 | `reel_gguf([... , "rms_norm_eps"], …)` |
| « le modèle ne déclare pas YaRN » | V4.1 déclare YaRN dans le **JSON** (`rope_scaling`, facteur 16), pas en clef GGUF | troisième source lue, et message qui dit ce qui est appliqué |

## 4. La vérification, sur le fichier de 365,7 Go

Commande (couches 0 et 1 : les seules en ratio 0, donc sans compression) :

```
DRAVE_DUMP_COUCHES=/tmp/dump_v41 ./drave-core/target/release/drave \
    /home/stephane/FastNVMe/modeles-lourds/DeepSeek-V4.1-Flash-Q2.gguf \
    --couches 0:1 --tete-partielle --ppl /tmp/v41_texte.txt.ids --ctx 8 --limit 4
```

`tools/verifier_v41_mhc.py` relit les vides et recalcule **en numpy**, depuis les
tenseurs du GGUF, les trois étapes — sans passer par le code Rust :

| position (jeton) | ① copie 0 = embarquement | ② les 24 mélanges | ③ la tête | dynamique |
|---|---|---|---|---|
| 0 (201) | **0,000e+00** | 8,354e-08 | 6,753e-07 | 3,113 |
| 1 (438) | **0,000e+00** | 8,210e-08 | 4,031e-07 | 2,939 |
| 2 (10498) | **0,000e+00** | 4,327e-08 | 4,696e-07 | 1,167 |
| 3 (102771) | **0,000e+00** | 8,594e-08 | 2,273e-07 | 1,178 |

- ① est **exact** : au premier raccord, le flux replié *est* la copie 0, au bit
  près. La chaîne de V4 donnerait `(Σ pre)·embarquement` — un vecteur différent,
  donc ce zéro est un discriminant, pas une tautologie.
- ② et ③ sont à ~1e-7 sur une dynamique de 1 à 3 : l'arrondi f32 (le moteur
  calcule en f32, le vérificateur en f64).

**Verdict : les trois égalités tiennent.** Et la chaîne écrite à l'envers n'est
pas une variante cosmétique : sur le témoin synthétique
(`tools/mhc_v41_synthetique.py`), la tête retardée diffère de **67 %** de la tête
directe. C'est aussi ce que fixe le test unitaire
`model::tests_hc::chaine_retardee_v41` (témoins générés par ce script).

Ce que cette vérification **ne** dit pas : que les couches 0 et 1 produisent les
mêmes nombres qu'un runtime de référence. Aucun runtime public ne charge ce
fichier (llama.cpp n'a qu'un patch de conversion), donc la comparaison externe
n'existe pas encore — c'est une vérification **interne**, de bout en bout, de la
chaîne mHC. Les logits publiés ci-dessus appartiennent à un modèle **tronqué**
(1 couche sur 40) : ils ne disent rien de sa qualité.

## 5. Ce qui reste, nommé

L'inventaire de V4.1 (1 046 tenseurs, 40 couches) donne la liste exacte :

| manque | ce que dit le fichier | pourquoi ce n'est pas fait |
|---|---|---|
| **cache compressé partagé** | `kv_source_layer_ids = [2,8,14,20]`, `compress_ratios = [0,0,2×18,1×20]` | « Compressors and compressed-KV caches live only on `kv_source_layer_ids`; consumers reuse the most recently published source below them » : les couches 3..7 lisent les clés publiées par la 2, 21..39 celles de la 20. Un compresseur par couche donnerait d'AUTRES clés |
| ratios 1 et 2 | `attn_compressor_kv` sans `ape`, `attn_compressor_gate` seulement en ratio 2 | le calcul est spécifié (vLLM) ; il n'est pas écrit ici, et le brancher sans le partage ci-dessus serait faux |
| indexeur sans compresseur propre | `indexer.attn_k` [128,512], `indexer.k_norm` [128], `indexer.attn_q_b`, `indexer.proj` | les clés de l'indexeur viennent du **latent du compresseur principal** (le fichier n'a pas d'`indexer_compressor_*`), et il partage le cache de son `kv_source` |
| sélection à deux niveaux | `candidate_source_layer_id = 20`, `candidate_topk_blocks = 2048`, `candidate_block_size = 8` | aucune source d'exécution lue à ce jour |
| **engram** | couches 1 et 14 : `engram_embd` (101 Go), `engram_kv` [25600,6144], `engram_q_norm`/`k_norm` [4,5120] | l'adressage et la lecture sont portés et validés ; **l'injection n'est branchée sur aucune passe avant** |
| **pré-mix sur le fil** | — | la chaîne retardée a besoin de `hc` valeurs par jeton que le protocole DRVF ne transporte pas (16 octets/jeton) : un découpage de V4.1 est refusé |
| YaRN toujours actif | `rope_scaling.factor = 16`, `original_max_position_embeddings = 65536` | le moteur ne l'applique qu'au-delà de 4 × la longueur déclarée (mesure gpt-oss) ; `DRAVE_YARN=1` l'applique partout, comme la référence — le message du chargement le dit désormais |
| DSpark / MTP | `num_nextn_predict_layers = 3`, `dspark_*` | tête spéculative, hors du chemin d'un modèle autorégressif simple |

Détail cosmétique connu : la ligne `[config] … ffn 2816 …` lit
`intermediate_size` dans le premier bloc JSON qui le contient — pour V4.1 c'est
celui de `vision_config` (2816) et non le texte (2304). Le champ est **inerte**
sur un modèle à experts (la largeur du FFN partagé vient de la forme du tenseur),
mais le chiffre affiché est faux.

## 6. Reproduire

```bash
# la chaîne, témoins numpy ↔ moteur
python3 tools/mhc_v41_synthetique.py          # témoins (test Rust)
(cd drave-core && cargo test --release chaine_retardee_v41)

# la vérification sur le vrai modèle
DRAVE_DUMP_COUCHES=/tmp/dump_v41 ./drave-core/target/release/drave \
    /home/stephane/FastNVMe/modeles-lourds/DeepSeek-V4.1-Flash-Q2.gguf \
    --couches 0:1 --tete-partielle --ppl /tmp/v41_texte.txt.ids --ctx 8 --limit 4
python3 tools/verifier_v41_mhc.py \
    /home/stephane/FastNVMe/modeles-lourds/DeepSeek-V4.1-Flash-Q2.gguf \
    /tmp/dump_v41 /tmp/v41_texte.txt.ids
```

## 7. Sources

- vLLM, `vllm/models/deepseek_v41/nvidia/model.py` (`mhc_shifted_post_pre`,
  `hc_collapse_triton`, `_collapse`, `kv_source_layer_ids`) —
  <https://github.com/vllm-project/vllm/blob/main/vllm/models/deepseek_v41/nvidia/model.py>
- vLLM, `vllm/model_executor/kernels/mhc/torch.py` et `cpu.py` (références
  « eager » des blocs mHC) —
  <https://github.com/vllm-project/vllm/blob/main/vllm/model_executor/kernels/mhc/torch.py>
- vLLM, `vllm/models/deepseek_v41/compressor.py` et
  `vllm/models/deepseek_v41/common/ops/fused_compress_quant_cache.py` (ratios 1
  et 2, softmax par canal, RoPE de groupe) —
  <https://github.com/vllm-project/vllm/blob/main/vllm/models/deepseek_v41/compressor.py>
- vLLM, `vllm/models/deepseek_v41/attention.py` (topologie « sparse-attention » :
  sources de KV et d'indexeur, candidats) —
  <https://github.com/vllm-project/vllm/blob/main/vllm/models/deepseek_v41/attention.py>
- vLLM, `vllm/model_executor/kernels/mhc/triton.py` (`hc_collapse_triton`,
  moyenne des copies pour les états auxiliaires) —
  <https://github.com/vllm-project/vllm/blob/main/vllm/model_executor/kernels/mhc/triton.py>
