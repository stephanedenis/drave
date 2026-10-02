# Rapport — test d'exécution locale de DeepSeek-V4.1-Flash, avec toutes les optimisations

02/10, sur la copie NVMe `/home/stephane/FastNVMe/modeles-lourds/DeepSeek-V4.1-Flash-Q2.gguf`
(365,71 Go, 1 046 tenseurs, 40 couches, 384 experts dont 6 par jeton).

**Verdict en une ligne : ce que le moteur sait faire de ce modèle marche et est
mesuré ; la passe avant est refusée en 0,33 s avec la liste exacte de ce qui
manque. Aucun chiffre de calcul sur V4.1 n'existe, ici ou ailleurs dans ce
dépôt — uniquement des mesures statiques.**

## 1. Ce qui tourne, avec les optimisations

| test | commande | résultat mesuré |
|---|---|---|
| en-têtes seuls (`--tensors`) | mmap, aucune copie | 1 046 tenseurs, **365,70 Go** lus en **63,8 ms** |
| configuration (`--config`) | en-tête seul | **74 ms** au total, aucune donnée lue |
| plan matériel (`--materiel`) | détection + heuristiques | 20 threads, 16 lecteurs disque, cache experts 19,5 Go, cache KV 32 bits |
| sonde engram (`--sonder-engram 10000`) | mmap, 16 lecteurs | table 1 : 10 000 entrées en **524 ms** (2,6 Mo touchés sur 101,4 Go) · table 2 : **219 ms** · RSS max **120 Mo** pour 365,7 Go adressés |
| passe avant (`--ppl`) | `DRAVE_PRELIRE_TOUT=1 DRAVE_GPU=1` | **refusée en 0,33 s**, RSS 47 Mo |

Les optimisations demandées sont donc toutes exercées là où elles s'appliquent :
mmap sans copie (365,7 Go adressés, 120 Mo résidents), parallélisme des lecteurs
de la sonde engram, heuristiques matérielles du plan, prélecture et déport GPU
activés pour la passe avant — qui, elle, ne va pas plus loin que le contrôle
d'architecture.

## 2. Pourquoi la passe avant s'arrête, en entier

Le contrôle nomme maintenant **les quatre mécanismes manquants**, d'après le
code de référence `llama.cpp/src/models/deepseek4.cpp` (1 253 lignes) :

| mécanisme | ce que c'est | où c'est dans llama.cpp |
|---|---|---|
| **hyper-connexions** | l'état résiduel n'est pas UN vecteur mais **hc = 4** copies, mélangées à chaque sous-couche par `sigmoid(W·RMSNorm(x))` et un **Sinkhorn** à 20 itérations (`hc_mult`, `hc_sinkhorn_iters`) | `build_hc_pre`, `build_hc_sinkhorn`, `build_hc_post` |
| **sortie à rang faible groupée** | la projection de sortie passe par `wo_a` (`[n_head·head/o_groups, o_lora_rank·o_groups]`) puis `wo_b` (`[o_lora_rank·o_groups, n_embd]`), avec `o_groups = 8` | ligne 1131 |
| **dé-rotation + puits** | `attn_derope` ramène la sortie d'attention dans le repère **non tourné**, et `attn_sinks` ajoute un logit appris par tête | lignes 1120-1127 |
| **attentions compressées CSA/HCA** | `compress_ratios` fait cohabiter **trois** attentions dans le même modèle : compressée à candidats (CSA/LID, `candidate_topk_blocks = 2048`), compressée simple (HCA) et brute | `build_csa_lid_attention`, `build_hca_attention`, `build_raw_attention` |

**Ce qui n'est PAS un obstacle** : l'engram. Le moteur sait déjà l'**adresser**
(sonde ci-dessus) ; `llama.cpp` ne le calcule pas non plus (aucune occurrence de
« engram » dans `src/`). Une exécution comparable à la sienne n'en a donc pas
besoin — c'est écrit dans le contrôle, pour ne pas compter un manque qui n'en
est pas un.

Ce qui est déjà fait et servira : routage **sigmoïde/racine-de-softplus** avec
`expert_weights_scale`, routage **par table `ffn_gate_tid2eid`** des 3 premières
couches, lecture du bloc JSON `<arch>.config` (c'est lui qui donne à V4.1 ses 40
couches, 384 experts et sa fonction de score), et l'**attention MLA à rang
faible** validée contre llama.cpp sur GLM-5.3 (corrélation 0,999024).

## 3. Ce que coûterait la suite, honnêtement

Par ordre de difficulté croissante :

1. **sortie à rang faible groupée** — deux produits matriciels au lieu d'un,
   une heure avec la validation ; c'est le plus simple et il est indépendant.
2. **hyper-connexions** — l'état passe de `[h]` à `[4][h]` et chaque sous-couche
   gagne un mélange appris + Sinkhorn. Touche le cœur de `forward` ; c'est une
   demi-journée, et **toute erreur y est silencieuse** (les quatre copies
   restent des vecteurs plausibles).
3. **dé-rotation + puits** — une rotation inverse et un logit par tête : courte,
   mais elle ne sert que si les attentions compressées existent.
4. **attentions CSA/HCA** — le gros morceau : trois variantes, une sélection de
   candidats par blocs, des états de compression par couche source. C'est
   plusieurs jours, et c'est *le* cœur de ce que V4.1 apporte.

Tant que 1 à 4 ne sont pas faits **et** validés contre une référence, une
exécution de V4.1 produirait des nombres faux sans rien casser — exactement ce
que cette session a passé la nuit à traquer ailleurs (routage, `wv_b`). Le
moteur refuse donc, et le refuse en 74 ms.

## 4. Reproduire

```bash
V=/home/stephane/FastNVMe/modeles-lourds/DeepSeek-V4.1-Flash-Q2.gguf
drave $V --config                       # 74 ms : routage, dimensions, ce qui manque
drave $V --tensors                      # inventaire mmap
drave $V --materiel                     # plan matériel
drave $V --sonder-engram 10000          # 203 Go de tables adressées, 5 Mo touchés
drave $V --ppl /tmp/ids_qwen.txt --ctx 32 --limit 2   # refus nommé, 0,33 s
```
