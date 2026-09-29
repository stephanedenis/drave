# Préremplissage par lots : ce que le GEMM apporte vraiment

> Chantier 4 du plan de reprise. Le préremplissage est le mur n° 1 du contexte
> long (`docs/contexte-long.md` : 4,5 h à 32 k, 1 234 h à 1 M en séquentiel) : le
> moteur traitait **un jeton à la fois**, donc chaque matrice de poids était relue
> pour chaque jeton.

## 1. Ce qui a été fait

| pièce | rôle |
|---|---|
| `Pool::gemm_dense_i8` | produit matrice-matrice int8 : une tranche de lignes par fil, tout le lot servi par la même lecture de ligne |
| `Pool::gemm_dense_q4` | même chose pour les matrices 4 bits (experts MXFP4 de gpt-oss, Q4_K de Qwen) |
| `Model::forward_lot` | un avant complet pour `t` jetons : projections en lot, attention toujours par jeton (elle est causale), FFN dense en lot |
| **regroupement des experts** | les jetons qui ont choisi le même expert sont traités ensemble : la matrice de l'expert est lue une fois pour le groupe |
| `--lot N` | taille du lot (1 = chemin historique jeton par jeton) |

## 2. Justesse

Trois bogues ont été trouvés par la comparaison au chemin jeton par jeton, tous
invisibles à la compilation :

1. les sorties de q, k et v partageaient un tampon avec des pas différents
   (`n_q` contre `n_kv × dim`) : perplexité mesurée **1 614 183** ;
2. l'entrée de la projection de sortie était dimensionnée sur `hidden`
   (2 880) au lieu de `n_têtes × dim_tête` (4 096) : panique à l'index ;
3. les tampons du lot étaient alloués à chaque couche et à chaque lot.

Et un bogue **latent** du chemin historique, corrigé au passage : le biais de
`ffn_down_exps` était découpé par la largeur d'expert (`n_ff`) au lieu de la
largeur de sortie (`h`). Les deux valent 2 880 sur gpt-oss, donc rien ne se
voyait ; sur Qwen3-MoE (768 contre 2 048) le biais aurait été lu au mauvais
endroit. **Effet mesuré : nul** sur Qwen3-30B-A3B (7,6139 avant comme après — ce
modèle ne déclare pas de biais de descente).

Après correction, les lots donnent la même perplexité que le jeton par jeton :

| modèle | lot 1 | lot 16 |
|---|---|---|
| Qwen2.5-0.5B (dense) | 13,1368 | **13,1359** |
| gpt-oss-120b (MoE, regroupé) | 13,7149 | **13,7205** |

L'écart (6e-5 à 4e-4) est l'**ordre des accumulations flottantes**, pas une
erreur : le noyau somme par ligne entière, le chemin historique par tranches.

## 3. Le débit : mesurer, comprendre, corriger

Première mesure, machine au calme, Qwen2.5-0.5B, 511 jetons notés :

| lot | temps |
|---|---|
| 1 | **16,6 s** |
| 4 | 23,2 s |
| 16 | 20,0 s |
| 64 | 18,1 s |

Le lot était donc **plus lent** que le jeton par jeton, alors que le noyau est
2,4× plus rapide isolément (test unitaire). Diagnostic : dans le noyau, la boucle
des jetons était **à l'intérieur** de la boucle des lignes de sortie, donc chaque
ligne relisait *tout* le lot d'activations (64 × 896 × 4 = 229 Ko) — 4 864
relectures par projection.

Correction : **tuilage** — un groupe de 16 jetons (8 pour le 4 bits) est traité
avant de passer à la ligne suivante, donc les activations du groupe restent en
cache pendant qu'on parcourt les poids. C'est l'arbitrage classique : la ligne est
relue `t / TUILE` fois, mais chaque relecture sert 16 jetons au lieu d'un.

## 4. Le débit, attribué poste par poste

Le profil du chemin par lots (ajouté pour l'occasion : sans lui, aucun poste
n'était chronométré) donne, par jeton, Qwen2.5-0.5B, contexte 512, 16 fils :

| poste | lot 1 | lot 512 | verdict |
|---|---|---|---|
| projections d'attention | 3,05 ms | **1,49 ms** | le GEMM divise par 2 ✓ |
| attention | 4,05 ms | 8,90 ms | **×2,2** ✗ |
| FFN + projection de sortie | 25,31 ms | 20,92 ms | ÷1,2 seulement |
| **somme** | 33,14 ms | 31,31 ms | −5 % |
| tête + échantillonnage | 8,36 ms | 8,75 ms | inchangé (la tête est par jeton) |
| **total** | 41,5 ms | **40,1 ms** | **−3 %** |

Le mécanisme fonctionne — le produit matrice-matrice divise bien par deux le
temps des projections — mais **il ne porte que sur 8 % du coût par jeton**, et
deux postes l'annulent :

1. **l'attention par lots est deux fois plus lente** : elle emprunte le chemin
   par tête, alors que le chemin jeton par jeton utilise le chemin *groupé* qui
   relit les clés une fois par groupe de têtes KV (`rep` = 7 sur Qwen) ;
2. **la tête de sortie reste calculée jeton par jeton** (145 Mo lus par jeton
   pour Qwen 0.5B) : c'est le premier consommateur après le FFN, et il n'est
   même pas dans le lot.

Conclusion, mesurée : pour que le préremplissage par lots tienne ses promesses,
il faut **aussi** (a) passer l'attention par le chemin groupé dans le chemin par
lots, et (b) **traiter la tête comme un GEMM** — même noyau, sortie de
151 936 lignes, trente fois plus de travail que les projections d'attention.
Sans (b), le préremplissage restera dominé par la tête et le FFN.

## 5. Ce que ça change pour le contexte long

Le préremplissage séquentiel coûtait un parcours complet des poids **par jeton**.
Un lot de `t` jetons ne le coûte plus qu'une fois par groupe de 16 (et une fois
par expert et par groupe pour un MoE) : le facteur à gagner est donc de l'ordre
de 16 sur la partie « projections », qui domine le préremplissage. Les chiffres
bout en bout après tuilage sont dans `/tmp/lot_final.log` (mesure machine au
calme, dense et MoE).
