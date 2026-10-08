# Ségrégation NUMA : ce que la machine répond

> 08/10. Réponse à une proposition de configuration : *station bi-processeur
> Xeon E5-2687W v3, topologie NUMA asymétrique stricte — nœud 0 pour l'OS et
> l'affichage (CPU 0, 32 Go, NVMe système, GPU AMD), nœud 1 pour le calcul
> (CPU 1, 128 Go, NVMe dédié aux modèles, deux Quadro RTX 5000 sous NVLink),
> l'objectif étant d'éviter tout goulot sur le bus QPI.*
>
> Tout ce qui suit est mesuré, soit sur cette machine le 08/10, soit dans les
> rapports cités. Ce qui est déduit est étiqueté **[déduit]**.

---

## 1. Réponse en trois lignes

1. **Séparer l'OS, le bureau et l'affichage du calcul : bénéfique**, pour la
   reproductibilité des mesures et pour la VRAM rendue au moteur — pas pour le QPI.
2. **Forcer le calcul sur un seul socket : coûteux et mesuré.** +8,1 % sur une
   passe dense (A/B ci-dessous), et **−19 % documenté** sur le MoE 30B
   (`docs/convertisseur.md:192`). La ressource rare n'est pas la liaison entre
   processeurs, c'est la bande passante mémoire d'un socket.
3. **Le goulot réel de Drave n'est ni le QPI ni le CPU : c'est le disque.**
   Mesuré aujourd'hui : **1,6 Go/s** en lecture séquentielle directe sur le NVMe
   contre **246 Mo/s** sur le disque dur `sda` — un facteur 6,5 qui décide d'une
   passe de 26 minutes, pas d'un placement NUMA.

---

## 2. Ce que la machine est aujourd'hui (mesuré)

| | valeur | source |
|---|---|---|
| processeurs | 2 × Xeon E5-2687W v3 · **10 cœurs / 20 threads par socket** | `lscpu` |
| nœuds NUMA | 2 · distances **10 local / 21 distant** (2,1×) | `numactl --hardware` |
| mémoire | **64,3 / 64,4 Go — symétrique** · 132 Go au total | idem |
| page cache | 93 à 111 Go en cache, 23 Go libres | `free` |
| GPU | 2 × Quadro RTX 5000, **les deux sur le nœud 0** (`03:00.0`, `04:00.0`) | `/sys/.../numa_node` |
| NVLink | **25,781 Go/s par sens**, lien 0 sur les deux cartes | `nvidia-smi nvlink -s` |
| NVMe | `nvme0n1`, 931 Go, **nœud 0** — monté `FastNVMe`, **97 % plein (29 Go libres)** | `/sys/block/.../numa_node`, `df` |
| disque dur | `sda`, 10,9 To → montage `Data13TB` (LVM `system-root`) | `lsblk` |
| modèle Kimi-K3 | actuellement sur le **NVMe** (`FastNVMe/k3-nvme/`), pas sur `sda` | `find` |

**Conséquence immédiate** : la proposition déplace les deux Quadro du nœud 0
(leur place actuelle) vers le nœud 1. C'est un changement de câblage, pas de
réglage — et il faut vérifier que chaque carte garde son propre *root complex*.
Aujourd'hui c'est le cas : `03:00.0` est derrière le pont `00:02.0` et `04:00.0`
derrière `00:03.0` (`/sys/bus/pci/devices/*/`), donc deux ports racine distincts
— la bonne disposition pour un tandem.

---

## 3. Pourquoi le QPI n'est pas le goulot — trois mesures

| mesure | écart | source |
|---|---|---|
| calcul pur, nœud 0 vs nœud 1 | 13,8 vs 14,2 Go/s → **3 %** | `REPRISE.md:1523` |
| lecture NVMe, nœud 0 vs nœud 1 | 22,41 vs 21,45 Go/s → **4 %** | `REPRISE.md:1524` |
| **épinglage sur UN socket**, charge réelle (30B MoE) | 23,2 → **27,6 s : −19 %** | `docs/convertisseur.md:192` |

Les deux premières lignes disent que traverser le QPI, quand on le traverse, ne
coûte que 3 à 4 % — l'ordre du bruit de fond de cette machine (le dépôt mesure
jusqu'à 30 % de variation du temps mur selon la charge du bureau). La troisième
dit l'essentiel : **restreindre le calcul à un socket le RALENTIT**, parce qu'on
divise par deux la bande passante mémoire disponible.

C'est contre-intuitif, et le dépôt a les deux faces de la médaille : le banc
mémoire *gagne* à être lié à un socket (20,7 → **24,7 Go/s**,
`docs/convertisseur.md:101`) parce qu'il fait un flux unique, alors que la charge
réelle perd 19 % parce qu'elle a beaucoup de flux simultanés. **Un banc qui ne
ressemble pas à la charge ne décide pas du placement.**

---

## 4. Les trois régimes de Drave, et ce qui limite chacun

| régime | exemple | ce qui limite | chiffre mesuré |
|---|---|---|---|
| **disque** | passe Kimi-K3, 4 jetons | le disque, et rien d'autre | `sda` occupé **87,6 %**, CPU **21 %**, 133 Mio/s contre 205 possibles |
| **mémoire** | passe dense d'un modèle qui tient en RAM | la bande passante mémoire | 20 cœurs = **22,5 Go/s**, + hyperthreads = **18,9** |
| **GPU** | attention et cache KV | la VRAM et le PCIe/NVLink | VRAM **84,9 Go/s** · NVLink **25,78** · PCIe x8 **6,5** |

Le placement NUMA ne parle qu'au deuxième régime. Sur le premier, il ne rapporte
rien (le QPI est au repos) ; sur le troisième, il ne parle pas du tout (les
cartes ont leur propre mémoire).

---

## 5. Ce que la ségrégation apporte réellement

1. **La reproductibilité — le gain le plus solide.** Le dépôt le répète : « la
   machine portait une charge de fond (bureau, autres projets) qui fait varier le
   temps mur de 30 % », et des campagnes entières ont dû être refaites sous
   charge 8-14. Isoler bureau et affichage sur le nœud 0 rend les chiffres
   comparables entre eux.
2. **La VRAM rendue au calcul.** Le plan du moteur dimensionne le cache
   d'experts sur la VRAM **libre** (« 27,8 Go libres moins 2 de réserve CUDA »,
   sortie de `--materiel`). Un GPU d'affichage y prend sa part en permanence.
   Passer l'affichage sur l'AMD est un délestage net.
3. **Le disque dédié aux modèles.** Mesuré aujourd'hui, en lecture séquentielle
   directe (3 Go, `iflag=direct`) :

   | support | débit | conséquences |
   |---|---:|---|
   | `sda` (disque dur, 10,9 To) | **246 Mo/s** | la passe K3 y lit 206,58 Gio → 26,5 min |
   | NVMe `nvme0n1` (nœud 0) | **1 600 Mo/s** | les mêmes octets → **~2,2 min** |

   Le disque, pas le NUMA, décide. **Mais** : le NVMe actuel est plein à 97 %
   (29 Go libres) et Kimi-K3 y est déjà — un « NVMe dédié aux datasets » suppose
   un disque de capacité suffisante, sinon on déplace le problème.

---

## 6. Ce que la ségrégation coûte

1. **La mémoire asymétrique 32/128 Go est le point faible.** Aujourd'hui c'est
   64/64. Toute charge dense forcée sur un socket paie les +8 % (mesuré
   ci-dessous) à −19 % (documenté sur le MoE). Et 128 Go sur un socket n'ont
   d'intérêt que si **les quatre canaux sont peuplés équilibré** — mal peuplés,
   ils donnent moins de bande passante, pas plus.
2. **Le gain de 128 Go est plus petit qu'il n'y paraît.** L'idée serait de garder
   en page cache le **dense de Kimi-K3 (57,93 Gio lus une fois par passe)**. Le
   dépôt a mesuré que **la page cache ne le retient pas** : deux passes
   consécutives ont pris 1 516 430 puis 1 522 584 ms. Plus de RAM, seul, n'achète
   donc pas ce temps-là.
3. **Figer la topologie fige la stratégie.** Drave alterne entre charges disque
   (un socket suffit, et de loin) et charges mémoire (les deux sont nécessaires).
   Une configuration figée « calcul sur le nœud 1 » transforme un choix
   réversible en contrainte permanente.

---

## 7. L'A/B fait sur cette machine (08/10)

Charge réelle : `--ppl` sur Qwen2.5-0.5B Q8_0, 256 jetons, contexte 512.
**Trois répétitions entrelacées** (A, B, C, D, puis on recommence) — c'est la
règle du dépôt : la charge de fond variant de 30 %, une mesure non entrelacée ne
compare rien.

| configuration | rép. 1 | rép. 2 | rép. 3 | médiane | écart |
|---|---:|---:|---:|---:|---:|
| **A** défaut (20 fils, aucune liaison) | 15 729 | 15 108 | 15 365 | **15 365 ms** | — |
| **B** nœud 1 seul (10 fils, mémoire nœud 1) | 16 787 | 16 496 | 16 614 | **16 614 ms** | **+8,1 %** |
| **C** nœud 1 (10 fils), mémoire entrelacée | 16 623 | 16 118 | 16 474 | **16 474 ms** | +7,2 % |
| **D** deux nœuds (20 fils), mémoire entrelacée | 15 225 | 15 307 | 14 774 | **15 225 ms** | −0,9 % |

Lecture : **la proposition B est la plus lente des quatre** ; la dispersion entre
répétitions (jusqu'à 4 %) est plus petite que l'écart entre configurations pour
B, mais pas pour D — d'où la médiane et l'entrelacement.

---

## 8. Recommandations

1. **Garder la mémoire symétrique (64/64).** La moitié des charges n'a besoin que
   d'un socket ; l'autre moitié a besoin des deux. Une asymétrie 32/128 retire
   une capacité sans rien rendre.
2. **Séparer par placement, pas par topologie** :
   - passes **disque** (K3, gros modèles) : un socket et le disque dédié suffisent
     — `numactl --cpunodebind=1 --membind=1`, ou le `--pin` du moteur ;
   - passes **mémoire** (0,5 B à 30 B en RAM) : **laisser les deux sockets** ;
   - et mesurer à chaque fois, parce que le croisement dépend de la charge.
3. **Isoler l'affichage et le bureau** sur le nœud 0 avec le GPU AMD : oui, pour
   la reproductibilité et la VRAM.
4. **Deux Quadro sur le même socket, sous NVLink** : oui — mais vérifier que
   chaque carte garde **son propre root complex** (c'est le cas aujourd'hui :
   `03:00.0` et `04:00.0` sur deux ponts distincts), sinon elles partagent le x8
   (6,5 Go/s mesuré) et le tandem perd son intérêt.
5. **Le disque dédié, oui — dimensionné.** C'est le seul poste où un facteur 6,5
   est disponible aujourd'hui (246 Mo/s → 1 600 Mo/s).
6. **Le levier suivant n'est pas matériel** : le motif d'accès disque laisse
   ~35 % sur la table (133 Mio/s obtenus contre 205 possibles, mesuré).

---

## 9. Réserves

- L'A/B du § 7 porte sur **un** modèle (0,5 B, chemin dense, Q8_0) et **une**
  charge ; la passe K3 (disque) n'a pas été refaite ici — elle dure 26 min par
  configuration, et le protocole est décrit au § 10.
- Les chiffres de `--pin` (−19 %) viennent d'un 30B MoE sur NVMe
  (`docs/convertisseur.md`) ; ceux de bande passante (20,7 → 24,7 Go/s) d'un banc
  mémoire syntétique. Les deux sont du dépôt, pas de la littérature.
- Les débits disque du § 5 sont mesurés **à chaud, sur des fichiers existants**,
  avec `iflag=direct` (donc sans page cache), mais sous la charge de fond du
  moment (bureau, deux entraînements GPU) : c'est un ordre de grandeur, pas un
  plafond constructeur.
- **[déduit]** Le gain d'un NVMe sur le nœud 1 pour les passes disque : le débit
  mesuré est celui du NVMe actuel, sur le nœud 0. Le placement change la latence
  d'accès, pas le débit séquentiel.

---

## 10. Le protocole, si la configuration proposée est retenue

Trois mesures, entrelacées, sur les deux charges qui comptent :

1. **passe K3** (`tools/test-plage-k3.sh`, ou une passe de 4 jetons) :
   (a) configuration actuelle · (b) `numactl --cpunodebind=1 --membind=1` ·
   (c) `--pin` du moteur ;
2. **passe dense** 0,5 B et 30 B : mêmes trois configurations ;
3. **stabilité** : trois répétitions entrelacées par configuration, et l'écart
   entre répétitions rapporté à côté de l'écart entre configurations — sans quoi
   on conclut sur du bruit.

La porte est simple : **une configuration n'est adoptée que si elle gagne sur les
deux charges, ou si le compromis est chiffré et assumé.** Les mesures du § 7
prédisent qu'aucune ne gagne sur les deux.

---

## 11. Second projet : carte 4×NVMe + AMD, RAM inchangée (2×32 + 2×32)

> Configuration annoncée : une carte PCIe 4×NVMe (bifurcation x4x4x4x4) portant
> **4 Patriot P320 256 Go** (Gen3 x4, 2 200 / 1 200 Mo/s, TBW 120 To), placée sur
> le nœud des GPU ; le NVMe système actuel déplacé sur l'autre nœud avec une
> carte AMD pour l'affichage ; RAM **inchangée** (2×32 Go par socket).

**Le bon côté, et il est réel.** Le placement est juste : les données vont du
disque au GPU sans traverser le QPI, l'OS et le bureau partent de l'autre côté, et
la RAM reste symétrique — ce que le § 9 recommandait. Les SSD P320 annoncent
2 200 Mo/s en lecture, soit **~5× le NVMe actuel** (mesuré **1,6 Go/s**) et
**~9× le disque dur** (mesuré 246 Mo/s).

**Trois contraintes à vérifier avant de commander le reste**, dans l'ordre où
elles mordent.

### 11.1 Les lignes PCIe : un x16 de plus ne rentre pas tel quel

Le Xeon E5-2687W v3 fournit **40 lignes PCIe 3.0 par socket**. Relevé aujourd'hui
sur le nœud 0 (`/sys/bus/pci/devices/*/` et `lspci`) :

| périphérique | liaison actuelle | max |
|---|---|---|
| Quadro RTX 5000 (`03:00.0`) | x16 (2,5 → 5,0 GT/s selon la charge) | x16 Gen3 |
| Quadro RTX 5000 (`04:00.0`) | x16 (2,5 → 8,0 GT/s selon la charge) | x16 Gen3 |
| NVMe système (`02:00.0`, MAP1602) | x4 Gen3 | x4 Gen4 |

Deux GPU en x16 (32 lignes) + le NVMe (4) = **36 lignes occupées sur 40**. Une
carte 4×NVMe **x16** en demande 16 de plus : **52 sur 40**. Il faudra donc choisir,
et le choix se fait dans le BIOS :

- **GPU en x8 + carte en x16** (16 + 16 + 4 = 36 ✅) : le tableau est complet, mais
  chaque GPU perd la moitié de sa bande passante hôte — le dépôt a mesuré
  **6,5 Go/s en x8** (`drave-core/src/gpu.rs:7`) contre ~13 en x16. Le trafic
  concerné est le miroir du cache KV et les projections déportées : c'est
  précisément ce qui a donné « attention 22,16 → 3,29 ms/jeton ».
- **GPU en x16 + carte en x4** (32 + 4 + 4 = 40 ✅) : les 4 SSD partagent alors
  ~3,9 Go/s — **le débit d'un seul SSD**. L'array ne sert à rien.

**À vérifier au BIOS** : la bifurcation `x4x4x4x4` sur le slot choisi, et que ce
slot est bien câblé au **CPU** (un slot derrière le PCH donne du x4 Gen2 partagé,
soit ~2 Go/s pour les quatre). Les cartes 4×M.2 passives l'exigent ; sans
bifurcation, **un seul SSD apparaît**.

### 11.2 Les canaux mémoire : la RAM n'est pas « 2×32 + 2×32 », elle est à moitié

EDAC répond sans ambiguïté (`/sys/devices/system/edac/mc/mc*/dimm*/`) :

```
CPU 0 : Chan#0 → 32 Go · Chan#1 → 32 Go
CPU 1 : Chan#0 → 32 Go · Chan#1 → 32 Go
```

Le Xeon E5-2687W v3 a **quatre canaux mémoire par socket**. Deux DIMM par socket,
c'est **deux canaux sur quatre vides**. La bande passante mesurée aujourd'hui le
confirme : **20,4 Go/s** (64 Mo lus, 16 threads) — c'est un ordre de grandeur de
dual-channel, pas de quad-channel.

Conséquence directe : **le plan garde la moitié de la bande passante mémoire de la
machine.** Or c'est *le* facteur limitant du régime mémoire (les passes denses),
celui-là même que le § 3 montre qu'on ne rattrape pas par le placement. Passer à
**4 DIMM par socket** (1 par canal) doublerait à peu près la bande passante —
probablement le meilleur rapport gain/prix de toute la liste, et il n'est pas
dans le plan.

### 11.3 Capacité : 1 To ne contient pas Kimi-K3

4 × 256 Go = **1,024 To** brut, ~950 Gio utiles. État actuel du NVMe
(`FastNVMe`, 828 Go, **97 % plein, 29 Go libres**) :

| contenu | taille | tient dans l'array de 1 To ? |
|---|---:|---|
| DeepSeek-V4.1-Flash Q2 | 341 Go | ✅ oui, avec de la place |
| Kimi-K3 (32 shards) | **1,5 To** — **5 shards seulement sont sur disque** (228 Go) | ❌ non, même complet |
| gpt-oss-120b MXFP4 | 63 Go | ✅ oui |
| artefacts, qwen3-30b | 134 Go | ✅ oui |

C'est le point qui décide de l'usage : l'array est un très bon support pour
**un** gros modèle de la classe 350-950 Go, pas pour K3 entier. Si l'objectif est
de faire tenir K3, il faut 2 To (8 SSD) ou garder K3 réparti entre l'array et le
disque dur.

### 11.4 Ce que l'array peut rapporter, et ce qu'il faut mesurer

- **Débit attendu** : 4 × 2 200 Mo/s = 8,8 Go/s en théorie, plafonné par le lien
  x16 Gen3 (~7,9 Go/s utiles) et par le caractère **DRAM-less** des contrôleurs.
  Attendre **6 à 8 Go/s** est raisonnable, contre 1,6 Go/s aujourd'hui.
- **Ce que ça change pour Drave** : la passe K3 lit 206,58 Gio. À 133 Mio/s (le
  débit *obtenu* par le moteur sur le disque dur) elle dure 26,5 min ; à 7 Go/s
  elle durerait **~30 s**. Mais attention : le moteur obtient 133 Mio/s là où le
  disque dur plafonne à 205 en séquentiel — **le motif d'accès coûte 35 %**. Un
  array ne corrige pas un motif ; il faut donc mesurer, pas extrapoler.
- **Répartition** : le moteur lit par `mmap`. Pour qu'un *seul* fichier soit lu
  par les 4 SSD, il faut un **RAID0** (`mdadm`) — le noyau répartit les bandes.
  Sinon chaque SSD est un volume et il faut quatre fichiers (le moteur sait lire
  un modèle en clusters multi-fichiers). **À mesurer dans les deux dispositions**
  avec la même passe.
- **Endurance** : les lectures n'usent pas le TBW. Les 120 To du P320 ne
  concernent que les écritures (téléchargements de modèles) — non critique ici.
- **Mesures avant/après**, dans l'ordre : `dd iflag=direct` par SSD puis sur
  l'array (plafond brut) → `--materiel` du moteur (topologie vue) → une passe
  disque (K3 ou 4 jetons de V4-Flash) en JBOD et en RAID0 → et la **relecture des
  largeurs de liaison** (`current_link_width`, `current_link_speed`) **sous
  charge**, pas au repos : au repos, les deux Quadro annoncent 2,5 GT/s alors
  qu'elles montent à 5,0 et 8,0 GT/s en travail.

### 11.5 La carte AMD

Le moteur n'a **aucun noyau AMD** : `drave-core/src/gpu.rs` compile du PTX pour
CUDA, et le déport se décide sur la VRAM libre des Quadro. Une carte AMD ne peut
donc servir qu'à **l'affichage** — ce qui est exactement l'usage proposé, et c'est
utile : c'est ce qui rend au calcul la VRAM et les cycles que le bureau prend
aujourd'hui. Aucune capacité de calcul n'est perdue en la déplaçant.

---

## 12. La RAM est hors de prix : quoi faire à la place

> DDR4 ECC en fin de vie de plateforme, prix du neuf dissuasifs. La question
> devient : que peut-on récupérer, économiser ou remplacer, sans acheter de RAM ?

### 12.1 Ce qui est déjà perdu, et qui ne coûte rien à reprendre

**26 Go sont en swap, sur le disque dur.** Relevé aujourd'hui : `Swap: 62 Gi
total, 26 Gi utilisé`, et le swap est sur `sda` (**246 Mo/s** mesuré). Toute page
touchée là coûte des centaines de microsecondes. Le dépôt avait déjà croisé ce
fantôme pendant les travaux Kimi-K3 (« VmSwap 28,5 Go » relevé alors que le
moteur affirmait « pas de swap »).

- `swapoff -a && swapon -a` ramène ces pages en RAM (103 Go disponibles, donc
  l'opération passe) ;
- quand l'array arrive, **le swap va sur le NVMe, jamais sur `sda`** ;
- `vm.swappiness` est déjà à 10, `vm.overcommit_memory` à 1 : les réglages ne
  sont pas le problème, le support l'est.

**La bande passante mémoire, entrelacée — mais elle ne se transfère pas à la
charge.** Trois mesures du banc du moteur (64 Mo lus) :

| placement | débit |
|---|---:|
| sans liaison (16 fils) | 20,4 Go/s |
| lié au nœud 0 (10 fils) | 22,4 Go/s (**+10 %**) |
| **entrelacé sur les deux nœuds** (20 fils) | **23,8 Go/s (+17 %)** |

Ces +17 % sont visibles **au banc**, pas sur la charge : l'A/B du § 7 donne
**−0,9 %** pour la même configuration sur une passe réelle. C'est la règle du
dépôt — *un banc qui ne ressemble pas à la charge ne décide pas du placement* —
et elle joue ici contre l'optimisation gratuite.

**Ce qui est déjà réglé** : gouverneur `performance`, THP `always`, `mmap` par
défaut. Il ne reste, côté gratuit, que la **fréquence de l'uncore** (le ring
plafonne la bande passante sur Haswell-EP ; MSR `0x620`, à mettre au maximum —
le noyau n'expose pas `intel_uncore_frequency` ici, il faut `msr-tools` et root).

### 12.2 Le substitut de RAM, c'est le disque — et il est déjà commandé

C'est le point qui rend l'achat de RAM inutile pour l'usage principal :

| | RAM aujourd'hui | array 4×NVMe (commandé) |
|---|---:|---:|
| bande passante | 20,4 Go/s *(mesuré)* | **6 à 8 Go/s** *(attendu)* |
| capacité | 125 Go (dont ~100 en cache) | **1 To** |
| lire 206,58 Gio (passe K3) | impossible à garder | **~30 s** |

La passe Kimi-K3 lit 206,58 Gio dont **57,93 Gio de dense, lus une fois** et
148,65 Gio d'experts relus à chaque jeton. Le dépôt a mesuré que **la page cache
ne retient pas le dense** d'une passe à l'autre (1 516 430 puis 1 522 584 ms) :
compter sur la RAM pour ça ne marche pas. Un array à 7 Go/s lit ces 58 Go en
**8 secondes** — le problème disparaît au lieu d'être résolu.

Et le corollaire du programme : **un modèle routé n'a pas besoin d'être en RAM
pour être gros.** Mesuré sur le prototype : 2,3 M poids lus par jeton pour
7,58 M stockés, soit **3,35× de paramètres pour la même lecture**. La RAM cesse
d'être le facteur limitant dès que le modèle est creux en lecture.

### 12.3 Réduire ce qui DOIT tenir en RAM

Le cache KV est le seul poste qui grandit avec l'usage, et il est déjà chiffré
par le dépôt :

| réglage | coût en qualité | gain en RAM |
|---|---|---|
| KV int8, 512 jetons | **+1,5 % de perplexité** | 2× |
| KV int8, 8 192 jetons | **+3,0 %** | 2× |
| KV int4 | +364 % → inutilisable | 4× |
| **KV paginé à la demande** | mesuré, contexte 1 M | **0,03 Go au lieu de 25,77 Go** |

À l'inverse, deux pistes mesurées **perdantes** qu'il ne faut pas rouvrir :
`DRAVE_EXPERTS_RAM` (+4 % à 4 Go, +21 % à 32 Go) et le cache d'experts en VRAM
tel quel (+6 %, verdict « ne pas activer »). La VRAM reste utile — 32 Go à
84,9 Go/s, 4× la RAM — mais pour le KV et les projections, pas comme cache
d'experts générique.

### 12.4 Si l'on achète quand même : quoi, exactement

1. **4 DIMM par socket (un par canal) est la seule configuration qui double la
   bande passante** — et elle double la capacité si l'on prend 4×32 Go. C'est le
   seul achat qui attaque le facteur limitant mesuré (2 canaux sur 4 vides,
   confirmé par EDAC).
2. **2×64 Go par socket ne double que la capacité**, pas la bande passante — et
   peut exiger des LRDIMM selon la carte mère.
3. **Attention au dérating** : sur Haswell-EP, 2 DIMM par canal fait tomber la
   fréquence (1866 au lieu de 2133). Un DIMM par canal tient la fréquence
   maximale : c'est un argument de plus pour 4 DIMM plutôt que 8.
4. **Plateforme en fin de vie = marché de l'occasion serveur.** Les RDIMM DDR4
   ECC déclassés coûtent une fraction du neuf. Vérifier la QVL de la carte mère,
   ne pas mélanger les rangs dans un canal, et garder les 4 DIMM identiques.
5. **L'ordre des dépenses** que ces mesures dictent : array NVMe (déjà commandé)
   → 4 DIMM par socket **seulement si** une charge réelle reste limitée par la
   mémoire → rien d'autre. Acheter de la RAM pour faire tenir un modèle de 1,5 To
   est perdu d'avance sur une machine de 125 Go (c'est la définition de la niche
   du projet).
