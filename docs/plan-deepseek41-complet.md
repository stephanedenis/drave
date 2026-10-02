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

`compress_ratios` (40 entrées) : **18 couches CSA** (ratio 2, couches 2-19),
**20 couches HCA** (ratio 1, couches 20-39), **2 couches brutes** (0, 1).
**38 des 40 couches** passent par une attention compressée : il n'y a pas de
validation « partielle » possible.

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

### P1 — Hyper-connexions : les connexions pondérées (≈ ½ journée)

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

### P2 — Épilogue d'attention : dé-rotation, puits, sortie groupée (≈ 3 h)

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

### P3 — Les couches brutes, de bout en bout (≈ 2 h)

- La couche 0 et la couche 1 de V4.1 (ratio 0) : toute la chaîne (embarquement,
  MLA, puits, dé-rotation, sortie groupée, experts IQ, résidu HC) **avant**
  d'ajouter la compression.
- **Porte de correction** : `l_out-0` **et** `l_out-1`, positions 0 à 3.
- **Porte Drave** : `--trace-flux` sur ces deux couches, puis `--flux-forcer` :
  perplexité **identique**. Et un premier chiffre d'événements par neurone actif.

### P4 — Compresseur et HCA : le premier flux qui n'existe nulle part (≈ ½ journée) — **HCA FAIT** (02/10)

> Le compresseur HCA (ratio 128) est implémenté et **validé contre llama.cpp** :
> corrélation **0,999992** sur `attn_derope` au 128ᵉ jeton, donc au **premier
> bloc compressé complet** (`reports/rapport-v4-hca.md`). Le softmax par canal,
> l'`ape` de rang dans le bloc, la norme, le RoPE de bloc (à la position de son
> premier jeton) et la concaténation fenêtre + blocs concordent. Quatrième bug
> trouvé par la comparaison : la **dé-rotation** utilisait la base RoPE des
> couches brutes (10 000) au lieu de la base compressée (160 000) — invisible
> dans la corrélation globale (0,996) et localisé en séparant nope et rope.
> **Reste pour P5** : le CSA (ratio 4), son compresseur à chevauchement, son
> indexeur et le masque top-k.

### P4 — Compresseur et HCA : le premier flux qui n'existe nulle part (≈ ½ journée)

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

### P5 — Indexeur et CSA : la liste de candidats (≈ 1 à 2 journées) — le gros morceau

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

### P6 — V4-Flash complet, en listes, et **sur plusieurs grappes** (≈ 1 journée)

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

### P7 — Adaptation à V4.1, et la question de provenance (≈ ½ journée + action externe)

- Code : métadonnées par couche (`compress_ratios` au lieu d'un régime global),
  experts IQ2_XXS/Q2_K, 384 experts, 40 couches, `exp_probs_b_vl`.
- **Action préalable, non-code** : établir si le GGUF V4.1-Flash-Q2 est complet.
  Les tenseurs `output_hc_fn/base/scale` manquent alors que `hc_mult = 4` est
  déclaré. Trois issues : (a) tenseurs perdus à la conversion →
  retélécharger/reconvertir ; (b) V4.1 ne les utilise pas → le prouver dans le
  graphe de référence ; (c) quantization communautaire incomplète → le dire dans
  l'inventaire des modèles lourds.
- **Porte** : la liste des manques de `--config` est vide **ou** le fichier est
  déclaré incomplet, et l'écart de perplexité V4.1 contre V4-Flash est écrit
  d'avance (seule comparaison possible, llama.cpp ne lisant pas V4.1).

### P8 — Engram : la liste d'adresses, et sa référence à écrire (≈ 1 à 2 journées)

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

### P9 — Noyaux natifs et encodage des poids : après la mesure (≈ 1 journée, optionnel)

- Deux sujets distincts, à ne pas confondre :
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
