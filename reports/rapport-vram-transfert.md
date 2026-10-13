# La VRAM : ce qui coûte n'est pas le lien, c'est l'allocation

> Campagne : **machine et moteur** · expérience 02 — le transfert vers la VRAM, par expert
> Question : la direction du 12/10 demande, pour la VRAM, le même remède que pour le disque —
> « granularité fine, allocation intelligente au lieu de virtualiser une grande mémoire en
> lecture aléatoire ». Le cache d'experts VRAM actuel a été mesuré **perdant** (×1,09) ; avant de
> le refaire, il faut savoir **ce qui coûte** dans un transfert : le lien, ou autre chose ?
> Verdict : **l'allocation.** Monter un expert coûte **3,39 ms** (Q4_K, 0,88 Mo) et **11,72 ms**
> (MXFP4, 4,41 Mo) quand chaque montage alloue son tampon ; dans **un tampon réutilisé**, les
> mêmes octets montent en **0,27 ms** et **1,05 ms**. Autrement dit : **37 % du coût en Q4_K et
> 91 % en MXFP4 sont l'allocation**, pas le transfert. Le lien, lui, rend **5,2 Go/s** (Q4_K) et
> **4,2 Go/s** (MXFP4) en copies paginées.
> Date réelle : 2026-10-12, 22 h 50-23 h 00 HAE (heure lue sur la machine ; source : git, commit `334f8085`)
> Protocole : `drave --gpu-banc --matrix blk.0.ffn_gate_exps.weight` (`DRAVE_GPU=1`), 16 experts
> montés un par un, puis 15 dans un tampon réutilisé ; banc dans `main.rs`
> (`banc_transfert`), GPU 1 (Quadro RTX 5000)

## 1. Les mesures

| format | expert | allocation + copie | **copie dans un tampon réutilisé** | noyau GPU | noyau CPU (20 fils) |
|---|---|---|---|---|---|
| **Q4_K** (Qwen3-30B) | 0,88 Mo | 0,269 ms/expert (**3,29 Go/s**) | **0,171 ms/expert (5,17 Go/s)** | 0,1 ms (11,8 Go/s) | 1,3 ms (0,7 Go/s) |
| **MXFP4** (gpt-oss-120b) | 4,41 Mo | 11,718 ms/expert (**0,38 Go/s**) | **1,051 ms/expert (4,19 Go/s)** | 0,1 ms (29,7 Go/s) | 65,8 ms (0,1 Go/s) |

Ce que ça dit :

* **le cache VRAM actuel alloue à chaque montage** (`charger_mxfp4` par expert, dans
  `CacheExperts::obtenir`) : en MXFP4, il paie **onze fois** le prix du transfert en allocation.
  À 4,41 Mo l'expert, un jeton de gpt-oss qui monte 4 experts × 3 matrices par couche paie
  ~1,4 s **rien qu'en allocations** — de quoi expliquer, seul, le « ×1,09 perdant » mesuré ;
* **un tampon réutilisé change l'ordre de grandeur** : 4,19 Go/s en MXFP4, 5,17 en Q4_K — c'est un
  débit de lien PCIe Gen3 x16 en copies paginées, cohérent et reproductible ;
* **le noyau GPU, lui, n'est pas le problème** : 0,1 ms contre 1,3 ms (Q4_K) et **65,8 ms**
  (MXFP4) au CPU. Sur cette matrice, le GPU est **658× plus rapide** que le chemin CPU — l'écart
  est si grand qu'il rend le débat « faut-il déporter » caduc *si* le transfert est amorti.

## 2. Ce que le dessin doit faire (et ce que la mesure impose)

1. **un pool de tampons VRAM**, pas une allocation par expert : c'est 37 % à 91 % du coût, et
   c'est le seul changement qui ne demande aucune notion nouvelle ;
2. **recouvrir** : une copie de 0,17 ms (Q4_K) sous un noyau de 0,1 ms ne se recouvre pas
   (le noyau est plus court que la copie) — mais sous un **calcul CPU** de 1,3 ms, oui. C'est le
   double tampon qui décide, et il se mesure ;
3. **la granularité fine reste possible** : 1152 montages par jeton (48 couches × 8 experts ×
   3 matrices, Qwen3-30B) à 0,171 ms = **0,20 s par jeton** — à comparer aux ~0,9 s de calcul
   mesurés sur cette machine. Ce qui est hors de question, c'est de payer 0,269 ms **plus** une
   allocation par montage, ce que fait le chemin actuel.

## 3. Ce que cette fiche ne dit pas

* **elle ne dit pas que le déport GPU des experts gagne** : elle dit que le coût du transfert
  était dominé par l'allocation, et que le noyau GPU est très en avance sur le CPU **sur cette
  matrice**. Le verdict de bout en bout demande une passe complète avec le pool et le recouvrement
  — c'est le chantier suivant, et il a maintenant ses chiffres ;
* **elle ne mesure que des copies paginées** (`cuMemcpyHtoD_v2` sur de la mémoire hôte ordinaire).
  La mémoire épinglée (`cuMemAllocHost`) et les copies asynchrones iraient plus haut — à mesurer
  avant de conclure sur le plafond du lien ;
* **elle ne dit rien du cache** : le cache LRU peut rester utile quand les mêmes experts reviennent
  d'un jeton à l'autre (localité temporelle) ; ce qui est mesuré ici est le prix d'un **montage**,
  pas le taux de succès du cache.

## 4. Deux erreurs de banc, corrigées et notées

* **une géométrie 3D lue comme 2D** : `q4k_blocks` rend `dims[1]/256`, juste pour une matrice de
  projections et **faux** pour un tenseur d'experts `[n_experts, n_out, n_in]` — le banc annonçait
  « 0,1 Mo, 3 super-blocs » pour un expert de 0,88 Mo et 8 super-blocs. Le chemin de production ne
  s'y trompe pas (`charger_moe` calcule son pas), mais un banc qui se trompe de taille annonce un
  débit pour autre chose ;
* **une boucle qui ne tournait pas** : `let mut n = 0; for e in 1..=n.min(...)` — zéro tour, et la
  ligne « copie seule » ne s'imprimait pas. **Un silence qui ressemble à un succès** : c'est la
  même famille que « une mesure à un seul moment ne dit pas où ça casse » (`REPRISE.md` § 4).

---

## 5. Le pool, mesuré dans le moteur (13/10, 00 h 17)

Le **pool de tampons VRAM** est entré dans `CacheExperts` : les évictions rendent leurs matrices au
pool au lieu de les jeter, et un montage réutilise un tampon de la bonne forme (`gpu::recopier`),
sinon il alloue. Le budget compte **aussi** le pool, sans quoi on dépasserait la carte en croyant la
respecter.

Mesures — gpt-oss-120b MXFP4, 2 jetons, `DRAVE_GPU_EXPERTS_GO=8`, mêmes identifiants, données
chaudes en page cache (ce qui rend la comparaison **propre** : elle porte sur les montages, pas sur
le disque) :

| | temps mural | demandes | manques | montés sur le bus | **perplexité** |
|---|---|---|---|---|---|
| avant (allocation par montage) | 5,60 s | 288 | 264 (8,3 %) | 3,49 Go | 27736,1204 |
| **après (pool)** | **4,95 s** | 288 | 264 (8,3 %) | 3,49 Go | 27736,1204 |

**−11,6 % à travail identique** (mêmes 264 montages, mêmes 3,49 Go) : ~**2,5 ms par montage** de
13,2 Mo, là où le banc annonçait l'allocation à ~10 ms sur un tampon de 4,4 Mo — l'écart vient de ce
que le noyau et la lecture des blocs se recouvrent en partie. Perplexité **identique**.

**Et une défaite trouvée dans le même chemin** : `MatriceGpu` n'a **pas de `Drop`** — une éviction
laissait la VRAM allouée pour de bon, ce que le pool répare en gardant les tampons. La mesure
ci-dessus n'a **0 éviction** (le budget de 8 Go tenait les 3,49 Go) : la fuite demande un run plus
long pour se voir, et c'est écrit ici plutôt que supposé.

## 6. Un faux A/B, corrigé — et pourquoi il faut le dire

Le premier essai comparait les deux binaires **sans `DRAVE_GPU_EXPERTS`** : le cache n'était donc
pas créé (`cache_experts` est *opt-in*), les deux runs étaient **CPU**, et les 10,7 % d'écart
observés n'étaient que la **variance du disque dur** sur 13 Go de lectures. Le chiffre était
plausible et faux — c'est exactement ce que `REPRISE.md` § 4 appelle « une mesure à un seul moment
ne dit pas *où* ça casse » : sans vérifier que le chemin mesuré était **actif**, on compare deux
fois la même chose.
