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

### ÉTAT : MLA EST FAIT ET VALIDÉ

Le moteur charge un modèle MLA (`attn_kv_a_mqa` reconnu à ses tenseurs, sans
aucune clé de configuration nouvelle — les rangs se lisent dans les FORMES) et
tient le **cache latent** : `c_kv` et `k_rope` par position, `k_nope` et `v`
reconstruits à la lecture par `W_kv_b`. La rotation ne porte que sur la partie
« rope », et le chemin est séparé de `forward` (le modèle du harnais n'a ni
teneurs Q8_0 ni fenêtre glissante).

Mesure : `--banc-mla` écrit les logits des 8 positions, comparés à la référence
numpy indépendante — **écart max relatif 5,2e-7**, soit le bruit de virgule
flottante du moteur. Le témoin imprimé le dit aussi : `MLA : 2 couches · q_lora
32 · kv_lora 48 · qk_nope 16 + qk_rope 16 · v 16 · cache latente 64 valeurs par
jeton (au lieu de 32)`.

Deux erreurs réelles ont été trouvées PAR la référence, et c'est tout l'intérêt
d'un témoin indépendant :

1. dans la référence elle-même, des indices d'`einsum` qui confondaient
   dimension de tête et dimension de clé ;
2. **la convention GGUF des tenseurs linéaires** : un poids est stocké
   (sortie, entrée) et déclaré (entrée, sortie) — s'y tromper multiplie par la
   transposée. L'écart est passé de 0,82 (relatif) à 5,2e-7 après correction.

Reste à faire pour MLA : le contrôle négatif (avec `W_kv_b = I` et
`kv_lora_rank = n_head × (qk_nope + v_dim)`, l'attention latente doit redonner
une MQA ordinaire) — la comparaison numpy le rend moins indispensable, mais il
relierait l'implémentation à une autre DÉJÀ validée par les portes de
non-régression. Et le branchement du cache latent dans le plan 1 M (mesurer le
cache ÷50 sur un vrai modèle MLA, ce qu'on n'a pas ici).

### État du harnais : FAIT

`tools/mla_synthetique.py` fabrique le modèle et la référence numpy :

* GGUF de 381 ko, 26 tenseurs, 15 clés de métadonnées, architecture
  `deepseek2` avec `q_lora_rank` 32, `kv_lora_rank` 48, `qk_rope` 16,
  `qk_nope` 16, `v_dim` 16, 4 têtes, 2 couches, hidden 64 ;
* référence numpy du même calcul (logits pour 8 jetons, forme `(8, 64)`),
  rangée dans `/tmp/mla_ref/` avec `ids.npy` et la description des formes ;
* l'écriture du GGUF a été vérifiée en relisant son en-tête (version 3, 26
  tenseurs, 15 métadonnées).

Ce qui reste : **le chemin MLA dans le moteur** — lire ces tenseurs, tenir le
cache latent (`c_kv` + `k_rope` par position), n'appliquer la rotation qu'à la
partie « rope », et comparer les logits à `logits.npy`.

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
