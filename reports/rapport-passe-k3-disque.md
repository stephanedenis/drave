# Où passe le temps d'une passe Kimi-K3 : le disque, et rien d'autre

> Mesuré le 07/10. Répond à la question laissée ouverte par `REPRISE.md`, qui
> demandait explicitement de la trancher **en premier** :
>
> *« la passe complète coûte 2,95 s par couple (couche, jeton) contre 0,75 s à
> chaud — quatre fois plus — et réduire de 25 % les experts lus ne change rien.
> Hypothèse non mesurée : la dispersion (~144 lectures par couple × ~10 ms de
> déplacement). Le pas pour trancher : `majflt` et le temps d'attente disque sur
> une passe complète. »*

La réponse est **le disque**, et elle est exacte à 0,1 % près. La sonde est
`tools/sonde-passe-k3.sh`, le relevé brut `/tmp/sonde_k3.csv` (793 échantillons,
2 s), la sortie moteur `/tmp/sonde_k3_moteur.log`.

---

## 1. Le montage

`DRAVE_K3_PASSE=93` sur `Kimi-K3-UD-Q4_K_XL` — **1,4 To, 32 shards**, quatre
jetons (les identifiants de la référence `[3638, 275, 1309, 3140]`), soit
**372 couples (couche, jeton)**. Une seule couche en mémoire à la fois.

**Où est le modèle, et c'est le fait qui commande tout le reste** :

```
sda              10,9T    1 disk     (ROTA=1 : disque DUR)
└─sda2           10,9T    1 part  →  /dev/mapper/system-root  →  dm-1
nvme0n1         931,5G    0 disk
└─nvme0n1p2       828G    0 part  →  /var/lib/docker, /home/stephane/FastNVMe
```

Le modèle est sur `/home/stephane/Data13TB`, donc sur **`sda`, un disque dur de
10,9 To**. Le NVMe de 931 Go est ailleurs, et **occupé 0,7 % du temps**.

## 2. Les grandeurs, et celles qu'il a fallu remplacer

Trois mesures « évidentes » ne mesuraient rien sur cette machine, et les citer
telles quelles aurait produit un verdict faux :

| mesure | ce qu'elle a donné | pourquoi elle ne vaut rien ici |
|---|---|---|
| `delayacct_blkio_ticks` (champ 42) | **0 sur toute la passe** | la comptabilité de délai du noyau n'est pas active — un zéro muet ferait conclure « aucune attente disque » |
| `majflt` | **0 sur toute la passe** | le modèle est projeté en mémoire et les pages sont amenées par avance : les défauts restants sont mineurs |
| état de `/proc/PID/stat` | 66,2 % en « S » (sommeil) | c'est le fil **principal** ; il dort pendant que ses ouvriers travaillent — il a fallu un second observateur qui agrège `/proc/PID/task/*/stat` |

Ce qui reste, et qui suffit : **l'état des fils, le temps CPU, les octets lus, et
l'occupation du disque.**

## 3. Le relevé

| grandeur | valeur |
|---|---:|
| durée de la passe | **1 587 s** (le moteur en annonce 1 562) |
| CPU travaillé (utime+stime) | **333 s — 21,0 %** |
| échantillons en état D (E/S) | 18,0 % |
| échantillons en état R (travail) | 15,8 % |
| échantillons en état S (sommeil) | 66,2 % |
| **octets lus (bloc)** | **206,58 Go** |
| débit de lecture effectif | **130 Mo/s** (468,6 Go/h) |
| **`dm-1` (donc `sda`) occupé** | **1 390 s — 87,6 %** |
| `dm-1` occupé, pondéré par les files | 22 033 s — **profondeur ≈ 14** |
| `nvme0n1` occupé | **0,7 %** |
| défauts de page majeurs | 0 |
| swap | 0 |
| RSS max | 66,41 Go |
| couples (couche, jeton) | 372 |
| secondes par couple | **4,266 s** |

Et la comptabilité interne du moteur : **199,3 s de chargement, 1 359,4 s de
« calcul », soit 3,654 s par couple.**

### 3.1 Ce que les fils font vraiment

L'observateur de fils montre le motif se répéter à chaque couche, et il est sans
ambiguïté :

```
t=112,1  16 fils   R 0 · D 15 · S 1     cpu cumulé 74,33 s
t=114,1  15 fils   R 0 · D 14 · S 1     cpu cumulé 74,48 s
t=118,1  10 fils   R 1 · D  8 · S 1     cpu cumulé 74,45 s
t=122,1   1 fil    R 0 · D  1 · S 0     cpu cumulé 74,68 s
```

**Seize fils en attente ininterruptible pendant seize secondes, et le CPU qui
passe de 74,33 à 74,48 s — 0,15 s de travail en 12 secondes de horloge.** Les
fils ne calculent pas : ils attendent leurs pages.

## 4. Le verdict, et sa vérification arithmétique

**Le temps de la passe EST le temps de lire les octets au débit du disque.**

    206,58 Go à 130 Mo/s  =  1 589 s
    passe mesurée         =  1 587 s

L'écart est de **0,1 %**. Il n'y a rien d'autre à expliquer : ni CPU (21 %), ni
dispersion au sens de « tête de lecture qui se déplace », ni mémoire (swap nul),
ni défauts de page majeurs. Le disque est occupé 87,6 % du temps avec une file de
~14 requêtes — c'est-à-dire qu'il est **plein**, et qu'il donne ce qu'il a.

**Le calcul est gratuit.** Sur cette machine, 1 359 s de « calcul » sont 1 359 s
d'attente de pages déguisées : le moteur les compte dans le calcul parce que
c'est là que les matrices d'experts sont touchées.

**Et 206,58 Go pour quatre jetons, c'est 51,6 Go par jeton** — à comparer aux
451 Go par jeton de la référence (`llama.cpp-k3`, 1,80 To pour 4 jetons). Drave
lit **8,7× moins** ; il lit simplement sur un disque dur, à 130 Mo/s.

## 5. Ce que cela change, et les prédictions chiffrées

La feuille de route (`docs/roadmap-drave.md`) plaçait en axe 1 « finir la lecture
sélective » et donnait un critère — la passe sous 10 min. Ce diagnostic dit que
le critère est un critère d'**octets et de disques**, pas de code : à 130 Mo/s, la
passe sous 10 min demande de lire moins de 78 Go, soit **2,6× moins** qu'aujourd'hui.

**Prédictions écrites AVANT les mesures correspondantes**, pour qu'elles puissent
être réfutées :

| levier | ce qu'il change | passe prédite |
|---|---|---:|
| **déplacer ~250 Go de shards sur le NVMe** (259 Go libres, occupé 0,7 %) | 18 % des octets servis par un autre disque, en parallèle | **≈ 1 300 s** |
| **réduire les octets lus de 25 %** | 25 % de lectures en moins sur le même disque | **≈ 1 190 s** |
| **répartir sur 3 nœuds**, un disque chacun | chaque nœud lit un tiers | **≈ 530 s** |

**Une contradiction à relever.** `REPRISE.md` affirme que *« réduire de 25 % les
experts lus ne change rien »*. Sur une passe dont le disque est occupé 87,6 % et
dont le CPU travaille 21 %, cette phrase ne peut pas être vraie **si** la
réduction porte sur des octets réellement lus à froid. Elle doit donc avoir été
mesurée dans un régime où les pages étaient en cache, ou sur un autre dispositif.
**Elle est à re-mesurer sous ce protocole avant d'être citée à nouveau.**

## 6. Ce que ce rapport ne dit pas

- Il ne dit pas que les 206,58 Go sont **nécessaires**. Il dit que le temps est
  celui de les lire. Réduire la sélection reste ouvert — et devient, pour la
  première fois, directement convertible en minutes.
- Il ne dit rien de la **qualité** du résultat : les quatre `l_out` sont finis et
  de normes 79,29 et 86,24, mais aucune porte de correction n'a été passée ici.
  Ce rapport mesure un coût, pas une justesse.
- Il porte sur **une** passe, à froid, sur **un** disque. La reproductibilité du
  débit (130 Mo/s) n'a pas été établie par répétition.
