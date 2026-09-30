# Rapport — la sélection top-k sur GPU (noyaux 2a et 2b du plan)

**En une ligne** : la sélection du top-k de l'attention tourne maintenant sur GPU en
**quatre passes d'histogramme + deux noyaux de collecte**, elle rend le **même
ensemble d'indices que le CPU** (14/14 lignes, différence symétrique 0 à toutes les
tailles testées) et coûte **0,89 ms** là où le tri CPU en coûte **497 ms** à
262 144 clés.

Plan suivi : [`docs/plan-gpu-topk.md`](../docs/plan-gpu-topk.md), étape 2.
Noyau 1 (les scores) : [`reports/rapport-gpu-scores.md`](rapport-gpu-scores.md).

## Ce qui a été écrit

Trois noyaux dans `drave-core/gpu/drave_gpu.cu` (11 → 13 noyaux) :

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
calculés par le CPU et ceux calculés par le GPU sur 5 à 7 des 14 lignes. Ce n'est
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
  étaient affichés sans conversion et annonçaient un noyau 1 500× trop rapide
  (0,0004 ms pour 14,7 Mo lus). Un affichage mal étiqueté est un affichage qui
  ment — et il a bien failli faire chercher un faux défaut dans le noyau.

## Ce qui reste

| # | étape du plan | état |
|---|---|---|
| 1 | `attn_scores` | ✅ 1,6–2,3e-7 · 27–40× |
| 2 | sélection (radix 2 passes → 4 passes, 3 noyaux) | ✅ ensemble identique, 0 écart |
| 3 | `attn_topk_somme` : softmax sur les k retenus + puits, puis Σ pondérée des V | à écrire |
| 4 | branchement dans `model.rs` (`attn_topk > 0` + miroir VRAM) | à faire |
| 5 | mesure 1 M de clés : ms/couche avec et sans top-k | à faire |
| 6 | portes de non-régression : 19,3885 et 15,1757 | inchangées (voir le rapport de sprint) |

Le top-k GPU n'est donc **pas encore branché dans le moteur** : il est mesuré,
exact et plus rapide que le tri CPU, mais l'attention creuse continue de passer par
le CPU jusqu'à l'étape 3.

## Reproduire

```bash
cargo build --release --manifest-path drave-core/Cargo.toml
DRAVE_GPU=1 ./drave-core/target/release/drave models/Qwen2.5-0.5B-Q4_0.gguf --banc-topk 262144
```

Le banc imprime la comparaison ligne par ligne ; la dernière ligne dit si
l'ensemble retenu est le même. `--attn-topk N` choisit `k` (256 par défaut).
