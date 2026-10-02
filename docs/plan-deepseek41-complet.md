# Plan — compléter Drave pour exécuter DeepSeek-V4.1 (et V4-Flash), sans trahir la méthode

**État au 02/10 09h30.** Ce document est un plan : il dit ce qu'il reste à faire,
dans quel ordre, **comment on saura que c'est fait** — et **sur quel modèle on le
prouve**. Il a été écrit après trois vérifications qui changent l'ordre des
choses (§1.2, §3.2, §4) et non d'après les intentions supposées.

---

## 1. Le point de départ, mesuré

### 1.1 Ce qui marche déjà sur `DeepSeek-V4.1-Flash-Q2.gguf` (365,71 Go, NVMe)

| capacité | mesure |
|---|---|
| en-têtes + inventaire | 1 046 tenseurs, 365,70 Go lus en **63,8 ms** (mmap, aucune copie) |
| description | **74 ms** : 40 couches, 5 120 cachés, 384 experts top-6, routage **racine de softplus ×1,5**, routage **par table** des 3 premières couches |
| plan matériel | 20 threads · 16 lecteurs · cache experts 19,5 Go · KV 32 bits |
| tables d'engram | 10 000 entrées en **219–524 ms**, 2,6 Mo touchés par table, **120 Mo de RSS** pour 365,7 Go adressés |
| formats nécessaires | IQ2_XXS, Q2_K, Q8_0, F16, F32, I32 — **tous vérifiés contre libggml** |
| MLA à rang faible | implémentée, **validée contre llama.cpp** sur GLM-5.3 (corrélation 0,999024, top-1 3/3) |
| routage des experts | quatre conventions + facteur d'échelle + table `tid2eid` |

La passe avant est refusée en 0,33 s, en nommant ce qui manque. C'est le bon
comportement : rien de faux n'a été produit.

### 1.2 Trois faits vérifiés le 02/10, qui commandent le plan

1. **llama.cpp ne connaît pas `deepseek41`.** `ref_logits` sur V4.1 rend
   `unknown model architecture: 'deepseek41'`. **Il n'existe donc aucune
   référence externe pour V4.1**, ni chez nous ni chez llama.cpp.
2. **llama.cpp connaît `deepseek4` et charge V4-Flash.** Mesuré à l'instant :
   1 325 tenseurs chargés, `NLL moy = 11,737136`, `perplexité = 125133,46` sur un
   jeton froid (identifiants tokenisés par un autre modèle — le chiffre n'est pas
   un résultat, c'est une **preuve que la référence fonctionne**).
3. **V4.1-Flash-Q2 n'a pas les tenseurs de mélange de tête.** Ses seuls tenseurs
   globaux sont `output`, `output_norm`, `token_embd` ; V4-Flash a en plus
   `output_hc_fn` `[4, 20480]`, `output_hc_base` `[4]`, `output_hc_scale` `[1]`.
   Or V4.1 **déclare** `hc_mult = 4` et `hc_sinkhorn_iters = 20`. Un fichier qui
   déclare le mécanisme et ne porte pas ses tenseurs de tête est **incomplet ou
   converti à tort** — c'est une question de provenance, pas de code.

---

## 2. La méthode, rendue opérationnelle

Ces règles ne sont pas décoratives : chacune a coûté une erreur dans ce dépôt.

1. **Aucune phase n'est « finie » sans comparaison externe**, étage par étage
   (`ref_logits --tensors` d'un côté, `DRAVE_DEBUG_MLA`/`DRAVE_DEBUG_ETAT` de
   l'autre). « Ça tourne » n'est pas un résultat : le 02/10, GLM-5.3 tournait avec
   une corrélation de −0,04.
2. **Une seule implémentation de chaque chose.** Deux copies d'un même contrôle
   ont déjà divergé dans cette session (`--config` contre le refus), comme les
   deux routages (lot contre jeton seul).
3. **Rien ne change une sortie en silence** — tout mécanisme ajouté est annoncé
   par `--config`, à l'ouverture, et dans un rapport.
4. **Chaque chiffre publié a sa source** ; « absent » se dit « absent ».
5. **Le contrôle d'architecture est la liste vivante du chantier** :
   `manques_architecture` perd **une ligne par phase** franchie. Liste vide =
   exécutable. C'est la définition de « fini ».
6. **Aucun code invalidable n'est livré** : sans référence, on n'implémente pas
   (l'engram, §7).
7. **Les portes restent vertes à chaque commit** : 48 tests, Qwen **19,3885**,
   clusters **799,8557**, 17 formats contre libggml, 4 conventions de routage.
8. **Un échec se documente** : la tête garantie a été implémentée, mesurée sans
   gain, et gardée avec son rapport.

---

## 3. Ce que l'architecture exige, et sur quel modèle on le prouve

### 3.1 Les mécanismes manquants (inventaire mesuré)

| mécanisme | V4.1 (40 couches) | V4-Flash (43 couches) |
|---|---|---|
| hyper-connexions `hc_attn_*`, `hc_ffn_*` | ×40 | ×43 |
| mélange de tête `output_hc_*` | **ABSENT** | ✓ `fn` `[4, 20480]`, `base` `[4]`, `scale` `[1]` |
| MLA latente (`attn_q_a/q_b`, `attn_kv`, `_norm`) | ×40 | ×43 |
| puits par tête `attn_sinks` | ×40 | ×43 |
| sortie groupée `attn_output_a/b` (`o_groups = 8`) | ×40 | ×43 |
| compresseur `attn_compressor_*` | 4 couches (kv/norm) | **41 couches** (kv, norm, ape, gate) |
| indexeur `indexer.*` | 8 + 4 couches | **21 couches** (+ `indexer_compressor_*`) |
| routage par table `ffn_gate_tid2eid` | 3 couches | 3 couches |
| engram (`engram_embd` I8, 101,4 Go × 2) | couches 1 et 14 | **absent** |
| experts | IQ2_XXS (porte/up) + Q2_K (descente) | IQ1_M, IQ2_XXS, IQ3_XXS |

**Trois régimes d'attention dans V4.1** (`compress_ratios`, 40 entrées) :

| ratio | couches | attention |
|---|---|---|
| **2** | **18** (2 → 19) | CSA : à candidats (`candidate_topk_blocks = 2048`, `candidate_block_size = 8`) |
| **1** | **20** (20 → 39) | HCA : compressée simple |
| **0** | **2** (0, 1) | brute (MLA + puits) |

**38 des 40 couches utilisent une attention compressée.** Une exécution
« partielle » n'aurait donc aucun sens : les 2 couches brutes ne valident rien du
modèle. C'est ce qui met le compresseur et l'indexeur **sur le chemin critique**.

### 3.2 La conséquence : on construit et on prouve sur V4-Flash, puis on adapte V4.1

| | V4-Flash (`deepseek4`) | V4.1 (`deepseek41`) |
|---|---|---|
| poids | 86,9 Go — **tient en RAM** | 365,7 Go — mmap seul |
| llama.cpp | **reconnaît et exécute** ✅ | **refuse** (`unknown architecture`) |
| file complète ? | oui (tenseurs de tête présents) | **non** : `output_hc_*` absents |
| mécanismes | **les mêmes** (hc, MLA, compresseur, indexeur, table) | idem + engram |
| rôle dans le plan | **le banc d'essai et la référence** | la cible finale, après adaptation |

C'est la décision structurante du plan : **on implémente les mécanismes une fois,
et on les valide sur V4-Flash**, où une référence externe existe et où le modèle
tient en mémoire (donc où les passes de validation coûtent des minutes, pas des
heures). V4.1 devient ensuite un travail d'**adaptation** (métadonnées, quelques
noms de tenseurs, 3 couches brutes au lieu de 2, experts IQ2_XXS/Q2_K) — plus une
**question de provenance** à trancher pour ses tenseurs de tête manquants.

---

## 4. Le plan, par phases

Chaque phase : ce qu'elle change, **sa porte** (commande + résultat attendu), ce
qui est interdit. Une phase qui ne passe pas sa porte ne passe pas à la suivante.

### P0 — Harnais de comparaison, sur V4-Flash (≈ 3 h)

- Charger V4-Flash dans le moteur (`--config` doit annoncer les mêmes mécanismes
  que V4.1 moins l'engram), mesurer le coût d'un jeton, et rendre opérationnelle
  la comparaison **par étage** sur ce modèle.
- **Porte** : `--config` sur V4-Flash donne « calculable : NON » avec la liste
  attendue ; deux passes `ref_logits` (référence) + moteur sur les mêmes jetons
  produisent les mêmes tenseurs nommés ; coût par jeton écrit.
- **Interdit** : commencer par V4.1 « parce que c'est le modèle qui nous
  intéresse ». Sans référence, on ne peut rien prouver.

### P1 — Hyper-connexions (≈ ½ journée)

- État résiduel en **4 copies** `[hc][h]` ; par couche `hc_pre` (RMSNorm sur les
  4·h aplatis → `hc_fn` → 24 mélanges → `pre` sigmoïde, `post` sigmoïde ×2,
  `comb` Sinkhorn 20 itérations), `hc_post`, et le mélange de tête
  `output_hc_*` avant la norme finale.
- **Porte** : `hc_attn_pre-0` concorde avec llama.cpp (quelques pour cent, comme
  `l_out-0` sur GLM : 1,9 %), puis `hc_attn_post-0`.
- **Interdit** : « les 4 copies sans le Sinkhorn », ou sans le mélange de tête.
  Une HC approximative ne se voit pas — les quatre copies restent plausibles.

### P2 — Épilogue d'attention (≈ 3 h)

- Dé-rotation de la sortie (`attn_derope`, rotation inverse à la position
  courante), **puits** par tête (`attn_sinks`), **sortie groupée** (permutation
  par groupes → `attn_output_a` → `attn_output_b`).
- **Porte** : `kqv_out-0`, puis `attn_out-0` concordent.
- **Interdit** : fusionner `attn_output_a/b` en une matrice dense « pour
  simplifier » — c'est un changement de calcul.

### P3 — Les couches brutes, de bout en bout (≈ 2 h)

- Première étape où le modèle **calcule quelque chose de comparable** : la couche
  0 de V4.1 (ratio 0) et les couches non compressées de V4-Flash.
- **Porte** : `l_out-0` **et** `l_out-1` concordent, **aux positions 0 à 3**.
- **Interdit** : se contenter de la position 0 (elle ne teste qu'une clé).

### P4 — Compresseur et HCA (≈ ½ journée)

- `attn_compressor_kv` + `attn_compressor_norm` (+ `_ape`, `_gate` sur V4-Flash),
  puis l'attention compressée simple.
- **Porte** : la sortie de la première couche compressée de V4-Flash concorde ;
  sur V4.1, `l_out-20`.
- **Interdit** : supposer que « c'est la MLA avec un cache plus court » sans le
  vérifier tenseur par tenseur.

### P5 — Indexeur et CSA à candidats (≈ 1 à 2 journées) — le gros morceau

- `indexer.proj`, `indexer.attn_q_b`, `indexer.attn_k`, `indexer.k_norm`, les
  compresseurs d'indexeur, la sélection (`candidate_topk_blocks = 2048`,
  `candidate_block_size = 8`, `candidate_source_layer_id = 20`), puis l'attention
  sur les seuls candidats.
- **Porte** : `l_out-2` concorde ; puis **les logits complets** : corrélation
  ≥ 0,99 et top-1 identique sur 4 positions, **contre llama.cpp sur V4-Flash**.
- **Interdit** : « en deçà de `index_topk`, l'indexeur ne sert à rien » — vrai
  pour un banc d'essai, faux pour un moteur. Si ce raccourci est retenu pour le
  premier jet, il est **écrit** dans `--config` et limité par `--ctx`.

### P6 — Passe complète sur V4-Flash (≈ ½ journée)

- 43 couches, 86,9 Go, cache latent, mémoire, débit.
- **Porte** : perplexité de V4-Flash contre llama.cpp sur les **mêmes 8 à 64
  jetons** (corrélation, top-1, rapport de perplexité), **et** les portes du
  dépôt vertes. C'est la première fois que « V4 tourne » sera un résultat.

### P7 — Adaptation à V4.1, et la question de provenance (≈ ½ journée + action externe)

- Ce qui reste à faire côté code : métadonnées (`compress_ratios` par couche au
  lieu du régime global), experts IQ2_XXS/Q2_K (déjà lus), 384 experts, 40
  couches, `exp_probs_b_vl`.
- **Action préalable, non-code** : établir si le GGUF V4.1-Flash-Q2 est complet.
  Les tenseurs `output_hc_fn/base/scale` manquent alors que `hc_mult = 4` est
  déclaré. Trois issues : (a) le convertisseur les a perdus → **retélécharger ou
  reconvertir** ; (b) V4.1 ne les utilise pas → le prouver dans le graphe de
  référence, et alors le mélange de tête est inutile ; (c) le fichier est une
  quantization communautaire incomplète → le dire dans l'inventaire des modèles
  lourds.
- **Porte** : `--config` sur V4.1 ne liste plus que ce qui manque réellement, et
  la perplexité de V4.1 est comparée **à celle de V4-Flash** (pas à llama.cpp,
  qui ne le lit pas) sur les mêmes jetons, avec l'écart attendu écrit d'avance.

### P8 — Engram : à décider, jamais à improviser (≈ 1 à 2 journées)

- Deux tables de 101,4 Go (couches 1 et 14 de V4.1 uniquement) : hachage de
  n-grammes (`engram.primes`, `multipliers`, `token_map`), recherche, injection.
- **Le problème de méthode** : llama.cpp ne le calcule pas, et V4-Flash ne l'a
  pas — **il n'existe aucune référence**. Livrer serait violer la règle 6.
- **Deux issues acceptables** : (a) écrire une référence indépendante en Python
  (comme `tools/mla_synthetique.py` pour la MLA) que le moteur doit retrouver ;
  (b) ne pas le faire et l'écrire (le moteur le dit déjà).
- **Porte** (si (a)) : la sonde et la référence Python concordent sur 10 000
  entrées, et le changement de sortie est **annoncé**.

### P9 — Noyaux IQ natifs : après la mesure, pas avant (≈ 1 journée, optionnel)

- Les experts passent aujourd'hui par déquantification + produit f32 (juste,
  lent). Un noyau ne se justifie que si le débit mesuré en P6 le demande.
- **Porte** : le chiffre qui dit ce que coûte la déquantification, et le gain du
  noyau sur le même protocole.

---

## 5. Budget et campagne de validation

| poste | estimation |
|---|---|
| implémentation | P0 3 h · P1 ½ j · P2 3 h · P3 2 h · P4 ½ j · P5 1-2 j · P6 ½ j · P7 ½ j ≈ **4 à 5 journées** |
| passes de validation | ~20, mais sur **V4-Flash (86,9 Go, tient en RAM)** : chargement de la référence ~1 min, 4 à 8 jetons par passe |
| machine | un seul travail lourd à la fois (règle du dépôt) |
| disque | V4-Flash sur le mécanique (lecture mmap), artefacts sur le NVMe |

**Jalons visibles, dans l'ordre** : `hc_attn_pre-0` juste (P1) → `l_out-1` juste
(P3) → couche compressée juste (P4) → **logits corrélés à 0,99 sur V4-Flash**
(P5) → perplexité V4-Flash publiée, portes vertes (P6) → V4.1 exécutable ou
provenance tranchée (P7).

---

## 6. Ce qu'on ne fera pas, et les conditions d'arrêt

- **Pas de bypass du contrôle d'architecture.** Il perd une ligne par phase et ne
  se contourne pas par un drapeau.
- **Pas d'engram sans référence** (P8) : (a) ou (b), jamais « on suppose ».
- **Pas d'approximation silencieuse** : tout raccourci (indexeur ignoré en deçà de
  `index_topk`, couche compressée traitée comme brute) est **dit** dans
  `--config`, le rapport et le message d'ouverture.
- **Si une phase coûte plus du double de son estimation, on s'arrête** et on
  documente — comme la tête garantie.
- **Aucun chiffre de V4.1 n'est publié avant P7.** Jusque-là s'applique la phrase
  du moteur : « ce modèle n'a jamais été exécuté ici ».

---

## 7. Pourquoi cet ordre

- **V4-Flash avant V4.1** : c'est le seul des deux qui ait une référence externe
  **et** qui tienne en mémoire. On implémente une fois, on prouve là où c'est
  possible.
- **P1 avant P2** : sans le mélange des 4 copies, tout ce qui suit a la mauvaise
  entrée — et l'erreur serait silencieuse.
- **P3 avant P4/P5** : valider toute la chaîne (embarquement, MLA, puits,
  dé-rotation, sortie groupée, experts IQ, résidu HC) sur les couches **non
  compressées** avant d'ajouter la compression. Si `l_out-1` diverge, chercher
  dans 38 couches compressées coûte quatre fois plus cher.
- **P4 avant P5** : HCA est le cas dégradé de CSA (sans sélection de candidats) ;
  le faire d'abord donne une implémentation de référence interne.
- **P7 après P6** : adapter à V4.1 avant d'avoir prouvé la famille serait
  empiler deux inconnues.
- **P8 et P9 en dernier** : ce sont les seuls postes sans gate externe (engram) ou
  sans nécessité démontrée (noyaux IQ).

**Fichiers prévisibles** : `drave-core/src/model.rs` (état HC, épilogue
d'attention, trois chemins d'attention), `drave-core/src/gguf.rs` (nouveaux
tenseurs — I8, F16 déjà lus), `drave-core/src/main.rs` (`--config`, aide),
`tools/ref_logits.cpp` (filtres déjà en place), `tools/portes.sh` (une porte
V4-Flash quand elle existera), plus un rapport par phase dans `reports/`.
