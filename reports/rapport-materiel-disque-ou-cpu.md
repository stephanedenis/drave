# Disque ou CPU ? — ce que la mesure dit d'un deuxième NVMe

> Question posée le 03/10 : « est-ce que ça vaudrait la peine d'acheter un 2ᵉ NVMe
> pour le mettre sur le 2ᵉ CPU (chacun son NVMe pour le mmap) ? »
>
> Réponse mesurée : **non, pas pour la vitesse**, parce que le mur est le CPU, pas
> le stockage — y compris sur le seul modèle qui ne tient pas en RAM. Ce rapport
> existe pour que la décision ne repose pas sur une impression.

## 1. La machine, telle qu'elle est

| | |
|---|---|
| CPU | 2 × Intel Xeon E5-2687W v3 @ 3,10 GHz — 2 sockets, 10 cœurs chacun, 40 fils |
| NUMA | node 0 = CPU 0-9,20-29 · node 1 = CPU 10-19,30-39 |
| RAM | 125 Go (≈ 110 Go disponibles, ≈ 95 Go en `buff/cache`) |
| NVMe | **un seul** : Fanxiang S660 1 To, `numa_node = 0`, monté sur `/home/stephane/FastNVMe` (828 Go) |
| « 11 To » | `/home/stephane/Data13TB` — LVM sur **`WDC WD120EFGX` : un disque ROTATIONNEL (ROTA=1)**, 12 To |

Les deux emplacements de modèles ne sont donc pas équivalents : **V4.1 Q2 (341 Go)
est sur le NVMe**, **V4-Flash IQ1_M (82 Go) est sur le disque dur**.

## 2. Le débit réel du NVMe, et ce que le moteur en fait

```bash
dd if=…/DeepSeek-V4.1-Flash-Q2.gguf of=/dev/null bs=1M count=8000 iflag=direct
# 8 388 608 000 octets en 4,247 s → 2,0 Go/s
```

Passe V4.1 Q2, ctx 32, 5 jetons notés, `read_bytes` et CPU échantillonnés toutes
les 2 s (`/proc/<pid>/io`, `/proc/<pid>/stat`) :

| temps | lu sur le disque | CPU cumulé |
|---|---|---|
| 0 → 24 s (chargement) | 5,4 Go | 23 s (≈ 1 cœur) |
| 28 s | 6,8 Go | 104 s |
| 32 s | 8,3 Go | 202 s |
| 36 s | 9,2 Go | 300 s |
| 40 s | 10,3 Go | **398 s** |

**Conclusion : 375 s de CPU en 16 s de mur (23× parallèle) contre ~0,6 Go/s lus —
soit ~30 % du débit du disque.** Le moteur est **borné par le calcul**, pas par les
entrées-sorties, même sur le modèle de 341 Go qu'aucun cache ne peut tenir.

## 3. V4-Flash : le disque ne le voit même plus

`read_bytes = 0` sur un run entier (ctx 32, 93 jetons) : les 82 Go sont en page
cache. Le fichier est sur le disque **dur** ; il n'est lu qu'une fois, au premier
passage après un vidage de cache (~7 minutes à ~200 Mo/s). Un NVMe rapide
n'accélérerait donc **que ce premier passage**.

## 4. Ce qui limite vraiment, et c'est mesuré ailleurs

- Le poste dominant est `proj+mlp` (le produit des experts) : **3 270,65 ms/token**
  sur V4-Flash en scalaire, tombé à **1 070,52 ms/token** par la vectorisation
  AVX2+FMA du produit scalaire (`DRAVE_SIMD_DOT=1`, ×2,06 sur la passe) — un gain
  de **calcul**, sans toucher au disque (`sprints/24`).
- llama.cpp fait la même passe de 1 024 jetons en ~4 minutes là où le moteur est
  encore à des ordres de grandeur au-dessus : l'écart est dans les noyaux et dans
  la mécanique des blocs compressés, pas dans le stockage.
- Les deux verdicts négatifs déjà consignés vont dans le même sens : le **cache RAM
  d'experts** est plus lent (+4 % à 4 Go, +21 % à 32 Go) et l'**épinglage NUMA**
  a été mesuré perdant. Les jeux mémoire ne paient pas ici ; le calcul paie.

## 5. « Chacun son NVMe pour le mmap » : ce que ça veut dire techniquement

Un `mmap` porte sur **un** fichier, servi par le système de fichiers d'**un**
périphérique : deux disques ne peuvent pas servir le même `mmap`. Pour que
« chacun son disque » ait un sens, il faut **deux fichiers** et **deux processus** —
c'est-à-dire le découpage que le dépôt implémente déjà :

- `commun.gguf` + `cluster-XX.gguf` (86,9 Go, 11 008 entrées de mapping, aucune
  requantification) ;
- `--ppl-reparti` entre deux nœuds, écart mesuré **0,00e0** (`tools/porte-flux.sh`,
  modes exacts), perplexité identique à un nœud unique.

Dans cette configuration, chaque nœud lit **sa** moitié depuis **son** disque et la
garde dans la RAM de **son** socket : c'est le seul montage où un deuxième NVMe
apporte quelque chose — ×2 de bande passante agrégée et de mémoire utile.

## 6. Recommandation

1. **Ne pas acheter pour accélérer les passes actuelles** : le disque est utilisé à
   ~30 %, les modèles qui tiennent en RAM ne le touchent plus, et le facteur
   limitant est le calcul.
2. **Un deuxième NVMe se justifie si** l'objectif devient de faire tourner des
   modèles **plus gros que la RAM** (V4.1 Q2 = 341 Go pour 125 Go de RAM) en
   **deux nœuds**, chacun avec sa moitié sur son disque et son socket. C'est une
   architecture déjà écrite et validée, pas un pari.
3. **Un NVMe se justifie aussi** pour sortir V4-Flash du disque dur (démarrages à
   froid), à condition d'accepter que cela n'accélère que le premier passage.
4. **Avant tout achat** : mesurer le montage à deux nœuds sur V4.1 (≈ 20 min) et
   vérifier que le découpage tient sa promesse sur *ce* modèle, pas seulement sur
   le petit. Un achat se décide sur une mesure, pas sur une intuition de topologie.
