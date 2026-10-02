# V4-Flash, couches 0 et 1 — la première comparaison étage par étage

**En une ligne** : les deux premières couches de **DeepSeek-V4-Flash** tournent
dans Drave et **concordent avec llama.cpp** — hyper-connexions à **1e-7**,
attention et sortie groupée à **0,99999** de corrélation — et cette comparaison a
trouvé **trois bugs** qu'aucun test interne n'aurait vus : un `attn_norm` manqué,
un puits mis à l'échelle, et la **mauvaise convention RoPE**.

## 1. Pourquoi ces deux couches

`attention.compress_ratios` de V4-Flash : **21 couches CSA** (ratio 4),
**20 couches HCA** (ratio 128), **3 couches brutes** (0, 1, 43). Les couches 0 et
1 n'ont donc **pas** besoin de la compression — ni de P4 ni de P5 — pour être
exécutées et comparées. C'est le seul endroit du modèle où la chaîne complète
(embarquement → hyper-connexions → MLA V4 → puits → dé-rotation → sortie groupée
→ experts → hyper-connexions) peut être validée **avant** d'écrire la
compression.

## 2. Le harnais

| pièce | ce qu'elle fait |
|---|---|
| `--couches a:b` (`Model::load_partiel`) | exécute une **plage** de couches. Le manque « attentions compressées » n'est retiré que s'il ne tombe pas dans la plage, et il est **annoncé** : « le RESTE du modèle reste non implémenté » |
| `DRAVE_DUMP_COUCHES=<préfixe>` | écrit en f32 brut l'état résiduel et les intermédiaires (`hc_attn_pre`, `qr`, `qr_norm`, `q_norm`, `kv_norm`, `attn_derope`, `attn_out`, `l_last`), **par couche et par position** |
| `REF_DUMP=<préfixe>` (dans `tools/ref_logits`) | fait écrire par llama.cpp les **mêmes** tenseurs, en entier (les noms sont ceux des `cb()` du graphe) |
| `tools/compare_etats.py` | compare les vecteurs entiers : écart max, dynamique, **corrélation** |

Le même texte (20 000 octets de WikiText-2) est tokenisé par le tokenizer **du
modèle** (`--tokenize --fichier`), et les identifiants sont donnés tels quels à
llama.cpp : aucune divergence d'entrée possible.

## 3. Résultat

| tenseur | couche | corrélation (4 positions) | écart max |
|---|---|---|---|
| `hc_attn_pre` (mélange des 4 copies) | 0 | **1,000000** | **1,5e-8** |
| `qr` (descente q_a) | 0 | 0,999993 | 1,1e-3 |
| `qr_norm` | 0 | 0,999993 | 6,1e-4 |
| `q_norm` (norme par tête) | 0 | 0,999982 | 3,5e-2 |
| `attn_derope` (sortie d'attention dé-tournée) | 0 | **0,999996** | 1,9e-2 |
| `attn_derope` | 1 | 0,99984 – 0,99999 | 9,5e-2 |
| `l_last` (état après `hc_post`) | 0 | 0,999811 – 0,999959 | 1,7e-2 |
| `l_last` | 1 | 0,999831 – 0,999938 | 2,1e-2 |

**L'écart résiduel est du bruit, pas un biais** : sur les 16 384 valeurs de
`l_last-0`, **49,5 % des écarts sont positifs** (50 % = bruit), la médiane des
erreurs relatives est de **0,1 %**, et l'écart absolu moyen de 1,0e-3 sur une
dynamique de 0,9. C'est la signature de la **quantification des activations de
ggml** (les produits quantifiés de llama.cpp passent les activations en Q8_1),
là où Drave déquantifie exactement et calcule en f32 : Drave est *plus* précis
que la référence, et l'écart ne grandit pas avec la position.

Les hyper-connexions, elles, sont **exactes** (1e-7, soit l'arrondi f32) : de
l'aplatissement `hc × h` à la norme RMS sans poids, aux 24 mélanges, aux trois
groupes `pre`/`post`/`comb`, au Sinkhorn à 20 itérations.

## 4. Les trois bugs, et comment ils ont été trouvés

1. **`attn_norm` manqué.** L'attention V4 recevait le mélange **avant** sa
   normalisation, alors que la référence enchaîne `hc_attn_pre` → `attn_norm` →
   attention. Corrélation `qr` **0,99866 → 0,999993**. Un écart « presque
   juste » : c'est le pire, il ne se voit pas à l'œil.
2. **Le puits mis à l'échelle.** `ggml_soft_max_ext(kq, mask, kq_scale)` applique
   l'échelle aux **scores**, puis `ggml_soft_max_add_sinks(kq, sinks)` ajoute le
   puits **brut**. Drave le multipliait par `1/sqrt(head_dim)` : la sortie
   divergeait **dès la position 0**, où l'attention est pourtant triviale — un
   écart qui n'attend pas la longueur est un écart de formule, pas
   d'accumulation.
3. **La convention RoPE.** V4 est en `LLAMA_ROPE_TYPE_NORM` (paires
   `(2i, 2i+1)`), alors que GLM et Kimi — les deux modèles MLA qui marchaient
   déjà — sont en `NEOX` (paires `(i, i + n_rot/2)`). Les deux conventions
   coïncident **à la position 0** (rotation identité) et divergent ensuite :
   position 0 juste, position 1 fausse de 30 %. `rope_norm` et son inverse
   (dé-rotation) sont maintenant dans le moteur, et le commentaire dit pourquoi
   les deux existent.

## 5. Ce que la porte ne dit pas encore

- Les couches 2 à 42 ne sont pas exécutées : il leur faut P4 (HCA) et P5 (CSA +
  indexeur).
- La **fenêtre glissante** (`sliding_window` 128) et la « queue » de l'attention
  brute (`build_raw_tail`) n'ont pas d'effet à 4 positions ; elles devront être
  traitées au-delà de 128 jetons, et c'est écrit ici pour ne pas l'oublier.
- Le **cache KV quantifié** n'est pas exercé ici (32 bits).
- La comparaison porte sur 4 positions et 2 couches : c'est une porte de
  correction, pas une validation du modèle.

## 6. Référence externe, mesurée au passage

llama.cpp sur V4-Flash, mêmes identifiants, 4 jetons :
**NLL moyenne 11,077944 · perplexité 64 727,68**. C'est le chiffre auquel la
perplexité de Drave devra se comparer quand le modèle tournera en entier (P6) —
et il remplace celui qui circulait (11,737136 / 125 133), mesuré sur un autre
découpage.
