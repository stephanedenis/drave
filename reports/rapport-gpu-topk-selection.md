# Rapport — la sélection top-k et la somme sur GPU (noyaux 2 et 3 du plan)

**En une ligne** : la sélection du top-k de l'attention tourne maintenant sur GPU en
**quatre passes d'histogramme + deux noyaux de collecte**, elle rend le **même
ensemble d'indices que le CPU** (14/14 lignes, différence symétrique 0 à toutes les
tailles testées) et coûte **0,89 ms** là où le tri CPU en coûte **497 ms** à
262 144 clés. Le **noyau 3** (softmax sur les k retenus + puits, puis Σ w·V) est
écrit et vérifié à **2,7–4,8e-7** — sous le critère de 1e-6 du plan.

Plan suivi : [`docs/plan-gpu-topk.md`](../docs/plan-gpu-topk.md), étape 2.
Noyau 1 (les scores) : [`reports/rapport-gpu-scores.md`](rapport-gpu-scores.md).

## Ce qui a été écrit

Trois noyaux dans `drave-core/gpu/drave_gpu.cu` (10 → 13 noyaux : les scores
avaient porté le fichier à 10, la sélection le porte à 13) :

| noyau | rôle |
|---|---|
| `attn_topk_histo` | histogramme d'un OCTET des scores, pour les seuls scores dont les octets au-dessus valent le préfixe de leur ligne |
| `attn_topk_compte` | par (ligne, tranche) : combien de scores au-dessus du seuil, combien égaux |
| `attn_topk_ecrit` | écrit les indices retenus, **dans l'ordre croissant des indices** |

Le plan prévoyait **un** noyau de sélection. Il en faut trois, et ce n'est pas un
choix de style : un bloc ne peut pas connaître son rang global avant que les blocs
qui le précèdent aient compté. D'où le découpage **compte → somme préfixée sur
l'hôte → écriture**, qui est le schéma classique d'une compaction parallèle.

## Pourquoi c'est EXACT et pas approximatif

Un f32 transformé en entier **monotone** — `b | 0x80000000` si positif, `~b` si
négatif — est une bijection qui **préserve l'ordre**. Le radix select sur ces
entiers n'est donc pas une heuristique : quatre passes de 8 bits déterminent le
score k-ième **au bit près**, et les comptes « strictement au-dessus » et « égaux »
sont exacts. Le noyau n'approxime rien.

La seule décision non arithmétique est le départage des ex æquo : le CPU trie par
(score décroissant, index croissant) ; le GPU prend les premiers égaux **par ordre
d'indices**, chaque fil possédant une plage **contiguë** de sa tranche. Une plage
entrelacée (`i += 256`) écrirait les indices dans le désordre et rendrait la
perplexité non reproductible — c'est écrit dans le noyau.

## Mesures

`--banc-topk N` avec `DRAVE_GPU=1`, Qwen2.5-0.5B Q4_0, k = 256, 2 têtes KV ×
64 dim, 7 têtes de requête par tête KV (**14 lignes**), cache KV 8 bits, **une clé
distincte par position**. La référence CPU est calculée sur **les scores rendus par
le GPU** : le critère porte ainsi sur les noyaux 2a/2b seuls, pas sur l'écart du
noyau 1.

| N clés | k-ième score identique | comptes identiques | ensembles identiques | diff. sym. | 4 passes GPU | tri CPU | collecte GPU | tri complet CPU |
|---|---|---|---|---|---|---|---|---|
| 4 096 | 14/14 | 14/14 | 14/14 | **0** | 0,14 ms (9×) | 1,31 ms | 0,13 ms (35×) | 4,33 ms |
| 65 536 | 14/14 | 14/14 | 14/14 | **0** | 0,32 ms (69×) | 22,17 ms | 0,34 ms (258×) | 86,53 ms |
| 262 144 | 14/14 | 14/14 | 14/14 | **0** | 0,44 ms (224×) | 97,88 ms | 0,45 ms (896×) | 399,21 ms |

L'ordre de sortie est vérifié séparément de l'ensemble : les `k` indices sont
**ceux au-dessus du seuil puis les égaux**, chaque groupe par indices croissants —
zéro doublon, zéro indice hors bornes, zéro case non écrite, sur les trois tailles.

**Bornes** (mêmes vérifications, toutes vertes) : n = 1 avec k = 1 ; n = 100 avec
k = 3 ; n = 4 097 et n = 5 000 (le pas de tranche est 4 096, donc la dernière
tranche est partielle) ; n = 8 191 avec k = 4 096 (la moitié de la ligne).

### Le banc mentait, et c'est en le relisant qu'on l'a vu

Première version du banc : **la même clé pour toutes les positions**. Tous les
scores d'une ligne étaient alors *exactement égaux* — donc l'histogramme n'avait
qu'un seul seau non vide, la descente radix ne choisissait jamais entre deux seaux,
et le banc validait un cas dégénéré en ayant l'air de valider la sélection. Le
défaut ne se voyait pas : les 14/14 lignes passaient. Corrigé (une clé par
position), les chiffres ci-dessus sont ceux d'un vrai test.

Effet secondaire de la correction : l'écart du **noyau 1** n'est plus 1,03e-7 mais
**1,60 à 2,25e-7** selon la taille — c'est la même mesure faite sur des données non
dégénérées, et elle reste 4× sous le critère de 1e-6 du plan. Le rapport du noyau 1
est corrigé dans le même commit.

**Ce que le banc refuse de cacher** : le k-ième score **change** entre les scores
calculés par le CPU et ceux calculés par le GPU sur 5 à 7 des 14 lignes aux trois
tailles principales — et jusqu'à 14/14 sur les petites (n = 8 191 avec k = 4 096,
où le k-ième est au milieu d'une distribution dense). Ce n'est
pas un défaut de la sélection : l'écart entre le 256e et le 257e score est du même
ordre que l'exactitude du noyau 1, donc le *rang* bascule sur des valeurs
quasiment égales. La comparaison qui compte — le k-ième score des scores GPU
retrouvé par la descente — est exacte au bit près (écart entier max 0) partout.

### Le second passage, avec un k plus grand

Le banc refait un seuil et une collecte avec **k doublé (512)**, dans le MÊME
processus, et vérifie l'ensemble contre le CPU : **14/14 lignes identiques**,
0,45 ms de collecte et 0,27 ms de seuil à 262 144 clés. Ce passage existe pour un
défaut précis, trouvé à la relecture et pas par un banc : les tampons de la
collecte n'étaient réalloués que si `(lignes, tranches)` grandissait, donc un `k`
plus grand gardait un tampon de sortie trop petit et le noyau écrivait **au-delà**
— un débordement en VRAM silencieux (`t.k < k` est entré dans la condition).

## Les pièges, payés une fois chacun

* **`atom.shared.add.u32` n'est pas `atom.global.add.u32`** : un atomique global
  sur une adresse partagée rend `CUDA_ERROR_INVALID_ADDRESS_SPACE (717)` — et
  l'erreur ne remonte **pas** au lancement, mais à la copie suivante. D'où deux
  fonctions distinctes dans `cuda_stub.h`, la version partagée passant par
  `cvta.to.shared.u64`.
* **`__float_as_uint` / `__uint_as_float` n'existent pas** sans en-têtes CUDA : le
  compilateur refusait le fichier, donc plus de PTX du tout. Remplacés par
  `reinterpret_cast`.
* **Un préfixe par ligne, pas un scalaire** : chaque tête de requête a son propre
  k-ième score ; un préfixe scalaire aurait obligé à relancer le noyau une fois
  par tête (56 lancements au lieu de 4).
* **Deux passes sur la tranche** dans la collecte : il faut les rangs avant
  d'écrire. Les clés relues viennent du cache L2, pas de la VRAM.
* **L'invariant vérifié avant d'écrire** : l'hôte refuse la collecte si le compte
  « au-dessus » ne tombe pas sur `k − besoin`. Un seuil faux écrirait à côté des
  `k` places ; ici il rend `false` avec le détail de la ligne fautive.
* **Une durée en secondes étiquetée « ms »** : les deux temps du second passage
  étaient affichés sans conversion et annonçaient un noyau ≈1 100× trop rapide
  pour la collecte et ≈900× pour le seuil (0,0004 ms au lieu de 0,45 ms, 0,0003 au
  lieu de 0,27 ms). Un affichage mal étiqueté est un affichage qui ment — et il a
  bien failli faire chercher un faux défaut dans le noyau.

## Noyau 3 : le softmax sur les k retenus, puis Σ w·V

`attn_topk_somme` : un bloc par ligne, les k scores rassemblés en mémoire partagée
(le max et le dénominateur se calculent donc une fois par ligne, pas une fois par
composante), un fil par composante pour la somme pondérée. Les indices sont lus
**en VRAM** — ceux que la collecte vient d'y écrire —, donc aucun aller-retour par
l'hôte. Les puits comptent dans le dénominateur, jamais au numérateur.

Référence CPU : mêmes indices (ceux du GPU), mêmes scores (ceux du GPU), valeurs
relues du cache hôte — le seul écart possible vient donc du noyau 3.

| N clés | k | GPU | CPU | écart relatif |
|---|---|---|---|---|
| 100 | 3 | 0,03 ms | 0,02 ms | **1,04e-7** |
| 4 096 | 256 | 0,07 ms | 0,64 ms | **4,79e-7** |
| 65 536 | 256 | 0,07 ms | 1,07 ms | **3,10e-7** |
| 262 144 | 256 | 0,07 ms | 0,98 ms | **2,70e-7** |

Le temps GPU est **constant** (0,07 ms de 4 k à 262 k clés) : le noyau ne lit que
les k scores retenus et k × hd valeurs, pas la ligne entière. C'est exactement le
gain cherché — le coût du top-k devient indépendant de la longueur du contexte.

**Limite** : k ≤ 1 024 (le partagé du noyau tient 2k + 256 flottants) et valeurs
8 ou 32 bits ; au-delà, le noyau rend `false` avec le détail plutôt que de deviner.
Les valeurs 4 bits ne sont pas gérées (refusées explicitement).

### Le bug que le banc a attrapé en une ligne

Première version : **le puits était ajouté par chaque fil** alors que chaque fil ne
tient qu'une somme PARTIELLE — la réduction l'additionnait donc 256 fois. Mesuré :
dénominateur ×45,7 et sortie 55× trop petite à k = 1 ; écart relatif 2,05e-1. Une
fois corrigé (`tid == 0`), 4,79e-7. La relecture ne l'aurait pas vu : le code a
l'air juste, et c'est le banc — qui compare à une référence CPU écrite
indépendamment — qui a parlé.

## Étape 4 : le branchement dans le moteur

Le miroir VRAM était **interdit dès que `attn_topk > 0`**
(`groupe = fen == 0 && self.attn_topk == 0 && rep > 1`, `model.rs:3150`) : le mode
creux retombait donc sur le CPU. La condition est complétée par une branche
`DRAVE_GPU_TOPK=1` (opt-in) qui enchaîne les quatre noyaux sur le miroir et ne
publie son résultat que si **tous** rendent `true` — sinon le chemin CPU reprend,
sans résultat partiel.

Vérification A/B, même binaire, même modèle (Qwen2.5-0.5B Q8_0), `--ctx 2048
--limit 1024 --attn-topk 256 --dense` :

| chemin | perplexité | durée |
|---|---|---|
| CPU (`--attn-topk 256`) | 9,4167 | 41,59 s |
| **GPU** (`DRAVE_GPU=1 DRAVE_GPU_KV=1 DRAVE_GPU_TOPK=1`) | **9,4162** | 41,45 s |

L'écart de perplexité (5e-4 en relatif) est du même ordre que l'exactitude des
noyaux (1e-7 sur les scores) propagée par un top-k dont le **rang** bascule entre
deux scores quasi égaux — le banc le montre déjà (5 à 7 lignes sur 14). Le
résultat est identique à la précision près, pas bit à bit, et c'est écrit ici
plutôt que passé sous silence.

**Le gain n'est pas encore là** : le poste « attention » (ms/jeton, 24 couches,
511 jetons, même modèle, `--attn-topk 256`) le dit —

| contexte | jetons | attention CPU | attention GPU top-k | perplexité CPU / GPU | balayage CPU / GPU |
|---|---|---|---|---|---|
| 2 048 | 511 | **4,21** | 7,68 | 13,1358 / 13,1355 | 18,1 / 20,4 s |
| 8 192 | 511 | **6,35** | 7,36 | 13,1358 / 13,1355 | 19,2 / 19,7 s |
| **16 384** | 4 095 | 20,69 | **7,72** | 12,2267 / **12,2265** | **207,8 / 160,7 s (−23 %)** |

Le GPU est **plat** (7,4–7,7 ms/jeton, indépendant du contexte : c'est le but), le
CPU croît — de 4,21 à 20,69 ms/jeton entre 2 k et 16 k. **Le croisement est donc
entre 8 192 et 16 384 clés**, et à 16 k le déport gagne franchement : attention
**20,69 → 7,72 ms/jeton (−63 %)**, balayage **207,8 → 160,7 s (−23 %)**, perplexité
identique à 2e-5 près. C'est plus loin que le croisement de l'attention complète
(~4 000 clés), et pour la raison déjà identifiée : le coût fixe des lancements et
des recopies. La
raison est la même que celle déjà payée sur le miroir KV (« les tampons alloués à
chaque appel : 24,5 ms/jeton au lieu de 2,9 », `docs/contexte-long.md` §4.ter) :
la chaîne fait **six lancements et cinq recopies par couche et par jeton**, soit
~74 000 lancements pour ces 511 jetons, à comparer aux ~0,1 ms de calcul utile par
couche. Ce n'est pas un noyau de plus qu'il faut, c'est **la fusion des quatre
passes** dans un seul noyau (descente radix sur le périphérique) et la
réutilisation des tampons hôtes.

## Un faux résultat silencieux trouvé AILLEURS, par la relecture du branchement

La seconde relecture adversariale (celle du branchement dans le moteur) a trouvé un
défaut dans un noyau **plus ancien**, `attn_kv_recombine` : il lisait `sinks[warp]`
— la tête de requête DANS le groupe KV — alors que sa sortie est écrite par tête
GLOBALE (`out[(kvh*rep + warp)*hd …]`). Sur gpt-oss (64 têtes de requête, 8 têtes
KV, puits allant de −1,95 à +3,38), la tête `kvh×rep + w` recevait donc le puits de
la tête `w`, avec jusqu'à **4,65 logit** d'écart — un facteur 105 sur le terme de
drainage du dénominateur. Le chemin CPU, le noyau 3 du top-k et la référence HF
indexent tous par tête globale : seul ce noyau était faux.

**Mesuré, avant et après** (gpt-oss-120b MXFP4, ctx 256, 510 jetons,
`--dense`, `DRAVE_GPU=1 DRAVE_GPU_KV=1`) :

| | perplexité |
|---|---|
| avant correction | **17,6531** |
| après correction | **15,1786** |
| référence CPU (sans miroir VRAM) | 15,1757 |

Qwen2.5 n'a pas de puits : la porte de 19,3885 ne pouvait pas voir ce défaut, et
aucun banc ne le couvrait (les bancs KV n'ont pas de puits non plus). C'est la
démonstration la plus nette de la journée qu'une relecture **par un autre** trouve
ce que les mesures ne cherchent pas.

## Limites connues du contrat

Le radix select s'appuie sur la transformation monotone du f32. Elle est
**strictement croissante pour deux valeurs distinctes**, mais :

* `monotone(-0,0) = 0x7FFFFFFF` et `monotone(+0,0) = 0x80000000` : deux scores que
  le f32 déclare **égaux** ont deux entiers différents, donc si le k-ième score est
  un zéro signé, le départage des ex æquo peut différer du CPU ;
* les **NaN** sont rangés par leur bit de signe (au-dessus de +inf ou en dessous de
  -inf) au lieu de n'être comparables à rien.

Aucune des deux n'a été observée : il faut une clé nulle et une échelle négative
pour produire -0,0, et les scores NaN n'apparaissent pas dans un modèle sain. Le
contrat est corrigé dans le noyau plutôt que tu ; la normalisation de -0,0 des deux
côtés est le correctif si le cas se présente un jour.

## Ce qui reste

| # | étape du plan | état |
|---|---|---|
| 1 | `attn_scores` | ✅ 1,6–2,3e-7 · 26,7–40× |
| 2 | sélection (radix 2 passes → 4 passes, 3 noyaux) | ✅ ensemble identique, 0 écart |
| 3 | `attn_topk_somme` : softmax sur les k retenus + puits, puis Σ pondérée des V | ✅ 1,0–4,8e-7 · temps GPU constant (0,07 ms) |
| 4 | branchement dans `model.rs` (`attn_topk > 0` + miroir VRAM) | ✅ **fait** (opt-in `DRAVE_GPU_TOPK=1`) : PPL identique (9,4162 contre 9,4167 à 2 k ; 12,2265 contre 12,2267 à 16 k) et **gain à 16 k** : attention 20,69 → 7,72 ms/jeton, balayage −23 % |
| 5 | mesure 1 M de clés : ms/couche avec et sans top-k | à faire |
| 6 | portes de non-régression : 19,3885 et 15,1757 | ✅ inchangées, mesurées le 30/09 au soir (voir le journal de la session) |

Le top-k GPU n'est donc **pas encore branché dans le moteur** : il est mesuré,
exact et plus rapide que le tri CPU, mais l'attention creuse continue de passer par
le CPU jusqu'à l'étape 3.

## Reproduire

```bash
cargo build --release --manifest-path drave-core/Cargo.toml
DRAVE_GPU=1 ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q4_0.gguf --banc-topk 262144
```

Le banc imprime la comparaison ligne par ligne ; l'avant-dernier bloc dit si
l'ensemble retenu est le même, et la dernière ligne refait le seuil et la collecte
avec **k doublé** dans le même processus (chemin de réutilisation des tampons). `--attn-topk N` choisit `k` (256 par défaut).
