# Contexte long : ce que 1 M veut dire, et par où ça casse

> Tous les chiffres de budget viennent de `qtrinet-core <modele> --plan --ctx N`,
> qui les calcule depuis les métadonnées du GGUF. Les bandes passantes sont
> celles mesurées sur cette machine (deux Quadro RTX 5000 16 Go, 125 Go de RAM,
> NVMe à ~3,5 Go/s, 20 cœurs Haswell AVX2).

## 1. Ce que les modèles déclarent

| modèle | contexte entraîné | initial | facteur YaRN | 1 M, c'est… |
|---|---|---|---|---|
| gpt-oss-120b | 131 072 | 4 096 | ×32 | ×8 au-delà du déclaré → extrapolation |
| Qwen3-30B-A3B | 262 144 | — | — | ×4 au-delà du déclaré |
| Qwen2.5-VL-7B | 32 768 | — | — | ×32 au-delà |

Autrement dit : **le moteur peut être prêt pour 1 M, aucun modèle d'ici ne l'est.**
Le travail d'ingénierie (mémoire, débit, rotation) est faisable et mesurable ; la
qualité à 1 M, elle, se mesurerait par récupération (« aiguille dans la botte de
foin »), pas par perplexité, et n'a de sens qu'avec un modèle entraîné pour.

## 2. Le budget, mesuré

`--plan --ctx N` chiffre le KV pour trois précisions et tient compte du fait que
**la moitié des couches de gpt-oss s'arrêtent à 128 entrées** (fenêtre
glissante) : leur KV ne grandit pas avec le contexte.

gpt-oss-120b (8 têtes KV × 64 dim × 2) :

| contexte | KV f32 | KV int8 | KV int4 | relecture/jeton int4 | décodage KV seul (RAM 20 Go/s, int4) |
|---|---|---|---|---|---|
| 32 768 | 2,43 Go | 0,61 Go | **0,30 Go** | 0,30 Go | 15 ms |
| 131 072 | 9,67 Go | 2,42 Go | **1,21 Go** | 1,21 Go | 61 ms |
| 1 048 576 | 77,32 Go | 19,33 Go | **9,66 Go** | 9,66 Go | 483 ms |

Sans la fenêtre par couche, les mêmes chiffres doublent (154,6 Go en f32 à 1 M).
Conclusion immédiate : **le KV f32 interdit 1 M** (154 Go pour 125 Go de RAM) ;
en int4 il tient dans **un seul GPU de 16 Go** (9,7 Go).

## 3. Les trois murs, dans l'ordre où ils frappent

### a. Le préremplissage — le mur n° 1, et de très loin

Notre moteur traite **un jeton à la fois** : remplir une fenêtre coûte ce que
coûterait de générer la même longueur.

| contexte | préremplissage estimé, séquentiel |
|---|---|
| 32 768 | 4,5 h |
| 131 072 | 31 h |
| 1 048 576 | **1 234 h** |

C'est le vrai obstacle, et il ne se contourne pas par la quantification : il faut
**traiter des tranches par lots** (produits matrice-matrice au lieu de
matrice-vecteur). Un préremplissage par tranches de 2 048 jetons relit les poids
une fois par tranche au lieu d'une fois par jeton : à 1 M, 512 passes de 62 Go à
20 Go/s ≈ 26 min, et l'attention devient le poste dominant (O(N²) sur la
séquence, ≈ 2·10¹⁵ MACs — quelques heures sur CPU, ~30 min sur les deux GPU avec
un vrai noyau d'attention). **C'est le chantier à ouvrir en premier** ; il
améliore aussi le temps de premier jeton sur tous les contextes.

### b. La bande passante du KV — le mur du décodage

À chaque jeton, l'attention relit **tout** le KV des couches pleines (les couches
à fenêtre ne relisent que 128 entrées). À 1 M, en f32 : 77 Go par jeton, soit
3,9 s par jeton depuis la RAM. En int4 : 9,7 Go, 483 ms depuis la RAM, **13 ms
depuis les deux GPU** (760 Go/s).

Le remède est donc double, et il est déjà à moitié en place :
1. **KV quantifié** (int8 puis int4) — le même travail que `DenseQ8`/`DenseQ4`,
   appliqué au cache ;
2. **résidence GPU** du KV : à 1 M en int4, le KV tient dans un RTX 5000 ;
   il faut alors que les couches pleines tournent sur le GPU, sinon le trafic
   PCIe (1,5 s/jeton à 1 M) annule le gain.

### c. La portée de la rotation — le mur discret, et la température qui n'aide pas

YaRN ×32 couvre **exactement** 131 072 jetons (4 096 × 32), c'est-à-dire le
`max_position_embeddings` déclaré. À 1 M il faudrait ×256, soit huit fois plus
que ce que le modèle a vu : les fréquences basses feraient alors plus d'un tour
complet sur la séquence et l'attention longue distance deviendrait du bruit.

Deux résultats mesurés (§5) changent la façon de poser le problème :

- **l'interpolation des basses fréquences est la partie utile** de YaRN pour
  étendre la portée : elle garde les phases lointaines dans ce que le modèle a
  vu, et c'est elle qu'il faut garder ;
- **la mise à l'échelle de température est nuisible sur du texte brut** (÷8,9 de
  perplexité à 512 jetons quand on la retire). Le moteur l'éteint donc par
  défaut dans le mode retardé ; `QT_YARN=1` la rétablit pour reproduire les
  implémentations de référence.

Au-delà du facteur déclaré, la seule réponse honnête reste « extrapolation,
qualité non garantie » — et désormais, ce n'est plus la rotation qui limite le
plus tôt : c'est le préremplissage (§3.a).


## 4. Plan par étapes

| # | étape | état | débloque | coût |
|---|---|---|---|---|
| E1 | **Préremplissage par lots** | **fait** : `gemm_dense_i8` et `gemm_dense_q4` (produits matrice-matrice par tranches), `forward_lot` juste sur dense **et** sur MoE avec regroupement des jetons par expert ; débit bout en bout à chiffrer | 32 k utilisable ; TTFT | le noyau est là ; reste à mesurer et à élargir les tranches |
| E2 | **KV int8** | **fait** (échelle par vecteur, dequantification à la lecture) | ÷4 sur le KV ; 128 k confortable | mesuré : +7,1 % de perplexité (llama.cpp q8_0 : +3,1 %) |
| E3 | **KV int4** | **fait** (nibbles empaquetés) | 1 M tient en RAM (9,7 Go) et en VRAM | mesuré : **+384 %** — llama.cpp q4_0 : +411 % ; à réserver aux cas où la mémoire manque |
| E4 | **KV déporté sur les 2 GPU** (pagination, préchargement) | à faire — les noyaux existent (`tete_q8_warp` fait passer la tête de 15,6 à 6,2 ms/jeton, PPL identique) | décodage 13 ms/jeton à 1 M | moyen |
| E5 | **Attention creuse** | à faire — `--attn-topk` et `--attn-window` existent et se mesurent au protocole `--depuis` | casse le O(N) du décodage | moyen |
| E6 | **MLA** (DeepSeek) | **non testable ici** : aucun modèle MLA en GGUF sur cette machine (le « deepseek-r1-distill » local est un Qwen dense) | compression structurelle du KV | gros |
| E7 | **Vision** | **non testable ici sans le chemin image** : le projecteur `mmproj` est présent, mais rien ne lit les patchs | images | gros |

Ordre recommandé : **E1 d'abord** (sans lui, aucun contexte long n'est
utilisable), puis E2+E3 ensemble (la qualité se mesure sur un petit modèle en
quelques minutes), puis E4/E5 selon l'usage (décodage long ou préremplissage
long).

## 4.bis KV quantifié : mesuré, et le 4 bits est cher

Cache KV en 8 puis 4 bits, échelle par vecteur (tête, position), nibbles
empaquetés en 4 bits — `QT_KV_BITS=8` ou `4`, `[config] cache KV` dit ce qui est
alloué. Banc d'essai : Qwen2.5-0.5B Q8_0, 511 jetons, contexte 512, comparé à
llama.cpp sur le même texte.

| KV | nous (512 jetons) | llama.cpp (512) | nous (~4 600 jetons) | llama.cpp (8 192) |
|---|---|---|---|---|
| f32 / f16 | 13,14 | 14,24 | 12,91 | 16,59 |
| **int8** | **14,07** (+7,1 %) | 14,68 (+3,1 %) | **13,58** (+5,2 %) | 16,73 (+0,8 %) |
| **int4** | **63,61** (+384 %) | 72,80 (+411 %) | **71,05** (+450 %) | 98,53 (+494 %) |

Trois choses :

1. **L'int8 coûte quelques pour cent, à contexte court comme à 4 600 jetons** :
   le coût ne grandit pas avec la longueur, donc le KV int8 est un bon défaut
   pour le contexte long (et c'est lui qui fait tenir 128 k en mémoire).
2. **Le 4 bits détruit la perplexité d'un facteur 5**, chez les deux moteurs. Il
   reste implémenté — c'est lui qui fait tenir 1 M en RAM (9,7 Go) et en VRAM —
   mais il ne doit pas être le défaut, et il se valide modèle par modèle.
3. **Notre int8 est un peu plus cher que celui de llama.cpp** (+5,2 % contre
   +0,8 %). Nos échelles sont **par vecteur** (une par tête et par position),
   les leurs **par bloc de 32** dans le format Q8_0. C'est la piste
   d'amélioration la plus directe du cache : passer aux échelles par bloc de 32,
   comme on l'a fait pour `DenseQ8`.

## 5. YaRN à retardement : ce que la mesure a dit

Politique implémentée (`[config] rotation` le dit à chaque chargement) : **RoPE
simple tant que le contexte demandé tient dans la longueur initiale déclarée
(4 096 pour gpt-oss), interpolation YaRN au-delà — sans la mise à l'échelle de
température** ; `QT_YARN=1` force le YaRN complet des implémentations de
référence, `QT_YARN_NON=1` jamais, `QT_YARN_MSCALE=0/1` tranche sur la
température seule. Décision **par séquence**, pas par position : la structure de
position relative ne survit que si toutes les clés partagent le même jeu de
fréquences.

> **Protocole.** Les courbes ci-dessous ont été mesurées « par longueur »
> (`--ctx N --limit N`), ce qui **confond la longueur et le contenu** : à
> 8 192 jetons on ne note pas les mêmes tranches qu'à 512, et le même corpus va
> de 6 à 542 de perplexité selon la tranche. Le protocole `--depuis N` corrige
> cela en notant **toujours les mêmes jetons**. La comparaison appariée qui suit
> (§5.bis) est celle qui tranche ; les chiffres ci-dessous restent des points de
> repère.

Les courbes, mesurées sur gpt-oss-120b et le même corpus (une seule fenêtre,
`--dense`, 16 fils) :

| longueur | RoPE simple | YaRN **sans mscale** | YaRN complet |
|---|---|---|---|
| 63 | **20,84** | — | 41,11 |
| 512 | **18,58** | 19,65 | 174,34 |
| 1 024 | **46,94** | 71,35 | 417,65 |
| 2 048 | **121,75** | 192,63 | 722,56 |
| 4 096 | **170,78** | 400,13 | — |
| 4 608 | — | 476,09 | 1 105,20 |

### 5.bis Comparaison appariée (mêmes jetons, contexte variable)

Jetons **1536 à 2047** du corpus (512 notés), contexte croissant, deux régimes —
c'est la mesure qui répond à la question « à partir de quand faut-il étirer ? » :

| contexte réel | RoPE simple | interpolation seule |
|---|---|---|
| 128 | **39,52** | 42,13 |
| 512 | **49,79** | 82,02 |
| 1 024 | **49,93** | 82,15 |
| 1 536 | **298,56** | 578,86 |

**Le RoPE simple gagne à toutes les longueurs mesurées**, y compris là où les
deux régimes décrochent (×6 entre 1 024 et 1 536 jetons de contexte). La
comparaison étant appariée, les effets de contenu s'annulent : c'est bien la
rotation qui est jugée, pas le texte.

Deux réserves, mesurées elles aussi :

- le **saut à ~1 500 jetons de contexte** est commun aux deux régimes : il vient
  du contenu AJOUTÉ (non contrôlé par le protocole), pas forcément de la
  longueur ;
- au-delà de 4 096 jetons de contexte, le RoPE simple extrapole : la mesure
  manque (il faut un corpus plus long que la cible + le contexte).

Trois enseignements :

1. **La mise à l'échelle de température (`mscale = 1 + 0,1·ln f`) est la moitié
   nuisible de YaRN** : la retirer divise la perplexité par 8,9 à 512 jetons,
   5,9 à 1 024, 3,8 à 2 048. C'est elle, et non l'interpolation des fréquences,
   qui rend le YaRN déclaré catastrophique sur du texte brut — les trois
   implémentations de référence (HF, llama.cpp, OpenAI) l'appliquent pourtant
   telle quelle, et notre moteur les reproduit au chiffre près quand on la
   garde.
2. **Le RoPE simple gagne à toutes les longueurs mesurées**, y compris à 4 096 —
   la longueur « initiale » du modèle. Le seuil de bascule n'est donc pas un
   croisement mesuré : c'est une décision d'ingénierie prudente (au-delà de la
   fenêtre d'entraînement initiale, le RoPE simple extrapole).
3. **Tous les régimes se dégradent fortement avec la longueur** (×9 pour le RoPE
   simple entre 512 et 4 096). Ce n'est pas le moteur : la référence llama.cpp,
   mêmes 2 048 identifiants, un seul lot, YaRN déclaré, donne **714,83** contre
   **722,56** chez nous (1,1 %). Le profil par profondeur (`--ppl-profil`) montre
   que deux causes se superposent — le contenu du corpus (même tranche : 13,94 en
   tête, 59,36 prise plus loin mais présentée à la position 0) et la position
   (~facteur 7 de plus à sa place réelle).

**Ce que la mesure ne dit pas** : la qualité des réponses générées. Sur une
question à étapes (« 3 pommes par jour pendant 17 semaines »), les trois
configurations partent en boucle de répétition en décodage glouton — le test ne
discrimine donc rien sur la rotation, et il reste à le refaire avec
`--rep-penalty`.



## 6. Ce qui se mesure tout de suite

1. **Aiguille dans la botte de foin** (`tools/aiguille.py`) : la perplexité ne dit
   pas si le modèle RETROUVE une information. Le script plante un code à une
   profondeur donnée et vérifie qu'il ressort ; c'est la mesure de qualité qui
   manque au plan.
2. **Attention creuse** : `--attn-topk N` et `--attn-window N` au protocole
   `--depuis` (mêmes jetons, contexte long) donnent le prix en perplexité de
   chaque restriction.
3. **Débit du préremplissage** : `--lot N` sur un modèle dense et sur gpt-oss,
   machine au calme ; c'est le chiffre qui dit si E1 tient ses promesses.

## 7. Rappel de méthode

Le contexte long est le seul chantier où **le mur change de nature** : à contexte
court, tout est bande passante de poids ; à contexte long, c'est le KV puis le
préremplissage. Un chiffre de perplexité obtenu à 512 jetons ne dit rien de ce
qui se passera à 128 k — c'est pourquoi `--plan` chiffre désormais les deux, et
pourquoi toute étape ci-dessus doit être mesurée à la longueur où elle sert.
