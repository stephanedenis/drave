# Nouvelle configuration : array NVMe sur le nœud 1, AMD pour le bureau

> **Document daté.** Plan, note ou étude d'un chantier : il porte sa date et son état en tête. La
> **feuille de route courante** est [`roadmap.md`](roadmap.md) ; l'**état** est
> [`en-cours.md`](en-cours.md).

> **2026-10-12 — l'intervention a eu lieu, et le pari est mesuré.** L'array existe (4 NVMe,
> raid0, 938 Go, monté `/home/stephane/IA`) et la fiche
> [`reports/rapport-raid0-nvme.md`](../reports/rapport-raid0-nvme.md) répond au protocole du § 7 :
> les 4 NVMe sont bien sur le **nœud 1**, les Quadro sont en **x16** (le pari du § 1 tient),
> l'array rend **7,45 Go/s** en lecture à 8 flux pour **6-7 Go/s** attendus au § 8, et **2,86 Go/s**
> en écriture — la réserve du § 8 sur les contrôleurs **DRAM-less** se confirme en aléa QD1 (l'array
> n'y bat pas un NVMe seul). Le § 6.3 est tranché côté lecture : **le QPI ne coûte rien** à pleine
> bande (7,41-7,47 Go/s selon le placement). Restent ouverts, et nommés dans la fiche : le
> `read_ahead_kb` du § 6.2 (**root requis**), la montée du lien GPU **sous charge** (§ 7.5), et la
> moitié « calcul » du § 6.3. Un écart trouvé : `drave … --materiel` **ne voit pas l'array** (§ 7.2).

> 08/10. Document de préparation, écrit **avant** l'intervention : ce qu'il faut
> vérifier au BIOS, ce qu'il faut installer, comment monter le RAID, comment
> faire cohabiter la carte AMD avec les Quadro, et ce qu'il faudra mesurer pour
> savoir si le pari est tenu.
>
> Configuration visée : les **4 NVMe sur une carte PCIe** vont sur le **second
> CPU** (pour laisser leurs 16 voies à chacun des deux GPU), la **carte AMD
> 6 mini-DP** prend l'affichage sur le **même nœud**, la **RAM ne bouge pas**
> (2×32 Go par socket), et les deux Quadro restent en x16 avec NVLink.

---

## 1. La configuration cible, et pourquoi elle tient debout

| | nœud 0 (calcul) | nœud 1 (bureau + stockage) |
|---|---|---|
| CPU | Xeon 0 · 10 cœurs / 20 fils | Xeon 1 · 10 cœurs / 20 fils |
| RAM | 64 Go (2×32, canaux 0-1) | 64 Go (2×32, canaux 0-1) |
| GPU | **2 × Quadro RTX 5000, x16, NVLink 25,78 Go/s** | Yeston AMD 6×mini-DP (affichage) |
| Disques | — | **carte 4×NVMe en RAID0 (1 To)** + NVMe système |
| Voies PCIe | 32 + 4 = 36 / 40 | 4 (array) + 4 (système) + AMD |

**Ce que ce plan achète, et c'est mesuré** : les GPU gardent leurs **x16** (36
voies utilisées sur 40 — la carte 4×NVMe n'aurait pas pu tenir sur le nœud 0 sans
faire tomber les GPU en x8, mesuré à **6,5 Go/s** au lieu de ~13). Le bureau et
l'affichage sortent du nœud de calcul, ce qui rend au calcul la VRAM et les
cycles que le compositeur prend aujourd'hui. La RAM reste **symétrique**, ce que
les mesures recommandaient.

**Ce qu'il coûte, et qu'il faudra mesurer** : les octets des modèles devront
**traverser le QPI** pour atteindre la RAM et les GPU du nœud 0. Le QPI d'un E5 v3
écoule ~12-14 Go/s utiles par sens ; un array à 6-8 Go/s en occupe donc la moitié.
Les mesures du dépôt donnent une pénalité de **3 à 4 %** pour traverser le QPI
(calcul pur et lecture NVMe entre nœuds), donc le pari est raisonnable — mais
c'est un pari, et le § 7 dit comment le vérifier.

**Un point à ne pas manquer** : le cache de page se pose sur le nœud du fil qui
touche la page le premier. Si le moteur tourne sur le nœud 0, chaque lecture
franchit le QPI **une fois** ; si les fils de lecture tournent sur le nœud 1, la
DMA reste locale mais le calcul franchit ensuite. Les deux dispositions se
mesurent (§ 7) ; la réponse n'est pas dans ce document, elle est dans la machine.

---

## 2. L'outillage est déjà là — mais pas dans le PATH

Vérification par chemin complet (un `command -v` depuis un shell d'utilisateur
les dit « absents », parce que **`/sbin` n'est pas dans le PATH** ; root, lui,
l'a) :

| outil | chemin | état |
|---|---|---|
| `mdadm` | `/sbin/mdadm` | ✅ présent |
| `mkfs.xfs`, `xfs_info` | `/sbin/mkfs.xfs` | ✅ présent |
| `smartctl` | `/sbin/smartctl` | ✅ présent |
| `nvme` | `/sbin/nvme` | ✅ présent |
| `fstrim`, `wipefs`, `blkid` | `/sbin/…` | ✅ présents |
| `dracut` | `/usr/bin/dracut` | ✅ présent |

Le noyau a tout ce qu'il faut aussi : modules `md-mod`, `raid0`, `raid456`,
`amdgpu`, `radeon`, et le **firmware `amdgpu/` est en place** (`/lib/firmware/`).
Aucune installation n'est nécessaire — si un paquet manquait malgré tout :
`sudo zypper install mdadm xfsprogs smartmontools nvme-cli`.

*Système : openSUSE Tumbleweed, noyau 7.2.6-1-default — relevé sur la machine.*

---

## 3. Le BIOS, avant de démonter quoi que ce soit

1. **Bifurcation `x4x4x4x4`** sur le slot qui portera la carte 4×NVMe. Les cartes
   passives l'exigent : sans elle, **un seul SSD apparaît**.
2. **Ce slot doit être câblé au CPU 1**, pas au PCH. Derrière le PCH, c'est du
   x4 Gen2 partagé, soit ~2 Go/s pour les quatre SSD, et tout le bénéfice part.
3. **`Above 4G Decoding` activé**, sinon une carte à plusieurs périphériques peut
   ne pas être mappée.
4. **ASPM désactivé** sur les slots NVMe : l'économie d'énergie se paie en
   latence, et c'est la latence qu'on vient chercher.
5. **Affichage primaire = la carte AMD.** Sinon le BIOS et le chargeur sortent
   sur une Quadro, qui garde un framebuffer pendant que le calcul l'attend.
6. **IOMMU (`VT-d`)** : inutile ici (pas de passthrough). Le laisser activé coûte
   un peu de latence sur les accès directs ; le désactiver est un essai gratuit,
   à mesurer.
7. **Carte AMD dans un slot x4 ou x8**, pas x16 : une carte d'affichage n'a pas
   besoin de 16 voies, et chaque voie laissée libre est une voie pour les SSD.

---

## 4. Le RAID

### 4.1 Quel niveau, et pourquoi

**RAID0 (`mdadm`), pour les modèles.** Le raisonnement est celui du dépôt : les
poids se retéléchargent, la capacité compte (1 To) et le débit de lecture se
multiplie par le nombre de disques. Ce qui est stocké là est **reproductible par
définition** — modèle téléchargé, corpus extrait d'une source publique. **Tout ce
qui n'est pas reproductible n'a rien à y faire.**

- **RAID0** : 4 × 256 Go = ~953 Gio utiles, 4× le débit d'écriture comme de
  lecture, **aucune tolérance à la panne** : un SSD mort perd l'array entier.
- **RAID5** (si l'on veut survivre à une panne) : ~716 Gio utiles, et l'écriture
  coûte un calcul de parité — sur des SSD **DRAM-less**, c'est précisément ce
  qu'ils font le plus mal. À ne choisir que si les données ne sont pas
  retéléchargeables.

### 4.2 Les commandes

```bash
# Identifier les 4 disques par leur NUMÉRO DE SÉRIE, pas par leur nom :
# l'ordre des /dev/nvmeXn1 dépend des slots et change au rebranchement.
sudo nvme list
sudo smartctl -a /dev/nvme1n1 | head -20     # santé avant intégration

# Table de partition neuve (efface ce qu'il y a) :
sudo wipefs -a /dev/nvme1n1 /dev/nvme2n1 /dev/nvme3n1 /dev/nvme4n1

# L'array. `--assume-clean` évite une resynchronisation initiale inutile
# (un RAID0 neuf n'a rien à synchroniser, et la faire use les SSD pour rien).
# `--chunk=512K` : un flux séquentiel est découpé en bandes de 512 Ko
# réparties sur les 4 disques — c'est ce qui parallélise une lecture de modèle.
sudo mdadm --create /dev/md0 --level=0 --raid-devices=4 --chunk=512K \
     --assume-clean /dev/nvme1n1 /dev/nvme2n1 /dev/nvme3n1 /dev/nvme4n1

# Système de fichiers : XFS, pour les fichiers de plusieurs centaines de Go et
# les lectures parallèles. (ext4 convient aussi ; XFS vieillit mieux à cette
# taille.)
sudo mkfs.xfs -f -L modeles /dev/md0

# Montage : `noatime` (ne pas écrire une date à chaque lecture), et un
# read_ahead large — un modèle se lit en flux.
sudo mkdir -p /srv/modeles
echo "/dev/md0 /srv/modeles xfs noatime,allocsize=1m 0 0" | sudo tee -a /etc/fstab
sudo mount -a
sudo blockdev --setra 8192 /dev/md0          # 4 Mio de lecture anticipée

# Survie au redémarrage : l'array doit être assemblable sans son nom de périphérique
sudo mdadm --detail --scan | sudo tee -a /etc/mdadm.conf
sudo dracut -f                                # openSUSE : reconstruire l'initramfs
sudo systemctl enable --now fstrim.timer      # TRIM hebdomadaire
```

### 4.3 Vérifications, dans l'ordre

```bash
cat /proc/mdstat                              # les 4 disques, [UUUU]
lsblk -o NAME,SIZE,TYPE,MOUNTPOINT
dd if=/dev/nvme1n1 of=/dev/null bs=1M count=2000 iflag=direct   # par SSD
dd if=/dev/md0 of=/dev/null bs=1M count=4000 iflag=direct       # l'array
```

**Ce qu'on attend** : ~2 Go/s par SSD (le P320 annonce 2 200 Mo/s) et **6 à
7 Go/s sur `md0`**, plafonnés par le lien x16 Gen3 (~7,9 Go/s utiles) — pas par
les disques. Si `md0` plafonne à ~2 Go/s, c'est que la bifurcation n'est pas
active ou que le slot n'a que 4 voies : vérifier
`/sys/block/nvmeXn1/device/current_link_width`.

**Le piège des P320** : ce sont des contrôleurs **DRAM-less**. En lecture
séquentielle, c'est sans conséquence ; en **écriture soutenue** (télécharger
350 Go de poids), le débit s'effondre une fois le cache SLC épuisé. Écrire les
gros modèles un par un, pas quatre en parallèle.

---

## 5. La carte AMD Yeston (6 mini-DP)

Le modèle le plus courant sous cette description est une **Yeston R7 350
6×mini-DP** (GCN 1.0, 2 ou 4 Go). **À identifier à réception** plutôt qu'à
supposer :

```bash
lspci -nn | grep -i vga          # donne l'identifiant 1002:xxxx exact
```

### 5.1 Le pilote : `radeon` ou `amdgpu` — les deux sont là

Le noyau 7.2.6 fournit **les deux modules** et le firmware `amdgpu/` est présent
(vérifié). Pour les GPU **GCN 1.0 — Southern Islands, familles Cape Verde et
Oland, dont la R7 350** — le noyau choisit par défaut le pilote **`radeon`** ;
`amdgpu` peut aussi les piloter, mais il faut le lui demander explicitement au
démarrage (et désactiver `radeon` en face, sinon les deux se disputent la carte) :

```
# /etc/default/grub — compléter GRUB_CMDLINE_LINUX_DEFAULT :
amdgpu.si_support=1 radeon.si_support=0
```

`cik_support` (Sea Islands : Bonaire, Hawaii) ne concerne **pas** cette carte —
le confondre avec `si_support` est l'erreur courante, et elle se solde par un
écran noir.

puis `sudo grub2-mkconfig -o /boot/grub2/grub.cfg` et redémarrer.

- **Commencer par `radeon`** (rien à faire, mature pour GCN 1.0) : c'est
  suffisant pour six écrans de bureau.
- Passer à `amdgpu` **seulement si** Wayland ou Vulkan le réclame.

*Si la carte reçue est en fait une RX 550 (GCN 4, Polaris), elle est pilotée par
`amdgpu` d'origine : aucun paramètre de noyau, et le firmware est là aussi. La
commande `lspci -nn` du § 5.0 tranche.*

### 5.2 Ne pas laisser X prendre les Quadro

C'est le point qui annule tout le bénéfice si on le rate : si le serveur
graphique ouvre aussi les Quadro, elles gardent un framebuffer et de la VRAM
occupée. À vérifier **après** le basculement :

```bash
xrandr --listproviders                  # un seul fournisseur : AMD
nvidia-smi                              # aucun processus, 0 Mio utilisés par l'affichage
fuser -v /dev/nvidia* 2>&1 | head       # personne
```

Si les Quadro apparaissent, forcer le `BusID` de l'AMD dans la configuration X
(`/etc/X11/xorg.conf.d/20-amd.conf`, section `Device` avec
`BusID "PCI:XX:00.0"`), et **ne pas** installer de sortie écran dessus.

### 5.3 Les six écrans

```bash
xrandr | grep " connected"              # six sorties mini-DP (adaptateurs actifs
                                        # si les moniteurs sont en HDMI/DVI)
```

Un adaptateur **mini-DP → HDMI/DVI passif** ne fonctionne que si la sortie
émet du DP++ ; sinon il faut un adaptateur **actif**. C'est l'erreur classique
sur ces cartes à six sorties.

---

## 6. Les autres optimisations, par ordre de gain

### 6.1 Mémoire — 26 Go sont déjà perdus (gratuit)

`Swap: 62 Gi, 26 Gi utilisés`, et le swap est sur le **disque dur** (246 Mo/s).

```bash
sudo swapoff -a && sudo swapon -a       # ramène les pages (103 Go disponibles)
```

Puis, quand l'array vit : **pas de swap sur le RAID0** (une panne de SSD y
corromprait la mémoire paginée). Deux bonnes options : `zram` (swap compressé en
RAM, paquet `zram-generator`) ou une petite partition de swap **sur un seul**
des NVMe, hors array.

### 6.2 Entrées/sorties (mesurable en une commande)

| réglage | état actuel | à essayer |
|---|---|---|
| ordonnanceur NVMe | `[none]` ✅ | rien — c'est le bon |
| `read_ahead_kb` | **1 024** | **4 096 à 8 192** sur `md0` et sur les NVMe |
| `nr_requests` | 1 023 ✅ | rien |

### 6.3 NUMA — trois placements à comparer, pas un principe

Le seul point où ce document ne peut pas trancher à l'avance :

| disposition | ce qui traverse le QPI |
|---|---|
| moteur sur le **nœud 0** (avec les GPU) | chaque octet lu (6-8 Go/s) |
| moteur sur le **nœud 1** (avec les disques) | chaque tenseur envoyé au GPU |
| **fils de lecture nœud 1, calcul nœud 0** | les deux, une fois chacun |

Les mesures du dépôt donnent 3-4 % pour traverser le QPI, mais elles portaient
sur des charges légères. Avec 6-8 Go/s, c'est la moitié du QPI : **à mesurer**
(§ 7).

### 6.4 Ce qui est déjà bon, et qu'il ne faut pas « optimiser »

- gouverneur CPU **`performance`** ✅ · THP **`always`** ✅ · `vm.swappiness` **10** ✅
- ECC des Quadro **désactivé** ✅ (VRAM et bande passante maximales)
- `mmap` par défaut : **47 Mo de RSS pour 365 Go adressés** — ne pas passer à
  `DRAVE_MMAP=0`, qui lit au lieu de mapper.
- **Ne pas** activer `DRAVE_EXPERTS_RAM` (+4 % à 4 Go, +21 % à 32 Go — mesuré
  perdant) ni le cache d'experts VRAM tel quel (+6 %).

### 6.5 Côté moteur — les deux chantiers que cette machine rend payants

1. **Les lecteurs parallèles ne sont pas utilisés.** Le plan calcule
   `lecteurs = 16` (« le NVMe passe de 5,4 à 31,1 Go/s ») et **ne s'en sert
   jamais** : le parallélisme vient des défauts de page, pas d'un lecteur dédié.
   Sur un RAID0, c'est le chemin de lecture qu'il faut paralléliser
   explicitement (`pread` par bande, ou `O_DIRECT`).
2. **Le motif d'accès coûte 35 %** : 133 Mio/s obtenus sur le disque dur là où
   le séquentiel plafonne à 205. Un array ne corrige pas un motif — mais il rend
   l'écart visible : si `md0` donne 6 Go/s en `dd` et 2 Go/s dans la passe, le
   motif est le coupable, pas le matériel.
3. **La fréquence de l'uncore** (le ring plafonne la bande passante mémoire sur
   Haswell-EP) : MSR `0x620`, à mettre au maximum. Le noyau n'expose pas
   `intel_uncore_frequency` ici — il faut `msr-tools` et root.

---

## 7. Le protocole de mesure, avant/après

Trois répétitions **entrelacées** par configuration (la charge de fond fait
varier le temps mur de 30 % : c'est la règle du dépôt).

1. **Débit brut** : `dd iflag=direct` par SSD, puis sur `md0` — 2 Go, 4 Go.
2. **Topologie vue par le moteur** : `drave <modèle> --materiel` — doit montrer
   les GPU sur le nœud 0, et l'array sur le nœud 1.
3. **Passe disque** (le régime qui compte) : la passe K3 ou 4 jetons de
   V4-Flash, en comparant l'array aux 246 Mo/s du disque dur.
4. **Placement des fils** : la même passe avec (a) moteur sur le nœud 0,
   (b) sur le nœud 1, (c) lecture sur le nœud 1 et calcul sur le nœud 0.
5. **Largeur des liaisons** GPU **sous charge** — au repos, les Quadro annoncent
   2,5 GT/s alors qu'elles montent à 5,0 et 8,0 :
   ```bash
   for d in 0000:03:00.0 0000:04:00.0; do
     echo "$d $(cat /sys/bus/pci/devices/$d/current_link_width)x @ $(cat /sys/bus/pci/devices/$d/current_link_speed)"; done
   ```
   **Attendu : x16.** Si c'est x8, la bifurcation a volé des voies aux GPU et le
   pari du § 1 est perdu.
6. **La porte de non-régression du moteur** : `tools/portes.sh` — elle doit
   rester verte après chaque changement de montage.

---

## 8. Réserves

- **Aucune de ces optimisations n'est mesurée sur cette configuration** : elle
  n'existe pas encore. Les chiffres cités viennent de la configuration actuelle
  (mesures du 08/10) ou des rapports du dépôt.
- Le débit attendu de l'array (**6-7 Go/s**) est **extrapolé** de 4 × 2 200 Mo/s
  et du plafond du lien x16 Gen3 ; les contrôleurs DRAM-less peuvent être en
  dessous, surtout en écriture.
- Le modèle exact de la carte Yeston n'est pas connu : le § 5 est écrit pour les
  deux cas (R7 350 GCN 1.0, ou RX 550) et commence par la commande qui tranche.
- Le QPI portera 6-8 Go/s : c'est **la moitié de ce qu'il écoule**. Si le § 7
  montre une pénalité supérieure aux 3-4 % déjà mesurés, la conclusion change et
  il faudra soit un array partiel sur le nœud 0, soit accepter x8 sur un GPU.
