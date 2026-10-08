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
