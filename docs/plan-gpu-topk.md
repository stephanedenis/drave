# Plan — le top-k de l'attention dans le noyau GPU (phase 1.1)

> **Document daté.** Plan, note ou étude d'un chantier : il porte sa date et son état en tête. La
> **feuille de route courante** est [`roadmap.md`](roadmap.md) ; l'**état** est
> [`en-cours.md`](en-cours.md).

**En une ligne** : l'attention creuse (`--attn-topk`) ne peut pas se servir du KV
déporté en VRAM — le code l'interdit explicitement — donc à long contexte elle
retombe sur le CPU et coûte **~70 fois** le chemin GPU complet. Ce plan
chiffre l'écart et décrit les trois noyaux qui le comblent. C'est un chantier de
**placement d'opérateur** (axe 2 de `docs/vision.md` : « on place un opérateur là
où son flux coûte le moins cher »), local à une machine ; ni la répartition entre
grappes ni la lecture des flux ne sont traitées ici.

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

* `drave-core/gpu/drave_gpu.cu` (956 lignes, 14 noyaux) : `attn_kv_partiels` (scores
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
   * les indices sortent **dans un ordre fixe** (au-dessus du seuil, puis les
     égaux, chacun par indices croissants) — c'est ce qui rend la somme pondérée
     déterministe, et le départage des ex æquo est celui du CPU (premiers égaux
     par ordre d'indice).
   ✅ **fait** : ensemble identique au CPU sur 14/14 lignes (différence symétrique
   0) à 4 096, 65 536 et 262 144 clés — `reports/rapport-gpu-topk-selection.md`
3. **`attn_topk_somme`** — softmax sur les k scores retenus (le max et le
   dénominateur se calculent sur ces k seulement, plus les **puits** qui comptent
   dans le dénominateur comme aujourd'hui), puis somme pondérée des V lus en VRAM
   par les k indices. Sortie : le vecteur d'attention, même disposition que
   `attn_kv`.
   ✅ **fait** : écart **1,0 à 4,8e-7** (critère 1e-6), temps GPU **constant**
   (0,07 ms de 4 k à 262 k clés) — `reports/rapport-gpu-topk-selection.md`.
   Limites : k ≤ 1 024, valeurs 8 ou 32 bits (refus explicite sinon).

## Le contrat d'exactitude

Le top-k CPU et le top-k GPU doivent retenir **le même ensemble** aux ex æquo près.
Le banc doit donc vérifier deux choses séparément :

1. **l'ensemble retenu** : différence symétrique avec l'ensemble CPU, à comparer
   aux ex æquo (des scores égaux au bit près peuvent être départagés différemment) ;
2. **la sortie** : écart max relatif sur le vecteur d'attention, attendu ≤ 1e-6
   hors ex æquo.

Puis, à l'échelle du modèle : la perplexité de `--attn-topk 256` à contexte 2 048
doit rester **celle du CPU** à la tolérance près — le critère chiffré d'origine
(234,88, gpt-oss, contexte 2 048, mêmes 512 jetons notés : `docs/contexte-long.md`
§6) dépend des réglages et n'a pas été reproduit par ce binaire — et le banc 1 M
doit montrer l'effet cherché : **968 ms → quelques dizaines de ms par couche**.

## Le plan, en étapes

| # | étape | critère de succès |
|---|---|---|
| 1 | `attn_scores` + FFI + banc `--banc-topk` sur 4 k de contexte | ✅ **fait** : écart **1,6 à 2,3e-7** de 4 096 à 262 144 clés (clés distinctes — la valeur de 1,03e-7 venait d'un banc dégénéré), **26,7 à 40× plus rapide** que le CPU ; c'est la re-mesure du 30/09 au soir qui fait foi dans `reports/rapport-gpu-scores.md` |
| 2 | `attn_topk_select` (radix, 3 noyaux) | ✅ **fait** : ensemble retenu identique au CPU, 14/14 lignes (différence symétrique 0) — `reports/rapport-gpu-topk-selection.md` |
| 3 | `attn_topk_somme` (softmax sur k + puits) | ✅ **fait** : 1,0–4,8e-7 à toutes les tailles (critère 1e-6) — `reports/rapport-gpu-topk-selection.md` |
| 4 | branchement dans `model.rs` (autoriser le GPU quand `attn_topk > 0` **et** que le noyau rend `true`, garder le repli CPU sinon) | ✅ **fait**, en opt-in (`DRAVE_GPU_TOPK=1`) : PPL à ctx 2 048 = **9,4162** contre **9,4167** au CPU (le critère chiffré d'origine (234,88, `docs/contexte-long.md` §6) n'est pas reproduit par ce binaire — c'est la comparaison A/B qui fait foi) · ⚠️ le gain de TEMPS n'est pas là à 2 048 clés : six lancements et cinq recopies par couche et par jeton — la fusion des quatre passes est la prochaine étape |
| 5 | mesure 1 M : ms/layer avec et sans top-k, sur GPU | ✅ **fait au niveau des noyaux** : la chaîne complète (scores sans relecture + 4 passes + collecte + somme) coûte **3,90 ms** pour 14 lignes × 1 M de clés, contre **539,9 ms** pour l'attention complète sur CPU (×138) et 13,2 ms pour l'attention complète en VRAM — soit **0,3×** le complet, mieux que le critère des 2× |
| 6 | porte de non-régression : les deux valeurs restent 19,3885 et 15,6017 | ✅ **vertes**, mesurées sur le binaire final : Qwen 19,3885 (CPU **et** avec `DRAVE_GPU_KV`) · gpt-oss 15,6017 (CPU) — 15,1757 était la valeur d'avant la correction du biais de routage du 02/10, voir `reports/rapport-routage-experts.md` |

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

## La prochaine étape n'est pas un noyau de plus, c'est une fusion

> **État au 24/10 — FAITE et MESURÉE.** Le noyau `attn_topk_tout` existe, est branché en opt-in, et le banc le
> compare à la chaîne : il **gagne jusqu'à ~64 k clés** (×1,1 à ×1,9) et **perd au-delà** (×1,43 à 1 M) — le
> croisement est entre 65 k et 131 k, d'où le seuil **`SEUIL_NOYAU4 = 131_072`** dans `model.rs`. La fusion ne
> remplace pas la chaîne séparée : elle la **complète** en dessous de ~100 k. Résultats :
> [`reports/rapport-gpu-topk-tout.md`](../reports/rapport-gpu-topk-tout.md).

Mesuré à 16 384 clés : la chaîne déportée gagne (attention 19,58 → 7,59 ms/jeton,
balayage −24 %), mais elle coûte **8 lancements et 17 transferts par couche et par
jeton**, dont 8 copies DtoH bloquantes — d'où un croisement entre 8 k et 16 k au
lieu des ~4 000 clés de l'attention complète. Le levier est donc :

1. **fusionner** la descente radix, la collecte et la somme dans **un seul noyau**
   par ligne (les k scores tiennent en partagé) : 8 lancements → 2 ;
2. **supprimer deux allers-retours inutiles** : la recopie de la sélection (le
   moteur ne lit que la copie VRAM — mais elle sert de contrôle de couverture, à
   déplacer dans le noyau) et le `cuCtxSynchronize()` de `attn_scores_sans_relecture` ;
3. **budgéter le tampon de scores** `nh × n × 4` par couche (56 Mo à 1 M pour
   14 têtes, 9,2 Go pour gpt-oss) : c'est exactement ce que ce plan déclarait
   « trop », et la fusion le supprime aussi.

## Ce que ce plan ne fait pas

Il ne rend pas le top-k *exact* plus rapide que O(N) : noter toutes les clés reste
nécessaire. Le gain vient de la VRAM. Une vraie réduction de complexité demanderait
un **index** (clés regroupées, sélection approximative avant notation) — c'est un
autre chantier, et il n'est pas dans la feuille de route aujourd'hui.
