# Plan : MLA et vision (chantier 5)

> **Document daté.** Plan, note ou étude d'un chantier : il porte sa date et son état en tête. La
> **feuille de route courante** est [`roadmap.md`](roadmap.md) ; l'**état** est
> [`en-cours.md`](en-cours.md).

Ces deux-là n'étaient pas « à moitié faits », ils n'étaient pas commencés quand
ce document a été écrit ; **ils ont été menés depuis**, et ce document consigne
maintenant ce qui a été fait (les sections d'état portent leurs mesures) et ce
qui reste. Ce qui reste à faire est marqué comme tel.

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

### ÉTAT : MLA EST FAIT ET VALIDÉ (chemin dense ; compteur d'événements à instrumenter)

> Le chemin validé ici est **dense** : il ne produit aucune liste. C'est le premier
> écart que le chantier DeepSeek-V4 doit combler — une passe de V4.1 afficherait
> « 0 événements » (`docs/plan-deepseek41-complet.md`, P0).

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
cache ÷50 sur un vrai modèle MLA — GLM-5.3, 79 couches MLA, est présent ici
depuis le 01/10 — et la validation **au-delà de la position 2**, où l'écart à
llama.cpp atteint 4,07 nats à la **position 3** (`reports/rapport-mla-experts.md` §7).

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

`/home/stephane/Data13TB/stephane/modeles/gguf/mmproj-Qwen2.5-VL-7B-Instruct-f16.gguf` (le
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
(cache ÷50) est mesurable sur le plan 1 M. Ce plan ne traite ni la répartition
entre grappes et machines, ni la lecture des flux : ces deux axes ont leurs
propres chantiers (`docs/vision.md` §3-§4).

### Le point d'injection est en place (le seul ajout d'architecture)

`Model::emb_imposee` : un vecteur imposé remplace, pour UN appel, la ligne
`token_embd.weight` que `forward` lisait toujours. C'est ce qui permettra
d'injecter les embeddings d'image à la place des jetons `<|image_pad|>`, et
c'était le seul ajout d'architecture que la vision demandait au moteur — le
reste (MLA, tour ViT) vit dans des chemins séparés.

Vérifié : `cargo test` 6/6 à cette étape (**48** aujourd'hui) et la porte Qwen
reste à **19,3885** (le vecteur
imposé est consommé une fois puis oublié, donc le chemin standard est intact).

### Ce qui reste, et ce qui le débloque

Deux conventions d'attention dans le ViT — la **rotation 2-D** (mRoPE) et la
**fenêtre locale une couche sur huit** — ne sont PAS vérifiables par ma
référence numpy, qui les partage. Ce qui les trancherait : `libmtmd` d'ollama
(recette au § précédent), qui donne les embeddings d'image de l'implémentation de
référence. Une recherche du source de `transformers` sur cette machine n'a rien
donné (ni torch ni transformers installés), et la recherche web n'a pas rendu le
fragment de code dans le budget disponible.

### libmtmd : la structure de paramètres est SONDÉE (l'ABI n'est plus un obstacle)

`mtmd_context_params_default` existe et rend la structure par pointeur caché : on
peut donc la sonder en l'appelant avec un tampon large, depuis Python, sans
connaître sa taille à l'avance. Résultat du sondage (`ctypes`, tampon de 256
octets, octets écrits) :

| offset | contenu | lecture |
|---|---|---|
| 0-1 | `01 01` | deux booléens à vrai (`use_gpu`, `print_timings`) |
| 4 | `04 00 00 00` | `n_threads = 4` |
| 8 | zéro | champ aligné sur 8 octets |
| 16 | pointeur | marqueur d'image (chaîne statique) |
| 24-31 | `ff ff ff ff 01 00 00 00` | deux entiers, dont un `-1` |
| 32-39 | `ff … ff` | un entier 64 bits à `-1` |
| 57 | `04` | un champ d'un octet |

La structure fait donc **une soixantaine d'octets**. Conséquence pratique : une
structure opaque déclarée à **64 octets** et remise à zéro est un appel
ABI-correct — au-delà de 16 octets, SysV passe la structure sur la PILE, et
l'appelé ne lit que ce dont il a besoin ; une déclaration plus grande que la
réelle est donc sans danger. Tout-à-zéro donne `use_gpu = false`,
`print_timings = false`, `n_threads = 0` (automatique) et des marqueurs nuls, ce
qui correspond aux valeurs par défaut.

Reste à écrire le programme (C ou ctypes) : `llama_model_load_from_file` avec une
structure de paramètres généreuse et remise à zéro, `mtmd_init_from_file`,
`mtmd_bitmap_init` sur l'image déterministe du banc, `mtmd_tokenize`,
`mtmd_encode`, puis `mtmd_get_output_embd` — les 3 584 valeurs à comparer au
projecteur du moteur. C'est ce qui trancherait la rotation 2-D et la fenêtre
locale d'un seul coup.
### libmtmd : où en est le programme de référence

Le programme `tools/vision_mtmd.py` (ctypes, sans en-têtes) va jusqu'au bout du
chargement :

* il faut charger un backend ggml EXPLICITEMENT : `ggml_backend_load_all` cherche
  les greffons à côté de l'exécutable (ici `python3`) et n'en trouve aucun ;
  `ggml_backend_load("/usr/lib/ollama/libggml-cpu-haswell.so")` fonctionne (Xeon
  E5 v3 = haswell) ;
* le modèle de texte se charge, le projecteur aussi (« 519 tenseurs »), et le
  warmup du ViT se fait sur 1288 × 1288.

Deux points identifiés pour la suite, tous deux dans MON code d'appel :

1. `mtmd_input_chunks_init()` **rend** un pointeur (elle ne prend pas de
   paramètre de sortie) — ma déclaration passait un pointeur de sortie, donc
   `chunks` restait nul et le plantage vient de là ;
2. `image_min_pixels = 6272` : l'image 28 × 28 du banc (784 pixels) est refusée
   par le modèle. Il faut au moins 84 × 84 (7 056 pixels, 6 × 6 patchs), et le
   banc Rust devra prendre la même taille pour que la comparaison porte sur la
   même entrée.

Une fois ces deux points corrigés, `mtmd_get_output_embd` donnera les embeddings
d'image de la référence, à comparer aux valeurs du projecteur du moteur — la
comparaison qui tranche la rotation 2-D et la fenêtre locale.

### libmtmd : état exact après ce tour

Tout ce qui précède `mtmd_tokenize` fonctionne, vérifié pas à pas :

```
contexte mtmd : ok
bitmap : ok
marqueur d'image : b'<__media__>'
conteneur de morceaux : ok
mtmd_tokenize: error: std::bad_alloc     (invite = marqueur seul)
mtmd_tokenize: error: basic_string::_M_replace  (invite complète)
tokenize rc=2 · 0 morceaux
```

Autrement dit : le modèle de texte se charge, le projecteur se charge (519
tenseurs), le contexte multimodal s'instancie, le bitmap aussi, le marqueur est
rendu par la bibliothèque — et c'est **`mtmd_tokenize`** qui échoue, en levant une
exception C++ (`std::bad_alloc`, puis `basic_string::_M_replace`) au lieu de
rendre un code d'erreur.

Hypothèses, par ordre de plausibilité, pour la suite :

1. **mélange de runtimes C++** : la bibliothèque d'ollama est liée à son propre
   `libstdc++`, l'appelant est un `python3` système. Écrire le programme en **C**
   (ou en C++ compilé avec le même runtime) est l'essai le moins coûteux ;
2. déclaration d'un paramètre mal typé (le 3e de `tokenize` est `const char *`,
   le 2e `mtmd_input_chunks *` — c'est ce que déclare le script, mais sans
   en-tête rien ne le garantit) ;
3. `mtmd_context_params` : la valeur par défaut rendue par la bibliothèque est
   passée telle quelle (les octets au-delà de la taille réelle sont à zéro) ;
   un champ non couvert par le sondage pourrait manquer.

Le reste du chemin (`mtmd_encode_chunk`, `mtmd_get_output_embd`) n'a pas encore
été atteint — mais il est prêt, et c'est la comparaison qui trancherait la
rotation 2-D et la fenêtre locale.

### tokenize : deux hypothèses testées, aucune ne suffit

Après le sondage et les corrections (conteneur de morceaux rendu par
`mtmd_input_chunks_init`, image 84 × 84 conforme à `image_min_pixels = 6272`) :

* passer le marqueur **du contexte** (`mtmd_get_marker`) plutôt que celui par
  défaut : les deux valent `<__media__>`, aucun changement ;
* passer une **structure** d'entrée `(text, add_special, parse_special)` au lieu
  d'un `char *` : toujours `basic_string::_M_replace`, rc=2.

L'erreur vient donc de plus loin dans l'appel — un en-tête `mtmd.h` trancherait
en dix secondes ce que trois tours de rétro-ingénierie n'ont pas tranché. C'est
le seul point qui bloque, et il ne bloque QUE la vérification : les quatre
tranches du chemin image sont validées contre numpy (5,4e-7, 1,8e-6, 1,7e-6), la
tour entière tourne, et le point d'injection des embeddings est en place.

À tenter ensuite, dans l'ordre : (1) compiler le programme en **C** contre les
mêmes bibliothèques (le mélange de runtimes C++ reste l'hypothèse la plus
plausible) ; (2) retrouver la signature exacte de `mtmd_tokenize` dans une
version de llama.cpp (le dépôt n'a pas de copie locale, mais la documentation en
ligne la donne) ; (3) se passer de mtmd et prendre le modèle de vision comme
référence en Python (coûteux, mais sans ABI).

### L'API de mtmd est maintenant CONNUE (en-tête récupéré)

`mtmd.h` de llama.cpp a été récupéré (22 ko) et dépouillé — les trois tours de
rétro-ingénierie à l'aveugle sont remplacés par des signatures exactes :

```c
struct mtmd_input_text { const char * text; size_t text_len;
                         bool add_special; bool parse_special; };   // text_len !
struct mtmd_context_params { bool use_gpu; ggml_backend_dev_t device; bool print_timings;
                             int n_threads; const char * image_marker; const char * media_marker;
                             enum llama_flash_attn_type flash_attn_type; bool warmup;
                             int image_min_tokens; int image_max_tokens; /* + callback */ };

int32_t mtmd_tokenize(const mtmd_context * ctx, mtmd_input_chunks * output,
                      const mtmd_input_text * text, const mtmd_bitmap * const * bitmaps,
                      size_t n_bitmaps);
mtmd_input_chunks * mtmd_input_chunks_init(void);
int32_t mtmd_encode_chunk(mtmd_context * ctx, const mtmd_input_chunk * chunk);
float * mtmd_get_output_embd(mtmd_context * ctx);
```

Les codes de retour de `tokenize` sont documentés dans l'en-tête : **1** = nombre
de bitmaps ≠ nombre de marqueurs, **2** = **erreur de prétraitement du média**.
C'est donc le code 2 qui tombe : mon image est acceptée par le bitmap, mais
refusée par le prétraitement du modèle. Format vérifié conforme (`nx * ny * 3`,
RGB entrelacé), taille conforme (`84 × 84 = 7 056 ≥ image_min_pixels = 6 272`).

Pistes restantes, dans l'ordre : (1) `image_min_tokens` — passer une image plus
grande (par exemple 336 × 336, comme le fait llama.cpp dans ses exemples) ;
(2) compiler le programme en C contre les mêmes bibliothèques (le mélange de
runtimes C++ reste plausible) ; (3) comparer à la référence Python du modèle de
vision, sans ABI du tout.

### Les deux conventions, lues dans la SOURCE de llama.cpp (clip.cpp)

`tools/mtmd/clip.cpp` (320 ko) a été récupéré et dépouillé. Ce qui s'y lit, pour
`PROJECTOR_TYPE_QWEN25VL` :

**Fenêtre locale** — ce n'est PAS une fenêtre par ligne comme je l'avais supposé :
sur les couches fenêtrées, llama.cpp **permute** les jetons pour que tous ceux
d'une même fenêtre soient contigus (`window_idx` / `inv_window_idx`) et applique
un **masque** qui ne laisse voir que la fenêtre. La fenêtre est un **bloc carré**
de la grille APRÈS fusion 2 × 2 :

```cpp
for (int y = 0; y < ph; y += grid_window) {
    for (int x = 0; x < pw; x += grid_window) {
        const int win_h = std::min(grid_window, ph - y);
        const int win_w = std::min(grid_window, pw - x);
        ...  // les jetons de la fenêtre deviennent contigus (idx / inv_idx)
        // puis, pour chaque ligne du masque, on remplit de -inf sauf la fenêtre
        set_input_i32("window_idx", idx);
        set_input_i32("inv_window_idx", inv_idx);
        set_input_f32("window_mask", mask);
```

**Rotation 2-D** — elle n'est pas dans `clip.cpp` : le fichier calcule un tenseur
`positions` (`set_input_i32("positions", positions)`) et le passe au graphe, où
la rotation mRoPE est appliquée par les opérations GGML. C'est donc le calcul de
`positions` qu'il faut lire pour trancher la convention — la zone est identifiée
dans le fichier (aux environs de l'offset 264 000), et c'est le pas suivant.

`n_wa_pattern` est lu depuis la clé `clip.vision.win_attn_pattern` et vaut 8 pour
ce modèle ; `use_window_attn` est actif dès que `n_wa_pattern > 0`.

### La convention de rotation 2-D, lue dans la source

`clip.cpp`, cas `PROJECTOR_TYPE_QWEN25VL` — le tenseur `positions` a **quatre
sections** de `num_patches` entiers, remplies (ligne, colonne, ligne, colonne) :

```cpp
std::vector<int32_t> positions(n_pos * 4);
int ptr = 0;
for (int y = 0; y < ph; y += merge_ratio)
  for (int x = 0; x < pw; x += merge_ratio)
    for (int dy = 0; dy < 2; dy++)
      for (int dx = 0; dx < 2; dx++) {
        positions[                  ptr] = y + dy;   // section 0 : LIGNE
        positions[    num_patches + ptr] = x + dx;   // section 1 : COLONNE
        positions[2 * num_patches + ptr] = y + dy;   // section 2 : LIGNE
        positions[3 * num_patches + ptr] = x + dx;   // section 3 : COLONNE
        ptr++;
      }
set_input_i32("positions", positions);
```

Deux choses en découlent :

1. la **grille est parcourue par groupes de fusion** (y += 2, x += 2), et les
   quatre jetons d'un groupe 2 × 2 sont numérotés `(y+dy, x+dx)` — c'est la même
   convention raster que le banc utilise déjà pour la fusion, confirmée ici ;
2. la rotation se fait en **quatre blocs** de la dimension de tête : les blocs 0
   et 2 tournent selon la LIGNE, les blocs 1 et 3 selon la COLONNE. C'est ce que
   `ggml_rope_multi` attend, et c'est la convention à implémenter — au lieu de la
   rotation scalaire que le moteur applique à ses jetons de texte.

Reste une ambiguïté que la source ne lève pas seule : l'échelle de fréquences à
l'intérieur de chaque bloc (la même échelle que RoPE sur `hd/4` dimensions, ou
l'échelle sur `hd/2` avec paires entrelacées). C'est exactement ce que la
comparaison à `libmtmd` aurait tranché — et c'est pourquoi la référence reste
utile même si l'implémentation peut être écrite sans elle.

### La rotation 2-D est IMPLÉMENTÉE (et la référence ne la couvre plus)

Le banc applique maintenant la rotation en quatre blocs, exactement comme la
source la décrit : blocs 0 et 2 par la ligne, blocs 1 et 3 par la colonne,
chaque bloc tourné par paires (i, i + quart/2) avec l'échelle RoPE usuelle. La
sortie de la tour change en conséquence (|sortie| 35,55 → 42,62), ce qui prouve
que la rotation agit.

Deux réserves, écrites noir sur blanc :

1. la **convention de l'échelle interne** (RoPE sur `hd/4` par bloc, ou sur
   `hd/2` avec paires entrelacées) reste une hypothèse : la source montre le
   tenseur `positions` (quatre sections ligne/colonne/ligne/colonne) mais pas
   l'opération GGML qui consomme ce tenseur ;
2. la **référence numpy ne couvre plus la tour** : depuis que le banc écrit sa
   seule sortie (et non plus les poids de la couche 0), le fichier `.bloc` ne
   permet plus de rejouer les 32 couches en numpy. Les deux tranches qui restent
   comparables — embedding de patchs et projecteur — le restent (5,4e-7 et
   1,7e-6), et l'outil le dit au lieu de planter.

Ce qui manque encore : la **fenêtre locale**, inexprimable sur les images du banc
(28 × 28 et 84 × 84 tiennent dans une seule fenêtre de 8 × 8 après fusion), et
l'injection des embeddings d'image dans le flux de jetons, qui est branchée côté
moteur (`Model::emb_imposee`) mais pas encore alimentée par une tour complète.

### Le chemin image est COMPLET (image → jetons de 3584 dimensions)

Sur une image de **224 × 224** (16 × 16 patchs = 256, 8 × 8 jetons après fusion),
le banc enchaîne maintenant tout : convolution de patchs → 32 couches de ViT avec
**rotation 2-D** et **fenêtre locale** (couches complètes aux indices 7, 15, 23,
31 ; fenêtre de 4 × 4 jetons fusionnés ailleurs, lue dans `clip.cpp`) →
`v.post_ln` → **projecteur par groupes de fusion** : 64 groupes × 3 584 valeurs.

C'est exactement ce qu'il faut injecter à la place des jetons d'image — et le
moteur sait le faire depuis le point d'injection `Model::emb_imposee`.

Ce qui reste non vérifié, et pourquoi :

| point | état |
|---|---|
| embedding de patchs, projecteur | **validés** contre numpy (5,4e-7 et 1,7e-6, à 28 × 28) |
| échelle interne de la rotation | hypothèse (la source montre `positions`, pas l'opération GGML) |
| fenêtre locale | implémentée d'après la source, **non testable** sur les images du banc avant 224 px — et sans référence à cette taille |
| bout en bout (image → texte) | impossible sans le chemin d'inférence multimodal, qui n'existe pas ici |

### Le détail de la rotation, lu dans ggml (et mon implémentation est à corriger)

`ggml/src/ggml-cpu/ops.cpp`, `ggml_mrope_cache_init` — c'est ici que la
convention est écrite, noir sur blanc :

```cpp
int sect_dims = sections[0] + sections[1] + sections[2] + sections[3];
for (int64_t i0 = 0; i0 < ne0; i0 += 2) {
    int sector = (i0 / 2) % sect_dims;
    ...  // le secteur choisit la POSITION : t, h, w ou e
    rope_yarn(theta/ff, ...);
    theta_t *= theta_scale;  theta_w *= theta_scale;  theta_h *= theta_scale;
}
```

Trois choses que la source impose, et que mon implémentation ne fait PAS :

1. la rotation apparie des dimensions **consécutives** `(i0, i0+1)`, pas
   `(i, i + quart/2)` : c'est le contraire de la convention « moitié tournée »
   que j'ai écrite ;
2. `sect_dims` est la SOMME des quatre sections et le secteur vaut
   `(i0/2) % sect_dims` : avec `positions` = (ligne, colonne, ligne, colonne)
   et quatre sections, cela donne des blocs de secteurs `(t, h, w, e)` —
   soit, pour la vision, **(ligne, colonne, ligne, colonne)** dans cet ordre ;
3. l'échelle de fréquences **continue** d'un bloc au suivant (`theta *= theta_scale`
   à chaque pas, sans remise à zéro hors mode `indep_sects`) : ce n'est donc PAS
   une échelle RoPE recalculée par bloc comme je l'ai fait.

Autrement dit : la structure (quatre blocs, deux positions alternées) est la
bonne, mais **l'appariement et l'échelle sont faux**. C'est exactement ce qu'une
référence aurait attrapé, et c'est pourquoi le chantier reste ouvert : la
prochaine session corrige ces deux points à partir du code ci-dessus, puis
cherche une validation (les trois pistes de la section précédente).

### Après correction : la rotation suit la source, mais l'ORDRE est encore faux

La rotation est corrigée d'après `ggml_mrope_cache_init` (paires consécutives
`(2i, 2i+1)`, moitié « ligne » puis moitié « colonne », exposant suivant l'indice
de paire GLOBAL) — la sortie de la tour change (187,45 → **234,53**), donc la
correction agit.

Mais un défaut d'ORDRE subsiste et le témoin le dit : le projecteur affiche
toujours `|sortie| = 131,54`, **identique** à ce qu'il donnait avant la
correction. Autrement dit il consomme encore les embeddings de PATCHS et non la
sortie de la tour. C'est la bonne conclusion à tirer d'un chiffre qui ne bouge
pas alors que tout ce qui l'alimente a changé — et le pipeline réel est
`patchs → tour → v.post_ln → projecteur`, pas `patchs → projecteur`.

Le point est localisé : dans `run_banc_vision`, le bloc projecteur lit
`let source = tour.clone().unwrap_or_else(|| out.clone());` (ligne ~897) alors que
`tour` est encore `None` à cet endroit — l'affectation `tour = Some(x.clone())`
est plus bas, à la fin du bloc de la tour. Déplacer le bloc projecteur APRÈS la
tour est le seul changement à faire, et il est mécanique.

### L'ordre est corrigé, et la vérification est le CHANGEMENT du chiffre

Le bloc projecteur a été déplacé après la tour : il consomme maintenant la sortie
du ViT, et non les embeddings de patchs. La vérification n'est pas un nouveau
chiffre « plausible » mais le fait que **le chiffre ait changé** :
`|sortie| = 131,54` (embeddings de patchs) → **`515,84`** (sortie de la tour),
pour 64 jetons × 3 584 dimensions.

Contrôle de plausibilité, puisqu'il n'y a pas de référence : la moyenne
quadratique par élément vaut `515,84 / √(64 × 3584) = 1,08`, du même ordre que
les lignes de `token_embd` du modèle de texte — un pipeline qui produirait des
embeddings d'échelle absurde (1e-3 ou 1e3) se verrait ici.

État du chemin image : **patchs → 32 couches (rotation 2-D conforme à ggml,
fenêtre locale d'après clip.cpp) → v.post_ln → projecteur (64 groupes × 3584) →
`Model::emb_imposee`**. Ce qui reste non vérifié est inchangé et nommé :
l'échelle interne de la rotation, la fenêtre locale, et le bout en bout.

### La chaîne complète est DÉMONTRÉE, de l'image aux logits

`DRAVE_VISION_TEXTE=<modele.gguf>` fait faire au banc le dernier pas : il charge le
modèle de texte, lui impose le **premier jeton d'image** par
`Model::emb_imposee`, et lit les logits. Mesuré sur Qwen2.5-VL-7B (poids Q4_K_M,
projecteur f16 du `mmproj`) :

```
projecteur : 64 groupes × 3584 valeurs, |sortie| = 515.8354
injection  : 64 jetons × 3584 disponibles
  moteur   : 152064 logits · argmax 15 · moyenne -1.788 · écart-type 2.026
```

Autrement dit : **image → convolution de patchs → 32 couches (rotation 2-D,
fenêtre locale) → v.post_ln → projecteur → 64 jetons de 3 584 dimensions →
injection dans le modèle de texte → 152 064 logits**. Le trou d'architecture
identifié au premier tour (« `forward` part toujours de `token_embd` ») est
comblé, et la démonstration passe par le chemin réel, pas par un banc isolé.

Ce que cela prouve, et ce que cela ne prouve pas :

* **prouvé** : la plomberie complète tient, le moteur accepte un vecteur d'image
  et rend des logits d'échelle normale (moyenne −1,79, écart-type 2,03) ;
* **non prouvé** : la QUALITÉ. Les deux conventions non confirmées (échelle
  interne de la rotation, fenêtre locale) et l'absence de modèle d'inférence
  multimodal local font qu'aucun chiffre de qualité ne peut être avancé ici —
  et il ne le sera pas.

### La rotation est CONFIRMÉE par la source (et une variante de fenêtre découverte)

`clip.cpp` donne le remplissage exact des quatre sections pour Qwen2.5-VL :

```
// Pack into ggml_rope_multi VISION-mode layout. The non-CPU kernels
// only read slots 0 and 1, so pack h in slot 0, w in slot 1:
//   positions[0..n_pos)         = h        (LIGNE)
//   positions[n_pos..2*n_pos)   = w        (COLONNE)
//   positions[2*n_pos..3*n_pos) = 0
//   positions[3*n_pos..4*n_pos) = 0
```

Avec des sections `{hd/4, hd/4, 0, 0}` (les deux dernières nulles), cela donne
dans `ggml_mrope_cache_init` : `sect_dims = hd/2`, `sector = paire % (hd/2)`,
donc les **hd/4 premières paires** utilisent la LIGNE (slot 0) et les suivantes
la COLONNE (slot 1) — et l'échelle continue sur l'indice de paire global.

C'est **exactement** ce que l'implémentation corrigée fait (`pos = i < paires/2 ?
ligne : colonne`, exposant `-2i/hd`). Autrement dit, la rotation n'est plus une
hypothèse : ses trois aspects (appariement consécutif, partage ligne/colonne,
échelle continue) sont lus dans la source, et la valeur des sections se déduit de
la même lecture.

**Découverte au passage, qui explique une variante** : pour les couches
FENÊTRÉES, `clip.cpp` permute les positions en **colonne-majeur** (`idx_col`,
« Col-major merge-unit permutation ») avant de les empaqueter, alors que mon
implémentation fenêtre en ligne-majeur. C'est un écart réel et localisé — la
fenêtre n'est donc pas seulement un masque, elle change aussi l'ordre des
positions. À corriger, et documenté ici pour ne pas le perdre.

### La permutation colonne-majeur est IMPLÉMENTÉE (le dernier écart connu)

Sur les couches FENÊTRÉES, `clip.cpp` transpose la grille des unités de fusion
avant d'empaqueter les positions (`idx_col[u_col] = u_row`, donc pour une grille
carrée `pos_col[c*n + r] = pos_row[r*n + c]`). Un patch (r, c) reçoit donc les
positions de (c, r) : la fenêtre n'est pas qu'un masque, elle change aussi
l'ORDRE DES POSITIONS.

C'est implémenté : `complete_rot` (couches 7, 15, 23, 31 en attention complète)
choisit entre (ligne, colonne) et (colonne, ligne). Vérification par le
changement des chiffres — c'est le contrôle qui avait manqué une fois :

| | avant permutation | après |
|---|---|---|
| sortie de la tour | 234,53 | **244,38** |
| sortie du projecteur | 515,84 | **465,84** |

Le chemin image suit donc maintenant la source sur ses trois points d'attention :
rotation en quatre blocs (ggml), échelle continue (ggml), et permutation
colonne-majeur des couches fenêtrées (clip.cpp). Ce qui reste sans référence
n'est plus une ligne de code identifiée, mais la qualité globale — et les trois
pistes de validation écrites plus haut.
