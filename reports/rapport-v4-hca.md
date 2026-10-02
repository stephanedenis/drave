# Les compresseurs de DeepSeek-V4 (HCA et CSA), validés contre llama.cpp

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

## 4. Le compresseur **CSA** (ratio 4), même méthode

CSA fait tout ce que fait HCA, avec deux différences :
1. la fenêtre d'un bloc est **2 × ratio** jetons : la seconde moitié du bloc
   **précédent** puis le bloc courant (chevauchement) ;
2. le projecteur fait **1024** valeurs par jeton, et ses deux moitiés ont deux
   rôles : la première (colonnes 0-511) sert quand le jeton est « contexte
   précédent », la seconde (512-1023) quand il est « bloc courant ».

Résultat sur la couche 2 (première couche CSA), positions 3 à 9, état injecté :
`attn_derope` **0,999990-0,999991**, `l_last` **0,99992-0,999994**.

Deux pièges, tous deux invisibles autrement :

- **Le premier bloc.** Les quatre jetons « précédents » du bloc 0 n'existent
  pas : la référence ajoute une ligne dont la **valeur est nulle mais la porte
  vaut −∞** (`dsv4_append_zero_row(score_state, /*neg_inf=*/true)`), donc leur
  poids de softmax est nul. Mettre 0 laissait ces slots compter dans le
  dénominateur : corrélation **0,989** au lieu de 1,000000 — et **seulement au
  premier bloc**, ce qui rend le symptôme difficile à croire.
- **Les moitiés.** L'hypothèse inverse (précédent = seconde moitié) donne 0,42 de
  corrélation ; « tout première moitié », 0,80. C'est le **bloc 1** qui tranche
  (le bloc 0 ne peut pas : ses jetons précédents sont les slots nuls). Trouver
  l'orientation a demandé de comparer les **états par jeton** — qui, eux,
  concordaient déjà à 0,003 — puis de reconstruire la compression **hors du
  moteur**, en lisant la norme directement dans le GGUF
  (`tools/lire_meta_gguf.py --tenseur`).

## 5. L'indexeur, à son tour validé

L'indexeur (« lightning indexer ») note chaque bloc compressé et n'en garde que
les `indexer.top_k` meilleurs. Ses blocs sont plus étroits — **128** valeurs au
lieu de 512 — mais suivent la même règle de chevauchement que le CSA, et sa
requête descend de `qr_norm` (la requête MLA normalisée) plutôt que de l'état.

Ses **scores** sont comparés à `lid_score_masked` de llama.cpp, mêmes jetons :

| position | blocs | Drave | référence |
|---|---|---|---|
| 4 | 1 | 3,2246 | 3,2279 |
| 7 | 2 | 2,8615 · 3,1334 | 2,8656 · 3,1367 |
| 8 | 2 | 3,1752 · 4,9255 | 3,1756 · 4,9261 |
| 9 | 2 | 3,2338 · 2,9185 | 3,2371 · 2,9270 |

Écart **0,1 à 0,3 %**, du même ordre que partout ailleurs. Le top-k lui-même
(sélection des meilleurs blocs) n'a d'effet qu'au-delà de `indexer.top_k` blocs,
soit 2 048 jetons : en deçà il les garde tous, et c'est ce que ces mesures
montrent. La sélection est implémentée (tri décroissant puis troncature) et le
moteur ne refuse plus au-delà.

## 5.bis Le top-k de l'indexeur, validé sans attendre 2 048 jetons

La sélection des blocs ne change rien tant qu'il y a moins de blocs que son
`top_k` (512) : il les garde tous. La valider demandait donc soit un run de
2 048 jetons (plusieurs heures sur ce modèle), soit de **rendre la sélection
active tout de suite** — en changeant un **entier dans les métadonnées** :

```
deepseek4.attention.indexer.top_k : 512 → 1     (4 octets, aucune weight touchée)
```

Les deux moteurs lisent cette clé au chargement ; à la position 8, deux blocs
existent et **un seul est gardé** — la sélection s'exerce donc dès 10 jetons.

| `l_last-2`, `top_k = 1` | corrélation | écart max |
|---|---|---|
| pos 4 (1 bloc) | 0,999919 | 1,3e-2 |
| pos 8 (**2 blocs, 1 gardé**) | **0,999943** | 1,8e-2 |
| pos 9 (2 blocs, 1 gardé) | **0,999920** | 1,3e-2 |

Même niveau d'accord qu'avec tous les blocs (0,9999x) : la **sélection** est
juste, pas seulement les scores. La perplexité, elle, bouge dans le même sens des
deux côtés (546,3 contre 548,3 chez llama.cpp ; 677,3 contre 678,1 chez Drave).

## 6. Ce qui reste de P5 : l'indexeur

Les couches CSA gardent, en plus des blocs, ceux que l'**indexeur** choisit
(`ggml_lightning_indexer` : `relu(q·k)` pondéré par tête, puis top-k). Tant que
le nombre de blocs compressés reste sous `attention.indexer.top_k` (512), le
top-k les garde **tous** : le résultat est alors exact sans l'indexeur, et c'est
la plage dans laquelle les validations ci-dessus ont été faites (4 × 512 =
2 048 jetons). Au-delà, le moteur **refuse** au lieu de calculer faux.

## 7.bis Un manque trouvé en relisant les métadonnées : le **clamp SwiGLU**

V4-Flash déclare `swiglu_clamp_exp = 10.0` et `swiglu_clamp_shexp = 10.0`,
**couche par couche** — et le moteur ne l'appliquait pas. La référence
(`llama.cpp/src/llama-graph.cpp`) borne les activations d'expert avant le
produit : `gate = min(gate, limite)`, `up = clamp(up, ±limite)`, puis
`silu(gate) · up`. Implémenté (`activation`, troisième régime).

Il ne s'est pas vu dans les validations de couches 0-3 parce que les activations
y restent sous 10 : le clamp n'y change rien. C'est un manque qui ne se serait
manifesté que **plus loin dans le modèle**, sur les jetons où l'activation
dépasse la borne — le genre d'écart qui n'apparaît ni au début ni dans une
corrélation globale.

## 8. Reste à faire

- La **stabilité de la liste de candidats** (recouvrement entre jetons
  consécutifs, périodicité) : c'est la question que la vision pose à ce flux, et
  elle n'a pas encore été posée.
- La « queue » de l'attention brute (`build_raw_tail`) : absente des tenseurs de
  V4-Flash, à vérifier si un modèle la déclare.
- Le cache d'état incrémental du compresseur (ici recalculé par bloc) : c'est une
  optimisation de vitesse, pas de justesse — à mesurer avant d'y toucher.
