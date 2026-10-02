# Rapport — détection matérielle et configuration automatique

Session du 01/10 au 02/10. Ce qui a été **implémenté**, ce que chaque heuristique
s'appuie comme mesure, et ce qui a été retiré après essai.

## Le module `materiel.rs`

`Materiel::detecter()` lit la machine sans charger de modèle :

| quoi | comment | pourquoi pas autrement |
|---|---|---|
| **cœurs physiques** | `/sys/devices/system/cpu/cpu*/topology/{core_id,physical_package_id}` | `available_parallelism` rend 40 threads logiques pour 20 cœurs |
| **paires hyperthread** | regroupement par `(paquet, cœur)` | il faut savoir quels threads partagent L1/L2 |
| **nœuds NUMA** | `/sys/devices/system/node/node*` | mémoire par nœud incluse |
| **caches** | `cpu0/cache/index*/{level,type,size}` | — |
| **GPU** | `nvidia-smi --query-gpu` | le pilote CUDA n'est ouvert que si on en a besoin |
| **NVLink** | `nvidia-smi nvlink -s` | 25,8 Go/s, 2× le PCIe |
| **RAM** | `/proc/meminfo` | — |
| **disques** | `df` + `findmnt` → périphérique bloc → `numa_node` | attribuer le nœud du premier NVMe à tous les disques donnait « nœud 0 » au disque mécanique, qui n'en a pas |

`--materiel` affiche le tout **et le plan**, chaque ligne portant son chiffre.

## Les heuristiques, et la mesure qui les justifie

### Threads = cœurs physiques

| configuration | Go/s |
|---|---|
| 20 cœurs | **22,5** |
| 20 cœurs + hyperthreads (40 fils) | 18,9 |
| 10 cœurs | 14,7 |
| **10 cœurs + leurs hyperthreads** | **18,7** (+27 %) |
| 10 cœurs, 3 fils par cœur | 15,0 — régression |

Au-delà des cœurs physiques, la bande passante sature. **Sauf** quand on n'en a
que dix : là, les jumeaux rendent 27 %. D'où deux règles :

- défaut : `threads = cœurs physiques` — le moteur prenait `cpu × 3/4` = **30**
  fils sur 40 threads logiques, il en prend **20** ;
- si la machine a moins de 8 cœurs : épinglage sur les **paires hyperthread**.

### Lecteurs disque = 16

| lecteurs simultanés | 1 | 2 | 4 | 8 | **16** |
|---|---|---|---|---|---|
| Go/s | 5,37 | 9,68 | 18,08 | 28,29 | **31,08** |

Vérifié sur 50,5 Go (parcours complet du disque) : 3,42 / 21,02 / 33,19. **Le
NVMe parallélisé dépasse la RAM** (31 contre 22 Go/s).

### Cache KV : f32 tant qu'il tient, int8 au-delà

Le seuil est **un tiers de la RAM libre** — un tiers et pas la moitié, parce que
les experts et le commun doivent tenir aussi.

Mesuré : le KV de MLA de V4.1 pèse **90 Ko par jeton en F16**, soit 96,6 Go à 1 M
— plus que les 71 Go d'experts. En int8, 48,3 Go.

Vérifié en vrai sur Qwen3-30B :

```
ctx 4096   : [config] cache KV : 32 bits, 0.20 Go pour 4096 jetons
ctx 262144 : [config] cache KV en int8 : 51.5 Go en f32 pour 262144 jetons,
             soit plus du tiers de la RAM libre (116 Go) — DRAVE_KV_BITS pour forcer
```

### Cache d'experts VRAM : ce que la carte peut donner

`VRAM libre − 2 Go de réserve CUDA − le commun`. La VRAM lit à 84,9 Go/s contre
22,5 pour la RAM.

## Ce qui a été mesuré puis retiré

**La prélecture parallèle** (`madvise(MADV_WILLNEED)` après le routage) :
implémentée, comparée en apparié sur trois tours alternés — **25,73 s avec,
25,80 sans, soit 0,3 %**. Le modèle de test tient dans le cache RAM, donc les
lectures ne vont jamais au disque. Le code est conservé (inoffensif, et utile sur
un modèle plus gros que le cache) mais **ne compte pas comme un gain**.

**La tête à restriction garantie** : trois voies explorées, aucune ne tient. La
borne de Cauchy-Schwarz ne conclut jamais, et la sparsité de l'entrée détruit le
modèle (densité 5,1 % ⇒ perplexité ×107). Détail dans
[`rapport-tete-restreinte.md`](rapport-tete-restreinte.md).

## Ce qui est mesuré puis **gardé**, avec son avertissement

**`--tete-restreinte`** : +10,5 % (liste française) à +15 % (anglaise), mais la
sortie **change**. Ce n'est pas une optimisation, c'est une **génération
contrainte**. Refusée en perplexité (une perplexité calculée sur un vocabulaire
restreint n'est comparable à rien), et le refus est explicite.

## Les compteurs de densité

`TETE_ACTIFS / TETE_TOTAL / TETE_APPELS` : trois `fetch_add` par appel de tête,
gratuits, et ils ont servi à trancher la voie 3. Conservés.

## État du dépôt

35 tests verts (3 nouveaux sur la détection), portes **Qwen 19,3885** et
**clusters 799,8557** inchangées, génération identique au token près.
