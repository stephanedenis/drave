# V4.1 : la chaîne mHC **retardée**, et les trois égalités vérifiées sur le vrai modèle

**En une ligne** : les deux manques que le moteur annonçait pour DeepSeek-V4.1
(« réduction finale non spécifiée », « compression de ratio 2 sans référence »)
étaient **faux tous les deux** — la référence d'exécution existe (vLLM), elle dit
que V4.1 n'a **pas de tête apprise** et que ses coefficients se **retardent d'un
raccord** — et cette chaîne est maintenant implémentée, exécutée sur le fichier
de 365,7 Go, et vérifiée par trois égalités recalculées hors du moteur.

## 1. Ce que le moteur disait, et pourquoi c'était faux

Message de refus, tel qu'il sortait du binaire (mesuré le 02/10 à 17:33) :

```
architecture « deepseek41 » non implémentée par ce moteur :
  compression de ratio 2 (V4.1) : sans référence d'exécution — le support amont
  de V4.1 n'existe pas encore (llama.cpp n'accepte que 0, 4 et 128) ·
  réduction des copies avant la norme finale : V4.1 ne déclare pas `output_hc_*`
  (c'est son jeu de tenseurs) et aucun moteur ne spécifie ce cas.
```

Les deux affirmations sont réfutées par les sources, pas par un raisonnement :

| ce qui était dit | ce que dit la source |
|---|---|
| « sans référence d'exécution » | vLLM porte `vllm/models/deepseek_v41/compressor.py` (`DeepseekCompressor`, ratios **1 et 2**) et le noyau `fused_save_compress_norm` : softmax **par canal** sur le groupe (`tl.softmax(score, 0)`), norme RMS du latent, RoPE à la position du premier jeton du groupe ; ratio 1 = aucune porte, aucun groupe, aucun `ape` |
| « aucun moteur ne spécifie ce cas » | `vllm/models/deepseek_v41/nvidia/model.py:1009-1014` : `hc_collapse_triton(hidden_states, pre_mix)` puis `self.norm`, avec le commentaire « Collapse the hc copies with the pre-mix from the last layer's FFN mixes — the mix the reference applies via `last_layer.hc_pre(h, pre_mix)` (**v4.1 has no learned hc_head**) » |

Leçon, la même qu'au tour précédent : **« je n'ai pas trouvé » n'est pas « ça
n'existe pas »**. Le refus était honnête dans sa forme (il nommait le manque) et
faux dans son contenu — et un refus faux coûte plus cher qu'un refus muet, parce
qu'il décourage la recherche.

## 2. La chaîne de V4.1, en trois phrases

1. **Le post d'abord** : `mhc_shifted_post_pre` applique le `post` du raccord
   précédent, *puis* appelle la pré-retardée sur le flux **post-mappé**
   (`vllm/models/deepseek_v41/nvidia/ops/mhc.py:256-280` : `residual =
   mhc_post_tilelang(...)` puis `mhc_pre_delayed_overlap(residual, ...)` avec
   `x=None`, donc les mélanges sont calculés sur le flux post-mappé).
2. **Les coefficients se retardent d'un raccord** : « The reference collapses
   each sublayer's input with the *previous* sublayer's pre-mix: attention uses
   the pre-mix carried in (identity for the first layer), the FFN uses this
   layer's attention pre-mix ». Au tout premier raccord, `pre_mix is None` →
   la référence prend **`residual[:, 0]`**, la copie 0, sans mélange
   (`kernels/mhc/torch.py`, `mhc_pre_delayed_torch`).
3. **Pas de tête apprise** : le flux final est replié avec la `pre` de la
   **dernière FFN** (celle qui a été calculée sur le flux d'avant son `post`),
   puis `output_norm`. C'est le seul repliement que le fichier permet : le jeu de
   tenseurs `deepseek41` ne contient aucun `output_hc_*`.

V4 (`deepseek4`, V4-Flash) ne fait **pas** ça : chaque raccord s'y replie avec
ses propres coefficients — c'est la chaîne validée à 1e-7 contre llama.cpp
(`reports/rapport-v4-couches-0-1.md`). Deux architectures, deux chaînes, un seul
drapeau pour les distinguer (`general.architecture`), et le moteur **annonce**
laquelle il applique.

## 3. Ce qui a été implémenté

| pièce | où | ce que ça change |
|---|---|---|
| `hc_retarde` (détecté sur `general.architecture == "deepseek41"`) | `model.rs` (champ + chargement) | choisit la chaîne ; annoncé au chargement |
| coefficients portés d'un raccord au suivant | `forward` (attn puis FFN) | `melanger(&x, &hc_porte)` au lieu de `&s.pre` ; `hc_porte = sf.pre` après la FFN |
| tête non apprise | `forward` (fin) | repliement par `hc_porte` + `output_norm` |
| refus si le flux ne peut pas porter la `pre` | `forward` (nœud qui reprend à `couche_debut > 0`), `norme_finale` | un nœud de grappe replierait avec la copie 0 : faux et muet |
| `--tete-partielle` | `main.rs` | applique la tête à la fin d'une plage `--couches`, sinon une plage partielle rend le flux brut et la tête ne voit jamais le jour |
| dumps `hc_ffn_in`, `hc_ffn_pre`, `hidden_final` | `vider_couche` | de quoi recalculer la chaîne hors du moteur |

Trois bugs de configuration ont été trouvés **par** cette exécution — chacun
rendait le modèle faux en silence, et aucun n'était visible dans un inventaire :

| symptôme | cause | correctif |
|---|---|---|
| `tenseur blk.0.ffn_gate.weight absent` | `n_expert` relu en GGUF-seul (`expert_count`) alors que V4.1 ne déclare que `n_routed_experts` ; `routage_du_gguf` lisait déjà correctement les trois sources, mais **le résultat était jeté** (variables mortes) | `Cfg` prend les valeurs de `routage_du_gguf` |
| toutes les normes décalées d'environ 1e-6 | `rms_norm_eps` (**1e-20**, déclaré par le GGUF `deepseek41.rms_norm_eps` et par le JSON) au lieu de `attention.layer_norm_rms_epsilon` (absent) → repli sur 1e-6 | `reel_gguf([... , "rms_norm_eps"], …)` |
| « le modèle ne déclare pas YaRN » | V4.1 déclare YaRN dans le **JSON** (`rope_scaling`, facteur 16), pas en clef GGUF | troisième source lue, et message qui dit ce qui est appliqué. **Ce que ce correctif ne fait pas** : changer la rotation aux contextes courts — le moteur bascule à 4 × 65536 = 262144 jetons, donc à `--ctx 8` le RoPE appliqué est le même avant et après. Ce qui change vraiment : le message, `DRAVE_YARN=1` (inerte tant que la déclaration n'était pas lue) et l'application au-delà du seuil |

## 4. La vérification, sur le fichier de 365,7 Go

Commande — `--couches 0:1` exécute la couche **0** seule (`[0,1)`) : c'est la
seule couche du modèle sans compression ET sans engram, donc la seule dont la
passe avant soit complète à ce stade. La couche 1 porte l'engram (dont l'injection
n'est pas branchée), la 2 ouvre les couches compressées :

```
DRAVE_DUMP_COUCHES=/tmp/dump_v41 ./drave-core/target/release/drave \
    /home/stephane/FastNVMe/modeles-lourds/DeepSeek-V4.1-Flash-Q2.gguf \
    --couches 0:1 --tete-partielle --ppl /tmp/v41_texte.txt.ids --ctx 8 --limit 4
```

`tools/verifier_v41_mhc.py` relit les vides et recalcule **en numpy**, depuis les
tenseurs du GGUF, les quatre étapes — sans passer par le code Rust :

| position (jeton) | ① copie 0 = embarquement | ② les 24 mélanges | ④ repli de la FFN | ③ la tête | dynamique |
|---|---|---|---|---|---|
| 0 (201) | **0,000e+00** | 8,354e-08 | 1,049e-08 | 6,753e-07 | 3,113 |
| 1 (438) | **0,000e+00** | 8,210e-08 | 1,449e-08 | 4,031e-07 | 2,939 |
| 2 (10498) | **0,000e+00** | 4,327e-08 | 2,846e-08 | 4,696e-07 | 1,167 |
| 3 (102771) | **0,000e+00** | 8,594e-08 | 4,885e-08 | 2,273e-07 | 1,178 |

④ est le **maillon central** de la chaîne retardée : l'entrée de la FFN se replie
avec la `pre` de l'**attention**, pas avec la sienne. Les trois premières égalités
ne le couvraient pas (elles vivent toutes en aval de `l_last`) : une relecture
adverse l'a relevé, et ces deux vides (`hc_pre_attn`, `hc_mel_ffn`) le rendent
vérifiable — échanger les deux coefficients à cet endroit ferait tomber ④.

- ① est **exact** : au premier raccord, le flux replié *est* la copie 0, au bit
  près. La chaîne de V4 donnerait `(Σ pre)·embarquement` — un vecteur différent,
  donc ce zéro est un discriminant, pas une tautologie.
- ②, ③ et ④ sont à 1e-8…7e-7 sur une dynamique de 1 à 3 : l'arrondi f32 (le
  moteur calcule en f32, le vérificateur en f64).

**Verdict : les quatre égalités tiennent.** Et la chaîne écrite à l'envers n'est
pas une variante cosmétique : sur le témoin synthétique
(`tools/mhc_v41_synthetique.py`), la tête retardée diffère de **67 %** de la tête
directe. C'est aussi ce que fixe le test unitaire
`model::tests_hc::chaine_retardee_v41` (témoins générés par ce script).

Ce que cette vérification **ne** dit pas : que les couches 0 et 1 produisent les
mêmes nombres qu'un runtime de référence. Aucun runtime public ne charge ce
fichier (llama.cpp n'a qu'un patch de conversion), donc la comparaison externe
n'existe pas encore — c'est une vérification **interne**, de bout en bout, de la
chaîne mHC. Les logits publiés ci-dessus appartiennent à un modèle **tronqué**
(1 couche sur 40) : ils ne disent rien de sa qualité.

## 5. Le compresseur des ratios 1 et 2 : les couches SOURCES tournent, et sont vérifiées

Deuxième manque annoncé, deuxième manque faux. Le compresseur de V4.1 est
spécifié par `DeepseekCompressor` + `fused_save_compress_norm` : une **valeur** de
512 par jeton, une **porte** de 512 seulement si `ratio > 1` (`has_gate =
compress_ratio > 1`), **aucun `ape`**, et un pool qui est un softmax **par canal**
sur le groupe (`pooled = tl.sum(kv * tl.softmax(score, 0), 0)`) — pour le ratio 1,
la référence écrit simplement `pooled = kv`.

Ce chemin est implémenté pour les couches **sources** (celles qui possèdent leurs
tenseurs de compresseur), et vérifié sur le fichier réel :

| couche (ratio) | bloc | pool (`comp_brut`) | norme + RoPE de bloc (`comp_bloc`) | dynamique |
|---|---|---|---|---|
| 2 (ratio 2) | 0, groupe {0,1} | 5,08e-07 | 3,04e-06 | 1,245 |
| 2 (ratio 2) | 1, groupe {2,3} | 5,08e-07 | 3,04e-06 | 1,245 |
| 20 (ratio 1) | 0..3, un par jeton | 3,47e-07 | 5,59e-06 | 2,561 |

`tools/v41_compresseur_reference.py` recalcule en numpy, depuis les tenseurs du
GGUF, la projection, la norme RMS du latent et le RoPE appliqué aux **64
dernières** composantes à la position du **premier** jeton du groupe (`position //
ratio * ratio`, appariement NORM) : l'écart est de l'ordre de l'arrondi f32, donc
la projection, l'instant d'émission du bloc, le groupe et la rotation sont justes.
Réserves assumées, et elles sont plus larges que « l'orientation du softmax » :
l'état injecté est le même à toutes les positions, donc le pool d'un groupe y vaut
la valeur du jeton **quel que soit** le jeu de poids — ce tableau ne prouve ni le
groupe, ni l'orientation du softmax par canal, ni la **projection de porte**
(`attn_compressor_gate`, jamais comparée) ; il ne prouve pas non plus la
comparaison à une référence EXTERNE, puisque la rotation du moteur est ici le RoPE
simple alors que vLLM applique YaRN (facteur 16) à toutes les positions des couches
compressées. Ce qui est prouvé : la projection de valeur, la norme du latent, la
position du RoPE de bloc, et l'instant d'émission du bloc (un par jeton en ratio 1,
un par groupe de deux en ratio 2).

L'**indexeur** de V4.1 n'a pas de compresseur propre : ses clés viennent du latent
du compresseur principal (`indexer.attn_k` [128,512] + `indexer.k_norm`) et il
partage le cache de clés de sa source. Ce chemin n'est pas porté ; tant qu'il ne
l'est pas, le moteur **garde tous les blocs**, ce qui est exact sous `indexer.top_k`
(512) — et il **refuse** au-delà plutôt que de choisir au hasard. Les deux
comportements sont annoncés une fois.

## 6. Le cache compressé partagé : les 34 couches consommatrices aussi

« Compressors and compressed-KV caches live only on `kv_source_layer_ids`;
consumers reuse the most recently published source below them » (vLLM,
`deepseek_v41/attention.py`). Le moteur **n'indexe donc pas** les tampons du
compresseur par couche, mais par **source** (`comp_source`) : une couche
consommatrice lit l'état et les blocs publiés par sa source, qui a déjà été
calculée pour ce jeton (sa couche est en dessous). Elle ne projette rien — elle
n'a pas de tenseurs — et ne réécrit aucun bloc.

Vérification, par **contrôle positif/négatif** plutôt que par relecture : la même
couche 3, exécutée (a) après sa source (plage 2..5) et (b) seule (plage 3..4, donc
avec un cache de source jamais rempli).

| mesure | résultat |
|---|---|
| sortie de la couche 3 (a) contre (b) | **écart max 1,30 à 2,16** sur une dynamique de 2,49 à 3,53 → la couche 3 dépend bien de l'état de sa source |
| sortie de la couche **2** dans les deux exécutions | **0,000000e+00** (identique au bit) → le partage ne perturbe pas la source, et le harnais est stable |
| sortie de la couche 3 contre la couche 2 | écart 0,76 à 1,12 → la couche 3 a bien ses propres requêtes et poids |

Si la couche 3 lisait un état à elle (ou un tampon vide), les deux exécutions
donneraient le **même** résultat : c'est ce que ce contrôle exclut. Reste non
vérifié : la valeur *absolue* de la sortie d'une couche consommatrice contre une
référence externe (aucun runtime public ne charge ce fichier) ; et l'orientation
du softmax par canal, qui est maintenant couverte par un test unitaire à témoin
(`model::tests_hc::pool_du_compresseur_est_par_canal` : deux jetons différents,
poids 0,5/0,5 et 0,25/0,75).

## 7. L'engram : branché, et vérifié de bout en bout

Dernier manque de code de P7, et le plus gros morceau de V4.1 : **deux tables de
101 Go** (203 Go à elles deux, 55 % du fichier), un hachage d'n-grammes, et une
injection sur le flux résiduel. La référence dit tout :
`vllm/models/deepseek_v41/common/engram.py` — « The hash ids fetch `n_hash_cols`
rows; `wkv` turns them into **one key per hc copy plus a shared value**. The gate
is a normalized dot product of the stream against the key, signed-sqrt'ed before
the sigmoid ».

Ce qui a été branché dans la passe avant :

| pièce | où | ce qu'elle fait |
|---|---|---|
| hachage glissant | `Engram::adresses` | 24 colonnes = 3 reculs × 8 têtes ; la FENÊTRE suffit (`max_ngram − 1` jetons), donc O(1) par jeton — le vérificateur recalcule, lui, sur tout le préfixe, ce qui contrôle l'équivalence |
| lecture des rangées | `engram::lire_rangee` | 264 octets = 256 valeurs e4m3 + 8 échelles e8m0, par blocs de 32 |
| projection | `wkv` [25 600, 6 144] | 24 colonnes × 256 valeurs → `hc` clés + **une valeur partagée** (5 × 5 120) |
| injection | `PorteEngram::injecter` | par copie : `sigmoïde(signe(d)·racine(max(\|d\|, 1e-6)))` · valeur partagée, ajoutée au flux ; `eps` = `rms_norm_eps` = 1e-20 |
| position | en tête de la couche, avant les mélanges | la référence : `residual = self.engram(previous_post, …)` **puis** `mhc_pre(residual, …)` |

Vérification (`tools/verifier_v41_engram.py`), sur les couches 0 et 1 du fichier de
365,7 Go — les adresses recalculées par la **référence** (`tools/engram_reference.py`,
transcription de `engram.py`, déjà validée), les rangées relues dans la vraie
table, puis la projection et l'injection :

| position | projection (`engram_kv`) | injection (`engram_sortie`) | dynamique |
|---|---|---|---|
| 0 | 3,135e-05 | 1,744e-07 | 0,538 |
| 1 | 8,613e-06 | 1,057e-06 | 0,548 |
| 2 | 2,789e-05 | 1,157e-06 | 1,160 |
| 3 | 9,716e-06 | 1,089e-06 | 3,491 |

La projection est à ~1e-5 : c'est l'accumulation f32 sur 6 144 termes (le
vérificateur calcule en f64), et une seule valeur de table mal déquantifiée
donnerait un écart cent fois plus grand — donc la lecture des rangées et l'ordre
d'assemblage des 24 colonnes sont justes. L'injection est à ~1e-6.

Ce que ça coûte, annoncé au chargement : **6 336 octets par jeton et par table**
(24 rangées de 264), soit 12 672 pour les deux — la mesure de flux antérieure
(12 665) donnait 7 octets de moins, une rangée partagée entre deux colonnes.

**Ce qui n'est pas fait sur l'engram** : le masque des jetons d'**image**
(`dead_mask = image_sentinel_mask`) — un texte seul n'a aucun jeton sentinelle,
donc l'équivalence est exacte ici, mais un modèle multimodal demanderait ce
masque ; et le pas de temps du hachage sur de très longues séquences
(l'implémentation est O(1) par jeton, le vérificateur O(préfixe)).

## 8. La première passe avant V4.1 **complète**

Avec l'engram branché, la liste des manques de V4.1 est **vide** : le moteur
exécute les **40 couches** du fichier de 365,7 Go — hyper-connexions retardées,
cache compressé partagé (ratios 1 et 2), engram, MoE à 384 experts, tête finale
sans poids appris.

```
$ ./drave-core/target/release/drave DeepSeek-V4.1-Flash-Q2.gguf \
      --ppl /tmp/v41_texte.txt.ids --ctx 8 --limit 4
       3 tokens notés — perplexité cumulée 39839289.516  (0.1 tok/s)
```

Ce que ce chiffre est : **la preuve que la passe tourne**, pas une mesure de
qualité. Ce qu'il n'est pas : une perplexité. Trois jetons et huit positions ne
disent rien d'un modèle, et à cette taille l'indexeur garde tous les blocs
(`n_vis` ≪ `top_k`). Le débit non plus n'est pas une mesure du modèle : 55 s pour
la passe entière (chargement compris), dont **7 223 ms/jeton d'attention** et
**6 874 ms/jeton de projections + MoE**, parce que le chemin V4 fait ses
projections en `f32` naïf (`matvec_f32`) — c'est un poste de P9, pas un résultat.

Ce que la passe établit, en revanche, et que rien d'autre ne pouvait établir :
les 40 couches s'enchaînent sans incohérence, le flux est compté
(**19 191 M paires/jeton**, dont 7 204 M pour l'attention et 11 325 M pour les
experts — 37,5 % d'attention), et les 203 Go de tables d'engram sont lus sans
être chargés.

## 9. Ce qui reste, nommé

L'inventaire de V4.1 (1 046 tenseurs, 40 couches) donne la liste exacte :

| manque | ce que dit le fichier | pourquoi ce n'est pas fait |
|---|---|---|
| **cache compressé partagé** | `kv_source_layer_ids = [2,8,14,20]`, `compress_ratios = [0,0,2×18,1×20]` | **fait** : les sources projettent, les consommatrices lisent leurs tampons (`comp_source`), et le contrôle positif/négatif est concluant (§6). La couche 14 (source ET engram) reste refusée par le manque engram |
| ratios 1 et 2 | `attn_compressor_kv` sans `ape`, `attn_compressor_gate` seulement en ratio 2 | **fait** pour les couches sources, vérifié sur les couches 2 et 20 (§5) |
| indexeur sans compresseur propre | `indexer.attn_k` [128,512], `indexer.k_norm` [128], `indexer.attn_q_b`, `indexer.proj` | les clés de l'indexeur viennent du **latent du compresseur principal** (le fichier n'a pas d'`indexer_compressor_*`), et il partage le cache de son `kv_source` |
| sélection à deux niveaux | `candidate_source_layer_id = 20`, `candidate_topk_blocks = 2048`, `candidate_block_size = 8` | aucune source d'exécution lue à ce jour |
| **engram** | couches 1 et 14 : `engram_embd` (101 Go), `engram_kv` [25600,6144], `engram_q_norm`/`k_norm` [4,5120] | **fait** (§7) : hachage, lecture des rangées, projection et injection branchés et vérifiés ; restent le masque des jetons d'image (sans objet en texte seul) |
| **pré-mix sur le fil** | — | la chaîne retardée a besoin de `hc` valeurs par jeton que le protocole DRVF ne transporte pas (16 octets/jeton) : un découpage de V4.1 est refusé |
| YaRN toujours actif | `rope_scaling.factor = 16`, `original_max_position_embeddings = 65536` | le moteur ne l'applique qu'au-delà de 4 × la longueur déclarée (mesure gpt-oss) ; `DRAVE_YARN=1` l'applique partout, comme la référence — le message du chargement le dit désormais |
| DSpark / MTP | `num_nextn_predict_layers = 3`, `dspark_*` | tête spéculative, hors du chemin d'un modèle autorégressif simple |

Détail cosmétique connu : la ligne `[config] … ffn 2816 …` lit
`intermediate_size` dans le premier bloc JSON qui le contient — pour V4.1 c'est
celui de `vision_config` (2816) et non le texte (2304). Le champ est **inerte**
sur un modèle à experts (la largeur du FFN partagé vient de la forme du tenseur),
mais le chiffre affiché est faux.

## 10. Reproduire

```bash
# la chaîne, témoins numpy ↔ moteur
python3 tools/mhc_v41_synthetique.py          # témoins (test Rust)
(cd drave-core && cargo test --release chaine_retardee_v41)

# la vérification sur le vrai modèle
DRAVE_DUMP_COUCHES=/tmp/dump_v41 ./drave-core/target/release/drave \
    /home/stephane/FastNVMe/modeles-lourds/DeepSeek-V4.1-Flash-Q2.gguf \
    --couches 0:1 --tete-partielle --ppl /tmp/v41_texte.txt.ids --ctx 8 --limit 4
python3 tools/verifier_v41_mhc.py \
    /home/stephane/FastNVMe/modeles-lourds/DeepSeek-V4.1-Flash-Q2.gguf \
    /tmp/dump_v41 /tmp/v41_texte.txt.ids

# le compresseur d'une couche SOURCE (ratio 2 : couche 2 ; ratio 1 : couche 20).
# La plage commence au milieu du modèle : le moteur l'annonce, et l'état est
# INJECTÉ pour que l'entrée du compresseur soit reproductible.
python3 -c "import numpy as np; h=5120; v=(np.sin(np.arange(h)*0.01)+(np.arange(h)%7)*0.1).astype(np.float32); np.tile(v,4).astype('<f4').tofile('/tmp/etat_l2.bin')"
DRAVE_ETAT_ENTREE=/tmp/etat_l2.bin DRAVE_DUMP_COUCHES=/tmp/dump_l20 \
  ./drave-core/target/release/drave \
    /home/stephane/FastNVMe/modeles-lourds/DeepSeek-V4.1-Flash-Q2.gguf \
    --couches 20:21 --tete-partielle --ppl /tmp/v41_texte.txt.ids --ctx 8 --limit 4
python3 tools/v41_compresseur_reference.py \
    /home/stephane/FastNVMe/modeles-lourds/DeepSeek-V4.1-Flash-Q2.gguf \
    /tmp/dump_l20 20 /tmp/etat_l2.bin 1 0 1 2 3
```

## 11. Sources

- vLLM, `vllm/models/deepseek_v41/nvidia/model.py` (`mhc_shifted_post_pre`,
  `hc_collapse_triton`, `_collapse`, `kv_source_layer_ids`) —
  <https://github.com/vllm-project/vllm/blob/main/vllm/models/deepseek_v41/nvidia/model.py>
- vLLM, `vllm/model_executor/kernels/mhc/torch.py` et `cpu.py` (références
  « eager » des blocs mHC) —
  <https://github.com/vllm-project/vllm/blob/main/vllm/model_executor/kernels/mhc/torch.py>
- vLLM, `vllm/models/deepseek_v41/compressor.py` et
  `vllm/models/deepseek_v41/common/ops/fused_compress_quant_cache.py` (ratios 1
  et 2, softmax par canal, RoPE de groupe) —
  <https://github.com/vllm-project/vllm/blob/main/vllm/models/deepseek_v41/compressor.py>
- vLLM, `vllm/models/deepseek_v41/attention.py` (topologie « sparse-attention » :
  sources de KV et d'indexeur, candidats) —
  <https://github.com/vllm-project/vllm/blob/main/vllm/models/deepseek_v41/attention.py>
- vLLM, `vllm/model_executor/kernels/mhc/triton.py` (`hc_collapse_triton`,
  moyenne des copies pour les états auxiliaires) —
  <https://github.com/vllm-project/vllm/blob/main/vllm/model_executor/kernels/mhc/triton.py>
