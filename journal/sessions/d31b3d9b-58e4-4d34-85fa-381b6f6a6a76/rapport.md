# Session d31b3d9b — Où en est-on

| | |
|---|---|
| Identifiant | `d31b3d9b-58e4-4d34-85fa-381b6f6a6a76` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-08 09:11 |
| Durée | 4.3 h |
| Tours | 7 |
| Messages | 356 |
| Appels d'outils | 358 |
| Fichiers touchés | 11 |
| Commandes | 267 |
| Sous-agents | 3 |
| Commits | 9 |
| Compactages de contexte | 0 |

## Objectifs déclarés

- **create** — Produire un modèle nativement événementiel qui soit à son meilleur dans l'architecture de Drave : parcimonie ENTRAÎNÉE (décharge/LIF ou parcimonie structurée), exécutable en listes d'événements, et découpable en unités de travail autonomes plaçables sur les unités d'une machine (cœurs, GPU, disque) 
… [348 caractères tronqués]
- **pause** — Produire un modèle nativement événementiel qui soit à son meilleur dans l'architecture de Drave : parcimonie ENTRAÎNÉE (décharge/LIF ou parcimonie structurée), exécutable en listes d'événements, et découpable en unités de travail autonomes plaçables sur les unités d'une machine (cœurs, GPU, disque) 
… [348 caractères tronqués]

## 1. Ce qui a été demandé

**Tour 1** — où en est-on

**Tour 2** — ça fait plusieurs jours qu'on est sur des travaux lourds avec peu de résultats constructifs. Il faut revenir à l'essence de Drave et produire un modèle qui est à son meilleur dans une architecture événementielle facilement distribuable sur les divers types d'unité de traitement et ressources d'une machine et de plusieurs machines en réseau.

**Tour 3** — <goal_round> Objective: "Produire un modèle nativement événementiel qui soit à son meilleur dans l'architecture de Drave : parcimonie ENTRAÎNÉE (décharge/LIF ou parcimonie structurée), exécutable en listes d'événements, et découpable en unités de travail autonomes plaçables sur les unités d'une machine (cœurs, GPU, disque) puis sur plusieurs machines en réseau. Chaque affirmation porte sa mesure : … [816 caractères tronqués]

**Tour 4** — <goal_round> Objective: "Produire un modèle nativement événementiel qui soit à son meilleur dans l'architecture de Drave : parcimonie ENTRAÎNÉE (décharge/LIF ou parcimonie structurée), exécutable en listes d'événements, et découpable en unités de travail autonomes plaçables sur les unités d'une machine (cœurs, GPU, disque) puis sur plusieurs machines en réseau. Chaque affirmation porte sa mesure : … [816 caractères tronqués]

**Tour 5** — Hypothèse de changement de configuration matériel : Si je déploie ce projet sur une station de travail bi-processeur (Xeon E5-2687W v3) sous Linux, configurée avec une topologie NUMA asymétrique stricte pour séparer le système du calcul intensif.  Voici la ségrégation matérielle exacte de la machine : - Nœud NUMA 0 (OS & Tâches de fond) : CPU 0, 32 Go de RAM, SSD NVMe système, et GPU AMD dédié à l … [403 caractères tronqués]

**Tour 6** — je viens de commander une carte pcie pour 4 nvme 4x4 et 4 unités Patriot P320 256GB PCIe Gen 3x4 M.2 2280 SSD pour aller dessus. je compte mettre cet array de nvme sur le même noeud que les gpu, déplacer aussi le nvme existant pour le mettre sur l'autre noeud avec une carte graphique amd 100-c44971-00 pour avoir un noeud xeon de travail et un noeud os et desktop. je maintiens la topologie ram actu … [16 caractères tronqués]

**Tour 7** — le ram est actuellement hors de prix. je t'ai fait évaluer une approche asymétrique, mais c'est déconseillé. Que peut-on faire pour le ram.

## 2. Déroulé, étape par étape

### Tour 1 — où en est-on

*32 appels d'outils.* Actions notables :

- bash — Show git status and recent commits
- bash — List top-level files
- bash — Check sizes and diff stat of modified files
- bash — List most recent reports and sprints
- read
- bash — Show diff of journal metadata files
- get_goal
- bash — Diff tool changes and inspect new script
- bash — Read head of REPRISE.md status file
- bash — Read tail of latest session digest
- bash — List state sections in REPRISE.md
- bash — Find DRVF readers and running processes
- bash — List REPRISE.md section headings
- bash — List recent docs and commit dates
- … et 17 autres

**Synthèse produite :**

⏵ Point complet sur l'état du projet Drave

\## Où on en est — 08/10 09:12

**Dernière activité** : hier soir 21h14 (session `bbd6969f`, 222,5 h, archivée dans le journal). Dépôt sur `7d32b4f`, **aucun job en cours**, portes vertes (`portes.sh` exit 0, 77 tests cargo).

\### Les trois chantiers du mandat en cours

| chantier | état | ce qui le dit |
|---|---|---|
| **1. Écart froid/chaud de la passe K3** | ✅ **clos** | La mesure « une moitié de modèle » (47 couches) tranche : `sda` occupé **85,3 %**, CPU **31 %**, **367 Go/h**, 554 s. Le temps de la passe est le temps de **lire les octets**. Rien d'autre. |
| **2. Regroupement par expert / critère « 4 jetons < 10 min »** | ❌ **impossible à un nœud** | Le regroupement **existait déjà** (`MoeK3::avant_lot`) — le levier est la **taille du lot**, pas le code. Et la loi des octets `79,0 + 31,9·T Gio` (validée sur 3 points, §11) interdit le critère : 4 jetons = 206,6 Gio à 133 Mio/s. |
| **3. Grappe, un nœud = une plage de couches** | ✅ **fait, porte tenue au bit près** | Commit `3c2b542` : 2 plages + monolithe, sorties **identiques au bit**. Mais « 2,5 min/passe » demande **11 nœuds** — c'est une extrapolation, pas une mesure. Transport réseau encore par **fichier**, et la porte n'a été tenue que pour **deux** plages. |

\### En chantier, non commité (l'heure finale d'hier)

**Un vrai bug, trouvé par comparaison moteur/GPU** : le moteur quantifie chaque enregistrement DRVF v2 sur 127 niveaux (`round(v/s)`) et range `s` dans l'en-tête… que **les lecteurs du dépôt ignoraient**. Preuve : le rapport de normes passe de **×100 à ×1,003** une fois l'échelle appliquée (cosinus couche 0 : 0,849 → 0,864).

- corrigé **seulement** dans `tools/premiere_couche_semantique.py`, avec `--sans-echelle` pour mesurer l'écart — **non commité** ;
- **15 autres outils** lisent toujours les entiers ±127 comme des valeurs physiques (`profil_couches`, `localite_couches`, `invariance_unites`, `pont_*`, `cache_pont`, `sonde_pont`, `compare_professeurs`…) ;
- **l'impact sur le résultat publié n'est pas mesuré** : la « bande sémantique 10–15 » (`rapport-cycle-rapide.md`, commits `8b232d0`/`9eb9732`) a été calculée avec le lecteur bogué, et les caches `/tmp/pcs_*.sans_echelle.npz` n'existent pas → la session s'est arrêtée juste avant.

**Deux autres fichiers en attente** : `tools/trace_gpu.py` (nouveau — traçage du professeur sur GPU dans le format du moteur, calibré hier 21h11 ; sa propre note dit qu'il faut passer en **DRVF v3** pour les éche
… [425 caractères tronqués]

### Tour 2 — ça fait plusieurs jours qu'on est sur des travaux lourds avec peu de résultats constructifs. Il faut revenir à l'essence … [222 caractères tronqués]

*107 appels d'outils.* Actions notables :

- sous-agent — Inventaire parcimonie événementielle
- sous-agent — Inventaire du travail modèle
- sous-agent — Inventaire capacités de distribution
- read
- bash — Search spiking-related work in repo
- bash — Check corpora, torch and GPU availability
- bash — Read imposed-sparsity and campaign reports
- bash — Check training code and Python env packages
- bash — Locate available text corpora
- list_agents
- job_list
- bash — Read push/pull crossover report
- bash — Inventory corpora and HF cache
- bash — Inspect token id format and tokenizers
- … et 88 autres

**Synthèse produite :**

⏵ Cycle 1 bouclé et commité : la cible se déplace, et c'est la mesure qui la déplace

\## Ce que le banc a établi (dim 192, 100 Mo, 20 000 pas, meilleur point de validation)

| modèle | val (bits/octet) | densité | coût |
|---|---|---|---|
| **dense (jumeau)** | **2,2572** | 1,00 | 1,77 M MACs/jeton |
| décharge, poids valués | 3,2128 | 0,16 | 0,29 M événements |
| décharge, poids binaires | 3,4924 | 0,18 | 0,32 M événements |
| décharge, poids ternaires | 3,5091 | 0,17 | 0,30 M événements |

**La parcimonie s'entraîne** — c'était la question ouverte du dépôt, et elle est tranchée : R̂ = 0,17 obtenu par l'entraînement, réglable jusqu'à 0,03 par le seuil, là où la parcimonie *imposée* après coup plafonnait à 85 % de densité. Mais à taille égale, le dense garde ~0,9 bit/octet d'avance, et les poids signés coûtent 0,3 de plus.

\## Le chiffre qui manquait, et qui déplace la cible

J'ai fait tourner le banc du moteur (binaire du dépôt, `blk.0.ffn_gate.weight`, 16 fils) :

- le **pull dense est au mur mémoire** : 14,0 Go/s, soit 67 % de la bande passante mesurée (20,8 Go/s) ;
- un **événement coûte 2,9× (valué) à 4,3× (signé) un poids dense** — 0,210 et 0,305 ns contre 0,0716 ns.

Donc le « R̂ = 0,15 → 6,7× moins d'événements → ~100 tok/s » de `docs/comparaison-spiking.md` **n'est pas soutenable** : à R̂ = 0,17, le gain réel de temps est ≈ 1,4×, pas 6,7×. Et le push *signé* est aujourd'hui plus lent par événement que le push valué, alors qu'il stocke 1 bit au lieu de 8 — un défaut de noyau (`FusedSign` n'a pas reçu le traitement AVX2 du push int8), pas une loi de la nature.

**Et le constat qui commande la suite** : à 1,9 M paramètres, le modèle dense tient dans le cache et le chemin par listes n'a structurellement rien à gagner. L'avantage de Drave — ne lire que ce qui parle — n'existe que sur un modèle **plus gros que la mémoire**, avec une activité par jeton minuscule. C'est exactement la leçon du disque de Kimi-K3, et ça recentre tout : un modèle « à son meilleur dans Drave » se mesure en **octets lus par jeton**, pas en MACs ni en événements.

\## La suite, dans cet ordre

1. **Banc 2 — gros modèle, activité minuscule, routé par blocs** : paramètres ≫ cache, quelques pour cent actifs par jeton, mesure en octets/jeton contre un dense à *même lecture d'octets* (c'est la comparaison honnête).
2. **Distillation depuis Qwen2.5-0.5B** (sur le disque, jamais utilisée dans ce dépôt) pour payer la qualité du routage.
3. **Noyau signé** : chronométrer `FusedSign` optim
… [563 caractères tronqués]

### Tour 3 — <goal_round> Objective: "Produire un modèle nativement événementiel qui soit à son meilleur dans l'architecture de Drave … [1096 caractères tronqués]

*95 appels d'outils.* Actions notables :

- bash — Check workspace and resources state
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/essai_blocs.py`
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/essai_blocs.py`
- bash — Smoke test block-routed bench
- bash — Locate cache and family lines
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/essai_blocs.py`
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/essai_blocs.py`
- bash — Show family loop for edit
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/essai_blocs.py`
- bash — Smoke test iso-reads routed bench
- bash — Launch routed-model experiments on both GPUs
- bash — Check engine MoE architecture support
- bash — Look for a GGUF writer in the repo
- bash — Read the repo's GGUF writer
- … et 80 autres

**Synthèse produite :**

⏵ Réponse chiffrée sur la ségrégation NUMA, à partir des mesures du dépôt

\## Réponse courte

**Une partie est bénéfique, une autre est probablement contre-productive, et la raison invoquée — le QPI — n'est pas le goulot sur cette machine.** Le dépôt a déjà mesuré les trois régimes qui comptent, et ils ne répondent pas de la même façon.

\## Ce que la machine mesure aujourd'hui

| mesure | valeur | source |
|---|---|---|
| distances NUMA | 10 local / **21 distant** (2,1×) | `numactl --hardware` |
| RAM | **64,3 / 64,4 Go symétrique** (libre : 2,6 / 0,4 Go — page cache) | idem |
| calcul pur, nœud 0 vs nœud 1 | 13,8 vs 14,2 Go/s → **3 %, du bruit** | `REPRISE.md:1523` |
| lecture NVMe, nœud 0 vs nœud 1 | 22,41 vs 21,45 Go/s → **4 %** | `REPRISE.md:1524` |
| **épinglage sur UN socket, charge réelle** (30B MoE) | **23,2 → 27,6 s, soit −19 %** | `docs/convertisseur.md:192` |
| banc mémoire, lié à un socket | 20,7 → **24,7 Go/s** | `docs/convertisseur.md:101` |
| 20 cœurs / +hyperthreads | 22,5 / 18,9 Go/s | plan du moteur |
| NVMe 16 lecteurs | 5,4 → **31,1 Go/s** | idem |
| passe Kimi-K3 | `sda` occupé **87,6 %**, CPU **21 %**, 133 Mio/s (plafond 205) | `rapport-passe-k3-disque.md` |

Les deux dernières lignes sont la clé : **la passe lourde du projet est liée au disque, pas à l'interconnexion.** Pendant 26 minutes, le CPU est à 21 % — le QPI est quasiment au repos. Le séparer ne rapporte rien ; c'est le **motif d'accès disque** qui laisse 35 % sur la table (133 contre 205 Mio/s).

\## Pourquoi le QPI n'est pas votre goulot

Les deux seules mesures « inter-nœuds » du dépôt donnent 3 % et 4 % — de l'ordre du bruit de cette machine. Et surtout, l'expérience qui devait montrer le coût du QPI montre l'inverse : **restreindre un calcul au seul socket 1 le ralentit de 19 %**. La ressource rare n'est pas la liaison entre processeurs, c'est **la bande passante mémoire d'un socket**. Le micro-banc dit le contraire (20,7 → 24,7 Go/s en liant un socket) parce qu'il fait un flux unique : une charge réelle a beaucoup de flux simultanés et a besoin des deux contrôleurs mémoire.

\## Ce que votre ségrégation apporte réellement

1. **La reproductibilité des mesures — et c'est le gain le plus solide.** Le dépôt le répète partout : « la machine portait une charge de fond (bureau, autres projets) qui fait varier le temps mur de 30 % », et plusieurs campagnes ont dû être refaites sous charge 8-14. Isoler le bureau et l'affichage sur le nœud 0 rend les chiffres reproductibles. **Bén
… [3380 caractères tronqués]

### Tour 4 — <goal_round> Objective: "Produire un modèle nativement événementiel qui soit à son meilleur dans l'architecture de Drave … [1096 caractères tronqués]

*76 appels d'outils.* Actions notables :

- bash — Check trained model and bench outcome
- bash — Check bench process state
- bash — Kill diverged bench and start dense twin
- bash — Stop leftover bench, confirm dense twin running
- bash — Export trained routed model to GGUF
- bash — Run reference and engine on trained routed model
- bash — Run formal gate on trained routed model
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/exporter_gguf.py`
- bash — Simplify exporter flags
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-reparti-moteur.sh`
- bash — Run the distributed gate on our trained model
- bash — Inspect distributed run output in detail
- bash — Compare truncated vs full model perplexity
- bash — Verify the reference flux gate is green
- … et 60 autres

**Synthèse produite :**

⏵ Erreur plus grave : le décalage double était aussi dans la **boucle d'entraînement**

### Tour 5 — Hypothèse de changement de configuration matériel : Si je déploie ce projet sur une station de travail bi-processeur (Xe … [683 caractères tronqués]

*33 appels d'outils.* Actions notables :

- bash — Check background work and machine state
- bash — Prepare interleaved NUMA A/B script
- bash — Run interleaved NUMA A/B on real workload
- bash — Re-run NUMA A/B with bash timing
- bash — Inspect GPU/PCIe topology and NVLink
- bash — Locate big models and disks
- bash — Map disks to NUMA nodes and locate K3 model
- bash — Measure sequential read ceilings of both disks
- bash — Find large files for disk benchmarks
- bash — Measure both disks sequential read
- bash — Check routed training and load
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/numa-segregation.md`
- bash — Verify cited numbers in the document
- bash — Verify PCIe root complex for each GPU
- … et 18 autres

**Synthèse produite :**

⏵ Document NUMA livré et commité ; je fais le point sur l'objectif

\## Le document demandé

**`docs/numa-segregation.md`** (207 lignes, commit `29a68c8`) répond à la question avec des mesures faites **sur cette machine aujourd'hui**, pas des principes.

**Réponse en trois lignes :**

1. **Séparer l'OS, le bureau et l'affichage du calcul : bénéfique** — pour la reproductibilité des mesures (le dépôt note jusqu'à 30 % de variation du temps mur à cause de la charge de fond) et pour la VRAM rendue au moteur. Pas pour le QPI.
2. **Forcer le calcul sur un seul socket : coûteux, et mesuré.** J'ai lancé un A/B entrelacé (3 répétitions, charge réelle, Qwen 0.5B) :

| configuration | médiane | écart |
|---|---:|---:|
| A — défaut (20 fils, aucune liaison) | 15 365 ms | — |
| **B — nœud 1 seul (10 fils, mémoire nœud 1)** | **16 614 ms** | **+8,1 %** |
| C — nœud 1, mémoire entrelacée | 16 474 ms | +7,2 % |
| D — deux nœuds, mémoire entrelacée | 15 225 ms | −0,9 % |

La proposition est **la plus lente des quatre**, et le dépôt avait déjà mesuré pire sur un 30B MoE (`--pin` : 23,2 → 27,6 s, −19 %). Le facteur limitant n'est pas la liaison QPI (3 à 4 % d'écart entre nœuds en calcul pur et en lecture NVMe) mais **la bande passante mémoire d'un socket**.

3. **Le goulot réel est le disque.** Mesuré aujourd'hui en lecture directe : **246 Mo/s** sur le disque dur `sda` contre **1 600 Mo/s** sur le NVMe — facteur 6,5, qui décide d'une passe de 26 minutes. Le document note aussi que la page cache ne retient pas le dense de Kimi-K3 (déjà mesuré : 1 516 430 puis 1 522 584 ms), donc les 128 Go n'achètent pas ce qu'on croit, et que le NVMe actuel est plein à 97 %.

Il contient aussi la topologie relevée (distances NUMA 10/21, 64/64 Go symétrique, **les deux Quadro déjà sur le nœud 0, sur deux root complexes distincts**, NVLink 25,781 Go/s), les recommandations, les réserves, et un protocole à trois mesures entrelacées si la configuration proposée est retenue.

\## Et l'objectif, pendant ce temps

Deux portes ont été franchies et sont commitées (`a9f4b40`) :

- **Porte d'exécution** : un Qwen3-MoE **entraîné ici** tourne dans Drave — 5,3397 de perplexité contre 5,3585 pour la référence à poids quantifiés identiques, corrélation des logits min 0,9906, top-1 95,7 %, `compare_logits --porte` **exit 0**.
- **Porte de répartition** : deux processus, deux plages de couches — **3,9020 = 3,9020**, écart de flux 0,00e0, écart relatif **0,0000 %**.
- **À lecture égale** (2,3 M poids/jeton, v
… [892 caractères tronqués]

### Tour 6 — je viens de commander une carte pcie pour 4 nvme 4x4 et 4 unités Patriot P320 256GB PCIe Gen 3x4 M.2 2280 SSD pour aller … [296 caractères tronqués]

*9 appels d'outils.* Actions notables :

- bash — Inspect PCIe link widths for GPUs and NVMe
- bash — Check DIMM population
- bash — Try verbose lspci and EDAC DIMM data
- bash — Read PCIe link widths and measure memory bandwidth
- bash — Check NVMe contents and capacity
- web_search
- bash — Measure PCIe link speed under GPU load
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/numa-segregation.md`
- bash — Commit the array analysis section

**Synthèse produite :**

⏵ Analyse terminée et ajoutée au document (§11) — voici l'essentiel

\## Le plan est bon sur le placement, mais trois contraintes mordent avant lui

J'ai ajouté une section au document (`docs/numa-segregation.md` §11, commit `42ea1ae`). Ce qui est juste d'abord : **l'array sur le nœud des GPU, l'OS/affichage isolés de l'autre côté, la RAM symétrique** — c'est exactement ce que les mesures recommandaient. Et les P320 annoncent 2 200 Mo/s, soit ~5× le NVMe actuel (mesuré **1,6 Go/s**) et ~9× le disque dur (**246 Mo/s**).

\### 1. Les lignes PCIe — c'est là que ça coince

Le Xeon E5-2687W v3 donne **40 lignes PCIe 3.0 par socket**. Relevé à l'instant sur le nœud 0 :

| périphérique | liaison | max |
|---|---|---|
| Quadro RTX 5000 (`03:00.0`) | **x16** (2,5 → 5,0 GT/s selon la charge) | x16 Gen3 |
| Quadro RTX 5000 (`04:00.0`) | **x16** (2,5 → 8,0 GT/s) | x16 Gen3 |
| NVMe système (`02:00.0`, MAP1602) | x4 Gen3 | x4 Gen4 |

**36 lignes sur 40 sont déjà prises.** Une carte 4×NVMe x16 en demande 16 de plus : **52**. Il faudra choisir, et ce choix se fait au BIOS :

- **GPU en x8 + carte en x16** : l'array est complet, mais chaque GPU perd la moitié de sa bande passante hôte (le dépôt a mesuré **6,5 Go/s en x8**) — et c'est ce trafic qui porte le miroir du cache KV, donc le « 22,16 → 3,29 ms/jeton ».
- **GPU en x16 + carte en x4** : les 4 SSD partagent ~3,9 Go/s, soit **le débit d'un seul**. L'array ne sert à rien.

Deux vérifications à faire **avant** de tout démonter : la **bifurcation `x4x4x4x4`** du slot choisi (les cartes passives l'exigent ; sans elle, **un seul SSD apparaît**), et que ce slot est bien câblé au **CPU** — derrière le PCH, c'est du x4 Gen2 partagé, ~2 Go/s pour les quatre. Et c'est le slot qui décide du nœud : si le seul x16 libre est câblé au CPU 1, l'array sera sur le nœud 1, pas avec les GPU.

\### 2. Les canaux mémoire — la moitié est vide

EDAC le dit sans ambiguïté : **2 DIMM par socket, sur un contrôleur à 4 canaux**. Deux canaux sur quatre sont vides, et la bande passante mesurée aujourd'hui le confirme : **20,4 Go/s** (64 Mo, 16 threads) — un ordre de grandeur de dual-channel.

Donc « je maintiens 2×32 + 2×32 » = **la moitié de la bande passante mémoire de la machine**, dans le régime même que le placement NUMA ne rattrape pas (§3 : forcer un socket coûte 8 à 19 %). Passer à **4 DIMM par socket** doublerait à peu près cette bande passante. C'est probablement le meilleur gain par dollar de toute la liste, et il n'est pas dans le plan.


… [1410 caractères tronqués]

### Tour 7 — le ram est actuellement hors de prix. je t'ai fait évaluer une approche asymétrique, mais c'est déconseillé. Que peut-on … [19 caractères tronqués]

*6 appels d'outils.* Actions notables :

- bash — Check uncore, governor, THP settings
- bash — Check swap, memory sysctls and zram
- bash — Read swap settings and biggest swap users
- bash — Measure memory bandwidth under three placements
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/numa-segregation.md`
- bash — Commit the RAM section

**Synthèse produite :**

⏵ La RAM est chère : je regarde ce qui est récupérable gratuitement avant de recommander un achat

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/essai_decharge.py` | 2 | 20 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/corpus_wikipedia.py` | 2 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-parcimonie-entrainee.md` | 1 | 3 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/essai_blocs.py` | 1 | 5 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/exporter_gguf.py` | 1 | 18 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte_moteur.py` | 1 | 4 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/entrainer_moteur.py` | 1 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-reparti-moteur.sh` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs` | 0 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/numa-segregation.md` | 1 | 3 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-modele-moteur.md` | 1 | 0 |

### Sous-agents lancés

- tour 2 — Inventaire parcimonie événementielle
- tour 2 — Inventaire du travail modèle
- tour 2 — Inventaire capacités de distribution

### Commandes exécutées (échantillon)

- **T1** Show git status and recent commits
- **T1** List top-level files
- **T1** Check sizes and diff stat of modified files
- **T1** List most recent reports and sprints
- **T1** Show diff of journal metadata files
- **T1** Diff tool changes and inspect new script
- **T1** Read head of REPRISE.md status file
- **T1** Read tail of latest session digest
- **T1** List state sections in REPRISE.md
- **T1** Find DRVF readers and running processes
- **T1** List REPRISE.md section headings
- **T1** List recent docs and commit dates
- **T1** Read the rapid-cycle report intro
- **T1** Check which tools handle per-record scale
- **T1** Count tools and show recently modified
- **T1** Inspect scale handling in key readers
- **T1** Search echelle usage in readers
- **T1** Check temp caches from recent runs
- **T1** Read end of new GPU tracer script
- **T1** Search digest for calibration and scale-fix mentions
- **T1** Check rapid-cycle report conclusions
- **T1** Read half-model measurement logs
- **T1** Read K3 disk-pass report conclusion
- **T1** Extract latest session objective text
- **T1** Read last tour summary in session report
- **T1** Find readers that apply the record scale
- **T1** Inspect last commit and gates status
- **T1** Locate raw DRVF record parsers in tools
- **T1** Check gates log and count affected tools
- **T2** Search spiking-related work in repo
- **T2** Check corpora, torch and GPU availability
- **T2** Read imposed-sparsity and campaign reports
- **T2** Check training code and Python env packages
- **T2** Locate available text corpora
- **T2** Read push/pull crossover report
- **T2** Inventory corpora and HF cache
- **T2** Inspect token id format and tokenizers
- **T2** Check engine support for binary/ternary events
- **T2** Inspect corpus file formats
- **T2** Check English corpus size
- … et 227 autres

## 4. Mesures et résultats marquants

- **T1** `6df6de4 §10 : le palier NVMe donne −8,8 %, la prédiction était de −16,3 %`
- **T1** `3169941 Attribution des 206,58 Gio : 72 % sont les experts, relus à chaque jeton`
- **T1** `d186466 §94 : rang 1, 2 ou 3 — le meilleur rang n'est pas celui du meilleur chiffre`
- **T1** `df8980e §92 : la pire paire après échelle — de–en à 486 % du professeur, mais 5 paires sur 15 échouent`
- **T1** `| `8e04c99a` | 2026-09-30 18:17 | 0.7 Mo | 118 Ko | 1 | 59 | 85 | 0 | 0 |`
- **T1** `| `aa5f9fc5` | 2026-09-30 15:17 | 0.8 Mo | 129 Ko | 1 | 78 | 100 | 0 | 0 |`
- **T1** `| `b13a6032` | 2026-10-02 15:09 | 0.3 Mo | 88 Ko | 1 | 17 | 43 | 0 | 0 |`
- **T1** `-| `bbd6969f` | 2026-10-07 20:45 | 56.7 Mo | 8968 Ko | 205 | 9596 | 9018 | 63 | 26 |`
- **T1** `+| `bbd6969f` | 2026-10-07 21:14 | 56.9 Mo | 9009 Ko | 205 | 9630 | 9050 | 63 | 26 |`
- **T1** `| `bcfe0b97` | 2026-09-30 12:39 | 1.0 Mo | 145 Ko | 1 | 102 | 110 | 0 | 0 |`
- **T1** `| `c25f97d1` | 2026-09-30 11:59 | 0.8 Mo | 126 Ko | 1 | 73 | 104 | 0 | 0 |`
- **T1** `| `c776b71f` | 2026-09-30 18:43 | 0.7 Mo | 82 Ko | 1 | 35 | 54 | 0 | 0 |`
- **T1** `| `fba448b3` | 2026-10-02 15:10 | 0.5 Mo | 39 Ko | 1 | 19 | 26 | 0 | 0 |`
- **T1** `| `ff364db0` | 2026-10-01 05:58 | 0.5 Mo | 120 Ko | 1 | 63 | 75 | 0 | 0 |`
- **T1** `-Total : 99.0 Mo de traces brutes.`
- **T1** `+Total : 99.2 Mo de traces brutes.`
- **T1** `+⏵ **PREUVE : les normes passent de ×100 à ×1,003 une fois l'échelle appliquée. Nos lecteurs l'ignorent depuis toujours. Je quantifie l'impact sur le résultat publié.**`
- **T1** `- **T1** : 511 tokens notés — perplexité cumulée 247.031  (4.9 tok/s) === perplexité 247.0308 sur 511 tokens (0 événements, 104.5 s) ===  ### B3 harmony assistant 511 --- ref --- 0.0 0.0 0:00 ls: cann`
- **T1** `+    le rapport de normes va de ×6 à ×100 selon la couche ; avec, il tombe entre`
- **T1** `> Budget par jeton **mesuré** : **86,787 Go** — experts routés 25,830 (29,8 %),`
- **T1** `> dense 60,958 (70,2 %). Le dense pèse 2,3× les experts : aucune technique sur`
- **T1** `> les experts n'adresse plus de 30 % du trafic d'un jeton.`
- **T1** `> sans avoir jamais été mesuré, vaut **×1,58** (Qwen3-30B-A3B, invite de`
- **T1** `> refermés (« paires experts » tombait à 1 % dès le lot 2), et `forward_lot``
- **T1** `> **11 % de CPU** (borné par le disque : 1,80 To lus, 451 Go/jeton, 5,2 balayages`
- **T1** `>   trace** — 25 à 60 % des positions sur la donnée à une unité, 3 % à dix unités.`
- **T1** `⏵ **PREUVE : les normes passent de ×100 à ×1,003 une fois l'échelle appliquée. Nos lecteurs l'ignorent depuis toujours. Je quantifie l'impact sur le résultat publié.**`
- **T1** `1290:#    moteur déporte alors tout seul les projections Q8_0 de plus de 8 Mo — le`
- **T1** `1295:#    du même ordre que les 0,06 % mesurés alors — non re-mesuré depuis.)`
- **T1** `1512:# attendu : CPU 20,9 Go/s · GPU ligne par fil 41,9 · GPU warp par ligne 84,9`
- **T1** `1595:### L'engram : 16 ms par entrée sur le disque mécanique`
- **T1** `6df6de4 07/10 18:11 §10 : le palier NVMe donne −8,8 %, la prédiction était de −16,3 %`
- **T1** `| ajustement d'un pont | **5 à 10 min** sur 1 446 entrées × 575 positions, parce que la Grammaire `AᵀA` coûte `n·d²` avec `d = 1 792` |`
- **T1** `- **diviser `d` par 1,5** (un modèle de 576 cachés au lieu de 896) gagne **×2,4** ;`
- **T1** `- **diviser `n` par 20** (une phrase au lieu d'un article) gagne **×20**.`
- **T1** `26884:⏵ Trace DRVF v3 : valeurs i8 + échelle f16 par bloc (l'étude déléguée annonce −63 % ; je vérifie).`
- **T1** `27144:ae85043 DRVF v3 : −66 % de trace au total, pour +0,074 % de perplexité`
- **T1** `| traçage article 1 (399 langues × 24 couches) | **26 min** |`
- **T1** `| traçage article 2 (399 langues × 24 couches) | **48 min** |`
- **T1** `#    occupé                                  473 s   (85.3%)`
- **T1** `#    occupé, pondéré par les files         12578 s   (2270.4%)`
- **T1** `#   LE DISQUE. `sda` est occupé 85% du temps et le CPU ne`
- **T1** `#   travaille que 31% : le temps de la passe est le temps de LIRE les`
- **T1** `#   octets au débit du disque. Vérification : 56.5 Go à 0 Mo/s`
- **T1** `couche 41 :   2254 ms de chargement +  14302 ms de calcul · banque 4`
- **T1** `couche 42 :   1619 ms de chargement +  14274 ms de calcul · banque 4`
- **T1** `couche 43 :   3285 ms de chargement +  12625 ms de calcul · banque 4`
- **T1** `couche 44 :   1619 ms de chargement +  15101 ms de calcul · banque 4`
- **T1** `couche 45 :   1738 ms de chargement +  15464 ms de calcul · banque 4`
- **T1** `couche 46 :   1851 ms de chargement +  12578 ms de calcul · banque 4`
- **T1** `---- chargement 69.0 s (15 %) · calcul 394.9 s (85 %) [attention 90.3 s · FFN 304.6 s]`
- **T1** `passe complète : 466359 ms au total`
- **T1** `bit près, et le relais qui circule entre deux nœuds fait 142 ko par saut.`
- **T1** `La couche 0 a une séparation **nulle** (+0,001) : le même texte dans deux langues ne se ressemble pas plus que deux textes différents. La couche 13 a **+0,034**, et les couches **10 à 15 forment un pl`
- **T2** `avons mesuré le contraire sur un LLM dense : **0,00 % d'activations nulles**, donc`
- **T2** `| 0,1 % | 343,8 M (−2,6 %) | 19,5750 | 1,02× |`
- **T2** `| 0,2 % | 334,9 M (−5,1 %) | 19,6502 | 1,02× |`
- **T2** `| 0,5 % | 312,3 M (−11,5 %) | 20,1511 | 1,05× |`
- **T2** `| 1,0 % | 281,1 M (−20,3 %) | 22,2286 | 1,15× |`
- **T2** `| 2,0 % | 230,8 M (−34,6 %) | 30,5837 | 1,59× |`
- **T2** `| 5,0 % | 145,0 M (−58,9 %) | **2264,84** | **117×** |`
- **T2** `➡️ Économiser 11 % d'événements coûte 5 % de perplexité, et au-delà de 2 % le`
- **T2** `| 100 % | 354,3 M | 23,6125 | 26,2565 |`
- **T2** `| 90 % | 319,1 M (−9,9 %) | 23,6790 (+0,28 %) | 26,2950 (+0,15 %) |`
- **T2** `| 85 % | 301,5 M (−14,9 %) | 23,7468 (+0,57 %) | 26,5785 (+1,23 %) |`
- **T2** `| 80 % | 283,7 M (−19,9 %) | 23,8251 (+0,90 %) | 26,8586 (+2,29 %) |`
- **T2** `➡️ **À sparsité comparable, le k-WTA coûte dix fois moins que le seuil** : −15 %`
- **T2** `d'événements pour +0,6 à +1,2 % de perplexité, contre +4,6 % pour le seuil à`
- **T2** `−11 %. La raison est simple : un seuil relatif au *maximum* coupe d'autant plus`
- **T2** `| **poids d'attention** (top-k clés) | **améliore** de 0,5 à 1,2 % | ✅ à garder |`
- **T2** `| activations du FFN (k-WTA 90 %) | +0,15 à +0,28 % | ✅ acceptable |`
- **T2** `| activations du FFN (k-WTA 85 %) | +0,5 à +1,2 % | ⚠️ selon le budget |`
- **T2** `| entrée des projections d'attention (90 %) | +0,06 % | ✅ quasi gratuit |`
- **T2** `| **Q et K** (après RoPE) | ×2,2 à 50 %, ×36 à 25 % | ❌ intouchable |`
- **T2** `| activations du FFN (seuil absolu) | ×117 à 5 % du max | ❌ inutilisable |`
- **T2** `**Attention à 32 clés + projection `gate` à 85 %.**`
- **T2** `| attention 32 clés seule | 354,3 M | 23,3279 (**−1,21 %**) | 26,1178 (**−0,53 %**) |`
- **T2** `| **+ `gate` à 85 %** | **338,8 M (−4,4 %)** | 23,2811 (**−1,40 %**) | 26,1417 (**−0,44 %**) |`
- **T2** `➡️ **On améliore la qualité de 0,4 à 1,4 % tout en réduisant le flux`
- **T2** `d'événements de 4,4 %.** Ce n'est pas un compromis : les deux vont dans le même`
- **T2** `| renormalisation homéostatique après k-WTA | **dégrade** (+0,2 à +3,6 %) : le modèle préfère la troncature franche |`
- **T2** `| FFN complet à 85 % + attention creuse | **non additif, défavorable** (+0,19 % en B) |`
- **T2** `Elles donnent **exactement le même résultat** — vérifié : perplexité 19,2647 au`
- **T2** `Mesure refaite sur `blk.0.ffn_gate.weight` (4 864 × 896, 4,36 M poids), 16 threads,`
- **T2** `| 0 % | 0,004 | 0,167 | 0,03 |`
- **T2** `| 1 % | 0,019 | 0,162 | 0,12 |`
- **T2** `| 5 % | 0,047 | 0,168 | 0,28 |`
- **T2** `| **10 %** | 0,078 | 0,163 | **0,48** |`
- **T2** `| **25 %** | 0,180 | 0,163 | **1,11** |`
- **T2** `| 50 % | 0,355 | 0,165 | 2,15 |`
- **T2** `| **100 %** | 0,801 | 0,171 | **4,69** |`
- **T2** `➡️ **Les deux architectures se croisent à ~22 % de densité d'activation**, pas à`
- **T2** `10 %. Le chiffre se lit dans le rapport à pleine densité : le pull traite 4,7 fois`
- **T2** `/dev/mapper/system-root   11T  8,8T  2,1T  81% /home/stephane/Data13TB`
- **T2** `// sursouscription (mesuré : ×1,3 de perte à 40+1 threads sur 40 CPU).`
- **T2** `blk.0.ffn_gate.weight  [4864 × 896]  densité 99.2 %`
- **T2** `dense 8 bits               8.000 b/poids  (   4.36 Mo)`
- **T2** `bitmap + signe             1.992 b/poids  (   1.09 Mo)`
- **T2** `creux k=1 (signe seul)     1.992 b/poids  (   1.09 Mo)`
- **T2** `creux k=4                  4.970 b/poids  (   2.71 Mo)`
- **T2** `creux k=8                  8.939 b/poids  (   4.87 Mo)`
- **T2** `listes signées + écarts    7.975 b/poids  (   4.34 Mo)`
- **T2** `blk.0.ffn_down.weight  [896 × 4864]  densité 99.2 %`
- **T2** `creux k=4                  4.967 b/poids  (   2.71 Mo)`
- **T2** `creux k=8                  8.934 b/poids  (   4.87 Mo)`
- **T2** `listes signées + écarts    7.941 b/poids  (   4.33 Mo)`
- **T2** `blk.0.attn_q.weight  [896 × 896]  densité 99.1 %`
- **T2** `dense 8 bits               8.000 b/poids  (   0.80 Mo)`
- **T2** `bitmap + signe             1.991 b/poids  (   0.20 Mo)`
- **T2** `creux k=1 (signe seul)     1.991 b/poids  (   0.20 Mo)`
- **T2** `creux k=4                  4.964 b/poids  (   0.50 Mo)`
- **T2** `creux k=8                  8.929 b/poids  (   0.90 Mo)`
- **T2** `listes signées + écarts    7.964 b/poids  (   0.80 Mo)`
- **T2** `blk.0.attn_output.weight  [896 × 896]  densité 99.2 %`
- **T2** `bitmap + signe             1.992 b/poids  (   0.20 Mo)`
- **T2** `creux k=1 (signe seul)     1.992 b/poids  (   0.20 Mo)`
- **T2** `creux k=4                  4.968 b/poids  (   0.50 Mo)`
- **T2** `creux k=8                  8.936 b/poids  (   0.90 Mo)`
- **T2** `listes signées + écarts    7.972 b/poids  (   0.80 Mo)`
- **T2** `0.0%             0  fusion   0.00 G (0.0064 ms) | 2-listes   0.00 G (0.0062 ms)`
- … (tronqué)

## 5. Erreurs rencontrées

14 sorties en erreur ou divergentes. Les premières :

- **T1** : ```  ### 🤖 Assistant  ⏵ **En transformers 5, `AutoModel` rend directement `Qwen2Model` (pas de `.model`). Je corrige le diagnostic.**  - **bash** `{"command": "cd /home/stephane/Data13TB/stephane/GitH
- **T2** : 3310393 bash -c pgrep -af "essai_decharge" | grep python | head; echo "--- logs ---"; tail -2 /tmp/ec_d192_lr3e3.log 2>/dev/null; tail -2 /tmp/ec_d192_lr1e3.log 2>/dev/null; echo "---"; ls -la /tmp/ec
- **T2** : === /tmp/ec_lr3e3.log === === VERDICT (validation tenue à l'écart) ===   dense    :   1875072 paramètres · 2.4420 bits/octet ·    1.77 M MACs/token   décharge :   1880064 paramètres · 3.2004 bits/octe
- **T2** : println!("  pool 4 bits vs scalaire : {}",                  if pire.1 == 0.0 { "IDENTIQUE ✅".to_string() }                  else { format!("DIVERGENT rang {} (écart relatif {:.3}) ❌", pire.0, pire.1) 
- **T3** : File "/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/exporter_gguf.py", line 155, in kv_depuis_config     (f"{arch}.expert_count", int(cfg["num_experts"])),                                  ~~~
- **T3** : gu = poids[p + "mlp.experts.gate_up_proj"]      # (E, 2·ff, d)          ~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ KeyError: 'model.layers.0.mlp.experts.gate_up_proj' === en-tête vu par le moteur ===  thre
- **T3** : /tmp/moe_ids.txt : 256 tokens, fenêtres de 256 [moe] couche 0 : « blk.0.ffn_gate_exps.weight » de type F32 — format sans noyau ni déquantification  thread 'main' (3319853) panicked at src/model.rs:148
- **T3** : # /tmp/moe_test.gguf : 51 tenseurs · 6.2 Mo (f32, experts Q4_0) · 17 métadonnées # architecture 4 couches · 192 cachés · 8 experts (top-2) · norm_topk_prob=True /tmp/moe_ids.txt : 256 tokens, fenêtres
- **T3** : assert a.shape[-1] % 32 == 0, f"dernière dimension non multiple de 32 : {a.shape}"            ^^^^^^^^^^^^^^^^^^^^^ AssertionError: dernière dimension non multiple de 32 : (4, 64, 48) === le moteur ch
- **T4** : [config] mélanges d'experts chargés : 4/4 couches · mapping absent (experts en clair dans le fichier) [config] puits appris sur 0/4 couches · n_rot 48 · ffn 768 · experts 8 [config] rotation : RoPE si
- **T4** : [flux] quantification : 127 niveaux, seuil 0, top-k 0, renorm false [flux] pilote : 2 couches en local, 2 chez le pair, 128 jetons   référence locale  : perplexité 1186.5313  (0.1 s)   deux nœuds     
- **T4** : ~~~~~^^^^^^^^^^^^^^^^^^^^^^^ KeyError: 'model.layers.0.mlp.gate.weight' === charge ===  thread 'main' (3374822) panicked at src/main.rs:2427:40: === ppl dense === [exit code: 1]
- **T4** : Error: tool call aborted
- **T5** : fichier :  === NVMe === fichier :  [exit code: 1]

## 6. Commits

- Parcimonie entraînée : premier banc, et la loi du coût par événement mesurée dans le moteur  Le dépôt n'avait jamais entraîné un seul modèle (zéro rétropropagat
- Porte d'exécution : un modèle entraîné ici tourne dans Drave, logits identiques  Le moteur lit le GGUF en place et n'avait pas de convertisseur : le dépôt ne po
- Réparti : --ids-file était ignoré, et les jetons synthétiques sortaient du vocabulaire  Deux défauts trouvés en essayant de répartir le modèle entraîné ici.  1.
- entrainer_moteur : deux erreurs qui faussaient la mesure, corrigées  1. Double décalage. Le modèle HF décale lui-même (shift_logits/shift_labels) ;    lui passe
- entrainer_moteur : le double décalage était AUSSI dans la boucle d'entraînement  La correction précédente n'avait touché que l'évaluation. Le défaut était plus 
- docs/numa-segregation : la ségrégation NUMA proposée, mesurée plutôt que raisonnée  Réponse à une proposition de station bi-Xeon avec topologie asymétrique stri
- Le modèle produit ici tourne dans Drave et se découpe — les deux portes sont tenues  Porte d'exécution : un Qwen3-MoE entraîné ici (4 couches, 8 experts, top-2,
- docs/numa-segregation §11 : la carte 4xNVMe et l'AMD, chiffrées avant achat du reste  Le placement proposé est juste (array sur le nœud des GPU, OS/affichage is
- docs/numa-segregation §12 : quoi faire de la RAM quand elle est hors de prix  Trois réponses, dans l'ordre où elles paient, et toutes mesurées :  1. RÉCUPÉRER C

