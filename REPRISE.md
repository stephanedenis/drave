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

`drave-core` est un moteur d'inférence Rust (~5 000 lignes, `std` seul) qui
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
| Qwen2.5-0.5B Q8_0, 6 bits | `--dense --bits-attn 6 --bits-ffn 6 --limit 512` | **19,3045** ← bat l'int8 |
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

1. **Noyau de la tête Q8_0.** Le chemin CPU de la tête par lots est **lié au
   calcul** (5,5 ms/jeton pour Qwen 0.5B, le lot n'y change rien). Deux voies :
   un noyau AVX2 (le déport GPU Q8_0 existe déjà : 15,6 → 6,2 ms/jeton sur
   gpt-oss). C'est le premier consommateur après le FFN.
2. **Second GPU.** 16 Go dorment. Le cache d'experts MXFP4 (13,2 Mo par expert,
   4 608 experts chez gpt-oss) et le KV à 1 M le rempliraient utilement ; il faut
   un second contexte CUDA et une règle de répartition.
3. ~~**Rotation au-delà de 5 120 jetons.**~~ **MESURÉ À 16 k** : RoPE simple
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
| `DRAVE_GPU_EXPERTS=1` | cache LRU des experts MXFP4 en VRAM | inutile sans `DRAVE_GPU` ; budget par `DRAVE_GPU_EXPERTS_GO` (défaut 8) |
| `DRAVE_KV_BITS=8` ou `4` | quantifie le cache KV (défaut f32) | le 4 bits coûte +364 % de perplexité à 8 192 |
| `DRAVE_KV_K_F32=1` | garde les CLÉS en f32 (valeurs quantifiées) | **le bon compromis mesuré** : à 8 192, 75 % de la taille f32 pour +0,02 % de perplexité, contre +3,0 % pour l'int8 complet — l'écart int8 vient des clés à 99 % (`reports/rapport-attribution-kv.md`) |
| `DRAVE_KV_V_F32=1` | garde les VALEURS en f32 | +3,01 % : ne sert à rien, l'erreur ne passe pas par là |
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
**9,5146 des deux côtés à 1 024 jetons** (1 024 flux, texte réel), le banc
réparti prenant le temps du calcul local (19,7 contre 19,4 ms par jeton). Il a
fallu deux corrections dans `Model::forward`, et la première ne suffisait pas :

1. la boucle partait de `0` au lieu de `couche_debut..couche_fin` : le pilote
   calculait les 24 couches, envoyait l'état FINAL, et le pair les recalculait
   toutes par-dessus (`forward_lot` et `forward_mla`, eux, respectaient la plage) ;
2. la norme finale était appliquée DEUX fois (le nœud moteur normait parce que sa
   plage allait jusqu'à la dernière couche, puis le pilote normait). La règle est
   maintenant portée par un drapeau explicite, `flux_brut`.

**Le protocole de flux est en v2** (`docs/format-flux.md`) : en-tête de 39 octets
avec version, mode et **réglages d'activation** — deux nœuds réglés différemment
calculaient deux choses différentes en silence (0,69 d'écart mesuré). Un pair
d'une autre version est refusé en le disant. `--flux-serveur` accepte
`hôte:port` (donc un pair distant) et `docs/colab-reparti.md` est la recette de
la phase 3.4.

**Ce que coûte le transport** (`reports/rapport-transport-liste.md`) :

| | octets par flux | écart local/réparti |
|---|---|---|
| dense f32 | 3 623 | **0,00e0** |
| listes i16, seuil 0,01 | ~2 300 | 2,7e-2 |
| échelles par bloc, seuil 0,01 | 2 268 | 2,7e-2 |

`TCP_NODELAY` a divisé l'attente du pair par six (**97,6 → 16,1 ms** par jeton,
soit 1,01× le calcul local) : le banc réparti prend maintenant le temps du calcul
local, à logits identiques. Le seuil de rentabilité (phase 3.3) est donc une
affaire de latence, pas de débit — moins de 1 Mbit/s par flux de jetons.

**Phase 1.4 attribuée** (`reports/rapport-attribution-kv.md`) : l'écart du cache
KV int8 (+3,0 % à 8 192) vient **entièrement des clés** — clés f32 + valeurs int8
donne +0,023 %, clés int8 + valeurs f32 donne +3,01 %. Réglage utilisable tout de
suite : `DRAVE_KV_BITS=8 DRAVE_KV_K_F32=1` (75 % de la taille f32 pour +0,02 %).

**Une hypothèse réfutée** : transmettre l'entrée NORMÉE au lieu du résidu brut
passait l'écart de 0,00e0 à **5,61e0** en mode dense — la connexion résiduelle a
besoin du résidu lui-même. Drapeau retiré, réfutation écrite.

### Les prochains chantiers, dans l'ordre

1. **Préremplissage par LOTS sur le fil** : le transport est séquentiel (un flux
   par jeton), c'est le vrai bloqueur d'une démonstration Colab utile — la vision
   dit « préremplissage réparti, décodage séquentiel ».
2. **Clés du cache KV** : clés f32 + valeurs int4 (62,5 % de la taille f32), ou
   un meilleur quantificateur de clés (échelle par tête, rotation avant
   quantification) pour passer sous les +0,8 % de llama.cpp.
3. **Transport** : rendre le mode « blocs » meilleur que le dense en toutes
   circonstances (l'écart croît avec la longueur : chercher pourquoi, sans doute
   la dérive du KV de chaque nœud).
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
    --ppl /tmp/ids_oss.txt --ctx 256 --dense --threads 16 --limit 512   # attendu 15,1757

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
