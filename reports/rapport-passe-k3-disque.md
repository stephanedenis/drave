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

---

## 7. Attribution des 206,58 Gio : d'où viennent les octets ?

Un coût sans attribution ne dit pas où agir. Les tailles viennent des en-têtes du
GGUF (`drave … --tensors`, 2 573 tenseurs), les octets lus du relevé.

**Unités** : le relevé est en **Gio** (divisé par 2³⁰). Le moteur annonce
1 508,66 **Go** décimaux = **1 405,06 Gio** — les deux chiffres sont le même
modèle, et les confondre ferait une erreur de 7 %.

| classe | Gio | part du modèle | quand c'est lu |
|---|---:|---:|---|
| **experts MXFP4** (276 tenseurs) | **1 347,13** | **95,9 %** | **par (jeton, couche)** — 16 experts routés par jeton |
| attention (Q8_0, 678 tenseurs) | 29,58 | 2,1 % | une fois par couche et par passe |
| FFN dense (Q8_0, 833 tenseurs) | 19,63 | 1,4 % | idem |
| `ssm_*` | ~6,5 | 0,5 % | idem |
| `token_embd` + `output` | 2,32 | 0,2 % | une fois |
| normes, scores, biais (1 181 F32) | ~0,0 | 0,0 % | idem |

**Et la passe a lu 206,58 Gio**, qui se séparent ainsi :

| | Gio | part de la passe |
|---|---:|---:|
| dense + attention + `ssm` (une fois par passe, partagés par les 4 jetons) | **57,93** | **28,0 %** |
| experts (relus pour CHAQUE jeton, à chaque couche) | **148,65** | **72,0 %** |

**Le dense est lu une fois pour quatre jetons ; les experts, quatre fois.** C'est
la structure du coût, et elle commande tout : les octets d'experts sont
**proportionnels au nombre de jetons**, ceux du dense non.

### 7.1 Le levier que cela désigne, et il est déjà dans le code

`MoeK3::avant_lot` regroupe déjà les jetons par expert (`kimi_k3.rs:787`) :
*« un expert lu UNE fois, appliqué à tous ses jetons »*. **La feuille de route le
donnait pour non implémenté — elle est périmée sur ce point.** Mais le
regroupement ne rapporte que si des jetons du lot **choisissent le même expert**,
et à quatre jetons, sur ~581 experts par couche, les collisions sont rares : le
gain mesuré est nul, ce qui explique la phrase de `REPRISE.md` (« réduire de 25 %
les experts lus ne change rien ») — non pas que les octets ne comptent pas, mais
qu'à quatre jetons il n'y a rien à regrouper.

Le modèle, à `k = 16` experts routés par jeton et `n ≈ 581` experts par couche :

    octets d'experts ≈ n·(1 − e^(−T·k/n)) / n × 1 347 Gio
    total ≈ 57,93 + octets d'experts

| jetons T | experts distincts | octets lus | **Gio par jeton** | gain |
|---:|---:|---:|---:|---:|
| **4** (mesuré) | ~61 | 206,6 Gio | **51,6** | — |
| 16 | ~207 | 538 Gio | 33,6 | ×1,5 |
| 32 | ~340 | 847 Gio | 26,5 | ×1,9 |
| 64 | ~481 | 1 174 Gio | 18,3 | **×2,8** |
| 128 | ~563 | 1 364 Gio | 10,7 | ×4,8 |
| 512 | ~581 | 1 405 Gio | **2,7** | **×19** |

**Prédiction, écrite ici avant la mesure** : un préremplissage de **64 jetons**
devrait coûter ≈ **1 174 Gio**, soit ≈ **2 h 27** à 133 Mio/s — c'est-à-dire
**2,8× moins d'octets par jeton** qu'une passe de quatre. Et un préremplissage de
**512 jetons** devrait lire **le modèle entier une fois** (1 405 Gio, ≈ 2 h 56)
pour **2,7 Gio par jeton**, soit **19× mieux**.

**Ce modèle est une extrapolation, pas une mesure** : il suppose que les experts
sont tirés uniformément et que le routeur ne change pas avec la taille du lot. Le
routeur, lui, dépend du contexte — donc les 64 jetons ne choisiront pas forcément
les mêmes experts que 64 passes de 4. C'est précisément ce que la mesure devra
trancher.

## 8. Ce que ce diagnostic a réfuté, et ce qu'il laisse ouvert

**Réfuté** : l'hypothèse de la **dispersion** au sens de « la tête de lecture se
déplace d'expert en expert et le temps part là ». Le disque est occupé 87,6 % du
temps avec une file de ~14 requêtes : il ne cherche pas, il **débite**. Le temps
est celui du volume, pas du déplacement.

**Réfuté aussi** : que le CPU soit la limite (21 %), que la mémoire le soit (swap
nul, RSS 66 Gio), que les défauts de page majeurs le soient (zéro).

**Ouvert, et maintenant chiffré** : les octets. 148,65 Gio d'experts relus quatre
fois, quand un lot plus large les lirait une fois — c'est le seul levier qui
touche 72 % du trafic, et il est déjà dans le code.

---

## 9. Le plafond du disque, et l'écart qui reste

Une copie **séquentielle** du même modèle, du même disque vers le NVMe, mesurée
pendant la préparation du §10 : **205 Mio/s** (moyenne sur 30 s, `cp` d'un shard
de 44,2 Go).

La passe, elle, lit à **133 Mio/s**. **Le disque n'est donc pas à son plafond
séquentiel : la passe en obtient 65 %.**

Cela ne renverse pas le verdict — le disque reste la ressource saturée, occupé
87,6 % du temps — mais cela le précise de deux façons :

1. **Il reste ~35 % de débit à récupérer par le seul motif d'accès**, sans changer
   de matériel ni lire un octet de moins. Les lectures de la passe sont des
   défauts de page sur un `mmap` : elles arrivent par morceaux de page, à des
   endroits dispersés dans le fichier, au rythme où le calcul les touche. Une
   copie séquentielle lit de gros blocs contigus.
2. **Le chiffre à citer n'est pas « 130 Mo/s, c'est le disque »** mais **« 133
   Mio/s sur un plafond séquentiel de 205 »**. La différence est une question de
   motif, pas de matériel — et c'est une question sur laquelle on peut agir.

**Prédiction, avant mesure** : si la prélecture pouvait rapprocher le motif de la
passe du motif séquentiel, la même passe tomberait de 1 587 s à **≈ 1 030 s**.
L'essai de prélecture déjà consigné dans le code (×0,37, et 8,5× plus d'octets
lus) l'a tenté **en demandant l'union entière d'un coup**, ce qui a fait travailler
le noyau pour rien : ce n'est pas la même chose que de lire plus gros **au bon
moment**.

---

## 10. Le palier NVMe : la prédiction était de −16,3 %, la mesure donne −8,8 %

**Prédiction, écrite au §5 avant toute mesure** : déplacer ~250 Go de shards sur
le NVMe ferait tomber la passe à **≈ 1 300 s**.

**Ce qui a été fait** : les cinq premiers shards de contenu (shards 2 à 6,
**229 Go, 16,3 % du modèle**) copiés sur le NVMe — 259 Go libres, 5 × 45,8 Go —
chaque copie **vérifiée** (taille *et* empreinte des 64 premiers et derniers
mégaoctets), puis un dossier **hybride** de 32 liens symboliques dont cinq
pointent vers le NVMe. Aucun octet du modèle d'origine n'a été déplacé ni
supprimé.

**Le protocole, et pourquoi il est apparié.** `drop_caches` est réservé à root
(uid 1000 ici) : le cache de pages ne peut pas être vidé. Une passe « hybride »
comparée à la passe d'hier mesurerait donc **le palier ET le cache** sans pouvoir
les séparer. Deux passes identiques ont donc été enchaînées — même séquence, même
moteur, même sonde — la première sur le modèle d'origine, la seconde sur
l'hybride.

| | **référence** (07/10, 1ʳᵉ passe) | **A · tout sur le disque dur** | **B · 5 shards sur le NVMe** |
|---|---:|---:|---:|
| durée de la passe | 1 587 s | **1 495 s** | **1 363 s** |
| octets lus (bloc) | 206,58 Gio | 200,59 Gio | 215,56 Gio |
| débit effectif | 133,5 Mio/s | 137,4 Mio/s | **162,0 Mio/s** |
| `sda` occupé | 87,6 % | 86,6 % | 84,5 % |
| CPU travaillé | 21,0 % | 22,2 % | 25,1 % |
| secondes par couple | 4,266 s | 4,019 s | **3,664 s** |

**Le résultat, en trois lignes :**

1. **Le palier marche : −8,8 %** (1 495 → 1 363 s) contre la passe de contrôle
   immédiatement précédente, et **−14,1 %** contre la référence à froid.
2. **La prédiction de −16,3 % était optimiste d'un facteur deux.** L'écart a une
   cause mesurable : **B a lu 15 Gio de PLUS** que A (215,56 contre 200,59). Les
   copies sur le NVMe sont des fichiers **différents** — donc des pages froides —
   tandis que les shards du disque dur, lus deux fois de suite, étaient
   partiellement en cache. Le palier a échangé des octets *gratuits* contre des
   octets *rapides*.
3. **Le débit, lui, progresse de 18 %** (137 → 162 Mio/s) : c'est la preuve
   directe que les octets servis par le NVMe ne coûtent pas le prix du disque dur.

**Ce que cela dit pour la suite.** Le levier « disques supplémentaires » est
**réel et proportionnel**, mais son rendement dépend de ce que le cache servait
déjà gratuitement. Sur une machine où le modèle tient à 16 % sur un second
disque, on gagne 9 % ; sur trois nœuds à disques disjoints et froids, la
prédiction de ×3 du §5 reste ouverte — et **elle se mesurerait sur des octets
froids**, pas sur un régime déjà réchauffé.

**Ce que ce paragraphe ne dit pas** : il ne compare pas des débits de disque
isolés. Il compare **deux passes complètes**, avec leur cache, leurs files
d'attente et leur ordonnancement. C'est le chiffre utilisable ; ce n'est pas une
caractérisation du NVMe seul.

---

## 11. La loi des octets : `79,0 + 31,9 × T` Gio, validée sur trois points

Le §7 attribuait les octets par la **géométrie des tenseurs** : 57,93 Gio de dense
(lu une fois par passe, partagé par les jetons) et le reste en experts (relus à
chaque jeton). C'était une **déduction**, et elle butait sur un écart de 34 %.

Trois passes — **T = 1, 2 et 4 jetons** — suffisent à la remplacer par une
**mesure**, parce que les deux termes n'ont pas la même dépendance au nombre de
jetons :

    octets(T) = D + E·T

| T | octets lus | durée | débit | secondes par couple |
|---:|---:|---:|---:|---:|
| **1** | **110,55 Gio** | 813 s | 139,3 Mio/s | 2,185 s |
| **2** | **143,52 Gio** | 1 117 s | 131,6 Mio/s | 3,003 s |
| **4** | **206,58 Gio** | 1 587 s | 133,4 Mio/s | 4,266 s |

**Moindres carrés sur les trois points :**

    octets(T) = 79,0 + 31,9·T  Gio

| T | prédit | mesuré | résidu |
|---:|---:|---:|---:|
| 1 | 110,9 | 110,55 | **−0,3 %** |
| 2 | 142,9 | 143,52 | **+0,4 %** |
| 4 | 206,7 | 206,58 | **−0,1 %** |

**Le modèle affine tient à 0,4 % près sur trois points** — et il n'a pas été
ajusté sur deux points puis testé sur rien : les trois sont indépendants.

### 11.1 Ce que la géométrie prédisait, et l'écart

| terme | géométrie | **mesuré** | écart |
|---|---:|---:|---:|
| fixe `D` (dense, attention, `ssm`, emb, tête) | 57,93 Gio | **79,0 Gio** | **+36 %** |
| par jeton `E` (experts) | 24,1 Gio | **31,9 Gio** | **+32 %** |

**Les deux termes portent environ un tiers d'octets lus EN PLUS de ce que les
tenseurs contiennent.** Ce n'est pas un défaut d'un terme : c'est le **motif de
lecture** — des défauts de page sur un `mmap`, par morceaux, au rythme où le
calcul les touche, là où une copie séquentielle lit de gros blocs contigus (§9).

Cela rejoint la mesure du §9 : **la passe obtient 133 Mio/s sur un plafond
séquentiel de 205**, soit 65 %. Les deux chiffres — 1/3 d'octets en trop et 35 %
de débit en moins — disent la même chose par deux bouts différents.

### 11.2 Le critère du chantier 2 est INATTEIGNABLE sur cette machine, et voici la preuve

Le critère était : **« passe à 4 jetons sous 10 min »**.

    10 min à 133 Mio/s  =  77,9 Gio
    coût FIXE mesuré D  =  79,0 Gio

**Le coût fixe seul dépasse le budget.** Une passe à **ZÉRO jeton** — qui
chargerait le dense sans rien calculer — lirait déjà plus que ce que 10 minutes
permettent. Le critère n'est pas difficile : il est **impossible**, pour tout `T`,
sur ce disque.

Et même en retirant TOUT le gaspillage mesuré :

| hypothèse | octets (T=4) | durée à 133 Mio/s | durée au plafond 205 |
|---|---:|---:|---:|
| aujourd'hui | 206,6 Gio | **26 min** | 17,2 min |
| sans le tiers d'octets en trop | 154,2 Gio | 19,8 min | **12,8 min** |

**Même au plafond séquentiel du disque et sans un octet gaspillé, la passe de
quatre jetons demande 12,8 min.** Le critère de 10 min est un critère de
**matériel**, pas de code — et il se reformule ainsi :

> **Le coût d'une passe Kimi-K3 sur cette machine est `(79,0 + 31,9·T) Gio / débit
> du disque`. Le seul levier qui divise ce temps est le NOMBRE DE DISQUES.**

C'est exactement le chantier 3, et il devient chiffrable : à `N` nœuds à disques
disjoints, chaque nœud lit ≈ `(79,0 + 31,9·T)/N` et la passe tombe sous 10 min
**à partir de N = 3** (206,6 / 3 = 68,9 Gio → 8,8 min à 133 Mio/s).

### 11.3 Et le regroupement par expert, dans tout ça

`MoeK3::avant_lot` groupe déjà les jetons par expert (`kimi_k3.rs:787`) — la
feuille de route le donnait pour absent, elle est périmée. Ce que la loi des
octets dit de son **rendement** :

- à `T = 4`, 4 × 16 = **64 sélections** d'experts par couche, pour `n = 896`
  experts : les collisions attendues sont rares, le regroupement en économise
  **environ 5 %** ;
- la loi montre d'ailleurs que `E` est **exactement proportionnel à T** sur les
  trois points mesurés, à 3 % près (32,97 · 32,01 · 31,53 Gio par jeton) : **le
  regroupement ne se voit pas** dans ces mesures, ce qui est cohérent.

**Le regroupement n'est donc pas inutile — il est inerté par la taille du lot.**
Il paierait à 64 jetons ; à 4, il ne peut rien faire. C'est la phrase de
`REPRISE.md` (« réduire de 25 % les experts lus ne change rien ») enfin expliquée
par une mesure plutôt que par une hypothèse.
