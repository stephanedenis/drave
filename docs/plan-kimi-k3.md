# Plan — Kimi-K3 : exécuter en local ce qui ne tient pas en local

> Écrit le 03/10 (bloc 27) après une réorientation explicite : **les modèles
> périmés sortent du chemin critique** (DeepSeek-V4-Flash : acquis conservés,
> portes archivées) et le travail se porte sur **les meilleurs modèles ouverts**,
> « particulièrement ceux qui sont typiquement trop gros pour l'exécution
> locale ». Kimi-K3 est la cible : le plus récent des gros ouverts, 1 M de
> contexte, multimodal, et **1,5 To** dans sa quantization Q4.

## 1. Ce qui est mesuré (03/10)

| fait | valeur | source |
|---|---|---|
| GGUF visé | `unsloth/Kimi-K3-GGUF`, **UD-Q4_K_XL**, **32 shards, 1 508,7 Go** | API Hugging Face |
| architecture déclarée | **`kimi-k3`** — notre moteur ne la connaît pas | `general.architecture` du shard 1 |
| structure du texte | **93 couches** · hidden **7 168** · ffn 33 792 · **896 experts, 16 par jeton** · groupe 1 · gating 2 · contexte **1 048 576** | métadonnées `kimi-k3.*` |
| attention | `head_count 96` · `key_length 576` · `value_length 74` · `head_count_kv` **par couche** (1 sur 4) → hybride | idem |
| le texte EST Kimi-Linear | `text_config.architectures = ['KimiLinearForCausalLM']`, `linear_attn_config.full_attn_layers = [4,8,12,…]`, `hidden_act = situ`, `mla_use_nope`, `mla_use_output_gate`, `kv_lora_rank 512`, `first_k_dense_replace 1` | `config.json` du dépôt officiel |
| experts | **MXFP4** dans le Q4 (41,93 Go pour 3 couches) | en-tête du shard 2 |
| **poids lus par jeton** | **≈ 35 Go** (16/896 experts × 93 couches) = **2,3 % du modèle** | `tools/analyse_octets_par_jeton.py` |
| planchers qui en découlent | disque dur **173 s/jeton** · NVMe (2 Go/s) **17 s** · PCIe x8 (6,5 Go/s) **5,4 s** · RAM (20 Go/s) **1,7 s** | débits mesurés les 02-03/10 |
| débit de téléchargement | **108 Mo/s** → ~4 h pour 1,5 To | mesuré sur le transfert en cours |

**Ce que ce tableau dit en une phrase** : un jeton de Kimi-K3 Q4 a besoin de
**35 Go de poids**, soit 12 fois notre RAM (125 Go) pour *huit* jetons. Le
problème n'est donc pas « faire tenir le modèle » (1,5 To ne tiendront jamais),
c'est **de ne lire que ce qui sert** — et c'est exactement le sujet du projet.

## 2. La référence existe — et c'est nouveau

Contrairement à V4.1 (où llama.cpp refuse l'architecture, ce qui a rendu la porte
de correction **impossible**), Kimi-K3 a une référence exécutable :

- **llama.cpp amont connaît `kimi-k3`** (`LLM_ARCH_KIMI_K3` dans `llama-arch.cpp`
  de `master`, vérifié par `web_fetch` le 03/10) — et Unsloth publie un *fork PR*
  dédié (`unslothai/llama.cpp#48`) ;
- notre copie locale de llama.cpp est **plus ancienne** (elle ne connaît que
  `kimi-linear`) : une **seconde copie** est donc construite
  (`/home/stephane/Data13TB/stephane/GitHub/llama.cpp-k3`) pour servir de
  **référence externe**, sans toucher à celle qui produit nos chiffres actuels ;
- le dépôt officiel publie le **code de référence** (`modeling_kimi_k3.py`,
  `configuration_kimi_k3.py`, `encoding_k3.py`) — de quoi vérifier pièce par
  pièce, comme on l'a fait pour V4.1 avec vLLM.

**Conséquence pour les portes** : la porte de correction peut être **tenue** sur
ce modèle (étage par étage contre llama.cpp amont), là où elle était impossible
sur V4.1. C'est la première fois que la classe « trop gros pour le local » a les
deux portes disponibles **en même temps**.

## 3. Ce qui nous distingue sur cette classe (mesuré, pas supposé)

1. **Le placement du stockage décide** : le même protocole rejoué sur disque dur
   et sur NVMe donne **1 027,7 s contre 567,1 s (×1,81)** — et un débit *plat*
   sur NVMe contre *décroissant* sur disque dur (`sprints/25`).
2. **Le découpage en grappes** : `commun.gguf` + `cluster-XX.gguf`, 11 008
   entrées de mapping, **aucune requantification**, perplexité identique au
   chiffre près, et perplexité répartie **exacte** (0,00e0 sur les modes 0, 1, 3).
   Sur un modèle dont **chaque jeton ne touche que 16 experts sur 896**, chaque
   nœud ne lit que ce qu'il sert : c'est le levier principal.
3. **La réutilisation entre jetons** : mesurée sur un autre modèle (50 % des
   lectures dans 394 experts, **31,9 % de réutilisation entre jetons
   consécutifs**) — avec 896 experts et un top-16, elle est à remesurer *ici*, et
   c'est elle qui décide si un cache paie (le cache RAM d'experts a été mesuré
   **plus lent** sur V4.1 : +4 % à 4 Go, +21 % à 32 Go — le noyau fait déjà le
   travail ; il faut donc une raison plus forte, comme le découpage).
4. **Le transport compact** : cinq modes de flux, listes DRVF, perte mesurée et
   plafonnée (3,65e-2 · 4,45e-3) ; la granularité **route** plus qu'elle ne
   compresse (`reports/rapport-granularite-flux.md`).
5. **Les noyaux** : le CPU est 5 à 7× au-dessus du plancher PCIe → le calcul est
   le mur ; matvec parallèle par lignes (**×9,34**, bit à bit identique),
   déquantification AVX2 **bit-exacte** (Q2_K ×1,33), produit scalaire vectorisé
   (**×1,18** sur la passe, écart **dit** : +0,15 % de perplexité).

## 4. Jalons

| # | jalon | état |
|---|---|---|
| M1 | **Télécharger** le Q4 (1 508,7 Go, 32 shards, reprise par tranches) | **en cours** (~108 Mo/s, ~4 h) |
| M2 | **Lire la structure** : tous les tenseurs, leurs types, les clés `kimi-k3.*` — et faire dire au moteur ce qui lui manque (`--config`, refus **bruyant**, jamais un silence) | à faire |
| M3 | **Construire la référence** (llama.cpp amont, `kimi-k3`) et la faire tourner sur quelques jetons | **en cours** (clone + build) |
| M4 | **Premier étage** : embarquement + la première couche dense (`first_k_dense_replace = 1`), comparaison tenseur par tenseur | à faire |
| M5 | **Les couches à attention linéaire** (le cœur nouveau : `full_attn_layers` une sur quatre, `situ`, `mla_use_nope`) vérifiées contre le code publié | à faire |
| M6 | **Trace de routage** sur le vrai modèle : quels experts, quelle réutilisation entre jetons — puis **grappes** | à faire |
| M7 | **Exécution locale mesurée** : 1 nœud, 2 nœuds, avec et sans grappes ; jetons/s, octets lus par jeton, et comparaison à llama.cpp | à faire |
| M8 | **Le verdict « trop gros »** : ce qu'il faut (RAM, disques, nœuds) pour un débit utile, et où le projet gagne ou perd | à faire |

## 5. Ce qui est mis de côté, et pourquoi c'est écrit

- **DeepSeek-V4-Flash** : périmé comme cible (acquis conservés dans les rapports
  et l'audit `reports/rapport-portes-p0-p9.md` ; la copie NVMe est supprimée, la
  copie disque dur reste tant que les portes archivées s'y réfèrent). Les
  enseignements — stockage, noyaux, portes — servent directement à Kimi-K3.
- **DeepSeek-V4.1-Flash-Q2** : reste sur le disque (341 Go) ; son intérêt est
  d'être le cas « porte de correction impossible », pas une cible.
- **Le plan V4.1 (P0→P9)** : son exécution est auditée porte par porte ; il n'est
  pas effacé, il est **clos** comme référence méthodologique.
