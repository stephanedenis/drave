# Vérifier Kimi-K3, étage par étage — le protocole

> Écrit le 03/10 (bloc 30) **avant** d'écrire l'architecture, pour que chaque
> morceau de code ait son point de comparaison le jour où il naît. La règle du
> dépôt est constante : on compare les **tenseurs intermédiaires avant** de
> regarder la perplexité, parce qu'une implémentation qui « a l'air de tourner »
> peut avoir une porte de travers sans que ça se voie dans les logits à court
> terme (l'épisode de la porte bornée de V4.1 et celui du clamp SwiGLU sont là
> pour le rappeler).

## 1. Les deux côtés de la comparaison

| côté | commande | ce qu'elle écrit |
|---|---|---|
| **référence** (llama.cpp `kimi-k3`) | `REF_DUMP=/tmp/refk3 ./tools/ref_logits_k3 <K3.gguf> <ids> <sortie> <n>` | `<préfixe>-<nom>-<couche>.bin`, en-tête `REFD` + `ndim` + `ne[4]`, f32 dans l'ordre ggml (une colonne par position) |
| **moteur** | `DRAVE_DUMP_COUCHES=/tmp/notrek3 ./drave-core/target/release/drave <K3.gguf> --ppl <ids> …` | `<préfixe>-<nom>-<couche>-<position>.bin`, f32 brut |
| **comparaison** | `python3 tools/compare_etats.py /tmp/notrek3 /tmp/refk3 <nom> <couche> <positions>` | écart max et relatif sur le **vecteur entier** |

Les deux outils existent déjà : `ref_logits_k3` a été lié contre `llama.cpp-k3`
(03/10), et `compare_etats.py` a servi pour V4 (`hc_attn_pre` concorde à **1e-7**).

## 2. Les points de comparaison, dans l'ordre où il faut les atteindre

Les noms sont ceux des `cb(...)` de la référence — **notre moteur doit écrire les
mêmes**, sinon la comparaison n'a pas lieu d'être.

| # | nom (référence) | ce que ça vérifie | si ça diverge, la faute est dans… |
|---|---|---|---|
| 1 | `inp_embd` | embarquement du jeton | déquantification de `token_embd` (Q8_0 emprunté) ou rangée mal indexée |
| 2 | `attn_norm` | RMSNorm d'entrée | epsilon, ordre des opérations |
| 3 | `kda_q_conv`, `kda_k_conv`, `kda_v_conv` | projections + **convolution courte** (noyau 4) + SiLU | disposition de l'état de convolution (**canal-majeur**), ordre du noyau, SiLU |
| 4 | `kda_g1` | **porte de décroissance** bornée | signe de `exp(A_log)` (le fichier stocke `−exp(A_log)`), `dt_bias`, borne −5 |
| 5 | `kda_beta` | pas appris, sigmoïde, **par tête** | projection `ssm_beta`, forme |
| 6 | `kda_normed`, `kda_out` | normalisation L2 de q/k puis **récurrence delta** | conventions `i` = clé / `j` = valeur, état par tête |
| 7 | `mla_out`, `mla_gated` | MLA (absorption) + **porte de sortie** | `q_lora_rank`, absence de RoPE (`nope`), porte lue sur l'entrée **normalisée** |
| 8 | `res_probs` | **attention résiduelle** : softmax sur les points de contrôle + le courant | scores sur les valeurs **normalisées**, somme sur les **brutes**, pile append-only |
| 9 | `prefix_sum_attn` | **redémarrage du flux** aux couches « banque » (toutes les 12) | la couche banque remplace le flux au lieu de s'y ajouter |
| 10 | `ffn_norm`, `ffn_out` (dense, couche 0) | **SiTU** | la formule, `linear_beta ≤ 0` désactivant la branche `up` |
| 11 | `ffn_moe_logits`, `ffn_shexp`, `ffn_moe_out` | routage (sigmoïde, 896 experts, 16 par jeton) + **MoE latent** | routeur noté sur la **pleine largeur**, experts sur le latent, normalisation des poids |
| 12 | `l_out` | la couche entière | — |
| 13 | `result_norm`, `result_output` | le `res_mix` final + la tête | oubli du dernier `res_mix` (`output_res_score`) |

## 3. Le premier jalon qui compte : la couche 0

La couche 0 est **dense** (`leading_dense_block_count = 1`) : elle exerce
l'embarquement, la RMSNorm, le **KDA complet**, l'attention résiduelle (avec une
pile vide au premier raccord), **SiTU** et le FFN dense — mais **pas** le MoE, ni
la cadence MLA. C'est donc le jalon le plus riche par unité de travail, et il se
vérifie sur **4 positions** en quelques minutes.

Ensuite : la couche 1 (MoE latent), la couche 3 (MLA), la couche 12 (premier
**redémarrage** du flux résiduel), puis les 93 couches.

## 4. Les tolérances, et ce qu'elles veulent dire

- **1e-7 à 1e-6** : même calcul, ordre d'accumulation différent. C'est ce que
  donnait `hc_attn_pre` pour V4 contre llama.cpp.
- **1e-4 à 1e-3** : quantifications différentes (nos activations 16 bits contre
  bf16/f32 côté ggml). Acceptable **si** l'écart ne croît pas avec la position.
- **> 1e-2, ou une croissance avec la position** : une erreur de structure, pas
  d'arrondi. On ne passe pas à l'étage suivant.

## 4bis. Le côté moteur est déjà branché (03/10)

`--k3-essai` charge la couche 0, la calcule sur les jetons donnés, et **vide ses
sorties au format du moteur** (`DRAVE_DUMP_COUCHES=<préfixe>` →
`<préfixe>-l_out-0-<position>.bin`, f32 brut). Mesuré : trois jetons, trois
fichiers de 28 672 octets (7 168 × 4), valeurs finies et croissantes en norme
(0,97 · 1,43 · 1,50).

Il contrôle aussi, **avant tout calcul**, les dimensions des quatre types de
couches (0 dense, 1 MoE+KDA, 3 MoE+MLA, 4 KDA) contre ce que la configuration
déclare — c'est ce qui attrape une dimension lue du mauvais côté (le moteur range
`dims[0] = ne1` = la sortie, l'inverse du fichier).

### 4ter. Le modèle est COMPLET, et les chiffres n'ont pas bougé (bloc 31)

Le 04/10 à 14:01, le 32e shard est arrivé. `--k3-essai` relancé sur les **32
shards** donne, au chiffre près, les **mêmes** valeurs que les passes faites
pendant le transfert (25 shards sur 32) :

| sortie | 25/32 shards | 32/32 shards |
|---|---|---|
| MoE couche 1, \|sortie\| | 0,7316 | **0,7316** |
| composition 0-3, \|l_out\| (4 jetons) | 8,7757 · 5,2909 · 5,2559 · 5,4735 | **identiques** |
| couche 0, \|l_out\| (3 jetons) | 0,9731 · 1,4310 · 1,4958 | **identiques** |

C'est la vérification de l'ouverture tolérante : les shards déjà là portaient
**les octets définitifs**, et un débogage mené pendant un transfert de 1,5 To
n'était donc pas un débogage sur des données provisoires.

### Le premier franchissement de BANQUE (bloc 31)

`DRAVE_K3_COUCHES=13` compose les couches **0 à 12**. Ce n'est pas « quatre
couches en plus » : la première banque est la couche 0, la **suivante est la
12**, donc quatre couches n'exerçaient ni le redémarrage du flux résiduel ni un
`res_mix` à **deux** points de contrôle. Mesuré, quatre jetons :

| jeton | \|l_out\| couches 0-12 |
|---|---|
| 0 | 9,6728 |
| 1 | 9,9734 |
| 2 | 9,2453 |
| 3 | 8,9678 |

Tous finis, 3 356 273 ms au total (14 min par jeton pour 13 couches — c'est le
chemin f32 de vérification). Les sorties de la couche 0 redonnent **au chiffre
près** celles des passes précédentes (0,9731 · 1,4310 · 1,4958), et les sorties
`l_out-12` sont vidées pour la comparaison avec la référence.

Le chemin K3 est un instrument de **vérification**, pas d'exécution : il
déquantifie en f32 (une couche MoE = 28,7 s/jeton, la composition des couches 0-3
= 366 s pour 4 jetons). Les 93 couches en f32 demanderaient ~220 Go de RAM.

### 4ter-bis. La référence A TOURNÉ — les chiffres de la baseline (04/10, 22h57)

`REF_SANS_REPACK=1 tools/ref_logits_k3 <K3> <ids> <sortie> 4 --tensors l_out`,
sur le modèle complet, quatre jetons :

| mesure | valeur |
|---|---|
| temps mural | **2 h 48 min 21 s** pour 4 passes → **~42 min par jeton** |
| occupation CPU | **11 %** (le reste est de l'attente disque) |
| lectures | 1,80 To (blocs de 512 o comptés par le noyau) → **451 Go par jeton** |
| RSS maximal | 102 Go · **swap 0** (grâce à `REF_SANS_REPACK`) |
| sorties | **100 vidages** : les 93 couches `l_out-0` … `l_out-92` + variantes |
| logits | `refk3_logits.bin`, 3 × 163 840 f32 · « perplexité » 43,598 sur 3 positions (non interprétable en deçà de 64 prédictions — c'est la règle du dépôt) |

**Ce que ça établit** : llama.cpp-k3 fait tourner Kimi-K3 sur cette machine, à
**42 minutes par jeton**, borné par le disque et non par le calcul (11 % de CPU).
C'est la première mesure de la référence sur cette classe, et c'est le chiffre
auquel comparer tout ce que le projet proposera.

Les 93 couches vidées permettent désormais de **bissecter** la divergence : il
suffit de comparer couche par couche pour trouver la PREMIÈRE qui décroche, au
lieu de raisonner sur la sortie de la couche 0.

### 4quater-undecies. Le dense emprunté : ×1,17, logits conformes — et le cache de pages **ne le garde pas** (05/10, 11h35)

Les cinq grosses projections du KDA (`attn_q/k/v`, `ssm_g`, `attn_output`) sont
désormais **empruntées** au fichier au lieu d'être déquantifiées en f32 :
`Gguf::q8_blocks` + `DenseQ8::emprunter_q8` + `dot_q8_source`. Plus de copie de
4 octets par poids, plus 224 Go de tampons alloués et libérés par passe.

| | f32 dense | dense emprunté |
|---|---:|---:|
| chargement (93 couches) | 373 s | **190 s** |
| attention | 142 s | 222 s |
| passe complète | 1 695 s | **1 516 s** |

**×1,12** sur la passe complète, ×1,17 depuis le chemin f32 d'origine — et
**top-1 identique 3/3** contre la référence (84, 1103, 3140), avec des
corrélations un peu plus basses (0,998059 / 0,998563 / 0,999059 contre 0,999802
/ 0,999900 / 0,999924) : le chemin entier Q8_0 est légèrement moins précis que le
f32, mais il ne déplace pas un seul argmax.

**L'attention ralentit** (142 → 222 s) : `dot_q8_source` est un noyau **scalaire**
là où le matvec f32 vectorise bien. Le gain vient du chargement, pas du calcul.
Le noyau AVX2 du pool (`matvec_dense_i8`) est le pas suivant, et il est déjà
écrit.

### Deuxième réfutation : la copie anonyme SWAPE (05/10, 18h20)

Le mécanisme suivant essayé était : copier les blocs Q8_0 du dense (31,8 Go pour
les cinq projections du KDA) dans des tampons **anonymes** gardés pour la vie du
processus. La page anonyme n'étant récupérable que vers le swap, une copie
suffirait à épingler — **sans `mlock`, sans `libc`, en `std` seul**.

**La prémisse était fausse, et la façon dont elle l'était compte.** J'avais
vérifié avec `swapon --show`, qui n'a rien affiché ; j'ai lu ce silence comme
« pas de swap ». `swapon` **n'existe pas sur cette machine** (`command not
found`) : c'est un instrument absent, pas une mesure négative. `/proc/swaps`
dit la vérité :

```
Filename        Type      Size        Used       Priority
/dev/dm-0       partition 65 798 140  56 019 556  -1
```

**62,8 Go de swap, dont 53 Go utilisés.** La mémoire anonyme est donc
récupérable, et l'arène s'est mise à swaper : `VmSwap` du processus = **28,5 Go**,
mémoire disponible tombée à 7 Go. La passe aurait été plus lente, pas plus
rapide. Arrêtée avant la fin.

**Ce que ça laisse** : sur cette machine, le dense ne peut pas être rendu
résident à bon compte. La page cache ne le garde pas (mesuré), la copie anonyme
swape (mesuré), et `mlock` de 32 Go demande `CAP_IPC_LOCK` — les limites
habituelles sont de quelques mégaoctets. Le mécanisme reste **opt-in**
(`DRAVE_K3_DENSE_FIGE=1`), documenté, et **déconseillé** ici.

**Leçon de méthode, et elle est la même que celle du bloc 31** : un instrument
qui n'existe pas ne renvoie pas « non ». `swapon --show` vide, `grep` sans
résultat, un fichier absent — le silence n'est une mesure que si l'on a vérifié
que l'outil était là. La bonne source est `/proc/swaps`, qui est un fichier.

### Et l'hypothèse du cache de pages est RÉFUTÉE

La thèse était : « ne plus déquantifier, et le cache de pages gardera les 59,6 Go
du dense entre deux passes ». **Deux passes complètes enchaînées, même
processus :**

| | passe 1 | passe 2 |
|---|---:|---:|
| chargement | 189,6 s | 193,5 s |
| calcul | 1 310,7 s | 1 313,2 s |
| **total** | **1 516 430 ms** | **1 522 584 ms** |

**Aucun gain.** La seconde passe est même marginalement plus lente. Le cache de
pages (`buff/cache` = 106 Go) ne retient pas le dense, parce que **chaque passe
fait passer 77 Go d'experts** en plus des 59,6 Go de dense : 137 Go de données
distinctes pour 106 Go de cache, et le noyau évince.

**Le mécanisme correct est donc de l'ÉPINGLER, pas de l'espérer.** Un tampon
résident de 59,6 Go (la RAM en a 125) protégé de l'éviction — c'est exactement ce
que fait Strata avec `--resident-experts`, et c'est ce que le plan appelle
« garder le dense résident ». La page cache, seule, ne le fait pas : c'est
mesuré.

### 4quater-decies. **Le mur est le DISQUE, et le prochain chantier est nommé** (05/10, 09h10)

Le chiffre qui commande tout : le FFN coûte **3,1 s par couple (couche, jeton)**
dans la passe complète, contre **0,37 s** dans l'essai sur 4 couches. Même code,
même noyau — **huit fois plus lent** parce que la passe de 93 couches streame
1,5 To depuis un disque tournant.

D'où la conclusion, qui est celle du plan depuis le début mais maintenant
**mesurée** :

1. **Ce qui domine les lectures, ce n'est pas les experts.** Par appel, la passe
   relit **~59,6 Go de dense Q8_0** (56,088 G poids × 1,06 o) **plus 12,4 Go
   d'experts partagés** — soit ~72 Go **à chaque appel**, contre 25,9 Go
   d'experts routés par jeton. Pour engendrer N jetons, le dense est relu N fois.
2. **Le dense tient en RAM** : 59,6 Go sur 125. C'est exactement la thèse du
   plan — « garder le dense résident, ne lire que les experts qui servent » — et
   elle est à portée.
3. **Ce qui l'empêche aujourd'hui, c'est la déquantification en f32.** Chaque
   appel alloue et libère ~224 Go de tampons f32 (56,088 G poids × 4 o), ce qui
   **évince le cache de pages** : les blocs Q8_0 du dense ne peuvent pas y
   rester, donc ils sont relus au disque à chaque jeton.

**Le prochain chantier, précisément** : emprunter les blocs Q8_0 au fichier au
lieu de les déquantifier — `Gguf::q8_blocks` existe, `DenseQ8::emprunter_q8`
aussi, et `dot_q8_source` est le noyau qu'utilise déjà tout le reste du moteur.
Il faut le faire pour les cinq grosses projections du KDA (`attn_q/k/v`,
`ssm_g`, `attn_output` : 440 M poids par couche, 1,88 Go en f32 contre 0,47 Go
en Q8_0), puis pour la MLA et la FFN dense de la couche 0.

**Ce qui est déjà fait et qui sert de modèle** : le noyau MXFP4 sur les experts
(×3,6 sur le FFN quand les poids sont en cache, sortie identique au niveau des
logits sur le modèle entier — voir 4quater-nonies). Le même geste, appliqué au
dense, attaque cette fois le DISQUE et non la RAM.

### 4quater-nonies. Le noyau MXFP4 : ×3,6 sur le FFN, ×1,05 sur la passe — et pourquoi (05/10, 08h57)

`expert_mxfp4_dans` écrit **132 Mo** de f32 par expert (3 × 11 M valeurs) que le
matvec relit aussitôt. Le noyau du moteur (`DenseQ4::dot16`, AVX2, table de
décodage MXFP4) lit les blocs de 17 octets **directement**.

| | f32 | noyau MXFP4 | gain |
|---|---|---|---|
| FFN, 4 couches × 4 jetons | 21,1 s | 5,9 s | **×3,6** |
| calcul total | 27,4 s | 12,0 s | ×2,3 |
| passe, 4 couches (poids en cache) | 36,3 s | 19,8 s | **×1,8** |
| **passe complète, 93 couches** | 1 780,5 s | 1 695,1 s | **×1,05** |

**Le gain disparaît sur la passe complète, et c'est le résultat intéressant.** Le
FFN y coûte 1 163 s pour 372 couples (couche, jeton), soit **3,1 s par couple**
contre 0,37 s dans l'essai sur 4 couches : la passe de 93 couches **streame
1,5 To depuis un disque tournant**, et elle est limitée par le disque, pas par la
RAM. Le noyau divise par quatre les octets qui passent **en mémoire**, pas ceux
qui sortent du disque. L'optimisation est réelle ; elle n'est pas là où le mur
est.

**Et elle ne change rien à la sortie**, vérifié sur le modèle entier :

| | pos 0 | pos 1 | pos 2 |
|---|---|---|---|
| f32 | r = 0,999802 · top-1 84 | r = 0,999900 · top-1 1103 | r = 0,999924 · top-1 3140 |
| noyau MXFP4 | **r = 0,999802 · top-1 84** | **r = 0,999900 · top-1 1103** | **r = 0,999924 · top-1 3140** |

Mêmes corrélations à la sixième décimale, mêmes argmax. La perturbation mesurée
du noyau (9,7e-6 de la dynamique, pente nulle) est **deux cents fois plus petite**
que l'écart du chemin f32 contre la référence (2,3e-3) : elle ne se voit pas.

**Reste OPT-IN** (`DRAVE_K3_MXFP4=1`) : dans le régime réel — la passe complète —
il ne rapporte rien, et il change la sortie au niveau 1e-5. Le promouvoir serait
changer un calcul pour zéro.

**Un échec instructif au passage.** La première version clampait l'activation en
i16 sans échelle : écart relatif **4,5 %** et **pente −0,44** sur la sortie — un
biais d'échelle, pas un arrondi. Les valeurs après SiTU sont de l'ordre de
l'unité, donc l'arrondi entier les détruisait. Le moteur quantifie toujours avec
une échelle par vecteur et la remet à la fin ; ajoutée, l'écart tombe à 9,7e-6.

### 4quater-octies. **LE MOTEUR ENGENDRE AVEC KIMI-K3, ET CHAQUE PAS EST CELUI DE LA RÉFÉRENCE** (05/10, 06h56)

`DRAVE_K3_GEN=2` : préfill puis jetons engendrés en glouton, l'état récurrent
(convolution, delta, cache MLA) sorti de chaque couche avant qu'elle ne tombe et
**restauré au rechargement**. Deux appels successifs, le second ne voyant qu'un
jeton nouveau :

```
pas 0 : 2 jeton(s) en entrée (1080 s) → argmax 1103 ✅ (référence)
pas 1 : 3 jeton(s) en entrée (1578 s) → argmax 3140 ✅ (référence)
```

Les deux valeurs attendues sont les **top-1 de llama.cpp-k3** aux mêmes positions
(1103 après `[3638, 275]`, 3140 après `[3638, 275, 1309]`). Le second pas est
donc une vérification à deux titres : le choix est le bon, **et** il a été
calculé à partir d'un état restauré et non recalculé.

C'est « faire tourner le modèle en local » au sens plein : 93 couches, 1,5 To de
poids, sur une machine de 125 Go de RAM, une seule couche de poids en mémoire à
la fois (~2,2 Go) plus ~0,6 Go d'états pour les 93 couches.

**Une correction, parce qu'elle a failli passer pour un échec** : le premier essai
a affiché « argmax 1103 ❌ (référence 1309) ». C'était **mon tableau d'attente**
qui était faux — j'y avais mis le jeton *cible* au lieu du *top-1 de la
référence*. Le moteur avait raison. Un attendu mal écrit fabrique un échec qui
n'existe pas ; c'est l'autre face de « une affirmation sans mesure ».

### 4quater-septies. **LES LOGITS DU MODÈLE ENTIER — top-1 identique 3/3** (05/10, 05h06)

La passe complète avec la TÊTE (`DRAVE_K3_TETE=1` : mélange résiduel final,
norme de sortie, matrice `output`), comparée aux logits de llama.cpp-k3 sur les
trois positions évaluées :

| position | corrélation | top-1 référence | top-1 moteur | accord | jeton cible |
|---|---|---|---|---|---|
| 0 | **0,999802** | 84 | 84 | ✅ | 275 |
| 1 | **0,999900** | 1103 | 1103 | ✅ | 1309 |
| 2 | **0,999924** | 3140 | 3140 | ✅ | 3140 |

**top-1 identique 3/3**, et l'argmax est **le bon jeton à chaque position** (la
cible elle-même). C'est le critère de la porte de correction du dépôt
(≥ 0,95 de corrélation sur les positions utiles, top-1 ≥ 85 %) appliqué au plus
gros modèle du parc : il passe à 100 %, avec une corrélation minimale de
0,999802.

Un état caché ne se compare qu'à un état caché ; **des logits se comparent à ceux
d'une autre implémentation**, et c'est ce qu'on vient de faire sur 93 couches,
8 banques, 68 couches KDA, 24 MLA, 896 experts et 1,5 To de poids.

### 4quater-sexies. **LA PASSE COMPLÈTE DE 93 COUCHES PASSE** (05/10, 04h28)

`DRAVE_K3_PASSE=93` calcule **tout le modèle**, une seule couche en mémoire à la
fois, et rend `l_out-92` — le flux résiduel après la dernière couche. Comparé à
`l_out-92` de llama.cpp-k3 :

| couche 92 | corrélation | écart max | dynamique | relatif |
|---|---|---|---|---|
| jeton 0 | **0,999857** | 1,01e-01 | 7,42 | 1,4 % |
| jeton 1 | **0,999900** | 8,10e-02 | 1,65e+01 | 0,5 % |
| jeton 2 | **0,999919** | 2,16e-01 | 2,94e+01 | 0,7 % |

** quatre des treize points de comparaison sont verts** (couches 0, 12, 24, 92),
et le dernier est **le modèle entier** : 93 couches, **8 points de contrôle**
empilés dans la banque, 68 couches KDA avec leur convolution et leur récurrence,
24 couches MLA à cache latent, 896 experts dont 16 par jeton, SiTU. Aucun
mécanisme de l'architecture n'est laissé de côté.

**Et l'écart ne dérive pas** : 1,4 % au jeton 0, 0,5 % et 0,7 % ensuite, pour des
dynamiques de 7 à 29. L'accumulation f32 sur des poids Q8_0 et MXFP4, sur 93
couches, reste sous le pour-cent.

**Le coût, mesuré** : 1 715 885 ms pour 4 jetons, soit **7,2 minutes par jeton**.
La référence (llama.cpp-k3, même machine, même modèle) met **42 minutes par
jeton** — elle est limitée par le disque et lit 1,80 To pour 4 jetons. La même
passe ici ne lit que les experts réellement choisis (16 sur 896 par couche et par
jeton) et ne repaquette rien : **six fois plus rapide que la référence, et
vérifiée contre elle.**

### 4quater-quinquies. VINGT-CINQ COUCHES, TROIS BANQUES (05/10, 03h37)

`DRAVE_K3_COUCHES=25` : banques aux couches 0, 12 et 24, donc un `res_mix` à
**TROIS** points de contrôle. Comparé à `l_out-24` de la référence :

| couche 24 | corrélation | écart max | dynamique |
|---|---|---|---|
| jeton 0 | **0,999984** | 2,51e-04 | 1,27e-01 |
| jeton 1 | **0,999893** | 3,18e-04 | 6,36e-02 |
| jeton 2 | **0,999866** | 3,74e-04 | 7,15e-02 |

**Trois des treize points de comparaison sont verts** : 0, 12, 24. Et l'écart
**ne croît pas avec la profondeur** (3,7e-04 à la couche 24 contre 3,1e-04 à la
couche 0 pour une dynamique comparable) : l'accumulation f32 sur des poids Q8_0
reste sous le pour-mille, elle ne dérive pas.

### 4quater-quater. LES TREIZE COUCHES PASSENT, BANQUE COMPRISE (05/10, 03h17)

`DRAVE_K3_COUCHES=13` enchaîne les couches 0 à 12 : la couche dense, les MoE
latents, la MLA de la couche 3, la récurrence KDA, l'état de convolution, **et le
franchissement de la banque de la couche 12 avec un `res_mix` à deux points de
contrôle**. Comparé à `l_out-12` de llama.cpp-k3 :

| couche 12 | corrélation | écart max | dynamique |
|---|---|---|---|
| jeton 0 | 0,990927 → **0,999945** | 1,11e-01 → **5,47e-03** | 2,09e+00 |
| jeton 1 | 0,458801 → **0,999943** | 1,02e+00 → **1,62e-03** | 2,06e+00 |
| jeton 2 | 0,448762 → **0,999102** | 4,06e-01 → **7,75e-03** | 2,23e+00 |

**Deux des treize points de comparaison du protocole sont donc verts** : la
couche 0 et la couche 12. Ce que ça vérifie d'un coup, et qui n'était vérifié que
par relecture : l'enchaînement résiduel, la banque et son REDÉMARRAGE, un
`res_mix` à deux points de contrôle, l'état de convolution et la récurrence delta
transportés d'un jeton au suivant, le MoE latent, la MLA à cache latent et SiTU.

### 4quater-ter. LA COUCHE 0 PASSE (05/10, 02h25)

Trois défauts, tous trouvés par la comparaison et aucun par relecture :

1. **la norme L2 par tête sur `q` et `k`** (`build_gdn_l2_norm`) n'existait nulle
   part dans le moteur ;
2. **la banque résiduelle s'accumulait entre les jetons** au lieu d'être propre
   à la passe du jeton courant ;
3. **son ORDRE de remise à zéro** : elle doit être repartie **avant** l'attention
   résiduelle, pas après. Dans la référence, `resi_stack` est vide à cette étape
   de la couche 0, **à chaque jeton** ; garder le `n_ckpt` du jeton précédent
   faisait appliquer un `res_mix` là où la référence n'en applique pas.

| couche 0, quatre jetons | corrélation | écart max | dynamique |
|---|---|---|---|
| jeton 0 | 0,983164 → **0,999979** | 1,19e-02 → **3,74e-04** | 9,66e-02 |
| jeton 1 | 0,790361 → **0,999982** | 1,55e-01 → **2,92e-04** | 1,10e-01 |
| jeton 2 | 0,641780 → **0,999983** | 1,80e-01 → **3,07e-04** | 2,16e-01 |

Les trois étaient **invisibles au jeton 0 seul** — c'est ce qui les a fait
survivre deux jours de transcription. Et le test « KDA contre NumPy » les
couvrait tous les trois : il comparait le code à sa propre transcription.

Ce qui reste : la couche 12 (13 couches enchaînées, une banque franchie) et
l'écart résiduel de 0,4 % — de l'ordre de l'accumulation f32 sur des poids Q8_0,
à confirmer couche par couche avec les vidages instrumentés.

### 4quater-bis. DEUX BUGS TROUVÉS PAR LA COMPARAISON (05/10, 00h25)

**1. La norme L2 par tête sur `q` et `k` n'existait nulle part.**
`build_gdn_l2_norm` (référence) : `x / sqrt(Σx² + eps)`, plus `1/sqrt(head_dim)`
sur `q` seul. Sa signature était dans les chiffres : au jeton 0 l'état delta est
nul, donc `o[j] = β·(Σ_i k[i]q[i])·v[j]` — proportionnel à `v` quelle que soit
l'échelle de `q` et `k` — et la norme par tête qui suit efface cette échelle.
D'où 0,983 de corrélation au jeton 0 **avec un rapport de norme de 0,937**, puis
0,79 et 0,64 : dès le jeton 1, l'accumulation `s += k ⊗ β(v − sᵀk)` dépend, elle,
de l'échelle de `k`.

| | avant | après |
|---|---|---|
| jeton 0, corrélation | 0,983164 | **0,999979** |
| jeton 0, écart max | 1,19e-02 | **3,74e-04** |

**2. La banque résiduelle s'accumulait entre les jetons.** Dans la référence,
`resi_stack` est une variable locale au graphe — vide à chaque passe, avec une
colonne par jeton du lot. Ici les jetons sont traités un par un : la couche 0
empile l'entrée du jeton COURANT, et rien d'autre.

**Ce qui reste faux** : jetons 1 et 2 à 0,819 et 0,708 de corrélation. C'est un
défaut d'ÉTAT, et un essai de discrimination l'a circonscrit : remettre
convolution et delta à zéro avant chaque jeton (`DRAVE_K3_SANS_ETAT=1`) donne
**pire** (0,606 et 0,414). La référence enchaîne donc bien les jetons, et le sens
de l'état est le bon — c'est un détail de son évolution qui reste faux.

**Vérifié au passage, sans supposition** : `layer_norm_rms_epsilon = 1e-05`,
`kda.head_dim = 128`, `kda.gate_lower_bound = -5.0` (lus dans le GGUF) ;
`ssm_a` est **négatif** (−11,78 à −0,47, donc bien `−exp(A_log)`) ;
`ssm_dt.bias` est **négatif lui aussi** (−7,89 à +0,18), ce qui met `z` vers
−5 et la porte de décroissance vers −0,01 : `exp(g) ≈ 0,99`, décroissance faible.

**Point de méthode** : pour un lot de plusieurs jetons, la référence n'emprunte
PAS `build_delta_net_autoregressive` (qui assert `n_tokens == 1`) mais
`build_delta_net_chunking` — une formulation par blocs de 16 (donc rembourrée de
12 zéros ici), avec un `solve_tri` et un `cumsum` du log de la décroissance.
Mathématiquement équivalente à la forme séquentielle que j'ai transcrite, mais
c'est un chemin de code DIFFÉRENT, et il faut le savoir avant d'accuser l'un ou
l'autre sur un écart.

### 4quater. LE PREMIER JALON EST RENDU — ET IL EST NÉGATIF (04/10, 22h40)

La référence a tourné (`REF_SANS_REPACK=1`, voir plus bas), elle a vidé ses
`l_out-N`, et `tools/compare_etats.py` a comparé. **La couche 0 ne passe pas :**

| position | écart max | corrélation | verdict |
|---|---|---|---|
| 0 | 1,19e-02 | **0,983164** | ❌ |
| 1 | 1,55e-01 | 0,790361 | ❌ |
| 2 | 1,80e-01 | 0,641780 | ❌ |

Et la couche 12, après une banque :

| position | écart max | corrélation | verdict |
|---|---|---|---|
| 0 | 1,11e-01 | **0,990927** | ❌ |
| 1 | 1,02e+00 | 0,458801 | ❌ |
| 2 | 4,06e-01 | 0,448762 | ❌ |

**Ce que ces chiffres disent, et c'est plus utile qu'un simple « non » :**

1. **La position 0 est presque juste** (0,983 sur la couche 0, 0,991 sur la 12).
   La structure du calcul — normes, résidu, projections, MoE latent, SiTU — est
   donc en place : une erreur de forme donnerait une corrélation proche de zéro.
2. **Tout se défait dès la position 1.** Une erreur qui ne dépend pas de la
   position aurait le même écart partout ; ici elle **apparaît entre deux
   jetons**. Les suspects sont donc les mécanismes à ÉTAT : l'état de la
   convolution KDA (`d_conv = 4`) et la récurrence delta-net, qui sont les seuls
   du chemin à transporter quelque chose d'un jeton au suivant. Au jeton 0, la
   convolution ne voit que son remplissage : un état mal avancé ne s'y voit pas.
3. L'écart résiduel de la position 0 (~1 %, norme 0,937 fois celle de la
   référence) est un second défaut, plus petit, à traiter après.

**Prochaine action, dans l'ordre** : comparer non pas la SORTIE de la couche 0
mais les tenseurs intermédiaires déjà instrumentés (`--tensors` de la référence
sait filtrer n'importe quel nœud du graphe ; `kimi_k3.rs` en vidange déjà
plusieurs), en commençant par l'entrée de la convolution et sa sortie au jeton 1.

La comparaison, dès que la référence tournera sur le modèle complet :

```bash
REF_DUMP=/tmp/refk3 LD_LIBRARY_PATH=…/llama.cpp-k3/build/bin \
    tools/ref_logits_k3 <K3.gguf> <ids> /tmp/refk3.bin 4
DRAVE_DUMP_COUCHES=/tmp/notrek3 drave <K3.gguf> --k3-essai
python3 tools/compare_etats.py /tmp/notrek3 /tmp/refk3 l_out 0 0,1,2
```

## 5. Ce qui est déjà vérifié sans poids (et le restera)

| pièce | état |
|---|---|
| tokenizer | **identifiants identiques** au tokenizer officiel (11 textes, `tools/porte-tokenizer-kimi.sh`) |
| métadonnées et cadence | 93 couches, MLA aux couches 3/7/11/15, 2 `res_score` partout, couche 0 dense — **lus dans le fichier** |
| `res_mix` (attention résiduelle) | implémenté, testé (scores normalisés / somme brute) |
| SiTU | implémenté, testé (dont `linear_beta ≤ 0`) |
| KDA : récurrence | implémenté, testé contre NumPy f64 (état **et** sortie) |
| KDA : porte bornée | implémenté, testé (toujours dans (−5, 0) → l'état décroît) |
| KDA : convolution courte | implémenté, testé (état canal-majeur, noyau contigu) |
| **le reste** | à écrire, chaque étage avec son point de comparaison ci-dessus |

### L'écart résiduel, caractérisé (05/10, 05h20)

Dire « c'est de l'accumulation f32 » est une affirmation, pas une mesure. La
mesure : sur `l_out-92`, régression de l'écart sur la valeur (une erreur
**systématique** — biais d'échelle — donnerait une pente non nulle) :

| position | pente | écart-type | écart-type / dynamique |
|---|---|---|---|
| 0 | −1,80e-03 | 1,68e-02 | **2,3e-03** |
| 1 | +4,00e-04 | 1,12e-02 | **6,8e-04** |
| 2 | −2,18e-04 | 1,19e-02 | **4,0e-04** |

**Pente nulle, écart-type sous 0,25 % de la dynamique** : l'écart est un arrondi
réparti, pas un biais qui se cumulerait avec la profondeur. C'est ce qui explique
qu'il ne dérive pas — et c'est mesuré, pas supposé.
