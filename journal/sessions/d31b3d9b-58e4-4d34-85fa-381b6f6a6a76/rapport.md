# Session d31b3d9b — Où en est-on

| | |
|---|---|
| Identifiant | `d31b3d9b-58e4-4d34-85fa-381b6f6a6a76` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-08 09:11 |
| Durée | 12.9 h |
| Tours | 14 |
| Messages | 490 |
| Appels d'outils | 480 |
| Fichiers touchés | 19 |
| Commandes | 364 |
| Sous-agents | 3 |
| Commits | 21 |
| Compactages de contexte | 0 |

## Objectifs déclarés

- **create** — Produire un modèle nativement événementiel qui soit à son meilleur dans l'architecture de Drave : parcimonie ENTRAÎNÉE (décharge/LIF ou parcimonie structurée), exécutable en listes d'événements, et découpable en unités de travail autonomes plaçables sur les unités d'une machine (cœurs, GPU, disque) 
… [348 caractères tronqués]
- **pause** — Produire un modèle nativement événementiel qui soit à son meilleur dans l'architecture de Drave : parcimonie ENTRAÎNÉE (décharge/LIF ou parcimonie structurée), exécutable en listes d'événements, et découpable en unités de travail autonomes plaçables sur les unités d'une machine (cœurs, GPU, disque) 
… [348 caractères tronqués]
- **edit** — Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'architecture de Drave — listes d'événements, streaming depuis le disque, répartition entre nœuds — vaut pour CHAQUE famille de tâches disponible sur la machine : langage, génération et latence, contexte long, cod
… [728 caractères tronqués]
- **resume** — Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'architecture de Drave — listes d'événements, streaming depuis le disque, répartition entre nœuds — vaut pour CHAQUE famille de tâches disponible sur la machine : langage, génération et latence, contexte long, cod
… [728 caractères tronqués]

## 1. Ce qui a été demandé

**Tour 1** — où en est-on

**Tour 2** — ça fait plusieurs jours qu'on est sur des travaux lourds avec peu de résultats constructifs. Il faut revenir à l'essence de Drave et produire un modèle qui est à son meilleur dans une architecture événementielle facilement distribuable sur les divers types d'unité de traitement et ressources d'une machine et de plusieurs machines en réseau.

**Tour 3** — <goal_round> Objective: "Produire un modèle nativement événementiel qui soit à son meilleur dans l'architecture de Drave : parcimonie ENTRAÎNÉE (décharge/LIF ou parcimonie structurée), exécutable en listes d'événements, et découpable en unités de travail autonomes plaçables sur les unités d'une machine (cœurs, GPU, disque) puis sur plusieurs machines en réseau. Chaque affirmation porte sa mesure : … [816 caractères tronqués]

**Tour 4** — <goal_round> Objective: "Produire un modèle nativement événementiel qui soit à son meilleur dans l'architecture de Drave : parcimonie ENTRAÎNÉE (décharge/LIF ou parcimonie structurée), exécutable en listes d'événements, et découpable en unités de travail autonomes plaçables sur les unités d'une machine (cœurs, GPU, disque) puis sur plusieurs machines en réseau. Chaque affirmation porte sa mesure : … [816 caractères tronqués]

**Tour 5** — Hypothèse de changement de configuration matériel : Si je déploie ce projet sur une station de travail bi-processeur (Xeon E5-2687W v3) sous Linux, configurée avec une topologie NUMA asymétrique stricte pour séparer le système du calcul intensif.  Voici la ségrégation matérielle exacte de la machine : - Nœud NUMA 0 (OS & Tâches de fond) : CPU 0, 32 Go de RAM, SSD NVMe système, et GPU AMD dédié à l … [403 caractères tronqués]

**Tour 6** — je viens de commander une carte pcie pour 4 nvme 4x4 et 4 unités Patriot P320 256GB PCIe Gen 3x4 M.2 2280 SSD pour aller dessus. je compte mettre cet array de nvme sur le même noeud que les gpu, déplacer aussi le nvme existant pour le mettre sur l'autre noeud avec une carte graphique amd 100-c44971-00 pour avoir un noeud xeon de travail et un noeud os et desktop. je maintiens la topologie ram actu … [16 caractères tronqués]

**Tour 7** — le ram est actuellement hors de prix. je t'ai fait évaluer une approche asymétrique, mais c'est déconseillé. Que peut-on faire pour le ram.

**Tour 8** — donc les nouveaux nvme seront sur l'autre cpu pour ne pas réduire le nombre de voies des gpu. La ram reste tel-quelle. la carte amd pour le desktop sera sur le même cpu que les nouveaux nvme à mettre en raid. Quelels sont les autres optimisations à faire ? prépare un document pour ce changement de configuration et la configuration de la carte amd-yeston (6 ports mini-dp) et les nouveaux nvme en ra … [2 caractères tronqués]

**Tour 9** — encore une journée complète avant l'arrivé du nouveau matériel. Exécute pendant 24h les tâches que tu trouves les plus adéquates pour explorer les bénéfices attendus de Drave pour tout type de tâches.

**Tour 10** — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'architecture de Drave — listes d'événements, streaming depuis le disque, répartition entre nœuds — vaut pour CHAQUE famille de tâches disponible sur la machine : langage, génération et latence, contexte long, code, raisonnement, MoE/routage d'experts, multilingue et sémantique, prérempl … [1196 caractères tronqués]

**Tour 11** — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'architecture de Drave — listes d'événements, streaming depuis le disque, répartition entre nœuds — vaut pour CHAQUE famille de tâches disponible sur la machine : langage, génération et latence, contexte long, code, raisonnement, MoE/routage d'experts, multilingue et sémantique, prérempl … [1196 caractères tronqués]

**Tour 12** — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'architecture de Drave — listes d'événements, streaming depuis le disque, répartition entre nœuds — vaut pour CHAQUE famille de tâches disponible sur la machine : langage, génération et latence, contexte long, code, raisonnement, MoE/routage d'experts, multilingue et sémantique, prérempl … [1196 caractères tronqués]

**Tour 13** — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'architecture de Drave — listes d'événements, streaming depuis le disque, répartition entre nœuds — vaut pour CHAQUE famille de tâches disponible sur la machine : langage, génération et latence, contexte long, code, raisonnement, MoE/routage d'experts, multilingue et sémantique, prérempl … [1196 caractères tronqués]

**Tour 14** — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'architecture de Drave — listes d'événements, streaming depuis le disque, répartition entre nœuds — vaut pour CHAQUE famille de tâches disponible sur la machine : langage, génération et latence, contexte long, code, raisonnement, MoE/routage d'experts, multilingue et sémantique, prérempl … [1196 caractères tronqués]

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

⏵ Section RAM ajoutée au document (§12, commit `ffa46da`) — voici la réponse

\## 1. D'abord : 26 Go sont déjà perdus, et ça ne coûte rien à reprendre

Relevé à l'instant : **62 Go de swap, 26 Go utilisés — et le swap est sur le disque dur** (246 Mo/s mesuré). Toute page touchée là coûte des centaines de microsecondes. Le dépôt avait déjà croisé ce fantôme pendant les travaux Kimi-K3 (« VmSwap 28,5 Go » relevé alors que le moteur affirmait « pas de swap »).

`swapoff -a && swapon -a` les ramène en RAM — il y a 103 Go disponibles. Et quand l'array arrive, **le swap va sur le NVMe, jamais sur `sda`**. `vm.swappiness` est déjà à 10 : le réglage n'est pas le problème, le support l'est.

Côté réglages, le reste est déjà propre (gouverneur `performance`, THP `always`, `mmap` par défaut). J'ai quand même mesuré le banc mémoire sous trois placements :

| placement | débit |
|---|---:|
| sans liaison (16 fils) | 20,4 Go/s |
| lié au nœud 0 (10 fils) | 22,4 Go/s (+10 %) |
| **entrelacé sur les deux nœuds** (20 fils) | **23,8 Go/s (+17 %)** |

**Mais** : le même entrelacement donne **−0,9 %** sur une passe réelle (l'A/B du § 7). Le gain de banc ne se transfère pas — c'est exactement la règle du dépôt, et elle joue ici contre l'optimisation gratuite. Le seul levier gratuit qui reste est la **fréquence de l'uncore** (le ring plafonne la bande passante sur Haswell-EP ; MSR `0x620`, non exposé par le noyau ici, il faut `msr-tools` et root).

\## 2. Le substitut de RAM, c'est le disque — et il est déjà commandé

La passe K3 lit **206,58 Gio** dont 57,93 de dense lu une fois. Le dépôt a mesuré que **la page cache ne retient pas ce dense** d'une passe à l'autre (1 516 430 puis 1 522 584 ms). Un array à 7 Go/s lit ces 58 Go en **8 secondes** : le problème disparaît au lieu d'être résolu.

Et le corollaire du programme, qui est le vrai argument : **un modèle routé n'a pas besoin d'être en RAM pour être gros**. Mesuré sur le prototype — 2,3 M poids lus par jeton pour 7,58 M stockés, **3,35× de paramètres pour la même lecture**. Acheter de la RAM pour faire tenir un modèle de 1,5 To sur une machine de 125 Go est perdu d'avance : c'est la définition de la niche du projet.

\## 3. Réduire ce qui *doit* tenir en RAM

Le cache KV est le seul poste qui grandit avec l'usage, et il est déjà chiffré :

| réglage | coût qualité | gain RAM |
|---|---|---|
| KV int8 à 512 jetons | **+1,5 %** de perplexité | 2× |
| KV int8 à 8 192 jetons | **+3,0 %** | 2× |
| KV int4 | +364 % → inutilisable |
… [1303 caractères tronqués]

### Tour 8 — donc les nouveaux nvme seront sur l'autre cpu pour ne pas réduire le nombre de voies des gpu. La ram reste tel-quelle. l … [282 caractères tronqués]

*11 appels d'outils.* Actions notables :

- bash — Check RAID tooling, ECC and kernel
- web_search
- bash — Check I/O queue settings, md modules, amdgpu firmware
- bash — Verify md RAID and GPU driver modules
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/configuration-nvme-raid-amd.md`
- bash — Verify missing storage tools
- bash — Check tools by full path, not PATH
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/configuration-nvme-raid-amd.md`
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/configuration-nvme-raid-amd.md`
- bash — Check section 5 numbering for the lspci reference
- bash — Commit the reconfiguration document

**Synthèse produite :**

⏵ Document livré (`docs/configuration-nvme-raid-amd.md`, commit `1353c8e`) — voici l'essentiel

\## Le plan tient : les GPU gardent leurs x16

36 voies sur 40 utilisées sur le nœud 0 (2 GPU x16 + NVMe système x4). En mettant l'array sur le CPU 1, les Quadro **restent en x16** — c'est le bon arbitrage, puisque les faire tomber en x8 coûte la moitié de la bande passante hôte (6,5 Go/s mesuré). Le prix à payer : **6 à 8 Go/s traverseront le QPI**, soit la moitié de ce qu'il écoule. Les mesures du dépôt donnent 3-4 % de pénalité pour le traverser, donc le pari est raisonnable — mais c'est un pari, et le § 7 dit comment le vérifier (trois placements de fils à comparer).

\## Les vérifications à faire **avant** de démonter

1. **Bifurcation `x4x4x4x4`** sur le slot, et qu'il est bien câblé au **CPU 1** — derrière le PCH c'est du x4 Gen2 partagé, ~2 Go/s pour les quatre SSD, et tout le bénéfice part.
2. **`Above 4G Decoding`**, **ASPM désactivé** sur les slots NVMe, **affichage primaire = AMD**.
3. **La carte AMD dans un slot x4 ou x8**, pas x16 : elle n'en a pas besoin, et chaque voie laissée libre va aux SSD.

\## Le RAID

RAID0 `mdadm` (les poids se retéléchargent), `--chunk=512K`, `--assume-clean`, XFS, `noatime`, `fstrim.timer`, `mdadm.conf` + `dracut -f`. Attendu : **~2 Go/s par P320, 6-7 Go/s sur `md0`** (plafonné par le lien x16 Gen3, pas par les disques). Si `md0` plafonne à 2 Go/s → la bifurcation n'est pas active : `current_link_width` le dira. **Deux pièges** : les P320 sont **DRAM-less** (l'écriture soutenue s'effondre après le cache SLC — télécharger les gros modèles un par un), et **pas de swap sur le RAID0** (une panne de SSD corromprait la mémoire paginée).

\## La carte Yeston 6 mini-DP

C'est très probablement une **R7 350** (GCN 1.0, Southern Islands). Le noyau la pilote avec **`radeon` par défaut** — rien à faire. Pour `amdgpu` : `amdgpu.si_support=1 radeon.si_support=0`. **Attention** : `cik_support` concerne Sea Islands (Bonaire/Hawaii), pas cette carte — les confondre donne un écran noir. Le firmware `amdgpu/` est déjà en place, et les deux modules aussi.

**Le point qui annule tout si on le rate** : vérifier que X ne prend pas les Quadro (`xrandr --listproviders` → un seul fournisseur ; `nvidia-smi` → aucun processus). Si elles apparaissent, forcer le `BusID` de l'AMD dans `xorg.conf.d`. Et pour les six écrans : les adaptateurs mini-DP→HDMI/DVI doivent être **actifs** sauf si la sortie émet du DP++.

\## Les autres optimisations, par ordre de 
… [1255 caractères tronqués]

### Tour 9 — encore une journée complète avant l'arrivé du nouveau matériel. Exécute pendant 24h les tâches que tu trouves les plus a … [80 caractères tronqués]

*24 appels d'outils.* Actions notables :

- bash — Inventory runnable models
- bash — Inventory corpora and traces
- bash — Verify big model paths and free space
- bash — Check speculative decoding support
- bash — Check time tool, tokenizer and a second model
- bash — Find KV and sparsity CLI flags
- bash — Find KV precision flag
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/campagne-benefices.sh`
- bash — Launch the scaled training pairs on both GPUs
- bash — Smoke-test campaign steps
- bash — Measure dense/push baselines before the sweep
- bash — Verify the tokenizer trap
- bash — Fix the tokenizer trap in the campaign
- bash — Launch the full 24h campaign queue
- … et 9 autres

**Synthèse produite :**

⏵ Campagne 24 h lancée : file de mesures + deux paires d'entraînement en parallèle

\## Ce qui tourne maintenant, et jusqu'à demain

**1. La file de mesures** (`tools/campagne-benefices.sh`, commit `596de74`) — neuf étapes, ~4 à 8 h, journal dans `/tmp/campagne24/journal.txt` :

| étape | ce qu'elle mesure |
|---|---|
| `grille` | **6 modèles, 0,5 B → gpt-oss-120b** : perplexité, RSS, octets lus, débit — le HDD et le NVMe à l'œuvre |
| `parcimonie` | 12 réglages × {dense, listes} : le coût suit-il l'activité sur un VRAI modèle ? |
| `contexte` | ctx 512 → 8 192 : PPL, cache KV choisi, mémoire |
| `lot` | `--lot` 1 → 64 : le seul levier qui multiplie un débit de disque |
| `routage` | MoE 30B-A3B : experts réveillés, volume à router |
| `semantique` | traces UDHR **avec et sans** l'échelle corrigée |
| `noyau` | bande passante, push/pull par densité |
| `repartition` | deux nœuds, porte du modèle entraîné |
| `portes` | non-régression |

**2. Deux paires d'entraînement** sur les deux GPU, à **lecture égale** — pour voir si l'avantage du routage tient à l'échelle :

| GPU | paire | lectures/jeton/couche |
|---|---|---|
| 0 | dense dim 256 (3,2 M) vs **routé 8 experts** (~10 M) | 0,85 M |
| 1 | dense dim 384 (7,2 M) vs **routé 16 experts** (~40 M) | 1,92 M |

Déjà à 8 000 pas, val **2,12-2,16 bits/octet**.

**3. Un batch 2 enchaîné automatiquement** (`batch2.sh`) pour la question que je trouve la plus intéressante de la journée : **le bénéfice événementiel dépend-il de la tâche ?** Même modèle, quatre corpus — prose anglaise, français, code, multilingue — et pour chacun, densité d'activation en dense et en listes. Plus chaque modèle sur sa tâche *et* sur l'autre (codestral-22B sur du code et sur de la prose), et la carte de latence réseau.

\## Deux trouvailles avant même de commencer

**Le piège du tokenizer.** `data/wikitext2_test.txt.ids` vient d'un **autre** tokenizer que Qwen2.5 (`201,438,10498…` contre `198,284,8397…`). Sur les mêmes octets :

| identifiants | perplexité (256 jetons, ctx 512) |
|---|---:|
| ceux du dépôt | **7 710,72** |
| tokenisés par le modèle | **17,43** |

Toute la campagne serait partie d'un chiffre faux. La règle est maintenant dans le script : **chaque modèle tokenise son propre corpus**.

**Deux manques, consignés comme manques.** `bge-m3` (embeddings, BERT 24 couches) est lisible en en-tête mais **inexécutable** — le moteur exige `blk.0.attn_norm.weight` et une attention causale : la famille « recherche/embeddings » n'est pas co
… [528 caractères tronqués]

### Tour 10 — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'archite … [1476 caractères tronqués]

*34 appels d'outils.* Actions notables :

- bash — Check campaign and training status
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/campagne_synthese.py`
- bash — Test the synthesis parser on current logs
- bash — Inspect time -v output format
- bash — Debug the time -v capture
- bash — List campaign directory
- bash — Inspect the 14B run and time output
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/campagne_synthese.py`
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/campagne_synthese.py`
- bash — Verify the fixed synthesis parser
- bash — Check HuggingFace network access and cache
- bash — Download a 1.5B target model for the speculative test
- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/speculatif.py`
- bash — Test the speculative acceptance script
- … et 20 autres

**Synthèse produite :**

⏵ Point de mi-campagne : deux résultats solides, et la file continue

\## Ce que la campagne a déjà établi (21 h 45, 25 min après le départ)

**1. Le décodage spéculatif naïf vaut ×1,2 — mesuré avant d'écrire une ligne de moteur.**

`tools/speculatif.py` : brouillon Qwen2.5-0.5B, cible Qwen2.5-1.5B (même tokenizer), 40 préfixes, k = 8.

| | |
|---|---:|
| acceptation moyenne | **3,35 jetons sur 8 (41,9 %)** |
| médiane · min · max | 3 · 0 · 8 |
| au moins 1 / 2 / 3 / 4 acceptés | 68 % · 60 % · 52 % · 42 % |
| gain si le brouillon coûte 0,25× / **0,33×** / 0,50× la cible | ×1,45 · **×1,20** · ×0,87 |

Sur cette machine, bornée par la bande passante mémoire, un 0,5 B coûte ~1/3 d'un 1,5 B par pas : **×1,20**, là où la feuille de route attendait ×1,58. Un brouillon **générique** ne paie pas — il faut un brouillon aligné (distillé, ou une tête Eagle3 qui consomme les états cachés de la cible), donc un chantier d'entraînement, pas une option de moteur.

**2. La perplexité n'est comparable qu'à tokenizer égal — et la taille ne dit pas la qualité.**

Trois modèles de la grille partagent **exactement** le même tokenizer (mêmes premiers jetons `198,284,8397,…`) :

| modèle | perplexité | **bits/octet** | tok/s | RSS | lus |
|---|---:|---:|---:|---:|---:|
| Qwen2.5-0.5B Q8 | 17,43 | **0,983** | 28,7 | 1,28 Go | 0 |
| r1-distill-1.5B Q4 | **47,14** | **1,326** | 9,5 | 4,76 Go | 1,04 Go |
| r1-distill-14B Q4 | 14,30 | **0,915** | 0,5 | 39,8 Go | 8,71 Go |

**Le 1.5B est 2,7× pire que le 0.5B** : un distillat de raisonnement est mauvais en langue pure. Et codestral (tokenizer Mistral, 32 768 entrées) découpe le même texte en **288 554** jetons contre 85 626 : sa perplexité ne se lit pas sur la même échelle, d'où la colonne **bits/octet** que j'ai ajoutée au dépouillement.

\## Ce qui tourne

- **La file** : grille (codestral-22B en cours, puis Qwen3-30B-A3B, puis gpt-oss-120b depuis le disque dur), puis parcimonie, contexte, lots, routage, sémantique, noyau, répartition, portes.
- **Batch 2 enchaîné** : la densité d'activation dépend-elle de la **tâche** (prose, français, code, multilingue) ?
- **Batch 3 enchaîné** : l'aiguille dans la botte de foin — la perplexité moyenne ne dit pas si la mémoire tient à 4 000 jetons.
- **Les entraînements** : `d256 dense` **terminé** (val 1,9307 bits/octet), le routé 8 experts suit ; `d384` à 32 000/40 000. La chaîne export → porte → mesure moteur → répartition à deux nœuds est armée pour se déclencher dès qu'ils finissent.
- **Deux ma
… [291 caractères tronqués]

### Tour 11 — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'archite … [1476 caractères tronqués]

*23 appels d'outils.* Actions notables :

- bash — Collect campaign results so far
- bash — Locate the training loop for distillation
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/entrainer_moteur.py`
- bash — Show the loss computation block
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/entrainer_moteur.py`
- bash — Add distillation CLI options and validate syntax
- bash — Smoke-test distillation training
- bash — Fix KL normalization and retest
- bash — Chain the distillation experiment
- bash — Check campaign and training progress
- bash — Verify the semantic tool CLI before its campaign step
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-campagne-benefices.md`
- bash — Commit distillation support and the state of the art
- bash — Verify commit message and progress
- … et 9 autres

**Synthèse produite :**

⏵ Mi-parcours : deux modèles entraînés passent la porte, la nuit est armée

\## Ce qui a atterri depuis le dernier point

**Les modèles entraînés passent la porte du moteur, automatiquement.** J'ai armé une chaîne qui exporte, calcule la référence PyTorch **sur les mêmes poids quantifiés**, passe la porte de logits, puis mesure dans le moteur :

| modèle | val (bits/octet) | PPL moteur | paires/jeton | événements/jeton | tok/s | porte |
|---|---:|---:|---:|---:|---:|---|
| `m5_d256_dense` (3,2 M) | 2,007 | **5,3973** | 3,2 M | 732,9 M | 438,3 | ✅ |
| `m5_d384_dense` (7,2 M) | 1,919 | **5,3719** | 7,2 M | 1 648,5 M | 240,2 | ✅ |

**Le rendement décroît vite** : 2,25× plus de paramètres lus n'apporte que **0,5 %** de perplexité et coûte **1,8× de débit**. C'est exactement l'argument du modèle qui *stocke* plus sans *lire* plus — ce que les deux routés de la même paire vont trancher.

Et j'ai consigné une mise en garde qui évite une erreur facile : la colonne « val » (16 000 jetons répartis) et la colonne « PPL moteur » (les 256 premiers octets) **ne mesurent pas la même tranche de texte** — 34 % d'écart systématique, qui n'est pas un défaut du moteur.

**La distillation est implémentée** — le levier que l'inventaire du dépôt notait « mentionné, jamais réalisé ». L'élève creux imite la distribution entière d'un dense gelé, pas seulement son argmax. Piège corrigé au passage : `kl_div(reduction="batchmean")` divise par la taille du **lot**, pas par le nombre de jetons — sur des logits (lot, séquence, vocabulaire) la KL sortait **128 fois trop grande** (perte 622 mesurée, contre ~7 après correction).

\## La nuit est armée

- **GPU 0** : distillation du routé dim 256 (enseignant = dense dim 384) → puis **dim 512 dense** → puis **dim 512 routé, 16 experts**.
- **GPU 1** : **dim 384 routé distillé** — le témoin non distillé existe déjà, seul le terme de KL change.
- **CPU/disque** : la file de campagne continue (codestral-22B en cours, puis Qwen3-30B-A3B, puis **gpt-oss-120b depuis le disque dur**), puis batch 2 (densité par tâche), batch 3 (aiguille dans la botte de foin), et l'export continu à chaque modèle.

Tout est commité (`d8e1311`), et les journaux sont horodatés avec la charge de fond — parce qu'elle a déjà atteint 47 pendant la passe du 14B, et qu'un temps mesuré sous cette charge ne se compare pas à un temps mesuré sous charge 3.

### Tour 12 — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'archite … [1476 caractères tronqués]

*13 appels d'outils.* Actions notables :

- bash — Check campaign and training state
- bash — Add the generation and task-quality batch
- bash — Check the default lot for prefill
- bash — Find the default lot value
- bash — Measure dense vs push on our trained models
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-campagne-benefices.md`
- bash — Commit the dense-vs-push measurement
- bash — Chain the batch-size sweep on the 30B MoE
- bash — Fix the batch 5 waiter to wait for a real end marker
- bash — List waiter PIDs only
- bash — Rewrite and launch the fixed waiter
- bash — Fix all waiters to use end markers
- bash — Final state check for this round

**Synthèse produite :**

⏵ Chaînage corrigé, et une réponse nette sur « pour quel type de tâche »

\## Ce que ce round a établi

**Le chemin par listes coûte 1,8 à 2,1× sur nos propres modèles — et c'est la réponse.** Mêmes jetons, mêmes 8 fils :

| modèle | dense | listes | densité |
|---|---:|---:|---:|
| `m5_d256_dense` (3,2 M) | **787,2 tok/s** | 442,3 tok/s | 2,874 M événements / 3,2 M paires ≈ **90 %** |
| `m5_d384_dense` (7,2 M) | **528,2 tok/s** | 255,0 tok/s | 6,465 M / 7,2 M ≈ **90 %** |

La densité d'activation vaut **90 %**, très au-dessus du croisement mesuré de 22 %. Autrement dit : **sur un modèle de langue ordinaire, l'architecture par listes est un coût, pas un bénéfice.** C'est la réponse la plus directe à « pour quel type de tâche » — et c'est précisément ce que la branche « parcimonie entraînée » cherche à changer. (J'ai aussi corrigé une étiquette trompeuse dans le rapport : la colonne « événements » portait le total de la fenêtre, pas le compte par jeton.)

**Un bug de chaînage trouvé et corrigé avant qu'il ne fausse la nuit.** Mes quatre « enchaîneurs » attendaient la fin d'un script avec `pgrep` — or `pgrep` sur un script **pas encore lancé** rend la main immédiatement : le batch 5 serait parti en parallèle de la campagne, deux gros modèles lus en même temps, et des temps qui ne mesurent plus rien. Ils attendent maintenant un **marqueur de fin** écrit dans le journal.

\## La file, désormais complète

1. **Campagne** (en cours : codestral-22B, puis Qwen3-30B-A3B, puis **gpt-oss-120b depuis le disque dur**) ;
2. **batch 2** — la densité d'activation dépend-elle de la **tâche** (prose, français, code, multilingue) ?
3. **batch 3** — l'aiguille dans la botte de foin : la perplexité moyenne ne dit pas si la mémoire tient ;
4. **batch 4** *(nouveau)* — la **génération** : TTFT et débit par modèle, quatre tâches (code, traduction, arithmétique, résumé) avec les sorties **verbatim**, et une conversation à trois tours ;
5. **batch 5** *(nouveau)* — le **lot** sur le Qwen3-30B-A3B lu depuis le NVMe, de 1 à 64 : l'axe 1 de la feuille de route, mesuré sur le modèle qui ne tient pas en cache.

Côté GPU : `d256_route` et `d384_route` s'entraînent ; ensuite distillation, dim 512, et l'export continu qui passe déjà la porte pour chaque modèle dès qu'il existe.

### Tour 13 — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'archite … [1476 caractères tronqués]

*9 appels d'outils.* Actions notables :

- write `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/census_routage.py`
- bash — Run the routing census on the trained model
- bash — Fix the hook and run the census
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-campagne-benefices.md`
- bash — Commit the routing census
- bash — Chain the extreme-size model test
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/campagne-benefices.md`
- bash — Commit the campaign plan update
- bash — Round status check

**Synthèse produite :**

⏵ Nouvelle mesure livrée : le recensement du routage, et le cas extrême armé

\## Ce round a produit

**Le recensement du routage** (`tools/census_routage.py`, commit `1e11cc7`) — les trois chiffres qui décident d'un découpage par **experts** plutôt que par plages de couches, mesurés sur `m4_route` (4 couches, 8 experts, top-2, 1 024 jetons) :

| couche | charge max | moyenne | déséquilibre | experts pour 90 % des jetons |
|---|---:|---:|---:|---:|
| 0 | 537 | 256 | **×2,10** | 5 sur 8 |
| 1 | 517 | 256 | ×2,02 | 7 sur 8 |
| 2 | 703 | 256 | **×2,75** | 6 sur 8 |
| 3 | 999 | 256 | **×3,90** | 4 sur 8 |

**Trois conséquences** : le déséquilibre est réel (jusqu'à 3,9× — un partage naïf donnerait un nœud quatre fois plus chargé) ; **on ne peut pas élaguer** (4 à 7 experts sur 8 servent) ; et **le volume à router est négligeable — 847 octets par jeton**, du même ordre que les 848 octets déjà mesurés pour un flux de couche. Ce qui coûte, c'est l'**aller-retour par couche**, pas les octets : répartir par experts multiplie les allers-retours que répartir par couches évite.

**Le cas extrême armé** : batch 6 exécute **DeepSeek-V4.1-Flash Q2 — 365,7 Go sur une machine de 125 Go de RAM** — et mesure les octets lus, la mémoire résidente et le temps. C'est la revendication centrale du projet, et elle méritait son propre chiffre plutôt qu'une extrapolation.

**La chaîne complète est posée** : campagne (codestral-22B en cours, puis Qwen3-30B-A3B, puis gpt-oss-120b depuis le disque dur) → batch 2 (densité par tâche) → batch 3 (aiguille) → batch 4 (génération, quatre tâches verbatim, conversation) → batch 5 (le lot sur le 30B depuis le NVMe) → batch 6 (V4-Flash). Cinq enchaîneurs, chacun attendant un **marqueur de fin** dans le journal — la correction qui évite que deux gros modèles se fassent lire en même temps et que les temps ne mesurent plus rien.

Côté GPU : `d256_route` (12 000/40 000, val 2,075) et `d384_route` (8 000/40 000, val 2,117) s'entraînent ; ensuite distillation, dim 512, et l'export continu. Charge 24, tout tourne.

### Tour 14 — <goal_round> Objective: "Pendant 24 h (et jusqu'à l'arrivée du nouveau matériel), mesurer et documenter ce que l'archite … [1476 caractères tronqués]

*8 appels d'outils.* Actions notables :

- bash — Understand the restricted-head feature
- bash — Read the restricted-head implementation
- bash — Build the label token list for a classification task
- bash — Compare full head vs restricted head
- bash — Measure the restricted head with 64 tokens, interleaved
- bash — Chain the constrained-output batch
- edit `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-campagne-benefices.md`
- bash — Commit the constrained-output finding

**Synthèse produite :**

⏵ Famille de tâches non couverte : les sorties contraintes — je mesure `--tete-restreinte`

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
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/entrainer_moteur.py` | 1 | 4 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/porte-reparti-moteur.sh` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/drave-core/src/main.rs` | 0 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/numa-segregation.md` | 1 | 3 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-modele-moteur.md` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/configuration-nvme-raid-amd.md` | 1 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/campagne-benefices.sh` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/docs/campagne-benefices.md` | 1 | 1 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/campagne_synthese.py` | 1 | 2 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/speculatif.py` | 1 | 0 |
| `/tmp/campagne24/batch3_niah.sh` | 1 | 0 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/reports/rapport-campagne-benefices.md` | 1 | 6 |
| `/home/stephane/Data13TB/stephane/GitHub/Qtrinet/tools/census_routage.py` | 1 | 0 |

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
- … et 324 autres

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

15 sorties en erreur ou divergentes. Les premières :

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
- **T9** : === bge-m3 : exécution ? ===  thread 'main' (3706022) panicked at src/gguf.rs:1752:53: tenseur blk.0.attn_norm.weight absent note: run with `RUST_BACKTRACE=1` environment variable to display a backtra

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
- docs/configuration-nvme-raid-amd : préparation de la reconfiguration (array sur le nœud 1, AMD pour le bureau)  Document écrit AVANT l'intervention, pour que ch
- Campagne 24 h : mesurer ce que l'architecture par listes vaut, tâche par tâche  Le dépôt a surtout mesuré un couple (Qwen2.5-0.5B, perplexité). tools/campagne-b
- Campagne : le décodage spéculatif naïf vaut ×1,2 (mesuré), et deux familles manquent  tools/speculatif.py mesure ce qu'il faut savoir AVANT d'écrire le décodage
- Campagne : le décodage spéculatif naïf vaut ×1,2 (mesuré), et deux familles manquent  tools/speculatif.py mesure ce qu'il faut savoir AVANT d'écrire le décodage
- Campagne : la perplexité n'est comparable qu'à tokenizer égal — colonne bits/octet  Trois modèles de la grille partagent EXACTEMENT le même tokenizer (leurs fic
- Distillation implémentée (jamais faite dans ce dépôt) + l'état des lieux par famille de tâches  tools/entrainer_moteur.py accepte --enseignant, --alpha-distill 
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && cat > /tmp/msg.txt <<'MSG' Distillation implémentée (jamais faite dans ce dépôt) + l'état des lieux par fa
- Campagne : les quatre premiers modèles entraînés passent la porte du moteur  Chaîne automatique : chaque dossier d'entraînement est exporté dès qu'il apparaît, 
- Campagne : le chemin par listes coûte 1,8 à 2,1x sur nos propres modèles, et c'est la réponse  Mesuré sur les deux modèles denses entraînés ici, mêmes jetons, m
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 300 git add tools/census_routage.py reports/rapport-campagne-benefices.md && timeout 300 git commi
- Campagne : les cinq batches enchaînés (tâche, mémoire, génération, lot, cas extrême)  Le plan porte maintenant la file complète : après les neuf étapes viennent
- cd /home/stephane/Data13TB/stephane/GitHub/Qtrinet && timeout 300 git add reports/rapport-campagne-benefices.md && timeout 300 git commit -q -F - <<'MSG' Les tâ

