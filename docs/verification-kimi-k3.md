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

## 4bis. Le côté moteur est déjà branché (03/10)

`--k3-essai` charge la couche 0, la calcule sur les jetons donnés, et **vide ses
sorties au format du moteur** (`DRAVE_DUMP_COUCHES=<préfixe>` →
`<préfixe>-l_out-0-<position>.bin`, f32 brut). Mesuré : trois jetons, trois
fichiers de 28 672 octets (7 168 × 4), valeurs finies et croissantes en norme
(0,97 · 1,43 · 1,50).

Il contrôle aussi, **avant tout calcul**, les dimensions des quatre types de
couches (0 dense, 1 MoE+KDA, 3 MoE+MLA, 4 KDA) contre ce que la configuration
déclare — c'est ce qui attrape une dimension lue du mauvais côté (le moteur range
`dims[0] = ne1` = la sortie, l'inverse du fichier).

### 4ter. Le modèle est COMPLET, et les chiffres n'ont pas bougé (bloc 31)

Le 04/10 à 14:01, le 32e shard est arrivé. `--k3-essai` relancé sur les **32
shards** donne, au chiffre près, les **mêmes** valeurs que les passes faites
pendant le transfert (25 shards sur 32) :

| sortie | 25/32 shards | 32/32 shards |
|---|---|---|
| MoE couche 1, \|sortie\| | 0,7316 | **0,7316** |
| composition 0-3, \|l_out\| (4 jetons) | 8,7757 · 5,2909 · 5,2559 · 5,4735 | **identiques** |
| couche 0, \|l_out\| (3 jetons) | 0,9731 · 1,4310 · 1,4958 | **identiques** |

C'est la vérification de l'ouverture tolérante : les shards déjà là portaient
**les octets définitifs**, et un débogage mené pendant un transfert de 1,5 To
n'était donc pas un débogage sur des données provisoires.

### Le premier franchissement de BANQUE (bloc 31)

`DRAVE_K3_COUCHES=13` compose les couches **0 à 12**. Ce n'est pas « quatre
couches en plus » : la première banque est la couche 0, la **suivante est la
12**, donc quatre couches n'exerçaient ni le redémarrage du flux résiduel ni un
`res_mix` à **deux** points de contrôle. Mesuré, quatre jetons :

| jeton | \|l_out\| couches 0-12 |
|---|---|
| 0 | 9,6728 |
| 1 | 9,9734 |
| 2 | 9,2453 |
| 3 | 8,9678 |

Tous finis, 3 356 273 ms au total (14 min par jeton pour 13 couches — c'est le
chemin f32 de vérification). Les sorties de la couche 0 redonnent **au chiffre
près** celles des passes précédentes (0,9731 · 1,4310 · 1,4958), et les sorties
`l_out-12` sont vidées pour la comparaison avec la référence.

Le chemin K3 est un instrument de **vérification**, pas d'exécution : il
déquantifie en f32 (une couche MoE = 28,7 s/jeton, la composition des couches 0-3
= 366 s pour 4 jetons). Les 93 couches en f32 demanderaient ~220 Go de RAM.

### 4ter-bis. La référence A TOURNÉ — les chiffres de la baseline (04/10, 22h57)

`REF_SANS_REPACK=1 tools/ref_logits_k3 <K3> <ids> <sortie> 4 --tensors l_out`,
sur le modèle complet, quatre jetons :

| mesure | valeur |
|---|---|
| temps mural | **2 h 48 min 21 s** pour 4 passes → **~42 min par jeton** |
| occupation CPU | **11 %** (le reste est de l'attente disque) |
| lectures | 1,80 To (blocs de 512 o comptés par le noyau) → **451 Go par jeton** |
| RSS maximal | 102 Go · **swap 0** (grâce à `REF_SANS_REPACK`) |
| sorties | **100 vidages** : les 93 couches `l_out-0` … `l_out-92` + variantes |
| logits | `refk3_logits.bin`, 3 × 163 840 f32 · « perplexité » 43,598 sur 3 positions (non interprétable en deçà de 64 prédictions — c'est la règle du dépôt) |

**Ce que ça établit** : llama.cpp-k3 fait tourner Kimi-K3 sur cette machine, à
**42 minutes par jeton**, borné par le disque et non par le calcul (11 % de CPU).
C'est la première mesure de la référence sur cette classe, et c'est le chiffre
auquel comparer tout ce que le projet proposera.

Les 93 couches vidées permettent désormais de **bissecter** la divergence : il
suffit de comparer couche par couche pour trouver la PREMIÈRE qui décroche, au
lieu de raisonner sur la sortie de la couche 0.

### 4quater-ter. LA COUCHE 0 PASSE (05/10, 02h25)

Trois défauts, tous trouvés par la comparaison et aucun par relecture :

1. **la norme L2 par tête sur `q` et `k`** (`build_gdn_l2_norm`) n'existait nulle
   part dans le moteur ;
2. **la banque résiduelle s'accumulait entre les jetons** au lieu d'être propre
   à la passe du jeton courant ;
3. **son ORDRE de remise à zéro** : elle doit être repartie **avant** l'attention
   résiduelle, pas après. Dans la référence, `resi_stack` est vide à cette étape
   de la couche 0, **à chaque jeton** ; garder le `n_ckpt` du jeton précédent
   faisait appliquer un `res_mix` là où la référence n'en applique pas.

| couche 0, quatre jetons | corrélation | écart max | dynamique |
|---|---|---|---|
| jeton 0 | 0,983164 → **0,999979** | 1,19e-02 → **3,74e-04** | 9,66e-02 |
| jeton 1 | 0,790361 → **0,999982** | 1,55e-01 → **2,92e-04** | 1,10e-01 |
| jeton 2 | 0,641780 → **0,999983** | 1,80e-01 → **3,07e-04** | 2,16e-01 |

Les trois étaient **invisibles au jeton 0 seul** — c'est ce qui les a fait
survivre deux jours de transcription. Et le test « KDA contre NumPy » les
couvrait tous les trois : il comparait le code à sa propre transcription.

Ce qui reste : la couche 12 (13 couches enchaînées, une banque franchie) et
l'écart résiduel de 0,4 % — de l'ordre de l'accumulation f32 sur des poids Q8_0,
à confirmer couche par couche avec les vidages instrumentés.

### 4quater-bis. DEUX BUGS TROUVÉS PAR LA COMPARAISON (05/10, 00h25)

**1. La norme L2 par tête sur `q` et `k` n'existait nulle part.**
`build_gdn_l2_norm` (référence) : `x / sqrt(Σx² + eps)`, plus `1/sqrt(head_dim)`
sur `q` seul. Sa signature était dans les chiffres : au jeton 0 l'état delta est
nul, donc `o[j] = β·(Σ_i k[i]q[i])·v[j]` — proportionnel à `v` quelle que soit
l'échelle de `q` et `k` — et la norme par tête qui suit efface cette échelle.
D'où 0,983 de corrélation au jeton 0 **avec un rapport de norme de 0,937**, puis
0,79 et 0,64 : dès le jeton 1, l'accumulation `s += k ⊗ β(v − sᵀk)` dépend, elle,
de l'échelle de `k`.

| | avant | après |
|---|---|---|
| jeton 0, corrélation | 0,983164 | **0,999979** |
| jeton 0, écart max | 1,19e-02 | **3,74e-04** |

**2. La banque résiduelle s'accumulait entre les jetons.** Dans la référence,
`resi_stack` est une variable locale au graphe — vide à chaque passe, avec une
colonne par jeton du lot. Ici les jetons sont traités un par un : la couche 0
empile l'entrée du jeton COURANT, et rien d'autre.

**Ce qui reste faux** : jetons 1 et 2 à 0,819 et 0,708 de corrélation. C'est un
défaut d'ÉTAT, et un essai de discrimination l'a circonscrit : remettre
convolution et delta à zéro avant chaque jeton (`DRAVE_K3_SANS_ETAT=1`) donne
**pire** (0,606 et 0,414). La référence enchaîne donc bien les jetons, et le sens
de l'état est le bon — c'est un détail de son évolution qui reste faux.

**Vérifié au passage, sans supposition** : `layer_norm_rms_epsilon = 1e-05`,
`kda.head_dim = 128`, `kda.gate_lower_bound = -5.0` (lus dans le GGUF) ;
`ssm_a` est **négatif** (−11,78 à −0,47, donc bien `−exp(A_log)`) ;
`ssm_dt.bias` est **négatif lui aussi** (−7,89 à +0,18), ce qui met `z` vers
−5 et la porte de décroissance vers −0,01 : `exp(g) ≈ 0,99`, décroissance faible.

**Point de méthode** : pour un lot de plusieurs jetons, la référence n'emprunte
PAS `build_delta_net_autoregressive` (qui assert `n_tokens == 1`) mais
`build_delta_net_chunking` — une formulation par blocs de 16 (donc rembourrée de
12 zéros ici), avec un `solve_tri` et un `cumsum` du log de la décroissance.
Mathématiquement équivalente à la forme séquentielle que j'ai transcrite, mais
c'est un chemin de code DIFFÉRENT, et il faut le savoir avant d'accuser l'un ou
l'autre sur un écart.

### 4quater. LE PREMIER JALON EST RENDU — ET IL EST NÉGATIF (04/10, 22h40)

La référence a tourné (`REF_SANS_REPACK=1`, voir plus bas), elle a vidé ses
`l_out-N`, et `tools/compare_etats.py` a comparé. **La couche 0 ne passe pas :**

| position | écart max | corrélation | verdict |
|---|---|---|---|
| 0 | 1,19e-02 | **0,983164** | ❌ |
| 1 | 1,55e-01 | 0,790361 | ❌ |
| 2 | 1,80e-01 | 0,641780 | ❌ |

Et la couche 12, après une banque :

| position | écart max | corrélation | verdict |
|---|---|---|---|
| 0 | 1,11e-01 | **0,990927** | ❌ |
| 1 | 1,02e+00 | 0,458801 | ❌ |
| 2 | 4,06e-01 | 0,448762 | ❌ |

**Ce que ces chiffres disent, et c'est plus utile qu'un simple « non » :**

1. **La position 0 est presque juste** (0,983 sur la couche 0, 0,991 sur la 12).
   La structure du calcul — normes, résidu, projections, MoE latent, SiTU — est
   donc en place : une erreur de forme donnerait une corrélation proche de zéro.
2. **Tout se défait dès la position 1.** Une erreur qui ne dépend pas de la
   position aurait le même écart partout ; ici elle **apparaît entre deux
   jetons**. Les suspects sont donc les mécanismes à ÉTAT : l'état de la
   convolution KDA (`d_conv = 4`) et la récurrence delta-net, qui sont les seuls
   du chemin à transporter quelque chose d'un jeton au suivant. Au jeton 0, la
   convolution ne voit que son remplissage : un état mal avancé ne s'y voit pas.
3. L'écart résiduel de la position 0 (~1 %, norme 0,937 fois celle de la
   référence) est un second défaut, plus petit, à traiter après.

**Prochaine action, dans l'ordre** : comparer non pas la SORTIE de la couche 0
mais les tenseurs intermédiaires déjà instrumentés (`--tensors` de la référence
sait filtrer n'importe quel nœud du graphe ; `kimi_k3.rs` en vidange déjà
plusieurs), en commençant par l'entrée de la convolution et sa sortie au jeton 1.

La comparaison, dès que la référence tournera sur le modèle complet :

```bash
REF_DUMP=/tmp/refk3 LD_LIBRARY_PATH=…/llama.cpp-k3/build/bin \
    tools/ref_logits_k3 <K3.gguf> <ids> /tmp/refk3.bin 4
DRAVE_DUMP_COUCHES=/tmp/notrek3 drave <K3.gguf> --k3-essai
python3 tools/compare_etats.py /tmp/notrek3 /tmp/refk3 l_out 0 0,1,2
```

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
