# P4 — le compresseur HCA de DeepSeek-V4, validé contre llama.cpp

**En une ligne** : la couche 3 de V4-Flash (première couche **compressée**, ratio
128) tourne et **concorde avec llama.cpp** — corrélation **0,999992** sur la
sortie d'attention au 128ᵉ jeton, c'est-à-dire **au premier bloc compressé
complet** — et cette validation a trouvé **un quatrième bug** : la dé-rotation
utilisait la base RoPE des couches brutes au lieu de celle des couches
compressées.

## 1. Ce qu'est HCA (ratio 128), d'après la référence

`attention.compress_ratios` de V4-Flash : 21 couches **CSA** (ratio 4), 20
couches **HCA** (ratio 128), 3 brutes (0, 1, 43). HCA est le régime simple :

1. Chaque jeton produit une **valeur** (`attn_compressor_kv`) et une **porte**
   (`attn_compressor_gate`) de 512 dimensions.
2. À la porte s'ajoute une **`ape`** — une ligne apprise par rang dans le bloc
   (`pos % ratio`), de forme `[512, 128]`.
3. Quand un bloc de 128 jetons est complet, chaque **canal** fait son propre
   softmax sur les 128 portes, et la clé du bloc est la somme pondérée des 128
   valeurs de ce canal. Ce n'est donc pas un résumé scalaire : c'est un résumé
   **par dimension**.
4. La clé du bloc est normalisée (RMS), puis tournée à la position de son
   **premier** jeton (`compress_rope_freq_base` = 160 000, pas 10 000).
5. L'attention d'un jeton voit **la fenêtre brute** (`sliding_window` = 128) et
   **tous les blocs complets** : `n_visible = (pos + 1) / ratio`, ce qui veut
   dire qu'un bloc n'est visible qu'une fois terminé.

## 2. Résultat

Couche 3, état d'entrée **injecté** depuis llama.cpp (`l_last-2`, via
`DRAVE_ETAT_ENTREE`) pour isoler la couche :

| tenseur | pos 0-3 (aucun bloc) | pos 127-131 (bloc 0 visible) |
|---|---|---|
| `hc_attn_pre` | 1,000000 (1e-5) | **1,000000** (1e-5) |
| `attn_derope` | 0,99999 | **0,999992 – 0,999994** |
| `l_last` | 0,99998 – 0,999999 | **0,99997 – 0,999991** |

La position 127 est celle du **dernier jeton du premier bloc** : à partir de là,
`n_visible` passe à 1 et l'attention utilise réellement le bloc compressé. Que
les cinq positions 127-131 concordent prouve trois choses à la fois : la
compression est juste, la **fenêtre** est juste (sinon le nombre de clés serait
faux), et le **masque** est juste (un bloc n'apparaît qu'une fois complet).

L'écart résiduel (0,02 sur une dynamique de 6,5, soit 0,3 %) est du même ordre
que partout ailleurs : la quantification des activations de ggml.

## 3. Le quatrième bug : la base de la dé-rotation

`attn_derope` était faux de 10 % dans ses **64 dernières dimensions** (la partie
tournée) alors que les **448 premières** (nope) étaient justes à 0,4 %. Signature
trompeuse : la corrélation globale restait à 0,996, donc « plausible ».

La cause : la dé-rotation (`ggml_rope_ext_back`) appelait `m.rope_base`
(10 000, la base des couches **brutes**) au lieu de la base **compressée**
(160 000). Une rotation et sa dé-rotation doivent partager la même base — sinon
on « dé-tourne » d'un angle qui n'a jamais été appliqué.

Ce que ça a coûté à voir, et ce qui l'a montré :
- la comparaison par **régions** (nope contre rope) a localisé l'écart, que la
  corrélation globale cachait ;
- puis un test de **réversibilité** (`rope_norm` puis son inverse) — six lignes,
  ajoutées depuis : il aurait dit le bug **avant** toute passe de 86 Go.

## 4. Reste à faire (P5)

- **CSA** (ratio 4) : compresseur à **chevauchement** (`build_overlap_…`, lit
  2×ratio jetons), **indexeur** (`ggml_lightning_indexer`, `indexer.proj`,
  `attn_q_b`), sélection de candidats (`candidate_topk_blocks`) et masque
  top-k. Le moteur refuse ces couches explicitement plutôt que de calculer
  faux.
- La « queue » de l'attention brute (`build_raw_tail`) : absente des tenseurs de
  V4-Flash, à vérifier si un modèle la déclare.
- Le cache d'état incrémental du compresseur (ici recalculé par bloc) : c'est une
  optimisation de vitesse, pas de justesse — à mesurer avant d'y toucher.
