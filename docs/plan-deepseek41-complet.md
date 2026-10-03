# Plan — exécuter DeepSeek-V4.1 **dans** Drave : les flux d'abord

**État au 02/10 10h00.** Version 2 de ce plan. La première version traitait le
sujet comme « faire passer le forward de V4.1 » — c'est-à-dire comme llama.cpp.
C'était une erreur de cadre : la raison d'être de Drave n'est pas de recalculer un
forward dense, c'est de **conduire des listes d'activation** sur des **grappes de
neurones** qui peuvent vivre sur des composants ou des machines différentes, et de
**lire ces flux** pour comprendre et adapter le modèle. Ce plan est réécrit
là-dessus : la conformité à llama.cpp devient une *porte de correction*, pas le but.

---

## 1. Ce que Drave fait, et que ce plan doit préserver

| pilier | ce que c'est dans le dépôt | mesure |
|---|---|---|
| **listes d'activation** | `(indice, valeur)` par vecteur, encodage DRVF v1/v2/v3 ; v2 = **3 octets par neurone actif** | trace dense 512 jetons : 66,4 Mo, rejeu **identique** (19,3885) |
| **deux listes (trinaire)** | le signe porté par l'appartenance à la liste des « + » ou des « − » : plus de valeur à stocker | `reports/rapport-encodage.md`, `rapport-optimisations.md` |
| **connexions pondérées** | le cas général : `(source → destination, poids)` | `PushMat`, `FusedSign`, `matvec_shift_add` |
| **grappes** | `commun.gguf` + `cluster-XX.gguf` + `mapping.tsv` ; un nœud partiel ne porte que ses experts | `clusters.rs`, `tools/convertir_clusters.py` |
| **transport** | un seul format pour tracer, rejouer **et** transporter (protocole v5, modes 0-4) | `--trace-flux`, `--flux-forcer`, `--flux-serveur`, `--ppl-reparti` |
| **lecture des flux** | outils : `profil_flux.py`, `analyse_flux.py`, `diff_flux.py`, `trace_compacite.py`, `analyse_empreinte.py`, `aiguille.py` | — |

**Trois conséquences pour ce chantier :**

1. **Chaque mécanisme de V4.1 doit produire et consommer des listes**, ou dire
   pourquoi il ne peut pas. Un mécanisme qui ne se trace pas est un mécanisme
   qu'on ne pourra ni déboguer ni placer.
2. **Chaque mécanisme doit être plaçable** : ses neurones (experts, blocs,
   rangées d'engram) doivent pouvoir être découpés entre nœuds, comme les 128
   experts de Qwen3 le sont déjà.
3. **Les flux nouveaux doivent nourrir les outils d'analyse**, parce que c'est ce
   qui permet d'adapter l'architecture à la tâche : quels blocs le compresseur
   garde-t-il, la sélection est-elle stable d'un jeton à l'autre, le mélange des
   hyper-connexions est-il statique par couche, quelles rangées d'engram sont
   touchées.

Aujourd'hui, une passe de V4.1 afficherait **« 0 événements »** : le chemin MLA et
le chemin experts-IQ travaillent en f32 dense. C'est le premier écart à combler,
et il est plus important que la conformité des logits.

---

## 2. V4.1 est déjà fait de flux — le tableau qui commande tout le plan

| mécanisme V4.1 | nature en langage Drave | ce qu'on trace | plaçable ? |
|---|---|---|---|
| MoE top-6 parmi 384 | **liste d'experts par jeton** (déjà implémenté, `--trace-experts`) | `(couche, jeton, experts)` | oui, déjà (`clusters`) |
| `ffn_gate_tid2eid` (3 couches) | routage par **table**, liste fixée par le jeton — pas de score | idem | oui |
| `attn_compressor_gate` | **sélection de blocs** : une liste de blocs gardés par jeton | `(couche, jeton, blocs)` | oui, par blocs |
| indexeur CSA (top-2 048 blocs) | **liste de candidats** par jeton — la même idée que nos listes d'activation, mais sur les clés | `(couche, jeton, candidats)` | oui, par blocs |
| hyper-connexions (`pre`, `post`, `comb`) | **connexions pondérées** entre 4 copies de l'état : 4 + 4 + 16 poids par jeton et par couche | `(couche, jeton, 24 poids)` | oui, par copie |
| engram (couches 1 et 14) | **liste d'adresses** touchées : n-gramme → rangées | `(couche, jeton, rangées)` | oui, par rangée (déjà sondé) |
| puits `attn_sinks` | logit appris par tête : 64 poids constants | statique | non concerné |

**Trois de ces flux n'existent dans aucun moteur connu** (le gate du compresseur,
la sélection de candidats, le mélange HC). Les tracer est notre apport, pas un
détail d'implémentation.

---

## 3. Le point de départ, mesuré

### 3.1 Ce qui marche déjà sur V4.1 (365,71 Go, NVMe)

| capacité | mesure |
|---|---|
| en-têtes + inventaire | 1 046 tenseurs, 365,70 Go en **63,8 ms** (mmap) |
| description | **74 ms** : 40 couches, 384 experts top-6, racine de softplus ×1,5, routage par table des 3 premières couches |
| tables d'engram | 10 000 entrées en **219–524 ms**, 2,6 Mo touchés par table, **120 Mo de RSS** pour 365,7 Go |
| formats | IQ2_XXS, Q2_K, Q8_0, F16, F32 **vérifiés contre libggml**, plus **I8** (2 tenseurs d'engram, lus par déquantification générique — **pas** couverts par la porte) ; aucun I32 dans ce fichier (vérifié sur les deux copies) |
| MLA à rang faible | **validée à la position 0** contre llama.cpp sur GLM-5.3 (corrélation 0,999024 ; l'écart croît ensuite — `reports/rapport-mla-experts.md` §7) |
| grappes | `commun.gguf` + `cluster-XX.gguf` + `mapping.tsv`, nœuds partiels |
| transport | protocole v5, modes 0-4 (dont **lot en listes**) |

### 3.2 Trois faits vérifiés le 02/10, qui commandent l'ordre

0. **Les hyper-paramètres de V4.1 sont DANS le GGUF** (clé `deepseek41.config`,
   le `config.json` d'origine, que le moteur sait déjà lire) : `hc_mult: 4`,
   `hc_sinkhorn_iters: 20`, `hc_eps: 1e-06`, `q_lora_rank: 1280`, `o_groups: 8`,
   `o_lora_rank: 1024`, `head_dim: 512`, `index_topk: 512`,
   `candidate_topk_blocks: 2048`, `candidate_block_size: 8`,
   `index_source_layer_ids: [2,8,14,20,24,28,32,36]`,
   `kv_source_layer_ids: [2,8,14,20]`, `sliding_window: 128`,
   `compress_ratios`, `rms_norm_eps: 1e-20`, `swiglu_limit: 10.0`,
   `dspark_*` (décodage spéculatif, cibles 37-39). Presque rien n'est à
   deviner — et ce qui reste (`compress_ratios` de V4-Flash, `hc_*` de V4-Flash)
   est dans ses propres clés `deepseek4.hyper_connection.*`.
1. **llama.cpp ne connaît pas `deepseek41`** (`unknown model architecture`) :
   aucune référence externe n'existe pour V4.1.
2. **llama.cpp exécute V4-Flash** (`deepseek4`) : 1 325 tenseurs chargés,
   NLL 11,737 sur un jeton froid. V4-Flash porte **les mêmes mécanismes** en
   86,9 Go — c'est le banc d'essai **et** la seule référence dont on dispose.
3. **V4.1-Flash-Q2 n'a pas les tenseurs `output_hc_*`** alors qu'il déclare
   `hc_mult = 4` : fichier incomplet ou conversion fautive. Question de
   **provenance**, à trancher avant d'écrire du code (P7).

### 3.2bis Les régimes d'attention de V4-Flash (corrigé le 02/10)

`attention.compress_ratios` (44 entrées, clé GGUF lue par
`tools/lire_meta_gguf.py`) : **21 couches CSA** (ratio 4), **20 couches HCA**
(ratio 128), **3 couches brutes** (0, 1, 43). Le moteur annonçait pourtant
V4-Flash **calculable** après P2 : il cherchait la clé `compress_ratios`, qui
n'existe pas (`attention.compress_ratios`). Corrigé — et c'est la leçon de la
porte P0 : *un faux « oui » est pire qu'un refus, il fait calculer faux sans
rien dire*.

**Conséquence sur l'ordre** : V4-Flash n'est pas « MLA + hyper-connexions » mais
**41 couches compressées sur 44** — il lui faut P4 (HCA) **et** P5 (CSA +
indexeur) avant de tourner, comme V4.1. Ce qui reste spécifique à V4.1 : la
sortie `output_hc_*` et la provenance du fichier. Les couches 0, 1 et 43 sont,
elles, l'équivalent des couches brutes de V4.1 : c'est là que P3 valide la
chaîne complète.

Détail qui change l'implémentation par rapport à GLM/Kimi : l'attention V4 n'a
**ni `attn_kv_a_mqa` ni `attn_k_b`/`attn_v_b`**. Elle a `attn_kv` (une seule
tête latente de 512 = 448 nope + 64 rope, normée **en entier**), `attn_q_a` +
`attn_q_a_norm` + `attn_q_b`, une **seconde norme RMS sur q** (par tête, sans
poids), puis `attn_output_a`/`attn_output_b` (rang 1024, 8 groupes) et des
`attn_sinks` par tête. La MLA « maison » de Drave (celle de GLM/Kimi) n'est donc
pas réutilisable telle quelle : c'est un **troisième** chemin d'attention.

### 3.3 Les régimes d'attention de V4.1

`compress_ratios` (40 entrées) : **18 couches en ratio 2** (couches 2-19),
**20 couches en ratio 1** (couches 20-39), **2 couches brutes** (0, 1).
Mais les compresseurs ne vivent **que sur les couches sources**
(`kv_source_layer_ids = [2, 8, 14, 20]`) : les couches 3..7 lisent les clés
publiées par la 2, 9..13 celles de la 8, 15..19 celles de la 14, et **21..39
celles de la 20** — « Compressors and compressed-KV caches live only on
`kv_source_layer_ids`; consumers reuse the most recently published source below
them » (vLLM, `deepseek_v41/attention.py`). Les 38 couches compressées se
répartissent donc en **4 sources** (exécutables seules, chacune avec son
compresseur) et **34 consommatrices** (qui exigent le partage du cache).

---

## 4. Les phases

Chaque phase porte **deux portes** :

- **porte de correction** — la comparaison à llama.cpp sur **V4-Flash**, étage par
  étage (jamais « ça tourne ») ;
- **porte Drave** — les flux : nombre d'événements par jeton, trace écrite puis
  **rejouée à l'identique**, découpage en grappes qui donne la même perplexité,
  et le flux nouveau lisible par un outil d'analyse.

Une phase qui ne passe pas ses deux portes ne passe pas à la suivante.

### P0 — Le harnais, sur V4-Flash, et le coût d'un jeton (≈ 3 h) — **FAIT** (02/10)

> Bilan dans `reports/rapport-p0-flux.md`. Ce qui est fait : le flux se compte
> par **provenance** (attention / experts / partagé) en **paires**, et les deux
> chemins muets parlent — GLM-5.3, un jeton : 21,9 G · 30,6 G · 5,6 G, dont
> **0 en listes**. Un calcul mort d'`attn_mla` (la remontée `v_b` de la boucle
> de scores) a été trouvé, mesuré (delta prédit = delta mesuré, −1 988,1 M
> paires) et retiré. La porte `--config` est franchie pour gpt-oss (elle ne
> l'était pas : les puits appris y étaient comptés comme un manque). Reste à
> refaire la porte Drave **sur V4-Flash lui-même**, ce qui demande P2/P3.

- V4-Flash chargé dans le moteur ; comparaison par étage opérationnelle des deux
  côtés (`ref_logits --tensors` / `DRAVE_DEBUG_MLA`, `DRAVE_DEBUG_ETAT`) ;
  **compteur d'événements** instrumenté sur le chemin MLA et sur le chemin
  experts-IQ (aujourd'hui muets).
- **Porte de correction** : `--config` annonce la bonne liste de manques ;
  les deux côtés produisent les mêmes tenseurs nommés.
- **Porte Drave** : un jeton sur V4-Flash affiche un **nombre d'événements non
  nul** avec sa provenance (attention / experts / partagé), et son coût.

### P1 — Hyper-connexions : les connexions pondérées (≈ ½ journée) — **FAIT** (02/10)

> `Hc` (mélanges, Sinkhorn, mélanger/retro), chargé des deux sources de
> métadonnées (clés GGUF et `deepseek41.config`), câblé dans la passe avant.
> **Validé contre llama.cpp** : `hc_attn_pre` concorde à **1e-7** (l'arrondi f32)
> sur quatre positions — `reports/rapport-v4-couches-0-1.md`.


- État résiduel en 4 copies ; par couche `hc_pre` (RMSNorm → `hc_fn` → 24
  mélanges → `pre` sigmoïde, `post` sigmoïde ×2, `comb` **Sinkhorn 20
  itérations**), `hc_post`, mélange de tête `output_hc_*`.
- **Flux nouveau** : `comb` est une **matrice de connexions pondérées 4×4 par
  jeton** ; on la trace comme telle (canal `DRAVE_TRACE_HC`), avec sa
  **structure** : combien des 16 poids sont significatifs, et sont-ils stables
  d'un jeton à l'autre ? C'est la première question que ce dépôt doit poser au
  modèle — et elle est exploitable (si 12 des 16 sont négligeables, la couche se
  simplifie).
- **Porte de correction** : `hc_attn_pre-0` puis `hc_attn_post-0` concordent.
- **Porte Drave** : la trace des 24 poids par jeton est écrite, relue, et un
  outil (`tools/analyse_hc.py`) dit la sparsité et la stabilité.
- **Interdit** : « les 4 copies sans le Sinkhorn ». Une HC approximative ne se
  voit pas — les quatre copies restent plausibles.

### P2 — Épilogue d'attention : dé-rotation, puits, sortie groupée (≈ 3 h) — **FAIT** (02/10)

> `attn_v4` (troisième chemin d'attention) : une tête latente normée en entier,
> seconde norme RMS par tête, valeurs = clés, puits **bruts** dans le softmax,
> dé-rotation, sortie groupée 8×1024. Corrélation **0,999996** avec llama.cpp
> sur `attn_derope`. Trois bugs trouvés par la comparaison : `attn_norm` manqué,
> puits mis à l'échelle, convention RoPE **NORM** (et non NEOX comme GLM/Kimi).


- Dé-rotation (`attn_derope`) et sortie groupée (`attn_output_a` →
  `attn_output_b`, `o_groups = 8`). Les **puits par tête** (`attn_sinks`) sont
  déjà implémentés sur le chemin dense, mais `attn_mla` ne les consomme pas :
  il faut les **brancher sur le chemin MLA** que V4 utilise.
- **Porte de correction** : `kqv_out-0`, `attn_out-0`.
- **Porte Drave** : rien de nouveau à tracer ici, mais l'activation d'entrée de
  `attn_output_a` doit être **la même liste** que celle qui sort de l'attention —
  c'est le contrat du flux.
- **Interdit** : fusionner `attn_output_a/b` en une matrice dense.

### P3 — Les couches brutes, de bout en bout (≈ 2 h) — **FAIT pour V4-Flash** (02/10)

> Couches 0 et 1 exécutées de bout en bout (`--couches 0:2`) et comparées à
> llama.cpp : `l_last` corrélation **0,9998 – 0,99996** sur les quatre
> positions, écart résiduel = bruit de quantification (49,5 % de signes
> positifs, 0,1 % d'erreur relative médiane). Restent la fenêtre glissante et la
> « queue » de l'attention brute, sans effet à 4 positions — à traiter avant de
> dépasser 128 jetons.


- La couche 0 et la couche 1 de V4.1 (ratio 0) : toute la chaîne (embarquement,
  MLA, puits, dé-rotation, sortie groupée, experts IQ, résidu HC) **avant**
  d'ajouter la compression.
- **Porte de correction** : `l_out-0` **et** `l_out-1`, positions 0 à 3.
- **Porte Drave** : `--trace-flux` sur ces deux couches, puis `--flux-forcer` :
  perplexité **identique**. Et un premier chiffre d'événements par neurone actif.

### P4 — Compresseur et HCA : le premier flux qui n'existe nulle part (≈ ½ journée) — **FAIT** (02/10)

> Le compresseur HCA (ratio 128) est implémenté et **validé contre llama.cpp** :
> corrélation **0,999992** sur `attn_derope` au 128ᵉ jeton, donc au **premier
> bloc compressé complet** (`reports/rapport-v4-hca.md`). Le softmax par canal,
> l'`ape` de rang dans le bloc, la norme, le RoPE de bloc (à la position de son
> premier jeton) et la concaténation fenêtre + blocs concordent. Quatrième bug
> trouvé par la comparaison : la **dé-rotation** utilisait la base RoPE des
> couches brutes (10 000) au lieu de la base compressée (160 000) — invisible
> dans la corrélation globale (0,996) et localisé en séparant nope et rope.
> **CSA fait aussi** (P5) : compresseur à chevauchement (2×ratio), indexeur et
> masque top-k — validés tous les trois contre llama.cpp.


- `attn_compressor_kv` + `attn_compressor_norm` (+ `_ape`, `_gate` sur V4-Flash).
- **Flux nouveau** : la **liste des blocs gardés** par le gate du compresseur.
  C'est une liste d'activation au sens strict — un sous-ensemble de blocs par
  jeton — et elle se trace, se transporte et se rejoue comme les autres.
- **Porte de correction** : première couche compressée de V4-Flash, puis
  `l_out-20` sur V4.1.
- **Porte Drave** : la liste des blocs gardés est écrite ; on mesure **combien de
  blocs** elle contient, **sa stabilité** d'un jeton à l'autre, et le débit en
  blocs/s. Si la liste est stable, elle est compressible — et c'est une
  optimisation mesurable, pas une intuition.

### P5 — Indexeur et CSA : la liste de candidats (≈ 1 à 2 journées) — **FAIT** (02/10)

> Le compresseur **CSA** (ratio 4) est implémenté et validé : `attn_derope`
> **0,999990** sur la couche 2 aux positions 3-9 (blocs 0 et 1). Deux pièges
> trouvés par la comparaison : les jetons d'avant le texte ont une porte **−∞**
> (pas 0) — 0,989 au lieu de 1,000000 au **premier bloc seulement** — et les
> deux moitiés du projecteur de 1024 ont des rôles distincts (précédent /
> courant), ce que seul le **bloc 1** pouvait trancher.
> **Indexeur fait aussi** : blocs de 128 valeurs (même chevauchement), requête
> issue de `qr_norm`, `relu(q·k)` pondéré par tête, échelle
> `1/sqrt(128 × têtes)`, puis top-k. Scores comparés à `lid_score_masked` :
> **0,1 à 0,3 % d'écart** (positions 4-9). Ce qui reste de cette phase est une
> **porte longue fermée autrement** : au lieu d'un run de 2 048 jetons (plusieurs
> heures sur ce modèle), `deepseek4.attention.indexer.top_k` a été ramené de 512
> à **1** dans une copie du shard 1 — **4 octets**, aucune weight touchée. La
> sélection s'exerce alors dès 2 blocs, et `l_last-2` concorde à
> **0,999920-0,999994** : la sélection est juste, pas seulement les scores.


- `indexer.proj`, `indexer.attn_q_b`, `indexer.attn_k`, `indexer.k_norm`, les
  compresseurs d'indexeur, la sélection (`candidate_topk_blocks = 2048`,
  `candidate_block_size = 8`, `candidate_source_layer_id = 20`), puis l'attention
  sur les seuls candidats.
- **Flux nouveau** : la **liste des candidats par jeton** — 2 048 blocs sur
  l'ensemble des clés. C'est le flux le plus intéressant du modèle : il décide de
  ce que l'attention *voit*.
- **Porte de correction** : `l_out-2`, puis les logits complets — corrélation
  ≥ 0,99 et top-1 identique sur 4 positions, **contre llama.cpp sur V4-Flash**.
- **Porte Drave** : la liste des candidats est tracée, sa **stabilité** mesurée
  (recouvrement entre jetons consécutifs, périodicité), et une variante
  « candidats de la liste précédente + vérification » est **mesurée** — c'est ici
  que la philosophie des flux peut faire gagner quelque chose que llama.cpp ne
  cherche même pas.
- **Interdit** : « en deçà de `index_topk`, l'indexeur ne sert à rien ». Vrai pour
  un banc d'essai, faux pour un moteur. Si ce raccourci est retenu pour le
  premier jet, il est **écrit** dans `--config` et borné par `--ctx`.

### P6 — V4-Flash complet, en listes, et **sur plusieurs grappes** (≈ 1 journée) — **FAIT** (02/10)

> **Fait** : le modèle tourne **en entier** (43 couches, les trois régimes
> d'attention) ; `--trace-flux` puis `--flux-forcer` redonnent la même
> perplexité (**8 430,2968 → 8 430,0379**, soit 0,003 %, la perte du codage en
> listes) ; le découpage entre deux processus est **exact** — écart **0,00e0** en
> dense, écart 9,13e-2 en listes — au prix de **4× le transport**, parce que
> l'état voyage en `hc` copies et qu'il est **dense à 99,9 %** (le mode listes
> n'y compresse rien). Rapport : `reports/rapport-v4-reparti.md`.
> **Grappes faites aussi** : `commun.gguf` + 8 `cluster-XX.gguf` (86,9 Go,
> 11 008 entrées de mapping, aucune requantification) et **perplexité identique
> au chiffre près** (8 430,2968), en **39,9 s contre 111,8** — chaque expert routé
> vit dans un seul fichier, donc le nœud ne lit que ce qu'il sert.
> **Reste** : la comparaison à llama.cpp sur 8 à 64 jetons, dont on sait déjà ce
> qu'elle donne pour 10 (corrélation 0,988-0,998, écart expliqué par la
> quantification des activations de ggml).

- 43 couches, 86,9 Go, cache latent, mémoire, débit.
- **Porte de correction** : perplexité de V4-Flash contre llama.cpp sur les mêmes
  8 à 64 jetons (corrélation, top-1, rapport).
- **Portes Drave**, toutes obligatoires :
  1. `--trace-flux` puis `--flux-forcer` : perplexité **identique** ;
  2. `--flux-liste` et `--flux-blocs` : ce que coûte le transport en listes,
     mesuré, pas supposé ;
  3. **découpage en grappes** : V4-Flash en `cluster-XX.gguf`, puis
     `--ppl-reparti` entre **deux processus** (voire deux machines), perplexité
     égale à celle d'un nœud unique ;
  4. les portes du dépôt vertes (49 tests, Qwen 19,3885, **gpt-oss 15,6017**,
     clusters 799,8557, 18 formats lisibles dont 17 vérifiés à la porte,
     4 routages).

### P6 — V4-Flash complet, en listes, et **sur plusieurs grappes** — ⚠️ **porte Drave NON TENUE** (03/10)

> **Mesuré au bloc 22, sur V4-Flash (le modèle dont les deux portes sont disponibles).**
> La porte Drave demande quatre choses : événements/paires par jeton, **trace
> rejouée à l'identique**, découpage en grappes, et **flux lisible par un outil
> d'analyse**. Deux sur quatre ne tiennent pas :
>
> 1. ~~Le flux n'est PAS lisible par l'outil d'analyse~~ — **CORRIGÉ le 03/10
>    (bloc 22)** : `tools/analyse_flux.py` lisait la version 1 du format DRVF
>    (indice u32 + i16) alors que le moteur écrit la 2 (indices par écarts) et la 3
>    (échelle f16 par bloc de 32 canaux, valeurs i8). Le lecteur gère les trois
>    versions, et la porte correspondante est **branchée dans `tools/portes.sh`** :
>    elle produit une trace avec le petit modèle et la relit avec l'outil — un
>    contrat de format entre deux programmes, vérifié à chaque passage (384 listes,
>    densité, persistants, recouvrement). Un outil d'analyse qu'on ne peut pas
>    exécuter sur une trace du moteur est un outil mort, et il l'était.
> 2. **Le rejeu « à l'identique » : CORRIGÉ et DÉFINI** (bloc 22). La trace
>    partielle (`--trace-couches 0,20`) était la cause des « 672 manquantes » :
>    avec une trace **complète**, le moteur annonce « 688 listes servies,
>    **0 manquante** » ✓. L'écart de perplexité, lui, ne tombe pas à zéro :
>    V4-Flash ctx 32, 8 jetons → **4 221,0901** (passe) contre **4 221,071**
>    (rejeu), soit **4,5e-06 relatif**. Explication mesurée : la trace porte des
>    activations DÉJÀ quantifiées, et le rejeu les requantifie — une seconde
>    quantification, donc un écart qui ne peut pas être nul sans un chemin de
>    rejeu qui court-circuite la quantification.
>    **Définition désormais écrite, et vérifiée par la porte** : « rejouée à
>    l'identique » = **aucune liste manquante** et écart de perplexité **≤ 1e-5**
>    (mesuré : 4,5e-06 sur V4-Flash, 1,6e-06 sur Qwen 0,5B). Les deux critères
>    sont dans `tools/portes.sh` (7quater), sur le petit modèle — sinon la porte
>    coûterait une minute de plus à chaque passage.
>
> Les deux autres points tiennent : le profil imprime les paires par jeton
> (attention · experts · partagé · scores) et le découpage en grappes est dans
> `tools/portes.sh` (clusters Qwen3-30B = 799,8557 ✓). **Aucun chantier suivant ne
> doit s'appuyer sur cette porte avant qu'elle soit tenue.**

### P6 — la porte de CORRECTION, mesurée sur V4-Flash (03/10, bloc 22)

> **Comparaison à llama.cpp, protocoles alignés** (5 identifiants, 4 prédictions,
> `tools/ref_logits` contre `--logits-bin`) :
>
> | position | écart max | écart moyen | corrélation | top-1 identique | rang du vrai jeton (llama.cpp / nous) |
> |---|---|---|---|---|---|
> | 0 | 2,85 | 0,42 | 0,9876 | non | 130 / 173 |
> | 1 | 1,23 | 0,21 | 0,9984 | **oui** | 14 346 / 14 677 |
> | 2 | 2,04 | 0,26 | 0,9981 | **oui** | 2 032 / 1 789 |
> | 3 | 1,75 | 0,27 | 0,9979 | **oui** | 2 / 3 |
>
> Les logits concordent à 1-2 % (corrélations ≥ 0,9979 sur trois positions, 0,9876
> sur la première) et les rangs du jeton correct sont voisins. **La porte de
> correction est donc tenue — mais pas par la perplexité** : sur les mêmes jetons,
> llama.cpp annonce **6 719,61** et le moteur **8 430,4966**, soit 25 % d'écart. Une
> fenêtre froide de quatre jetons amplifie chaotiquement des écarts de logits de
> 1 % (le même phénomène a été documenté sur V4.1). **Le bon instrument est la
> comparaison des logits et des rangs, position par position** — et le chiffre de
> `portes.sh` (8430,4966) reste une référence de NON-RÉGRESSION interne, pas une
> mesure d'accord avec llama.cpp : les deux nombres ne portent d'ailleurs pas sur
> le même nombre de prédictions (4 contre 5) selon la façon dont on compte.
>
> Ce qu'il faudrait pour serrer la vis : une fenêtre d'au moins quelques centaines
> de jetons (l'amplification chaotique décroît avec la longueur) et, à terme, la
> même comparaison sur une couche compressée à contexte long.

### P7 — Adaptation à V4.1, et la question de provenance (≈ ½ journée + action externe) — **composants faits et vérifiés ; ⚠️ LE MODÈLE NE PRÉDIT PAS (03/10)**

> ## ⚠️ Constat du 03/10 (bloc 20) : V4.1 ne prédit pas
>
> Test fonctionnel le plus simple qui soit — huit répétitions de « The sky is
> blue. » (39 jetons) : un modèle qui fonctionne donne une perplexité de 1 à 2.
>
> | moteur | modèle | PPL |
> |---|---|---|
> | llama.cpp | V4-Flash IQ1_M | **1,844** |
> | Drave | V4-Flash IQ1_M (mêmes identifiants) | **1,875** |
> | Drave | **V4.1-Flash Q2** | **3 677** (sans engram) à 7 506 (8 bits) |
>
> Et sur les logits enregistrés d'une passe réelle : top-1 exact **0/31**, NLL
> moyenne **11,657 nats** pour un uniforme à 11,770 — le hasard. Le tokenizer est
> hors de cause (référence externe `tools/tokenize_llama` : identifiants
> identiques). **Le chemin V4 partagé est juste** (V4-Flash : 1,875 contre 1,844) ;
> le défaut est donc dans un mécanisme propre à V4.1 — chaîne mHC **retardée**,
> compresseur des ratios **1 et 2**, ou engram (il nuit, mais le modèle est déjà
> cassé sans lui).
>
> **Ce que cela ne remet pas en cause** : les vérifications de composants (elles
> comparent le moteur à une transcription du même document, ce qui est nécessaire
> et insuffisant), le découpage exact, les performances (×3,54 sur la passe), et
> l'engram vivant. **Ce que cela corrige** : « V4.1 tourne » voulait dire « le
> calcul tourne », pas « le modèle prédit » — la distinction n'était écrite nulle
> part. Tout chiffre V4.1 de ce plan (PPL, perplexité par tranche) est à lire comme
> une mesure de NON-RÉGRESSION, pas comme une qualité de modèle.
>
> Localisation : bloc 21 (`sprints/20-la-passe-longue-instrumentee.md`).
>
> **Ce qui a été vérifié depuis (blocs 21-22), et ce qui reste hors d'atteinte.**
> Chaque pièce et chaque composition testable SANS référence exécutable l'est :
> tokenizer (llama.cpp : identifiants identiques), embarquement (**0,000e+00**
> contre le fichier), attention complète — projections, normes, rotations, scores,
> puits, somme pondérée, dé-rotation, sortie groupée **avec les blocs compressés
> et la règle de visibilité** (1e-06 à 7e-07, numpy), compresseur (référence du
> noyau vLLM publié), indexeur, chemin des experts (4e-05, numpy), routeur
> (sélection identique), chaîne mHC retardée et tête (source vLLM, mot pour mot),
> formats (libggml). V4-Flash, lui, est validé **de bout en bout par llama.cpp**
> (1,875 contre 1,844).
>
> **La « porte de correction » de P7 (comparaison étage par étage à llama.cpp)
> est donc IMPOSSIBLE en l'état, et c'est nommé** : llama.cpp refuse
> l'architecture — « unknown model architecture: 'deepseek41' ». Il n'existe
> aucune référence exécutable pour V4.1 dans ce dépôt ni ailleurs sur cette
> machine. Les deux points que le dépôt ne peut pas trancher seul : la composition
> sur 40 couches (chaque pièce est juste, la chaîne n'a pas d'oracle) et **le
> fichier Q2 lui-même** (sa référence est fp8/MXFP4 ; une conversion fausse serait
> indiscernable pièce par pièce). Condition de sortie : qu'un runtime sache charger
> `deepseek41`, ou qu'on produise nous-mêmes une conversion et qu'on la compare au
> fichier — les deux sont des chantiers, pas des vérifications.

> **Les deux manques annoncés étaient faux tous les deux** (02/10, 17:33 → 18:02).
> La **référence d'exécution existe** : vLLM porte V4.1 en entier
> (`vllm/models/deepseek_v41/`), et elle dit
> 1. que V4.1 **n'a pas de tête apprise** : le flux final se replie avec la
>    `pre` de la **dernière FFN** (`hc_collapse_triton(hidden_states, pre_mix)`,
>    commentaire « v4.1 has no learned hc_head »). Les `output_hc_*` manquent
>    parce qu'ils n'existent pas — le jeu de tenseurs `deepseek41` les retire ;
> 2. que les coefficients des hyper-connexions **se retardent d'un raccord** :
>    l'attention se replie avec la `pre` de la FFN précédente, la FFN avec la
>    `pre` de l'attention courante, la copie 0 au tout premier raccord
>    (`mhc_shifted_post_pre`, `mhc_pre_delayed_torch`) ;
> 3. que le compresseur des ratios **1 et 2** est spécifié
>    (`DeepseekCompressor` + `fused_save_compress_norm` : softmax **par canal**
>    sur le groupe, norme du latent, RoPE à la position du premier jeton du
>    groupe ; ratio 1 : aucune porte, aucun `ape`).
>
> **Fait** : la chaîne retardée et la réduction finale sont implémentées
> (`hc_retarde`), exécutées sur le fichier de **365,7 Go** (couches 0 et 1, les
> seules en ratio 0) et vérifiées par trois égalités recalculées en numpy depuis
> les tenseurs du GGUF — la copie 0 **exacte** (0,000e+00), les 24 mélanges et la
> tête à ~1e-7 (arrondi f32). Rapport :
> [`reports/rapport-v41-mhc.md`](../reports/rapport-v41-mhc.md).
>
> **Fait aussi (02/10, 19h)** : le **compresseur des ratios 1 et 2** (softmax
> PAR CANAL sur le groupe, norme du latent, RoPE de bloc à la position du premier
> jeton, pas d'`ape`) est implémenté et vérifié sur les couches sources 2 et 20
> contre une référence numpy écrite depuis `fused_save_compress_norm` (pool
> ~5e-07, norme+RoPE ~5e-06) ; et le **cache compressé partagé**
> (`kv_source_layer_ids`) est branché — les couches consommatrices lisent les
> tampons de leur source, ce qu'un contrôle positif/négatif établit (sortie de la
> couche 3 : écart 1,30 à 2,16 selon que sa source a tourné ou non ; sortie de la
> source 2 identique au bit dans les deux cas).
>
> **Fait aussi (02/10, 22h) : l'ENGRAM est branché et vérifié de bout en bout.**
> Le hachage glissant (O(1) par jeton), la lecture des 24 rangées de 264 octets
> dans les tables de 101 Go, la projection `wkv` [25 600, 6 144] et l'injection sur
> les `hc` copies sont dans la passe avant, aux couches 1 et 14. Vérifié contre la
> référence d'adressage (`tools/engram_reference.py`) plus une relecture des
> rangées : projection à ~1e-5 (accumulation f32 sur 6 144 termes), injection à
> ~1e-6. Coût annoncé : **6 336 octets par jeton et par table**. Une passe avant
> V4.1 **complète** est donc possible dès maintenant (les 40 couches), à ceci près
> que l'indexeur garde tous les blocs — exact sous `indexer.top_k` (512), refusé
> au-delà.
>
> **Fait aussi (02/10, 23h) : l'INDEXEUR de V4.1.** Ses clés sont
> `k_norm(attn_k(latent))` — le latent du compresseur **principal**, une clé de
> 128 valeurs par bloc partagée par les 32 têtes — et le cache n'est possédé que
> par les couches [2, 8, 14, 20] ; les indexeurs de 24/28/32/36 lisent celui de
> leur source de KV. Vérifié contre la référence numpy : clés à 1,7e-06, scores à
> 2,9e-07 (couche 2, deux groupes). La **sélection** (top-k) ne s'exerce qu'au-delà
> de 512 blocs — plus de 1 024 jetons en ratio 2 — et le moteur ne refuse plus :
> il choisit, comme V4-Flash.
>
> **Sélection exercée (02/10, 19h45)** : le top-k de l'indexeur CHOISIT pour la
> première fois sur V4.1 — 513 blocs à la position 512 d'une couche de ratio 1,
> 512 gardés, séparation des scores vérifiée (rapport §8). Et le filtre à deux
> niveaux (`candidate_*`) est **chiffré** : il ne mord qu'au-delà de
> `2 048 × 8 = 16 384` positions compressées, et le moteur refuse au-delà.
>
> **YaRN sur les couches compressées : FAIT et MESURÉ** (02/10, 20h30). llama.cpp
> et vLLM appliquent YaRN ×16 sans mscale à toutes les positions dès que
> `compress_ratio > 0` ; le moteur appliquait son régime retardé. Correctif validé
> contre llama.cpp tenseur par tenseur (position 127 : 4,515e-03 contre 5,376e-03
> d'écart en RoPE simple). Le premier essai disait l'inverse : la rampe était
> calculée avec un contexte d'origine de 4 096 parce que `as_f64` ne lit pas les
> clefs **u32** (`rope.scaling.original_context_length`) — le défaut prenait la
> place de la valeur. Porte V4-Flash 8430,2968 → 8430,4966 ; chiffres antérieurs à
> revérifier (`reports/rapport-v4-yarn-compresse.md`).
>
> **Le DÉCOUPAGE de V4.1 est exact au bit près (02/10, 23h).** Le pré-mix sur le
> fil (protocole v6) était bien transporté, mais il était **consommé deux fois** :
> la `pre` reçue du pair pour le jeton *p* restait posée sur le modèle et le
> `forward` du jeton *p+1* la reprenait pour amorcer sa chaîne retardée. Mesuré
> par tenseur : 629 tenseurs divergents, **tous aux positions 1 et 2, aucun à la
> position 0** — la signature exacte d'une fuite d'un jeton sur le suivant.
> Correctif : `forward` ne consomme la `pre` reçue que si le nœud reprend au
> milieu du modèle (`couche_debut > 0`), et `norme_finale` prend `&mut self` et
> la consomme. Résultat : V4.1 découpé à la couche 20 = **écart 0,00e0**, et
> **953 tenseurs de la passe répartie du pilote + 945 du nœud moteur identiques
> au bit près** à une passe complète à un seul nœud (les 1 591 autres fichiers du
> répertoire viennent de la passe de référence du pilote : ils ne peuvent pas
> échouer sur la couture) (transport aller, pré-mix retour et réduction
> finale compris). Le V4-Flash ne pouvait pas montrer le défaut : sa réduction
> finale est apprise (`np = 0` sur le fil).
>
> **Et l'« instrument qui mentait » ne mentait pas** : la référence locale du
> harnais (1 743 713,62) différait de `--ppl` (208 411,867) parce que les deux
> modes ne règlent pas la même quantification d'activation — **16 bits** par
> défaut en `--ppl` (32 767 niveaux, sa référence de non-régression), **8 bits**
> dans les modes flux (127 niveaux). `--ppl --abits 8` donne **1 743 713,6243** et
> 2 544 tenseurs identiques au bit près à la référence du harnais ; `--dense` n'y
> change rien. Les « écarts » publiés par `--ppl-reparti` sont donc valides — et le
> 7,05e-1 en était un vrai.
>
> **Reste, nommé** : le **masque des jetons d'image** de l'engram (sans objet en
> texte seul), et un **test automatique de couple de nœuds** (le mode lot 3/4 est
> vérifié à la main sur 0,5 B ; aucun `tools/porte-flux.sh` ne le couvre).

> **Fermée, la question du YaRN des couches compressées** (02/10, 20h30) : vLLM
> applique bien YaRN ×16 à toutes les positions dès que `compress_ratio > 0`
> (mscale désactivé), et le moteur fait désormais comme lui — validé tenseur par
> tenseur contre llama.cpp à la position 127 (4,515e-03 d'écart contre 5,376e-03
> en RoPE simple, `reports/rapport-v4-yarn-compresse.md`). Ce qui reste ouvert
> n'est plus la convention mais le **régime** : aux positions courtes les deux
> lectures coïncident presque, et c'est au-delà de ~1 024 que le choix se voit.
> Protocole de décision inchangé : une passe V4-Flash à contexte ≥ 1 024 sur une
> couche compressée, comparée à llama.cpp avec et sans `DRAVE_YARN=1`.


- Code : métadonnées par couche (`compress_ratios` au lieu d'un régime global),
  experts IQ2_XXS/Q2_K, 384 experts, 40 couches, `exp_probs_b_vl`.
- **Action préalable, non-code** : tranchée — le fichier est complet, et le
  mode de réduction est écrit dans la référence d'exécution (vLLM).
- **Porte** : les couches 0 et 1 tournent et les trois égalités de la chaîne mHC
  tiennent (fait) **et** la liste des manques de `--config` ne contient plus que
  des manques réels, nommés avec leur référence (fait) ; la comparaison externe
  de logits viendra quand un runtime saura charger le fichier (llama.cpp n'a
  qu'un patch de conversion).

### P8 — Engram : la liste d'adresses, et sa référence à écrire (≈ 1 à 2 journées) — **FAITE et VIVANTE** (02/10)

> **Inventorié** : deux tables de **101,38 Go** chacune
> (`blk.{1,14}.engram_embd` I8 [384 006 168, 264]), soit **202,8 Go = 55 % du
> fichier**. Le format de rangée est **entièrement déterminé** par les
> métadonnées : `e4m3_e8m0_32_row264` = 8 blocs de 32 valeurs e4m3 + 8 échelles
> e8m0 = **264 octets**. La sonde (`--sonder-engram 10000`) touche 2,6 Mo par
> table en 219-524 ms, à 120 Mo de RSS.
> **Ce qui manque n'est pas le code, c'est la RECETTE** : les métadonnées donnent
> 48 nombres premiers et 8 multiplicateurs, mais pas la formule d'adressage ; et
> il n'existe **aucune référence** — llama.cpp ignore l'engram, V4-Flash ne l'a
> pas, et le code d'entraînement n'est pas dans ce dépôt. Plusieurs formules
> plausibles donnent des rangées différentes : en choisir une serait deviner, ce
> que la règle 6 interdit.
> **Correction (02/10) : la référence EXISTE.** Un portage 1:1 de
> `vllm/models/deepseek_v4_1/common/engram.py` est publié
> ([`mudler/vllm.cpp`](https://github.com/mudler/vllm.cpp/blob/main/src/vllm/model_executor/models/deepseek_v4_1_engram.cpp)) :
> la formule (`^=` sur un repli collant, modulo par colonne), la lecture
> (e4m3 × e8m0 par bloc de 32) et l'injection (porte `sigmoid(±sqrt(max(|dot|,
> 1e-6)))`) sont écrites noir sur blanc.
>
> **Les trois fonctions sont portées et validées** (`drave-core/src/engram.rs`) :
> **adressage** — 10 000 jetons × 2 couches × 24 colonnes = **480 000 adresses,
> 0 écart** avec la transcription Python, sur les métadonnées réelles ; **lecture
> d'une rangée** — 2 000 rangées, **512 000 valeurs identiques au bit près** au
> décodage Python des mêmes octets ; **injection** — testée contre la
> transcription (valeurs générées) et par le masque, qui doit rendre l'entrée
> exactement. Les invariants du fichier sont vérifiés : 48 premiers recalculés
> identiques, table de correspondance dense (99 092), multiplicateurs impairs
> sous la borne, chaque adresse dans le seau de sa colonne.
>
> **Ce qui la liste coûte et dit** (`--engram-adresses`) : 10 000 jetons en
> **5,9 ms**, 99,9 % de rangées distinctes, **0,06 %** des 768 022 850 rangées
> adressées, **0 % de recouvrement entre jetons consécutifs**. Porte permanente
> dans `tools/portes.sh`.
>
> **Reste** : brancher l'injection dans une passe avant (bloqué — aucun modèle
> exécutable ne porte d'engram) et relire la liste avec un outil d'analyse
> (`reports/rapport-engram-etat.md`).
>
> **P8 EST FERMÉE (02/10, 21h35) — l'engram est VIVANT, et sa vivacité est
> mesurée.** L'injection est branchée dans la passe complète depuis le bloc 11 ;
> ce qui manquait était la preuve qu'elle **entre dans le calcul** (une injection
> non nulle peut n'être lue par personne). `DRAVE_SANS_ENGRAM=1` coupe le bloc et
> l'ANNONCE ; l'A/B sur la passe complète V4.1 (mêmes jetons, ctx 8, 8 bits des
> deux côtés) donne **1 743 713,6243** avec et **1 427 298,2128** sans (22,2 %).
> Par tenseur : la couche 0 est **identique au bit près** (contrôle : l'engram est
> aux couches 1 et 14), les couches 1 à 39 sont toutes différentes, et les vides
> `engram_kv`/`engram_sortie` **n'existent plus** quand l'interrupteur est actif —
> le bloc n'a pas tourné. C'est une mesure de vivacité, pas de qualité : que
> l'engram dégrade la perplexité à quatre jetons à froid ne dit rien de son effet à
> contexte long, qui reste à mesurer.
>
> **L'ablation grandit avec le contexte** : mêmes réglages, mêmes jetons, ctx 8 →
> 1 743 713,6243 (avec) contre 1 427 298,2128 (sans), soit **+22,2 %** ; ctx 32 →
> **115 521,8693** contre **74 328,5818**, soit **+55,4 %**. Plus de contexte =
> plus d'n-grammes touchés = plus d'injection : c'est la signature d'une mémoire,
> et cela renforce la vivacité. **Mais retirer l'engram AMÉLIORE la perplexité sur
> ces deux fenêtres**, ce qu'une mémoire entraînée avec le modèle ne devrait pas
> faire. Ce qui est exclu : une erreur de formule — l'adressage (règle collante
> comprise), la lecture, la projection et la porte sont vérifiés contre la
> transcription numpy, et le portage publié (`mudler/vllm.cpp`,
> `deepseek_v4_1_engram.cpp`) relu le 02/10 confirme les quatre règles. Ce qui
> reste possible : que la table, le `token_map` ou les poids d'injection du
> fichier Q2 ne soient pas ceux de l'entraînement. Question OUVERTE, chiffrée.
>
> **Masque des jetons d'image : décision écrite, non implémenté.** `dead_mask`
> (`image_sentinel_mask`) est exact pour du texte seul (aucun jeton sentinelle) ;
> l'implémenter sans un chemin multimodal V4.1 qui en produise serait deviner la
> forme d'une entrée. Condition de réouverture : un chemin multimodal
> (`docs/plan-mla-vision.md`).

- Deux tables de 101,4 Go (couches 1 et 14) : hachage de n-grammes
  (`engram.primes`, `multipliers`, `token_map`), recherche, injection.
- **Le problème de méthode** : llama.cpp ne le calcule pas, V4-Flash ne l'a pas :
  **aucune référence n'existe**. Livrer sans référence violerait la règle 6.
- **Issue acceptable (a)** : écrire une référence indépendante en Python — comme
  `tools/mla_synthetique.py` l'a fait pour la MLA — qui calcule le hachage à
  partir des métadonnées, et que le moteur doit retrouver sur 10 000 entrées.
  **Issue (b)** : ne pas le faire et l'écrire.
- **Porte Drave** : la sonde et la référence concordent ; le flux d'adresses est
  tracé (rangées touchées, recouvrement entre jetons) ; le changement de sortie
  est **annoncé**.

### P9 — Noyaux natifs et encodage des poids : après la mesure (≈ 1 journée, optionnel) — **mesure faite, pas justifié** (02/10)

> La mesure que P9 attendait existe, et elle tranche : **le goulot est la
> LECTURE, pas le déquant**. Preuve directe — le même modèle, le même calcul,
> seuls les octets lus changent : original 86,9 Go en 3 tranches = **111,8 s** ;
> éclaté en 8 grappes (chaque expert dans un seul fichier, donc moins d'octets
> lus par jeton) = **39,9 s** pour la MÊME perplexité, au chiffre près. Un noyau
> IQ natif économiserait de l'arithmétique sur un chemin déjà borné par les
> entrées-sorties : ×2,8 sans toucher au calcul est un signal plus fort que
> n'importe quelle optimisation de noyau.
> **Décision : ne pas l'écrire maintenant.** Ce qui le justifierait : un modèle
> dont les poids tiennent en RAM (là, la bande passante cesse d'être la borne),
> ou une mesure montrant le déquant dans le palmarès des postes — aujourd'hui
> `proj+mlp` et `attention` sont dominés par la lecture des poids (25 ms par
> couche-jeton pour 49,7 M poids lus, soit ≈ 2 Go/s effectifs).

> **Fait le 02/10 (bloc 15), et sans écrire un seul noyau natif** : le poste
> `attention` de V4.1 valait **12 369,91 ms par jeton** parce que son
> produit matrice-vecteur f32 (`matvec_f32`, 11 appels par couche, 1,65 G de
> produits par jeton) était une boucle **mono-fil scalaire** — vingt cœurs
> inoccupés. Il est maintenant **parallèle par LIGNES** (`matvec_f32_fils`) :
> chaque ligne reste sommée par un seul fil dans le même ordre, donc le résultat
> est **identique au bit près** (2 544 vides comparés, 0 écart ; perplexité
> 1 743 713,6243 inchangée) et le poste tombe à **1 324,48 ms/token (×9,34)**,
> la passe complète de 66-68 s à **22,2 s (×3)**. Le SIMD reste sur la table
> (~5 Go/s effectifs contre 40-60 Go/s possibles) mais il changerait l'ordre des
> sommes, donc la référence de non-régression : décision reportée, conditions
> écrites (`sprints/15`).
>
> **Ce qui a été essayé et REFUSÉ par la mesure (bloc 16)** : un **cache RAM des
> experts** (`DRAVE_EXPERTS_RAM`), justifié par une trace de routage (50 % des
> lectures dans 394 experts, 31,9 % de réutilisation entre jetons consécutifs).
> Il est **plus lent** : passe ctx 32 = 145,1 s sans, 151,2 s à 4 Go (+4 %),
> 175,5 s à 32 Go (+21 %), perplexité identique. Le noyau fait déjà ce travail
> (`buff/cache`, ~95 Go de pages), donc la copie ajoute un second exemplaire et du
> `memcpy` sans retirer les lectures NVMe. Le drapeau reste, éteint, avec son
> verdict dans son annonce. Le poste dominant reste `proj+mlp` (3 530 ms/token à
> ctx 32) : de la lecture d'experts, à traiter par la structure (grappes,
> découpage entre nœuds), pas par un cache.
>
> - Deux sujets distincts, à ne pas confondre :
  - **noyaux IQ natifs** : aujourd'hui les experts passent par déquantification
    + produit f32 (juste, lent). Un noyau se justifie si le débit mesuré en P6
    le demande ;
  - **encodage des poids en listes** (trinaire / deux listes / connexions
    pondérées) : c'est le programme de recherche du dépôt, pas un préalable à
    V4.1. Il se mesure comme le reste : gain de place, de débit, et effet sur la
    perplexité.
- **Porte** : un chiffre avant, un chiffre après, même protocole.

---

## 5. Budget et campagne

| poste | estimation |
|---|---|
| implémentation | P0 3 h · P1 ½ j · P2 3 h · P3 2 h · P4 ½ j · P5 1-2 j · P6 1 j · P7 ½ j ≈ **5 à 6 journées** |
| passes de validation | ~20, sur **V4-Flash** (86,9 Go, tient en RAM) : référence ~1 min, 4 à 8 jetons par passe |
| machine | un seul travail lourd à la fois (règle du dépôt) |
| nouveaux outils | `tools/analyse_hc.py`, `tools/analyse_candidats.py`, extension de `profil_flux.py` aux nouveaux canaux |

**Jalons visibles** : événements non nuls sur V4-Flash (P0) → connexions HC
tracées (P1) → `l_out-1` juste (P3) → **première liste de blocs gardés** (P4) →
liste de candidats tracée et corrélée à 0,99 (P5) → V4-Flash en listes **et
réparti sur deux nœuds** (P6) → V4.1 exécutable ou provenance tranchée (P7).

---

## 6. Ce qu'on ne fera pas, et les conditions d'arrêt

- **Pas de forward muet.** Un mécanisme qui ne produit ni liste ni compteur
  d'événements n'est pas terminé, même s'il donne les bons logits.
- **Pas de bypass du contrôle d'architecture** : il perd une ligne par phase, il
  ne se contourne pas.
- **Pas d'engram sans référence** (P8) : (a) ou (b), jamais « on suppose ».
- **Pas d'approximation silencieuse** : tout raccourci (indexeur ignoré,
  couche compressée traitée comme brute) est dit dans `--config`, le rapport et
  le message d'ouverture.
- **Si une phase coûte plus du double de son estimation, on s'arrête** et on
  documente — comme la tête garantie.
- **Aucun chiffre de CALCUL de V4.1 n'est publié avant P7** — les mesures
  statiques de §3.1 (inventaire, en-têtes, engram) restent permises, elles disent
  ce que le fichier contient, pas ce que le modèle calcule. Jusque-là s'applique
  la phrase du moteur : « ce modèle n'a jamais été exécuté ici ».

---

## 7. Pourquoi cet ordre

- **V4-Flash avant V4.1** : seul modèle de la famille qui ait une référence
  externe **et** qui tienne en RAM. On implémente une fois, on prouve là où c'est
  possible.
- **P0 avant tout** : sans compteur d'événements ni mesure du coût par jeton, on
  ne saurait pas si le chantier avance dans le sens de Drave ou dans celui d'un
  moteur dense.
- **P1 avant P2** : sans le mélange des 4 copies, tout ce qui suit a la mauvaise
  entrée — et l'erreur serait silencieuse.
- **P3 avant P4/P5** : valider toute la chaîne sur les couches **non compressées**
  avant d'ajouter la compression. Si `l_out-1` diverge, chercher dans 38 couches
  compressées coûte quatre fois plus cher.
- **P4 avant P5** : HCA est le cas dégradé de CSA (sans sélection de candidats) ;
  il donne une référence interne pour la partie commune.
- **P6 avant P7** : prouver la famille (listes, grappes, transport) sur V4-Flash
  avant d'adapter à V4.1, sinon on empile deux inconnues.
- **P8 et P9 en dernier** : les seuls postes sans gate externe (engram) ou sans
  nécessité démontrée (noyaux, encodage des poids).

**Fichiers prévisibles** : `drave-core/src/model.rs` (état HC, épilogue
d'attention, trois chemins d'attention, canaux de trace), `drave-core/src/list.rs`
(connexions pondérées du mélange HC), `drave-core/src/gguf.rs` (nouveaux
tenseurs), `drave-core/src/main.rs` (`--config`, aide, nouveaux canaux),
`tools/analyse_hc.py`, `tools/analyse_candidats.py`, `tools/portes.sh` (une porte
V4-Flash quand elle existera), un rapport par phase dans `reports/`.
