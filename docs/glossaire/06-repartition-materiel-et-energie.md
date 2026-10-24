# 6. Répartition, matériel et énergie

> **Famille 6 du glossaire** (11 familles). Index : [le glossaire](../glossaire.md).

---

## 6. Répartition, matériel et énergie

**ALM (Adaptive Logic Module)** — La brique logique élémentaire d'un FPGA Intel
(Altera) Stratix V : un petit bloc capable de réaliser une fonction combinatoire.
Le projet compte ses opérateurs en ALM : un PE d'événements tient en 176 ALM et
0 DSP, contre 115 ALM et 1 DSP avec un multiplieur
(`docs/programme-recherche.md:58`, `reports/bilan-multi-materiel.md:66-67`).
**Réf.** : documentation Intel « Stratix V Device Handbook » — citée sans lien.

**AVX2 · AVX-512 · SIMD** — *SIMD* : une instruction qui traite plusieurs nombres à
la fois. *AVX2* est le jeu d'instructions 256 bits des processeurs x86 Haswell du
banc ; le noyau de tête `Q8_0` l'utilise (`vpmaddwd` sur 32 niveaux), et la somme
entière est exacte **au bit près** (`docs/contexte-long.md:378-382`). *AVX-512* est
évoqué comme la génération qui « paierait mieux » le 4 bits
(`reports/rapport-mur-memoire-4bits.md:205`). **Réf.** : Intel Intrinsics Guide —
cité sans lien (page officielle non vérifiable depuis cette machine).

**Bande passante (bandwidth)** — Débit maximal d'un chemin de données : RAM (~20-25
Go/s), VRAM (~380-750 Go/s), DDR3 du FPGA (9,66 Go/s), PCIe x8 (6,5 Go/s), NVMe
(3,5 à 31 Go/s selon la parallélisation). C'est la ressource qui borne le décodage :
« à contexte court, tout est bande passante de poids ; à contexte long, c'est le KV
puis le préremplissage » (`docs/contexte-long.md:580-586`,
`reports/bilan-multi-materiel.md:9`).

**Cœur physique · SMT · hyperthreading · paire HT** — Un cœur *physique* exécute un
flux ; le *SMT* (hyperthreading) fait apparaître deux fils logiques par cœur en
partageant certaines ressources. Mesure du dépôt : 10 cœurs avec 20 fils
hyperthreadés donnent +27 %, mais 20 cœurs avec 40 fils ne font pas mieux que
20 cœurs (22,8 contre 22,6 Go/s) (`reports/rapport-architecture-memoire.md:249-260`,
`:163`).

**CUDA · noyau (kernel) · sm_75 · PTX · FFI** — *CUDA* est l'API de calcul GPU de
NVIDIA ; un *noyau* est la fonction exécutée massivement en parallèle ; *sm_75* est
le niveau de capacité de calcul du Quadro RTX 5000 (1024 fils par bloc, 48 ko de
mémoire partagée, pas de `__reduce_add_sync`) ; *PTX* est l'assembleur virtuel dans
lequel le noyau est précompilé et chargé par le moteur ; *FFI* est l'appel du code
Rust vers la bibliothèque C (`drave-core/gpu/drave_gpu.cu`, `gpu.rs`,
`cuda_stub.h`). **Réf.** : NVIDIA, *PTX ISA*,
[docs.nvidia.com/cuda/parallel-thread-execution](https://docs.nvidia.com/cuda/parallel-thread-execution/).

**DDR3 · DDR4** — Générations de mémoire vive externe. La carte FPGA Stratix V
embarque de la DDR3 mesurée à 9,66 Go/s, qui est **son goulot** : c'est elle qui
limite le FPGA à ~4,83 G événements/s projetés
(`reports/bilan-multi-materiel.md:9`, `docs/comparaison-spiking.md:63`). Les deux
sockets Xeon ont de la DDR4-2133 (~136 Go/s théoriques,
`reports/rapport-passage-a-l-echelle.md:152`). **Réf.** : JEDEC JESD79-3 (DDR3) —
cité sans lien.

**Débit · latence · aller-retour · TTFT** — Le *débit* est ce qui passe par
seconde (Go/s, tok/s, événements/s) ; la *latence* est le délai d'un aller-retour.
Leçon du transport réparti : « le débit ne compte pas (0,25 Mbit/s), la latence
compte quatre fois » — `attente ≈ calcul distant + 3,2 × latence`
(`docs/roadmap.md:57`). Le *TTFT* (time to first token) est le délai avant le
premier jeton généré : 74-95 ms mesurés (`reports/rapport-inference.md:83`).

**DMA (Direct Memory Access)** — Déplacement de données par le matériel sans
mobiliser le processeur ; sur cette machine, c'est le noyau qui s'en charge
(`reports/rapport-architecture-memoire.md:398`).

**DRAM-less · HMB (Host Memory Buffer)** — Un SSD *DRAM-less* n'a pas de cache
interne et emprunte un peu de RAM hôte (*HMB*) pour ses tables ; le NVMe de la
machine est un MAP1602 de ce type, ce qui explique une partie de ses performances
en lecture aléatoire (`reports/rapport-architecture-memoire.md:221`, `:285`).
**Réf.** : spécifications NVMe, [nvmexpress.org](https://nvmexpress.org/specifications/).

**DSP (Digital Signal Processor / bloc multiplieur)** — Bloc matériel spécialisé
dans la multiplication, très coûteux en surface. Le projet s'en passe comme d'un
principe (« 0 DSP ») : ses multiplications ternaires deviennent des additions et
des décalages, et le PE synthétisé tient en 176 ALM sans DSP
(`docs/histoire.md:11`, `docs/programme-recherche.md:58`, `reports/rapport-encodage.md:74`).

**Énergie par événement (nJ, pJ, TDP)** — Coût énergétique d'un événement traité :
57 nJ mesurés sur CPU, 8,3 nJ **projetés** sur FPGA (limite DDR3), ~12,7 nJ déduits
pour le GPU ; la comparaison neuromorphique cite E_AC = 0,9 pJ contre E_MAC = 4,5 pJ
sur du 45 nm (`reports/bilan-multi-materiel.md:46-48`,
`docs/comparaison-spiking.md:63`). Le *TDP* (thermal design power) est la puissance
nominale utilisée pour convertir un temps de calcul en énergie.

**FPGA (Field-Programmable Gate Array) · Stratix V · Quartus · iverilog · RTL** —
Un FPGA est un circuit dont on peut reconfigurer le câblage logique ; le projet vise
une carte Intel (Altera) **Stratix V GS « Storey Peak »**. *RTL* (register transfer
level) désigne le code Verilog qui décrit le circuit au niveau des registres et des
transferts entre eux ; *iverilog* est le simulateur libre utilisé pour vérifier,
*Quartus Prime* la chaîne de synthèse propriétaire.
Le PE et le lecteur DDR3 ont été vérifiés et synthétisés, mais le moteur complet
n'a jamais tourné sur la carte (`reports/bilan-multi-materiel.md:22-27`,
`docs/roadmap.md:71-81`). **Réf.** : [iverilog](https://steveicarus.github.io/iverilog/) ;
Quartus Prime et Stratix V — documentations Intel citées sans lien.

**GPU · Quadro RTX 5000 · miroir VRAM · déport** — Les deux Quadro RTX 5000 (16 Go
chacune) servent de *déport* : le cache KV y est recopié en **miroir** paginé, ce
qui fait passer l'attention à 1 M de clés de 968 ms à 13,2 ms par couche (×73) et
rend le poste « attention » plat (3,3 ms/jeton) au lieu de croître linéairement
(`docs/contexte-long.md:212-297`). **Où** : `DRAVE_GPU`, `DRAVE_GPU_KV`,
`DRAVE_GPU_TETE`, `DRAVE_GPU_TOPK`, `DRAVE_GPU_EXPERTS`.

**Grandes pages · TLB · alignement 2 Mo** — Le *TLB* est le cache des traductions
d'adresses mémoire ; chaque page manquée coûte une marche de table. Des pages de
2 Mo au lieu de 4 ko divisent ce coût par 512, et l'alignement à 2 Mo du conteneur
proposé prépare leur usage (`reports/rapport-passage-a-l-echelle.md:160`,
`docs/convertisseur.md:146-148`).

**Grappe · `commun.gguf` · `cluster-XX.gguf`** — Forme éclatée d'un modèle :
`commun.gguf` porte embeddings, tête, attention, normes et **routeurs**, chaque
`cluster-XX.gguf` porte les tranches d'experts d'une grappe, et `mapping.tsv` relie
les deux. Un nœud qui ne sert que la grappe 0 charge 3,20 Go au lieu de 18,56 et
625 ms au lieu de 3,9 s (`docs/format-clusters.md:1-13`, `:78-89`).
**Où** : `tools/convertir_clusters.py`, `DRAVE_CLUSTERS`.

**L1 · L2 · ligne de cache · banque mémoire** — Mémoires internes du processeur, du
plus rapide (L1, quelques dizaines de Kio) au plus grand (L2 partagé, 256 Kio ici).
L'accumulateur du mode push doit tenir en L1 sous peine de s'effondrer ; les
banques mémoire imposent un rembourrage des tuiles transposées, sans quoi 32 voies
d'une lecture tombent dans la même banque (`reports/bilan-multi-materiel.md:132`,
`docs/contexte-long.md:219-224`).

**M20K** — Bloc de mémoire embarqué du FPGA Stratix V (20 kbit). L'accumulateur
d'un PE (4 096 × 24 bits = 12 Kio) tient dans les M20K ; la collecte irrégulière
des listes en consomme 41 % (`reports/rapport-cpu-aer.md:11`,
`reports/bilan-multi-materiel.md:95`).

**MAC (Multiply-Accumulate) · AC (Accumulate)** — *MAC* : une multiplication suivie
d'une addition, l'opération de base d'un réseau dense. *AC* : la seule addition,
suffisante quand les valeurs sont binaires — c'est l'économie des réseaux à spikes
et du ternaire (`docs/comparaison-spiking.md:59`). Une carte FPGA fournit ~312
voies de MAC, soit ~9 400 ALM (`reports/rapport-minimal.md:80-81`).

**mmap (memory-mapped file) · `madvise` · `DRAVE_MMAP`** — *mmap* projette un
fichier en mémoire : le noyau lit les pages à la demande au lieu de charger le
fichier. C'est ce qui permet d'ouvrir un GGUF de 365,7 Go avec 47 Mo de mémoire
résidente ; `DRAVE_MMAP=0` revient à `read_to_end`, qui duplique le modèle (9,32 s
et 6,35 Go contre 30,68 s et 19,20 Go en clusters)
(`docs/format-clusters.md:181-186`, `reports/rapport-architecture-memoire.md:372-376`).
`madvise(MADV_WILLNEED)` demande la prélecture, sans gain mesuré ici.
**Réf.** : [mmap(2)](https://man7.org/linux/man-pages/man2/mmap.2.html),
[madvise(2)](https://man7.org/linux/man-pages/man2/madvise.2.html).

**NUMA (Non-Uniform Memory Access) · nœud · UPI/QPI · premier-touch · `--pin`** —
Sur une machine bi-socket, chaque processeur a sa mémoire proche (*nœud NUMA*) et
les accès croisés passent par un lien inter-socket (*UPI* chez Intel, *QPI* chez
d'autres). Le *premier-touch* est la règle qui alloue une page sur le nœud du fil
qui l'écrit. Gain au banc : 20,7 → 24,7 Go/s ; mais sur la charge réelle,
l'épinglage `--pin` est une **perte** (23,2 → 27,6 s) — l'ordonnanceur fait mieux
seul (`docs/convertisseur.md:99-109`, `:236-242`).
**Réf.** : documentation noyau Linux, [docs.kernel.org/mm/numa.html](https://docs.kernel.org/mm/numa.html).

**Nœud partiel** — Nœud qui ne charge qu'une partie des grappes
(`DRAVE_CLUSTERS=0,3`) au lieu du modèle entier. Un cluster **demandé mais absent du
disque est une erreur**, pas un silence ; et rien n'additionne encore les
contributions de deux nœuds partiels (`docs/format-clusters.md:160-178`,
`reports/rapport-lecteur-multifichiers.md:125`).

**NVLink** — Lien direct entre cartes NVIDIA, mesuré à 25,78 Go/s ici, soit ~2× le
PCIe réel ; `cudaMemcpy` l'emprunte automatiquement
(`docs/convertisseur.md:95`, `reports/rapport-architecture-memoire.md:226`).

**NVMe · SSD · `O_DIRECT` · `pread`** — *NVMe* est le protocole des SSD rapides
branchés en PCIe ; *pread* lit à une position donnée sans déplacer le curseur ;
*O_DIRECT* demande à contourner le cache du noyau (il échoue ici, errno 29). Le
NVMe parallélisé à 16 lecteurs (31 Go/s) dépasse la RAM (22 Go/s) : c'est le chemin
retenu pour les experts (`reports/rapport-architecture-memoire.md:181-195`).
**Réf.** : [pread(2)](https://man7.org/linux/man-pages/man2/pread.2.html).

**PCIe (Peripheral Component Interconnect Express)** — Bus qui relie les cartes
d'extension. Mesuré à 6,5 Go/s en x8 Gen3 ici ; c'est **le goulot d'un montage
hybride** : envoyer un flux d'événements au GPU coûte plus cher que de le calculer
sur CPU tant que celui-ci tient 5,3 G événements/s (~10,6 Go/s d'événements), donc
« le seuil d'intérêt du GPU par PCIe est proche de 1 »
(`docs/convertisseur.md:85-109`). **Réf.** : PCI-SIG — cité sans lien.

**PE (Processing Element ; élément de calcul)** — L'unité qui traite un événement
par cycle dans le FPGA. Le dépôt en dimensionne le nombre selon la DDR3 : 51 voies
tiennent la carte, l'optimum du banc seul est 32 PE à 177 MHz
(`reports/bilan-multi-materiel.md:55`, `reports/rapport-cpu-aer.md:11`).

**QSFP+** — Lien réseau 4,8 Go/s envisagé pour chaîner plusieurs cartes FPGA
(`reports/bilan-multi-materiel.md:9`, `docs/convertisseur.md:94`).
**Réf.** : spécifications SFF, [snia.org](https://www.snia.org/technology-communities/sff/specifications).

**RAM · VRAM · RSS** — *RAM* : mémoire de l'hôte (125 Go ici) ; *VRAM* : mémoire des
cartes graphiques (2 × 16 Go, 30,2 Go exploitables) ; *RSS* (resident set size) :
mémoire réellement occupée par un processus. Le contraste qui résume le projet :
**47 Mo de RSS pour 365,7 Go de modèle adressé** en `mmap`
(`reports/rapport-architecture-memoire.md:370-376`).
**Réf.** : [proc(5)](https://man7.org/linux/man-pages/man5/proc.5.html).

**Roofline** — Modèle qui prédit si un calcul est borné par la puissance de calcul
ou par la bande passante mémoire ; le dépôt l'utilise pour projeter un modèle sur
un matériel donné (`src/roofline.py`, `docs/programme-recherche.md:11`).
**Réf.** : Williams, Waterman & Patterson, *Roofline: An Insightful Visual
Performance Model*, Communications of the ACM, 2009 — cité sans lien.

**USB** — Seul lien effectivement configuré du Stratix V dans le relevé matériel
(625 Mo/s), cinquante fois moins que le NVMe parallélisé — ce qui interdit d'y
déléguer le calcul (`reports/rapport-architecture-memoire.md:385-397`).

**Xeon E5-2687W v3 · CPU** — Le processeur du banc : 2 sockets × 10 cœurs (40 fils
logiques), 125 Go de RAM, jeu d'instructions AVX2. Toutes les mesures « CPU » du
dépôt sont faites dessus (`reports/bilan-multi-materiel.md:7`,
`reports/rapport-inference.md:5`).

---

