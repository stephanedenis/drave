# Plan — Kimi-K3 : exécuter en local ce qui ne tient pas en local

> **Document daté.** Plan, note ou étude d'un chantier : il porte sa date et son état en tête. La
> **feuille de route courante** est [`roadmap.md`](roadmap.md) ; l'**état** est
> [`en-cours.md`](en-cours.md).

> Écrit le 03/10 (bloc 27) après une réorientation explicite : **les modèles
> périmés sortent du chemin critique** (DeepSeek-V4-Flash : acquis conservés,
> portes archivées) et le travail se porte sur **les meilleurs modèles ouverts**,
> « particulièrement ceux qui sont typiquement trop gros pour l'exécution
> locale ». Kimi-K3 est la cible : le plus récent des gros ouverts, 1 M de
> contexte, multimodal, et **1,5 To** dans sa quantization Q4.

## 1. Ce qui est mesuré

### 1a. Le fichier est LÀ (bloc 31, 14:01)

**32/32 shards, 1 508,7 Go**, vérifiés à l'octet contre l'API Hugging Face
(`tools/apres-telechargement-k3.sh`, étape 1). Le transfert a tenu **111 Mo/s**
de moyenne sur 1,5 To.

### 1b. Le budget par jeton n'est plus une extrapolation (bloc 31)

Mesuré sur le fichier **complet**, 93 couches vues :

| poste | Go par jeton | part |
|---|---|---|
| experts routés (16 sur 896) | 25,830 | 29,8 % |
| partagé + attention + tête | **60,958** | **70,2 %** |
| **TOTAL** | **86,787** | |

Inventaire des 2 573 tenseurs : **2 722,7 G poids en MXFP4** (les experts) et
**56,1 G poids en Q8_0** (tout le dense) — d'où les ~59,6 Go du dense par jeton.
**Le dense pèse 2,3× les experts routés** : aucune technique sur les experts ne
peut adresser plus de 30 % du trafic d'un jeton. C'est la conclusion qui
réoriente la suite.

### 1c. Ce qui est mesuré (03/10)

| fait | valeur | source |
|---|---|---|
| GGUF visé | `unsloth/Kimi-K3-GGUF`, **UD-Q4_K_XL**, **32 shards, 1 508,7 Go** | API Hugging Face |
| architecture déclarée | **`kimi-k3`** — notre moteur ne la connaît pas | `general.architecture` du shard 1 |
| structure du texte | **93 couches** · hidden **7 168** · ffn 33 792 · **896 experts, 16 par jeton** · groupe 1 · gating 2 · contexte **1 048 576** | métadonnées `kimi-k3.*` |
| attention | `head_count 96` · `key_length 576` · `value_length 74` · `head_count_kv` **par couche** (1 sur 4) → hybride | idem |
| le texte EST Kimi-Linear | `text_config.architectures = ['KimiLinearForCausalLM']`, `linear_attn_config.full_attn_layers = [4,8,12,…]`, `hidden_act = situ`, `mla_use_nope`, `mla_use_output_gate`, `kv_lora_rank 512`, `first_k_dense_replace 1` | `config.json` du dépôt officiel |
| experts | **MXFP4** dans le Q4 (41,93 Go pour 3 couches) | en-tête du shard 2 |
| **poids lus par jeton** | **86,787 Go** (mesuré, bloc 31 — voir 1b) | `tools/budget_execution_locale.py` sur les 32 shards |
| planchers qui en découlent | disque dur **173 s/jeton** · NVMe (2 Go/s) **17 s** · PCIe x8 (6,5 Go/s) **5,4 s** · RAM (40 Go/s, mesuré) **2,17 s** | débits mesurés les 02-03/10 et bloc 31 |
| débit de téléchargement | **111 Mo/s** → 4 h 05 pour 1,5 To | mesuré sur le transfert |
| cadence des couches | **1 dense, 68 KDA, 24 MLA** · couche 92 MLA alors que 92 % 4 ≠ 3 | `--config` sur le fichier complet |

**Ce que ce tableau dit en une phrase** : un jeton de Kimi-K3 Q4 lit **86,8 Go de
poids** — dont **61 Go de partie dense** (attention, experts partagés, tête) qu'il
faut avoir **résidente**, et 25,8 Go d'experts routés. Le problème n'est donc pas
« faire tenir le modèle » (1,5 To ne tiendront jamais), ni seulement « ne lire que
les experts qui servent » : c'est **de garder le dense en RAM et de réutiliser les
experts** — et c'est exactement le sujet du projet. Mais le dense étant 2,3× les
experts, **le préremplissage par lots est la seule porte sérieuse** : il amortit
le dense par la taille du lot (`reports/rapport-prefill-par-experts.md`,
×1,58 mesuré de lot 1 à lot 192 sur Qwen3-30B-A3B, et 15,5× moins d'octets
d'experts). Le calcul, lui, ne s'amortit pas : ~210 GFLOP/jeton contre
56,7 GFLOP/s mesurés, soit **~3,7 s/jeton** — estimation à remplacer par une
mesure.

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
2. **Le dense d'abord** (fait mesuré le 03/10, bloc 29) : **62 Go de partie dense
   par jeton** (attention, experts partagés, tête) contre 24,7 Go d'experts
   routés. Un dispositif qui ne traite que le MoE laisse **56 % du trafic** de
   côté ; la partie dense doit être **résidente** (elle tient dans nos 125 Go,
   mais pas en même temps que V4.1-Flash) ;
3. **Le découpage en grappes** : `commun.gguf` + `cluster-XX.gguf`, 11 008
   entrées de mapping, **aucune requantification**, perplexité identique au
   chiffre près, et perplexité répartie **exacte** (0,00e0 sur les modes 0, 1, 3).
   Sur un modèle dont **chaque jeton ne touche que 16 experts sur 896**, chaque
   nœud ne lit que ce qu'il sert : c'est le levier principal.
4. **La réutilisation entre jetons** : mesurée sur un autre modèle (50 % des
   lectures dans 394 experts, **31,9 % de réutilisation entre jetons
   consécutifs**) — avec 896 experts et un top-16, elle est à remesurer *ici*, et
   c'est elle qui décide si un cache paie (le cache RAM d'experts a été mesuré
   **plus lent** sur V4.1 : +4 % à 4 Go, +21 % à 32 Go — le noyau fait déjà le
   travail ; il faut donc une raison plus forte, comme le découpage).
5. **Le transport compact** : cinq modes de flux, listes DRVF, perte mesurée et
   plafonnée (3,65e-2 · 4,45e-3) ; la granularité **route** plus qu'elle ne
   compresse (`reports/rapport-granularite-flux.md`).
6. **Les noyaux** : le CPU est 5 à 7× au-dessus du plancher PCIe → le calcul est
   le mur ; matvec parallèle par lignes (**×9,34**, bit à bit identique),
   déquantification AVX2 **bit-exacte** (Q2_K ×1,33), produit scalaire vectorisé
   (**×1,18** sur la passe, écart **dit** : +0,15 % de perplexité).

## 3bis. Le tokenizer est déjà vérifié — et il a trouvé DEUX défauts

Le tokenizer vit dans le shard 1 (déjà téléchargé) et la référence officielle est
en Python : la vérification a donc pu se faire **avant** la fin du transfert.

`tools/tokenizer_kimi/reference_officielle.py` est la réimplémentation du
tokenizer **officiel** (le `pat_str` de `tokenization_kimi.py` + les rangs
`tiktoken.model` du dépôt, avec le module `regex` de python3.14) ;
`tools/porte-tokenizer-kimi.sh` compare ses identifiants aux nôtres.

Deux défauts trouvés, tous les deux **silencieux** :

1. **Le motif de pré-découpage `kimi` n'était pas implémenté.** Notre tokenizer
   retombait sur le motif qwen2 pour tout ce qui n'était ni qwen2 ni gpt-4o —
   donc pour `tokenizer.ggml.pre = kimi-k2`, que déclarent **Kimi-K2.7 (déjà dans
   le dépôt) et Kimi-K3**. Conséquence mesurée : « 2026 » sortait en UN jeton au
   lieu de « 202 » + « 6 », et le texte chinois divergeait. Le motif a été
   transcrit de la référence (`llama.cpp-k3`, `unicode_regex_split_custom_kimi_k2`) :
   idéogrammes Han, lettres coupées par casse **en excluant les Han**, nombres par
   trois, contractions en suffixe.
2. **Le découpage par casse enjambait les majuscules** : « HelloWorld » sortait
   d'un seul morceau au lieu de « Hello » puis « World ». Ce défaut-là **ne se
   voyait pas dans les identifiants** (la table de fusions n'a pas de fusion
   « oW », donc le résultat tombait juste par chance) — il a été trouvé par un
   **test unitaire**, puis confirmé contre le motif officiel. Corrigé pour les
   deux matchers (kimi **et** gpt-4o).

**État** : 11 textes sur 11 donnent des identifiants identiques à
l'implémentation officielle (français accentué, anglais, code, chiffres, chinois,
casse alternée, espaces) ; 69 tests unitaires verts ; et les 512 identifiants
gpt-oss de la référence publiée (15,6017) sont **inchangés** — la
non-régression est mesurée, pas espérée.

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

## 4bis. Ce qui est prêt pour le jour J

Quand le transfert se termine (`tools/apres-telechargement-k3.sh`), la séquence est
**automatique et ordonnée** : (1) les 32 shards sont-ils complets, à la bonne
taille ? (2) que dit notre `--config` — et **quels** manques annonce-t-il ?
(3) la porte du tokenizer tient-elle toujours ? (4) le budget par jeton est-il
celui qu'on a extrapolé (88,5 Go) ? (5) la référence `llama.cpp-k3` tourne-t-elle,
et à quelle vitesse ? Chaque étape échoue **en disant laquelle** : un transfert
incomplet, une architecture non reconnue et un manque de mémoire ne se
ressemblent pas, et il ne faut pas les confondre à 14 h du matin.

La vérification de l'implémentation, elle, est écrite d'avance :
`docs/verification-kimi-k3.md` (13 points de comparaison, l'ordre, les tolérances).

## 5. Ce qui est mis de côté, et pourquoi c'est écrit

- **DeepSeek-V4-Flash** : périmé comme cible (acquis conservés dans les rapports
  et l'audit `reports/rapport-portes-p0-p9.md` ; la copie NVMe est supprimée, la
  copie disque dur reste tant que les portes archivées s'y réfèrent). Les
  enseignements — stockage, noyaux, portes — servent directement à Kimi-K3.
- **DeepSeek-V4.1-Flash-Q2** : reste sur le disque (341 Go) ; son intérêt est
  d'être le cas « porte de correction impossible », pas une cible.
- **Le plan V4.1 (P0→P9)** : son exécution est auditée porte par porte ; il n'est
  pas effacé, il est **clos** comme référence méthodologique.
