# Noyau GPU de scores d'attention — le premier des trois du top-k

**En une ligne** : les scores d'attention se calculent maintenant **en VRAM**, avec
un écart de **1,03e-7** sur la référence CPU et **40× plus vite** à 262 144 clés —
c'est la brique qui manquait pour que le mode creux (`--attn-topk`) cesse de
retomber sur le CPU au long contexte.

## Ce que le noyau fait

`attn_scores` (dans `drave-core/gpu/drave_gpu.cu`) reprend la tuile de clés du noyau
d'attention complet — chargement coopératif de 32 clés, déquantification int8/int4/
f32, produit scalaire par tête de requête — mais **écrit les scores** `rep × n` au
lieu de les consommer dans une softmax en ligne. Une grille de `n_kv × nsplit`
blocs : le découpage en tranches est celui du noyau complet, et c'est lui qui fait
la différence de débit.

`--banc-topk N` compare les deux chemins sur des clés et une requête
déterministes (même générateur que le banc KV), et chronomètre les deux.

## Mesuré

Qwen2.5-0.5B (2 têtes KV × 64, 7 têtes de requête par tête KV), KV int8, un
Quadro RTX 5000 :

| clés | CPU (20 fils) | GPU | accélération | écart relatif |
|---|---|---|---|---|
| 256 | 0,25 ms | 0,07 ms | 3,8× | 1,03e-7 |
| 4 096 | 3,98 ms | **0,14 ms** | **29×** | 1,03e-7 |
| 65 536 | 65,3 ms | 7,4 ms | 8,9× | 1,03e-7 |
| **262 144** | 257,9 ms | **6,36 ms** | **40,6×** | 1,03e-7 |

L'écart est **constant** (mêmes données, même ordre de sommation) : il ne dépend ni
de la longueur ni du découpage, ce qui est exactement ce qu'on demande à un banc
d'exactitude. Le critère du plan (`docs/plan-gpu-topk.md`, étape 1) était 1e-6 : il
est tenu avec un facteur 10.

Le découpage en tranches a été ajouté **après** la première mesure (3,8× seulement) :
avec une grille de `n_kv` blocs, le GPU tournait à 1,2 Go/s, presque au repos. Une
grille `n_kv × nsplit` (une tranche ≈ 256 clés, plafonnée à 128 tranches) donne le
facteur 40 — la même leçon que le noyau d'attention complet, deux ans plus tôt.

## Ce que le banc a attrapé, et que la relecture n'aurait pas vu

Deux bugs, tous les deux au premier essai :

1. **le noyau sortait MANGLÉ** (`_Z11attn_scoresPKvPKfS2_Pfiiiiiif`) : ajouté après
   le bloc `extern "C"` du fichier, il n'était pas trouvé par
   `cuModuleGetFunction` — `CUDA_ERROR_NOT_FOUND` sur les deux cartes, et le banc
   disait « GPU absent » ;
2. **les scores étaient écrits sans l'offset de la tête KV** : chaque bloc écrasait
   la tranche du précédent, écart relatif **1,24**. Le banc l'a dit en une ligne.

## La suite (étapes 2 à 6 du plan)

La **sélection** (noyau 2) : un histogramme par ligne sur les 8 bits de poids fort
des scores transformés en entiers monotones, puis une collecte au-dessus du seuil.
Le présent noyau lui laisse les scores en VRAM ; il reste à écrire la collecte
déterministe (départage par indice) et le banc qui compare l'ENSEMBLE retenu à
celui du top-k CPU — c'est le second critère du plan, et il n'est pas encore tenu.
