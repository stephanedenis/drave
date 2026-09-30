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

### Ce que dit le fichier (relevé, plus deviné)

Le projecteur `mmproj-Qwen2.5-VL-7B-Instruct-f16.gguf` est en architecture
`clip` et déclare, relevé dans son en-tête :

| clé | valeur | sens |
|---|---|---|
| `clip.vision.image_size` | 560 | taille d'entrée du ViT |
| `clip.vision.patch_size` | 14 | 40 × 40 patchs |
| `clip.vision.embedding_length` | 1 280 | largeur du ViT |
| `clip.vision.block_count` | 32 | profondeur |
| `clip.vision.attention.head_count` | 16 | 80 par tête |
| `clip.vision.feed_forward_length` | 3 420 | MLP |
| `clip.vision.n_wa_pattern` | 8 | **une couche sur 8 en attention locale** |
| `clip.projector_type` | `qwen2.5vl_merger` | fusion 2 × 2 des patchs + MLP |
| `clip.vision.projection_dim` | 3 584 | dimension de sortie (celle du modèle) |
| `clip.vision.image_mean` / `image_std` | 0,4815/0,4579/0,4084 · 0,2686/0,2613/0,2758 | normalisation |

### Inventaire exact des tenseurs (relevé par `--tensors`)

Le moteur sait désormais LISTER un GGUF (`--tensors`, nom, dimensions, type) —
ce qui a permis de relever la structure au lieu de la supposer :

| tenseur | dimensions | rôle |
|---|---|---|
| `v.patch_embd.weight` | [1280, 3, 14, 14] | convolution des patchs |
| `v.patch_embd.weight.1` | [1280, 3, 14, 14] | **second** embedding de patchs (Qwen2.5-VL en a deux) |
| `v.blk.N.attn_q/k/v.weight` | [1280, 1280] | projections, **avec biais** (`attn_q.bias`…) |
| `v.blk.N.attn_out.weight` | [1280, 1280] | sortie d'attention (+ biais) |
| `v.blk.N.ffn_gate/up.weight` | [3420, 1280] | MLP (+ biais) |
| `v.blk.N.ffn_down.weight` | [1280, 3420] | MLP (+ biais) |
| `v.blk.N.ln1.weight`, `ln2.weight` | [1280] | LayerNorm avant attention et avant MLP |
| `v.post_ln.weight` | [1280] | norme finale de la tour |
| `mm.0.weight` | [5120, 5120] | projecteur : 5120 = 1280 × 4 (fusion 2 × 2) |
| `mm.2.weight` | [3584, 5120] | projecteur : sortie 3584 (largeur du modèle) |

Deux faits qui changent le plan :

1. **il n'y a AUCUN `position_embd`** — Qwen2.5-VL n'utilise pas d'embedding de
   position absolu dans le ViT, mais une rotation 2-D (mRoPE). Mon plan initial
   supposait un embedding de position : c'était faux ;
2. **les biais sont partout** (q, k, v, sortie, MLP) : les oublier est l'erreur
   classique de ce dépôt (elle a déjà coûté 39,80 → 20,84 sur gpt-oss).

Les 519 tenseurs couvrent donc la tour complète et son projecteur : le chemin
image peut se construire sur ce fichier seul, sans le modèle de langage.

`n_wa_pattern = 8` confirme le point délicat annoncé : **toutes les 8 couches,
l'attention est locale** — il faut la même fenêtre que llama.cpp, sinon les
embeddings d'image divergent sans que rien ne le signale.

### ÉTAT : les DEUX EXTRÉMITÉS du chemin image sont faites et validées

| tranche | écart max relatif contre numpy |
|---|---|
| embedding de patchs (convolution 14 × 14) | **5,37e-07** |
| **une couche du ViT** (bloc 0, sans rotation) | **1,82e-06** |
| projecteur (fusion 2 × 2 → `mm.0` → GELU → `mm.2`) | **1,73e-06** |

La couche validée fait toute la plomberie : LayerNorm (`ln1`, `ln2`, eps de
`clip.vision.attention.layer_norm_epsilon`), q/k/v **avec leurs biais**, attention
globale, `attn_out` + biais, deux résidus, MLP `ffn_gate`/`ffn_up` + biais,
**SiLU** (`clip.use_silu = 1` — ce n'est PAS un GELU dans le ViT, contrairement au
projecteur), `ffn_down` + biais. Ce qui n'y est pas encore : la rotation 2-D et la
fenêtre locale.

Le projecteur consomme les quatre patchs d'un groupe 2 × 2 concaténés en ordre
raster, applique `mm.0` (5120 → 5120) + biais, un GELU exact, puis `mm.2`
(5120 → 3584) + biais : 3 584 valeurs, |sortie| = 17,88. La référence numpy
utilise la MÊME approximation d'erf que le moteur (Abramowitz-Stegun 7.1.26) :
comparer deux formules différentes mesurerait l'approximation, pas
l'implémentation.

Ce qui reste est le MILIEU : la rotation 2-D des patchs (mRoPE), les 32 couches
avec attention locale une sur huit, `v.post_ln`. Puis l'injection des embeddings
dans le flux de jetons, qui manque au moteur.

**Le pas suivant, en détail** (pour qu'une session suivante n'ait pas à
l'enquêter) :

1. une couche = `ln1` → q/k/v (+ biais) → attention → `attn_out` (+ biais) →
   résidu → `ln2` → `ffn_up`/`ffn_gate` (+ biais, GELU sur la porte) →
   `ffn_down` (+ biais) → résidu. Les biais sont partout, et les oublier est
   l'erreur classique de ce dépôt ;
2. la rotation est **2-D** (mRoPE) : chaque patch a une position (ligne, colonne)
   et la rotation s'applique par paires d'axes, pas par positions scalaires. La
   CONVENTION exacte (répartition des fréquences entre les deux axes, moitié
   tournée) est le seul point non vérifiable localement : la lever en comparant
   les deux conventions plausibles à la référence numpy, puis en validant la
   sortie complète contre llama.cpp (`llama-mtmd-cli` si disponible) ;
3. l'attention est **locale une couche sur huit** (`n_wa_pattern = 8`) : sur les
   couches locales, la fenêtre est le groupe de patchs de la même ligne ; s'y
   tromper fait diverger les embeddings sans aucun signal ;
4. l'injection dans le flux de jetons demande un chemin qui parte d'un VECTEUR et
   non de `token_embd` — `forward` n'en a pas, et c'est le seul ajout
   d'architecture nécessaire au moteur.

### Détail de la première tranche (embedding de patchs)

`--banc-vision` fait tourner la convolution 14 × 14 du ViT sur une image 28 × 28
déterministe (dégradé + carré central) et écrit les 4 patchs × 1 280 canaux ;
`tools/vision_ref.py` refait le calcul en numpy à partir des mêmes poids. Le
partage des rôles est le même que pour MLA : la référence refait la FORMULE,
l'extraction des tenseurs étant vérifiée par `--tensors`.

Mesure : **écart max relatif 5,4e-7** — le bruit de virgule flottante du moteur,
comme pour MLA. La tranche est isolée à dessein : si l'embedding de patchs est
faux, tout ce qui suit l'est aussi, et le comparer seul évite d'attribuer au
modèle une erreur de découpage.

Reste, dans l'ordre : la rotation 2-D (mRoPE) des patchs, les 32 couches avec
l'attention locale une sur huit, la norme finale, le projecteur `mm.0`/`mm.2`
(fusion 2 × 2), et enfin l'injection des embeddings dans le flux de jetons — le
point d'architecture qui manque au moteur.

### Une RÉFÉRENCE est disponible sur cette machine (découverte)

Le plan disait « valider contre llama.cpp si `llama-mtmd-cli` est disponible » :
il ne l'est pas, mais **ollama embarque la bibliothèque multimodale de
llama.cpp** — `/usr/lib/ollama/libmtmd.so` exporte `mtmd_init_from_file`,
`mtmd_bitmap_init`, `mtmd_tokenize`, `mtmd_encode`… et `/usr/lib/ollama/libllama.so`
expose 3 989 symboles `llama_*`. Il n'y a pas d'en-têtes dans `/usr/include`, mais
ce dépôt a l'habitude de déclarer à la main ce dont il a besoin (c'est ainsi que
les noyaux CUDA sont liés).

Recette pour la prochaine session :

1. charger le modèle de texte (`llama_model_load_from_file`) — la 4,4 Go
   Qwen2.5-VL-Q4_K_M est là ;
2. `mtmd_init_from_file(mmproj, model, params)` avec une structure de paramètres
   **remise à zéro** (le tout-zéro donne les valeurs par défaut) ;
3. `mtmd_bitmap_init(28, 28, image_rgb)` avec la MÊME image déterministe que le
   banc, puis `mtmd_tokenize` sur un texte contenant le marqueur d'image ;
4. `mtmd_encode` puis `mtmd_get_output_embd` → les embeddings d'image, à
   comparer aux 3 584 valeurs du projecteur du moteur.

C'est la seule vérification qui trancherait D'UN COUP la convention de rotation
2-D, la fenêtre locale et la fusion 2 × 2 : elle compare la sortie complète, pas
une tranche.

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
