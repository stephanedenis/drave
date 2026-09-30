# Plan — le top-k de l'attention dans le noyau GPU (phase 1.1)

**En une ligne** : l'attention creuse (`--attn-topk`) ne peut pas se servir du KV
déporté en VRAM — le code l'interdit explicitement — donc à long contexte elle
retombe sur le CPU et coûte **~25 à 70 fois** le chemin GPU complet. Ce plan
chiffre l'écart et décrit les trois noyaux qui le comblent.

## Pourquoi (mesuré, pas supposé)

Le chemin GPU de l'attention est conditionné à `groupe = fen == 0 &&
self.attn_topk == 0 && rep > 1` (`model.rs:3150`) : **dès que le top-k est
demandé, le miroir VRAM est ignoré**. Les deux mesures qui existent déjà disent ce
que ça coûte :

| mesure (dépôt) | valeur |
|---|---|
| attention 1 M de clés, **CPU** (int4, host) | **968 ms** par couche |
| la même, **KV en VRAM** (`DRAVE_GPU_KV=1`, noyaux `attn_kv_*`) | **13,2 ms** (×73) |
| « masquer sans réécrire les boucles » en top-k CPU | 12,4 → 12,5 ms : **aucun gain** |

La troisième ligne est la clé : en top-k, le coût n'est pas le softmax mais la
**notation de toutes les clés** (O(N) lectures). Le gain ne peut donc venir que de
la VRAM, où les clés sont déjà. Aujourd'hui la phase 1.1 n'est pas « optimiser un
peu » : c'est rendre le mode creux **utilisable** au-delà de ~32 k de contexte.

## Ce qui existe

* `drave-core/gpu/drave_gpu.cu` (853 lignes, 13 noyaux) : `attn_kv_partiels` (scores
  et partiels par tranche, softmax en ligne), `attn_kv_recombine` (fusion des
  tranches + puits), puis `attn_scores` + les trois noyaux de la sélection ;
* `drave-core/src/gpu.rs` : `Machine::attn_kv(...)` (FFI, allocations, partiels) ;
* côté moteur : `kv_gpu` (le miroir paginé), `attn_gpu_part` (le tampon de
  partiels), le repli propre (`fait_en_gpu`) ;
* le banc `--gpu-banc` et son critère d'exactitude habituel : **1,99e-7** sur la
  tête Q8_0 (mesuré aujourd'hui) ;
* sm_75 (Quadro RTX 5000) : 1024 fils par bloc, 48 ko de partagé, pas de
  `__reduce_add_sync` (sm_80+) — les réductions se font en partagé.

## Les trois noyaux à écrire

1. **`attn_scores`** — un bloc par (tête KV × tranche) ; il écrit dans un tampon
   `tete × N` les scores **déquantifiés** (`int8`/`int4` × échelle de bloc, comme
   `attn_kv_partiels` sait déjà le faire). Sortie : `sc[nh][N]` en f32.
   *Budget mémoire* : 14 têtes × N × 4 octets — 56 Mo à 1 M ✗ trop. **Le tampon ne
   doit donc PAS contenir tous les scores** : chaque bloc garde sa tranche en
   partagé, sélectionne localement, et n'écrit que ses k candidats (voir 2).
2. **`attn_topk_select`** — la sélection, par tête. Méthode retenue : **radix select
   sur les scores transformés en entiers monotones** (le classique : pour un f32
   positif, les bits sont déjà ordonnés ; pour un négatif, on inverse) :
   * **quatre** passes de 8 bits — et non deux : avec deux passes, l'ensemble des
     scores partageant les 16 bits de tête peut dépasser k, et il faudrait alors
     choisir *dans* le paquet, ce qui n'est plus un top-k ; quatre passes donnent
     le score k-ième **au bit près** (`attn_topk_histo`) ;
   * la descente des seaux se fait sur l'hôte, avec **un préfixe par ligne** ;
   * la collecte des indices est **deux noyaux** (`attn_topk_compte` puis
     `attn_topk_ecrit`, séparés par une somme préfixée sur l'hôte) : un bloc ne
     peut pas connaître son rang global avant que les précédents aient compté ;
   * les indices sortent **par ordre croissant** — c'est ce qui rend la somme
     pondérée déterministe, et c'est le départage des ex æquo du CPU.
   ✅ **fait** : ensemble identique au CPU sur 14/14 lignes (différence symétrique
   0) à 4 096, 65 536 et 262 144 clés — `reports/rapport-gpu-topk-selection.md`
3. **`attn_topk_somme`** — softmax sur les k scores retenus (le max et le
   dénominateur se calculent sur ces k seulement, plus les **puits** qui comptent
   dans le dénominateur comme aujourd'hui), puis somme pondérée des V lus en VRAM
   par les k indices. Sortie : le vecteur d'attention, même disposition que
   `attn_kv`.

## Le contrat d'exactitude

Le top-k CPU et le top-k GPU doivent retenir **le même ensemble** aux ex æquo près.
Le banc doit donc vérifier deux choses séparément :

1. **l'ensemble retenu** : différence symétrique avec l'ensemble CPU, à comparer
   aux ex æquo (des scores égaux au bit près peuvent être départagés différemment) ;
2. **la sortie** : écart max relatif sur le vecteur d'attention, attendu ≤ 1e-6
   hors ex æquo.

Puis, à l'échelle du modèle : la perplexité de `--attn-topk 256` à contexte 2 048
doit rester **234,88** (la valeur CPU mesurée) à la tolérance près, et le banc 1 M
doit montrer l'effet cherché : **968 ms → quelques dizaines de ms par couche**.

## Le plan, en étapes

| # | étape | critère de succès |
|---|---|---|
| 1 | `attn_scores` + FFI + banc `--banc-topk` sur 4 k de contexte | ✅ **fait** : écart **1,6 à 2,3e-7** à toutes les longueurs (256 à 262 144 clés, clés distinctes — la valeur de 1,03e-7 venait d'un banc dégénéré), **27 à 40× plus rapide** que le CPU — `reports/rapport-gpu-scores.md` |
| 2 | `attn_topk_select` (radix, 3 noyaux) | ✅ **fait** : ensemble retenu identique au CPU, 14/14 lignes (différence symétrique 0) — `reports/rapport-gpu-topk-selection.md` |
| 3 | `attn_topk_somme` (softmax sur k + puits) | sortie identique au CPU à 1e-6 |
| 4 | branchement dans `model.rs` (autoriser le GPU quand `attn_topk > 0` **et** que le noyau rend `true`, garder le repli CPU sinon) | perplexité 2 048 = 234,88 ± tolérance |
| 5 | mesure 1 M : ms/layer avec et sans top-k, sur GPU | le top-k GPU ne doit pas coûter plus de ~2× le complet |
| 6 | porte de non-régression : les deux valeurs restent 19,3885 et 15,1757 | inchangées |

## Les pièges, déjà payés une fois chacun

* **la disposition du KV** : un partiel par (tranche, tête KV, tête de requête),
  `(hd + 2)` f32 — le +2 porte le max et la somme en ligne ; le top-k n'en a pas
  besoin de la même façon ;
* **les puits** comptent dans le dénominateur du softmax même quand la fenêtre est
  active — les oublier fausse la distribution, pas seulement la queue ;
* **la fenêtre** (`--attn-window`) et le top-k ne se combinent pas dans le même
  noyau : la fenêtre reste au CPU, c'est écrit aujourd'hui et ça peut le rester ;
* **les ex æquo** : un tri par index évite un non-déterminisme qui rendrait la
  perplexité non reproductible ;
* **l'ordre des sommes** : la somme pondérée GPU ne sommera pas dans le même ordre
  que le CPU (partiels par tranche) — c'est déjà le cas pour l'attention complète
  (écart 2e-7 documenté), et c'est acceptable **à condition de le dire**.

## Ce que ce plan ne fait pas

Il ne rend pas le top-k *exact* plus rapide que O(N) : noter toutes les clés reste
nécessaire. Le gain vient de la VRAM. Une vraie réduction de complexité demanderait
un **index** (clés regroupées, sélection approximative avant notation) — c'est un
autre chantier, et il n'est pas dans la feuille de route aujourd'hui.
