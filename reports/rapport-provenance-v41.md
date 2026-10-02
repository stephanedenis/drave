# DeepSeek-V4.1 : ce que le fichier dit, et ce qu'il ne dit pas

**En une ligne** : le GGUF de V4.1 est **refusé proprement** par Drave, pour deux
raisons qu'on peut montrer — il **manque les tenseurs du mélange de tête**
(`output_hc_*`) que llama.cpp déclare *requis*, et ses couches compressées sont
en **ratio 2**, un régime que **la référence elle-même n'implémente pas**
(« only supports compression ratios 0, 4, and 128 »).

## 1. Le fichier, tel qu'il est

`DeepSeek-V4.1-Flash-Q2.gguf` (365,71 Go, 1 046 tenseurs, 40 couches). Ses
métadonnées portent le `config.json` d'origine (`deepseek41.config`) :

- `hc_mult: 4`, `hc_sinkhorn_iters: 20`, `hc_eps: 1e-06` — les hyper-connexions
  sont déclarées, et Drave les lit ;
- `compress_ratios` : **[0, 0, 2, 2, …, 2, 1, 1, …, 1, 0, 0, 0]** — 18 couches
  en ratio **2**, 20 en ratio **1**, 5 en ratio 0 (contre 4 et 128 pour
  V4-Flash) ;
- `q_lora_rank: 1280`, `o_groups: 8`, `o_lora_rank: 1024`, `head_dim: 512`,
  `sliding_window: 128`, `index_topk: 512`, `rms_norm_eps: 1e-20`,
  `swiglu_limit: 10.0`, `engram_layer_ids: [1, 14]`, `dspark_*` (décodage
  spéculatif, cibles 37-39).

## 2. Les deux manques, montrés et non supposés

**a) Le mélange de tête n'existe pas dans l'architecture V4.1.** Les trois seuls
tenseurs hors `blk.*` sont `token_embd.weight`, `output_norm.weight`,
`output.weight` : aucun `output_hc_fn/base/scale` — **et c'est conforme** : la
liste des 39 familles de tenseurs `deepseek41` les retire explicitement de la
liste `DEEPSEEK4` (elle retire aussi `FFN_GATE_TID2EID`, `ATTN_KV_NORM`,
`ATTN_COMPRESSOR_APE`, `INDEXER_COMPRESSOR_*` et les six `NEXTN_*`, et ajoute
`ATTN_KV_A_NORM` et les quatre tenseurs d'engram). Ce qui reste ouvert est
ailleurs : **comment les `hc` copies se réduisent avant la norme finale** dans
V4.1, et aucun moteur ne le spécifie — le patch de conversion le dit : le fichier
converti **ne se charge pas encore**.

**b) Le ratio 2 n'a pas de référence.** Une couche compressée de V4.1 porte
`attn_compressor_kv` [512, 5 120] et `attn_compressor_norm` [512], mais **ni
`attn_compressor_gate` ni `attn_compressor_ape`** — les deux tenseurs qui, en
ratio 4 et 128, portent le softmax par canal. llama.cpp refuse explicitement ce
cas :

```cpp
} else if (ratio != 128) {
    throw std::runtime_error("DeepSeek-V4 loader only supports compression ratios 0, 4, and 128");
}
```

L'implémenter sans référence serait **deviner** — exactement ce que le plan
s'interdit. Le moteur le refuse donc en le nommant :

```
calculable : NON — il manque : compression de ratio 2 (V4.1) : ni notre moteur ni
la référence ne l'implémentent (llama.cpp n'accepte que 0, 4 et 128) ; mélange de
tête des hyper-connexions (`output_hc_fn`) absent — fichier incomplet, ou
conversion fautive (question de provenance, P7)
```

## 3. Ce que ça change pour P7

| question du plan | réponse |
|---|---|
| « le GGUF est-il complet ? » | **oui, conformément au jeu de tenseurs `deepseek41`** — qui n'est pas celui de V4. La question de provenance est tranchée : ce n'est pas un défaut de conversion |
| « peut-on valider V4.1 contre llama.cpp ? » | **non**, et pas à cause de Drave : `deepseek41` n'est pas encore en amont (une PR est ouverte, [#28696](https://github.com/ggml-org/llama.cpp/pull/28696)), le chargeur refuse le ratio 2, et le patch de conversion précise que le support d'**exécution** est un travail séparé, non fait |
| « que fait Drave en attendant ? » | il **refuse** à l'ouverture, avec les deux motifs nommés — pas de panique, pas de forward muet |

Ce qui reste faisable **sans** V4.1 tournant :
1. **l'engram** (P8) : `--sonder-engram` lit déjà ses tables (10 000 entrées en
   219-524 ms, 120 Mo de RSS pour 365,7 Go) ;
2. **les couches brutes** de V4.1 (0, 1, 40-42, ratio 0) : exécutables une à une
   avec `DRAVE_ETAT_ENTREE` **si** un état de référence existait — il n'en
   existe pas, faute de moteur de référence ;
3. **la structure** : les 8 couches d'indexeur, les 4 de compresseur, les 2
   d'engram sont inventoriées, et leurs tenseurs sont lisibles.
