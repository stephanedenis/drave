# Noyau GPU de scores d'attention — le premier des trois du top-k

**En une ligne** : les scores d'attention se calculent maintenant **en VRAM**, avec
un écart de **1,6 à 2,3e-7** sur la référence CPU et **40× plus vite** à 262 144 clés —
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
> ⚠️ **Correction du 30/09 (même journée)** : les écarts de 1,03e-7 ci-dessous ont
> été mesurés avec, pour toutes les positions, **la même clé** — un banc dégénéré
> (voir `reports/rapport-gpu-topk-selection.md`, § « Le banc mentait »). Sur des clés
> distinctes, l'écart relatif est de **1,60e-7 (4 096 clés)**, **2,13e-7 (65 536)** et
> **2,25e-7 (262 144)** : le critère de 1e-6 tient toujours, avec 4× de marge au
> lieu de 10×. Le TEMPS change aussi : la ligne « 65 536 » ci-dessous datait d'AVANT
> le découpage en tranches (7,4 ms, 8,9×) ; re-mesurée après, elle vaut **2,36 ms et
> 26,7×**. Les deux tableaux sont conservés pour la traçabilité.

**Mesure d'origine** (banc dégénéré, avant découpage pour la ligne 65 536) :

| clés | CPU (20 fils) | GPU | accélération | écart relatif |
|---|---|---|---|---|
| 256 | 0,25 ms | 0,07 ms | 3,8× | 1,03e-7 |
| 4 096 | 3,98 ms | **0,14 ms** | **29×** | 1,03e-7 |
| 65 536 | 65,3 ms | 7,4 ms | 8,9× | 1,03e-7 |
| **262 144** | 257,9 ms | **6,36 ms** | **40,6×** | 1,03e-7 |

**Re-mesure du 30/09 au soir** (clés distinctes, banc corrigé — c'est CE tableau
qu'il faut citer) :

| clés | CPU (20 fils) | GPU | accélération | écart relatif |
|---|---|---|---|---|
| 4 096 | 3,88 ms | **0,12 ms** | **31,6×** | 1,60e-7 |
| 65 536 | 63,06 ms | **2,36 ms** | **26,7×** | 2,13e-7 |
| **262 144** | 243,82 ms | **6,09 ms** | **40,0×** | 2,25e-7 |

L'écart est **constant** (mêmes données, même ordre de sommation) : il ne dépend ni
de la longueur ni du découpage, ce qui est exactement ce qu'on demande à un banc
d'exactitude. Le critère du plan (`docs/plan-gpu-topk.md`, étape 1) était 1e-6 : il
est tenu avec un facteur 4.

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

La **sélection** (noyau 2) : quatre passes d'histogramme par ligne sur les octets
des scores transformés en entiers monotones, une descente des seaux côté hôte, puis
deux noyaux de collecte. Elle est **faite** et mesurée depuis : ensemble retenu
identique au CPU sur 14/14 lignes à toutes les tailles testées —
`reports/rapport-gpu-topk-selection.md`. Reste le noyau 3 (softmax sur les k et
somme pondérée des V), puis le branchement dans `model.rs`.
