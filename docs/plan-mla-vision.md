# Plan : MLA et vision (chantier 5)

Ces deux-là ne sont pas « à moitié faits » : ils ne sont pas commencés, et ce
document dit exactement par quoi commencer, pour qu'une session suivante n'ait
pas à refaire l'enquête. Rien ici n'est mesuré — c'est une feuille de route, et
elle est marquée comme telle.

## 1. MLA (attention latente, DeepSeek-V2/V3)

### Pourquoi ce n'est pas testable en l'état

Aucun modèle MLA en GGUF sur cette machine : le `deepseek-r1-distill-14b` local
est un **Qwen dense**, pas un DeepSeek-V2. La seule voie honnête est donc un
**modèle synthétique** : des poids aléatoires mais de forme correcte, écrits en
GGUF par un script, et une **référence indépendante** (numpy) qui refait le même
calcul pour comparer les logits.

### Ce que MLA change (et pourquoi ça vaut le détour)

Le cache KV n'est plus `(n_kv, ctx, head_dim)` mais **une seule tête latente par
couche** : `kv_lora_rank + qk_rope_dim` valeurs par jeton (512 + 64 = 576 chez
DeepSeek-V3, contre 2 × 128 × 128 = 32 768 pour une attention à 128 têtes). Le
cache est donc ~50 × plus petit — c'est le seul levier structurel du plan 1 M, et
il rend le KV int4 inutile.

### Tenseurs et clés (convention llama.cpp / GGUF)

| tenseur | forme | rôle |
|---|---|---|
| `blk.N.attn_q_a.weight` | `[hidden, q_lora_rank]` | descente de Q |
| `blk.N.attn_q_a_norm.weight` | `[q_lora_rank]` | RMSNorm après la descente |
| `blk.N.attn_q_b.weight` | `[q_lora_rank, n_head × (qk_nope + qk_rope)]` | remontée de Q |
| `blk.N.attn_kv_a_mqa.weight` | `[hidden, kv_lora_rank + qk_rope]` | descente KV (MQA) |
| `blk.N.attn_kv_a_norm.weight` | `[kv_lora_rank]` | RMSNorm sur la partie latente |
| `blk.N.attn_kv_b.weight` | `[kv_lora_rank, n_head × (qk_nope + v_dim)]` | remontée K/V |
| `blk.N.attn_output.weight` | `[n_head × v_dim, hidden]` | sortie |

Clés de configuration : `attention.q_lora_rank`, `attention.kv_lora_rank`,
`attention.key_length` (= qk_nope + qk_rope), `attention.value_length`,
`rope.dimension_count` (= qk_rope seulement : la rotation ne porte QUE sur la
partie « rope », le reste de Q/K est **non tourné**, c'est le « decoupled RoPE »).

### Le calcul, dans l'ordre

1. `q = W_q_b · norm(W_q_a · h)` → découpé en `q_nope` (non tourné) et `q_rope` ;
2. `kv = W_kv_a · h` → `c_kv` (latent, `kv_lora_rank`) et `k_rope` (tourné) ;
3. `k_nope`, `v = W_kv_b · norm(c_kv)` ;
4. scores = `q_nope·k_nope + q_rope·k_rope` (la seconde partie seulement a subi la
   rotation), puis softmax et `Σ p·v`, comme partout ;
5. **cache** : on ne stocke QUE `c_kv` et `k_rope` par jeton — `k_nope` et `v`
   sont reconstruits à la lecture par `W_kv_b`, une fois par couche et par jeton
   (matrice `[512, n_head × 192]`, soit ~1 Mo en Q8 : le coût est réel mais petit
   devant le cache économisé).

### Validation proposée

1. script Python qui écrit un GGUF MLA minuscule (2 couches, hidden 256, 4 têtes,
   `q_lora_rank` 64, `kv_lora_rank` 128, `qk_rope` 32, tête liée) ;
2. référence numpy du même calcul, même ordre d'opérations ;
3. le moteur charge ce GGUF, on compare les logits : l'écart attendu est celui du
   reste du moteur (~1e-5 relatif) ;
4. contrôle négatif : en mettant `W_kv_b = I` et `kv_lora_rank = n_head × 192`, on
   doit retrouver une attention MQA ordinaire — le moteur doit donner les MÊMES
   logits qu'un modèle MQA équivalent construit à la main.

Ce dernier point est le vrai test : il relie l'implémentation nouvelle à une
implémentation déjà validée par les portes de non-régression.

## 2. Vision (Qwen2.5-VL)

### Ce qui est déjà là

`/home/stephane/FastNVMe/models/mmproj-Qwen2.5-VL-7B-Instruct-f16.gguf` (le
projecteur) et `Qwen2.5-VL-7B-Instruct-Q4_K_M.gguf` (le modèle). Rien ne lit les
patchs.

### Ce qu'il faut écrire, dans l'ordre

1. **pré-traitement** : redimensionnement (le ViT de Qwen2.5-VL accepte des
   images à résolution native, découpées en patchs de 14 px), normalisation
   CLIP, et **fusion 2 × 2 des patchs** avant le projecteur ;
2. **tour ViT** : charger `v.blk.N.*` du `mmproj` (attention + MLP + LayerNorm,
   fenêtre locale sur une partie des couches), produire les `image_embd` ;
3. **injection** : remplacer les jetons `<|image_pad|>` par ces embeddings dans le
   flux d'entrée — le moteur sait déjà injecter des vecteurs ? Non : `forward`
   part toujours de `token_embd`. C'est le point d'architecture à ajouter
   (`forward_vecteur(&[f32])`) ;
4. **validation** : le harnais `tools/ref_logits` s'appuie sur llama.cpp ; si sa
   version locale sait charger un `mmproj` (`llama-mtmd-cli`), la comparaison des
   logits sur une image fixe est la référence. Sinon, contrôle de bon sens : le
   modèle doit décrire une image simple (un carré rouge) mieux que le hasard, et
   les embeddings d'image doivent avoir une norme du même ordre que ceux de
   `token_embd`.

### Ordre de grandeur

C'est le plus gros morceau du dépôt : une tour ViT complète, un chemin
d'injection d'embeddings, et une chaîne de pré-traitement d'image. À mener APRÈS
MLA, dont le chemin d'injection (`c_kv`) est plus simple et dont le gain
(cache ÷50) est mesurable sur le plan 1 M.
