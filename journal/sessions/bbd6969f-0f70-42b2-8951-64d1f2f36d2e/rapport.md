# Session bbd6969f — Continue avec REPRISE.md

| | |
|---|---|
| Identifiant | `bbd6969f-0f70-42b2-8951-64d1f2f36d2e` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-09-28 14:46 |
| Durée | 30.2 h |
| Tours | 17 |
| Messages | 1199 |
| Appels d'outils | 1173 |
| Fichiers touchés | 38 |
| Commandes | 906 |
| Sous-agents | 1 |
| Commits | 50 |
| Compactages de contexte | 1 |

## Objectifs déclarés

- **create** — Réaliser les 8 chantiers restants du projet qtrinet-core dans l'ordre : (1) protocole de perplexité longue --depuis/--stride, (2) trancher le seuil de rotation YaRN avec ce protocole, (3) KV int8 puis int4 mesurés sur Qwen 0.5B à ctx 8192 contre llama.cpp, (4) préremplissage par lots (GEMM par tranc
… [374 caractères tronqués]
- **complete** — Réaliser les 8 chantiers restants du projet qtrinet-core dans l'ordre : (1) protocole de perplexité longue --depuis/--stride, (2) trancher le seuil de rotation YaRN avec ce protocole, (3) KV int8 puis int4 mesurés sur Qwen 0.5B à ctx 8192 contre llama.cpp, (4) préremplissage par lots (GEMM par tranc
… [374 caractères tronqués]
- **create** — Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test de l'aiguille sur contexte long (remplissage varié en vrai texte, moins de sondes, réponses plus longues) sur un modèle capable, grâce au préremplissage par lots et au KV déporté ; (2) chemin GPU : dépaquet
… [1023 caractères tronqués]

## 1. Ce qui a été demandé

**Tour 1** — continue avec REPRISE.md

**Tour 2** — prochaine étape?

**Tour 3** — que reste-t-il à faire

**Tour 4** — fais les 8 dans l'ordre

**Tour 5** — <goal_round> Objective: "Réaliser les 8 chantiers restants du projet qtrinet-core dans l'ordre : (1) protocole de perplexité longue --depuis/--stride, (2) trancher le seuil de rotation YaRN avec ce protocole, (3) KV int8 puis int4 mesurés sur Qwen 0.5B à ctx 8192 contre llama.cpp, (4) préremplissage par lots (GEMM par tranches), (5) échelles par bloc pour DenseQ8, (6) refactorisation des boucles C … [842 caractères tronqués]

**Tour 6** — <goal_round> Objective: "Réaliser les 8 chantiers restants du projet qtrinet-core dans l'ordre : (1) protocole de perplexité longue --depuis/--stride, (2) trancher le seuil de rotation YaRN avec ce protocole, (3) KV int8 puis int4 mesurés sur Qwen 0.5B à ctx 8192 contre llama.cpp, (4) préremplissage par lots (GEMM par tranches), (5) échelles par bloc pour DenseQ8, (6) refactorisation des boucles C … [842 caractères tronqués]

**Tour 7** — background job bash-35 (bash: cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && (QT_GPU=1 ./qtrinet-core/target/release/qtrinet-core /home/stephane/FastNVMe/models/gpt-oss-120b-MXFP4.gguf --ppl /tmp/ids_oss.txt --ctx 256 --dense --threads 16 --limit 512 2>&1 | grep -oE "perplexité [0-9.]+ sur [0-9]+ tokens \([0-9]+ événements, [0-9.]+ s\)" > /tmp/gate_oss_final.log; echo "=== fin ===" >> /tmp/ … [98 caractères tronqués]

**Tour 8** — que reste-t-il à faire

**Tour 9** — fais tous ces 6 nouveaux chantiers

**Tour 10** — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test de l'aiguille sur contexte long (remplissage varié en vrai texte, moins de sondes, réponses plus longues) sur un modèle capable, grâce au préremplissage par lots et au KV déporté ; (2) chemin GPU : dépaquetage vectorisé du noyau d'attention (13,2 ms/couche à 1 M en int4 vers ~3 ms … [1491 caractères tronqués]

**Tour 11** — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test de l'aiguille sur contexte long (remplissage varié en vrai texte, moins de sondes, réponses plus longues) sur un modèle capable, grâce au préremplissage par lots et au KV déporté ; (2) chemin GPU : dépaquetage vectorisé du noyau d'attention (13,2 ms/couche à 1 M en int4 vers ~3 ms … [1491 caractères tronqués]

**Tour 12** — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test de l'aiguille sur contexte long (remplissage varié en vrai texte, moins de sondes, réponses plus longues) sur un modèle capable, grâce au préremplissage par lots et au KV déporté ; (2) chemin GPU : dépaquetage vectorisé du noyau d'attention (13,2 ms/couche à 1 M en int4 vers ~3 ms … [1491 caractères tronqués]

**Tour 13** — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test de l'aiguille sur contexte long (remplissage varié en vrai texte, moins de sondes, réponses plus longues) sur un modèle capable, grâce au préremplissage par lots et au KV déporté ; (2) chemin GPU : dépaquetage vectorisé du noyau d'attention (13,2 ms/couche à 1 M en int4 vers ~3 ms … [1491 caractères tronqués]

**Tour 14** — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test de l'aiguille sur contexte long (remplissage varié en vrai texte, moins de sondes, réponses plus longues) sur un modèle capable, grâce au préremplissage par lots et au KV déporté ; (2) chemin GPU : dépaquetage vectorisé du noyau d'attention (13,2 ms/couche à 1 M en int4 vers ~3 ms … [1491 caractères tronqués]

**Tour 15** — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test de l'aiguille sur contexte long (remplissage varié en vrai texte, moins de sondes, réponses plus longues) sur un modèle capable, grâce au préremplissage par lots et au KV déporté ; (2) chemin GPU : dépaquetage vectorisé du noyau d'attention (13,2 ms/couche à 1 M en int4 vers ~3 ms … [1491 caractères tronqués]

**Tour 16** — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test de l'aiguille sur contexte long (remplissage varié en vrai texte, moins de sondes, réponses plus longues) sur un modèle capable, grâce au préremplissage par lots et au KV déporté ; (2) chemin GPU : dépaquetage vectorisé du noyau d'attention (13,2 ms/couche à 1 M en int4 vers ~3 ms … [1491 caractères tronqués]

**Tour 17** — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test de l'aiguille sur contexte long (remplissage varié en vrai texte, moins de sondes, réponses plus longues) sur un modèle capable, grâce au préremplissage par lots et au KV déporté ; (2) chemin GPU : dépaquetage vectorisé du noyau d'attention (13,2 ms/couche à 1 M en int4 vers ~3 ms … [1491 caractères tronqués]

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

*265 appels d'outils.* Actions notables :

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
- … et 208 autres

**Synthèse produite :**

Les 8 chantiers sont faits : implémentés, mesurés, documentés et commités. Voici le bilan.

\## Les huit chantiers

| # | chantier | résultat mesuré |
|---|---|---|
| 1 | protocole de perplexité longue | `--depuis`/`--stride` en place ; utilisés pour toutes les mesures appariées ci-dessous |
| 2 | seuil de rotation YaRN | **tranché, et le seuil était trop bas** : à contexte 5 120 (positions 4 608-5 119), RoPE simple **9,6986** contre **1 269,1777** en interpolation seule → la bascule passe de « longueur d'origine déclarée » à 1,25 × celle-ci |
| 3 | KV int8/int4 à ctx 8 192 | f32 14,2339 · int8 **14,6667 (+3,0 %)** contre +0,8 % chez llama.cpp · int4 **66,0369 (+364 %)** contre +494 % chez llama.cpp — meilleur que la référence, à moitié mémoire |
| 4 | préremplissage par lots | Qwen ctx 512 : **17,1 → 13,6 s (−20 %)** ; gpt-oss : ≈ 50 → 34,4 s ; perplexités identiques |
| 5 | échelles par bloc `DenseQ8` | hypothèse réfutée (23,6964 contre 23,6123) — le 6 bits garde son avantage de coût |
| 6 | boucles CLI unifiées | `struct Options` + `analyser` |
| 7 | noyaux GPU par ligne + 4 bits | warp Q8_0 / MXFP4 (bit à bit) / Q4_K / **Q6_K** (3,6 contre 8,3 ms sur la tête de 191 Mo) ; tête Q6_K branchée : 7,58 → **3,60 ms/jeton** |
| 8 | plan 1 M | **E4** : `attn_kv_partiels`/`recombine` + miroir VRAM paginé ; **E5** mesuré (`--attn-topk 256` : 234,9 contre 298,6) ; MLA et vision documentés non testables ici |

\## Le gain le plus net (E4)

À 1 M de clés, une couche : CPU **968 ms** → GPU **13,2 ms** (int4, ×73). Dans le moteur, ctx 4 096 : attention **22,16 → 3,29 ms/jeton**, balayage 219 → 136 s (−38 %), perplexité 12,2177 → 12,2175. Le miroir VRAM ne réserve plus `ctx` positions d'un coup : à **ctx 1 M**, 0,05 Go occupés pour 512 jetons écrits (l'allocation en bloc exigeait 25,77 Go et refusait).

\## Trois bugs silencieux, trouvés par la mesure

- `engine.rs` : un **pointeur de tranche (gras)** relu comme `Vec<Vec<i32>>` faisait lire au worker une longueur de 90 (blocs) au lieu du lot — panique, et surtout **blocage muet** du fil principal. Corrigé, test verrouillé (lots 1/8/9/17/40) et `catch_unwind` + compteur `morts` : une panique de worker échoue désormais en clair.
- noyau d'attention : la **requête** était lue par voie (accord parfait seulement pour un vecteur de base, écart 4e-1 sinon) ; les partiels n'étaient **pas indexés par tête KV** (7 têtes sur 14 à zéro) ; les **échelles** du KV quantifié étaient indexées en éléments (écart 7e7 en int8).
- miroir du c
… [1011 caractères tronqués]

### Tour 7 — background job bash-35 (bash: cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && (QT_GPU=1 ./qtrinet-core/target/rele … [378 caractères tronqués]

*7 appels d'outils.* Actions notables :

- job_output
- bash — Read gpt-oss gate result
- bash — Compare gpt-oss gate with and without GPU
- bash — Find all GPU-availability gates
- bash — Inspect un-gated GPU paths
- bash — Document the gate variance and commit
- bash — Final repo state check

**Synthèse produite :**

⏵ Fausse alerte levée : l'écart venait de `QT_GPU`, pas d'une régression

La porte gpt-oss qui tournait en arrière-plan affichait **15,1667** au lieu de 15,1757 : ce n'était pas une régression. Mesuré deux fois, même binaire, même commande :

| commande | perplexité |
|---|---|
| sans `QT_GPU` | **15,1757** ✓ (le chiffre de contrôle du dépôt) |
| avec `QT_GPU=1` | 15,1667 |

La cause est dans le moteur : `QT_GPU` ouvre le pilote, et `Proj::charger` déporte alors **de lui-même** toute projection Q8_0 de plus de 8 Mo (seuil `SEUIL_GPU`, fixé par mesure). Les projections de gpt-oss font 8,8 Mo → elles passent par le noyau GPU, même calcul mais ordre de sommation différent, d'où 0,06 % d'écart — ici légèrement *en faveur* du GPU.

J'avais ajouté `QT_GPU=1` par habitude dans la commande d'arrière-plan ; le gate documenté ne le met pas ✓.

C'est maintenant écrit noir sur blanc dans `REPRISE.md` (§8, commande du gate) et dans le tableau des mesures, avec le commit `45948e2`.

État final vérifié : `cargo test --release` 6/6, Qwen ctx 256 = **19,3885**, gpt-oss ctx 256 = **15,1757** (sans `QT_GPU`), arbre propre à l'exception de `journal/README.md` (churn du crochet d'archivage). Les 8 chantiers restent tels que décrits dans mon bilan précédent — rien d'autre à reprendre de ce côté.

### Tour 8 — que reste-t-il à faire

*5 appels d'outils.* Actions notables :

- bash — Read REPRISE next-steps list
- bash — Read full next-steps section
- bash — Check gpt-oss head type and MXFP4 wiring
- bash — Determine gpt-oss head tensor type
- bash — Read immediate-measurement section

**Synthèse produite :**

⏵ Inventaire des restes, par ordre de rentabilité

Les 8 chantiers sont clos ; voici ce qui reste ouvert, du plus rentable au plus lointain. Tout est chiffré dans `docs/contexte-long.md`, `reports/rapport-prefill-par-lots.md` et `REPRISE.md`.

\## 1. Qualité du contexte long : l'aiguille (le manque le plus visible)

La perplexité ne dit pas si le modèle **retrouve** une information. `tools/aiguille.py` plante un code et vérifie qu'il ressort : 6/6 échecs sur Qwen 0.5B (modèle trop faible) et **9,6 min pour une seule sonde** sur Qwen3-30B-A3B en préremplissage séquentiel → test arrêté. Il faut du remplissage **varié** (vrai texte), moins de sondes, des réponses plus longues. C'est devenu abordable : le préremplissage par lots donne −20 % (Qwen) et −31 % (gpt-oss), et le KV déporté rend l'attention plate.

\## 2. Chemin GPU

| reste | chiffre qui le justifie |
|---|---|
| **dépaquetage vectorisé** du noyau d'attention | 13,2 ms/couche à 1 M en int4 (25-40 Go/s) contre 158 Go/s en f32 → viser ~3 ms |
| **brancher MXFP4 dans le moteur** | noyau bit à bit identique, ×75 sur un expert (0,1 contre 7,5 ms) — mais aucun appel : il faut une politique de résidence, et `rapport-localite-activation.md` dit qu'un préchargement statique ne paie pas |
| **attention par lots sur GPU** | `forward_lot` garde le CPU, où l'attention par lots est **1,7 ×** le chemin par jeton ; le noyau ne sert qu'au décodage |
| **noyau de la tête Q8_0** | 5,5 ms/jeton en lot, lié au **calcul** (le lot n'y change rien) → AVX2 ou déport (`QT_GPU_TETE=1` : 15,6 → 6,2 ms/jeton sur gpt-oss) |
| **second GPU** | 16 Go libres, jamais utilisés : répartir le KV (128 Mo/couche en int4 à 1 M) ou les experts |

\## 3. Mémoire

- **Pagination du cache CPU** : à ctx 1 M, il réserve 25,77 Go pour 512 jetons écrits. Le miroir VRAM est paginé, l'hôte non.
- **Écart int8 avec llama.cpp** à 8 192 : +3,0 % contre +0,8 %. Hypothèse non testée : leurs clés sont calculées en f16 avant quantification.

\## 4. Rotation

Au-delà de 5 120 jetons : **non mesuré** (≈ 1 h par régime à 16 k, corpus de 17 k). Le seuil actuel (1,25 × longueur déclarée) n'est qu'une borne basse *mesurée*.

\## 5. Structurel, non testable ici

- **MLA** : aucun modèle MLA en GGUF sur la machine (le « deepseek-r1-distill » local est un Qwen dense).
- **Vision** : les poids Qwen2.5-VL-7B et le projecteur `mmproj` sont présents, mais rien ne lit les patchs — c'est une tour de vision entière à écrire.

\## 6. Hygiène

La section « Ce qu'il faut faire en
… [573 caractères tronqués]

### Tour 9 — fais tous ces 6 nouveaux chantiers

*88 appels d'outils.* Actions notables :

- create_goal
- todo_write
- bash — Inspect needle tool and 30B model
- bash — Check corpus and 30B chat speed
- bash — Find a large natural-text corpus
- bash — Check corpus and lot usage in inference
- bash — Inspect run_infer prefill
- bash — Read run_infer decode/prefill loop
- bash — Check generate prefill path
- bash — Find where options are applied to the model
- bash — Wire batched prefill into generate
- bash — Check lot is in scope in run_infer
- bash — Build with batched prefill
- bash — Read run_infer destructuring
- … et 72 autres

**Synthèse produite :**

⏵ Bilan de la fournée : 6 sous-chantiers sur 10 livrés, la rotation 16 k tourne encore

Six des dix sous-chantiers sont faits, mesurés et commités ; quatre restent, dont un qui tourne en ce moment.

\## Livré

| sous-chantier | mesure | commit |
|---|---|---|
| **1. Aiguille v2** | **12 sondes sur 12** trouvées (profondeurs 0,1/0,5/0,9) : Qwen1.5B 512+2048, Qwen3-30B 2048, gpt-oss-120b 4096 avec KV déporté — là où la v1 échouait 6/6 | `5dfa6b1`, `4512f69` |
| **2a. Dépaquetage vectorisé** du noyau d'attention | à 1 M de clés : f32 13,6 → **7,0 ms** (308 Go/s), int8 15,0 → **6,5**, int4 13,2 → **7,4 ms** ; écarts au CPU inchangés | `a64328d` |
| **2b. Experts MXFP4 en VRAM** | +6 % seulement (5,12 → 5,43 jetons/s), 53,5 % de succès, 10,64 Go montés — **verdict : ne pas activer par défaut**, le chemin CPU est déjà AVX2 | `4512f69` |
| **2c. Attention par lots déportée** | préremplissage ctx 4096, lot 512 : **261,6 → 93,7 s (×2,8)**, perplexité **identique** (12,2175) | `4512f69` |
| **3. Pagination + hypothèse f16** | cache CPU à ctx 1 M : **0,03 Go** au lieu de 25,77 Go ; hypothèse « clés en f16 avant quantification » **réfutée** (perplexité identique) | `bc5aa9a` |
| **6. Hygiène** | feuille de route réécrite, tableau des pièges `QT_GPU*` (`QT_GPU` ouvre le pilote : sans elle, les autres ne font rien et rien ne le dit) | `6664eef` |

Au passage : le préremplissage par lots est branché sur la **génération** (`Model::lot`) — il ne l'était que sur la perplexité, ce qui rendait toute invite longue hors de prix.

\## Reste

1. **2d — noyau de tête Q8_0.** Le chemin CPU est lié au calcul (5,5 ms/jeton en lot sur Qwen 0.5B ; la tête de gpt-oss fait 579 Mo, la plus grosse matrice du modèle). Voie AVX2 ou déport.
2. **2e — second GPU.** 16 Go dorment : à répartir entre KV et experts, avec un second contexte CUDA.
3. **4 — rotation à 16 k.** **En cours** : deux régimes, mêmes 512 jetons notés (15 872-16 383), KV déporté obligatoire pour que la passe ne dépasse pas l'heure par régime. Journal : `/tmp/rotation_16k.log`.
4. **5 — MLA et vision.** MLA demande un modèle **synthétique** écrit à la main (aucun modèle MLA local) validé contre une référence indépendante ; la vision demande la tour ViT + le chemin `mmproj`, entièrement à écrire.

L'objectif reste actif : la suite (2d, 2e, résultat du 16 k, puis MLA/vision) est exactement la liste du §6 de `REPRISE.md`, qui a été réécrite pour ça. Rien n'est laissé cassé : `cargo test` 6/6, porte Qwen **19,3885** revérifiée aprè
… [117 caractères tronqués]

### Tour 10 — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test d … [1771 caractères tronqués]

*19 appels d'outils.* Actions notables :

- bash — Check 16k rotation job and repo state
- bash — Read Q8_0 branch of q8_dot_at
- bash — Add AVX2 head kernel
- bash — Verify PPL unchanged with AVX2 head
- bash — Check rotation progress and GPU singleton
- bash — Expose second GPU and machine list
- bash — Find KV mirror plumbing sites
- bash — Split KV mirror across GPUs
- bash — Verify two-GPU KV split
- bash — Document and commit 2d/2e
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/plan-mla-vision.md`
- bash — Wait for 16k rotation result
- bash — Commit plan and wait for rotation
- bash — Fix commit message quoting
- … et 5 autres

**Synthèse produite :**

⏵ Tour 1 : quatre chantiers sur six livrés, la rotation 16 k tourne encore

\## Livré dans ce tour

| chantier | mesure | commit |
|---|---|---|
| **2d. Noyau de tête Q8_0 en AVX2** | `vpmaddwd` sur 32 niveaux, **somme entière donc exacte** : porte Qwen **19,3885** et gpt-oss **15,1757** inchangées au chiffre près — le noyau est bit-identique au scalaire | `38d4d8b` |
| **2e. KV réparti sur les deux Quadro** | couches allouées en tournant : **12 sur GPU 1, 12 sur GPU 0**, perplexité 13,1369 inchangée. La pagination rend la 2ᵉ carte inutile aux longueurs courantes ; sa valeur est la marge des très longs contextes (KV f32 à 1 M = 24 Go, soit 12 Go par carte) | `38d4d8b` |
| **5. Plan MLA + vision** | document `docs/plan-mla-vision.md` : tenseurs et clés GGUF, ordre du calcul MLA, et le **contrôle négatif** qui relie l'implémentation nouvelle à une déjà validée (avec `W_kv_b = I`, l'attention latente doit redonner exactement une MQA) | `c866186` |

Les deux portes de non-régression ont été revérifiées après le changement de noyau : **Qwen ctx 256 = 19,3885** et **gpt-oss ctx 256 = 15,1757**, toutes deux sans `QT_GPU` (piège documenté : `QT_GPU` déporte à lui seul les projections Q8_0 de plus de 8 Mo et décale le chiffre de 0,06 %).

\## En cours

**Chantier 4 — rotation à 16 k** : la première passe (RoPE simple, mêmes 512 jetons notés, positions 15 872-16 383) tourne depuis ~28 minutes ; la seconde (interpolation seule) suivra, ~30 minutes de plus. Le préremplissage par lots et le KV déporté la rendent possible, mais elle reste l'opération la plus chère du dépôt. Résultat à collecter dans `/tmp/rotation_16k.log` — je n'ai pas voulu l'interrompre pour tenir un délai.

\## Reste

**Chantier 5 — MLA et vision**, le seul non commencé. Le plan est écrit et chiffré : un modèle MLA **synthétique** en GGUF (aucun modèle MLA local), une référence numpy indépendante, et la validation par équivalence MQA ; pour la vision, la tour ViT, la fusion 2 × 2 des patchs et surtout le chemin d'injection d'embeddings qui manque au moteur (`forward` part toujours de `token_embd`).

L'objectif reste **actif** : le prochain tour commence par relever le résultat du 16 k, puis attaque MLA selon `docs/plan-mla-vision.md`. Rien n'est laissé cassé — `cargo test` 6/6, arbre propre, et tout ce qui est annoncé ici est dans un rapport, un document ou `REPRISE.md`.

### Tour 11 — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test d … [1771 caractères tronqués]

*11 appels d'outils.* Actions notables :

- bash — Collect 16k rotation result
- bash — Check engine elapsed time
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/mla_synthetique.py`
- bash — Generate synthetic MLA model and reference
- bash — Fix writer and verify GGUF header
- bash — Fix reference einsums and rerun
- bash — Debug MLA reference shapes
- bash — Fix einsum indices and regenerate
- bash — Document harness state and commit
- bash — Check rotation engine progress
- bash — Final repo and test check

**Synthèse produite :**

⏵ Tour 2 : le harnais MLA est prêt et vérifié ; le 16 k tourne toujours

\## Fait dans ce tour

**Chantier 5 — première moitié livrée : le harnais MLA.**

MLA n'était pas testable faute de modèle ; le harnais se fabrique maintenant au lieu d'attendre :

- `tools/mla_synthetique.py` écrit un **GGUF synthétique** de 381 ko — 26 tenseurs, 15 clés de métadonnées, architecture `deepseek2`, `q_lora_rank` 32, `kv_lora_rank` 48, `qk_rope` 16, `qk_nope` 16, `v_dim` 16, 4 têtes, 2 couches, hidden 64 — en-tête relu et vérifié (version 3, 26 tenseurs) ;
- il calcule en **numpy la référence du même calcul** (logits de 8 jetons, forme `(8, 64)`, rangés dans `/tmp/mla_ref/` avec les identifiants et les formes).

Deux bugs de la référence ont été trouvés en la relisant, et c'est exactement l'intérêt du harnais : un tableau d'entiers typé comme tableau de chaînes dans l'en-tête GGUF, et surtout des indices d'`einsum` qui **confondaient la dimension de tête et la dimension de clé** (les scores se calculent en `nhe,mhe->nhm` : n requête, m clé, h tête). Sans référence indépendante, ces deux erreurs seraient passées dans le moteur et auraient été attribuées au modèle.

Reste sur ce chantier : le **chemin MLA du moteur** — lire ces tenseurs, tenir le cache latent (`c_kv` + `k_rope` par position), ne tourner que la partie « rope », et retrouver `logits.npy`. Le plan complet (noms de tenseurs, ordre du calcul, contrôle par équivalence MQA) est dans `docs/plan-mla-vision.md`, mis à jour avec l'état du harnais.

\## Toujours en cours

**Chantier 4 — rotation à 16 k** : le premier régime (RoPE simple, 16 384 jetons de contexte, 512 notés) tourne depuis ~37 minutes et progresse normalement (10 h 20 de temps CPU sur 16 fils, 58 Go résidents). Le second (interpolation seule) suivra. Je ne l'ai pas interrompu : c'est la dernière mesure du chantier, et son journal `/tmp/rotation_16k.log` est prêt à être relevé.

\## État

`cargo test` 6/6, arbre propre (hors l'archive du journal), portes de non-régression vérifiées après chaque changement de noyau : **Qwen 19,3885** et **gpt-oss 15,1757**, toutes deux sans `QT_GPU`.

Bilan des six chantiers : **1, 2 (cinq sous-items), 3, 6 terminés** ; **4** en attente de sa seconde passe ; **5** à moitié — le harnais est prêt, le moteur reste à faire. L'objectif reste **actif** : le prochain tour relève le 16 k, puis implémente MLA contre la référence qui l'attend.

### Tour 12 — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test d … [1771 caractères tronqués]

*20 appels d'outils.* Actions notables :

- bash — Check rotation and helper APIs
- bash — Read Meta enum accessors
- bash — Add MLA struct and loader
- bash — Implement MLA forward path
- bash — Check build of MLA path
- bash — Add MLA bench and dummy tensors
- bash — Run MLA bench on synthetic model
- bash — Compare engine MLA logits with numpy reference
- bash — Fix GGUF convention and recompare
- bash — Diagnose MLA load failure
- bash — Check declared dims in the file
- bash — Verify loader edits applied
- bash — Re-run MLA bench after rebuild
- bash — Fix dims order and compare again
- … et 6 autres

**Synthèse produite :**

⏵ Tour 3 : MLA est validé (5,2e-7 contre la référence numpy)

\## Fait dans ce tour

**Chantier 5, moitié MLA : implémenté et validé.**

Le moteur charge maintenant un modèle MLA — reconnu à ses tenseurs (`attn_kv_a_mqa`), **sans aucune clé de configuration nouvelle** : les rangs se lisent dans les formes — et tient le **cache latent** (`c_kv` + `k_rope` par position, `k_nope` et `v` reconstruits à la lecture par `W_kv_b`). La rotation ne porte que sur la partie « rope ». Le chemin est volontairement séparé de `forward` : le modèle du harnais n'a ni tenseurs Q8_0 ni fenêtre glissante.

Mesure : `--banc-mla` écrit les logits des 8 positions, comparés à la référence numpy indépendante → **écart max relatif 5,2e-7**, soit le bruit de virgule flottante du moteur. Le témoin imprimé : `MLA : q_lora 32 · kv_lora 48 · qk_nope 16 + qk_rope 16 · v 16 · cache latente 64 valeurs par jeton (au lieu de 32)`.

Deux erreurs réelles ont été trouvées **par** la référence — c'est exactement son rôle : des indices d'`einsum` qui confondaient dimension de tête et dimension de clé dans la référence elle-même, et surtout la **convention GGUF des tenseurs linéaires** (stockés (sortie, entrée), déclarés (entrée, sortie)). L'écart est passé de 0,82 à 5,2e-7 après correction.

**Chantier 5, moitié vision : reconnaissance faite, plan corrigé par les faits.** Le `mmproj` est en architecture `clip` et contient la tour **complète** (519 tenseurs, `v.blk.N.*`) : image 560, patchs 14, largeur 1280, 32 couches, 16 têtes, MLP 3420, projecteur `qwen2.5vl_merger`, projection 3584, normalisation CLIP. Le point délicat est confirmé par le fichier : **`n_wa_pattern = 8`**, une couche sur huit en attention **locale** — se tromper de fenêtre ferait diverger les embeddings sans aucun signal.

\## En cours

**Chantier 4** : la première passe à 16 k est tombée — **RoPE simple : perplexité 35,1837** (512 jetons notés, 16 384 de contexte, 39 minutes). La seconde (interpolation seule) tourne depuis une vingtaine de minutes ; c'est elle qui dira si le seuil doit encore monter.

\## État

`cargo test` 6/6, porte Qwen **19,3885** revérifiée après les changements MLA (chemin séparé, portes intactes), arbre propre.

Bilan des six chantiers : **1, 2 (cinq sous-items), 3, 4 (première passe), 6 terminés** ; **5** : MLA **fait et validé**, vision **planifiée et reconnue**, l'implémentation ViT reste à écrire. L'objectif reste **actif** : prochain tour, relever la seconde passe du 16 k et l'écrire dans le rapport, p
… [57 caractères tronqués]

### Tour 13 — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test d … [1771 caractères tronqués]

*9 appels d'outils.* Actions notables :

- bash — Collect 16k interp result
- bash — List distinct ViT tensor patterns
- bash — Wait for 16k interp result
- bash — Poll interp run again
- bash — Poll interp run
- bash — Poll interp run once more
- bash — Document 16k verdict and raise threshold
- bash — Commit 16k verdict and threshold change
- todo_write

**Synthèse produite :**

⏵ Tour 4 : le 16 k est tranché, cinq chantiers et demi sur six sont clos

\## Livré dans ce tour

**Chantier 4 — rotation à 16 384 jetons, bouclé.** Protocole apparié, mêmes 512 jetons notés (positions 15 872 à 16 383), KV déporté — sans lui l'attention coûte ~180 ms/jeton et la passe dépasse l'heure par régime :

| régime | perplexité | durée |
|---|---|---|
| **RoPE simple** | **35,18** | 2 367 s |
| interpolation seule | **1 133,02** | 2 251 s |

**×32 en faveur du simple.** Sur toute l'étendue mesurée — 128, 512, 1 024, 1 536, 5 120, 16 384 — l'interpolation n'a **jamais** gagné, et l'écart se creuse avec la longueur (×1,1 à 512, ×131 à 5 120, ×32 à 16 384).

Conséquence appliquée : le seuil de bascule passe de 1,25 × à **4 ×** la longueur déclarée (16 384 pour gpt-oss, exactement la plus grande longueur mesurée). L'interpolation ne s'active plus dans la plage où l'on sait qu'elle nuit ; au-delà, c'est une extrapolation non mesurée, et le document le dit.

\## État des six chantiers

| # | chantier | état |
|---|---|---|
| 1 | aiguille long contexte | ✅ 12/12 sondes (1,5B 512/2048, 30B 2048, gpt-oss 4096) |
| 2 | chemin GPU (5 sous-items) | ✅ vectorisation ×1,8-2,3 · experts +6 % (verdict : ne pas activer) · lots ×2,8 · tête AVX2 · deux cartes 12/12 |
| 3 | mémoire KV | ✅ pagination CPU (0,03 Go à ctx 1 M) · hypothèse f16 **réfutée** |
| 4 | rotation à 16 k | ✅ **35,18 contre 1 133,02**, seuil corrigé |
| 5 | MLA + vision | ⏳ **MLA fait et validé** (5,2e-7 contre la référence numpy) ; **vision** : paramètres et nommage relevés dans le `mmproj` (560 px, patchs 14, 32 couches, `n_wa_pattern = 8`), tour ViT à écrire |
| 6 | hygiène | ✅ feuille de route réécrite + tableau des pièges `QT_GPU*` |

`cargo test` 6/6, porte Qwen **19,3885** revérifiée, arbre propre. Le changement de seuil ne touche que les contextes > 5 120, donc les deux portes de non-régression (ctx 256) sont structurellement intactes.

\## Reste

La **tour de vision** : c'est le seul morceau non commencé, et le plus gros du dépôt (ViT 32 couches avec attention locale une couche sur huit, fusion 2 × 2 des patchs, pré-traitement d'image, et le chemin d'injection d'embeddings qui manque au moteur). Le plan est dans `docs/plan-mla-vision.md`, désormais adossé aux chiffres relevés dans le fichier plutôt qu'à des suppositions.

L'objectif reste **actif** pour ce dernier morceau.

### Tour 14 — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test d … [1771 caractères tronqués]

*5 appels d'outils.* Actions notables :

- bash — Check Gguf tensor access API
- bash — Add tensor listing mode
- bash — List mmproj tensors with engine reader
- bash — List non-block mmproj tensors
- bash — Document verified vision inventory

**Synthèse produite :**

⏵ Tour 5 : inventaire vision relevé ; le plan est corrigé par les faits

\## Fait dans ce tour

**La vision n'est plus une supposition : elle est relevée.**

J'ai ajouté au moteur un mode `--tensors` (nom, dimensions, type de chaque tenseur d'un GGUF) — un outil qui servira à tout chemin qu'on ne sait pas encore lire — et il a donné la structure exacte du projecteur :

| tenseur | dimensions | rôle |
|---|---|---|
| `v.patch_embd.weight` **et** `.1` | [1280, 3, 14, 14] | **deux** convolutions de patchs |
| `v.blk.N.attn_q/k/v/out.weight` | [1280, 1280] | **avec biais** (`attn_q.bias`…) |
| `v.blk.N.ffn_gate/up.weight` | [3420, 1280] | MLP, **avec biais** |
| `v.blk.N.ffn_down.weight` | [1280, 3420] | MLP |
| `v.blk.N.ln1.weight`, `ln2.weight` | [1280] | LayerNorm |
| `v.post_ln.weight` | [1280] | norme finale |
| `mm.0.weight` | [5120, 5120] | projecteur : 5120 = 1280 × 4 → fusion 2 × 2 |
| `mm.2.weight` | [3584, 5120] | sortie 3584 = largeur du modèle |

Deux corrections au plan, toutes deux issues du relevé :

1. **aucun `position_embd`** — Qwen2.5-VL n'ajoute pas de position absolue, il tourne ses patchs en 2-D (mRoPE). Mon plan initial en supposait un : c'était faux ;
2. **les biais sont partout** (q, k, v, sortie, MLP) — l'erreur classique de ce dépôt, qui a déjà coûté 39,80 → 20,84 sur gpt-oss.

Les 519 tenseurs couvrent la tour complète et son projecteur : le chemin image peut se construire sur ce fichier seul, sans le modèle de langage.

\## État

`cargo test` 6/6, portes de non-régression intactes (le mode `--tensors` et le chemin MLA sont des ajouts, le seuil de rotation ne touche que les contextes > 5 120), arbre propre.

**Cinq chantiers et demi sur six :** 1 (aiguille 12/12), 2 (cinq sous-items GPU), 3 (pagination + hypothèse f16 réfutée), 4 (rotation à 16 k : 35,18 contre 1 133,02, seuil porté à 4 ×), 6 (hygiène) sont clos ; le **5** a sa moitié MLA **validée** (5,2e-7 contre la référence numpy) et sa moitié vision **relevée et planifiée**, l'implémentation de la tour ViT restant à écrire — c'est le seul morceau ouvert.

L'objectif reste **actif** pour ce dernier morceau : le prochain tour peut attaquer directement le pré-traitement d'image et l'embedding de patchs, dont les formes exactes sont maintenant dans `docs/plan-mla-vision.md`.

### Tour 15 — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test d … [1771 caractères tronqués]

*4 appels d'outils.* Actions notables :

- bash — Add patch embedding bench
- bash — Run vision patch embedding bench
- bash — Compare patch embedding with numpy reference
- bash — Document and commit vision first slice

**Synthèse produite :**

⏵ Tour 6 : le chemin image a sa première tranche validée

\## Fait dans ce tour

**Vision — première tranche implémentée et validée.** `--banc-vision` fait tourner la convolution 14 × 14 du ViT sur une image 28 × 28 déterministe (dégradé + carré central) et écrit les 4 patchs × 1 280 canaux ; `tools/vision_ref.py` refait le **calcul** en numpy à partir des mêmes poids — l'extraction des tenseurs étant vérifiée séparément par `--tensors`. Même partage des rôles que pour MLA, et même résultat :

**écart max relatif 5,4e-7**, le bruit de virgule flottante du moteur.

La tranche est isolée à dessein : si l'embedding de patchs est faux, tout ce qui suit l'est aussi, et le comparer seul évite d'attribuer au modèle une erreur de découpage.

Reste, dans l'ordre et avec l'inventaire exact des tenseurs déjà relevé : la rotation 2-D (mRoPE) des patchs, les 32 couches avec **attention locale une sur huit** (`n_wa_pattern = 8`), `v.post_ln`, le projecteur `mm.0`/`mm.2` (fusion 2 × 2, 5120 = 1280 × 4), et enfin **l'injection des embeddings dans le flux de jetons** — le point d'architecture qui manque au moteur, puisque `forward` part toujours de `token_embd`.

\## État général

| # | chantier | état |
|---|---|---|
| 1 | aiguille long contexte | ✅ 12/12 sondes |
| 2 | chemin GPU (vectorisation, experts, lots, tête AVX2, 2 cartes) | ✅ |
| 3 | mémoire KV (pagination 0,03 Go à 1 M, hypothèse f16 réfutée) | ✅ |
| 4 | rotation à 16 k (35,18 contre 1 133,02, seuil à 4 ×) | ✅ |
| 5 | MLA ✅ validé (5,2e-7) · vision ⏳ embedding de patchs validé (5,4e-7), tour à finir | en cours |
| 6 | hygiène (feuille de route + pièges `QT_GPU*`) | ✅ |

`cargo test` 6/6, portes de non-régression Qwen **19,3885** et gpt-oss **15,1757** intactes (les ajouts MLA/vision sont des chemins séparés), arbre propre.

L'objectif reste **actif** : il ne manque que la suite de la tour de vision, dont chaque étape est décrite dans `docs/plan-mla-vision.md` avec les formes et les biais relevés dans le fichier.

### Tour 16 — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test d … [1771 caractères tronqués]

*11 appels d'outils.* Actions notables :

- bash — Add projector slice and reference
- bash — Fix borrow and rebuild
- bash — Run and validate projector slice
- bash — Fix output write and erf, revalidate
- bash — Show build error
- bash — Fix order, rebuild and validate projector
- bash — Move projector before write and validate
- bash — Single declaration at function start
- bash — Validate projector slice end to end
- bash — Fix reference reading and validate
- bash — Document and commit projector validation

**Synthèse produite :**

⏵ Tour 7 : les deux extrémités du chemin image tiennent

\## Fait dans ce tour

**Vision — le projecteur est implémenté et validé**, après l'embedding de patchs du tour précédent. Les deux extrémités du chemin image sont donc en place et vérifiées contre une implémentation numpy indépendante :

| tranche | écart max relatif |
|---|---|
| embedding de patchs (convolution 14 × 14 sur 28 × 28) | **5,37e-07** |
| projecteur (fusion 2 × 2 → `mm.0` → GELU → `mm.2`) | **1,73e-06** |

Le projecteur concatène en ordre raster les quatre patchs d'un groupe 2 × 2 (5120 = 1280 × 4), applique `mm.0` (5120 → 5120) + biais, un GELU exact, puis `mm.2` (5120 → 3584) + biais — 3 584 valeurs, |sortie| = 17,88. Détail méthodologique qui compte : la référence numpy utilise **la même approximation d'erf** que le moteur (Abramowitz-Stegun 7.1.26, écrite en vectorisé) — comparer deux formules différentes aurait mesuré l'approximation, pas l'implémentation.

Reste le **milieu** : rotation 2-D des patchs (mRoPE), 32 couches avec attention locale une sur huit, `v.post_ln` — puis l'injection des embeddings dans le flux de jetons, le point d'architecture qui manque au moteur.

\## État général

| # | chantier | état |
|---|---|---|
| 1 | aiguille long contexte | ✅ 12/12 |
| 2 | chemin GPU (5 sous-items) | ✅ |
| 3 | mémoire KV | ✅ |
| 4 | rotation à 16 k | ✅ (35,18 contre 1 133,02, seuil à 4 ×) |
| 5 | MLA ✅ (5,2e-7) · vision ⏳ patchs ✅ + projecteur ✅, 32 couches à écrire | en cours |
| 6 | hygiène | ✅ |

`cargo test` 6/6, arbre propre, portes de non-régression intactes (les chemins MLA et vision sont des ajouts isolés).

L'objectif reste **actif** : il ne manque que le corps de la tour de vision, chaque étape étant décrite dans `docs/plan-mla-vision.md` avec les formes et les biais relevés dans le fichier réel.

### Tour 17 — <goal_round> Objective: "Réaliser les 6 nouveaux chantiers du projet qtrinet-core, dans l'ordre : (1) relancer le test d … [1771 caractères tronqués]

*2 appels d'outils.* Actions notables :

- bash — Final gpt-oss gate and repo check
- bash — Detail next vision step and commit

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
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/aiguille.py` | 2 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-prefill-par-lots.md` | 1 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/qtrinet-core/src/engine.rs` | 0 | 4 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/qtrinet-core/gpu/qtrinet_gpu.cu` | 0 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-aiguille.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/plan-mla-vision.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/mla_synthetique.py` | 1 | 0 |

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
- … et 866 autres

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

57 sorties en erreur ou divergentes. Les premières :

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
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add -A docs/contexte-long.md REPRISE.md journal && git commit -q -F - <<'EOF' && git log --oneline -3 
- journal : archive automatique" 2>/dev/null; cd qtrinet-core && cargo test --release 2>&1 | tail -3 && cd .. && git log --oneline -9 | cat && git status --short 
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='docs/contexte-long.md'; s=open(p).read() old = """Il reste, sur ce chemin : le **dépaq
- porte gpt-oss : préciser qu'elle se mesure SANS QT_GPU  Mesuré deux fois, même binaire, même commande :   sans QT_GPU   : 15,1757 (le chiffre de contrôle du dép
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='docs/contexte-long.md'; s=open(p).read() old = """2. **Le format ne change presque rie
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git add -A tools/aiguille.py reports/rapport-aiguille.md qtrinet-core/src && git commit -q -F - <<'EOF' &&
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='docs/contexte-long.md'; s=open(p).read() old = """Il reste, sur ce chemin : le **dépaq
- REPRISE : feuille de route réécrite et pièges des variables d'environnement  La section « Ce qu'il faut faire ensuite » datait d'avant les deux campagnes : ses 
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='docs/contexte-long.md'; s=open(p).read() old = """Il reste, sur ce chemin : la réparti
- cat /tmp/rotation_16k.log; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='docs/contexte-long.md'; s=open(p).read() old = """Il reste,
- docs : plan détaillé pour MLA et la vision (chantier 5)  MLA n'est pas testable en l'état (aucun modèle MLA en GGUF ici — le deepseek-r1-distill local est un Qw
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && git log -1 --format=%B | tail -4 && cat > /tmp/msg_plan.txt <<'EOF' docs : plan détaillé pour MLA et la vi
- journal : archive automatique" 2>/dev/null; git log --oneline -3 | cat
- cat /tmp/rotation_16k.log; cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='docs/plan-mla-vision.md'; s=open(p).read() old = "### Valid
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='docs/plan-mla-vision.md'; s=open(p).read() old = """### État du harnais : FAIT""" new 
- vision : relevé du projecteur mmproj (paramètres et nommage réels)  Le fichier est en architecture \`clip\` et contient la tour COMPLÈTE (519 tenseurs, \`v.blk.
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='REPRISE.md'; s=open(p).read() old = "| 2 | seuil de rotation YaRN | **fait, seuil corr
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='docs/plan-mla-vision.md'; s=open(p).read() old = """Les tenseurs sont nommés `v.blk.N.
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='docs/plan-mla-vision.md'; s=open(p).read() old = """### Ce qu'il faut écrire, dans l'o
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && python3 - <<'PY' p='docs/plan-mla-vision.md'; s=open(p).read() old = """### ÉTAT : première tranche FAITE 
- vision : détailler le pas suivant (couche, rotation 2-D, attention locale, injection)  Le plan dit maintenant, étape par étape, ce qui reste à écrire pour le co

