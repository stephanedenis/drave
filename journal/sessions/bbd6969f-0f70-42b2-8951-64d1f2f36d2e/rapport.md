# Session bbd6969f — Continue avec REPRISE.md

| | |
|---|---|
| Identifiant | `bbd6969f-0f70-42b2-8951-64d1f2f36d2e` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-09-28 14:46 |
| Durée | 25.0 h |
| Tours | 6 |
| Messages | 967 |
| Appels d'outils | 968 |
| Fichiers touchés | 35 |
| Commandes | 716 |
| Sous-agents | 1 |
| Commits | 29 |
| Compactages de contexte | 1 |

## Objectifs déclarés

- **create** — Réaliser les 8 chantiers restants du projet qtrinet-core dans l'ordre : (1) protocole de perplexité longue --depuis/--stride, (2) trancher le seuil de rotation YaRN avec ce protocole, (3) KV int8 puis int4 mesurés sur Qwen 0.5B à ctx 8192 contre llama.cpp, (4) préremplissage par lots (GEMM par tranc
… [374 caractères tronqués]

## 1. Ce qui a été demandé

**Tour 1** — continue avec REPRISE.md

**Tour 2** — prochaine étape?

**Tour 3** — que reste-t-il à faire

**Tour 4** — fais les 8 dans l'ordre

**Tour 5** — <goal_round> Objective: "Réaliser les 8 chantiers restants du projet qtrinet-core dans l'ordre : (1) protocole de perplexité longue --depuis/--stride, (2) trancher le seuil de rotation YaRN avec ce protocole, (3) KV int8 puis int4 mesurés sur Qwen 0.5B à ctx 8192 contre llama.cpp, (4) préremplissage par lots (GEMM par tranches), (5) échelles par bloc pour DenseQ8, (6) refactorisation des boucles C … [842 caractères tronqués]

**Tour 6** — <goal_round> Objective: "Réaliser les 8 chantiers restants du projet qtrinet-core dans l'ordre : (1) protocole de perplexité longue --depuis/--stride, (2) trancher le seuil de rotation YaRN avec ce protocole, (3) KV int8 puis int4 mesurés sur Qwen 0.5B à ctx 8192 contre llama.cpp, (4) préremplissage par lots (GEMM par tranches), (5) échelles par bloc pour DenseQ8, (6) refactorisation des boucles C … [842 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — continue avec REPRISE.md

*317 appels d'outils.* Actions notables :

- bash — List repository root files
- glob
- read
- bash — Inspect git log, status, tmp corpus, models
- bash — List qtrinet-core contents
- bash — Build release and run tests
- grep
- job_output
- bash — Run reference perplexity check
- bash — Read tokenizer head
- bash — Locate forward and positional logic
- bash — Check memory and cpu
- write `/tmp/gguf_meta.py`
- bash — Dump gpt-oss metadata and harmony tokens
- … et 244 autres

**Synthèse produite :**

Reprise terminée. Voici ce que la session a établi — tout est mesuré, commité, et `REPRISE.md` est à jour.

\## Les deux bugs réels de gpt-oss (§6.a)

| | avant | après |
|---|---|---|
| `attn_output.bias` ignoré (gpt-oss a un biais sur Q, K, V **et O**) — 63 jetons | 39,80 | **20,84** |
| fenêtre glissante sur les 36 couches au lieu d'une sur deux — 511 jetons | 129,9 | **15,08** |

Le motif de fenêtre est vérifié dans les sources : `layer_types` de gpt-oss alterne `sliding_attention`/`full_attention`, et llama.cpp pose `set_swa_pattern(2)`. Les deux extrêmes sont pires que le motif réel du modèle : 17,14 (toutes fenêtrées) et 26,15 (aucune). Un troisième bug latent — les puits appris absents du softmax des couches pleines — est corrigé, **effet mesuré nul** sur gpt-oss (le chemin groupé les comptait déjà).

\## La prémisse « devrait valoir ~6 » était fausse

Nouvel outil `tools/ref_logits` : llama.cpp évalue **exactement les mêmes identifiants, sans BOS**.

| mêmes prédictions | llama.cpp | qtrinet-core |
|---|---|---|
| 63 jetons, YaRN | 38,37 | 41,11 |
| 511 jetons, YaRN | 169,67 | 174,34 |

Corrélation des logits **0,999976**, **top-1 identique partout**, |ΔNLL| médian 0,076 (notre int15 contre son f32). Notre moteur n'était pas le maillon faible — il fait même mieux, parce qu'il sait éteindre YaRN, qui coûte **×9** ici (18,58 contre 174,34). Ce n'est pas un bug : HF, llama.cpp et l'implémentation officielle d'OpenAI appliquent le même YaRN statique (vérifié dans les trois sources).

\## Hypothèse harmony : réfutée, avec le mécanisme

Le modèle **exige son canal `analysis`** : après `<|start|>assistant<|channel|>`, p(analysis) = 0,9999 contre p(final) = 0,0001. Meilleur montage canonique (système officiel + `analysis` puis `final`) : **26,0** — contre **13,7** en brut pour le même texte. Le format rend le texte *moins* prévisible, pas plus.

\## Effet de bord utile

`Gguf::open_meta` ne lit plus que l'en-tête : `--tokenize` sur gpt-oss passe de ~60 s à **0,385 s** (identifiants inchangés) et chaque `--ppl` économise une lecture des 62 Go. Non-régression Qwen : **19,3885** exactement, tests 3/3.

Reste ouvert et documenté : le YaRN « à retardement » (au-delà de 4 096), protocole et coût dans `reports/rapport-gpt-oss-perplexite.md`.

### Tour 2 — prochaine étape?

*114 appels d'outils.* Actions notables :

- ask_user_question
- todo_write
- bash — llama.cpp reference on Qwen 512 tokens
- bash — Our Qwen logits at three activation precisions
- bash — Analyse the gpt-oss logit gap distribution
- read
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/qtrinet-core/src/model.rs`
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/qtrinet-core/src/model.rs`
- bash — Build and check rotation trace on Qwen
- bash — Build long corpus and count its tokens
- write `/tmp/bascule_yarn.sh`
- bash — Launch the rotation boundary series
- bash — Collect hardware facts for the 1M plan
- bash — Read run_plan implementation
- … et 96 autres

**Synthèse produite :**

⏵ YaRN à retardement livré ; la mesure à 8 192 tourne. Voici l'état

**Livré et commité**

1. **YaRN à retardement** (`[config] rotation` en dit la raison à chaque chargement) : RoPE simple tant que `--ctx` tient dans `rope.scaling.original_context_length` (4 096), **interpolation seule** au-delà — décision **par séquence**, pas par position, parce que la structure de position relative ne survit que si toutes les clés partagent le même jeu de fréquences. `QT_YARN=1` = YaRN complet des références, `QT_YARN_NON=1` / `--sans-yarn` = jamais, `QT_YARN_MSCALE=0/1` = température seule.

2. **Le résultat qui change la donne : la moitié nuisible de YaRN, c'est la température.**

| longueur | RoPE simple | YaRN **sans** mscale | YaRN complet |
|---|---|---|---|
| 512 | **18,58** | 19,65 | 174,34 |
| 1 024 | **46,94** | 71,35 | 417,65 |
| 2 048 | **121,75** | 192,63 | 722,56 |
| 4 096 | **170,78** | 400,13 | — |
| 4 608 | — | 476,09 | 1 105,20 |

Retirer `mscale = 1 + 0,1·ln f` divise la perplexité par **8,9 / 5,9 / 3,8**. L'interpolation des basses fréquences, elle, ne coûte presque rien. HF, llama.cpp et l'implémentation officielle d'OpenAI appliquent pourtant la température telle quelle — et notre moteur les reproduit au chiffre près quand on la garde. D'où le nouveau défaut : simple sous 4 096, interpolation seule au-delà.

3. **La dégradation avec la longueur n'est pas un bug du moteur** : llama.cpp, mêmes 2 048 identifiants, un seul lot, YaRN déclaré → **714,83** contre **722,56** chez nous (1,1 %). Le `--ppl-profil` ajouté pour ça montre deux causes superposées : le **contenu** (une même tranche vaut 13,94 en tête et 59,36 prise plus loin mais présentée en position 0) et la **position** (~×7 de plus à sa place réelle).

4. **Plan 1 M** : `docs/contexte-long.md` + `--plan --ctx N` qui chiffre tout. Les trois murs : **préremplissage séquentiel** (4,5 h à 32 k, 31 h à 128 k, **1 234 h à 1 M** → chantier n° 1, il faut le préremplissage par lots) ; **bande passante du KV** (77 Go relus par jeton à 1 M en f32, 9,7 Go en int4 — 13 ms depuis les deux GPU, et le KV int4 à 1 M tient dans **un seul RTX 5000**) ; **portée de la rotation** (×32 couvre 131 072, 1 M demanderait ×256, soit huit fois ce que le modèle a vu).

**En cours** (résultats dans `/tmp/audela_4096.log` d'ici ~2 h) : RoPE simple et interpolation seule à **8 192** — c'est la mesure qui tranche le seuil de bascule, puisque le simple gagne encore à 4 096. Restent aussi le test de génération à refaire avec `
… [256 caractères tronqués]

### Tour 3 — que reste-t-il à faire

*4 appels d'outils.* Actions notables :

- bash — Check running measurements and repo state
- bash — Read the 8192 results
- bash — Inspect corpus content in hard and easy regions
- bash — Launch content-vs-context decomposition run

**Synthèse produite :**

⏵ Point complet : ce qui tourne, ce que la mesure vient de changer, et l'ordre de travail

**En cours** (~30 min) : la déconfusion contenu/contexte — ctx 512 sur 8 192 jetons, PPL par fenêtre → `/tmp/contexte_ou_contenu.log`.

**Le résultat de 8 192 vient de tomber, et il change la lecture** : RoPE simple = **48,7** (meilleur qu'à 4 096, où c'était 170,8), interpolation seule = **835,2**. Le profil par profondeur explique pourquoi : les tranches 4 608-8 191 tournent autour de **10** alors que les tranches 512-4 095 montent jusqu'à 542. Or le corpus est du même genre de prose partout — donc **le protocole actuel confond le contenu et la longueur** : à `--ctx 8192` on ne score pas les mêmes jetons qu'à `--ctx 512`. Tant que ce n'est pas corrigé, aucune courbe « par longueur » n'est interprétable.

\## Ce qu'il reste, par ordre de valeur

**1. Protocole de perplexité longue** (`--depuis N`, ou un `--stride` comme llama-perplexity) — noter **les mêmes jetons** avec des contextes de longueurs différentes. ~30 lignes. C'est le préalable à toute conclusion sur le seuil de rotation, et ça invalide une partie de ce qu'on vient de mesurer.

**2. Trancher le seuil de rotation** avec ce protocole (simple contre interpolation seule, mêmes jetons, 512 → 8 192). Indice actuel : le simple gagne partout, l'interpolation se dégrade régulièrement — le défaut (bascule à 4 096) est donc peut-être à inverser en « simple partout » pour gpt-oss.

**3. KV int8 puis int4** (E2/E3 du plan 1 M) — ÷4 puis ÷8 sur le cache. Banc d'essai : Qwen2.5-0.5B à `--ctx 8192`, 5 min par passe, écart de perplexité à mesurer contre llama.cpp (`--ctk q8_0`). C'est ce qui fait tenir 1 M en mémoire.

**4. Préremplissage par lots** (E1) — le mur n° 1 : 4,5 h à 32 k, 31 h à 128 k, **1 234 h à 1 M** en séquentiel. Un noyau GEMM par tranches débloque tout le contexte long *et* le temps de premier jeton. Gros chantier, mais rien de long ne se fait sans lui.

**5. Échelles par bloc pour `DenseQ8`** — l'écart résiduel avec llama.cpp (|ΔNLL| médian 0,076) vient de là, et ça tranche la question « 6 bits contre int8 par bloc » à octets égaux.

**6. Refactoriser les boucles CLI** (3 modes → 1) — quatrième bug de la même classe rencontré cette session (`--attn-window`/`--attn-sinks` jamais appliqués en inférence).

**7. Noyaux GPU** — une warp par ligne puis les formats 4 bits (Q4_K/Q6_K/MXFP4) : toute la famille Qwen est en Q4_K/Q6_K, donc aujourd'hui rien de la leur n'est déportable. Le plus gros levier de débit
… [595 caractères tronqués]

### Tour 4 — fais les 8 dans l'ordre

*168 appels d'outils.* Actions notables :

- create_goal
- todo_write
- read
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/qtrinet-core/src/main.rs`
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/qtrinet-core/src/main.rs`
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/qtrinet-core/src/main.rs`
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/qtrinet-core/src/main.rs`
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/qtrinet-core/src/main.rs`
- bash — Build and check no regression with depuis=0
- bash — Validate depuis semantics against known window value
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/qtrinet-core/src/main.rs`
- bash — Validate overlapping windows and non-regression
- write `/tmp/seuil_rotation.sh`
- bash — Launch rotation threshold measurement
- … et 146 autres

**Synthèse produite :**

⏵ Analyse PowerInfer prête ; le profil d'experts gpt-oss est en file derrière la série

**Ce que fait PowerInfer** (dépôt SJTU-IPADS, miroir `Tiiny-AI`) : il exploite la **localité d'activation** — la distribution des neurones suit une loi de puissance, donc peu de neurones sont « chauds » (actifs presque toujours) et beaucoup sont « froids » (dépendants de l'entrée). Ils en tirent un moteur hybride : **les neurones chauds résident sur le GPU, les froids sont calculés sur le CPU**, plus un **prédicteur** qui devine l'ensemble actif à l'avance pour précharger, et des **opérateurs creux conscients des neurones**. Leur modèle TurboSparse (90 % de creux) est *entraîné* ainsi, précisément parce qu'imposer la parcimonie à l'inférence coûte cher.

**Ce que notre moteur a déjà, et qui est de la même famille**
- Le chemin **par listes d'événements** *est* un opérateur creux conscient des neurones : il n'itère que sur les sources actives, avec bascule mesurée vers le produit dense à **22 % de densité** (`seuil_push`).
- La parcimonie imposable (`--act-topk`, `--act-thresh`) avec sa courbe de qualité — et notre conclusion recoupe la leur : la parcimonie imposée coûte, elle se gagne à l'entraînement.
- Un capteur hebbien et, depuis aujourd'hui, un **profileur de neurones** (`--profil-neurones`, sortie `--neurones-sortie`).

**Leur idée centrale, mesurée chez nous** (Qwen2.5-0.5B, 512 jetons, seuil 5 % du max) :

| mesure | valeur |
|---|---|
| densité d'activation | **17,9 %** des neurones par jeton (82 % ne font rien) |
| concentration | les 10 % de neurones les plus lourds portent **33 %** de la magnitude |
| neurones **toujours** chauds (> 90 % du temps) | **0,08 %** |
| neurones chauds (> 50 % du temps) | 2,8 % |
| dispersion entre couches | tirs de 173 à 1 579 par jeton (×9) |

**Le verdict honnête** : leur mécanisme de *préchargement statique* repose sur un ensemble chaud **stable**, et sur un modèle SiLU comme Qwen2.5 cet ensemble est minuscule (0,08 %) — la localité existe mais elle est surtout **dynamique**, pas statique. C'est exactement pourquoi leurs gains spectaculaires sont sur des modèles ReLU/TurboSparse, entraînés pour ça. Ce qui se transpose vraiment chez nous :

1. **Le placement par neurone/expert piloté par le profil** — et pour gpt-oss, la vraie question n'est pas les neurones du FFN mais **les experts** : 4 sur 128 par jeton. Je viens d'ajouter ce comptage : le profil d'experts gpt-oss tourne (résultats dans `/tmp/profil_experts.log`). Si un pet
… [911 caractères tronqués]

### Tour 5 — <goal_round> Objective: "Réaliser les 8 chantiers restants du projet qtrinet-core dans l'ordre : (1) protocole de perple … [1122 caractères tronqués]

*124 appels d'outils.* Actions notables :

- bash — Check rotation series and expert profile
- bash — End-to-end batched prefill correctness and time
- bash — Fix the batched projection buffers
- bash — Re-test batched prefill correctness
- bash — Hoist batch buffers out of the layer loop
- bash — Fix closure signature and measure again
- bash — Commit item 4 correctness fixes
- bash — Wait for the rotation series progress
- bash — Fix the grep pattern and relaunch the series
- bash — Verify the script state after the kill
- bash — Clean engines and find the script process
- bash — Fix the grep pattern and relaunch cleanly
- bash — Read the MXFP4 CPU kernel for the layout
- bash — Find the MXFP4 scalar dot path
- … et 109 autres

**Synthèse produite :**

⏵ Tour terminé : les huit chantiers ont avancé, la non-régression tient (19,3885)

**Ce que ce tour a livré** (12 commits, tous vérifiés)

| # | chantier | état | mesure |
|---|---|---|---|
| 1 | protocole longue | ✅ | `--depuis` : `--depuis 256 --ctx 256` redonne exactement la fenêtre historique (21,565) |
| 2 | seuil de rotation | ✅ | apparié, mêmes 512 jetons : RoPE simple **39,5 / 49,8 / 49,9 / 298,6** contre interpolation 42,1 / 82,0 / 82,2 / 578,9 → le simple gagne partout |
| 3 | KV int8/int4 | ✅ | **échelles par bloc de 32** : int8 **+1,5 %** (512 j) et **+3,4 %** (4 591 j) — était +7,1 % et +5,2 % ; int4 +219 %/+287 % ; llama.cpp : +0,8 %/+494 % |
| 4 | préremplissage par lots | ✅ | GEMM int8 **et** 4 bits + regroupement des experts ; juste (13,1359 vs 13,1368) ; gain **−3 %** attribué : projections ÷2, mais attention non groupée ×2,2 et tête restée par jeton |
| 5 | échelles par bloc `DenseQ8` | ✅ | hypothèse **réfutée** : 23,696 contre 23,612 ; l'avantage du 6 bits est son coût (25 % d'octets en moins) |
| 6 | boucles CLI | ✅ | `Options` + `analyser` ; **3 drapeaux de plus** trouvés ignorés et un bug de pas de lecture (qui masquait `--ctx`/`--threads`) |
| 7 | noyaux GPU | ✅ | warp : tête **1,6 ms** contre 7,3 CPU ; MXFP4 **0,00e0** d'écart (bit à bit) ; Q4_K 4e-7 ; reste Q6_K |
| 8 | plan 1 M | 🔄 | E1/E2/E3 faits ; **attention creuse : top-256 améliore la perplexité de 21 %** (234,9 contre 298,6) tandis qu'élargir la fenêtre la détruit (×11) ; E4/E5 à implémenter ; MLA et vision non testables ici |

**Trois bogues de plus corrigés au passage** : le biais de descente des experts (latent, effet nul sur le 30B), le tampon de sortie dimensionné sur `h` au lieu de `n_têtes×dim`, et l'empaquetage 4 bits du KV. Plus une leçon de méthode : un remplacement de texte qui échoue en silence a produit une perplexité de 399 074 — un `assert` sur le motif l'aurait évité, et c'est désormais ce que je fais.

**L'étude PowerInfer** est dans `reports/rapport-localite-activation.md` : la localité existe (82 % des neurones inactifs par jeton) mais l'ensemble *toujours* chaud est minuscule (0,08 %) → leur préchargement statique ne paierait pas sur un modèle SiLU ; ce qu'on garde, c'est le placement **par expert** et un cache à éviction.

**Reste ouvert** (l'objectif continue) : attention groupée dans le chemin par lots puis **la tête en GEMM** (les deux corrections chiffrées du chantier 4), Q6_K, puis E4 (KV déporté GPU) et E5 (attention creuse implémentée) ; MLA et 
… [55 caractères tronqués]

### Tour 6 — <goal_round> Objective: "Réaliser les 8 chantiers restants du projet qtrinet-core dans l'ordre : (1) protocole de perple … [1122 caractères tronqués]

*241 appels d'outils.* Actions notables :

- bash — Check the starting state of round 2
- bash — Locate the batched attention loop
- bash — Read the batched per-head attention
- bash — Read the head computation
- bash — Group the batched attention and measure
- bash — Implement the batched head
- bash — Fix the SparseVec path
- bash — Measure the batched head
- bash — Check the batched MoE path with the new attention and head
- bash — See the gpt-oss lot 128 failure
- bash — Inspect the panicking line
- bash — Bisect the failing batch size
- bash — Add guards and rerun lot 128
- bash — Read dot16's fallback path
- … et 185 autres

**Synthèse produite :**

⏵ Verdict tranché : à 5 120 jetons, RoPE simple 9,70 contre 1 269 en interpolation

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/tmp/gguf_meta.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/qtrinet-core/src/model.rs` | 0 | 15 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/qtrinet-core/src/main.rs` | 0 | 43 |
| `/tmp/mesures_oss.sh` | 2 | 0 |
| `/tmp/mesures_oss2.sh` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/compare_logits.py` | 1 | 0 |
| `/tmp/mesures_oss3.sh` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/ref_logits.cpp` | 0 | 3 |
| `/tmp/mesures_oss4.sh` | 2 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-gpt-oss-perplexite.md` | 1 | 4 |
| `/tmp/controles_oss.sh` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/REPRISE.md` | 0 | 11 |
| `/tmp/controles2_oss.sh` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/harmony_canonique.py` | 1 | 1 |
| `/tmp/controles3_oss.sh` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/qtrinet-core/src/gguf.rs` | 0 | 2 |
| `/tmp/controles4_oss.sh` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/.gitignore` | 0 | 2 |
| `/tmp/bascule_yarn.sh` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/contexte-long.md` | 1 | 3 |
| `/tmp/croisement_yarn.sh` | 2 | 0 |
| `/tmp/profil_profondeur.sh` | 1 | 0 |
| `/tmp/contenu_ou_profondeur.sh` | 1 | 0 |
| `/tmp/ref_long.sh` | 1 | 0 |
| `/tmp/mscale_yarn.sh` | 1 | 0 |
| `/tmp/ref2048.sh` | 1 | 0 |
| `/tmp/interp_long.sh` | 1 | 0 |
| `/tmp/audela_4096.sh` | 1 | 0 |
| `/tmp/seuil_rotation.sh` | 1 | 0 |
| `/tmp/mesures_finales.sh` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-localite-activation.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aiguille.py` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-prefill-par-lots.md` | 1 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/qtrinet-core/src/engine.rs` | 0 | 4 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/qtrinet-core/gpu/qtrinet_gpu.cu` | 0 | 1 |

### Sous-agents lancés

- tour 1 — Harness logits llama.cpp

### Commandes exécutées (échantillon)

- **T1** List repository root files
- **T1** Inspect git log, status, tmp corpus, models
- **T1** List qtrinet-core contents
- **T1** Build release and run tests
- **T1** Run reference perplexity check
- **T1** Read tokenizer head
- **T1** Locate forward and positional logic
- **T1** Check memory and cpu
- **T1** Dump gpt-oss metadata and harmony tokens
- **T1** Filter metadata and harmony token ids
- **T1** Find gpt-oss FFN activation code
- **T1** List gpt-oss tensor names and biases
- **T1** Check for llama.cpp tools
- **T1** Read Proj::load implementation
- **T1** Read charger_moe implementation
- **T1** Check bias application in MoE and Proj
- **T1** Fetch HF gpt-oss reference implementation
- **T1** Inspect llama.cpp SWA pattern semantics
- **T1** Read SWA pattern and gpt-oss arch handling
- **T1** Locate gpt-oss arch implementation in llama.cpp
- **T1** Inspect openai-moe model implementation
- **T1** Read openai-moe.cpp head
- **T1** Check Gguf::cfg key resolution
- **T1** Find remaining window usages
- **T1** Dump gpt-oss control tokens
- **T1** Check build_tokenizer signature
- **T1** Locate inference-mode window assignment
- **T1** Find both model load sites
- **T1** Verify edit and build
- **T1** Validate reference PPL and text path
- **T1** Run gpt-oss PPL 64 tokens
- **T1** Check llama-perplexity stride semantics
- **T1** Locate perplexity source and version
- **T1** Read perplexity windowing logic
- **T1** Compare YaRN implementation with HF formula
- **T1** Check ppl-stride default
- **T1** Check available llama.cpp binaries
- **T1** Check tokenize binary and memory
- **T1** Check llama-tokenize usage
- **T1** Tokenize corpus with llama.cpp o200k
- … et 676 autres

## 4. Mesures et résultats marquants

- **T1** `// scalaire dense (pull). Le croisement mesuré est à 10 %.`
- **T1** `part de l'attention dans le flux d'événements : 100.0 %`
- **T1** `255 tokens notés — perplexité cumulée 17.431  (31.9 tok/s)`
- **T1** `510 tokens notés — perplexité cumulée 19.388  (31.8 tok/s)`
- **T1** `=== perplexité 19.3885 sur 510 tokens (0 événements, 16.1 s) ===`
- **T1** `0  1.00000000e+00  1.00000000e+00    0.000 %`
- **T1** `1  6.89044306e-01  6.89044306e-01    0.000 %`
- **T1** `2  4.74782055e-01  4.74782055e-01    0.000 %`
- **T1** `3  3.27145872e-01  3.27145872e-01    0.000 %`
- **T1** `4  2.25418000e-01  2.25418000e-01    0.000 %`
- **T1** `5  1.55322989e-01  1.55322989e-01    0.000 %`
- **T1** `6  1.07024421e-01  1.07024421e-01    0.000 %`
- **T1** `7  7.37445682e-02  7.37445682e-02    0.000 %`
- **T1** `8  5.08132748e-02  5.08132748e-02    0.000 %`
- **T1** `9  3.17056962e-02  3.16207523e-02    0.268 %`
- **T1** `10  1.93350011e-02  1.94509675e-02    0.600 %`
- **T1** `11  1.15920493e-02  1.17921911e-02    1.727 %`
- **T1** `12  6.79495949e-03  7.01571391e-03    3.249 %`
- **T1** `13  3.86035932e-03  4.06955471e-03    5.419 %`
- **T1** `14  2.09379238e-03  2.27727194e-03    8.763 %`
- **T1** `15  1.05260210e-03  1.20613097e-03   14.586 %`
- **T1** `16  4.56483919e-04  5.80947502e-04   27.266 %`
- **T1** `17  1.29318701e-04  2.27947796e-04   76.268 %`
- **T1** `18  3.83088124e-05  3.83088124e-05    0.000 %`
- **T1** `19  2.63964690e-05  2.63964690e-05    0.000 %`
- **T1** `20  1.81883367e-05  1.81883367e-05    0.000 %`
- **T1** `21  1.25325698e-05  1.25325698e-05    0.000 %`
- **T1** `22  8.63549588e-06  8.63549588e-06    0.000 %`
- **T1** `23  5.95023926e-06  5.95023926e-06    0.000 %`
- **T1** `24  4.09997848e-06  4.09997848e-06    0.000 %`
- **T1** `25  2.82506683e-06  2.82506683e-06    0.000 %`
- **T1** `26  1.94659621e-06  1.94659621e-06    0.000 %`
- **T1** `27  1.34129104e-06  1.34129104e-06    0.000 %`
- **T1** `28  9.24208950e-07  9.24208950e-07    0.000 %`
- **T1** `29  6.36820915e-07  6.36820915e-07    0.000 %`
- **T1** `30  4.38797825e-07  4.38797825e-07    0.000 %`
- **T1** `31  3.02351143e-07  3.02351143e-07    0.000 %`
- **T1** `63 tokens notés — perplexité cumulée 20.836  (5.2 tok/s)`
- **T1** `=== perplexité 20.8361 sur 63 tokens (0 événements, 12.2 s) ===`
- **T1** `63 tokens notés — perplexité cumulée 41.114  (5.0 tok/s)`
- **T1** `=== perplexité 41.1140 sur 63 tokens (0 événements, 12.5 s) ===`
- **T1** `[timed out after 600000ms]`
- **T1** `238 tokens notés — perplexité cumulée 144.168  (4.9 tok/s)`
- **T1** `357 tokens notés — perplexité cumulée 320.482  (4.9 tok/s)`
- **T1** `511 tokens notés — perplexité cumulée 247.031  (4.9 tok/s)`
- **T1** `=== perplexité 247.0308 sur 511 tokens (0 événements, 104.5 s) ===`
- **T1** `255 tokens notés — perplexité cumulée 13.715  (5.0 tok/s)`
- **T1** `509 tokens notés — perplexité cumulée 15.076  (5.0 tok/s)`
- **T1** `=== perplexité 15.0763 sur 509 tokens (0 événements, 102.5 s) ===`
- **T1** `119 tokens notés — perplexité cumulée 940.867  (4.9 tok/s)`
- **T1** `(**5,62 tok/s**), premier jeton en 166 ms.`
- **T1** `/// deux architectures se croisent à 10 % de densité ; on bascule un peu`
- **T1** `226 tokens notés — perplexité cumulée 3940.363  (4.6 tok/s)  [fenêtre 1 : 226 notés, PPL 3940.363]`
- **T1** `452 tokens notés — perplexité cumulée 3476.367  (4.6 tok/s)  [fenêtre 2 : 226 notés, PPL 3067.009]`
- **T1** `511 tokens notés — perplexité cumulée 3431.623  (4.5 tok/s)  [fenêtre 3 : 59 notés, PPL 3107.404]`
- **T1** `=== perplexité 3431.6228 sur 511 tokens (0 événements, 113.9 s) ===`
- **T1** `230 tokens notés — perplexité cumulée 5559.111  (4.7 tok/s)  [fenêtre 1 : 230 notés, PPL 5559.111]`
- **T1** `460 tokens notés — perplexité cumulée 10738.682  (4.6 tok/s)  [fenêtre 2 : 230 notés, PPL 20744.198]`
- **T1** `511 tokens notés — perplexité cumulée 8462.826  (4.6 tok/s)  [fenêtre 3 : 51 notés, PPL 987.567]`
- **T1** `=== perplexité 8462.8255 sur 511 tokens (0 événements, 111.7 s) ===`
- **T1** `230 tokens notés — perplexité cumulée 643.509  (4.8 tok/s)  [fenêtre 1 : 230 notés, PPL 643.509]`
- **T1** `460 tokens notés — perplexité cumulée 549.601  (4.9 tok/s)  [fenêtre 2 : 230 notés, PPL 469.398]`
- **T1** `511 tokens notés — perplexité cumulée 442.825  (4.8 tok/s)  [fenêtre 3 : 51 notés, PPL 63.104]`
- **T1** `=== perplexité 442.8254 sur 511 tokens (0 événements, 106.0 s) ===`
- **T1** `255 tokens notés — perplexité cumulée 14.483  (5.1 tok/s)  [fenêtre 1 : 255 notés, PPL 14.483]`
- **T1** `509 tokens notés — perplexité cumulée 17.141  (5.2 tok/s)  [fenêtre 2 : 254 notés, PPL 20.301]`
- **T1** `=== perplexité 17.1414 sur 509 tokens (0 événements, 98.5 s) ===`
- **T1** `255 tokens notés — perplexité cumulée 24.579  (5.2 tok/s)  [fenêtre 1 : 255 notés, PPL 24.579]`
- **T1** `509 tokens notés — perplexité cumulée 26.154  (5.2 tok/s)  [fenêtre 2 : 254 notés, PPL 27.837]`
- **T1** `=== perplexité 26.1538 sur 509 tokens (0 événements, 98.8 s) ===`
- **T1** `prompt  : 5 tokens en 0.815 s  (6.1 tok/s, TTFT 163.0 ms)`
- **T1** `généré  : 16 tokens en 2.989 s  (5.35 tok/s)`
- **T1** `prompt  : 5 tokens en 0.842 s  (5.9 tok/s, TTFT 168.4 ms)`
- **T1** `généré  : 16 tokens en 3.073 s  (5.21 tok/s)`
- **T1** `1 tokens notés — perplexité cumulée 14469095357.465  (0.2 tok/s)`
- **T1** `=== perplexité 14469095357.4649 sur 1 tokens (0 événements, 4.2 s) ===`
- **T1** `89 tokens notés — perplexité cumulée 25.009  (4.2 tok/s)`
- **T1** `=== perplexité 25.0091 sur 89 tokens (0 événements, 21.3 s) ===`
- **T1** `229 tokens notés — perplexité cumulée 13.657  (5.2 tok/s)`
- **T1** `=== perplexité 13.6567 sur 229 tokens (0 événements, 44.1 s) ===`
- **T1** `254 tokens notés — perplexité cumulée 203.115  (5.2 tok/s)`
- **T1** `=== perplexité 203.1151 sur 254 tokens (0 événements, 49.2 s) ===`
- **T1** `13 tokens notés — perplexité cumulée 14.626  (2.0 tok/s)`
- **T1** `=== perplexité 14.6260 sur 13 tokens (0 événements, 6.5 s) ===`
- **T1** `19 tokens notés — perplexité cumulée 5.721  (4.9 tok/s)`
- **T1** `=== perplexité 5.7209 sur 19 tokens (0 événements, 3.8 s) ===`
- **T1** `89 tokens notés — perplexité cumulée 677321.831  (2.0 tok/s)`
- **T1** `=== perplexité 677321.8310 sur 89 tokens (0 événements, 44.5 s) ===`
- **T1** `316 tokens notés — perplexité cumulée 258.640  (5.2 tok/s)`
- **T1** `=== perplexité 258.6401 sur 316 tokens (0 événements, 61.3 s) ===`
- **T1** `=== perplexité 258.6401 sur 316 tokens (0 événements, 61.6 s) ===`
- **T1** `=== perplexité 1880.7184 sur 301 tokens (0 événements, 57.6 s) ===`
- **T1** `89 tokens notés — perplexité cumulée 677321.831  (1.9 tok/s)`
- **T1** `=== perplexité 677321.8310 sur 89 tokens (0 événements, 46.7 s) ===`
- **T1** `255 tokens notés — perplexité cumulée 17.431  (31.8 tok/s)  [fenêtre 1 : 255 notés, PPL 17.431]`
- **T1** `510 tokens notés — perplexité cumulée 19.388  (31.8 tok/s)  [fenêtre 2 : 255 notés, PPL 21.565]`
- **T1** `=== perplexité 19.3885 sur 510 tokens (0 événements, 16.0 s) ===`
- **T1** `à      25.8 Go/s (NVLink) :   67.76 tok/s`
- **T1** `à     380.0 Go/s (GPU local) :  998.76 tok/s`
- **T1** `255 tokens notés — perplexité cumulée 13.715  (5.3 tok/s)  [fenêtre 1 : 255 notés, PPL 13.715]`
- **T1** `510 tokens notés — perplexité cumulée 15.176  (5.2 tok/s)  [fenêtre 2 : 255 notés, PPL 16.792]`
- **T1** `=== perplexité 15.1757 sur 510 tokens (0 événements, 97.3 s) ===`
- **T2** `511 tokens notés — perplexité cumulée 13.287  (28.7 tok/s)`
- **T2** `logits exportés : /tmp/nous_qwen_512_a8.bin — 511 positions × 151936 valeurs`
- **T2** `=== perplexité 13.2872 sur 511 tokens (0 événements, 17.8 s) ===`
- **T2** `511 tokens notés — perplexité cumulée 13.135  (30.6 tok/s)`
- **T2** `logits exportés : /tmp/nous_qwen_512_a12.bin — 511 positions × 151936 valeurs`
- **T2** `=== perplexité 13.1348 sur 511 tokens (0 événements, 16.7 s) ===`
- **T2** `511 tokens notés — perplexité cumulée 13.137  (30.2 tok/s)`
- **T2** `logits exportés : /tmp/nous_qwen_512_a16.bin — 511 positions × 151936 valeurs`
- **T2** `=== perplexité 13.1368 sur 511 tokens (0 événements, 16.9 s) ===`
- **T2** `255 tokens notés — perplexité cumulée 17.431  (32.5 tok/s)  [fenêtre 1 : 255 notés, PPL 17.431]`
- **T2** `510 tokens notés — perplexité cumulée 19.388  (32.5 tok/s)  [fenêtre 2 : 255 notés, PPL 21.565]`
- **T2** `=== perplexité 19.3885 sur 510 tokens (0 événements, 15.7 s) ===`
- **T2** `/dev/nvme0n1p2           828G  268G  561G  33% /home/stephane/FastNVMe`
- **T2** `/dev/mapper/system-root   11T  6,2T  4,7T  57% /home/stephane/Data13TB`
- **T2** `else { "GPU (PCIe 6,5 Go/s)" };`
- **T2** `// Mesuré sur le 30B-A3B : les tranches d'experts sont lues à 8 Go/s,`
- **T2** `// pas 20 — dix-huit mille tranches de 900 Ko dispersées sur 18 Go`
- **T2** `println!("  à       8.0 Go/s (MoE épars, mesuré) : {:>7.2} tok/s",`
- … (tronqué)

## 5. Erreurs rencontrées

42 sorties en erreur ou divergentes. Les premières :

- **T1** : a8f2635f8 docs: record which models this box is good at, and why src/llama-hparams.cpp:8:void llama_hparams::set_swa_pattern(uint32_t n_pattern, bool dense_first) { src/llama-hparams.h:308:    void se
- **T1** : 511 tokens notés — perplexité cumulée 247.031  (4.9 tok/s) === perplexité 247.0308 sur 511 tokens (0 événements, 104.5 s) ===  ### B3 harmony assistant 511 --- ref --- 0.0 0.0 0:00 ls: cannot access '
- **T1** : dump harmony : 254 lignes · dump brut : 511 lignes · ids : 4424 contenu    1  NLL harmony   16.651   NLL brut   10.270   écart   +6.381 contenu   21  NLL harmony    4.853   NLL brut    3.596   écart  
- **T1** : error[E0382]: borrow of moved value: `meta`    --> src/gguf.rs:165:71     | 162 |         let (meta, tensors, fin) = Self::entete(&buf).ok_or_else(|| {     |              ---- move occurs because `met
- **T4** : 6 error[E0382]: borrow of moved value: `cfg`    --> src/model.rs:892:34     | 718 |         let cfg = {     |             --- move occurs because `cfg` has type `Cfg`, which does not implement the `Co
- **T4** : error[E0382]: use of moved value: `cfg`    --> src/model.rs:893:49     | 718 |         let cfg = {     |             --- move occurs because `cfg` has type `Cfg`, which does not implement the `Copy` t
- **T4** : error[E0425]: cannot find value `n_layer` in this scope    --> src/model.rs:772:43     | 772 |         let caches_kv: Vec<KvCache> = (0..n_layer)     |                                           ^^^^^^
- **T4** : thread 'model::tests_kv::aller_retour_kv' (3097033) panicked at src/model.rs:1909:17: valeur 6 bits 8 : 0.2952756 contre 0.29999995 note: run with `RUST_BACKTRACE=1` environment variable to display a 
- **T4** : error[E0425]: cannot find value `gain` in this scope     --> src/main.rs:1135:27      |   27 | fn main() {      | --------- similarly named function `main` defined here ... 1135 |     if let Some((l, 
- **T4** : error[E0425]: cannot find value `idfile` in this scope     --> src/main.rs:1084:18      | 1084 |     let idfile = idfile.unwrap_or_default();      |                  ^^^^^^      | help: a local variab
- **T4** : 1168:    if args.iter().any(|a| a == "--sans-yarn") { mdl.cfg_yarn_off(); } 1259:    let profil = args.iter().any(|a| a == "--ppl-profil"); error[E0425]: cannot find value `args` in this scope     -->
- **T4** : error[E0599]: no method named `clone_ref` found for reference `&DenseQ8` in the current scope     --> src/model.rs:1495:82      | 1495 |                 let d8 = self.layers[l].wo.d.as_ref().expect("F
- **T4** : error[E0609]: no field `lot` on type `Options`    --> src/main.rs:393:26     | 393 |             "--lot" => o.lot = suivant(i).parse().unwrap(),     |                          ^^^ unknown field     | 
- **T4** : 20:use list::{dense_bits, BitmapSign, DenseQ4, DenseQ8, FusedSign, PushMat, SignedDelta, SparseK}; error[E0382]: use of moved value: `d`    --> src/main.rs:785:22     | 785 |             sc.spawn(move
- **T4** : /usr/lib64/clang/23/include/__clang_cuda_builtin_vars.h en-tête présent In file included from <built-in>:2: ./cuda_stub.h:16:76: error: redeclaration of 'threadIdx' with a different type: 'const __qua

## 6. Commits

- gpt-oss : biais attn_output et fenetre par couche corriges, reference llama.cpp  Deux bugs reels, trouves en reprenant REPRISE.md §6.a :  1. attn_output.bias et
- REPRISE : chiffres gpt-oss exacts (ids 15,1757 / texte 15,0757)" && git log --oneline -3 && git status --short | head -3
- Rotation : YaRN a retardement, et la temperature est la moitie nuisible  La politique de rotation se decide desormais par sequence, a la longueur du contexte de
- Rotation : points 4096 et 4608, et la limite du test de generation  Interpolation seule (sans temperature) : 400,13 a 4 096 et 476,09 a 4 608, contre 1 105,20 p
- Item 1 : protocole de perplexite longue --depuis N  Le protocole historique (--ctx N --limit N) confond la longueur du contexte et le contenu : a 8192 jetons on
- Item 3 : cache KV quantifie int8 et int4 empaquete  Le cache KV devient un KvCache : f32 (defaut, comportement inchange), int8 (un octet par valeur) ou int4 (de
- Item 5 : echelles par bloc pour DenseQ8 -- hypothese refutee  DenseQ8 sait maintenant se construire avec une echelle par bloc de 32 (QT_Q8_BLOCS=1, Source8::Pro
- Item 6 : une seule analyse de la ligne de commande pour les quatre modes  struct Options + fn analyser remplacent les deux boucles de 44 drapeaux ; run_infer, r
- Item 7 (1/2) : noyau GPU une warp par ligne, la tete redevient deportable  tete_q8_warp / proj_q8_warp : une warp par ligne, les 32 fils se partagent les blocs 
- Item 4 : prefill par lots -- justesse corrigee, debit a mesurer au calme  Deux bugs corriges dans forward_lot, tous deux invisibles a la compilation :  - les so
- Rapport localite d'activation (idees PowerInfer mesurees) + etat des 8 chantiers  - --profil-neurones / --neurones-sortie : taux de tir et magnitude par neurone
- Item 7 (2/2) : noyaux GPU 4 bits -- MXFP4 et Q4_K, une warp par ligne  - proj_mxfp4_warp : blocs de 17 octets (E8M0 + nibbles), table E2M1 doublee.   Mesure sur
- Item 4 : MoE par lots -- regroupement des jetons par expert  Les modeles a experts suivent desormais le meme chemin par lots que les denses, avec le regroupemen
- Item 2 : le seuil de rotation, tranche par une comparaison appariee  Meme jetons notes (1536-2047), contexte croissant, deux regimes :    contexte   RoPE simple
- Plan 1 M : etat reel des six etapes et ce qui se mesure tout de suite  E1 (prefill par lots) et E2/E3 (KV int8/int4) sont faits et mesures ; E4 (KV sur GPU) et 
- Item 3 : KV quantifie mesure aussi a 4 600 jetons, et compare a llama.cpp  Qwen2.5-0.5B, 4 591 jetons notes :    KV          nous              llama.cpp (8 192)
- Item 8 : premiers resultats d'attention creuse (et ils sont opposes)  gpt-oss, memes 512 jetons (1536-2047), contexte 2 048 :    aucune restriction             
- Item 4 : le GEMM sur le pool, et le gain reel attribue poste par poste  Le produit matrice-matrice s'execute desormais SUR les workers du pool : les fils crees 
- REPRISE : toutes les mesures du tour huit chantiers, et la suite ordonnee  Tableau recapitulatif (noyaux GPU, prefill par lots, KV int8/int4 a 4 600 jetons, att
- Aiguille : le 0.5B echoue 6 fois sur 6 (limite du modele, pas du moteur)  Qwen2.5-0.5B ne retrouve pas un code plante a 1 024 ou 2 048 jetons, a aucune des troi
- KV a echelles par bloc de 32 : int8 de +7,1 % a +1,5 %, int4 de +384 % a +219 %  Le cache KV quantifiait avec UNE echelle par vecteur (tete, position) ; Q8_0 et
- Aiguille : test arrete, et pourquoi (remplissage trop repetitif, prefill trop lent)  9,6 minutes pour UNE sonde sur Qwen3-30B-A3B (1 024 jetons) et un echec : l
- Aiguille : test arrete, et pourquoi (remplissage trop repetitif, prefill trop lent)  9,6 minutes pour UNE sonde sur Qwen3-30B-A3B (1 024 jetons) et un echec : u
- KV par bloc : mesure longue (4 591 jetons) -- int8 +3,4 %, int4 +287 %  Tableau complet :    KV     512 j, par vecteur   512 j, par bloc   4 591 j, par bloc   f
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add -A qtrinet-core/src reports/rapport-prefill-par-lots.md REPRISE.md && git commit -q -F - <<'EOF' &
- docs: préciser que QT_GPU_KV exige QT_GPU (le pilote ne s'ouvre que sur QT_GPU)" && git log --oneline -3 && git status --short | head -3
- docs E4 : comment le noyau d'attention a été validé (cas dégénérés, trois bugs)" && git log --oneline -1
- KV déporté : corriger la copie du chemin par lots  Le miroir était appelé DANS la boucle des jetons avec la position du jeton et la taille du lot : il copiait t
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='docs/contexte-long.md'; s=open(p).read() old = """Deux réserves, mesurées elles aussi 

