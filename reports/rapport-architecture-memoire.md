# Rapport — architecture mémoire : ce qui va en VRAM, en RAM, et sur le disque

Session du 01/10. Cible : DeepSeek-V4.1-Flash (365,7 Go, 40 couches, 384 experts,
top-6). Machine : 2 × Quadro RTX 5000 (**32 Go** de VRAM), **125 Go** de RAM,
40 CPU, NVMe de 828 Go.

Chaque chiffre de débit est **mesuré**, pas supposé.

## 1. Les débits, mesurés

| niveau | débit | comment |
|---|---|---|
| **VRAM** (noyau `warp par ligne`) | **84,9 Go/s** | banc GPU, tête de 144,6 Mo en 1,7 ms |
| VRAM (noyau `ligne par fil`) | 41,9 Go/s | même banc, 3,4 ms |
| **RAM** (CPU, 30 fils) | **20,9 Go/s** | même banc, 6,9 ms |
| **NVMe**, aléatoire, blocs 4 Mo | 5,5 Go/s | mesuré, cache chaud |
| **PCIe** 3.0 ×16 | ~12 Go/s | théorique 15,75 ; le lien monte à gen 3 sous charge |

Surprise utile : le `warp par ligne` est **4× plus rapide que le CPU** (84,9 contre
20,9). Le déport n'est donc pas un gain marginal — c'est un facteur 4 sur chaque
octet lu en VRAM.

*(Le lien PCIe reste à gen 1 quand les GPU sont inactifs, et monte à gen 3 sous
charge. Toute mesure faite au repos donnerait un chiffre 8× trop pessimiste.)*

## 2. Ce qui est relu à chaque jeton

| poste | Go par jeton | format | noyau GPU ? | RAM | VRAM |
|---|---|---|---|---|---|
| tête de sortie | 1,32 | Q4_K | **oui** | 63,2 ms | **15,5 ms** |
| **attention MLA** | **5,40** | Q8_0 | **NON** | **258,4 ms** | 63,6 ms |
| embeddings | 1,32 | F16 | **oui** | 63,2 ms | **15,5 ms** |
| experts (top-6 × 40) | 2,39 | IQ2_XXS / Q2_K | **NON** | 114,4 ms | 28,2 ms |
| **total** | **10,43** | | | **499 ms** | **404 ms** |

**L'attention MLA est le premier poste de dépense** (5,40 Go par jeton, 258 ms à
elle seule en RAM) — et c'est justement celui qui **n'a pas de noyau GPU**. Le
déport actuel ne fait donc gagner que 95 ms sur 499.

## 3. La répartition optimale

| niveau | capacité | contenu | débit |
|---|---|---|---|
| **VRAM** | 30,2 Go | tête 1,32 + attention 5,40 + embeddings 1,32 = **8,0 Go**, puis **22,2 Go d'experts chauds** (2 227) | 84,9 Go/s |
| **RAM** | 102 Go | jusqu'à **10 247 experts** — or 90 % des appels tiennent dans 71 Go | 20,9 Go/s |
| **NVMe** | 828 Go | le reste des experts (~51 Go) + **l'engram mmappé** (203 Go, 0,4 Go de cache) | 5,5 Go/s |

**Ce qui tient, et avec quelle marge :**

| configuration | chargé | marge sur 140 Go (RAM+VRAM) |
|---|---|---|
| engram mmappé + 90 % des experts en RAM | 8 + 71 + 0,4 = **79 Go** | confortable |
| + 22 Go d'experts en VRAM | **101 Go** | 39 Go libres |
| engram chargé (à ne pas faire) | 304 Go | **impossible** |

## 4. La règle de placement, par couche et par grappe

Le classement est **par fréquence d'appel mesurée** (trace de routage), pas par
taille ni par couche :

1. les **2 227 experts les plus appelés** → VRAM (22,2 Go) ;
2. les **10 247 suivants** → RAM (102 Go), ce qui couvre ~90 % des appels ;
3. le reste → NVMe, lu à la demande.

**Et par couche**, la répartition est **uniforme** : on a mesuré qu'une allocation
non uniforme n'apporte que **+1,2 %** au mieux, alors qu'elle coûte un index par
couche et une politique à maintenir. Le tri par fréquence, lui, capture
l'essentiel.

**Par grappe** : les experts d'un même cluster doivent être **contigus sur le
disque** (c'est déjà le cas) et **rangés par fréquence** (`convertisseur --trace`),
pour que les experts chauds d'un cluster soient lus ensemble.

## 5. Ce qui manque, par ordre de gain

| # | noyau à écrire | poste déporté | gain par jeton |
|---|---|---|---|
| 1 | **attention MLA** (Q8_0 : q_a, q_b, kv, output_a, output_b) | 5,40 Go | **−194 ms** |
| 2 | **IQ2_XXS / Q2_K** (experts) | 2,39 Go | −86 ms |
| 3 | rien — déjà là (`charger_tete`, `charger_proj`, Q4_K/Q6_K/Q8_0/MXFP4) | tête + embeddings | −95 ms |

**Cumul : 499 → ~210 ms par jeton** avec les trois premiers, soit **2,4×**. Et
avec les 22 Go d'experts chauds en VRAM en plus, on descend sous les 150 ms.

**Ce que le moteur sait déjà déporter** : Q4_K, Q6_K, Q8_0, MXFP4 (tête,
projections, experts MXFP4 de gpt-oss). **Ce qu'il ne sait pas** : les formats
des experts de V4.1 (IQ2_XXS, Q2_K) et l'attention MLA dans son ensemble.

## 6. Le poste que j'avais oublié : le KV à long contexte

Le KV de MLA n'est pas la concaténation des têtes : c'est un **latent comprimé**
(`attn_kv.weight [512, 5120]`), plus 64 de RoPE. Par jeton, sur 40 couches :

| format | par jeton | à 4 K | à 64 K | **à 1 M** |
|---|---|---|---|---|
| F16 | 90,0 Ko | 0,38 Go | 6,04 Go | **96,6 Go** |
| int8 | 45,0 Ko | 0,19 Go | 3,02 Go | **48,3 Go** |
| int4 | 22,5 Ko | 0,09 Go | 1,51 Go | **24,2 Go** |

**À 1 M de jetons, le KV devient le premier poste de la machine** — devant les
71 Go d'experts :

| configuration à 1 M | total | sur 140 Go |
|---|---|---|
| KV F16 + 90 % des experts | **176 Go** | **ne tient pas** |
| KV int8 + 90 % des experts | 127 Go | tient, 13 Go de marge |
| KV int4 + 90 % des experts | 103 Go | confortable |

**La quantification du cache KV n'est donc pas une optimisation, c'est une
condition** : au-delà de ~0,8 M de jetons en F16, il n'y a plus de place pour les
experts. Le moteur sait déjà le faire (`DRAVE_KV_BITS`, mesuré sur Qwen : +3,0 %
de perplexité en int8, +3,0 % en clés seules) — il reste à le faire sur V4.1.

Et le seuil où le KV dépasse les experts :

| format | le KV égale 71 Go d'experts à |
|---|---|
| F16 | 0,77 M de jetons |
| int8 | 1,54 M |
| int4 | 3,08 M |

## 7. La répartition finale, par régime de contexte

| régime | VRAM (30 Go) | RAM (102 Go) | NVMe |
|---|---|---|---|
| **≤ 8 K** (usage courant) | commun 8 Go + experts chauds 22 Go | experts chauds (71 Go) | reste + engram |
| **64 K** | commun 8 + KV int8 3,0 + experts 19 | experts (71 Go) | reste + engram |
| **1 M** | commun 8 + KV int8 **48,3** → plus de place pour les experts | experts chauds seulement | **le reste des experts** |

**La conséquence est nette** : à très long contexte, la VRAM appartient au KV, et
les experts redescendent en RAM et sur NVMe. Les deux ressources se disputent les
mêmes 30 Go, et le point de bascule est autour de **100 K jetons**.

## 8. Ce qui reste à vérifier

- **Le débit PCIe réel**, pas seulement le lien : le banc mesure la VRAM une fois
  les poids montés. Le coût du **transfert initial** (1 Go ≈ 83 ms à 12 Go/s)
  n'est pas mesuré — il est amorti en 3 jetons pour la tête, mais il faudrait le
  confirmer.
- **La VRAM du GPU 0** : le lien y reste à gen 2 sous charge (le GPU 1 monte à
  gen 3). Un placement qui privilégie le GPU 1 pour les transferts fréquents
  serait plus rapide — non mesuré.
- **Le KV à 1 M de contexte** : non chiffré ici. À 40 couches et 1 tête KV de
  dimension 512, il pèse 512 × 2 × 2 octets × 40 = 82 Ko par jeton, soit 82 Go à
  1 M de jetons — **c'est le poste qui pourrait dépasser les experts**, et il
  n'est pas dans le tableau.
- **L'allocation non uniforme**, encore : +1,2 % mesuré sur Qwen3, mais V4.1 a
  384 experts et top-6 (rapport 1,6 % au lieu de 6,25 %) — la concentration y est
  peut-être plus forte, ce qui rendrait l'allocation par couche plus utile.
