# Session c7e46dba — Tu travailles dans le dépôt

> **Journaux :** [le jour](../../2026-11-18/README.md) · [l'état](../../../docs/pilotage/en-cours.md) · [l'index des sessions](../../README.md#sessions).

| | |
|---|---|
| Identifiant | `c7e46dba-11cb-456b-a3b6-715428927f99` |
| Dossier | `/home/stephane/Data13TB/stephane/GitHub/Qtrinet` |
| Début | 2026-11-18 08:58 |
| Durée | 0.4 h |
| Tours | 1 |
| Messages | 73 |
| Appels d'outils | 102 |
| Fichiers touchés | 1 |
| Commandes | 93 |
| Sous-agents | 0 |
| Commits | 0 |
| Compactages de contexte | 0 |

## 1. Ce qui a été demandé

**Tour 1** — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet Drave, en français).  TÂCHE : une RECONNAISSANCE de la ligne A2.6 (« les experts et la tête » du moteur GGUF), pour que la session coordinatrice décide quoi implémenter. Tu ne modifies AUCUN code du moteur ; tu produis un document.  À lire (dans cet ordre, sans tout charger) : - docs/pilotage/roadmap.md — le progra … [1848 caractères tronqués]

## 2. Déroulé, étape par étape

### Tour 1 — Tu travailles dans le dépôt /home/stephane/Data13TB/stephane/GitHub/Qtrinet (projet Drave, en français).  TÂCHE : une RE … [2128 caractères tronqués]

*102 appels d'outils.* Actions notables :

- bash — Check repo state and recent commits
- grep
- bash — Read roadmap header and program A
- bash — Grep A2.6 across state, backlog and reports
- bash — Read the A2.6 backlog fiche
- bash — Read en-cours A line and expert mentions
- bash — Grep expert/MoE path in model.rs
- bash — Sizes and expert refs in placement/materiel
- read
- bash — List expert-related reports
- bash — Read headers of expert reports
- bash — Find A6.2 backlog fiche and mentions
- bash — Read A2.6 bilan body and A6.2 fiche
- bash — List local models and expert tools
- … et 84 autres

**Synthèse produite :**

⏵ Reconnaissance A2.6 terminée, rapport écrit

**Résumé (A2.6 — experts et tête)**

1. **Existe** : `placement.rs` (253 l., **8 tests**) mais la règle ne décide **que du KV** ; experts et tête sont placés par drapeaux/seuils durs (`SEUIL_GPU` 8 Mio, `DRAVE_GPU_EXPERTS_GO` = VRAM−2 Go, `DRAVE_EXPERTS_RAM`, `materiel::plan` imprimé, jamais appliqué).
2. Le chemin experts est déjà riche : 4 conventions de routage (`model.rs:26-46`), trace/imposition/élagage (`432-480`), `Moe` (`1504-1553`), caches RAM (`1583-1700`) et VRAM MXFP4 seulement (`1983-2100`, garde `8486`), prélecture 8 fils, noyau GPU Q4_K mesuré mais **non branché**.
3. **Manque** : coût « experts » (réutilisation + nb de lecteurs), **refus nommé** (`choisir` retombe sur NVMe en silence), trace du classement et test de reproductibilité, `Precision` tête à perte 0, et **une bande experts** — trois tables contradictoires (3,5 vs 31 Go/s) donnent 313 ou 35 ms pour le même opérateur.
4. **Mesuré ici** : 1,097 Go d'experts/jeton ; `proj+mlp` 194,8 ms à 8 fils (**5,6 Go/s**), 188,8 à 16 (saturation), 279,1 à 4 ; cache RAM 567,9 ms et tampons 362,8 ms (plus lents) ; PPL 799,8557 invariante.
5. **Bonus** : tête Q8_0 en VRAM → PPL **56,7642 = 56,7642**, tête **7,43 → 1,80 ms/jeton** (÷4,1), contrôle `DRAVE_GPU=0` = 7,75 ms.
6. **Prochaine expérience** : bande experts au `--limit 32` sur 4/8/16 fils, contrôles « cache RAM et tampons plus lents » + « PPL 37,2013 invariante » ; attendu 195 ms à 8 fils = **un lecteur**, pas 31 Go/s.
7. **Risque** : ≈ 200 lignes (3 fichiers) ; le risque est le chemin de chargement et le défaut → opt-in `DRAVE_PERTE_MAX`, portes `flux`/`pont`/`coupe`, `porte-echange-experts`, `cargo test placement`.

**Rapport** : `reports/rapport-a2.6-reconnaissance.md` — non committé, aucun autre fichier modifié.

## 3. Travail accompli

### Fichiers créés ou modifiés

| Fichier | Écritures | Éditions |
|---|---|---|
| `reports/rapport-a2.6-reconnaissance.md` | 1 | 0 |

### Commandes exécutées (échantillon)

- **T1** Check repo state and recent commits
- **T1** Read roadmap header and program A
- **T1** Grep A2.6 across state, backlog and reports
- **T1** Read the A2.6 backlog fiche
- **T1** Read en-cours A line and expert mentions
- **T1** Grep expert/MoE path in model.rs
- **T1** Sizes and expert refs in placement/materiel
- **T1** List expert-related reports
- **T1** Read headers of expert reports
- **T1** Find A6.2 backlog fiche and mentions
- **T1** Read A2.6 bilan body and A6.2 fiche
- **T1** List local models and expert tools
- **T1** Locate the local MoE model file
- **T1** Read etat-a A2.6 section
- **T1** Verify MoE file, GPU, RAM, cores
- **T1** Map expert code paths with line numbers
- **T1** Find expert placement env vars usage
- **T1** Read materiel.rs plan function
- **T1** Read RAM expert cache doc and behaviour
- **T1** Read cache setup at model load
- **T1** Find head placement flags and code
- **T1** Read head/rule placement reports
- **T1** Read head GPU placement code
- **T1** Find head-on-GPU measurements
- **T1** List all placement rule call sites
- **T1** Check crate layout for placement module
- **T1** Find source of RAM cache timings
- **T1** Read expert gate scripts
- **T1** Inventory local GGUF models
- **T1** Read VRAM expert cache report body
- **T1** Find VRAM expert cache experiments
- **T1** Read CacheExperts format support
- **T1** Read VRAM transfer report and coordination note
- **T1** Read coordination A report start
- **T1** Read coordination A report recommendations
- **T1** Check head GPU flags measurements
- **T1** Read expert measurement tools
- **T1** Check binary and token-id fixtures
- **T1** Check GPU idle state and lot measurement script
- **T1** Read prefill-by-experts timings
- … et 53 autres

## 4. Mesures et résultats marquants

- **T1** `18d49ce7 PROFILS SUR CINQ MODÈLES : BLOQUE ±0,04 % (LE CONTRAT NE BIAISE PAS) · FLOU +1,1 À +7,0 % (TOUJOURS UNE PERTE) · COURT −12,1 À +4,6 % (LE SENS DÉPEND DU MODÈLE)`
- **T1** `| **A — le moteur** | formats, placement, transport, [rejeu](../theorie/glossaire/entrees/rejeu.md), matériels, ordonnanceur | ✅ A1–A8 ; **A3.4, A5.4 bloqués** ; **A6.2 libre** (MoE local 18 Go) ; A2.`
- **T1** `| **R — le lecteur** | document, politique de [lecture](../theorie/glossaire/entrees/lecture.md), fenêtre, mémoire, restitution | ✅ R0.1–R0.3 **mesurés** ; **R0.4 et R0.5 closes (négatifs nommés)** ; `
- **T1** `| **S — les structures** | coloration, rôles, validation humaine, banque d'interprétations | ✅ **v7** : **61/61** types, **144/144** rôles, **56 tests** ; **19/19 verdicts `/paragraphes`** (11 accepté`
- **T1** `| **L — le bloc langue** | surface, heuristique CPU + neuronal, [contrat](../theorie/glossaire/entrees/contrat.md), cascade, pragmatique | 🔬 **R0.7** : 9 niveaux, **398 langues à 0,9687**, script 1,00`
- **T1** `| **D — les données** | inventaire, corpus 10 langues, texte intégral, PDF/[OCR](../theorie/glossaire/entrees/ocr.md), documents, genres | ✅ inventaire ; **10 corpus texte intégral** (20,53 M art., 67`
- **T1** `**État au 15/11 (nuit).** Semaine 2 close ; tag `semaine-2-2026-11-20` sur `73edb3dd` ; [rapport](../../reports/rapport-semaine-2.md). **État au 14/11 07 h 10.** B13 : **POS 86,25 %**, **F1 0,7902**, `
- **T1** `**J7.1** sépare la **sœur** de la **famille lointaine** : sur 532 textes Panini (445 langues, 1948), le top-1 est de la même famille **66,1 %** (hasard 10,3 %) et de la même branche **26,1 %** (hasard`
- **T1** `reports/rapport-a26-lot-disque.md:46:- Le prochain pas d'A2.6 reste les **experts et la tête** ; le placement KV (×1,93 / ×5,8 à 8 k)`
- **T1** `reports/rapport-etat-a.md:44:| **A2** placement machine, KV, top-k, ordonnanceur | ✅ / ⚠️ **A2.6 partiel** | A1 | KV ×**1,93** préremplissage / ×**5,8** attention à 8 k ; KV paginé 968 → **13,2 ms** ;`
- **T1** `reports/rapport-etat-a.md:50:| **A8** ordonnanceur place **et** perte | ✅ **opt-in** | A2.6, A8.0 | **19 portes PPL épinglées** (audit A8.0), **3** avec régime 1 % dual ; le défaut déplace de **−5,9 %`
- **T1** `reports/rapport-etat-a.md:60:| **A2.6** | **partiel, libre (P2)** | A2 acquis ; **pas** A6.2 pour les experts ; tête décidée | KV ×1,93/×5,8 ; lot **503/502 Mio**, **24,0 → 30,5 tok/s** (+27 %), PPL *`
- **T1** `reports/rapport-etat-a.md:183:- **Quoi** : A2.6 → « partiel, P2 ; tête refusée (décision, +10 % historique, pas de run courant) ;`
- **T1** `**où ça tient**. Le **KV l'applique** : à 8 k, **×1,93 / ×5,8**`
- **T1** `puis **revertée** : le 4 bits y coûte **+10 % de PPL** — la place n'est pas la qualité.`
- **T1** `- forcer la tête en 4 bits : la PPL doit **dégrader** (+10 %) — c'est le refus ;`
- **T1** `2. ✅ la tête essayée (refusée : +10 % de PPL) ;`
- **T1** `| **B — l'intelligence** | **B13** | **B13 : 183/183, F1 0,7902, 238/239** ; le produit installable (roue, quickstart) ; le tagger 95,75 % ; D1–E2 ; le natif (le banc, la numpy) | **le palier 1** (le `
- **T1** `- **A5.4** : 4 cartes + ring 40G (17/11) ; **P1 tranché** : la dispersion GPU **29,37 G év/s** bat la projection FPGA (19,3) → le kernel GPU.`
- **T1** `116:    // (une couche MoE = 1 366 ms/jeton, et 93 couches en f32 demanderaient`
- **T1** `drave-core/src/materiel.rs:387:46 % de l'empreinte", experts_go, pour_ram, 100.0 * part));`
- **T1** `drave-core/src/materiel.rs:409:        // Taux de succès du cache d'experts : mesuré, 25 % de l'empreinte sert`
- **T1** `| KV en VRAM | ✅ mesuré | ×1,93 au préremplissage 8 k, ×5,8 sur l’attention |`
- **T1** `| tête 4 bits | ❌ refusée | +10 % de PPL ; `choisir_avec_perte` la refuse à 5 % |`
- **T1** `**Réponse courte : non.** ×1,09 prédit, pour un plafond absolu de ×1,41 — contre`
- **T1** `un plafond de ×3,1 pour le chantier du dense, qui est déjà nommé.`
- **T1** `| **experts routés** (16 sur 896) | 25,83 | 29,3 % |`
- **T1** `| experts partagés (2 par couche) | 12,40 | 14,1 % |`
- **T1** `| **dense Q8_0** (attention, KDA, MLA, routage) | 48,56 | **55,1 %** |`
- **T1** `| tête de sortie | 1,30 | 1,5 % |`
- **T1** `| **réutilisation immédiate** (t−1 → t) | 46,9 % | **47,9 %** | **48,8 %** |`
- **T1** `| fenêtre de 2 jetons | 54,7 % | 57,1 % | 60,4 % |`
- **T1** `| fenêtre de 4 | 63,9 % | 68,5 % | 72,9 % |`
- **T1** `> Verdict : **non — et la mesure a d'abord menti.** Le premier essai donnait **×0,81** (une`
- **T1** `> amélioration de 19 % !) en imposant à A le routage de B à la dernière couche. Les contrôles l'ont`
- **T1** `> démonté : **tout** routage différent y fait varier la perplexité de ±20 à 50 %, **le signe dépend`
- **T1** `> du texte** (A : ×0,81 · A2 : ×1,46 · B en sens inverse : ×1,26), et l'ordre « le routage réel fait`
- **T1** `> ×0,94 contre réel ×1,26). Il n'y a **pas** de gain latéral.`
- **T1** `docs/pilotage/roadmap.md:30:| **A — le moteur** | formats, placement, transport, [rejeu](../theorie/glossaire/entrees/rejeu.md), matériels, ordonnanceur | ✅ A1–A8 ; **A3.4, A5.4 bloqués** ; **A6.2 lib`
- **T1** `docs/pilotage/roadmap.md:285:| **A2** | placer sur une machine : [KV](../theorie/glossaire/entrees/kv.md) paginé, [GPU](../theorie/glossaire/entrees/gpu-quadro-rtx-5000-miroir-vram-deport.md), [top-k]`
- **T1** `- `choisir_avec_perte` refuse la tête 4 bits à un budget de 5 % : la place ne suffit pas, la perte`
- **T1** `**testée**. La suite est **A6.2** (bloqué) ou **A8.3a** (épingler le régime 1 %), pas un nouveau`
- **T1** `/dev/nvme0n1p2           828G  123G  705G  15% /`
- **T1** `devtmpfs                  63G  8,0K   63G   1% /dev`
- **T1** `tmpfs                     63G     0   63G   0% /dev/shm`
- **T1** `efivarfs                 256K  140K  112K  56% /sys/firmware/efi/efivars`
- **T1** `tmpfs                     26G  3,8M   26G   1% /run`
- **T1** `none                     1,0M     0  1,0M   0% /run/credentials/systemd-journald.service`
- **T1** `/dev/nvme0n1p2           828G  123G  705G  15% /.snapshots`
- **T1** `/dev/nvme0n1p1           2,0G  1,6G  441M  79% /boot/efi`
- **T1** `/dev/nvme0n1p2           828G  123G  705G  15% /home`
- **T1** `/dev/nvme0n1p2           828G  123G  705G  15% /opt`
- **T1** `/dev/nvme0n1p2           828G  123G  705G  15% /root`
- **T1** `| **A2.6** | **partiel, libre (P2)** | A2 acquis ; **pas** A6.2 pour les experts ; tête décidée | KV ×1,93/×5,8 ; lot **503/502 Mio**, **24,0 → 30,5 tok/s** (+27 %), PPL **15,8452 → 15,8443** (−0,006 `
- **T1** `| **A3.2** | mesurée | A3 | **1 608 octets/flux** à 256 jetons ; **1,5 vs 3,5 ko** (÷2,3) | `bash tools/porte-flux.sh` (modes 2/4) | listes i16, échelles par bloc, indices par écarts, rejouées |`
- **T1** `| **A8.0** | mesurée | A8 | **19 / 33** portes épinglées ; 3 comparatifs, 2 rouges qualifiées, 1 verte sans PPL, 8 sans PPL | `bash tools/porte-flux.sh` ; `bash tools/porte-pont.sh` ; `bash tools/port`
- **T1** `| **A8.3** | mesurée **négative** | A8.0 | défaut **−5,9 % … +19,5 %** ; trois régimes reproductibles | `DRAVE_PERTE_MAX=0.001/1/10 bash tools/porte-flux.sh` | le défaut est **refusé** ; la règle rest`
- **T1** `| **A8.3a** | **fait 3/19** | A8.0 | flux **58,3200 / 62,7357** ; pont **111,8003 / 115,6406** ; coupe variance **8,9 → 2,4 %** | `DRAVE_PERTE_MAX=1 bash tools/porte-flux.sh` (rejoué **exit 0**) | les`
- **T1** `| **A8.3b** | décidé | A8.3a | **61,9920 / 60,8135** (f32) ; **58,3200 / 62,7357** (1 %) ; bascule lot 1 vs ≥2 | `LOT=1` / `LOT=4 bash tools/porte-flux.sh` | le signe bascule avec le **chemin lot**, p`
- **T1** `| **A8.3c** | expliqué | A8.3b | lot **1,90 %** à lui seul ; effet KV **−5,9 %** (jeton) / **+3,2 %** (lot) | `LOT=1/4` | la « non-monotonie » était **deux chemins** |`
- **T1** `| **A8.3d** | expliqué | A8.3c | **1,90 %** à **1** et **8** threads | `THREADS=1/8 LOT=1/4` | ce n'est pas le pool, c'est le **noyau par lots** |`
- **T1** `le KV l'applique ; ×1,93 / ×5,8 à 8 k ; le lot disque est mesuré (503/502 Mio, +27 % tok/s,`
- **T1** `−0,006 % PPL).`
- **T1** `choisie à 5 %. **Ce n'est pas une mesure courante** : le JSON dit « pas de chiffre courant » ; la`
- **T1** `**2 × 16 Go de VRAM** et **125 Go de RAM** ; `rapport-chargement-paresseux.md` le charge en`
- **T1** `- `porte-flux` **rejoué** en 1 % : **exit 0**, modes 0–4, réf. **58,3200 / 62,7357**.`
- **T1** `- `porte-pont` : **111,8003 / 115,6406** ; falaise 448 fibres **+2,81 → +5,88 %**.`
- **T1** `- `porte-coupe` : variance **8,9 → 2,4 %** ; coûts **0,52–17,09 % → 5,88–11,56 %**.`
- **T1** `(règle) et A8.3a (régime 1 %) au HEAD.`
- **T1** `machine a 125 Go de RAM et 2 × 16 Go de VRAM, et trois fiches l'ont fait tourner.`
- **T1** `1596:/// experts distincts, 50 % des lectures dans 394 experts, 31,9 % de réutilisation`
- **T1** `1985:/// Pourquoi un cache et pas un simple déport : un expert pèse 4,4 Mo et`
- **T1** `// Mesuré : 20 cœurs = 22,5 Go/s, 20 cœurs + HT = 18,9 (rien de plus,`
- **T1** `// leurs hyperthreads (+27 %, la latence mémoire est masquée et le L2`
- **T1** `// de 256 Ko est partagé). Trois fils par cœur régresse (15,0).`
- **T1** `bande passante mémoire sature : 20 cœurs = 22,5 Go/s, 20 cœurs + hyperthreads = 18,9",`
- **T1** `// coup : +27 % mesuré à dix cœurs.`
- **T1** `rendent +27 % (14,7 -> 18,7 Go/s) en masquant la latence mémoire",`
- **T1** `// Mesuré : 1 lecteur = 5,4 Go/s, 16 = 31,1. La courbe ne est pas plate`
- **T1** `"lecteurs disque = {} — le NVMe passe de 5,4 Go/s (1 lecteur) à \`
- **T1** `31,1 (16), soit ×6 ; c'est ce qui rend le chargement à la demande viable", lecteurs));`
- **T1** `réserve CUDA et {:.0} pour le commun ; la VRAM lit à 84,9 Go/s contre 22,5 pour la RAM",`
- **T1** `raisons.push("NVLink détecté (25,8 Go/s, 2× le PCIe) : les échanges \`
- **T1** `// Mesuré sur V4.1 : le KV de MLA fait 90,0 Ko par jeton en F16, soit`
- **T1** `l'empreinte) ; le reste se lit à la demande — mesuré, 90 % des appels tiennent dans \`
- **T1** `46 % de l'empreinte", experts_go, pour_ram, 100.0 * part));`
- **T1** `/// experts distincts, 50 % des lectures dans 394 experts, 31,9 % de réutilisation`
- **T1** `/// (31 jetons) : **145,1 s sans cache, 151,2 s à 4 Go (+4 %), 175,5 s à 32 Go`
- **T1** `/// (+21 %)** — plus le cache est grand, plus il coûte. Le drapeau reste, éteint`
- **T1** `// ~1 152 allocations de 0,88 Mo par jeton (et leurs défauts de page).`
- **T1** `// reste. Mesuré : la VRAM lit à 84,9 Go/s contre 22,5 pour la RAM,`
- **T1** `// et un cache de 25 % de l'empreinte sert 80 % des appels.`
- **T1** `// cette machine (110 Mo pour le 0,5 B) — et la tête s'y place sans drapeau.`
- **T1** `// coûte +10 % de perplexité (30,7660 → 33,8230). La règle de PLACE ne dit rien`
- **T1** `// × 3 matrices × 9,95 Mo ≈ 239 Mo).`
- **T1** `PLUS LENT que le cache de pages du noyau (ctx 32 : +4 % à 4 Go, +21 % à 32 Go ; voir \`
- **T1** `reports/rapport-placement-kv-8k.md:10:est le cas type : sa **lecture par jeton** croît linéairement avec le contexte (5 337 jetons × 24 couches × 2 têtes`
- **T1** `reports/rapport-placement-kv-8k.md:44:| VRAM | **84,9 Go/s** | le KV au-delà de ~2-4 k jetons, l'attention, la tête |`
- **T1** `reports/rapport-placement-kv-8k.md:59:33,8230** — **+10 %**. La règle de **place** ne dit rien de la **qualité** : le 4 bits de la tête est un choix de`
- **T1** `reports/rapport-regle-placement-perte.md:25:  **dans le budget de perte** » — un 4 bits de tête (+10 %) serait refusé par le même budget.`
- **T1** ``placement::kv_precision(couche, n_layer, budget_pct)` : l'**int8** si sa perte **mesurée** (A5.3 : **+2,28 %** sur les`
- **T1** `premières couches, **+0,03 %** sur les dernières) tient dans le budget, le **f32** sinon. C'est`
- **T1** `coûte +10 % de PPL) appliquée au KV. **Deux tests** : les 24 couches (l'int8 passe sur 12-23 seulement), le budget`
- **T1** `3 % (il passe partout), le budget 0 % (nulle part).`
- **T1** `| **la règle place + perte (`DRAVE_PERTE_MAX=1`, budget 1 %)** | **30,7286** |`
- **T1** `- Le coût mesuré est de **−0,12 %** (légèrement *mieux* que le f32) — **dans le bruit** des 255 jetons, à ne pas`
- **T1** `**dans le budget de perte** » — un 4 bits de tête (+10 %) serait refusé par le même budget.`
- **T1** ``porte-coupe` est passée de +0,52-17,09 % à 5,9-11,6 % et a **échoué**. *Un changement de défaut qui déplace les`
- **T1** `// rapide que le chemin scalaire Q6_K, qui coûtait 42 % du temps par`
- **T1** `// de 23 à 159 ms. Le noyau lit une ligne par fil, donc des adresses`
- **T1** `// rentable : l'ancien lisait une ligne par fil (23 → 159 ms mesurés).`
- **T1** `// mesurées, la mesure du 24/10 valide cette ligne (×1,93 au prefill).`
- **T1** `reports/rapport-architecture-memoire.md:13:| **VRAM** (noyau `warp par ligne`) | **84,9 Go/s** | banc GPU, tête de 144,6 Mo en 1,7 ms |`
- **T1** `reports/rapport-gpu-tandem-nvlink.md:41:du moteur l'annonce lui-même (« `[tête 4 bits] … 0 Mo` »). Les GPU sont au repos`
- **T1** `reports/rapport-modele-drave.md:41:| **1** | **têtes précoces** : entraîner le 2 M en octets avec 3 têtes ✓ | l'**accord** par profondeur ✓ (aujourd'hui 0 % / 8,3 % ✗) | `n4_dessin_b.py --accord` ✓, ``
- **T1** `reports/rapport-cache-chunker-applique.md:38:| 80 | 157,3 | 151,2 | ×1,0 |`
- **T1** `reports/rapport-vitesse-v41.md:51:| **cache RAM des experts** (justifié par une trace : 50 % des lectures dans 394 experts, 31,9 % de réutilisation entre jetons consécutifs) | **plus lent** : passe ct`
- **T1** `# S'il est faux, les effets mesurés (±20 %) baignent dans un artefact — et c'est arrivé : la`
- **T1** `[still running after 60000ms; moved to background job bash-290]`
- **T1** `| 100 % (impossible) | **×1,41** |`
- … (tronqué)

## 5. Erreurs rencontrées

1 sorties en erreur ou divergentes. Les premières :

- **T1** : #!/bin/bash # toutes-les-portes.sh — LA PASSE COMPLÈTE, et l'instrument qui manquait. # # POURQUOI CETTE PORTE EXISTE. Le 12 octobre, `tools/porte-gain.sh` §9 exigeait un REFUS # (`--attn-window` en r

