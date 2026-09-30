# Reprise — état du projet et mode d'emploi pour une nouvelle session

> Rédigé à la fin d'une session longue. Tout ce qui suit est **mesuré**, pas
> déduit. Les valeurs de perplexité sont des **références de non-régression** :
> si une modification les change, c'est qu'elle a changé le calcul.
>
> **Nom** : le projet s'appelle **Drave** (binaire `drave`, paquet `drave-core`,
> variables `DRAVE_*`, histoire du renommage dans `docs/histoire.md`). Le dossier
> de travail, lui, s'appelle encore `Qtrinet` — les chemins ci-dessous sont ceux
> qui existent.

---

## 1. En une phrase

`drave-core` est un moteur d'inférence Rust (~13 168 lignes, `std` seul) qui
charge les GGUF **en place** (aucune copie, aucune requantification), exécute les
projections soit en listes d'événements, soit en produit scalaire dense, gère les
MoE, tient une conversation, et déporte au GPU ce qui y gagne. Il fait tourner du
0,5 B au 120 B sur le CPU de cette machine.

```bash
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core && cargo build --release
./target/release/drave ../models/Qwen2.5-0.5B-Q8_0.gguf \
    --infer --chat --flux --prompt "Explique le ciel bleu en une phrase." \
    --n 64 --ctx 512 --threads 16 --temp 0
```

---

## 2. Références de non-régression

> **Revérifiées le 30/09 après tous les changements de la journée** (mode lot,
> protocole v4, DRVF v2/v3, plafond R4, tableau de bord) : Qwen ctx 256 =
> **19,3885** et gpt-oss ctx 256 = **15,1757**, `cargo test` **17/17**. La porte
> gpt-oss était la seule que la relecture adversariale n'avait pas pu faire
> tourner (bornes de temps) ; elle est verte.
>
> **Chemin GPU revérifié le même jour** (personne ne l'avait exercé depuis les
> changements) : gpt-oss avec `DRAVE_GPU=1` donne **15,1667**, la valeur attendue
> du pilote, et `--gpu-banc` retrouve l'exactitude des noyaux — 1,6 ms par ligne
> en warp-par-ligne contre 7,2 ms sur 30 fils CPU, **écart max 1,99e-7**.

Corpus : `/tmp/wt2_txt.txt` = 20 000 premiers octets de `data/wikitext2_test.txt`.
**Régénérable** (à refaire si `/tmp` a été vidé) :

```bash
cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet
head -c 20000 data/wikitext2_test.txt > /tmp/wt2_txt.txt
# les identifiants DOIVENT venir du tokenizer du modèle — jamais croisés
drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf \
    --tokenize --fichier /tmp/wt2_txt.txt --sortie /tmp/ids_qwen.txt
drave-core/target/release/drave /home/stephane/FastNVMe/models/gpt-oss-120b-MXFP4.gguf \
    --tokenize --fichier /tmp/wt2_txt.txt --sortie /tmp/ids_oss.txt
```

Le mode `--tokenize --fichier` **vérifie la réversibilité** (texte reconstruit
identique à la source) — les deux tokenizers la passent sur ce corpus.

| modèle | commande (abrégée) | perplexité attendue |
|---|---|---|
| Qwen2.5-0.5B Q8_0 | `--dense --limit 512` | **19,3885** |
| Qwen2.5-0.5B Q4_0 | `--q4 --limit 512` | **21,0110** |
| Qwen2.5-0.5B Q8_0, 6 bits | `--dense --bits-attn 6 --bits-ffn 6 --limit 512` (ctx 256) | **19,5633** ← bat l'int8 (19,8059), mais de moins loin qu'annoncé : la valeur **19,3045** qui figurait ici n'est PAS reproductible avec cette commande (re-mesuré le 30/09, deux fois) |
| Qwen2.5-0.5B Q8_0, 4 bits | `--dense --q4 --limit 512` | **23,1323** |
| Qwen2.5-1.5B Q4_K_M | `--q4 --limit 256` | **12,9228** |
| Qwen2.5-VL-7B Q4_K_M | défaut, `--limit 128` | **10,9947** |
| Qwen3-30B-A3B MoE | `--dense --limit 128` | **7,6139** |
| gpt-oss-120b MXFP4 | `--dense --limit 64`, ids_oss | **20,8361** (63 jetons) |
| gpt-oss-120b MXFP4 | `--dense --limit 512`, ids_oss | **15,1757** (510 jetons, deux fenêtres) |
| gpt-oss-120b MXFP4 | `--ppl-texte`, `--limit 512` (mêmes jetons) | **15,0757** (509 jetons) |
| gpt-oss-120b MXFP4 | `--dense --ctx 512 --limit 512`, ids_oss | **18,5803** (511 jetons, une fenêtre) |
| gpt-oss-120b MXFP4, YaRN | `DRAVE_YARN=1`, `--ctx 512 --limit 512` | **174,3375** ← le YaRN statique du modèle |

> **gpt-oss : les anciens chiffres (39,8 puis 129,9) sont périmés.** Ils ont été
> mesurés avec deux bugs depuis corrigés : le biais `attn_output` ignoré et la
> fenêtre glissante appliquée aux 36 couches au lieu d'une sur deux. Le détail
> est dans `reports/rapport-gpt-oss-perplexite.md` ; la **référence externe**
> (llama.cpp, mêmes identifiants, sans BOS) donne 38,37 à 63 jetons et 169,67 à
> 511 en mode YaRN — notre moteur fait **mieux**, parce qu'il sait éteindre
> YaRN, qui coûte ici un facteur 9.

Toujours `--ctx 256 --abits 16 --threads 16`, et **jamais croiser les fichiers
d'identifiants** : nourrir un modèle avec le découpage d'un autre donne une
perplexité qui ne mesure que l'absurdité de l'entrée (42 127 mesuré ainsi).
Un garde-fou le détecte maintenant (identifiant ≥ vocabulaire = erreur franche).

---

## 3. Ce qui est implémenté et vérifié

| domaine | état |
|---|---|
| Formats lus **en place** | Q4_K, Q6_K, Q4_0, Q8_0, MXFP4, F16, F32 |
| MoE | routeur + biais de routeur, biais par expert, top-k, expert partagé, tranches contiguës |
| Architectures | q/k-norm (Qwen3), `post_attention_norm` (gpt-oss), sinks appris, fenêtre glissante, YaRN (défaut **off**), RoPE simple et partiel, `head_dim` déclaré |
| Tête de sortie | `output.weight` si non lié (bug corrigé), sinon `token_embd` |
| Tokenizers | Qwen2 **et** o200k (gpt-4o), tous deux lus du GGUF, sélectionnés par `tokenizer.ggml.pre` |
| Échantillonnage | température, top-k 40, top-p, **pénalité de répétition** (`--rep-penalty`, fenêtre `--hist`) |
| Génération | **sortie en flux** (`--flux`), **session multi-tours** (`--session`), arrêt sur fin de tour |
| Encodages | listes d'événements (push), dense int8 par ligne, dense 4 bits par bloc, **6 bits empaqueté par bloc** |
| GPU | noyaux PTX + API pilote, tête et projections opt-in (`DRAVE_GPU=1`) |
| Outils | `--ppl`, `--plan` (placement), `--tokenize`, `--bits N` (simulation de précision) |
| Mesure | `--ppl-texte F` (identifiants du tokenizer du modèle), `--depuis N` (ne noter qu'à partir du jeton N, contexte ancré — les mêmes jetons deviennent comparables à 512, 1 024, 4 096… de contexte), `--ppl-profil` (perte par tranche de 256 positions), `--logits-bin F` (logits bruts), `--harmony*` (habillage harmony), `--swa-pattern N`, `--sans-fenetre` |
| Rotation | **YaRN à retardement** : RoPE simple tant que `--ctx` tient dans `rope.scaling.original_context_length` (4 096), **interpolation YaRN seule au-delà** (la température `mscale` est la moitié nuisible : divise la perplexité par 8,9 à 512 jetons). `DRAVE_YARN=1` = YaRN complet des références, `DRAVE_YARN_NON=1` (ou `--sans-yarn`) = jamais, `DRAVE_YARN_MSCALE=0/1` = température seule. La trace `[config] rotation` dit lequel est actif |
| Budget de contexte | `--plan --ctx N` : KV f32/int8/int4, relecture par jeton, décodage selon les bandes passantes, coût du préremplissage séquentiel, portée du YaRN |
| Référence externe | `tools/ref_logits` (llama.cpp, mêmes identifiants, sans BOS) + `tools/compare_logits.py` |

**Vérifications externes déjà faites** (elles ont trouvé les bugs) : déquantification
Q4_K/Q6_K comparée à une référence F16 des mêmes poids ; tokenizer o200k comparé
à `/tokenize` ; perplexités recoupées avec `llama-perplexity` ; **logits comparés
un à un à llama.cpp** sur les mêmes identifiants (corrélation 0,999976 au premier
jeton, top-1 identique sur 63 positions, |ΔNLL| médian 0,076) ; tokenizer o200k
comparé à `llama-tokenize` sur 4 424 jetons (0 écart).

---

## 4. Pièges de l'environnement (tous rencontrés)

| piège | solution |
|---|---|
| **CUDA 13 : les symboles non versionnés du pilote échouent** (`cuMemAlloc` → erreur 201 alors que le contexte est courant) | utiliser partout les `_v2` |
| `nvcc` refuse gcc 15/16 (conflit d'en-têtes glibc) | compiler en **PTX avec clang**, le pilote compile à la volée |
| Python/numpy lent | `LD_PRELOAD=/usr/lib64/libopenblas.so.0` |
| 16 fils **battent** 32 sur ce moteur | ne pas sursouscrire la barrière tournante ; `--threads 16` |
| Épinglage NUMA | **perd** (23,2 → 25,5 s sur le 30 B) ; `--pin` déconseillé |
| Déport GPU | rentable seulement au-delà de **8 Mo** par matrice ; la tête n'est **pas** déportée (noyau non coalescé, 23 → 159 ms) |
| Charge de fond de la machine | fait varier les durées du simple au double : entrelacer les A/B, préférer les métriques déterministes |
| Les boucles d'analyse CLI sont **triplées** | un drapeau en **dernière** position était ignoré ; `--pin` et `--moe-topk` absents d'un des modes. Vérifier le mode visé |

---

## 5. Règles de méthode (chacune a coûté une erreur)

1. **Mesurer avant de conclure.** Le croisement push/pull était annoncé à 10 %,
   il est à 22 %. Dérouler un noyau « évident » n'a rien donné : le chemin était
   au mur mémoire, pas mal écrit.
2. **La double quantification est le piège le plus cher** : +12 % de perplexité
   sur Q4_0, et une simulation de précision qui annonçait 19,96 là où le format
   réel donne 19,30.
3. **Une hypothèse se teste, elle ne se défend pas.** Trois ont été réfutées cette
   session : cache KV pour l'attention (c'était la vectorisation), rotary partiel
   pour gpt-oss (185 → 1 095), YaRN (184,9 contre 39,8 sans).
4. **Vérifier quel chemin est actif** avant de déboguer un chiffre : la trace
   `[config]` au chargement dit quelles particularités ont été reconnues.
5. **Ne pas conclure sur 255 jetons** : l'écart peut être du bruit ; 510 minimum.
6. **Ne pas laisser un dépôt cassé** pour finir une refactorisation : revenir au
   dernier état valide est une option honorable.

---

## 6. Les huit chantiers : où ils en sont

| # | chantier | état | mesure |
|---|---|---|---|
| 1 | protocole de perplexité longue | **fait** | `--depuis N` note les mêmes jetons à contexte variable ; `--depuis 256 --ctx 256` redonne exactement la fenêtre 2 historique (21,565) |
| 2 | seuil de rotation YaRN | **fait, seuil à 4 × la longueur déclarée** | comparaison appariée (mêmes 512 jetons) : contexte 128→1536, RoPE simple 39,52/49,79/49,93/298,56 contre interpolation 42,13/82,02/82,15/578,86 → le simple gagne partout. **Au-delà du seuil** (5 120 jetons, corpus de 17 k maintenant disponible) : simple **9,6986** contre interpolation seule **1 269,1777** → le seuil de 4 096 était **trop bas** ; le moteur ne bascule plus qu'à 1,25 × la longueur déclarée. Au-delà (16 k, 131 k) : non mesuré, une passe à 16 k coûte une heure |
| 3 | KV int8 puis int4 | **fait, jusqu'à 8 192** | **échelles par bloc de 32** : int8 +**1,5 %** à 512 (était +7,1 %), **+3,0 % à 8 192** (llama.cpp +0,8 %) ; int4 **+364 % à 8 192** contre +494 % pour llama.cpp — meilleur que la référence, et 1 M tient en int4 (9,7 Go). Prix caché : la passe coûte 864 s (f32) / 1 144 (int8) / 1 461 (int4), la déquantification par élément — c'est ce que le noyau GPU de E4 supprime |
| 4 | préremplissage par lots | **fait, −20 % et attribué** | tuilage, **attention groupée dans le lot** et **tête en lot** (`logits_lot`) : Qwen ctx 512, **17,1 s → 13,6 s (−20 %)** à perplexité égale (13,1368 → 13,1359) ; gpt-oss ctx 256, ≈ 50 s → **34,4 s** (13,7205 partout). Postes : projections ÷2,6, FFN/wo ÷1,43, attention par lots encore **×1,7** (5,59 contre 3,24 ms/jeton), tête inchangée (5,47 contre 5,63 — noyau lié au calcul, pas à la mémoire). Au passage : pointeur gras sur les sommes par bloc (lot > 90 → blocage muet) corrigé et verrouillé par un test — voir `reports/rapport-prefill-par-lots.md` |
| 5 | échelles par bloc pour `DenseQ8` | **fait, hypothèse réfutée** | 23,696 contre 23,612 : les échelles par bloc n'apportent rien ; l'avantage du 6 bits est son coût (25 % d'octets en moins à qualité égale) |
| 6 | boucles CLI unifiées | **fait** | `struct Options` + `analyser` ; trois drapeaux de plus trouvés ignorés (`--attn-topk`, `--qk-topk`, `--sans-yarn` en inférence) et un bug de pas de lecture corrigé |
| 7 | noyaux GPU | **fait, quatre formats** | warp par ligne : tête **Q8_0** (1,6 ms contre 7,3 CPU, écart 2e-7), **MXFP4** (0,1 ms, écart **0,00e0** — bit à bit), **Q4_K** (0,5 contre 1,2 ms, 4e-7), **Q6_K** (3,6 contre 8,3 ms sur la tête liée de 191 Mo, 3,3e-7 ; ×5 sur un tenseur de 11 Mo). **Tête Q6_K branchée** dans le moteur : `DRAVE_GPU=1 DRAVE_GPU_TETE=1` → 7,58 → **3,60 ms/jeton**, perplexité identique (13,6877). Reste le cache d'experts chauds en VRAM : la mesure d'activation (`rapport-localite-activation.md`) dit qu'un préchargement statique ne paie pas sur SiLU |
| 8 | suite du plan 1 M | **fait pour E4/E5** | **E4 KV déporté en VRAM** : noyaux `attn_kv_*` (tuiles de 32 clés, softmax en ligne, recombinaison + puits), miroir du cache **paginé** (capacité doublée à la demande : 0,05 Go de VRAM à ctx 1 M après 512 jetons) et `DRAVE_GPU_KV=1` — à 1 M de clés l'attention passe de 968 ms à **13,2 ms** par couche (int4, ×73) et, dans le moteur à 4 096 de contexte, de **22,2 à 3,3 ms/jeton** (−38 % de bout en bout) à perplexité identique (12,2177 → 12,2175). **E5 attention creuse** : mesurée (`--attn-topk 256` : 234,9 contre 298,6). MLA et vision restent non testables (aucun modèle MLA ici ; le projecteur `mmproj` est là mais rien ne lit les patchs) |

### Mesures du tour « huit chantiers » (toutes commitées)

| mesure | valeur |
|---|---|
| noyau GPU Q8_0 warp (tête Qwen 0.5B, 144,6 Mo) | **1,6 ms** contre 7,3 ms CPU (×4,6), écart 2e-7 |
| noyau GPU MXFP4 warp (expert gpt-oss, 4,4 Mo) | **0,1 ms** contre 7,5 ms CPU (×75), écart **0,00e0** |
| noyau GPU Q4_K warp (Qwen 1.5B, 7,7 Mo) | 0,5 ms contre 1,2 ms CPU (×2,2), écart 4e-7 |
| noyau GPU Q6_K warp (tête liée Qwen 1.5B, 191,4 Mo) | **3,6 ms** contre 8,3 ms CPU 16 fils (23,2 → 53,6 Go/s), écart 3,3e-7 |
| noyau GPU Q6_K warp (ffn_down Qwen 1.5B, 11,3 Mo) | **0,3 ms** contre 1,5 ms CPU (×5), écart 7,1e-7 |
| tête Q6_K déportée (Qwen 1.5B Q4_K_M, ctx 256, 510 jetons) | 7,58 → **3,60 ms/jeton** ; bout en bout 44,4 → 41,4 s (−7 %) ; lot 512 : 36,0 → 34,0 s ; **perplexité identique** (13,6877 / 13,6864) |
| préremplissage par lots (Qwen, ctx 512) | lot 1 = **17,1 s** · lot 512 = **13,6 s** → **−20 %** (perplexité 13,1368 → 13,1359) |
| préremplissage par lots (gpt-oss, ctx 256, MoE groupé) | ≈ 50 s à lot 1 · **34,4 s** à lot 256 (13,7205 dans tous les cas) |
| tête de sortie en lot | **aucun gain** (5,47 contre 5,63 ms/jeton) : noyau lié au calcul — il faut AVX2 ou le GPU |
| attente du pool après panique d'un worker | **échoue en clair** au lieu de boucler (constaté : 10 min d'attente active) |
| KV int8, échelles par bloc | +1,5 % (512 jetons) et +3,4 % (4 591) — était +7,1 % et +5,2 % |
| KV int4, échelles par bloc | +219 % (512) et +287 % (4 591) — était +384 % et +450 % |
| KV à 8 192 jetons (longueur de la référence llama.cpp) | f32 **14,2339** · int8 **14,6667 (+3,0 %)** contre +0,8 % chez llama.cpp · int4 **66,0369 (+364 %)** contre +494 % chez llama.cpp |
| porte gpt-oss selon l'ouverture du pilote | sans `DRAVE_GPU` : **15,1757** · avec `DRAVE_GPU=1` : **15,1667** — l'écart vient du déport automatique des projections Q8_0 (> 8 Mo), pas d'une régression |
| attention creuse (gpt-oss, ctx 2 048) | sans restriction 298,56 · **top-256 : 234,88** · fenêtre 512 : 3 269,34 |
| KV déporté en VRAM, 1 M de clés (une couche, `--banc-kv`) | f32 165,8 → **13,6 ms** (×12) · int8 510,6 → 15,0 (×34) · int4 968,5 → **13,2 ms (×73)**, écarts 1e-5 à 1e-4 |
| KV déporté dans le moteur (`DRAVE_GPU_KV=1`, ctx 4 096) | attention **22,16 → 3,29 ms/jeton** (÷6,7) · balayage 219,4 → **136,2 s** · perplexité 12,2177 → 12,2175 |
| attention déportée dans le PRÉREMPLISSAGE par lots (ctx 4 096, lot 512) | **261,6 → 93,7 s (×2,8)**, perplexité **identique** (12,2175) |
| dépaquetage vectorisé du noyau (1 M de clés) | f32 13,6 → **7,0 ms** (308 Go/s) · int8 15,0 → **6,5** · int4 13,2 → **7,4 ms** |
| cache d'experts MXFP4 en VRAM (gpt-oss, 32 jetons) | 5,12 → **5,43 jetons/s (+6 %)**, 53,5 % de succès — verdict : ne pas activer par défaut |
| cache KV CPU paginé (ctx 1 M, 512 jetons écrits) | **0,03 Go** alloués au lieu de 25,77 Go, perplexité inchangée |
| aiguille v2 (12 sondes) | **12/12 trouvées** : 1,5B 512/2048, 30B 2048, gpt-oss 4096, profondeurs 0,1/0,5/0,9 |
| KV déporté, ctx 512 (point de croisement) | attention 2,91 (CPU) contre 3,22 ms (GPU) : le noyau ne paie qu'au-delà de ~4 000 clés |
| miroir VRAM paginé (capacité doublée à la demande) | à **ctx 1 M** : cache CPU 25,77 Go contre **0,05 Go** de VRAM pour 512 jetons écrits (l'allocation d'un bloc exigeait 25,77 Go et refusait) ; perplexité 13,1369 inchangée |
| rotation, comparaison appariée | RoPE simple gagne à TOUTES les longueurs mesurées : 128 à 1 536 (39,5 → 298,6), 5 120 (**9,70 contre 1 269,18**), 16 384 (**35,18 contre 1 133,02**) |

### Ce qu'il faut faire ensuite, dans l'ordre

État au moment d'écrire : les huit chantiers de la campagne précédente sont clos
(voir le tableau du §6), et la campagne « six nouveaux chantiers » a livré
l'aiguille v2, le dépaquetage vectorisé du noyau d'attention, les experts MXFP4
en VRAM, l'attention par lots déportée et la pagination des deux caches KV. Ce
qui reste est classé par rentabilité mesurée.

1. **Fusionner la chaîne du top-k déporté.** Elle gagne déjà à 16 k (attention
   19,58 → **7,59 ms/jeton**, balayage −24 %), mais coûte 8 lancements et 17
   transferts par couche et par jeton : un seul noyau par ligne (descente radix +
   collecte + somme, les k scores en partagé) doit ramener les 8 lancements à 2 et
   supprimer le tampon `nh × n × 4` que le plan déclarait « trop ». Critère :
   dépasser le CPU dès 4 000 clés. Détail : `docs/plan-gpu-topk.md`, § « La
   prochaine étape n'est pas un noyau de plus ».
2. **Noyau de la tête Q8_0.** Le chemin CPU de la tête par lots est **lié au
   calcul** (5,5 ms/jeton pour Qwen 0.5B, le lot n'y change rien). Deux voies :
   un noyau AVX2 (le déport GPU Q8_0 existe déjà : 15,6 → 6,2 ms/jeton sur
   gpt-oss). C'est le premier consommateur après le FFN.
3. **Second GPU.** 16 Go dorment. Le cache d'experts MXFP4 (13,2 Mo par expert,
   4 608 experts chez gpt-oss) et le KV à 1 M le rempliraient utilement ; il faut
   un second contexte CUDA et une règle de répartition.
4. ~~**Rotation au-delà de 5 120 jetons.**~~ **MESURÉ À 16 k** : RoPE simple
   **35,18** contre **1 133,02** en interpolation seule, et le seuil est passé à
   **4 ×** la longueur déclarée (16 384, la plus grande longueur mesurée).
4. ~~**MLA et vision.**~~ **TOUS DEUX FAITS.** MLA : modèle synthétique + référence
   numpy, écart **5,2e-7**. Vision : chaîne COMPLÈTE et démontrée de bout en bout
   — image → patchs → 32 couches (rotation 2-D **conforme à la source** ggml,
   fenêtre locale d'après clip.cpp) → `v.post_ln` → projecteur (64 groupes ×
   3 584) → injection dans le modèle de texte → **152 064 logits**. Tranches
   validées contre numpy : patchs 5,4e-7, projecteur 1,7e-6, une couche 1,8e-6.
   Réserves NOMMÉES : la permutation colonne-majeur des couches fenêtrées
   (constatée dans la source, pas implémentée), et l'absence de référence locale
   pour la qualité (libmtmd d'ollama bloqué sur `tokenize`, cinq hypothèses
   testées). Tout est dans `docs/plan-mla-vision.md`.

5. **Top-k dans le noyau d'attention.** `--attn-topk 256` AMÉLIORE la perplexité
   (234,88 contre 298,56 à 2 048) mais repasse aujourd'hui par le CPU : le noyau
   GPU ne le gère pas.
6. ~~Experts MXFP4 dans le préremplissage par lots~~ **MESURÉ, À NE PAS FAIRE
   TEL QUEL** : le cache LRU donne +6 % en décodage (5,12 → 5,43 jetons/s,
   53,5 % de succès, 10,64 Go montés) — le chemin CPU des experts est déjà AVX2
   et le coût par expert est faible. Il faudrait supprimer les trois lancements
   et copies par expert, ou grouper les projections.
7. **Mesure de qualité à contexte long** (`reports/rapport-aiguille.md`) :
   étendre la grille à 8 192 et 16 384, plusieurs codes par sonde, et croiser avec
   `--attn-topk`.

### Les variables d'environnement, et leurs pièges

| variable | ce qu'elle fait | le piège |
|---|---|---|
| `DRAVE_GPU=1` | ouvre le pilote CUDA (`gpu::instance`) | **c'est elle qui commande tout** ; sans elle, les autres ne font RIEN et rien ne le dit |
| `DRAVE_GPU_TETE=1` | déporte la tête (Q8_0 ou Q6_K) | inutile sans `DRAVE_GPU` |
| `DRAVE_GPU_KV=1` | tient le cache KV en VRAM et y calcule l'attention | inutile sans `DRAVE_GPU` ; au-dessous de ~4 000 clés le CPU gagne (lancements + recopies) |
| `DRAVE_GPU_TOPK=1` | calcule le top-k de l'attention (`--attn-topk`) en VRAM : scores, seuil radix, collecte des k indices, softmax + Σ w·V | inutile sans `DRAVE_GPU` **et** `DRAVE_GPU_KV` ; exige `nkv × rep = nh` et `k ≤ 1 024` ; tout refus d'un noyau retombe sur le CPU. Perplexité identique à 5e-4 près (9,4162 contre 9,4167 à ctx 2 048), mais **pas encore de gain de temps à 2 048 clés** : six lancements et cinq recopies par couche et par jeton (la fusion des quatre passes est à faire) |
| `DRAVE_GPU_EXPERTS=1` | cache LRU des experts MXFP4 en VRAM | inutile sans `DRAVE_GPU` ; budget par `DRAVE_GPU_EXPERTS_GO` (défaut 8) |
| `DRAVE_KV_BITS=8` ou `4` | quantifie le cache KV (défaut f32) | le 4 bits coûte +364 % de perplexité à 8 192 |
| `DRAVE_KV_K_F32=1` | garde les CLÉS en f32 (valeurs quantifiées) | mesuré : à 8 192, **64 %** de la taille f32 (5,125 octets par élément, échelles comprises) pour +0,023 %, contre +3,04 % pour l'int8 complet (28 % de la taille) — l'écart int8 vient des clés à 99 % (`reports/rapport-attribution-kv.md`) |
| `DRAVE_KV_V_F32=1` | garde les VALEURS en f32 | +3,01 % : ne sert à rien, l'erreur ne passe pas par là |
| `DRAVE_KV_K_F16=1` | clés en **f16** (2 octets/valeur, précision relative) | **le meilleur réglage mesuré** : à 8 192 jetons, clés f16 + valeurs int8 = **+0,018 %** pour **39 % de la taille f32** — contre +0,023 % pour les clés f32 (64 % de la taille) et +3,04 % pour l'int8 complet (28 %) |
| `DRAVE_TRACE_BLOCS=1` | trace DRVF **v3** : valeurs i8, échelle f16 par bloc de 32 | 45 079 930 o contre 66 370 408 en v2 (−32 %), rejeu 19,4029 contre 19,3885 (+0,074 %) |
| `DRAVE_FLUX_VERIF=1` | vérifie l'écart entre l'activation calculée et celle que la trace impose | 1,5e-5 en v2 ; **muet dès que `--lot > 1`** (le rejeu par lots passe par `flux_lot`) |
| `DRAVE_HARMONY_TRACE=1` | trace les fenêtres du découpage « harmony » (gpt-oss) | diagnostic |
| `DRAVE_VISION_TEXTE=<gguf>` | modèle de texte qui reçoit le vecteur d'image | 152 064 logits démontrés de bout en bout |
| `DRAVE_Q8_BLOCS=1` | échelles par bloc de 32 pour `DenseQ8` | **hypothèse réfutée** : 23,696 contre 23,612 — aucun gain |
| `DRAVE_SANS_EMPRUNT=1` | reconstruit les matrices au lieu de les emprunter au GGUF | outil de diagnostic (le lecteur « en place » est le défaut) |
| `DRAVE_YARN_RAMPE=0` | force l'interpolation PURE de YaRN (rampe nulle) | mesure du §6.2 : le RoPE simple gagne partout |
| `DRAVE_BANC_KV_UNIT`, `_KUNIT`, `_K0`, `_V1`, `_GRAD`, `_DEBUG` | variantes du **banc KV** (`--banc-kv`) : valeurs unitaires, clés nulles, dégradé | outil de mesure, pas des réglages de production |
| `DRAVE_DEBUG_FLUX=1` | le nœud moteur imprime ce qu'il reçoit (n, positions, octets) | diagnostic du mode lot |
| `DRAVE_KV_F16=1` | arrondit clés/valeurs en f16 avant quantification | mesuré : aucun effet (hypothèse réfutée) |
| `DRAVE_YARN=1` / `DRAVE_YARN_NON=1` / `DRAVE_YARN_MSCALE=0` | force / interdit / règle la rotation | le défaut ne bascule qu'à 1,25 × la longueur déclarée |
| `DRAVE_BANC_KV_GPU_SEUL=1` | saute la référence CPU du banc de KV | à 1 M elle coûte 3 à 16 minutes |

Une porte de non-régression se mesure **sans** `DRAVE_GPU` : la variable déporte à
elle seule les projections Q8_0 de plus de 8 Mo, ce qui change le chiffre de
0,06 % (15,1757 → 15,1667 sur gpt-oss).

## 6bis. Session « Drave » — le calcul réparti tient debout

Tout est mesuré, tout est commité. Détail complet dans `docs/roadmap.md` (phases
0 à 3) et les rapports cités.

**Le découpage en deux nœuds est fidèle** (`reports/rapport-phase3-reparti.md`) :
écart local/réparti **0,00e0** — 144,8289 des deux côtés à 40 jetons, et
**9,5146 des deux côtés à 1 024 jetons** (1 023 flux : le dernier jeton n'a rien
à prédire, il n'est plus envoyé), le banc
réparti prenant le temps du calcul local (19,7 contre 19,4 ms par jeton). Il a
fallu deux corrections dans `Model::forward`, et la première ne suffisait pas :

1. la boucle partait de `0` au lieu de `couche_debut..couche_fin` : le pilote
   calculait les 24 couches, envoyait l'état FINAL, et le pair les recalculait
   toutes par-dessus (`forward_lot` et `forward_mla`, eux, respectaient la plage) ;
2. la norme finale était appliquée DEUX fois (le nœud moteur normait parce que sa
   plage allait jusqu'à la dernière couche, puis le pilote normait). La règle est
   maintenant portée par un drapeau explicite, `flux_brut`.

**Le protocole de flux est en v5** (`docs/format-flux.md`) : en-tête de **79
octets** avec version, mode et le **contrat d'activation complet** (niveaux, seuil,
top-k, renorm, les sept top-k par projection, attn/qk/moe top-k) — deux nœuds
réglés différemment calculaient deux choses différentes en silence (0,69 d'écart
mesuré, et un serveur en `--topk-q 900` contre un client en `--topk-q 4` divergeait
sans un mot). Un pair d'une autre version est refusé en le disant. Les modes sont
dense, listes, blocs et **lot** ; `--flux-serveur` accepte `hôte:port`, et
`colab/` (notebook + `tools/preparer_colab.sh`) porte la recette de la phase 3.4.

**Ce que coûte le transport** (`reports/rapport-transport-liste.md`) :

| | octets par flux | écart local/réparti |
|---|---|---|
| dense f32 | 3 663 | **0,00e0** |
| listes à échelle par bloc, seuil 0,01 | 1 608 | 2,7e-2 |
| échelles par bloc, seuil 0,01 | 2 268 | 2,7e-2 |

`TCP_NODELAY` a divisé l'attente du pair par six (**97,6 → 16,1 ms** par jeton,
soit 1,01× le calcul local) : le banc réparti prend maintenant le temps du calcul
local, à logits identiques. Et avec un relais retardateur
(`tools/proxy_latence.py`), la formule du coût est mesurée :
**attente ≈ calcul distant + 3,2 × latence par message** — 1,01× le calcul local à
0 ms, 1,99× à 5 ms, 4,89× à 20 ms, fidélité intacte (0,00e0) dans les trois cas.
Le seuil de rentabilité (phase 3.3) est donc une affaire de latence, pas de débit :
0,25 Mbit/s suffisent. Un aller-retour Colab de 60 ms donnerait ~8 jetons/s
contre ~60 en local.

**Phase 1.4 attribuée** (`reports/rapport-attribution-kv.md`) : l'écart du cache
KV int8 (+3,0 % à 8 192) vient **entièrement des clés** — clés f32 + valeurs int8
donne +0,023 %, clés int8 + valeurs f32 donne +3,01 %. Réglage utilisable tout de
suite : `DRAVE_KV_BITS=8 DRAVE_KV_K_F32=1` (75 % de la taille f32 pour +0,02 %).

**Une hypothèse réfutée** : transmettre l'entrée NORMÉE au lieu du résidu brut
passait l'écart de 0,00e0 à **5,61e0** en mode dense — la connexion résiduelle a
besoin du résidu lui-même. Drapeau retiré, réfutation écrite.

### Session « autonomie jusqu'à 15h » — ce qui s'ajoute (12h → 15h)

**Le préremplissage par lots sur le fil est FAIT** (mode 3 du protocole) : N états
d'un coup au lieu d'un flux par jeton. Vérifié : 256 jetons en 4 lots de 64 →
**écart 0,00e0** (18,0851 = 18,0851) ; en UN lot de 917 583 octets → **0,00e0**
aussi. C'était le bloqueur de la phase 3.4 ; `colab/` contient maintenant le
notebook prêt à ouvrir, `tools/preparer_colab.sh` fait le dépôt en un fichier
(`git bundle`, 4,5 Mo — il n'y a pas de dépôt distant) et vérifie l'empreinte du
modèle.

**Le protocole est en version 5** et le contrat d'activation transporte
niveaux, seuil, top-k, renorm, les sept top-k par projection, attn/qk/moe top-k :
un serveur lancé avec `--topk-q 900` et un client avec `--topk-q 4` donnent quand
même 0,00e0 — les réglages du client gagnent. En version 3 ils divergeaient en
silence.

**Le format de trace est en version 2 par défaut et 3 en option** :

| | v1 | v2 (défaut) | v3 (`DRAVE_TRACE_BLOCS=1`) |
|---|---|---|---|
| trace dense 512 jetons | 132 396 736 o | 66 370 408 o | **45 079 930 o** |
| rejeu `--flux-forcer` | 19,3885 | 19,3885 | 19,4029 (+0,074 %) |

La v2 (indices par écarts) est SANS PERTE ; la v3 (valeurs i8, échelle f16 par
bloc de 32) est avec perte. Le rejeu annonce ses comptes — `24 576 listes
servies, 0 manquantes` — et c'est ce qui a démasqué un FAUX POSITIF : mon premier
« rejeu v3 = 19,3885 » lisait en fait la perplexité du calcul normal, la trace
n'étant pas chargée du tout (l'écrivain décalait le fichier de huit octets).

**L'audit des drapeaux** (`reports/rapport-drapeaux-ignores.md`, délégué) : 110
options passées au crible, **46 ignorées dans au moins un mode**. Corrigés :
les top-k (ci-dessus), `--keep` en `--ppl` (prouvé : 1929,3230 identique avant),
`--ffn-gain` en `--infer`, `--threads` en FS/PR/BM, `--hebb-q`/`--hebb-out`,
`--plan` sans `--ctx` (annonçait 512 au lieu de 32 768), la précédence de fenêtre,
le pas de 2 du mode par défaut (`--dense --threads 4` annonçait 30 fils),
`--trace-flux` en inférence (muet), les modes multiples (silencieux). Restent :
`--banc-vision` (ne reçoit aucune `Options`), `--bits` du noyau GPU, et la
recommandation de fond — un `--options-actives` qui imprime les réglages
réellement en vigueur.

### Créneau 15h07 → 18h00 : le mode 4, et la frontière KV confirmée

**Le protocole est en version 5** avec un cinquième mode : le **mode 4 « lot en
listes »**. Chaque état d'un lot est encodé comme le mode 2 et auto-délimité par
ses trois tailles (`a_j · n_blocs_j · longueur_j`). Mesuré, 256 jetons, lots de 16,
seuil 0,01 : **1,5 ko par jeton au lieu de 3,5** (÷2,3) pour un écart de 3,03e-2 —
sous le critère (1,5 × les 2,74e-2 du mode 2 par jeton). Plan :
`docs/plan-mode4-lot-listes.md`.

Trois choses apprises en le faisant : la construction de l'en-tête est maintenant
UNE fonction (`tete_flux`) pour les trois émetteurs (sa duplication avait produit
l'en-tête d'un octet trop long) ; le serveur ne traitait que le mode 3 dans sa
branche lot, donc un flux de listes paniquait ; et le refus d'un mode inconnu est
devenu IMMÉDIAT, avant tout octet de corps. **17 tests**, dont quatre sur le mode 4
(état forgé, deux états, préfixe incohérent, flux à zéro élément).

**La frontière du cache KV tient à 4 096 comme à 8 192** : clés f16 + valeurs int8
= +0,011 % et +0,018 %, int8/int8 = +2,25 % et +3,04 %. Les clés f16 font aussi
bien que les clés f32 pour moitié moins d'octets. ⚠️ Interaction : le miroir VRAM
suppose une disposition homogène, donc les variantes d'attribution le DÉSACTIVENT —
à très long contexte avec `DRAVE_GPU_KV=1`, garder les clés en f32.

**Le noyau GPU de top-k** (phase 1.1) est spécifié et chiffré dans
`docs/plan-gpu-topk.md` : le chemin GPU est conditionné à `attn_topk == 0`
(`model.rs:3150`), donc le mode creux retombe sur le CPU où il coûte 968 ms par
couche à 1 M de clés contre 13,2 ms avec le miroir. Trois noyaux, six étapes, leur
critère d'exactitude — c'est le prochain chantier, et il n'a pas été bâclé faute de
temps : il est écrit.

### Créneau 17h41 → 19h41 (sprint 1) : le top-k GPU, du banc au moteur

**Les trois noyaux du plan sont écrits, mesurés et relus.** Le top-k de l'attention
ne retombait plus sur le CPU par nécessité : `model.rs:3150` interdisait le miroir
VRAM dès que `attn_topk > 0`.

| étape | ce qui est fait | mesure |
|---|---|---|
| 1 · scores | `attn_scores` (déjà là au début du sprint) | écart **1,6–2,3e-7**, **26,7–40×** le CPU (re-mesure sur clés distinctes : l'ancien 1,03e-7 venait d'un banc dégénéré) |
| 2 · sélection | `attn_topk_histo` (4 passes d'octets) + `attn_topk_compte` + `attn_topk_ecrit` | **même ensemble que le CPU** 14/14 lignes, différence symétrique 0 à 4 k / 65 k / 262 k / **1 M** clés ; collecte **0,95 ms** contre 1 653 ms de tri CPU à 1 M (×1 744) |
| 3 · somme | `attn_topk_somme` (softmax sur les k + puits, Σ w·V, indices lus en VRAM) | écart **1,0–4,8e-7** (critère 1e-6) · temps GPU **constant : 0,07 ms** de 4 k à 262 k clés |
| 4 · moteur | branche `DRAVE_GPU_TOPK=1` dans `forward`, repli CPU sur tout refus | PPL **9,4162** contre **9,4167** (CPU) à ctx 2 048 · 13,1355 contre 13,1358 à ctx 8 192 |
| 5 · 1 M | chaîne complète sans relecture des scores | **3,90 ms** pour 14 lignes × 1 M clés, contre 539,9 ms d'attention complète CPU (×138) et 13,2 ms en VRAM — **0,3×** le complet (critère : ≤ 2×) |

⚠️ **Le gain de TEMPS dans le moteur n'est pas encore là**, et c'est mesuré :

| contexte | jetons | attention CPU | attention GPU top-k | balayage |
|---|---|---|---|---|
| 2 048 | 511 | **4,21 ms/jeton** | 7,68 | 18,1 / 20,4 s |
| 8 192 | 511 | **6,35 ms/jeton** | 7,36 | 19,2 / 19,7 s |
| **16 384** | 4 095 | 19,58 ms/jeton | **7,59 ms/jeton** | **203,7 / 155,5 s (−24 %)** |

Le GPU est plat (c'est le but), le CPU croît fortement : **le croisement est entre
8 192 et 16 384 clés**, et à 16 k le déport gagne (attention −61 %, balayage −24 %,
perplexité identique à 2e-5). C'est plus loin que le croisement de l'attention
complète (~4 000), et pour la raison déjà identifiée : la chaîne coûte **8
lancements et 17 transferts par couche et par jeton** (dont 8 copies DtoH
bloquantes). Le prochain sprint doit donc **fusionner** — descente radix, collecte
et somme dans un seul noyau, tampons hôtes réutilisés — pas ajouter un noyau.

**Quatre défauts attrapés, chacun par un moyen différent** — c'est la leçon du
créneau :
1. le **banc était dégénéré** (même clé à toutes les positions : tous les scores
   d'une ligne égaux, donc la descente radix ne choisissait jamais entre deux
   seaux) — trouvé en RELISANT le banc, pas en le faisant échouer ;
2. le **puits était ajouté par chaque fil** dans le noyau 3 alors que chaque fil
   ne tient qu'une somme partielle : dénominateur ×45,7, sortie 55× trop petite à
   k = 1 — trouvé par le BANC en une ligne ;
3. une **relecture adversariale** (sous-agent) a trouvé 7 défauts de plus, dont un
   bloquant : le garde de réallocation de la collecte était piloté par les
   dimensions au lieu des capacités, donc un échec d'allocation au milieu du `||`
   laissait un pointeur 0 pour l'appel suivant. Corrigés, avec en plus une fuite
   VRAM (`kv_assurer`), trois capacités périmées, quatre copies DtoD non
   vérifiées, une boucle infinie latente et un `rep` tronqué ;
4. une SECONDE relecture adversariale, sur le branchement dans le moteur, a
   trouvé **un faux résultat silencieux dans un noyau plus ancien** :
   `attn_kv_recombine` lisait `sinks[warp]` (tête DANS le groupe KV) alors que la
   sortie est écrite par tête GLOBALE — sur gpt-oss, `DRAVE_GPU_KV=1` donnait donc
   à la tête `kvh×rep + w` le puits de la tête `w`, jusqu'à 4,65 logit d'écart
   (facteur 105 sur le drainage). **Mesuré avant/après** : perplexité gpt-oss ctx
   256 `DRAVE_GPU=1 DRAVE_GPU_KV=1` = **17,6531 AVANT** contre **15,1786 APRÈS**
   (référence CPU 15,1757 ; Qwen n'a pas de puits, donc la porte de 19,3885 ne
   pouvait pas le voir). Deux lignes de correction. La relecture a aussi listé 12
   autres points, dont cinq corrigés dans la foulée : garde du noyau 3 testé
   APRÈS sept lancements, couverture de la collecte non vérifiée alors que la
   copie qui le permet est déjà payée, unités de capacité mélangées
   (`sinks_cap`/`out_cap` en éléments d'un côté, en octets de l'autre), compteur
   d'événements incohérent entre les deux chemins, `DRAVE_GPU_TOPK=0` qui
   ACTIVE.

**Un audit de documentation** (second sous-agent) a corrigé quatre chiffres périmés
ou mal sourcés, dont la ligne « 65 536 » du rapport des scores (7,4 ms / 8,9×,
mesurée AVANT le découpage en tranches → 2,36 ms / 26,7×) et le compteur de lignes
Rust (12 171 → **13 168**, un seul chiffre dans tout le dépôt).

Portes du sprint, mesurées sur le binaire final : **Qwen2.5-0.5B Q8_0 ctx 256 =
19,3885** · **gpt-oss-120b MXFP4 ctx 256 = 15,1757** · `cargo test --release` =
**17/17** · `--banc-topk` toujours vert de n = 1 à n = 1 000 000.

### La frontière du cache KV, mesurée en entier

| réglage | octets/élément | % du f32 | écart |
|---|---|---|---|
| clés f16 · valeurs int8 | 3,125 | **39 %** | **+0,018 %** ← le meilleur point |
| clés f32 · valeurs int8 | 5,125 | 64 % | +0,023 % |
| clés f32 · valeurs int4 | 4,625 | 58 % | +0,46 % |
| clés f16 · valeurs int4 | 2,625 | 33 % | +0,61 % |
| int8 · int8 | 2,25 | 28 % | +3,04 % |
| int4 · int4 | 1,25 | 16 % | +364 % |

Réglage recommandé : **`DRAVE_KV_BITS=8 DRAVE_KV_K_F16=1`** — 2,5× plus petit que le
f32 pour deux centièmes de pour cent. Détail et reproduction :
`reports/rapport-placement-bits-kv.md`.

⚠️ **Mais le temps change le conseil** (mesuré au banc à 262 144 clés) : les clés
f16 coûtent **2,3× le temps CPU** des clés f32 (162 contre 70 ms par passe), et le
miroir VRAM — qui ramène l'attention à 1,7 ms par passe — **exige une disposition
homogène**, donc toute variante d'attribution le désactive. Par régime : clés f16
à contexte court ou moyen sur CPU ; **int8/int8 homogène** dès qu'on veut le miroir
ou qu'on est à très long contexte. Et l'aiguille v2 retrouve **9/9** sondes dans
les trois variantes, int8/int8 compris : la tâche est plus robuste que la
perplexité ne le suggère.

### Le mode lot gagne sur les deux tableaux

Chronométré sur 256 jetons, machine au repos : **116,7 ms par jeton** en flux simple
contre **16,6 ms en un seul lot** (7×, par le produit matrice-matrice), et **18×**
sur un lien à 20 ms par message (2,6 s contre 47,6 s). `reports/rapport-prefill-reparti.md`.

### Hygiène et garde-fous ajoutés depuis (13h)

- **`--options-actives`** : un tableau de bord qui imprime, APRÈS toutes les
  affectations, les réglages que le moteur utilise vraiment (niveaux, seuil,
  top-k, fenêtre, lot, cache KV avec sa variante…). C'est la réponse au défaut le
  plus coûteux du dépôt — un drapeau qui ne fait rien. Branché dans les quatre
  modes principaux.
- **Un drapeau inconnu est signalé** : `--keeep 0.05` était avalé en silence.
- **Règle R4 dans le code** : les trois modes qui allouent sur une taille lue dans
  l'en-tête refusent au-delà de 256 Mo — un pair pouvait demander ~15 To.
- **Les tests du protocole** : taille d'en-tête et version verrouillées,
  aller-retour des paires à échappement (écart de 255 compris), refus des corps
  tronqués, aller-retour dense par la vraie mise en trame, refus d'un lot géant.
  Le test de troncature a immédiatement trouvé une garde manquante dans le
  décodeur.
- **Six défauts de la première relecture adversariale corrigés** : compteur de
  listes manquantes aveugle en rejeu par lots, clés de trace incohérentes selon
  `--lot`, pair factice qui ne lisait pas le mode lot, modes sparse ignorés en
  silence avec `--lot > 1`, panique du client sur un refus du pair, `--limit 1` qui
  affichait NaN.
- **Huit de la seconde**, qui attaquait les correctifs eux-mêmes : le tableau de
  bord `--options-actives` s'exécutait AVANT les affectations en perplexité (il
  montrait donc l'état d'avant — pire que rien), la règle R4 ne couvrait pas
  `n_blocs` (16 Gio alloués sur une trame de 83 octets), le décodeur de paires
  allouait sur le `n` du fil (12 Gio avant de dire « tronqué »), une trame forgée
  hors dimension TUAIT le nœud (SIGABRT), l'envoi paniquait encore sur un pair
  fermé, `-keep` (un seul tiret) était avalé, `--flux-forcer` ignoré en inférence,
  `--banc-mla` muet sur la trace.
- **Dix-sept tests** : onze sur le protocole et le plafond — taille d'en-tête et
  version verrouillées, aller-retour des paires à échappement, refus des corps
  tronqués, deux trames FORGÉES envoyées dans une vraie socket (indice hors
  dimension, 100 millions de blocs, cumul au-delà des 256 Mo), quatre sur le mode 4
  (état forgé, deux états, préfixe incohérent, liste vide acceptée en modes 1/2).

### Les prochains chantiers, dans l'ordre

0. **Noyau GPU de top-k** (phase 1.1) : le seul poste de la feuille de route qui
   demande du travail GPU *neuf* ; les deux Quadro sont libres et le cadre existe
   (`gpu/compiler.sh`, `drave_gpu.cu`, sm_75). Vient ensuite le **second GPU**
   (16 Go dormants : cache d'experts MXFP4 et KV à 1 M paginé).
1. ~~Préremplissage par LOTS sur le fil~~ **FAIT** (mode 3), et ~~lot en listes~~
   **FAIT AUSSI** (mode 4 : 1,5 ko par jeton au lieu de 3,5).
2. **Clés du cache KV** : `DRAVE_KV_K_F16=1` (clés en f16, 3,125 octets par
   élément contre 2,25 en int8/int8 et 8 en f32) donne **+0,057 %** à contexte 256
   là où l'int8/int8 coûte +2,15 % — la campagne à 8 192 jetons est en cours ;
   reste à confirmer, puis à choisir la politique par défaut.
3. **Transport** : le mode « blocs » perd encore un peu de fidélité ; l'écart
   **décroît** avec la longueur (13,7 % à 64 jetons, 1,3 % à 1 024) — chercher
   pourquoi il ne descend pas plus vite.
4. Le reste des phases 1 et 2 de `docs/roadmap.md` (noyau GPU de top-k,
   ordonnanceur de placement, flux de poids depuis le NVMe).

---

## 7. Carte du dépôt

```
drave-core/src/
  engine.rs     pool de fils, barrière, accumulateurs, noyau dense int8
  model.rs      chargement, forward, attention, MoE, génération, YaRN, sinks
  list.rs       encodages (PushMat, DenseQ4/6/8), noyaux AVX2, sources empruntées
  gguf.rs       lecteur GGUF, dequantification, vues en place
  tokenizer.rs  BPE byte-level, motifs qwen2 et gpt-4o
  gpu.rs        API pilote CUDA (sans crate), noyaux PTX
  main.rs       modes : inférence, perplexité, plan, tokenize
gpu/drave_gpu.cu + .ptx    noyaux, compilés par clang
tools/ref_logits.cpp         référence llama.cpp : mêmes identifiants, sans BOS
tools/compare_logits.py      comparaison position par position (NLL, top-1, corrélation)
tools/harmony_canonique.py   montage harmony canonique (analysis puis final)
reports/rapport-travail-reel.md      ce que le moteur sait faire, tests réels
reports/rapport-gpt-oss-perplexite.md  les deux bugs de gpt-oss et la référence externe
docs/contexte-long.md                budget 1 M : KV, préremplissage, rotation
docs/convertisseur.md                plan de chargement, résultats négatifs
reports/rapport-passage-a-l-echelle.md   modèle de coût, faisabilité par modèle
journal/                             sessions archivées automatiquement
```

Le journal s'archive à chaque commit (`tools/archive_sessions.py` +
`tools/session_report.py`, crochet git et crontab horaire).

---

## 8. Premier pas suggéré pour la nouvelle session

```bash
# 1. l'état est-il vert ? (Qwen ne doit pas bouger : les corrections de cette
#    session ne touchent que les modèles à biais de sortie et à fenêtre par couche)
cd drave-core && cargo build --release && cargo test --release
./target/release/drave ../models/Qwen2.5-0.5B-Q8_0.gguf --ppl /tmp/ids_qwen.txt \
    --ctx 256 --abits 16 --threads 16 --limit 512 --dense   # attendu 19,3885

# 2. si /tmp a été vidé, régénérer le corpus et les identifiants (§2)

# 3. gpt-oss : le chiffre de contrôle de cette session (≈ 45 s de chargement,
#    ~100 s pour 510 jetons). SANS `DRAVE_GPU` : la variable ouvre le pilote, et le
#    moteur déporte alors tout seul les projections Q8_0 de plus de 8 Mo — le
#    chiffre devient 15,1667 (même calcul, ordre de sommation du noyau GPU).
./target/release/drave /home/stephane/FastNVMe/models/gpt-oss-120b-MXFP4.gguf \
    --ppl /tmp/ids_oss_512.txt --ctx 256 --dense --threads 16 --limit 512  # attendu 15,1757

# 4. puis §6.b : la rotation ne bascule plus qu'au-delà de 1,25 × la longueur
#    d'origine déclarée (5 120 pour gpt-oss) — mesuré, voir docs/contexte-long.md §5.ter

# 5. le calcul réparti (§6bis) : deux nœuds, 12 couches chacun, et le même chiffre
#    des deux côtés. Le nœud moteur doit être lancé AVANT le pilote.
cd ..   # racine du dépôt
(./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf \
     --flux-serveur 45999 --ctx 256 > /tmp/serveur.log 2>&1 &)
sleep 3
./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf \
    --ppl-reparti 127.0.0.1:45999 --couches-locales 12 --limit 40 --ctx 256
# attendu : « écart : 0.00e0 » en mode dense (le transport f32 est exact)

# 6. le contrôle qui attrape les fautes de banc : `tools/pair_factice.py` parle le
#    protocole sans charger de modèle et DIT ce qu'il reçoit (tailles, modes,
#    réglages). C'est lui qui a montré un flux de 919 canaux là où le modèle en a
#    896 — mon compteur divisait par le nombre de jetons notés, pas de flux envoyés.
python3 tools/pair_factice.py 45760 896 &
./drave-core/target/release/drave models/Qwen2.5-0.5B-Q8_0.gguf \
    --ppl-reparti 127.0.0.1:45760 --couches-locales 12 --limit 4 --ctx 256
```
