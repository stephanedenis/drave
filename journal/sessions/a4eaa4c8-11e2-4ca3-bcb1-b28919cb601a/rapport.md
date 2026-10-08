# Session a4eaa4c8 — Tu travailles dans le dépôt

| | |
|---|---|
| Identifiant | `a4eaa4c8-11e2-4ca3-bcb1-b28919cb601a` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-10-08 09:18 |
| Durée | 0.0 h |
| Tours | 1 |
| Messages | 28 |
| Appels d'outils | 38 |
| Fichiers touchés | 0 |
| Commandes | 22 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (moteur d'inférence Rust « Drave », drave-core/). LECTURE SEULE STRICTE : ne modifie aucun fichier, ne compile pas, ne lance aucun test ni binaire.  Objectif : inventorier la GESTION MÉMOIRE, DISQUE et FILS (exploitation des ressources d'UNE machine), avec chiffres mesurés.  À examiner : - drave-core/src/materiel.rs : déte … [2168 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (moteur d'inférence Rust « Drave », drave-co … [2448 caractères tronqués]

*38 appels d'outils.* Actions notables :

- bash — List repo structure
- grep
- bash — Count lines of source files
- read
- bash — Read main.rs thread selection regions
- bash — Read engine.rs affinity code
- bash — Inspect pinning and Pool::new bounds
- bash — Read expert LRU cache code
- bash — Check report sizes
- bash — Grep architecture report for figures
- bash — Grep keep/resident/prefetch options
- bash — Read expert prefetch and RAM cache code
- bash — Read --materiel plan output
- bash — Grep borrowed slice views
- … et 11 autres

**Synthèse produite :**

Résultat envoyé au parent (`482522d1-…`) : l'inventaire ci-dessus tient en ~28 lignes, avec les trois distinctions demandées (mesuré / déduit / supposé), les chemins et numéros de ligne, et deux constats à retenir — `plan.lecteurs = 16` n'est **pas câblé** (materiel.rs:322, seul usage main.rs:2400) et **aucune porte** ne couvre mmap, disque, éviction ou affinité (tools/portes.sh:63-68 ne teste que les threads par défaut).

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|

### Commandes exécutées (échantillon)

- **T1** List repo structure
- **T1** Count lines of source files
- **T1** Read main.rs thread selection regions
- **T1** Read engine.rs affinity code
- **T1** Inspect pinning and Pool::new bounds
- **T1** Read expert LRU cache code
- **T1** Check report sizes
- **T1** Grep architecture report for figures
- **T1** Grep keep/resident/prefetch options
- **T1** Read expert prefetch and RAM cache code
- **T1** Read --materiel plan output
- **T1** Grep borrowed slice views
- **T1** Read K3 prefetch and dense arena
- **T1** Inspect GGUF open paths
- **T1** Check lecteurs wiring and metadata plan
- **T1** Grep engram probe measurements
- **T1** Grep mmap/page cache in reports
- **T1** Read mmap vs read measurements
- **T1** Read resident cache helper and materiel dispatch
- **T1** Check dense arena swap claim
- **T1** Confirm absent env vars and syscalls
- **T1** Read GPU expert cache budget and stats

## 4. Mesures et résultats marquants

- **T1** `// sur 20 cœurs / 40 threads : 18 threads = 22,6 Go/s, 20 = 18,7 (bruité),`
- **T1** `// 15 = 19,9, 10 = 14,3. Le `× 3/4` d'avant visait à laisser un quart des CPU`
- **T1** `// sursouscription (mesuré : ×1,3 de perte à 40+1 threads sur 40 CPU).`
- **T1** `// tous les cœurs physiques : mesuré, 10 threads rendent 14,3 Go/s contre`
- **T1** `// 22,5 à 20 — le `cpu / 2` laissait 36 % sur la table.`
- **T1** `/// QPI. Au banc : 20,7 Go/s en laissant l'ordonnanceur placer les fils,`
- **T1** `/// **24,7 Go/s** en les liant à un socket.`
- **T1** `/// mémoire**, pas par le calcul : mesuré au banc, 40 threads font 22,8 Go/s et`
- **T1** `/// 256 Ko. S'en servir ne coûte pas grand-chose, mais les compter fait prendre`
- **T1** `/// 30 fils là où 20 suffisent — et les notes du projet relèvent déjà ×1,3 de`
- **T1** `// et le débit s'effondre (mesuré : ×3,3 de perte à 40+1`
- **T1** `/// survivent au-delà (bug trouvé par le banc : divergence au rang 895).`
- **T1** `// Mesuré : lier les seize fils au seul nœud 0 coûte 16 % de débit`
- **T1** `/// Pourquoi un cache et pas un simple déport : un expert pèse 4,4 Mo et`
- **T1** `/// gpt-oss en a 4 608 (36 couches × 128) — 60 Go, la VRAM n'en tient pas le`
- **T1** `13:| **VRAM** (noyau `warp par ligne`) | **84,9 Go/s** | banc GPU, tête de 144,6 Mo en 1,7 ms |`
- **T1** `14:| VRAM (noyau `ligne par fil`) | 41,9 Go/s | même banc, 3,4 ms |`
- **T1** `15:| **RAM** (CPU, 30 fils) | **20,9 Go/s** | même banc, 6,9 ms |`
- **T1** `16:| **NVMe**, aléatoire, blocs 4 Mo | 5,5 Go/s | mesuré, cache chaud |`
- **T1** `17:| **PCIe** 3.0 ×16 | ~12 Go/s | théorique 15,75 ; le lien monte à gen 3 sous charge |`
- **T1** `30:| tête de sortie | 1,32 | Q4_K | **oui** | 63,2 ms | **15,5 ms** |`
- **T1** `31:| **attention MLA** | **5,40** | Q8_0 | **NON** | **258,4 ms** | 63,6 ms |`
- **T1** `32:| embeddings | 1,32 | F16 | **oui** | 63,2 ms | **15,5 ms** |`
- **T1** `33:| experts (top-6 × 40) | 2,39 | IQ2_XXS / Q2_K | **NON** | 114,4 ms | 28,2 ms |`
- **T1** `34:| **total** | **10,43** | | | **499 ms** | **404 ms** |`
- **T1** `36:**L'attention MLA est le premier poste de dépense** (5,40 Go par jeton, 258 ms à`
- **T1** `38:déport actuel ne fait donc gagner que 95 ms sur 499.`
- **T1** `44:| **VRAM** | 30,2 Go | tête 1,32 + attention 5,40 + embeddings 1,32 = **8,0 Go**, puis **22,2 Go d'experts chauds** (2 227) | 84,9 Go/s |`
- **T1** `45:| **RAM** | 102 Go | jusqu'à **10 247 experts** — or 90 % des appels tiennent dans 71 Go | 20,9 Go/s |`
- **T1** `46:| **NVMe** | 828 Go | le reste des experts (~51 Go) + **l'engram mmappé** (203 Go, 0,4 Go de cache) | 5,5 Go/s |`
- **T1** `52:| engram mmappé + 90 % des experts en RAM | 8 + 71 + 0,4 = **79 Go** | confortable |`
- **T1** `78:| 1 | **attention MLA** (Q8_0 : q_a, q_b, kv, output_a, output_b) | 5,40 Go | **−194 ms** |`
- **T1** `79:| 2 | **IQ2_XXS / Q2_K** (experts) | 2,39 Go | −86 ms |`
- **T1** `80:| 3 | rien — déjà là (`charger_tete`, `charger_proj`, Q4_K/Q6_K/Q8_0/MXFP4) | tête + embeddings | −95 ms |`
- **T1** `82:**Cumul : 499 → ~210 ms par jeton** avec les trois premiers, soit **2,4×**. Et`
- **T1** `83:avec les 22 Go d'experts chauds en VRAM en plus, on descend sous les 150 ms.`
- **T1** `111:experts. Le moteur sait déjà le faire (`DRAVE_KV_BITS`, mesuré sur Qwen : +3,0 %`
- **T1** `136:### Le CPU sature à 22 Go/s — et l'hyperthreading n'apporte rien`
- **T1** `168:`cpu × 3/4` = **30 fils**, alors que **20 suffisent** — et les notes du projet`
- **T1** `169:mentionnent déjà ×1,3 de perte à 40+1 fils. Passer à `cœurs physiques` libère`
- **T1** `175:12,6 Go/s**. Un facteur 1,07 — pas de quoi écrire une politique de placement.`
- **T1** `183:Vérifié sur 50,5 Go (395 fichiers, parcours complet du disque) : **3,42 Go/s à un`
- **T1** `186:**Le NVMe parallélisé (31 Go/s) est plus rapide que la RAM (22 Go/s).**`
- **T1** `189:jeton passent de **435 ms** (lecture séquentielle à 5,5) à **77 ms** (16 lecteurs`
- **T1** `202:| cache de 90 % en RAM + NVMe séquentiel | 0,24 Go | 44 ms + calcul |`
- **T1** `203:| **cache de 25 % + NVMe parallèle** | **1,79 Go** | **58 ms + calcul** |`
- **T1** `204:| **aucun cache, NVMe parallèle** | **2,39 Go** | **77 ms + calcul** |`
- **T1** `224:| **GPU 0 ↔ GPU 1** | | | **NVLink, 25,78 Go/s** |`
- **T1** `226:**Le NVLink est là, et il vaut 2× le PCIe** (25,78 contre ~12 Go/s réels). CUDA`
- **T1** `239:| banc mémoire (calcul pur) | 13,8 | 14,2 | 15,0 Go/s |`
- **T1** `240:| **lecture NVMe** (8 lecteurs) | 22,41 | 21,45 | 22,57 Go/s |`
- **T1** `263:sature à ~22 Go/s), **mais il rend 27 % quand on n'en a que dix.** C'est le cas`
- **T1** `286:   Buffer), donc de la RAM hôte. Les 31 Go/s mesurés en parallèle en dépendent`
- **T1** `376:**47 Mo de mémoire résidente pour 365,7 Go adressés.** Le mmap ne dépend pas de`
- **T1** `386:**625 Mo/s au mieux** — cinquante fois moins que le NVMe parallélisé.`
- **T1** `393:| lecture d'une couche | 10,9 ms |`
- **T1** `394:| **calcul de la même couche** | **0,6 ms** |`
- **T1** `400:31 Go/s.`
- **T1** `411:  les poids montés. Le coût du **transfert initial** (1 Go ≈ 83 ms à 12 Go/s)`
- **T1** `/// experts distincts, 50 % des lectures dans 394 experts, 31,9 % de réutilisation`
- **T1** `/// (31 jetons) : **145,1 s sans cache, 151,2 s à 4 Go (+4 %), 175,5 s à 32 Go`
- **T1** `/// (+21 %)** — plus le cache est grand, plus il coûte. Le drapeau reste, éteint`
- **T1** `// et diviser par le total donnait 0,38 Mo au lieu de 3,05.`
- **T1** `utilisera 9,95 Mo par expert, valeur de DeepSeek-V4.1");`
- **T1** `drave-core/src/list.rs:483:    /// 256 garantit qu'aucune tranche ne débordé (127 × 32767 × 256 = 1,07e9).`
- **T1** `// dépôt, le NVMe passe de 5,4 à 31 Go/s quand les lectures se`
- **T1** `// couches : 6 min 57 s avec, 2 min 34 s sans — **×0,37**, et 8,5 fois`
- **T1** `// 40** (`Percent of CPU this job got: 99%`), avec 119 Ko lus en 47 s`
- **T1** `/// 1 516 430 ms puis 1 522 584 ms, aucun gain.`
- **T1** `/// entier (mesuré : 4,5 % d'écart et une pente de −0,44 sur la sortie).`
- **T1** `// 5,4 à 31 Go/s quand les lectures se recouvrent.`
- **T1** `// repasserait 4,4 Mo sur le bus à chaque jeton.`
- **T1** `reports/rapport-optimisations-auto.md:104:16 ms par entrée de 264 octets — là, la prélecture aurait de quoi faire, et c'est`
- **T1** `reports/rapport-engram-etat.md:27:| sonde | `--sonder-engram 10000` : **219 à 524 ms**, **2,6 Mo touchés** par table, **120 Mo de RSS** pour 365,7 Go | `reports/rapport-execution-v41.md` |`
- **T1** `reports/rapport-execution-v41.md:29:| sonde engram (`--sonder-engram 10000`) | mmap, 16 lecteurs | table 1 : 10 000 entrées en **524 ms** (2,6 Mo touchés sur 101,4 Go) · table 2 : **219 ms** · RSS max`
- **T1** `reports/rapport-execution-v41.md:90:drave $V --sonder-engram 10000          # 203 Go de tables adressées, 5 Mo touchés`
- **T1** `docs/plan-deepseek41-complet.md:800:> e8m0 = **264 octets**. La sonde (`--sonder-engram 10000`) touche 2,6 Mo par`
- **T1** `reports/rapport-optimisations-auto.md:79:| `madvise(WILLNEED)` après le routage (experts) | 25,73 s contre 25,80 | 0,3 % |`
- **T1** `reports/rapport-optimisations-auto.md:80:| `madvise` sur tout le fichier au chargement | 7,29 s contre 7,47 | −2 % |`
- **T1** `reports/rapport-vitesse-v41.md:51:| **cache RAM des experts** (justifié par une trace : 50 % des lectures dans 394 experts, 31,9 % de réutilisation entre jetons consécutifs) | **plus lent** : passe ct`
- **T1** `docs/roadmap-drave.md:109:| rendre le dense résident | la page cache ne le garde pas (deux passes : 1 516 430 puis 1 522 584 ms) et la copie anonyme swape (VmSwap 28,5 Go) |`
- **T1** `| `madvise(WILLNEED)` après le routage (experts) | 25,73 s contre 25,80 | 0,3 % |`
- **T1** `| `madvise` sur tout le fichier au chargement | 7,29 s contre 7,47 | −2 % |`
- **T1** `20 fils. Le mmap paresseux atteint déjà 2,7 Go/s, proche du débit séquentiel du`
- **T1** `NVMe (2,1 à 5,5 Go/s mesurés).`
- **T1** `16 ms par entrée de 264 octets — là, la prélecture aurait de quoi faire, et c'est`
- **T1** `25,80 sans, soit 0,3 %**. Le modèle de test tient dans le cache RAM, donc les`
- **T1** `fichier. C'est ce qui permet d'ouvrir un GGUF de 365,7 Go avec 47 Mo de mémoire`
- **T1** `/// Les formats IQ (IQ1_S, IQ1_M, IQ2_XXS, IQ3_XXS) portent 30 % des poids de`
- **T1** `| **total** | **1 516 430 ms** | **1 522 584 ms** |`
- **T1** `| un cache d'experts en VRAM pour K3 | mesuré : plafond ×1,41, verdict ×1,09 (29,3 % du trafic seulement) |`
- **T1** `| rendre le dense résident | la page cache ne le garde pas (deux passes : 1 516 430 puis 1 522 584 ms) et la copie anonyme swape (VmSwap 28,5 Go) |`
- **T1** `| **chercher la « dispersion » des lectures** | **réfuté (07/10)** : le disque est occupé 87,6 % avec une file de ~14 requêtes — il débite, il ne cherche pas. Le temps est celui du VOLUME. Reste en re`
- **T1** `PLUS LENT que le cache de pages du noyau (ctx 32 : +4 % à 4 Go, +21 % à 32 Go ; voir \`

