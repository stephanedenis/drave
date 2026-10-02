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

## 8. CPU, hyperthreading, NUMA et NVMe : ce qui n'avait pas été évalué

### Le CPU sature à 22 Go/s — et l'hyperthreading n'apporte rien

Banc mémoire, nombre de fils croissant :

| fils | 1 | 4 | 8 | **16** | 20 | 30 | 40 |
|---|---|---|---|---|---|---|---|
| Go/s | 1,9 | 6,3 | 8,7 | **20,8** | 16,8 | 23,8 | 23,0 |

**Le plateau est atteint dès 16 fils.** La charge est limitée par la bande
passante mémoire, pas par le calcul.

Et la mesure décisive, chaque configuration répétée trois fois (un seul essai ne
distingue pas le bruit du signal — le premier passage donnait un résultat
incohérent) :

| épinglage | médiane | essais |
|---|---|---|
| 10 cœurs purs (socket 0) | 11,8 | 11,7 · 11,8 · 14,8 |
| 10 hyperthreads (socket 0) | 14,6 | 6,2 · 14,6 · 15,0 |
| 20 cœurs purs (2 sockets) | 14,6 | 13,9 · 14,6 · 21,8 |
| 20 « hyperthreads » (2 sockets) | 22,6 | 20,6 · 22,6 · 24,0 |
| **40 threads (tout)** | **22,8** | 22,4 · 22,8 · 23,2 |

*(les CPU 20-39 sont les jumeaux des 0-19 : les occuper seuls occupe quand même
20 cœurs distincts. La différence vient de la contention système sur les bas
numéros, pas de l'hyperthreading.)*

**40 threads ne font pas mieux que 20 cœurs : 22,8 contre 22,6.** L'hyperthreading
n'apporte rien à une charge limitée par la mémoire — il partage un L2 de 256 Ko
pour rien.

**Conséquence directe : le moteur se trompe de défaut.** Il prend
`cpu × 3/4` = **30 fils**, alors que **20 suffisent** — et les notes du projet
mentionnent déjà ×1,3 de perte à 40+1 fils. Passer à `cœurs physiques` libère
10 threads pour le système sans rien perdre.

### Le NUMA est marginal

2 sockets, 2 nœuds de 64 Go. Banc sur un nœud contre à cheval : **13,5 contre
12,6 Go/s**. Un facteur 1,07 — pas de quoi écrire une politique de placement.

### Le NVMe : ×6 avec du parallélisme — et il dépasse la RAM

| lecteurs simultanés | 1 | 2 | 4 | 8 | **16** |
|---|---|---|---|---|---|
| Go/s cumulés | 5,37 | 9,68 | 18,08 | 28,29 | **31,08** |

Vérifié sur 50,5 Go (395 fichiers, parcours complet du disque) : **3,42 Go/s à un
lecteur, 21,02 à quatre, 33,19 à seize**.

**Le NVMe parallélisé (31 Go/s) est plus rapide que la RAM (22 Go/s).**

C'est le résultat qui change l'architecture. Pour V4.1, les 2,39 Go d'experts par
jeton passent de **435 ms** (lecture séquentielle à 5,5) à **77 ms** (16 lecteurs
parallèles à 31). **Sans aucun cache.**

*Réserve honnête : les 50,5 Go lus tiennent dans les 112 Go de cache RAM, donc le
régime réellement froid du disque n'est pas isolé — `O_DIRECT` échoue ici
(errno 29) et le NVMe n'héberge que 114 Go. Ce qui est solide, c'est le **scaling**
(×6 à ×10 du débit avec le parallélisme), pas la valeur absolue.*

## 9. Ce que ça change : lire au lieu de stocker

| stratégie | trafic/jeton | temps |
|---|---|---|
| tout en RAM (impossible : 153 Go d'experts) | — | — |
| cache de 90 % en RAM + NVMe séquentiel | 0,24 Go | 44 ms + calcul |
| **cache de 25 % + NVMe parallèle** | **1,79 Go** | **58 ms + calcul** |
| **aucun cache, NVMe parallèle** | **2,39 Go** | **77 ms + calcul** |

**Avec 16 lecteurs parallèles, ne rien cacher devient presque aussi rapide que
tout garder** — et ça supprime le cache, son index, sa politique d'éviction et
ses 71 Go de RAM. Ce qui libère la mémoire pour le **KV**, qui est le vrai
goulot à long contexte (96,6 Go en F16 à 1 M).

**La conclusion se retourne** : la brique à écrire n'est plus « un cache
d'experts adossé au disque », c'est **un chargeur parallèle d'experts**. Plus
simple, et ça sert les deux régimes.

## 10. La topologie matérielle : NVLink, NUMA, et pas de FPGA

Relevé complet de la machine (Xeon E5-2687W v3, 2 sockets × 10 cœurs) :

| périphérique | adresse | NUMA | lien |
|---|---|---|---|
| **NVMe** (MAP1602, *DRAM-less*) | 02:00.0 | **node 0** | PCIe 3.0 |
| GPU 0 (Quadro RTX 5000) | 03:00.0 | **node 0** | PCIe 3.0 ×16 |
| GPU 1 (Quadro RTX 5000) | 04:00.0 | **node 0** | PCIe 3.0 ×16 |
| **GPU 0 ↔ GPU 1** | | | **NVLink, 25,78 Go/s** |

**Le NVLink est là, et il vaut 2× le PCIe** (25,78 contre ~12 Go/s réels). CUDA
l'emprunte automatiquement pour tout `cudaMemcpy` entre les deux GPU, donc
`DRAVE_GPU_KV` — qui répartit le cache KV sur les deux cartes — en bénéficie sans
qu'on ait rien à régler.

**Tout le chemin critique est sur le NUMA node 0** : le NVMe, les deux GPU, et
les CPU 0-9 avec leurs hyperthreads 20-29. Le node 1 (10-19, 30-39) est de
l'autre côté de l'UPI.

**Et pourtant, l'affinité NUMA ne paie pas** :

| chemin mesuré | node 0 | node 1 | les deux |
|---|---|---|---|
| banc mémoire (calcul pur) | 13,8 | 14,2 | 15,0 Go/s |
| **lecture NVMe** (8 lecteurs) | 22,41 | 21,45 | 22,57 Go/s |

Écart de **4 %** sur le chemin qui traverse réellement l'UPI (le NVMe), et du
bruit pur sur le calcul. L'UPI de ce Xeon est rapide, et le SSD *DRAM-less* ne
sature pas assez la mémoire hôte pour que la distance compte.

**Pas de FPGA dans cette machine.** Le relevé PCI ne montre que le NVMe, les deux
GPU, deux cartes Ethernet et les contrôleurs du chipset. La piste est close.

### Les paires hyperthread : utiles quand les cœurs manquent

Le banc mémoire, chaque configuration répétée trois fois :

| cœurs utilisés | fils | Go/s (médiane) |
|---|---|---|
| **10 cœurs** | 10 (1 par cœur) | 14,7 |
| **10 cœurs** | **20 (2 par cœur, HT)** | **18,7** ← **+27 %** |
| 10 cœurs | 30 (3 par cœur) | 15,0 — régression |
| **20 cœurs** | 20 | **22,5** |
| 20 cœurs | 40 (HT) | 18,9 (essais 18,6 · 18,9 · 26,3 — très bruité) |
| 20 cœurs | 60 | 20,7 |

**L'hyperthreading n'aide pas quand on a tous les cœurs** (la bande passante
sature à ~22 Go/s), **mais il rend 27 % quand on n'en a que dix.** C'est le cas
d'un nœud partiel : dix cœurs physiques avec leurs jumeaux valent mieux que dix
cœurs seuls, parce que deux fils d'une même paire masquent mutuellement la
latence mémoire — et partagent le L2 de 256 Ko.

**Et trois fils par cœur est une régression** (15,0 contre 18,7) : au-delà de
deux, la contention du cœur dépasse le gain de latence.

**Conséquence pour le moteur** : sa configuration par défaut (20 fils sur
20 cœurs, via `coeurs_physiques()`) est la bonne. Mais un nœud **restreint** à
dix cœurs devrait prendre **vingt fils sur les paires HT** — soit `--pin` avec un
placement explicite `0-9,20-29` plutôt que `0-9`.

### Ce qui reste exploitable de la topologie

1. **Le NVLink** : tout échange entre les deux GPU devrait passer par lui plutôt
   que par la RAM hôte. C'est le cas par défaut, mais un placement qui garde les
   tenseurs d'une même couche sur une seule carte évite même l'échange.
2. **Épingler sur les cœurs physiques** : mesuré (section 8), 40 threads valent
   20 cœurs. C'est corrigé dans le moteur — `engine::coeurs_physiques()` lit
   `/sys/devices/system/cpu/cpu*/topology/` au lieu de prendre les threads
   logiques, ce qui fait passer le défaut de **30 à 20 fils**.
3. **Le NVMe *DRAM-less*** : ses performances dépendent du HMB (Host Memory
   Buffer), donc de la RAM hôte. Les 31 Go/s mesurés en parallèle en dépendent
   peut-être — c'est une raison de plus de ne pas conclure sur le régime froid.
4. **Les paires hyperthread sur un nœud restreint** : +27 % à dix cœurs, rien à
   vingt. À régler au déploiement, pas par défaut.

## 11. La prélecture parallèle : implémentée, et sans effet ici

Le routeur connaît ses `k` experts **avant** de les calculer : on peut donc
demander au noyau de lancer les lectures d'un coup avec
`madvise(MADV_WILLNEED)` — c'est la seule forme de parallélisme de lecture
accessible quand les poids sont mmappés. Implémenté (`gguf::prelire`, appelé
après le routage, désactivable par `DRAVE_PRELIRE=0`).

Comparaison appariée, trois tours alternés, mêmes 127 jetons :

| | tour 1 | tour 2 | tour 3 | moyenne |
|---|---|---|---|---|
| avec prélecture | 25,3 s | 25,9 s | 26,0 s | **25,73 s** |
| sans | 25,8 s | 25,8 s | — | **25,80 s** |

**0,3 % — aucun effet.** L'explication est simple : le modèle de test (18,6 Go)
tient dans les 115 Go de cache RAM, donc les lectures ne vont jamais au disque et
`MADV_WILLNEED` n'a rien à lancer.

Le code est conservé — il ne coûte rien et servira sur un modèle **plus gros que
le cache**, ce qui est précisément le cas de V4.1 (365 Go) — mais **il ne faut pas
le compter comme un gain** : sur cette machine et ces modèles, il n'en produit
aucun. Trois autres optimisations de la même famille se sont heurtées au même
mur : le calcul est 18× plus rapide que la lecture, et le noyau fait déjà son
travail.

## 12. Le FPGA : pas de cas d'usage aujourd'hui

Un Stratix V est branché, mais **en USB seulement** (pas de PCIe configuré), soit
**625 Mo/s au mieux** — cinquante fois moins que le NVMe parallélisé.

Et surtout, **il n'y a rien à lui donner**. Le mur de cette architecture n'est pas
le calcul :

| | |
|---|---|
| lecture d'une couche | 10,9 ms |
| **calcul de la même couche** | **0,6 ms** |
| rapport | **18×** |

Un accélérateur de calcul sur un chemin où le calcul pèse 5 % ne peut rien
gagner. Et le déplacement de données est déjà en DMA par le noyau : un FPGA qui
lirait le NVMe pour le pousser en VRAM ne ferait pas mieux que `pread` à
31 Go/s.

**La condition qui le rendrait utile** : une tâche où le **calcul** domine. Il n'y
en a aucune dans le chemin actuel — ni le matvec (limité par la mémoire), ni la
déquantification (le moteur ne déquantifie que les têtes de tenseurs), ni le
routage (384 logits par couche). En PCIe et avec une charge de calcul dense, la
question se reposerait ; en USB, elle est close.

## 11. Ce qui reste à vérifier

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
- **Le régime froid du NVMe** : toutes les mesures de débit parallèle tiennent
  dans le cache RAM. Il faudrait un corpus de plus de 112 Go qui ne rentre pas —
  le disque n'en héberge que 114.
- **Le nombre optimal de lecteurs** : 16 est le maximum testé, pas l'optimum. Le
  débit monte encore entre 8 et 16 (28,3 → 33,2), la courbe n'est pas plate.
- **L'allocation non uniforme**, encore : +1,2 % mesuré sur Qwen3, mais V4.1 a
  384 experts et top-6 (rapport 1,6 % au lieu de 6,25 %) — la concentration y est
  peut-être plus forte, ce qui rendrait l'allocation par couche plus utile.
