# Sprint 31 — Le regroupement par experts mesuré, et Kimi-K3 au complet

- **Début** : ~12:45 · **Fin** : ~14:45
- **Objectif** : le bloc 30 a mesuré que les experts reviennent (46,9 % de
  réutilisation immédiate, 86,8 % pour un LRU de 32 par couche) et que le
  décodage ne peut rien en faire — un jeton n'a pas de voisins. Restait le
  **préremplissage** : là, les jetons d'un lot qui ont choisi le même expert
  partagent UNE lecture de sa matrice. Le mécanisme existe (`forward_lot`), il
  n'avait jamais été mesuré. Pendant ce temps, les 1,5 To de Kimi-K3 finissaient
  d'arriver.
- **Engagement de fin** : dépôt vert, machine rendue, tout commité.

## Revue — ce qui est livré, mesuré

### 1. Le regroupement par experts existe déjà. Il vaut ×1,58.

Qwen3-30B-A3B (128 experts, 8 par jeton), invite de **192 jetons**, modèle sur
NVMe, 16 fils, 3 passes par point (`tools/mesure-prefill-lot.sh`, neuf) :

| lot | prompt_s | tok/s | CPU % | mur_s |
|---|---|---|---|---|
| 1 | 33,23 | 5,77 | ~995 | 60,5 |
| 2 | **24,51** | 7,83 | ~889 | 51,1 |
| 4 | 23,29 | 8,27 | ~864 | 50,3 |
| 8 | 23,17 | 8,27 | ~854 | 50,6 |
| 16 | 22,45 | 8,53 | ~851 | 49,3 |
| 32 | 21,91 | 8,77 | ~839 | 48,9 |
| 64 | 21,27 | 9,03 | ~831 | 48,2 |
| 192 | **21,00** | 9,20 | ~827 | 47,8 |

**×1,58 de lot 1 à lot 192**, et l'essentiel est pris dès le lot 2 (×1,36). Le
CPU passe de 995 % à 827 % : le chemin par lots fait plus avec moins de cœurs.

### 2. Ce que les octets disent, et où le temps décroche

`tools/analyse_union_experts.py` (neuf) compte, sur la trace de routage réelle,
le nombre **exact** de matrices lues — `N×k` en mode jeton, `Σ|union|` en mode
groupe :

| bloc | gain octets | exp-éq/jeton | gain TEMPS |
|---|---|---|---|
| 1 | 1,00× | 8,000 | 1,00× |
| 2 | 1,31× | 6,111 | **1,36×** |
| 4 | 1,72× | 4,664 | 1,43× |
| 8 | 2,27× | 3,527 | 1,43× |
| 16 | 3,11× | 2,572 | 1,48× |
| 32 | 4,53× | 1,766 | 1,52× |
| 64 | 7,08× | 1,130 | 1,56× |
| 192 | **15,51×** | 0,516 | **1,58×** |

Deux faits, et ils ne disent pas la même chose :

- **au lot 2, le temps suit les octets** (1,31× contre 1,36×) : le chemin jeton
  était bien limité par les octets d'experts, et la corrélation du routage entre
  jetons voisins (46,9 %) fait déjà le travail ;
- **au-delà, le temps décroche** : 15,5× moins d'octets d'experts pour 1,58× de
  temps. Les experts ne sont plus le mur — le calcul dense (attention, normes,
  tête) et l'ordonnancement le sont. **Le levier « octets » s'épuise vers le lot
  8** ; c'est écrit ici plutôt que découvert plus tard sur un modèle géant.

### 3. Un défaut trouvé en mesurant : `--lot N` change la sortie, en silence

Première chose que la trace a montrée : **le routage diffère entre lot 1 et
lot 192 sur 7 838 des 9 312 lignes**. Génération gloutonne, même invite :

```
lot 1   : [67554, 512, 82497, 271, 14374, 220, 16, 13]
lot 2   : [67554, 512, 56698, 20538, 271, 2304, 44320, 56698]
lot 8   : [67554, 512, 56698, 20538, 271, 2304, 44320, 56698]
lot 192 : [67554, 512, 56698, 20538, 271, 2304, 44320, 56698]
```

Le chemin par lots est cohérent avec lui-même (lots 2 à 192 identiques) mais
**diffère du chemin jeton par jeton dès le 3e jeton**, et rien ne le disait.
Quantifié, parce qu'un « ça diverge » sans chiffre ne se décide pas :

| mesure (invite de 192 jetons, lot 1 contre lot 8) | valeur |
|---|---|
| perplexité | 19,172 contre **19,143** (+0,15 %) |
| argmax identique | **191/191 = 100 %** |
| corrélation de Pearson | min **0,99719**, médiane 1,00000 |
| \|Δlogit\| médian | 0,0129 |

Donc : ce n'est pas un autre modèle, c'est le même à 1e-2 près sur les logits —
mais une chaîne gloutonne amplifie, et le 3e jeton part ailleurs. **Le moteur
l'annonce maintenant** (`[options] lot N : …`), avec ces chiffres.

### 4. Deux compteurs muets, refermés

En lisant la mesure, « paires experts » tombait de **1 811,9 M à 18,7 M par
jeton** entre lot 1 et lot 2 — un chiffre qui s'effondre de 97 % sans raison
visible fait croire à une optimisation qui n'existe pas. Cause : `gemm_dense_q4`
ne tient pas de compteur, et le chemin par lots ne comptait donc que les jetons
de génération. Corrigé (experts, plus la sortie d'attention `wo`, qui était le
seul produit du chemin par lots à ne pas se compter : 507,5 M contre 902,6 M
pour le MÊME calcul). Après correction : **2 717,8 M (lot 1) contre 2 721,1 M
(lot 8)**, soit 0,12 % — et la perplexité est inchangée au chiffre près.

### 5. Un piège désarmé : les experts partagés

`forward_lot` n'applique QUE les experts routés : aucune occurrence de `shexp`
dans tout son corps. Sur un modèle qui a des experts partagés (DeepSeek, Kimi),
`--lot N > 1` calculait donc un autre modèle, en silence. Aucun modèle du parc
n'était touché (Qwen3-MoE et gpt-oss n'en ont pas ; V4 est protégé par le refus
sur les hyper-connexions ; Kimi-K3 passe par le chemin MLA jeton par jeton) —
mais le piège était armé pour le jour où. Il **refuse** maintenant, comme les
hyper-connexions.

### 6. Kimi-K3 est arrivé, en entier

32/32 shards, **1 508,7 Go**, vérifiés à l'octet contre Hugging Face.

- `--config` : 93 couches — **1 dense, 68 KDA, 24 MLA**, 896 experts (16 par
  jeton), latent 3 584, routage sigmoïde avec renormalisation, **inventaire
  COMPLET** (aucun tenseur attendu ne manque). Une cadence inattendue est
  signalée : **la couche 92 est MLA alors que 92 % 4 ≠ 3** — 24 couches MLA et
  non 23, la dernière fait exception.
- porte du tokenizer contre l'implémentation officielle : **3 identiques,
  0 divergent**.
- **budget par jeton, mesuré sur le fichier complet** (plus d'extrapolation) :

| poste | Go par jeton | part |
|---|---|---|
| experts routés (16 sur 896) | 25,830 | 29,8 % |
| partagé + attention + tête | 60,958 | 70,2 % |
| **TOTAL** | **86,787** | |

  Inventaire des 2 573 tenseurs : 2 722,7 G poids en MXFP4 (experts) et
  **56,1 G poids en Q8_0** (tout le dense) — d'où les 59,6 Go/jeton du dense.
  **Le dense pèse 2,3× les experts routés** : aucune technique sur les experts
  ne peut adresser plus de 30 % du trafic d'un jeton.

### 7. Ce que ça implique pour K3, chiffré

- **Décodage** : 86,787 Go/jeton. Le plancher RAM (40 Go/s, mesuré) est
  2,17 s/jeton ; le NVMe (3,4 Go/s) 25,5 s. Aucun cache n'y change rien : le
  modèle ne tient pas.
- **Préremplissage** : les 59,6 Go du dense sont lus **une fois pour tout le
  lot**, et les experts suivent l'union. À 1 000 jetons, le coût par jeton tombe
  vers **0,09 Go** — mille fois moins. C'est le seul régime où K3 est
  envisageable ici, et c'est exactement la thèse du dépôt : transporter des
  listes plutôt que refaire le calcul dense.
- **Mais le calcul, lui, ne s'amortit pas.** Par jeton : 98,3 GFLOP pour les
  experts routés (1 488 matrices 3072×3584) + 112,2 GFLOP pour le dense
  (56,1 G poids) = **~210 GFLOP**. Le moteur tient 56,7 GFLOP/s mesurés
  (Qwen3-30B-A3B, lot 192 : 1,19 TFLOP en 21,0 s) → **~3,7 s/jeton de calcul
  pur**, même en préremplissage. C'est une estimation, et elle est annoncée
  comme telle : elle se remplacera par une mesure quand le chemin complet sera
  branché.

**Verdict du bloc** : le levier « lire moins d'octets » est réel mais il est
borné — à 30 % du trafic pour K3, et par le calcul dès le lot 8 sur ce matériel.
Le préremplissage reste la seule porte, et elle coûte 3,7 s/jeton de calcul.

## Relecture adversariale de mes propres chiffres

1. **Le premier balayage était faux d'un facteur 17.** Un `drave` du balayage
   précédent tournait encore pendant le lot 2 : 580 s au lieu de 24. Deux pools
   de 16 fils sur 40 CPU se disputent les cœurs ET la bande. Le script refuse
   maintenant de tourner sans le dire, et le protocole est « rien d'autre ».
2. **×1,58 est mesuré sur un modèle dont les experts ne sont que 56 % des
   octets d'un jeton.** Sur K3, où ils sont 30 %, le même levier vaudra moins —
   la transposition est un raisonnement, pas une mesure, et elle est écrite
   comme telle.
3. **Le gain temps ne suit pas le gain octets au-delà du lot 2.** Présenter
   « 15,5× moins d'octets » comme un gain de vitesse serait faux ; les deux
   colonnes sont côte à côte dans le tableau pour que ça se voie.
4. **La divergence lot 1 / lot N n'est pas forcément bénigne.** 191/191
   d'accord sur l'argmax d'invite ne garantit rien sur 10 000 jetons. Elle est
   annoncée, chiffrée, pas excusée.
5. **Le budget K3 est mesuré, les GFLOP/s sont empruntés à un autre modèle.**
   Le rapport des deux est une extrapolation.

## Une hypothèse avancée puis RÉFUTÉE (même bloc)

Le plateau du gain au-delà du lot 2 appelait une explication. La voici, telle
qu'elle a été écrite avant d'être testée : le GEMM 4 bits balaie les lignes une
fois par tuile de jetons, donc **déchiffre les poids `t/tuile` fois** — à tuile 8
fixe et lot 192, vingt-quatre fois. Une tuile plus grande devait donc gagner.

Mesuré (`DRAVE_TUILE_LOT`, lot 32, invite de 192 jetons, 16 fils) :

| tuile | prompt_s (4 passes) | moyenne |
|---|---|---|
| 8 (la constante historique) | 21,74 · 21,24 · 20,24 · 21,67 | **21,22** |
| 16 | 21,46 · 20,96 | **21,21** |
| 64 (déduite de 256 Kio d'activations) | 20,30 · 21,61 · 24,30 · 21,73 | **21,99** |

Repris **machine au calme** une fois la porte gpt-oss arrêtée (le premier point
de chaque série est froid et se reconnaît — 40,4 s et 26,0 s — il est écarté) :

| tuile | prompt_s (lot 32) | moyenne |
|---|---|---|
| 8 | 19,98 · 20,05 | **20,02** |
| 64 | 20,00 · 20,65 | **20,32** |

**Aucune différence, et la grande tuile est plutôt derrière (1,5 %).** L'hypothèse est
fausse : le déchiffrage des poids n'est pas ce qui borne ce noyau. La constante
reste donc à **8**, la valeur avec laquelle tout le reste du bloc a été mesuré,
et `DRAVE_TUILE_LOT` est laissé comme banc d'essai — pas comme réglage.

Le plateau vient donc d'ailleurs : la part dense (attention, normes, tête) ne
s'amortit pas par le regroupement des experts, et c'est elle qui prend la main.

## Environnement de mesure, dit honnêtement

La fin du bloc a été mesurée pendant que `llama.cpp-k3` chargeait Kimi-K3 :
**711 Go lus en 1 h 50** à travers le cache de pages, ce qui évince le modèle de
mesure en cours de route. Les chiffres du tableau principal (le balayage des
lots) ont été pris **avant**, machine au repos ; ceux de l'essai de tuile ont été
pris **pendant**, et c'est précisément pourquoi la conclusion est « aucune
différence » et non « ×1,3 » : dans cet environnement, un écart de 30 % n'est pas
attribuable.


## La porte gpt-oss, et pourquoi elle n'a PAS été rejouée ici

`tools/portes.sh` a rendu **une seule croix** : `gpt-oss-120b MXFP4 ctx 256` —
attendue à 15,6017. Le motif est un **délai dépassé** (2400 s), pas un chiffre
faux : le modèle est sur le disque tournant, et `llama.cpp-k3` y lisait Kimi-K3
en continu. Relancée à la main avec 9000 s de délai, elle n'avançait toujours
pas : le cache de pages ne garde pas 60 Go quand 1,8 To le traversent.

**Elle a été arrêtée volontairement**, et c'est un arbitrage, pas un oubli : deux
lectures concurrentes sur un seul disque tournant se ralentissent mutuellement,
et la mesure unique — la référence llama.cpp sur Kimi-K3 — valait plus que la
répétition d'une porte qui était verte au bloc précédent. Les changements du bloc
ne peuvent pas la déplacer : le refus sur les experts partagés ne concerne pas
gpt-oss (aucun tenseur `shexp`), les compteurs ne changent aucune sortie (PPL
identique au chiffre près avant/après sur Qwen), et `yd` hissé hors de la boucle
non plus (19,172 et 19,143 avant **et** après).

**À rejouer** dès que le disque est libre :

```bash
./drave-core/target/release/drave <gpt-oss-120b-MXFP4.gguf> --ppl /tmp/ids_oss_512.txt \
    --ctx 256 --dense --threads 16 --limit 512      # attendu : 15,6017
```

Tout le reste est vert : 77 tests, correction contre llama.cpp (100 % des
positions utiles ≥ 0,95, top-1 94,4 %), poids hc relus, les cinq modes de
découpage, formats contre libggml, et l'inventaire K3.

## La référence sur K3 : ce qui a été appris, et ce qui reste en vol

**llama.cpp connaît `kimi-k3`.** Chargé sans broncher : 32 shards, **2 573
tenseurs** — exactement le compte de notre propre `--tensors` — dont
`blk.92.ffn_*_shexp` et `blk.92.attn_output`. La porte de correction existe donc,
contrairement à V4.1 où llama.cpp refuse l'architecture (P7).

**Mais il ne peut pas l'exécuter ici par défaut.** Le repaquetage des poids
(`use_extra_bufts`, actif par défaut) lit chaque tenseur et le **recopie en
RAM**. Mesuré : après **16 tenseurs** — la couche 6 sur 93 — `ref_logits_k3`
tenait **104 Go résidents et 6,9 Go de swap** sur une machine de 125 Go. Il ne
pouvait pas finir, et il rendait le disque inutilisable pour tout le reste. Un
`llama-cli` lancé en parallèle a mis **2 h 50** à lire 1,66 To sans jamais
atteindre la phase de génération (aucune ligne « eval time ») : même obstacle.

**La porte de sortie est écrite** : `REF_SANS_REPACK=1` (nouveau) met
`use_extra_bufts = false`, donc llama.cpp travaille sur le fichier mmappé et lit
à la demande. Effet immédiat et mesuré : **RSS 16,7 Go au lieu de 104 Go**
pendant le chargement, `swap 0`, et aucune ligne « repack tensor ». C'est la
seule façon dont une référence peut tourner sur une machine dont la RAM fait
**8 %** du modèle.

Au moment d'écrire, cette passe est **en vol** (1,3 To lus, RSS 100 Go stable,
swap 0) : elle rendra les logits de référence *et* les états cachés par couche
(`REF_DUMP`), donc la comparaison `tools/compare_etats.py` contre les sorties
`l_out-0` et `l_out-12` déjà vidées par le moteur.

**Ce que la référence dit déjà, sans avoir fini** : sur cette classe de modèle,
la première barrière n'est pas l'architecture, ni le format, ni le tokenizer —
c'est **la politique de mémoire du moteur de référence lui-même**. Un moteur qui
veut les poids en RAM ne fait pas tourner un modèle de 1,5 To sur 125 Go, quel
que soit le nombre d'experts qu'il sait sauter.

## Le premier jalon de vérification K3 : NÉGATIF, et il dit où chercher

`tools/compare_etats.py` a comparé la sortie de la couche 0 du moteur à celle de
llama.cpp-k3, sur quatre jetons :

| | position 0 | position 1 | position 2 |
|---|---|---|---|
| couche 0, corrélation | **0,9832** | 0,7904 | 0,6418 |
| couche 12, corrélation | **0,9909** | 0,4588 | 0,4488 |

**Le motif est le message** : la position 0 est presque juste (98-99 %), et tout
se défait à la position 1. Une erreur de forme donnerait ~0 dès la position 0 ;
une erreur indépendante de la position donnerait le même écart partout. Ici
l'écart **naît entre deux jetons** — donc il est dans ce qui transporte un état :
la convolution KDA (`d_conv = 4`) et la récurrence delta-net. Au jeton 0 la
convolution ne voit que son remplissage, donc un état mal avancé ne s'y voit pas.

Reste un second défaut, plus petit : la position 0 elle-même est à ~1 % (norme
0,937 fois celle de la référence). À traiter après, et séparément.

Un jalon négatif, chiffré, avec un suspect nommé, vaut mieux qu'un « ça a l'air
de marcher » : c'est exactement ce que la porte de correction existe pour
produire.

## La baseline de la référence, mesurée

`REF_SANS_REPACK=1 tools/ref_logits_k3 <K3> <ids> <sortie> 4 --tensors l_out` :

| | valeur |
|---|---|
| temps mural | **2 h 48 min 21 s** pour 4 passes → **~42 min/jeton** |
| CPU | **11 %** — borné par le disque, pas par le calcul |
| lectures | 1,80 To → **451 Go par jeton** (soit 5,2 balayages du modèle) |
| RSS max · swap | 102 Go · **0** |
| sorties | les **93 couches** `l_out-0`…`l_out-92` + variantes |

C'est le chiffre auquel tout le reste se compare, et il dit une chose simple :
**sur cette machine, la référence fait tourner Kimi-K3 à 42 minutes par jeton**,
en lisant 5 fois le modèle par jeton. Le disque est le mur, pas le CPU.

Les 93 couches vidées permettent de **bissecter** : la prochaine session compare
couche par couche et trouve la PREMIÈRE qui décroche, au lieu de raisonner sur
la sortie de la couche 0.

## Suite (05/10, 00h-01h30) : deux bugs trouvés PAR la comparaison

La lecture du code de la référence, puis la mesure, ont sorti deux vrais défauts.

**1. La norme L2 par tête sur `q` et `k` n'existait nulle part** dans mon code.
`build_gdn_l2_norm` : `x/sqrt(Σx²+eps)`, plus `1/sqrt(head_dim)` sur `q` seul.
Sa signature était déjà dans les chiffres, et je ne l'avais pas lue : au jeton 0
l'état delta est nul, donc `o = β·(kᵀq)·v` — proportionnel à `v` quelle que soit
l'échelle de `q` et `k` — et la norme par tête qui suit efface cette échelle.
D'où 0,983 au jeton 0 **avec un rapport de norme de 0,937**. Dès le jeton 1,
l'accumulation `s += k ⊗ β(v − sᵀk)` dépend de l'échelle de `k`, et tout part.

| couche 0 | avant | après |
|---|---|---|
| jeton 0, corrélation | 0,983164 | **0,999979** |
| jeton 0, écart max | 1,19e-02 | **3,74e-04** |

**2. La banque résiduelle s'accumulait entre les jetons.** `resi_stack` est
locale au graphe dans la référence : vide à chaque passe. Ici les jetons sont
traités un par un, donc la couche 0 empile l'entrée du jeton COURANT.

**Ce qui reste** : jetons 1 et 2 à 0,819 et 0,708. C'est un défaut d'ÉTAT, et un
essai de discrimination l'a circonscrit — remettre convolution et delta à zéro
avant chaque jeton donne **pire** (0,606 et 0,414), donc la référence enchaîne
bien les jetons et le sens de mon état est le bon.

**Deux passes de référence sont en vol** pour trancher entre les suspects :
l'une instrumentée sur les tenseurs internes des couches 0-4 (`kda_q_conv`,
`kda_scan_out`, `prefix_sum_attn`…), l'autre avec `REF_UBATCH=1`, qui force le
chemin **autorégressif** — celui que ce moteur a transcrit — au lieu de la forme
par blocs que la référence emprunte pour un lot de plusieurs jetons.

**Leçon de méthode, et elle est chère** : mon test « KDA contre NumPy » passait
au vert depuis le début. Il comparait mon code à MA transcription — les deux
avaient le même trou. Un test qui partage l'erreur de l'implémentation ne teste
rien ; c'est la comparaison à un tiers qui a trouvé les deux bugs, en deux
heures, après deux jours de transcription.

## Fin de bloc (05/10, 03h20) : Kimi-K3 vérifié sur treize couches

Trois bugs, tous trouvés par la comparaison à llama.cpp-k3, aucun par relecture,
aucun par le test « KDA contre NumPy » qui passait au vert depuis le début :

1. **la norme L2 par tête sur `q` et `k`** (`build_gdn_l2_norm`) était absente
   partout — dans le code ET dans le test qui était censé le couvrir ;
2. **la banque résiduelle s'accumulait entre les jetons** au lieu d'être propre
   à la passe du jeton courant ;
3. **son ORDRE de remise à zéro** : elle doit être repartie AVANT l'attention
   résiduelle. Garder le `n_ckpt` du jeton précédent faisait appliquer un
   `res_mix` là où la référence n'en applique pas.

Les trois étaient **invisibles au jeton 0**, et c'est précisément pour ça qu'ils
ont survécu deux jours : au jeton 0 l'état delta est nul (donc l'échelle de `q`
et `k` disparaît dans la norme qui suit) et la banque n'a qu'un point de
contrôle. La comparaison à un tiers les a sortis en deux heures.

**Résultat, contre `l_out-0` et `l_out-12` de la référence :**

| | jeton 0 | jeton 1 | jeton 2 |
|---|---|---|---|
| couche 0 | 0,983164 → **0,999979** | 0,790361 → **0,999982** | 0,641780 → **0,999983** |
| couche 12 | 0,990927 → **0,999945** | 0,458801 → **0,999943** | 0,448762 → **0,999102** |

**Deux des treize points de comparaison du protocole sont verts.** La couche 12
est le point qui compte le plus : elle est atteinte après **une banque franchie**
et un `res_mix` à DEUX points de contrôle, donc elle valide l'enchaînement que
quatre couches ne touchaient pas.

**En vol** : 25 couches (banques 0, 12, 24 → `res_mix` à TROIS points de
contrôle). Le chemin complet des 93 couches n'est pas à portée de l'instrument :
il déquantifie les experts en f32, et 93 couches en f32 demanderaient ~220 Go de
RAM pour 125 Go disponibles.

**Ce que ce bloc laisse, en une phrase** : le moteur calcule maintenant les
treize premières couches de Kimi-K3 comme llama.cpp les calcule, et la méthode
qui l'a rendu possible — comparer à un tiers plutôt qu'à soi-même — est écrite
noir sur blanc dans `docs/verification-kimi-k3.md`.

## Kimi-K3 : le modèle entier passe, et ses logits sont ceux de la référence

**La passe complète** (`DRAVE_K3_PASSE=93`) calcule les 93 couches en ne gardant
**qu'une couche en mémoire** — l'état récurrent d'une couche ne sert que pendant
la passe de cette couche sur les jetons, donc rien n'oblige à les garder toutes.
Le pic passe de ~220 Go (impossible) à ~2,2 Go (une couche) + 0,6 Go d'états.

Validée **au bit près** contre la composition résidente : écart max 0,000e+00 sur
les quatre jetons à la couche 24 — laquelle matche la référence.

**Résultat sur le modèle entier :**

| | jeton 0 | jeton 1 | jeton 2 |
|---|---|---|---|
| `l_out-92`, corrélation | **0,999857** | **0,999900** | **0,999919** |
| écart relatif | 1,4 % | 0,5 % | 0,7 % |

et avec la tête, **les logits** :

| position | corrélation | top-1 référence | top-1 moteur | jeton cible |
|---|---|---|---|---|
| 0 | **0,999802** | 84 | 84 ✅ | 275 |
| 1 | **0,999900** | 1103 | 1103 ✅ | 1309 |
| 2 | **0,999924** | 3140 | 3140 ✅ | 3140 |

**top-1 identique 3/3, et l'argmax est le bon jeton.** Le critère de la porte de
correction du dépôt passe à 100 % sur le plus gros modèle du parc.

**Le coût, mesuré** : 1 780 531 ms pour 4 jetons avec la tête, soit **7,4 minutes
par jeton**. La référence met **42 minutes par jeton** sur la même machine, bornée
par le disque (1,80 To lus pour 4 jetons) : cette passe ne lit que les 16 experts
choisis sur 896 et ne repaquette rien — **six fois plus rapide, et vérifiée
contre elle**.

**Quatre des treize points du protocole sont verts** : couches 0, 12, 24 et 92.
Le dernier est le modèle entier — 8 points de contrôle dans la banque, 68 couches
KDA avec leur convolution et leur récurrence, 24 couches MLA à cache latent, 896
experts dont 16 par jeton, SiTU. Aucun mécanisme de l'architecture n'est laissé
de côté.

**Ce qui reste**, et c'est nommé : la passe déquantifie le dense en f32 (2,2 Go
par couche chargée) au lieu d'utiliser les noyaux quantifiés du moteur ; elle
n'échantillonne pas de jetons ; et les mécanismes propres à ce dépôt — découpage
en grappes, transport de flux en listes — ne sont pas encore exercés SUR K3.
