# V4-Flash : la rotation des couches compressées était le RoPE simple

**En une ligne** : sur les 41 couches compressées de V4-Flash, le moteur appliquait
son régime *retardé* (RoPE simple sous 4 × la longueur d'origine) là où **llama.cpp
et vLLM appliquent tous deux YaRN ×16 à toutes les positions** — et aucune
vérification ne pouvait le voir, parce que YaRN n'interpole que les basses
fréquences, dont les angles sont minuscules aux positions courtes.

## 1. Ce que disent les deux références

llama.cpp, `src/models/deepseek4.cpp:872-879` :

```c
const bool use_compress_rope = hparams.dsv4_compress_ratios[il] != 0;
const float freq_base_l    = use_compress_rope ? hparams.dsv4_compress_rope_base : freq_base;
const float freq_scale_l   = use_compress_rope ? freq_scale : 1.0f;
const float ext_factor_l   = use_compress_rope ? ext_factor : 0.0f;
const float beta_fast_l    = use_compress_rope ? beta_fast : 0.0f;
const float beta_slow_l    = use_compress_rope ? beta_slow : 0.0f;
const int32_t n_ctx_orig_l = use_compress_rope ? n_ctx_orig : 0;
```

Ces paramètres servent aux **trois** rotations de la couche : la requête (`:900`),
la clé (`:919`) et la dé-rotation de sortie (`:1124`). vLLM le dit en toutes
lettres (`vllm/models/deepseek_v41/common/rope.py:28-46`) : « YaRN applies to all
compressed-KV layers (compress_ratio > 0); only pure sliding-window layers use
plain RoPE », et il désactive `mscale` (`mscale = 0`, `mscale_all_dim = 0`).

Côté llama.cpp, `mscale` est **annulé pour V4** par un mécanisme propre au modèle :
`dsv4_rope_attn_factor` (`src/models/deepseek4.cpp:11-17`) renvoie l'**inverse** de
`1 + 0,1·ln(1/freq_scale)`, que le noyau `rope_yarn` remultiplie — produit **1,0
exactement** (vérifié numériquement). `cparams.yarn_attn_factor`, celui que
`llama-context.cpp:492-494` annule, n'est même pas utilisé par le graphe
`deepseek4`. Les deux références concordent donc : **YaRN ×16, sans mscale**.

## 2. Pourquoi aucune vérification ne l'avait vu

YaRN n'interpole que les fréquences **basses** — les paires de grande longueur
d'onde. À une position petite, leurs angles sont minuscules : à la position 4, la
paire la plus lente tourne de 4e-4 rad contre 2,5e-5 en interpolation. Les
comparaisons déjà faites contre llama.cpp sur une clé compressée tournée à une
position **non nulle** (couche 2 CSA, bloc 1 tourné à la position 4, positions
8-9 : corrélation 0,9999, écart 1,3e-2) ne pouvaient donc pas trancher : l'effet
cherché (3,9e-3 à 9,8e-3) était du même ordre que l'écart résiduel de
quantification (1,3e-2).

Le protocole qui tranche : **comparer les deux régimes à des positions où l'effet
dépasse le bruit**, c'est-à-dire 64 à 127 (l'écart d'angle de la paire la plus
lente y passe de 6e-3 à 1,2e-2 rad, l'effet sur l'état croît avec lui).

## 3. Ce qui a été mesuré avant la comparaison

| mesure | valeur |
|---|---|
| effet du correctif sur `l_last-2`, position 0 | **0,000e+00** (la rotation y est l'identité dans les deux régimes) |
| … position 1 | 3,6e-04 |
| … position 4 | 3,9e-03 |
| … position 9 | 1,2e-02 (relatif 7,2e-03) |
| porte V4-Flash 43 couches ctx 32 (5 jetons) | **8430,2968 → 8405,9477** |

Le chiffre de la porte **change parce que le calcul change**, et il change peu à
ctx 32 — exactement ce que la théorie du §2 prédit. La valeur attendue de
`tools/portes.sh` est mise à jour en conséquence, avec sa raison en commentaire.

## 4. Le correctif

| pièce | où | ce qu'elle fait |
|---|---|---|
| `yarn_declare` | `Cfg` | la **déclaration** du modèle, séparée de la décision retardée (`yarn`) : sans elle, le moteur ne savait pas que le modèle déclarait YaRN, il ne le lisait qu'au moment de décider |
| `yarn_compresse` | `Mla4` | la déclaration, retenue **seulement** sur les couches de ratio > 0 — les couches brutes gardent le RoPE simple, où YaRN est l'identité (`factor = 1`) |
| `rope_norm_yarn` | `Model` | convention **NORM** (paires 2i, 2i+1) + interpolation YaRN, sans mscale ; les dimensions de correction se comptent sur les dimensions **tournées** (64), pas sur la tête (512) |
| `tourner` | `attn_v4` | **une seule porte pour les six rotations** de la fonction (requête, clé, clé de bloc, clé et requête d'indexeur, dé-rotation) : llama.cpp utilise les mêmes paramètres pour toutes |
| `DRAVE_YARN_NON` | env | « jamais de YaRN » coupe **aussi** celui des couches compressées, sinon le drapeau ne ferait plus ce qu'il annonce — et c'est ce qui permet de mesurer les deux régimes |
| `--sans-yarn` | flags | **corrigé** : il ne coupait RIEN sur V4 (`cfg_yarn_off` ne touchait que `cfg.yarn`, lu par les seuls chemins denses, alors que `Mla4::yarn_compresse` est figé à la construction). Mesuré par la relecture adverse : `--sans-yarn` → 64 730 738,578 contre `DRAVE_YARN_NON=1` → 65 819 810,336 (+1,7 %) ⇒ le drapeau n'avait rien basculé |
| `as_u64` dans la lecture | `Cfg` | **la vraie cause du premier échec** : `original_context_length` est un **u32** et `as_f64` ne lit que les flottants — le défaut 4 096 prenait la place de 65 536, et la rampe interpolait des paires que la référence n'interpole pas |
| `corr0`/`corr1` **bornées** | `rope_norm_yarn` | `MAX(0,·)` et `MIN(n_dims − 1,·)`, comme ggml (`ggml.c:4471-4480`) et vLLM (`yarn_find_correction_range`, `truncate=True`) : sans elles, base 100 et contexte 2e6 donnent (63, 89) au lieu de (63, 63) et la rampe ne se termine jamais |

## 5. La comparaison décisive : FAITE, et elle valide le correctif

`l_last-2` de la couche 2 (CSA, ratio 4), 128 positions, état de la couche 1
**injecté** depuis llama.cpp (`DRAVE_ETAT_ENTREE=/tmp/ref_yr-l_last-1.bin`, le
harnais des rapports P3/P5), deux variantes du moteur contre le même dump :

| position | YaRN (corr / écart) | RoPE simple (corr / écart) | gagnant |
|---|---|---|---|
| 4 | 0,999919 / 1,342e-02 | 0,999919 / 1,344e-02 | (indiscernables) |
| 8 | 0,999940 / 1,624e-02 | 0,999940 / 1,623e-02 | — |
| 16 | 0,999995 / 1,325e-03 | 0,999995 / 1,321e-03 | — |
| 32 | 0,999995 / 1,943e-03 | 0,999995 / 1,919e-03 | — |
| 64 | 0,999998 / 1,005e-03 | 0,999998 / 9,905e-04 | — |
| 96 | **0,999998 / 1,052e-03** | 0,999997 / 1,107e-03 | YaRN |
| 120 | **0,999996 / 3,680e-03** | 0,999995 / 4,214e-03 | YaRN |
| 127 | **0,999996 / 4,515e-03** | 0,999993 / 5,376e-03 | YaRN |

**llama.cpp applique donc bien YaRN sur ses couches compressées** (son code le
disait, la mesure le confirme), et le correctif rapproche le moteur de sa
référence — l'écart se réduit de 15 % à la position 127 et la corrélation monte.
Aux positions courtes les deux régimes coïncident, comme le §2 l'annonçait.

### L'instrument était faux, et c'est la mesure qui l'a dit

La **première** comparaison donnait l'inverse (le RoPE simple gagnait partout, et
le YaRN perdait de plus en plus avec la position). En remontant des écarts aux
*angles* réellement appliqués — `θ = atan2(b'·a − a'·b, a·a' + b·b')` par paire —
la rampe du moteur s'est révélée être **(8, 18)** au lieu de **(15, 25)** : les
dimensions de correction étaient calculées avec un contexte d'origine de **4 096**
au lieu de 65 536, c'est-à-dire avec le **défaut** de la fonction de lecture.

La cause : `Meta::as_f64()` ne lit **que** les flottants, et
`rope.scaling.original_context_length` est un **u32** dans le GGUF
(`llama_model_loader` l'affiche « u32 »). La lecture renvoyait `None`, le défaut
prenait sa place, et la rampe interpolait des paires que la référence
n'interpole pas. Le facteur (16) et les bêtas (32/1), eux, sont des f32 : ils
étaient lus. **Le bug était invisible** : la rotation restait plausible, aucune
erreur ne sortait, et seule la comparaison de tenseurs pouvait le montrer.

Corrigé (`as_f64().or_else(|| as_u64()…)`), remesuré : le tableau ci-dessus.

## 6. Le protocole, pour rejouer

Une première tentative (sans injection d'état) ne prouvait rien et est conservée
ici comme avertissement :

| | ce que j'ai lancé | ce que ça compare |
|---|---|---|
| référence | `tools/ref_logits` sur V4-Flash, `REF_TENSORS='^(attn_derope|l_last)-2$'`, 128 positions | l'état de la couche 2 du **modèle entier** |
| moteur | `--couches 2:3` **sans état injecté** | la couche 2 seule, son entrée étant l'**embarquement** |

Les corrélations obtenues (0,05 à 0,40, pour les deux régimes, qui se tiennent à
1e-3 l'un de l'autre) mesurent cet écart d'entrée, pas la rotation : les deux
variantes sont indiscernables parce que toutes deux partent du mauvais état.
**Aucun chiffre de cette tentative ne doit être cité.**

Le protocole correct est celui des rapports P3/P5, et il tient en trois étapes :

```bash
# 1. llama.cpp vide l_last-1 ET l_last-2 (mêmes identifiants, ctx 128)
LD_LIBRARY_PATH=… REF_DUMP=/tmp/ref_yr REF_TENSORS='^(l_last)-[12]$' \
  ./tools/ref_logits <V4-Flash> /tmp/ids_v4flash.txt /tmp/ref_yr.bin 128
# 2. le moteur reprend à la couche 2 AVEC l'état de la couche 1
DRAVE_ETAT_ENTREE=/tmp/ref_yr-l_last-1.bin DRAVE_DUMP_COUCHES=/tmp/d_y128 \
  ./drave-core/target/release/drave <V4-Flash> --couches 2:3 --tete-partielle \
  --ppl /tmp/ids_v4flash.txt --ctx 128 --limit 128 --dense
DRAVE_YARN_NON=1 DRAVE_ETAT_ENTREE=/tmp/ref_yr-l_last-1.bin DRAVE_DUMP_COUCHES=/tmp/d_p128 \
  ./drave-core/target/release/drave <V4-Flash> --couches 2:3 --tete-partielle \
  --ppl /tmp/ids_v4flash.txt --ctx 128 --limit 128 --dense
# 3. comparer les DEUX variantes à la référence, positions 64 à 127
python3 tools/compare_etats.py /tmp/d_y128 /tmp/ref_yr l_last 2 64,96,120,127
python3 tools/compare_etats.py /tmp/d_p128 /tmp/ref_yr l_last 2 64,96,120,127
```

Ce que la comparaison doit montrer si le correctif est juste : l'écart de la
variante YaRN **plus petit** que celui de la variante simple, et l'écart entre les
deux variantes croissant avec la position (déjà mesuré, §3). Coût : ~15 min pour
l'étape 1 (modèle de 284 Go sur disque mécanique), ~2 min pour l'étape 2.

**Pourquoi le correctif est quand même appliqué** : il ne repose pas sur cette
mesure mais sur le **code des deux références**, cité au §1 (`use_compress_rope`
de llama.cpp, commentaire explicite de vLLM), et sur l'effet mesuré au §3. La
mesure manquante est une *confirmation*, pas la justification.

### Le signal faible, et pourquoi il ne tranche pas

La perplexité à 10 jetons sur la copie `topk2` (celle des rapports P5) passe de
**678,09** (RoPE simple) à **715,59** (YaRN), contre **548,32** chez llama.cpp.
Ce n'est **pas** un argument contre le correctif : à 10 jetons et à ces
magnitudes (PPL ~600 pour un texte coupé au milieu d'un paragraphe), l'écart de
24 % entre les deux moteurs vient de la quantification des activations de ggml —
c'est la conclusion du rapport P5 — et une seule unité de NLL sur un jeton déplace
la moyenne de 6 %. La comparaison qui tranche est celle du §5, par TENSEUR.

## 7. Ce que ce correctif ne règle pas

- **Rien n'est prouvé sur V4.1** par cette mesure : llama.cpp ne charge pas le
  fichier `deepseek41`. La source (vLLM) dit la même chose que pour V4-Flash, et
  le correctif s'applique aux deux par construction — mais la preuve numérique
  n'existe que pour V4-Flash.
- La porte V4-Flash est passée de 8430,2968 à 8405,9477 : **toute valeur publiée
  avant le 03/10 pour ce modèle est à revérifier** (elle a été calculée avec le
  RoPE simple sur 41 couches sur 44).
