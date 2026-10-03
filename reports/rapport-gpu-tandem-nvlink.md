# Le tandem GPU (2 × Quadro RTX 5000, NVLink) : ce qu'il fait, ce qu'il pourrait faire

> Question posée le 03/10 : « fais-tu bon usage du tandem de GPU en NVLink pour
> distribuer la charge principale ? »
>
> Réponse courte : **non — pour V4-Flash et V4.1, la charge principale (le MoE) est
> entièrement sur le CPU, et les deux GPU sont au repos.** Ce n'est pas un oubli :
> c'est la condition même du chemin GPU du moteur qui l'exclut. Ce rapport chiffre
> l'écart et ce qu'il faudrait pour le combler.

## 1. Le matériel, mesuré

```
GPU 0: Quadro RTX 5000 (16 Go)   GPU 1: Quadro RTX 5000 (16 Go)
topologie : GPU0 NV1 GPU1         (NVLink, 1 lien)
nvidia-smi nvlink -s : 25,781 Go/s par lien et par sens
NUMA : les deux GPU sur le node 0 (CPU 0-9,20-29)
PCIe : maximum Gen3 x16 (l'état courant oscille Gen1/Gen2 au repos — abaissement
       de veille classique, à revérifier sous charge)
```

Turing, 16 Go de VRAM chacun : **32 Go au total**, et 25,78 Go/s entre les deux
(soit ~4× le PCIe mesuré du dépôt).

## 2. Ce que le moteur fait des GPU aujourd'hui

Le principe est écrit dans `drave-core/src/gpu.rs` :

> « **les poids restent sur le GPU**. Mesuré : PCIe x8 6,5 Go/s contre 380 Go/s en
> lecture locale et 20 Go/s sur CPU. Déplacer les poids à chaque jeton coûterait
> plus cher que de les lire sur CPU ; ne traversent donc le bus que les activations
> (quelques kilo-octets). »

Implémenté et mesuré : le noyau de **tête**, la chaîne du **top-k** (les rapports
`rapport-aiguille-topk.md`, `rapport-gpu-topk-selection.md`), le **miroir VRAM du
cache KV**, et un **cache d'experts en VRAM** (`DRAVE_GPU_EXPERTS`) mesuré à
**+6 % seulement** sur gpt-oss-120b MXFP4, avec la mention « à ne pas activer par
défaut ».

Sur nos passes V4-Flash et V4.1, **aucun de ces chemins n'est actif** : le journal
du moteur l'annonce lui-même (« `[tête 4 bits] … 0 Mo` »). Les GPU sont au repos
pendant que 16 cœurs calculent.

## 3. Pourquoi : la condition « les poids restent en VRAM » n'est pas tenable ici

Nouvelle mesure de ce soir (`tools/analyse_octets_par_jeton.py`, en-têtes GGUF
seulement) — **octets de POIDS lus par jeton** :

| modèle | couches | experts | routés | **poids/jeton** | formats |
|---|---|---|---|---|---|
| V4-Flash IQ1_M | 43 | 256 | 6 | **2,669 Go** (experts seuls) | IQ3_XXS 33,7 · IQ1_M 20,7 · IQ2_XXS 23,3 · MXFP4 … |
| V4.1 Q2 | 40 | 384 | 6 | **3,893 Go** (experts seuls) | I8 202,8 · IQ2_XXS 93,4 · Q2_K 59,5 |

> ⚠️ **Ces deux chiffres ne comptent que les experts** (l'outil
> `analyse_octets_par_jeton.py` a été écrit pour la question du MoE). Le trafic
> **total** d'un jeton ajoute l'attention, les experts partagés et la tête :
> **8,56 Go** pour V4-Flash et **87 Go** pour Kimi-K3 Q4
> (`reports/rapport-budget-kimi-k3.md`, `tools/budget_execution_locale.py`). Le
> rapport sur les planchers de bus ci-dessous doit donc être lu avec le total :
> l'écart entre les deux chiffres est ce qui a fait sous-estimer le problème.

Or la VRAM disponible est de **32 Go** : un cache d'experts ne peut donc tenir, au
mieux, qu'une fraction du modèle — et un jeton a besoin de 2,7 à 3,9 Go de poids
**par pas**. Les planchers théoriques, à partir des débits mesurés :

| chemin | débit | V4-Flash | V4.1 |
|---|---|---|---|
| VRAM locale (poids résidents) | 380 Go/s | 7 ms/jeton | 10 ms/jeton |
| lecture CPU (RAM) | 20 Go/s | 133 ms/jeton | 195 ms/jeton |
| **bus PCIe (x8 mesuré)** | 6,5 Go/s | **411 ms/jeton** | **599 ms/jeton** |
| disque dur 12 To (ROTA, non caché) | ~200 Mo/s | **13,3 s/jeton** | 19,5 s/jeton |

Face à cela, le CPU fait aujourd'hui **2,06 s/jeton** (V4-Flash, `DRAVE_SIMD_DOT=1`,
ctx 64) et **4,3 s/jeton** (V4.1, ctx 32). Autrement dit : **le CPU est 5 à 7 fois
au-dessus du plancher PCIe** — il n'est pas limité par la mémoire (133 ms/jeton à
20 Go/s), mais par le **calcul de déquantification + produit scalaire**.

## 4. Ce qu'un « bon usage du tandem » voudrait dire, et ce que ça coûte

**Piste A — les modèles qui tiennent en VRAM (≤ 16 Go, ou ≤ 32 Go à deux).** C'est
le cas prévu par le moteur, et c'est là que le tandem est déjà bon : poids
résidents, activations sur le bus. Pour ces modèles, NVLink sert à mettre en commun
les 32 Go (un expert demandé par le GPU 1 et présent chez le GPU 0 arrive à
25,78 Go/s au lieu de 6,5).

**Piste B — les gros MoE (V4-Flash, V4.1) : un chemin « streaming ».** C'est la
seule façon de faire travailler le tandem sur la charge principale, et elle coûte
**411 à 599 ms/jeton de bus** — donc un potentiel de **×5 à ×7** sur l'état actuel.
Mais ce chemin **n'existe pas** et demande :

1. des tampons **pinned** côté hôte (un `mmap` pageable se copie à moitié vitesse) ;
2. des **noyaux PTX de déquantification** pour IQ1_M, IQ2_XXS, IQ3_XXS, Q2_K, Q4_K,
   Q5_K — c'est-à-dire ce que llama.cpp appelle ses noyaux MMQ/IQ ;
3. un **regroupement par expert** par couche (6 experts × 43 couches, avec
   double-tampon pour recouvrir le transfert par le calcul) ;
4. la gestion de deux GPU (moitié des couches chacun, ou experts pairs/impairs) —
   c'est là que NVLink compte, pas pour l'hôte.

**Le chiffre qui décide, et qui n'est pas encore mesuré** : le débit réel
hôte → device sur *cette* machine, sous charge, avec `cudaMemcpyAsync` sur mémoire
pinned. Le dépôt cite 6,5 Go/s en x8 ; les cartes annoncent x16 Gen3. Si le banc
donne ≥ 5 Go/s, la piste B vaut ses semaines de travail ; s'il donne 1-2 Go/s, elle
ne les vaut pas et la réponse reste « le CPU, avec de meilleurs noyaux ».

## 5. Ce que je propose de mesurer avant d'écrire la moindre ligne de CUDA

1. **Banc de bus** (½ h) : tampon pinned, transferts de 1-2 Go répétés, débit
   aller, retour, et **largeur de lien sous charge** (pour savoir si c'est x8 ou
   x16 en pratique).
2. **Banc de noyau** (½ h) : un noyau PTX qui déquantifie un super-bloc IQ1_M et
   fait le produit scalaire de 256 valeurs — comparé au même travail sur CPU. Le
   moteur a déjà un banc GPU (`--gpu-banc`) et un noyau de tête : la mécanique
   d'écriture d'un noyau PTX et de son lancement est en place.
3. **Recouvrement** : mesurer le débit utile d'une boucle double-tamponnée
   (transfert du bloc *n+1* pendant le calcul du bloc *n*). C'est le vrai chiffre :
   sans recouvrement, le bus s'ajoute au calcul au lieu de le remplacer.

Tant que ces trois chiffres ne sont pas sur la table, « distribuer la charge
principale sur le tandem » reste une intuition de topologie — et le dépôt a déjà
trois exemples de telles intuitions réfutées par la mesure (cache VRAM d'experts
+6 %, cache RAM d'experts plus lent, épinglage NUMA perdant).
